"""
AdGuard CLI wrapper.

Real commands (verified against /usr/local/bin/adguard-cli):
  adguard-cli status            – no root required, exit 0 when running
  adguard-cli start/stop/restart – starts/stops proxy (may need root)
  adguard-cli check-update      – updates filters, DNS filters, userscripts,
                                   SafebrowsingV2, CRLite, checks app update
  adguard-cli filters list      – list active filters
  adguard-cli filters list --all – list all available filters
  adguard-cli filters enable/disable <id>  – toggle a filter
  adguard-cli filters install <url>        – add custom filter
  adguard-cli filters remove <id>          – remove filter

Filter list output format (after ANSI strip):
  Group headers:  plain text line (e.g. "Ad blocking", "Privacy")
  Filter lines:   [x] |    ID | Title          YYYY-MM-DD HH:MM:SS
"""

import json
import logging
import re
import subprocess
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from .i18n import _t

_USERSCRIPTS_DIR = Path.home() / ".local" / "share" / "adguard-cli" / "userscripts"

logger = logging.getLogger(__name__)

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
_PORT_RE = re.compile(r"127\.0\.0\.1:(\d+)")
_RUNNING_RE = re.compile(r"\b(is running|has started)\b")
_STOPPED_RE = re.compile(r"\b(is not running|has been stopped)\b")


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


_FAILURE_KEYWORDS = (
    "failed to install",
    "failed to download",
    "failed to remove",
    "failed to enable",
    "failed to disable",
    "no userscripts matching",
    "no filters matching",
    "before filters can be enabled",
)


def _is_cli_failure(*streams: str) -> bool:
    """Detect failure reported in the output (adguard-cli exits 0 on some failures)."""
    lower = " ".join(streams).lower()
    return any(kw in lower for kw in _FAILURE_KEYWORDS)


# Messages end up in labels, menu entries and notifications; a runaway CLI
# must not freeze the GUI while Qt measures a multi-megabyte string. Only
# messages are clipped – parsers always see the full output.
_MAX_OUTPUT = 20_000


def _clip(text: str) -> str:
    return text if len(text) <= _MAX_OUTPUT else text[:_MAX_OUTPUT] + "\n…"


def _valid_url(url: str) -> bool:
    return url.lower().startswith(("http://", "https://"))


def mask_license(raw: str) -> str:
    """`adguard-cli license` output with the e-mail and licence key masked."""
    def _mask_email(m: re.Match) -> str:
        local, domain = m.group(0).rsplit("@", 1)
        return local[0] + "***@" + domain

    out = re.sub(r"[\w.+-]+@[\w.-]+", _mask_email, raw)
    return re.sub(r"(?<=License key: )(\w{4})\w+", r"\1****", out)


class AdGuardStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    NOT_INSTALLED = "not_installed"
    UNKNOWN = "unknown"


@dataclass
class StatusResult:
    status: AdGuardStatus
    message: str = ""
    proxy_port: str = ""
    filtering_enabled: bool = False


def _run(args: list[str], timeout: int = 15, stdin_data: str | None = None) -> tuple[int, str, str]:
    try:
        p = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.PIPE if stdin_data is not None else None,
        )
        try:
            raw_out, raw_err = p.communicate(
                stdin_data.encode("utf-8") if stdin_data is not None else None, timeout=timeout
            )
        except subprocess.TimeoutExpired:
            try:
                p.kill()
            except PermissionError:
                pass    # a root child started by pkexec can't be signalled
            for f in (p.stdin, p.stdout, p.stderr):
                if f:
                    f.close()
            # Reap whenever it exits instead of blocking the caller on it.
            threading.Thread(target=p.wait, daemon=True).start()
            return -2, "", f"Command timed out after {timeout}s"
        # Decode explicitly so a C-locale runtime (systemd unit, cron) doesn't
        # crash on filter titles with umlauts or CJK.
        out = raw_out.decode("utf-8", errors="replace").strip()
        err = raw_err.decode("utf-8", errors="replace").strip()
        return p.returncode, _strip_ansi(out), _strip_ansi(err)
    except FileNotFoundError:
        return -1, "", f"Binary not found: {args[0]}"
    except OSError as exc:
        return -3, "", str(exc)


