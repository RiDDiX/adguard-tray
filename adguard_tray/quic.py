"""Report whether browsers can bypass AdGuard over HTTP/3 (QUIC).

adguard-cli does handle QUIC, but only in `auto` proxy mode: its iptables rules
redirect UDP as well as TCP, and `https_filtering.http3_filtering_enabled`
decides whether an intercepted QUIC connection is filtered (true) or blocked so
the client falls back to TCP (false).

In `manual` mode – the default the first-run wizard offers – nothing touches
UDP/443, so a browser speaking HTTP/3 talks to the site directly and none of
its traffic is filtered. Nothing tells the user; the page simply loads with
ads. This module works out which case applies so the app can say so.
"""

import configparser
import glob
import json
import logging
import re
import socket
from dataclasses import dataclass, field
from pathlib import Path

from .i18n import _t
from .proxy_config_dialog import _load_yaml

logger = logging.getLogger(__name__)

HOME = Path.home()

# Chromium-family managed policy files (system-wide; the dir is a build-time
# constant, so forks either inherit /etc/chromium or patch it).
_POLICY_FILES = (
    "/etc/opt/chrome/policies/managed/*.json",
    "/etc/chromium/policies/managed/*.json",
    "/etc/chromium-browser/policies/managed/*.json",
    "/etc/brave/policies/managed/*.json",
    "/etc/opt/edge/policies/managed/*.json",
    "/etc/opt/opera/policies/managed/*.json",
)
_FIREFOX_POLICIES = ("/etc/firefox/policies/policies.json",)

_FIREFOX_ROOTS = (
    HOME / ".mozilla" / "firefox",
    HOME / ".librewolf",
    HOME / ".waterfox",
    HOME / ".zen",
)
_FIREFOX_GLOBS = (
    str(HOME / "snap" / "firefox*" / "common" / ".mozilla" / "firefox"),
    str(HOME / ".var" / "app" / "*" / ".mozilla" / "firefox"),
)

_HTTP3_PREF = "network.http.http3.enable"


@dataclass
class QuicStatus:
    """What happens to a browser's HTTP/3 traffic right now."""
    filtered: bool = False          # AdGuard sees QUIC (or blocks it)
    headline: str = ""
    details: list[str] = field(default_factory=list)
    firefox_profiles: list[Path] = field(default_factory=list)
    firefox_disabled: int = 0       # profiles with HTTP/3 switched off


def quic_blocked_by_firewall() -> bool:
    """True when outgoing UDP/443 is rejected for every address family we have.

    A drop/reject in the OUTPUT hook surfaces as EPERM on send. Probing
    loopback keeps the packet on this machine, and adguard-cli's own chain
    returns early for 127.0.0.0/8, so this measures the firewall, not AdGuard.
    A rule that only covers IPv4 leaves QUIC usable over IPv6, so both have to
    be blocked before we tell the user QUIC is impossible. Rules restricted to
    specific destinations are not detected – we then report "not blocked",
    which is the cautious answer.
    """
    reachable = 0
    for family, address in ((socket.AF_INET, ("127.0.0.1", 443)),
                            (socket.AF_INET6, ("::1", 443, 0, 0))):
        try:
            with socket.socket(family, socket.SOCK_DGRAM) as sock:
                sock.sendto(b"", address)
        except PermissionError:
            continue          # blocked for this family
        except OSError:
            continue          # family unavailable – can't be used to bypass
        reachable += 1
    return reachable == 0


def chromium_policy_blocks_quic() -> list[str]:
    """Managed-policy files that set QuicAllowed=false."""
    found = []
    for pattern in _POLICY_FILES:
        for path in sorted(glob.glob(pattern)):
            try:
                data = json.loads(Path(path).read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                logger.debug("Could not read policy %s: %s", path, exc)
                continue
            if isinstance(data, dict) and data.get("QuicAllowed") is False:
                found.append(path)
    for path in _FIREFOX_POLICIES:
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict):
            continue
        policies = data.get("policies")
        prefs = policies.get("Preferences") if isinstance(policies, dict) else None
        pref = prefs.get(_HTTP3_PREF) if isinstance(prefs, dict) else None
        if pref is False or (isinstance(pref, dict) and pref.get("Value") is False):
            found.append(path)
    return found


def firefox_profiles() -> list[Path]:
    """Every Gecko profile directory found via profiles.ini."""
    roots = [str(r) for r in _FIREFOX_ROOTS]
    for pattern in _FIREFOX_GLOBS:
        roots.extend(sorted(glob.glob(pattern)))
    profiles: list[Path] = []
    for root in roots:
        ini = Path(root) / "profiles.ini"
        if not ini.is_file():
            continue
        # interpolation=None: a '%' in a profile path is data, not a format
        parser = configparser.ConfigParser(interpolation=None)
        try:
            parser.read(ini, encoding="utf-8")
        except (OSError, configparser.Error, UnicodeDecodeError) as exc:
            logger.debug("Could not read %s: %s", ini, exc)
            continue
        for section in parser.sections():
            if not section.lower().startswith("profile"):
                continue
            rel = parser.get(section, "Path", fallback="")
            if not rel:
                continue
            relative = parser.get(section, "IsRelative", fallback="1") == "1"
            path = (ini.parent / rel) if relative else Path(rel)
            if path.is_dir():
                profiles.append(path)
    return profiles


