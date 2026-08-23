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


def _is_cli_failure(stdout: str) -> bool:
    """Detect failure reported in stdout (adguard-cli returns exit 0 on some failures)."""
    lower = stdout.lower()
    return any(kw in lower for kw in _FAILURE_KEYWORDS)


def _valid_url(url: str) -> bool:
    return url.lower().startswith(("http://", "https://"))


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


def _run(args: list[str], timeout: int = 15, stdin_data: str | None = None) -> tuple[int, str, str]:
    try:
        r = subprocess.run(
            args, capture_output=True, timeout=timeout,
            input=stdin_data.encode("utf-8") if stdin_data else None,
        )
        # Decode explicitly so a C-locale runtime (systemd unit, cron) doesn't
        # crash on filter titles with umlauts or CJK.
        out = r.stdout.decode("utf-8", errors="replace").strip()
        err = r.stderr.decode("utf-8", errors="replace").strip()
        return r.returncode, _strip_ansi(out), _strip_ansi(err)
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
            return StatusResult(AdGuardStatus.ACTIVE, out, out, proxy_port, filtering_enabled)

        if _STOPPED_RE.search(combined):
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
            # Stale socket from a previous unclean stop – kill and retry.
            logger.warning("Socket busy on start, cleaning up stale processes")
            self._force_kill()
            time.sleep(0.5)
            ok, msg = self._privileged_command("start")
        return ok, msg

    def stop(self) -> tuple[bool, str]:
        ok, msg = self._privileged_command("stop")
        if not ok:
            # e.g. polkit prompt cancelled – don't follow up with a force-kill
            # that would prompt again.
            return ok, msg
        # Verify the service actually stopped – adguard-cli stop can report
        # success while leaving the process alive (stale socket).
        time.sleep(1)
        status = self.get_status()
        if status.status == AdGuardStatus.ACTIVE:
            logger.warning("stop reported success but service still active, force-killing")
            return self._force_kill()
        return ok, msg

    def _force_kill(self) -> tuple[bool, str]:
        """Kill lingering adguard-cli processes and the root helper.

        First try unprivileged pkill; if the service is still up, retry with
        pkexec since adguard_root_helper runs as root and can't be signalled
        from the user session.
        """
        for name in ("adguard-cli", "adguard_root_helper"):
            code, _, err = _run(["pkill", "-x", name], timeout=5)
            # exit 1 means "no matching process" which is fine here
            if code not in (0, 1):
                logger.warning("pkill %s exit %d: %s", name, code, err)
        time.sleep(0.5)
        if self.get_status().status != AdGuardStatus.ACTIVE:
            logger.info("Force-kill succeeded (user)")
            return True, _t("AdGuard stopped (forced)")

        logger.warning("User-level pkill did not stop service, trying pkexec")
        for name in ("adguard-cli", "adguard_root_helper"):
            code, _, err = _run(["pkexec", "pkill", "-x", name], timeout=30)
            if code not in (0, 1):
                logger.warning("pkexec pkill %s exit %d: %s", name, code, err)
        time.sleep(0.5)
        if self.get_status().status != AdGuardStatus.ACTIVE:
            logger.info("Force-kill succeeded (pkexec)")
            return True, _t("AdGuard stopped (forced)")

        logger.error("Force-kill failed, service may still be running")
        return False, _t("Could not stop AdGuard – process may still be running")

    def restart(self) -> tuple[bool, str]:
        ok, msg = self._privileged_command("restart")
        if not ok:
            return ok, msg
        # `adguard-cli restart` doesn't always start a stopped proxy. Verify
        # and fall back to `start` if the service didn't come up.
        time.sleep(1)
        if self.get_status().status != AdGuardStatus.ACTIVE:
            logger.info("restart left the proxy inactive – calling start")
            return self.start()
        return ok, msg

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
            return True, out or _t("AdGuard {} ok", cmd)
        if code == -1:
            # Binary missing – pkexec would only raise pointless prompts.
            return False, err

        logger.debug("Direct %s failed (exit %d): %s – trying pkexec", cmd, code, err)

        # Attempt 2: pkexec adguard-cli
        code2, out2, err2 = _run(["pkexec", self.BINARY, cmd], timeout=60)
        if code2 == 0:
            logger.info("adguard-cli %s succeeded (pkexec)", cmd)
            return True, out2 or _t("AdGuard {} ok", cmd)

        # pkexec exits 126 when the user dismisses the dialog, 127 when
        # authorization failed or the command could not be run. Surface that
        # directly instead of falling through to systemctl, which would
        # prompt again.
        if code2 == 126:
            logger.info("pkexec authentication cancelled (exit 126)")
            return False, _t("Authentication cancelled")
        if code2 == 127:
            logger.error("pkexec authorization failed (exit 127): %s", err2)
            return False, _t("Authorization failed")

        logger.debug("pkexec adguard-cli %s failed (exit %d) – trying systemctl", cmd, code2)

        # Attempt 3: pkexec systemctl
        systemctl_cmd = {"start": "start", "stop": "stop", "restart": "restart"}.get(cmd)
        if systemctl_cmd:
            code3, out3, err3 = _run(
                ["pkexec", "systemctl", systemctl_cmd, "adguard-cli"], timeout=60
            )
            if code3 == 0:
                logger.info("systemctl %s adguard-cli succeeded (pkexec)", systemctl_cmd)
                return True, _t("AdGuard via systemctl {} ok", systemctl_cmd)
            if code3 == 126:
                return False, _t("Authentication cancelled")
            if code3 == 127:
                return False, _t("Authorization failed")
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

    def remove_filter(self, filter_id: int) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "filters", "remove", str(filter_id)], timeout=15)
        if code == 0 and not _is_cli_failure(out):
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
        """Return installed userscripts with their *real* (untruncated) IDs.

        The CLI's `userscripts list` output truncates long IDs with `...`,
        which would break enable/disable/remove calls. We use the list only
        for the enabled flag and the last-update timestamp, and take the real
        ID + human-readable title from the .meta.json files on disk.
        """
        code, out, err = _run([self.BINARY, "userscripts", "list"], timeout=15)
        if code != 0:
            return UserscriptListResult(error=err or out or _t("Could not retrieve userscript list"))
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
        for entry in parsed.scripts:
            pid = entry.name
            # CLI appends "..." when the ID was truncated. Exact match is
            # tried first below, so we don't lose IDs that legitimately end
            # in "...".
            truncated = pid.endswith("...")
            prefix = pid[:-3] if truncated else pid
            match: tuple[str, str] | None = None
            for real_id, title in real:
                if real_id in used:
                    continue
                if real_id == pid or (truncated and real_id.startswith(prefix)):
                    match = (real_id, title)
                    break
            if match:
                used.add(match[0])
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
        code, out, err = _run([self.BINARY, "userscripts", "enable", name], timeout=15)
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("Userscript '{}' enabled", name)
        msg = err or out or _t("Could not enable userscript '{}'", name)
        logger.error("enable_userscript(%s) failed: %s", name, msg)
        return False, msg

    def disable_userscript(self, name: str) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "userscripts", "disable", name], timeout=15)
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("Userscript '{}' disabled", name)
        msg = err or out or _t("Could not disable userscript '{}'", name)
        logger.error("disable_userscript(%s) failed: %s", name, msg)
        return False, msg

    def remove_userscript(self, name: str) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "userscripts", "remove", name], timeout=15)
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("Userscript '{}' removed", name)
        msg = err or out or _t("Could not remove userscript '{}'", name)
        logger.error("remove_userscript(%s) failed: %s", name, msg)
        return False, msg

    def install_userscript(self, url: str) -> tuple[bool, str]:
        if not _valid_url(url):
            return False, _t("URL must start with http:// or https://")
        code, out, err = _run([self.BINARY, "userscripts", "install", url], timeout=30)
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("Userscript installed")
        msg = err or out or _t("Installation failed")
        logger.error("install_userscript(%s) failed: %s", url, msg)
        return False, msg

    # ── DNS filter management ─────────────────────────────────────────────

    def get_dns_filters(self, all_available: bool = False) -> "FilterListResult":
        args = [self.BINARY, "dns", "filters", "list"]
        if all_available:
            args.append("--all")
        code, out, err = _run(args, timeout=20)
        if code != 0:
            return FilterListResult(error=err or out or _t("Could not retrieve DNS filter list"))
        return _parse_filter_list(out)

    def enable_dns_filter(self, filter_id: int) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "dns", "filters", "enable", str(filter_id)], timeout=15)
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("DNS filter {} enabled", filter_id)
        msg = err or out or _t("Could not enable DNS filter {}", filter_id)
        logger.error("enable_dns_filter(%s) failed: %s", filter_id, msg)
        return False, msg

    def disable_dns_filter(self, filter_id: int) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "dns", "filters", "disable", str(filter_id)], timeout=15)
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("DNS filter {} disabled", filter_id)
        msg = err or out or _t("Could not disable DNS filter {}", filter_id)
        logger.error("disable_dns_filter(%s) failed: %s", filter_id, msg)
        return False, msg

    def install_dns_filter(self, url: str, title: str = "") -> tuple[bool, str]:
        if not _valid_url(url):
            return False, _t("URL must start with http:// or https://")
        args = [self.BINARY, "dns", "filters", "install", url]
        if title:
            args += ["--title", title]
        code, out, err = _run(args, timeout=30)
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("DNS filter installed")
        msg = err or out or _t("Installation failed")
        logger.error("install_dns_filter(%s) failed: %s", url, msg)
        return False, msg

    def remove_dns_filter(self, filter_id: int) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "dns", "filters", "remove", str(filter_id)], timeout=15)
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("DNS filter {} removed", filter_id)
        msg = err or out or _t("Could not remove DNS filter {}", filter_id)
        logger.error("remove_dns_filter(%s) failed: %s", filter_id, msg)
        return False, msg

    def add_dns_filter(self, filter_id: str) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "dns", "filters", "add", str(filter_id)], timeout=15)
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("DNS filter added")
        msg = err or out or _t("Could not add DNS filter")
        logger.error("add_dns_filter(%s) failed: %s", filter_id, msg)
        return False, msg

    def set_dns_filter_title(self, filter_id: int, title: str) -> tuple[bool, str]:
        code, out, err = _run(
            [self.BINARY, "dns", "filters", "set-title", str(filter_id), title], timeout=15
        )
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("DNS filter title updated")
        msg = err or out or _t("Could not set DNS filter title")
        logger.error("set_dns_filter_title(%d) failed: %s", filter_id, msg)
        return False, msg

    # ── Extended filter management ────────────────────────────────────────

    def add_filter(self, filter_id: str) -> tuple[bool, str]:
        """Add an internal filter by ID or name."""
        code, out, err = _run([self.BINARY, "filters", "add", filter_id], timeout=15)
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("Filter added")
        msg = err or out or _t("Could not add filter")
        logger.error("add_filter(%s) failed: %s", filter_id, msg)
        return False, msg

    def set_filter_trusted(self, filter_id: int, trusted: bool) -> tuple[bool, str]:
        code, out, err = _run(
            [self.BINARY, "filters", "set-trusted", str(filter_id), str(trusted).lower()],
            timeout=15,
        )
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("Filter trust updated")
        msg = err or out or _t("Could not update filter trust")
        logger.error("set_filter_trusted(%d) failed: %s", filter_id, msg)
        return False, msg

    def set_filter_title(self, filter_id: int, title: str) -> tuple[bool, str]:
        code, out, err = _run(
            [self.BINARY, "filters", "set-title", str(filter_id), title], timeout=15
        )
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("Filter title updated")
        msg = err or out or _t("Could not set filter title")
        logger.error("set_filter_title(%d) failed: %s", filter_id, msg)
        return False, msg

    def install_filter_ext(self, url: str, trusted: bool = False, title: str = "") -> tuple[bool, str]:
        """Install custom filter with optional --trusted and --title flags."""
        if not _valid_url(url):
            return False, _t("URL must start with http:// or https://")
        args = [self.BINARY, "filters", "install", url]
        if trusted:
            args.append("--trusted")
        if title:
            args += ["--title", title]
        code, out, err = _run(args, timeout=30)
        if code == 0 and not _is_cli_failure(out):
            return True, out or _t("Filter installed")
        msg = err or out or _t("Installation failed")
        logger.error("install_filter_ext(%s) failed: %s", url, msg)
        return False, msg

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
        code, out, err = _run(
            [self.BINARY, "config", "set", "update_channel", channel], timeout=10
        )
        if code == 0 and not _is_cli_failure(out):
            logger.info("Update channel set to %s", channel)
            return True, out or _t("Update channel set to {}", channel)
        msg = err or out or _t("Could not set update channel")
        logger.error("set_update_channel(%s) failed: %s", channel, msg)
        return False, msg

    # ── License ───────────────────────────────────────────────────────────

    def get_license(self) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "license"], timeout=10)
        if code == 0:
            return True, out
        return False, err or out or _t("Could not retrieve license info")

    def reset_license(self) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "reset-license"], timeout=15)
        if code == 0:
            return True, out or _t("License reset")
        msg = err or out or _t("Could not reset license")
        logger.error("reset_license failed: %s", msg)
        return False, msg

    # ── Certificate ───────────────────────────────────────────────────────

    def generate_cert(self, firefox_profile: str = "") -> tuple[bool, str]:
        """Generate and install the HTTPS filtering certificate.

        Runs without pkexec — adguard-cli cert handles privilege
        elevation internally. Pipes 'yes' to confirm the interactive prompt.
        """
        args = [self.BINARY, "cert"]
        if firefox_profile:
            args += ["--firefox-profile", firefox_profile]
        code, out, err = _run(
            args, timeout=60, stdin_data="yes\n",
        )
        if code == 0:
            return True, out or _t("Certificate generated")
        msg = err or out or _t("Certificate generation failed")
        logger.error("generate_cert failed: %s", msg)
        return False, msg

    # ── Export / Import ───────────────────────────────────────────────────

    def export_logs(self, output_dir: str = "") -> tuple[bool, str]:
        args = [self.BINARY, "export-logs"]
        if output_dir:
            args += ["-o", output_dir]
        code, out, err = _run(args, timeout=60)
        if code == 0:
            return True, out or _t("Logs exported")
        msg = err or out or _t("Log export failed")
        logger.error("export_logs failed: %s", msg)
        return False, msg

    def export_settings(self, output_dir: str = "") -> tuple[bool, str]:
        args = [self.BINARY, "export-settings"]
        if output_dir:
            args += ["-o", output_dir]
        code, out, err = _run(args, timeout=60)
        if code == 0:
            return True, out or _t("Settings exported")
        msg = err or out or _t("Settings export failed")
        logger.error("export_settings failed: %s", msg)
        return False, msg

    def import_settings(self, input_path: str) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "import-settings", "-i", input_path], timeout=60)
        if code == 0:
            return True, out or _t("Settings imported")
        msg = err or out or _t("Settings import failed")
        logger.error("import_settings failed: %s", msg)
        return False, msg

    # ── Update / Speed ────────────────────────────────────────────────────

    def check_cli_update(self) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "update"], timeout=120)
        if code == 0:
            return True, out or _t("Update check completed")
        msg = err or out or _t("Update check failed")
        logger.error("check_cli_update failed: %s", msg)
        return False, msg

    def run_speed_benchmark(self) -> tuple[bool, str]:
        code, out, err = _run([self.BINARY, "speed", "--json"], timeout=120)
        if code == 0:
            return True, out
        msg = err or out or _t("Benchmark failed")
        logger.error("run_speed_benchmark failed: %s", msg)
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

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        # Skip table header row
        if _HEADER_RE.search(line):
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
            # names are short. Use length as the structural cue (locale-safe).
            if "|" not in line and len(line) <= 40:
                current_group = line
                logger.debug("Filter group: %r", current_group)

    return result