class AdGuardCLI:
    BINARY = "adguard-cli"

    def __init__(self, binary: str = "") -> None:
        if binary:
            self.BINARY = binary
        # Tray menu and Overview both drive start/stop; one at a time.
        self._action_lock = threading.Lock()
        self._last_status_error = ""

    # ── Version ────────────────────────────────────────────────────────────

    def get_version(self) -> str:
        """Return adguard-cli version string (e.g. '1.3.45'), or empty on error."""
        code, out, _ = _run([self.BINARY, "--version"], timeout=5)
        if code == 0 and out:
            # Output: "AdGuard CLI v1.3.45"
            parts = out.strip().rsplit("v", 1)
            return parts[-1] if len(parts) == 2 else out.strip()
        return ""

    # ── Status ─────────────────────────────────────────────────────────────

    def get_status(self) -> StatusResult:
        code, out, err = _run([self.BINARY, "status"])

        if code == -1:
            return StatusResult(
                AdGuardStatus.NOT_INSTALLED,
                _t(
                    "adguard-cli was not found.\n"
                    "Install via official script or AUR:\n"
                    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
                    "  paru -S adguard-cli-bin"
                ),
            )
        if code < 0:
            return StatusResult(AdGuardStatus.ERROR, err or _t("Unknown error retrieving status"))

        combined = (out + " " + err).lower()

        # Parse proxy port from output
        port_match = _PORT_RE.search(out)
        proxy_port = port_match.group(1) if port_match else ""
        filtering_enabled = "enabled" in combined

        if _RUNNING_RE.search(combined):
            return StatusResult(AdGuardStatus.ACTIVE, out, proxy_port, filtering_enabled)

        if _STOPPED_RE.search(combined):
            # adguard-cli may lack a PID file when managed by systemd → verify
            fallback = self._systemctl_fallback(out)
            if fallback.status == AdGuardStatus.ACTIVE:
                return StatusResult(AdGuardStatus.ACTIVE, out, proxy_port, filtering_enabled)
            return StatusResult(AdGuardStatus.INACTIVE, out, proxy_port, filtering_enabled)

        # Ambiguous output → fallback to systemctl, but keep what we parsed
        logger.debug("Status output ambiguous, checking systemctl: %r", out)
        fallback = self._systemctl_fallback(out)
        if code != 0 and err:
            # e.g. an unreadable proxy.yaml: show it instead of a silent "stopped".
            # A known systemd state stays, the restart guards rely on INACTIVE.
            if err != self._last_status_error:
                logger.warning("adguard-cli status failed (exit %d): %s", code, _clip(err))
            self._last_status_error = err
            status = AdGuardStatus.ERROR if fallback.status == AdGuardStatus.UNKNOWN else fallback.status
            return StatusResult(status, _clip(err), proxy_port, filtering_enabled)
        return StatusResult(fallback.status, out or err, proxy_port, filtering_enabled)

    def _systemctl_fallback(self, original: str) -> StatusResult:
        code, out, _ = _run(["systemctl", "is-active", "adguard-cli"], timeout=5)
        state = out.strip()
        if state == "active":
            return StatusResult(AdGuardStatus.ACTIVE, original)
        if state in ("inactive", "failed", "dead"):
            return StatusResult(AdGuardStatus.INACTIVE, original)
        return StatusResult(AdGuardStatus.UNKNOWN, original)

    # ── Control commands ───────────────────────────────────────────────────

    def _exclusive(self, fn) -> tuple[bool, str]:
        if not self._action_lock.acquire(blocking=False):
            return False, _t("Another action is still running")
        try:
            return fn()
        finally:
            self._action_lock.release()

    def start(self) -> tuple[bool, str]:
        return self._exclusive(self._start)

    def stop(self) -> tuple[bool, str]:
        return self._exclusive(self._stop)

    def restart(self) -> tuple[bool, str]:
        return self._exclusive(self._restart)

    def _start(self) -> tuple[bool, str]:
        ok, msg, first_error = self._privileged_command("start")
        if not ok and "socket busy" in (msg + " " + first_error).lower():
            # Stale socket from a previous unclean stop – kill and retry.
            logger.warning("Socket busy on start, cleaning up stale processes")
            self._force_kill()
            time.sleep(0.5)
            ok, msg, _ = self._privileged_command("start")
        return ok, msg

    def _stop(self) -> tuple[bool, str]:
        ok, msg, _ = self._privileged_command("stop")
        if not ok:
            # e.g. polkit prompt cancelled – don't follow up with a force-kill
            # that would prompt again.
            return ok, msg
        # Verify the service actually stopped – adguard-cli stop can report
        # success while leaving the process alive (stale socket).
        time.sleep(1)
        code, out, err = _run([self.BINARY, "status"])
        cli_says_stopped = code >= 0 and _STOPPED_RE.search((out + " " + err).lower())
        unit_active = _run(["systemctl", "is-active", "adguard-cli"], timeout=5)[1].strip() == "active"
        if unit_active:
            # systemd keeps it alive (the CLI may lack a PID file and report
            # "not running"). Stop the unit instead of pkill-ing root processes.
            logger.info("adguard-cli unit still active after stop, stopping the unit")
            code2, out2, err2 = _run(["pkexec", "systemctl", "stop", "adguard-cli"], timeout=60)
            if code2 == 0:
                return True, _t("AdGuard via systemctl {} ok", "stop")
            if code2 == 126:
                return False, _t("Authentication cancelled")
            return False, _clip(err2 or out2) or _t("Could not stop AdGuard – process may still be running")
        if cli_says_stopped:
            return ok, msg
        if self.get_status().status == AdGuardStatus.ACTIVE:
            logger.warning("stop reported success but service still active, force-killing")
            return self._force_kill()
        return ok, msg

    def _force_kill(self) -> tuple[bool, str]:
        """Kill lingering adguard-cli processes and the root helper.

        First try unprivileged pkill; if the service is still up, retry with
        pkexec since adguard_root_helper runs as root and can't be signalled
        from the user session.
        """
        # pkill -x matches comm, which the kernel cuts to 15 characters.
        for name in ("adguard-cli", "adguard_root_he"):
            code, _, err = _run(["pkill", "-x", name], timeout=5)
            # exit 1 means "no matching process" which is fine here
            if code not in (0, 1):
                logger.warning("pkill %s exit %d: %s", name, code, err)
        time.sleep(0.5)
        if self.get_status().status != AdGuardStatus.ACTIVE:
            logger.info("Force-kill succeeded (user)")
            return True, _t("AdGuard stopped (forced)")

        logger.warning("User-level pkill did not stop service, trying pkexec")
        for name in ("adguard-cli", "adguard_root_he"):
            code, _, err = _run(["pkexec", "pkill", "-x", name], timeout=30)
            if code not in (0, 1):
                logger.warning("pkexec pkill %s exit %d: %s", name, code, err)
        time.sleep(0.5)
        if self.get_status().status != AdGuardStatus.ACTIVE:
            logger.info("Force-kill succeeded (pkexec)")
            return True, _t("AdGuard stopped (forced)")

        logger.error("Force-kill failed, service may still be running")
        return False, _t("Could not stop AdGuard – process may still be running")

    def _restart(self) -> tuple[bool, str]:
        ok, msg, _ = self._privileged_command("restart")
        if not ok:
            return ok, msg
        # `adguard-cli restart` doesn't always start a stopped proxy. Verify
        # and fall back to `start` if the service didn't come up.
        time.sleep(1)
        if self.get_status().status != AdGuardStatus.ACTIVE:
            logger.info("restart left the proxy inactive – calling start")
            return self._start()
        return ok, msg

    def _privileged_command(self, cmd: str) -> tuple[bool, str, str]:
        """
        Try in order:
          1. adguard-cli <cmd>              (no privilege needed if configured)
          2. pkexec adguard-cli <cmd>       (polkit GUI prompt)
          3. pkexec systemctl <cmd> adguard-cli  (fallback via systemd)
        """
        # Attempt 1: direct. Its output is returned alongside the final
        # message: the fallbacks' errors hide the real cause (e.g. "socket busy").
        code, out, err = _run([self.BINARY, cmd])
        first_error = err or out
        if code == 0:
            logger.info("adguard-cli %s succeeded (direct)", cmd)
            return True, _clip(out) or _t("AdGuard {} ok", cmd), first_error
        if code == -1:
            # Binary missing – pkexec would only raise pointless prompts.
            return False, err, first_error

        logger.info("Direct %s failed (exit %d): %s – trying pkexec", cmd, code, err or out)

        # Attempt 2: pkexec adguard-cli
        code2, out2, err2 = _run(["pkexec", self.BINARY, cmd], timeout=60)
        if code2 == 0:
            logger.info("adguard-cli %s succeeded (pkexec)", cmd)
            return True, _clip(out2) or _t("AdGuard {} ok", cmd), first_error

        # pkexec exits 126 when the user dismisses the dialog, 127 when
        # authorization failed or the command could not be run. Surface that
        # directly instead of falling through to systemctl, which would
        # prompt again.
        if code2 == 126:
            logger.info("pkexec authentication cancelled (exit 126)")
            # No first_error: the user said no, so callers must not "recover"
            # by force-killing and prompting again.
            return False, _t("Authentication cancelled"), ""
        if code2 == 127:
            logger.error("pkexec authorization failed (exit 127): %s", err2)
            return False, _t("Authorization failed"), ""
        if code2 == -2:
            # The prompt may still be open; the systemctl fallback would stack a second one.
            logger.error("pkexec adguard-cli %s timed out", cmd)
            return False, err2, ""

        logger.info("pkexec adguard-cli %s failed (exit %d): %s – trying systemctl",
                    cmd, code2, err2 or out2)

        # Attempt 3: pkexec systemctl
        systemctl_cmd = {"start": "start", "stop": "stop", "restart": "restart"}.get(cmd)
        if systemctl_cmd:
            code3, out3, err3 = _run(
                ["pkexec", "systemctl", systemctl_cmd, "adguard-cli"], timeout=60
            )
            if code3 == 0:
                logger.info("systemctl %s adguard-cli succeeded (pkexec)", systemctl_cmd)
                return True, _t("AdGuard via systemctl {} ok", systemctl_cmd), first_error
            if code3 == 126:
                return False, _t("Authentication cancelled"), ""
            if code3 == 127:
                return False, _t("Authorization failed"), ""
            final_err = err3 or out3
        else:
            final_err = err2 or out2 or err or out

        msg = _clip(final_err or first_error) or _t("'{}' failed – insufficient privileges?", cmd)
        logger.error("All privilege attempts for '%s' failed. First error: %s | last error: %s",
                     cmd, first_error, final_err)
        return False, msg, first_error

    # ── Filter management ──────────────────────────────────────────────────

    def get_filters(self, all_available: bool = False) -> "FilterListResult":
        """Parse `adguard-cli filters list [--all]` output into structured data."""
        args = [self.BINARY, "filters", "list"]
        if all_available:
            args.append("--all")
        code, out, err = _run(args, timeout=20)
        if code != 0:
            return FilterListResult(error=_clip(err or out) or _t("Could not retrieve filter list"))
        return _parse_filter_list(out)

    def _simple(
        self, args: list[str], ok_msg: str, fail_msg: str, label: str = "", *,
        timeout: int = 15, check: bool = True, stdin_data: str | None = None, done_log: str = "",
    ) -> tuple[bool, str]:
        """Run `adguard-cli <args>` and turn it into (ok, message).

        check: also treat failure text in the output as failure (the CLI
        exits 0 on some failures). label: name logged on failure.
        """
        code, out, err = _run([self.BINARY, *args], timeout=timeout, stdin_data=stdin_data)
        if code == 0 and not (check and _is_cli_failure(out, err)):
            if done_log:
                logger.info("%s", done_log)
            return True, _clip(out) or ok_msg
        msg = _clip(err or out) or fail_msg
        if label:
            logger.error("%s failed: %s", label, msg)
        return False, msg

    def enable_filter(self, filter_id: int) -> tuple[bool, str]:
        return self._simple(["filters", "enable", str(filter_id)], _t("Filter {} enabled", filter_id),
                            _t("Could not enable filter {}", filter_id), f"enable_filter({filter_id})",
                            done_log=f"Filter {filter_id} enabled")

    def disable_filter(self, filter_id: int) -> tuple[bool, str]:
        return self._simple(["filters", "disable", str(filter_id)], _t("Filter {} disabled", filter_id),
                            _t("Could not disable filter {}", filter_id), f"disable_filter({filter_id})",
                            done_log=f"Filter {filter_id} disabled")

    def remove_filter(self, filter_id: int) -> tuple[bool, str]:
        return self._simple(["filters", "remove", str(filter_id)], _t("Filter {} removed", filter_id),
                            _t("Could not remove filter {}", filter_id), f"remove_filter({filter_id})",
                            done_log=f"Filter {filter_id} removed")

    def update_filters(self) -> tuple[bool, str]:
        """
        Run `adguard-cli check-update` which updates:
        filters, DNS filters, userscripts, SafebrowsingV2, CRLite, app.
        (`adguard-cli filters update` is deprecated and redirects here.)
        """
        # No _is_cli_failure here: check-update updates filters, DNS filters,
        # userscripts, Safebrowsing and CRLite in one run, and a single failed
        # download must not mark the whole update as failed. The raw output is
        # shown to the user.
        return self._simple(["check-update"], _t("Filters updated"), _t("Update failed"), "update_filters",
                            timeout=120, check=False, done_log="Filter update completed")

    # ── Userscript management ──────────────────────────────────────────────

    def get_userscripts(self) -> "UserscriptListResult":
        """Return installed userscripts with their *real* (untruncated) IDs.

        The CLI's `userscripts list` output truncates long IDs with `...`,
        which would break enable/disable/remove calls. We use the list only
        for the enabled flag and the last-update timestamp, and take the real
        ID + human-readable title from the .meta.json files on disk.
        """
        code, out, err = _run([self.BINARY, "userscripts", "list"], timeout=15)
        if code != 0:
            return UserscriptListResult(error=_clip(err or out) or _t("Could not retrieve userscript list"))
        parsed = _parse_userscript_list(out)

        # Build filesystem inventory: real_id → (real_id, title).
        # Wrap the glob too — if the dir is unreadable we'd otherwise hang the
        # load worker on an uncaught PermissionError.
        real: list[tuple[str, str]] = []
        try:
            if _USERSCRIPTS_DIR.is_dir():
                for meta in sorted(_USERSCRIPTS_DIR.glob("*.meta.json")):
                    real_id = meta.name[: -len(".meta.json")]
                    title = real_id
                    try:
                        data = json.loads(meta.read_text(encoding="utf-8"))
                        title = data.get("name") or real_id
                    except (OSError, json.JSONDecodeError) as exc:
                        logger.warning("meta.json read failed for %s: %s", meta, exc)
                    real.append((real_id, title))
        except OSError as exc:
            logger.warning("Could not list userscripts dir %s: %s", _USERSCRIPTS_DIR, exc)

        if not real:
            # Filesystem not accessible – fall back to parsed list (may have
            # truncated IDs). Better than nothing.
            return parsed

        # Match parsed entries (possibly truncated) to real IDs by prefix.
        result = UserscriptListResult()
        used: set[str] = set()

        def candidates(entry):
            pid = entry.name
            # CLI appends "..." when the ID was truncated. An exact match wins,
            # so we don't lose IDs that legitimately end in "...".
            truncated = pid.endswith("...")
            prefix = pid[:-3] if truncated else pid
            return [(real_id, title) for real_id, title in real if real_id not in used
                    and (real_id == pid or (truncated and real_id.startswith(prefix)))]

        # Truncated IDs can share a prefix: exact IDs and titles are settled
        # first, so a guess never takes a script another entry names.
        matches = {}
        for pick in (lambda c, e: c[0] == e.name, lambda c, e: c[1] == e.title, lambda c, e: True):
            for i, entry in enumerate(parsed.scripts):
                if i not in matches and (match := next(
                        (c for c in candidates(entry) if pick(c, entry)), None)):
                    matches[i] = match
                    used.add(match[0])

        for i, entry in enumerate(parsed.scripts):
            match = matches.get(i)
            if match:
                result.scripts.append(UserscriptEntry(
                    name=match[0],
                    title=match[1] or entry.title,
                    enabled=entry.enabled,
                    last_update=entry.last_update,
                ))
            else:
                # Keep the parsed entry so the user still sees something
                result.scripts.append(entry)

        # Surface any on-disk userscript the CLI didn't report
        for real_id, title in real:
            if real_id not in used:
                result.scripts.append(UserscriptEntry(
                    name=real_id, title=title, enabled=False, last_update="",
                ))
        return result

    def enable_userscript(self, name: str) -> tuple[bool, str]:
        return self._simple(["userscripts", "enable", name], _t("Userscript '{}' enabled", name),
                            _t("Could not enable userscript '{}'", name), f"enable_userscript({name})")

    def disable_userscript(self, name: str) -> tuple[bool, str]:
        return self._simple(["userscripts", "disable", name], _t("Userscript '{}' disabled", name),
                            _t("Could not disable userscript '{}'", name), f"disable_userscript({name})")

    def remove_userscript(self, name: str) -> tuple[bool, str]:
        return self._simple(["userscripts", "remove", name], _t("Userscript '{}' removed", name),
                            _t("Could not remove userscript '{}'", name), f"remove_userscript({name})")

    def install_userscript(self, url: str) -> tuple[bool, str]:
        if not _valid_url(url):
            return False, _t("URL must start with http:// or https://")
        return self._simple(["userscripts", "install", url], _t("Userscript installed"),
                            _t("Installation failed"), f"install_userscript({url})", timeout=30)

    # ── DNS filter management ─────────────────────────────────────────────

    def get_dns_filters(self, all_available: bool = False) -> "FilterListResult":
        args = [self.BINARY, "dns", "filters", "list"]
        if all_available:
            args.append("--all")
        code, out, err = _run(args, timeout=20)
        if code != 0:
            return FilterListResult(error=_clip(err or out) or _t("Could not retrieve DNS filter list"))
        return _parse_filter_list(out)

    def enable_dns_filter(self, filter_id: int) -> tuple[bool, str]:
        return self._simple(["dns", "filters", "enable", str(filter_id)], _t("DNS filter {} enabled", filter_id),
                            _t("Could not enable DNS filter {}", filter_id), f"enable_dns_filter({filter_id})")

    def disable_dns_filter(self, filter_id: int) -> tuple[bool, str]:
        return self._simple(["dns", "filters", "disable", str(filter_id)], _t("DNS filter {} disabled", filter_id),
                            _t("Could not disable DNS filter {}", filter_id), f"disable_dns_filter({filter_id})")

    def install_dns_filter(self, url: str, title: str = "") -> tuple[bool, str]:
        if not _valid_url(url):
            return False, _t("URL must start with http:// or https://")
        args = ["dns", "filters", "install", url]
        if title:
            args += ["--title", title]
        return self._simple(args, _t("DNS filter installed"), _t("Installation failed"),
                            f"install_dns_filter({url})", timeout=30)

    def remove_dns_filter(self, filter_id: int) -> tuple[bool, str]:
        return self._simple(["dns", "filters", "remove", str(filter_id)], _t("DNS filter {} removed", filter_id),
                            _t("Could not remove DNS filter {}", filter_id), f"remove_dns_filter({filter_id})")

    def add_dns_filter(self, filter_id: str) -> tuple[bool, str]:
        return self._simple(["dns", "filters", "add", str(filter_id)], _t("DNS filter added"),
                            _t("Could not add DNS filter"), f"add_dns_filter({filter_id})")

    def set_dns_filter_title(self, filter_id: int, title: str) -> tuple[bool, str]:
        return self._simple(["dns", "filters", "set-title", str(filter_id), title], _t("DNS filter title updated"),
                            _t("Could not set DNS filter title"), f"set_dns_filter_title({filter_id})")

    # ── Extended filter management ────────────────────────────────────────

    def add_filter(self, filter_id: str) -> tuple[bool, str]:
        """Add an internal filter by ID or name."""
        return self._simple(["filters", "add", filter_id], _t("Filter added"), _t("Could not add filter"),
                            f"add_filter({filter_id})")

    def set_filter_trusted(self, filter_id: int, trusted: bool) -> tuple[bool, str]:
        return self._simple(["filters", "set-trusted", str(filter_id), str(trusted).lower()],
                            _t("Filter trust updated"), _t("Could not update filter trust"),
                            f"set_filter_trusted({filter_id})")

    def set_filter_title(self, filter_id: int, title: str) -> tuple[bool, str]:
        return self._simple(["filters", "set-title", str(filter_id), title], _t("Filter title updated"),
                            _t("Could not set filter title"), f"set_filter_title({filter_id})")

    def install_filter_ext(self, url: str, trusted: bool = False, title: str = "") -> tuple[bool, str]:
        """Install custom filter with optional --trusted and --title flags."""
        if not _valid_url(url):
            return False, _t("URL must start with http:// or https://")
        args = ["filters", "install", url]
        if trusted:
            args.append("--trusted")
        if title:
            args += ["--title", title]
        return self._simple(args, _t("Filter installed"), _t("Installation failed"),
                            f"install_filter_ext({url})", timeout=30)

    # ── Config (adguard-cli config get/set) ───────────────────────────────

    UPDATE_CHANNELS = ("release", "beta", "nightly", "default")

    def get_update_channel(self) -> str:
        """Return the current update channel, or "" on error."""
        code, out, _ = _run([self.BINARY, "config", "get", "update_channel"], timeout=10)
        if code != 0 or not out:
            return ""
        # Output: "update_channel = nightly"
        if "=" in out:
            return out.split("=", 1)[1].strip()
        return out.strip()

    def set_update_channel(self, channel: str) -> tuple[bool, str]:
        if channel not in self.UPDATE_CHANNELS:
            return False, _t("Invalid channel: {}", channel)
        return self._simple(["config", "set", "update_channel", channel], _t("Update channel set to {}", channel),
                            _t("Could not set update channel"), f"set_update_channel({channel})",
                            timeout=10, done_log=f"Update channel set to {channel}")

    # ── License ───────────────────────────────────────────────────────────

    def get_license(self) -> tuple[bool, str]:
        return self._simple(["license"], "", _t("Could not retrieve license info"), timeout=10, check=False)

    def reset_license(self) -> tuple[bool, str]:
        return self._simple(["reset-license"], _t("License reset"), _t("Could not reset license"),
                            "reset_license", check=False)

    # ── Certificate ───────────────────────────────────────────────────────

    def generate_cert(self, firefox_profile: str = "") -> tuple[bool, str]:
        """Generate and install the HTTPS filtering certificate.

        Runs without pkexec — adguard-cli cert handles privilege
        elevation internally. Pipes 'yes' to confirm the interactive prompt.
        """
        args = ["cert"]
        if firefox_profile:
            args += ["--firefox-profile", firefox_profile]
        return self._simple(args, _t("Certificate generated"), _t("Certificate generation failed"),
                            "generate_cert", timeout=60, check=False, stdin_data="yes\n")

    # ── Export / Import ───────────────────────────────────────────────────

    def export_logs(self, output_dir: str = "") -> tuple[bool, str]:
        args = ["export-logs"] + (["-o", output_dir] if output_dir else [])
        return self._simple(args, _t("Logs exported"), _t("Log export failed"), "export_logs",
                            timeout=60, check=False)

    def export_settings(self, output_dir: str = "") -> tuple[bool, str]:
        args = ["export-settings"] + (["-o", output_dir] if output_dir else [])
        return self._simple(args, _t("Settings exported"), _t("Settings export failed"), "export_settings",
                            timeout=60, check=False)

    def import_settings(self, input_path: str) -> tuple[bool, str]:
        return self._simple(["import-settings", "-i", input_path], _t("Settings imported"),
                            _t("Settings import failed"), "import_settings", timeout=60, check=False)

    # ── Update / Speed ────────────────────────────────────────────────────

    def check_cli_update(self) -> tuple[bool, str]:
        return self._simple(["update"], _t("Update check completed"), _t("Update check failed"),
                            "check_cli_update", timeout=120, check=False)

    def run_speed_benchmark(self) -> tuple[bool, str]:
        return self._simple(["speed", "--json"], "", _t("Benchmark failed"), "run_speed_benchmark",
                            timeout=120, check=False)


