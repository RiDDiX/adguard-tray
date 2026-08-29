"""Read per-request activity from adguard-cli's access log.

adguard-cli has no statistics command, no query log command and no API – the
only per-request record it keeps is the access log named by `access_log_file`
in proxy.yaml. Its format is undocumented, so this parser is structural: it
anchors on the parts that carry meaning (the quoted request line, the `…b`
size, the `…ms` duration and the ` -- ` rule separator) and ignores the fields
in between rather than guessing what they mean. Lines it cannot read are
counted, not dropped silently.

Whether a request was blocked is derived from the matched rule using AdGuard's
documented syntax (`@@` marks an exception), not from a column.
"""

import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit

logger = logging.getLogger(__name__)

# The logger prefixes every line: "26.08.2026 21:42:16.791495 "
_TS_RE = re.compile(r"^(\d{2})\.(\d{2})\.(\d{4}) (\d{2}):(\d{2}):(\d{2})\.(\d{1,6})\s+")
_QUOTED_RE = re.compile(r'^"([^"]*)"\s*')
_BYTES_RE = re.compile(r"^(\d+)b$")
_MS_RE = re.compile(r"^(\d+)ms$")
_RULE_SEP = " -- "

# Placeholders adguard-cli writes when no rule matched.
_NO_RULE = {"", "-", "NONE", "none", "null"}

# Reading the whole file would stall the UI on a long-running proxy.
MAX_READ_BYTES = 4 * 1024 * 1024


@dataclass
class Request:
    """One filtered request."""
    when: datetime | None
    url: str
    host: str
    rule: str
    size: int
    duration_ms: int
    raw: str

    @property
    def blocked(self) -> bool:
        return bool(self.rule) and not self.rule.startswith("@@")

    @property
    def allowed_by_rule(self) -> bool:
        return self.rule.startswith("@@")


@dataclass
class Activity:
    """Everything read from one access log."""
    requests: list[Request] = field(default_factory=list)
    unparsed: int = 0
    log_path: Path | None = None
    problem: str = ""

    @property
    def total(self) -> int:
        return len(self.requests)

    @property
    def blocked(self) -> int:
        return sum(1 for r in self.requests if r.blocked)

    @property
    def allowed(self) -> int:
        return self.total - self.blocked

    def top_hosts(self, limit: int = 10, blocked_only: bool = False) -> list[tuple[str, int]]:
        counts: dict[str, int] = {}
        for r in self.requests:
            if blocked_only and not r.blocked:
                continue
            if r.host:
                counts[r.host] = counts.get(r.host, 0) + 1
        return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]

    def top_rules(self, limit: int = 10) -> list[tuple[str, int]]:
        counts: dict[str, int] = {}
        for r in self.requests:
            if r.rule:
                counts[r.rule] = counts.get(r.rule, 0) + 1
        return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]

    def per_hour(self, limit: int = 24) -> list[tuple[datetime, int, int]]:
        """(hour, total, blocked) for the last *limit* hours the log covers.

        Hours without requests are returned as zeros: a quiet hour has to read
        as a gap, not be collapsed away.
        """
        buckets: dict[datetime, list[int]] = {}
        for r in self.requests:
            if not r.when:
                continue
            hour = r.when.replace(minute=0, second=0, microsecond=0)
            slot = buckets.setdefault(hour, [0, 0])
            slot[0] += 1
            if r.blocked:
                slot[1] += 1
        if not buckets:
            return []
        last = max(buckets)
        out = []
        for back in range(max(1, limit) - 1, -1, -1):
            hour = last - timedelta(hours=back)
            total, blocked = buckets.get(hour, [0, 0])
            out.append((hour, total, blocked))
        return out


def data_dir() -> Path:
    """adguard-cli's data directory for the current user."""
    override = os.environ.get("AG_CLI_DATA_PATH")
    if override:
        return Path(override)
    xdg = os.environ.get("XDG_DATA_HOME")
    base = Path(xdg) if xdg else Path.home() / ".local" / "share"
    return base / "adguard-cli"


