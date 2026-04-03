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

import logging
import re
import subprocess
import time
from dataclasses import dataclass, field
from enum import Enum

from .i18n import _t

logger = logging.getLogger(__name__)

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
_PORT_RE = re.compile(r"127\.0\.0\.1:(\d+)")


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


_FAILURE_KEYWORDS = ("failed to install", "failed to download", "failed to remove", "failed to enable", "failed to disable")


def _is_cli_failure(stdout: str) -> bool:
    """Detect failure reported in stdout (adguard-cli returns exit 0 on some failures)."""
    lower = stdout.lower()
    return any(kw in lower for kw in _FAILURE_KEYWORDS)


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
    raw_output: str = ""
    proxy_port: str = ""
    filtering_enabled: bool = False


def _run(args: list[str], timeout: int = 15) -> tuple[int, str, str]:
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return r.returncode, _strip_ansi(r.stdout.strip()), _strip_ansi(r.stderr.strip())
    except FileNotFoundError:
        return -1, "", f"Binary not found: {args[0]}"
    except subprocess.TimeoutExpired:
        return -2, "", f"Command timed out after {timeout}s"
    except OSError as exc:
        return -3, "", str(exc)


class AdGuardCLI:
    BINARY = "adguard-cli"

    def __init__(self, binary: str = "") -> None:
        if binary:
            self.BINARY = binary

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

        if "is running" in combined or "has started" in combined:
            return StatusResult(AdGuardStatus.ACTIVE, out, out, proxy_port, filtering_enabled)

        if (
            "is not running" in combined
            or "has been stopped" in combined
            or "stopped" in combined
        ):
            # adguard-cli may lack a PID file when managed by systemd → verify
            fallback = self._systemctl_fallback(out)
            if fallback.status == AdGuardStatus.ACTIVE:
                return StatusResult(AdGuardStatus.ACTIVE, out, out, proxy_port, filtering_enabled)
            return StatusResult(AdGuardStatus.INACTIVE, out, out, proxy_port, filtering_enabled)

        # Ambiguous output → fallback to systemctl
        logger.debug("Status output ambiguous, checking systemctl: %r", out)
        return self._systemctl_fallback(out)

    def _systemctl_fallback(self, original: str) -> StatusResult:
        code, out, _ = _run(["systemctl", "is-active", "adguard-cli"], timeout=5)
        state = out.strip()
        if state == "active":
            return StatusResult(AdGuardStatus.ACTIVE, original, original)
        if state in ("inactive", "failed", "dead"):
            return StatusResult(AdGuardStatus.INACTIVE, original, original)
        return StatusResult(AdGuardStatus.UNKNOWN, original, original)

    # ── Control commands ───────────────────────────────────────────────────

    def start(self) -> tuple[bool, str]:
        ok, msg = self._privileged_command("start")
        if not ok and "socket busy" in msg.lower():
            # Stale socket from a previous unclean stop – kill and retry
            logger.warning("Socket busy on start, cleaning up stale processes")
            self._force_kill()
            time.sleep(0.5)
            ok, msg = self._privileged_command("start")
        return ok, msg

    def stop(self) -> tuple[bool, str]:
        ok, msg = self._privileged_command("stop")
        # Verify the service actually stopped – adguard-cli stop can report
        # success while leaving the process alive (stale socket).
        time.sleep(1)
        status = self.get_status()
        if status.status == AdGuardStatus.ACTIVE:
            logger.warning("stop reported success but service still active, force-killing")
            return self._force_kill()
        return ok, msg

    def _force_kill(self) -> tuple[bool, str]:
        """Kill lingering adguard-cli processes and the root helper."""
        killed = False
        for name in ("adguard-cli", "adguard_root_helper"):
            code, out, _ = _run(["pkill", "-f", name], timeout=5)
            if code == 0:
                killed = True
        if killed:
            time.sleep(0.5)
            status = self.get_status()
            if status.status != AdGuardStatus.ACTIVE:
                logger.info("Force-kill succeeded")
                return True, _t("AdGuard stopped (forced)")
        logger.error("Force-kill failed, service may still be running")
        return False, _t("Could not stop AdGuard – process may still be running")

    def restart(self) -> tuple[bool, str]:
        return self._privileged_command("restart")

    def toggle(self) -> tuple[bool, str]:
        s = self.get_status()
        return self.stop() if s.status == AdGuardStatus.ACTIVE else self.start()

    def _privileged_command(self, cmd: str) -> tuple[bool, str]:
        """
        Try in order:
          1. adguard-cli <cmd>              (no privilege needed if configured)
          2. pkexec adguard-cli <cmd>       (polkit GUI prompt)
          3. pkexec systemctl <cmd> adguard-cli  (fallback via systemd)
        """
        # Attempt 1: direct
        code, out, err = _run([self.BINARY, cmd])
        if code == 0:
            logger.info("adguard-cli %s succeeded (direct)", cmd)
            return True, out or _t("AdGuard {} successful", cmd)

        logger.debug("Direct %s failed (exit %d): %s – trying pkexec", cmd, code, err)

        # Attempt 2: pkexec adguard-cli
        code2, out2, err2 = _run(["pkexec", self.BINARY, cmd], timeout=60)
        if code2 == 0:
            logger.info("adguard-cli %s succeeded (pkexec)", cmd)
            return True, out2 or _t("AdGuard {} successful", cmd)

        logger.debug("pkexec adguard-cli %s failed (exit %d) – trying systemctl", cmd, code2)

        # Attempt 3: pkexec systemctl
        systemctl_cmd = {"start": "start", "stop": "stop", "restart": "restart"}.get(cmd)
        if systemctl_cmd:
            code3, out3, err3 = _run(
                ["pkexec", "systemctl", systemctl_cmd, "adguard-cli"], timeout=60
            )
            if code3 == 0:
                logger.info("systemctl %s adguard-cli succeeded (pkexec)", systemctl_cmd)
                return True, _t("AdGuard via systemctl {} successful", systemctl_cmd)
            final_err = err3 or out3
        else:
            final_err = err2 or out2 or err or out

        msg = final_err or _t("'{}' failed – insufficient privileges?", cmd)
        logger.error("All privilege attempts for '%s' failed. Last error: %s", cmd, msg)
        return False, msg

    # ── Filter management ──────────────────────────────────────────────────

    def get_filters(self, all_available: bool = False) -> "FilterListResult":
        """Parse `adguard-cli filters list [--all]` output into structured data."""
        args = [self.BINARY, "filters", "list"]
        if all_available:
            args.append("--all")
        code, out, err = _run(args, timeout=20)
        if code != 0:
            return FilterListResult(error=err or out or _t("Could not retrieve filter list"))
        return _parse_filter_list(out)

    def enable_filter(self, filter_id: int) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "filters", "enable", str(filter_id)], timeout=15)
        if code == 0 and not _is_cli_failure(out):
            logger.info("Filter %d enabled", filter_id)
            return True, out or _t("Filter {} enabled", filter_id)
        msg = err or out or _t("Could not enable filter {}", filter_id)
        logger.error("enable_filter(%d) failed: %s", filter_id, msg)
        return False, msg

    def disable_filter(self, filter_id: int) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "filters", "disable", str(filter_id)], timeout=15)
        if code == 0 and not _is_cli_failure(out):
            logger.info("Filter %d disabled", filter_id)
            return True, out or _t("Filter {} disabled", filter_id)
        msg = err or out or _t("Could not disable filter {}", filter_id)
        logger.error("disable_filter(%d) failed: %s", filter_id, msg)
        return False, msg

    def install_filter(self, url: str) -> tuple[bool, str]:
        """Install a custom filter from a URL."""
        code, out, err = _run([self.BINARY, "filters", "install", url], timeout=30)
        if code == 0 and not _is_cli_failure(out):
            logger.info("Custom filter installed: %s", url)
            return True, out or _t("Filter installed")
        msg = err or out or _t("Installation failed")
        logger.error("install_filter(%s) failed: %s", url, msg)
        return False, msg

    def remove_filter(self, filter_id: int) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "filters", "remove", str(filter_id)], timeout=15)
        if code == 0:
            logger.info("Filter %d removed", filter_id)
            return True, out or _t("Filter {} removed", filter_id)
        msg = err or out or _t("Could not remove filter {}", filter_id)
        logger.error("remove_filter(%d) failed: %s", filter_id, msg)
        return False, msg

    def update_filters(self) -> tuple[bool, str]:
        """
        Run `adguard-cli check-update` which updates:
        filters, DNS filters, userscripts, SafebrowsingV2, CRLite, app.
        (`adguard-cli filters update` is deprecated and redirects here.)
        """
        code, out, err = _run([self.BINARY, "check-update"], timeout=120)
        if code == 0:
            logger.info("Filter update completed")
            return True, out or _t("Filters updated")
        msg = err or out or _t("Update failed")
        logger.error("update_filters failed: %s", msg)
        return False, msg

    # ── Userscript management ──────────────────────────────────────────────

    def get_userscripts(self) -> "UserscriptListResult":
        """Parse `adguard-cli userscripts list` output."""
        code, out, err = _run([self.BINARY, "userscripts", "list"], timeout=15)
        if code != 0:
            return UserscriptListResult(error=err or out or _t("Could not retrieve userscript list"))
        return _parse_userscript_list(out)

    def enable_userscript(self, name: str) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "userscripts", "enable", name], timeout=15)
        if code == 0:
            return True, out or _t("Userscript '{}' enabled", name)
        msg = err or out or _t("Could not enable userscript '{}'", name)
        logger.error("enable_userscript(%s) failed: %s", name, msg)
        return False, msg

    def disable_userscript(self, name: str) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "userscripts", "disable", name], timeout=15)
        if code == 0:
            return True, out or _t("Userscript '{}' disabled", name)
        msg = err or out or _t("Could not disable userscript '{}'", name)
        logger.error("disable_userscript(%s) failed: %s", name, msg)
        return False, msg

    def remove_userscript(self, name: str) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "userscripts", "remove", name], timeout=15)
        if code == 0:
            return True, out or _t("Userscript '{}' removed", name)
        msg = err or out or _t("Could not remove userscript '{}'", name)
        logger.error("remove_userscript(%s) failed: %s", name, msg)
        return False, msg

    def install_userscript(self, url: str) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "userscripts", "install", url], timeout=30)
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("Userscript installed")
        msg = err or out or _t("Installation failed")
        logger.error("install_userscript(%s) failed: %s", url, msg)
        return False, msg