# ── Filter data structures ─────────────────────────────────────────────────

@dataclass
class FilterEntry:
    id: int
    title: str
    enabled: bool
    last_update: str  # raw timestamp string, may be empty
    group: str = ""
    is_custom: bool = False
    # True if the filter is in the active list. False only for rows that
    # only appear in `filters list --all` because they're not added yet.
    is_added: bool = True


@dataclass
class FilterListResult:
    groups: dict[str, list[FilterEntry]] = field(default_factory=dict)
    error: str = ""

    @property
    def all_filters(self) -> list[FilterEntry]:
        return [f for group in self.groups.values() for f in group]


# ── Filter list parser ─────────────────────────────────────────────────────

# Matches installed/enabled:  [x] |    -10001 | Bypass Paywalls Clean filter   2026-03-10 20:19:53
# Matches installed/disabled: [ ] |        2 | AdGuard Base filter             2026-03-10 21:12:04
# Matches not-added (--all):      |        4 | AdGuard Social Media filter    Filter is not added
_FILTER_LINE_RE = re.compile(
    r"^(?:\[(?P<enabled>[x ])\])?\s*\|\s*(?P<id>-?\d+)\s*\|\s*(?P<rest>.+)$"
)
# Timestamp at end of title: 4 digits-2-2 space 2:2:2
_TIMESTAMP_RE = re.compile(r"\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s*$")
# Status text appended by CLI instead of a timestamp
_STATUS_SUFFIX_RE = re.compile(r"\s+Filter is (?:not added|disabled)\s*$")
# Header line of the table (contains "ID" and "Title") – skip it
_HEADER_RE = re.compile(r"^\s*\|?\s*ID\s*\|")


