"""Read per-request activity from adguard-cli's access log.

adguard-cli has no statistics command, no query log command and no API – the
only per-request record it keeps is the access log named by `access_log_file`
in proxy.yaml. The format is undocumented; it was recovered by disassembling
the emitting function, which formats fourteen fields:

    "<app>" <proto> <method> <url> <?> <status> <types> <verdict> <rules>
    <ID=n> <address> <n>b <n>ms -- <rule>

Reading it positionally alone would be reckless – the map came from a binary,
not from documentation, and field 8 is a space-joined flag set, so the token
count varies. So the parser anchors on what cannot move (the quoted first
field, the `…b`/`…ms` suffixes, the ` -- ` separator), then reads the fields
between them only when their own markers hold: a known protocol name, an
`ID=<n>` or `-`, a three-digit status. A field whose marker fails stays empty
instead of being guessed, and the request still counts.

The verdict field says outright whether a request was blocked, whitelisted or
modified. When it is missing or unreadable, blocked/allowed falls back to
AdGuard's rule syntax, where `@@` marks an exception.
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
# The emitter escapes only spaces in this field, so a quote inside it shifts
# every column. Demanding whitespace after the closing quote makes such a line
# fail here instead of producing plausible-looking nonsense.
_QUOTED_RE = re.compile(r'^"([^"]*)"\s+')
_BYTES_RE = re.compile(r"^(\d+)b$")
_MS_RE = re.compile(r"^(\d+)ms$")
_RULE_SEP = " -- "

# Placeholders adguard-cli writes when no rule matched.
_NO_RULE = {"", "-", "NONE", "none", "null"}

# Field 2: the AGPROTO_ enum with its prefix stripped, plus DNS for DNS records.
PROTOCOLS = frozenset({
    "TCP", "UDP", "STUN_TURN", "GQUIC", "TLS", "HTTP1", "HTTP2", "IQUIC",
    "HTTP3", "OTHER", "EOF", "DNS",
})
# Field 8: the filtering verdict. Several flags can be set at once, joined by
# spaces, which is why the fields around it are found by their own markers.
VERDICTS = frozenset({
    "NONE", "BLOCKED", "WHITELISTED", "MODIFIED_CONTENT", "MODIFIED_META",
    "blocked", "allowed", "error",
})
_BLOCKED_FLAGS = frozenset({"BLOCKED", "blocked"})
_ALLOWED_FLAGS = frozenset({"WHITELISTED"})
_MODIFIED_FLAGS = frozenset({"MODIFIED_CONTENT", "MODIFIED_META"})

_METHOD_RE = re.compile(r"^[A-Z]{3,10}$")
_STATUS_RE = re.compile(r"^[1-5]\d\d$")
_FILTER_ID_RE = re.compile(r"^ID=(\d+)$")
_COUNT_RE = re.compile(r"^\d+$")

# Field 1 escapes spaces as "\ "; nothing else is escaped.
_ESCAPED_SPACE = "\\ "

# Reading the whole file would stall the UI on a long-running proxy.
MAX_READ_BYTES = 4 * 1024 * 1024


@dataclass
class Request:
    """One filtered request. Fields that could not be read stay empty."""
    when: datetime | None
    url: str
    host: str
    rule: str
    size: int
    duration_ms: int
    raw: str
    app: str = ""
    protocol: str = ""
    method: str = ""
    status: int = 0
    content_type: str = ""
    verdict: str = ""
    rule_count: int = 0
    filter_id: int = -1

    @property
    def blocked(self) -> bool:
        """The verdict decides; the rule only when there is no verdict."""
        flags = self.verdict.split()
        if flags:
            # A modified request is not a blocked one, even though it matched a
            # rule written in blocking syntax – so the verdict settles it.
            return bool(_BLOCKED_FLAGS.intersection(flags))
        return bool(self.rule) and not self.rule.startswith("@@")

    @property
    def allowed_by_rule(self) -> bool:
        if _ALLOWED_FLAGS.intersection(self.verdict.split()):
            return True
        return self.rule.startswith("@@")

    @property
    def modified(self) -> bool:
        return bool(_MODIFIED_FLAGS.intersection(self.verdict.split()))


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

    @property
    def bytes_total(self) -> int:
        return sum(r.size for r in self.requests if r.size > 0)

    def window(self, hours: int | None) -> "Activity":
        """A copy holding only the last *hours* of requests (None = all).

        The cut is relative to the newest entry in the log, not to the wall
        clock: a log from yesterday would otherwise come out empty.
        """
        if not hours or not self.requests:
            return self
        newest = max((r.when for r in self.requests if r.when), default=None)
        if newest is None:
            return self
        cutoff = newest - timedelta(hours=hours)
        return Activity(
            requests=[r for r in self.requests if r.when is None or r.when >= cutoff],
            unparsed=self.unparsed, log_path=self.log_path, problem=self.problem,
        )

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
    if head.startswith("["):                      # [::1]:443
        return head[1:].split("]", 1)[0]
    if head.count(":") == 1:
        head = head.split(":", 1)[0]
    return head


def _split_rule(body: str) -> tuple[str, str]:
    """Peel the matched rule off the end.

    The format ends in ` -- {}`, so a request that matched nothing leaves the
    line ending in " -- " — with the separator still there and nothing after
    it. Stripping the whole line first would swallow that and make the record
    unreadable, which is why only the line ending is stripped here.
    """
    body = body.rstrip("\r\n")
    if _RULE_SEP in body:
        head, rule = body.rsplit(_RULE_SEP, 1)
        rule = rule.strip()
        return head.rstrip(), "" if rule in _NO_RULE else rule
    if body.rstrip().endswith(" --"):                  # trailing space eaten
        return body.rstrip()[:-3].rstrip(), ""
    return body.rstrip(), ""


def _read_fields(tokens: list[str], request: Request) -> None:
    """Fill the positional fields, but only where their markers hold.

    The six leading fields are counted from the left and the three trailing
    ones from the right, because the verdict between them is a space-joined
    flag set of unpredictable width. Every field is checked against its own
    marker first; one that does not match is left empty rather than guessed,
    so a changed format degrades to fewer columns instead of wrong numbers.
    """
    if len(tokens) < 10:
        return

    left, right = tokens[:6], tokens[-3:]
    # ID=<n> is the strongest marker in the line: without it, trust nothing
    # that depends on counting from the right.
    filter_id = _FILTER_ID_RE.match(right[1])
    if not (filter_id or right[1] == "-") or not _COUNT_RE.match(right[0]):
        return

    if left[0] in PROTOCOLS:
        request.protocol = left[0]
    if left[2] not in ("-", ""):
        request.url = left[2]
        request.host = _host_of(left[2])
    if _METHOD_RE.match(left[1]):
        request.method = left[1]
    if _STATUS_RE.match(left[4]):
        request.status = int(left[4])
    if left[5] not in ("-", ""):
        request.content_type = left[5]

    request.rule_count = int(right[0])
    if filter_id:
        request.filter_id = int(filter_id.group(1))

    middle = tokens[6:-3]
    if middle and all(token in VERDICTS for token in middle):
        request.verdict = " ".join(middle)


def parse_line(line: str) -> Request | None:
    """Turn one access-log line into a Request, or None if it isn't one."""
    match = _TS_RE.match(line)
    if not match:
        # Every record carries the logger's timestamp. Without it this is
        # something else that happens to end in a byte count.
        return None
    d, mo, y, h, mi, s, frac = match.groups()
    try:
        when = datetime(int(y), int(mo), int(d), int(h), int(mi), int(s),
                        int(frac.ljust(6, "0")))
    except ValueError:
        when = None
    rest = line[match.end():]

    rest, rule = _split_rule(rest)

    quoted = _QUOTED_RE.match(rest)
    if not quoted:
        return None
    app = quoted.group(1).replace(_ESCAPED_SPACE, " ")
    tokens = rest[quoted.end():].split()

    # The two trailing anchors: "<size>b <duration>ms".
    size = duration = -1
    if len(tokens) >= 2:
        ms = _MS_RE.match(tokens[-1])
        by = _BYTES_RE.match(tokens[-2])
        if ms and by:
            duration = int(ms.group(1))
            size = int(by.group(1))
    if size < 0:
        return None
    tokens = tokens[:-2]

    # A guess before the fields are validated: only tokens that cannot be the
    # trailing address are considered, and the quoted field is the last
    # resort. _read_fields overrides this with the real column when its
    # markers hold, and an unrecognisable line keeps an empty host rather than
    # inventing one out of an app name.
    candidates = tokens[:-3] if len(tokens) >= 10 else tokens
    url = next((token for token in candidates
                if "://" in token or "." in token or ":" in token), "")
    if not url:
        url = next((part for part in app.split() if "://" in part or "." in part), "")
    request = Request(when=when, url=url, host=_host_of(url), rule=rule,
                      size=size, duration_ms=duration, raw=line.rstrip(), app=app)
    _read_fields(tokens, request)
    return request


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