# ── Filter data structures ─────────────────────────────────────────────────

@dataclass
class FilterEntry:
    id: int
    title: str
    enabled: bool
    last_update: str  # raw timestamp string, may be empty
    group: str = ""
    is_custom: bool = False


@dataclass
class FilterListResult:
    groups: dict[str, list[FilterEntry]] = field(default_factory=dict)
    error: str = ""

    @property
    def all_filters(self) -> list[FilterEntry]:
        return [f for group in self.groups.values() for f in group]


# ── Filter list parser ─────────────────────────────────────────────────────

# Matches:  [x] |    -10001 | Bypass Paywalls Clean filter   2026-03-10 20:19:53
# or:       [ ] |        2 | AdGuard Base filter             2026-03-10 21:12:04
_FILTER_LINE_RE = re.compile(
    r"^\[(?P<enabled>[x ])\]\s*\|\s*(?P<id>-?\d+)\s*\|\s*(?P<rest>.+)$"
)
# Timestamp at end of title: 4 digits-2-2 space 2:2:2
_TIMESTAMP_RE = re.compile(r"\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s*$")
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

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        # Skip table header row
        if _HEADER_RE.search(line):
            continue

        m = _FILTER_LINE_RE.match(line)
        if m:
            enabled = m.group("enabled") == "x"
            fid = int(m.group("id"))
            rest = m.group("rest").strip()

            # Extract trailing timestamp
            ts_m = _TIMESTAMP_RE.search(rest)
            if ts_m:
                last_update = ts_m.group(1).strip()
                title = rest[: ts_m.start()].strip()
            else:
                last_update = ""
                title = rest

            entry = FilterEntry(
                id=fid,
                title=title,
                enabled=enabled,
                last_update=last_update,
                group=current_group,
                is_custom=(fid < 0),
            )
            result.groups.setdefault(current_group, []).append(entry)
        else:
            # Non-filter line without leading spaces/pipes = group header
            # (avoids picking up "To view the full list…" footer)
            if not line.startswith("|") and not line.startswith("To "):
                current_group = line
                logger.debug("Filter group: %r", current_group)

    return result