@dataclass
class UserscriptEntry:
    name: str        # ID used for CLI commands
    title: str
    enabled: bool
    last_update: str


@dataclass
class UserscriptListResult:
    scripts: list[UserscriptEntry] = field(default_factory=list)
    error: str = ""


# ── Userscript list parser ─────────────────────────────────────────────────
# Input format (two lines per script):
#   [x] | Title: AdGuard Extra                 2026-03-10 20:10:25
#       |    ID: adguard-extra

_US_TITLE_RE = re.compile(
    r"^\[(?P<enabled>[x ])\]\s*\|\s*Title:\s*(?P<rest>.+)$"
)
_US_ID_RE = re.compile(r"^\s*\|\s*ID:\s*(?P<id>\S+)\s*$")


def _parse_userscript_list(raw: str) -> UserscriptListResult:
    result = UserscriptListResult()
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    i = 0
    while i < len(lines):
        m_title = _US_TITLE_RE.match(lines[i])
        if m_title:
            enabled = m_title.group("enabled") == "x"
            rest = m_title.group("rest").strip()
            ts_m = _TIMESTAMP_RE.search(rest)
            if ts_m:
                last_update = ts_m.group(1).strip()
                title = rest[: ts_m.start()].strip()
            else:
                last_update = ""
                title = rest

            # Next line should be the ID
            name = ""
            if i + 1 < len(lines):
                m_id = _US_ID_RE.match(lines[i + 1])
                if m_id:
                    name = m_id.group("id")
                    i += 1  # consume the ID line too

            if name:
                result.scripts.append(
                    UserscriptEntry(name=name, title=title, enabled=enabled, last_update=last_update)
                )
        i += 1
    return result