def access_log_path() -> Path:
    """Where the access log should be, honouring proxy.yaml.

    An absolute `access_log_file` is used as given. A relative name lives in
    the logs directory next to app.log, unless only the data directory has it.
    """
    name = "access.log"
    try:
        from .proxy_config_dialog import _load_yaml
        configured = _load_yaml().get("access_log_file")
        if isinstance(configured, str) and configured.strip():
            name = configured.strip()
    except Exception as exc:                     # config unreadable – use default
        logger.debug("Could not read access_log_file: %s", exc)

    path = Path(name)
    if path.is_absolute():
        return path
    base = data_dir()
    in_logs = base / "logs" / name
    in_root = base / name
    return in_root if (in_root.exists() and not in_logs.exists()) else in_logs


def _host_of(url: str) -> str:
    """Host part of a URL, also for the `CONNECT host:443` form."""
    if "://" in url:
        host = urlsplit(url).hostname or ""
        return host
    head = url.split("/", 1)[0]
    if head.count(":") == 1:
        head = head.split(":", 1)[0]
    return head


def parse_line(line: str) -> Request | None:
    """Turn one access-log line into a Request, or None if it isn't one."""
    match = _TS_RE.match(line)
    when = None
    rest = line
    if match:
        d, mo, y, h, mi, s, frac = match.groups()
        try:
            when = datetime(int(y), int(mo), int(d), int(h), int(mi), int(s),
                            int(frac.ljust(6, "0")))
        except ValueError:
            when = None
        rest = line[match.end():]

    rest = rest.rstrip()
    rule = ""
    if _RULE_SEP in rest:
        rest, rule = rest.rsplit(_RULE_SEP, 1)
        rule = rule.strip()
        if rule in _NO_RULE:
            rule = ""

    quoted = _QUOTED_RE.match(rest)
    if not quoted:
        return None
    request_line = quoted.group(1)
    tail = rest[quoted.end():].split()

    # The two trailing anchors: "<size>b <duration>ms".
    size = duration = -1
    if len(tail) >= 2:
        ms = _MS_RE.match(tail[-1])
        by = _BYTES_RE.match(tail[-2])
        if ms and by:
            duration = int(ms.group(1))
            size = int(by.group(1))
    if size < 0:
        return None

    url = ""
    for token in request_line.split():
        if "://" in token or "." in token or ":" in token:
            url = token
            break
    if not url:
        url = request_line
    return Request(when=when, url=url, host=_host_of(url), rule=rule,
                   size=size, duration_ms=duration, raw=line.rstrip())


def read_activity(max_lines: int = 5000) -> Activity:
    """Read the tail of the access log. Never raises."""
    path = access_log_path()
    result = Activity(log_path=path)
    try:
        size = path.stat().st_size
    except FileNotFoundError:
        result.problem = _missing_problem(path)
        return result
    except OSError as exc:
        result.problem = _permission_problem(path, exc)
        return result

    try:
        with path.open("rb") as fh:
            if size > MAX_READ_BYTES:
                fh.seek(size - MAX_READ_BYTES)
                fh.readline()               # drop the partial first line
            data = fh.read()
    except OSError as exc:
        result.problem = _permission_problem(path, exc)
        return result

    lines = data.decode("utf-8", errors="replace").splitlines()[-max_lines:]
    for line in lines:
        if not line.strip():
            continue
        parsed = parse_line(line)
        if parsed is None:
            result.unparsed += 1
        else:
            result.requests.append(parsed)
    return result


def _missing_problem(path: Path) -> str:
    from .i18n import _t
    return _t(
        "No access log yet ({}). AdGuard writes it once it has filtered "
        "traffic; when it runs as a system service the log belongs to root "
        "and is not readable here.", str(path))


def _permission_problem(path: Path, exc: OSError) -> str:
    from .i18n import _t
    return _t("Cannot read the access log ({}): {}", str(path), exc.strerror or str(exc))