# user_pref("network.http.http3.enable", false);  – and nothing else
_PREF_RE = re.compile(
    r'^\s*user_pref\s*\(\s*["\']' + re.escape(_HTTP3_PREF) + r'["\']\s*,\s*(true|false)\s*\)\s*;',
    re.IGNORECASE,
)


def _pref_value(path: Path) -> bool | None:
    """Last value assigned to the HTTP/3 pref in a prefs file, if any.

    Only real assignments count – a commented-out line or a "true" inside a
    trailing comment must not change the answer.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    value = None
    for line in text.splitlines():
        match = _PREF_RE.match(line)
        if match:
            value = match.group(1).lower() == "true"
    return value


def firefox_http3_disabled(profile: Path) -> bool:
    """True when this profile has HTTP/3 switched off.

    user.js is applied over prefs.js at every start, so it decides.
    """
    for name in ("user.js", "prefs.js"):
        value = _pref_value(profile / name)
        if value is not None:
            return value is False
    return False


def set_firefox_http3(profile: Path, enabled: bool) -> tuple[bool, str]:
    """Write the HTTP/3 pref into a profile's user.js.

    Disabling writes the pref as false; enabling writes it as true rather than
    dropping the line – Firefox keeps the old value in prefs.js otherwise.
    """
    from ._allowlist import write_atomic

    user_js = profile / "user.js"
    try:
        lines = user_js.read_text(encoding="utf-8").splitlines() if user_js.exists() else []
    except (OSError, ValueError) as exc:   # ValueError: not UTF-8
        return False, str(exc)
    kept = [ln for ln in lines if not _PREF_RE.match(ln)]
    kept.append(f'user_pref("{_HTTP3_PREF}", {"true" if enabled else "false"});')
    try:
        write_atomic(user_js, "\n".join(kept) + "\n")
    except OSError as exc:
        return False, str(exc)
    return True, ""


def status(running: bool | None = None) -> QuicStatus:
    """Work out what happens to HTTP/3 traffic and describe it.

    *running* is whether adguard-cli is actually up; auto mode only redirects
    UDP 443 while the service (and its iptables rules) exist.
    """
    result = QuicStatus()
    data = _load_yaml()
    if not isinstance(data, dict):
        data = {}
    mode = str(data.get("proxy_mode", "") or "").lower()
    https = data.get("https_filtering") if isinstance(data.get("https_filtering"), dict) else {}

    def flag(key: str) -> bool:
        # Same reading as the configuration dialog: YAML 1.1 gives ints for
        # 0/1, and anything unexpected falls back to the default (on).
        value = https.get(key)
        if isinstance(value, (bool, int)):
            return bool(value)
        return True

    https_on = flag("enabled")
    http3_filtering = flag("http3_filtering_enabled")

    result.firefox_profiles = firefox_profiles()
    result.firefox_disabled = sum(1 for p in result.firefox_profiles if firefox_http3_disabled(p))
    firewall = quic_blocked_by_firewall()
    policies = chromium_policy_blocks_quic()

    if not data:
        result.headline = _t("Could not read proxy.yaml – HTTP/3 state unknown.")
    elif mode == "auto" and https_on and running is False:
        result.headline = _t("AdGuard is not running – nothing is filtered.")
    elif mode == "auto" and https_on:
        result.filtered = True
        result.headline = (
            _t("HTTP/3 is filtered by AdGuard.") if http3_filtering
            else _t("HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.")
        )
        result.details.append(_t("Proxy mode: auto – UDP port 443 is redirected to AdGuard."))
    elif https_on:
        result.headline = _t(
            "Browsers can bypass AdGuard over HTTP/3 (UDP 443)."
        )
        result.details.append(
            _t("Proxy mode: {} – only traffic sent through the proxy is filtered, "
               "and browsers do not send QUIC through it.", mode or _t("unknown"))
        )
    else:
        result.headline = _t("HTTPS filtering is off – nothing is filtered.")

    if firewall:
        if not result.filtered:
            result.headline = _t("HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.")
        result.filtered = True
        result.details.append(_t("A firewall rule rejects outgoing UDP 443, so QUIC cannot be used."))
    if policies:
        # A managed policy covers the browsers it applies to, not the machine –
        # so it is worth reporting but must not turn the verdict green.
        result.details.append(_t("Browser policy disables QUIC: {}", ", ".join(policies)))
    apps = data.get("apps")
    if result.filtered and isinstance(apps, list):
        bypassed = [
            str(a.get("name")) for a in apps
            if isinstance(a, dict) and str(a.get("action", "")).startswith("bypass") and a.get("name")
        ]
        if bypassed:
            result.details.append(
                _t("Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}",
                   ", ".join(bypassed[:8]))
            )
    if result.firefox_profiles:
        result.details.append(
            _t("Firefox-family profiles with HTTP/3 switched off: {} of {}",
               result.firefox_disabled, len(result.firefox_profiles))
        )
    return result