# ── Filter list parser ─────────────────────────────────────────────────────

def _parse_filter_list(raw: str) -> FilterListResult:
    result = FilterListResult()
    current_group = _t("Other")
    pending_group = ""
    saw_header = False

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        # Skip table header row
        if _HEADER_RE.search(line):
            saw_header = True
            continue

        m = _FILTER_LINE_RE.match(line)
        if m:
            enabled_ch = m.group("enabled")
            # None = not-added filter (no checkbox), " " = disabled, "x" = enabled
            enabled = enabled_ch == "x"
            is_added = enabled_ch is not None
            fid = int(m.group("id"))
            rest = m.group("rest").strip()

            # Extract trailing timestamp
            ts_m = _TIMESTAMP_RE.search(rest)
            if ts_m:
                last_update = ts_m.group(1).strip()
                title = rest[: ts_m.start()].strip()
            else:
                # Strip status suffix ("Filter is not added" / "Filter is disabled")
                rest = _STATUS_SUFFIX_RE.sub("", rest)
                last_update = ""
                title = rest.strip()

            if pending_group:
                current_group = pending_group
                pending_group = ""
            entry = FilterEntry(
                id=fid,
                title=title,
                enabled=enabled,
                last_update=last_update,
                group=current_group,
                is_custom=(fid < 0),
                is_added=is_added,
            )
            result.groups.setdefault(current_group, []).append(entry)
        else:
            # Non-filter line without `|` is either a group header or a footer.
            # CLI footers wrap to multiple lines and tend to be long; group
            # names are short. Use length as the structural cue (locale-safe)
            # and only commit the name once a filter line actually follows, so
            # a short footer doesn't create a phantom group.
            if "|" not in line and len(line) <= 40:
                pending_group = line
                logger.debug("Filter group candidate: %r", pending_group)

    if raw.strip() and not result.groups and not saw_header:
        # Neither a filter row nor a table header: the CLI changed its format.
        # Report it instead of showing an empty list as if nothing was
        # installed. (A header-only table is a legitimate "nothing installed".)
        result.error = _t("Could not read the filter list (unexpected CLI output).")
    return result
