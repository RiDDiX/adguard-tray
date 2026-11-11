"""AdGuard VPN CLI next to AdGuard CLI: find it, read and switch its mode,
read its account, locations and connection, connect and disconnect (the VPN
page starts `login` itself).

AdGuard Tray never runs the CLI as root: in TUN mode the CLI asks for the
password through sudo itself, so the VPN page starts that connect in a
terminal. It also watches the one combination AdGuard documents as
unsupported – the VPN in TUN mode while adguard-cli filters in automatic
mode, a routing loop – and offers AdGuard's own fix: the VPN in SOCKS5 mode
as adguard-cli's outbound proxy.
https://adguard.com/kb/adguard-for-linux/vpn-cli-interaction/
"""

import fnmatch
import os
import re
import shutil
import threading
from dataclasses import dataclass

from .cli import _cli_error, _run, _strip_ansi, mask_license
from .i18n import _t
from .proxy_settings import get

BINARY = "adguardvpn-cli"
_OPT_BINARY = "/opt/adguardvpn_cli/adguardvpn-cli"   # official script without the symlink
INSTALL_SCRIPT = "https://raw.githubusercontent.com/AdguardTeam/AdGuardVPNCLI/HEAD/scripts/release/install.sh"
AUR_PACKAGE = "adguardvpn-cli-bin"

OUTBOUND = "outbound_proxy"

# adguard-cli's own default rule: apps with "vpn" in the name skip the outbound
# proxy, so the VPN's traffic does not loop back into itself.
VPN_RULE = {"name": "*vpn*", "action": "bypass", "skip_outbound_proxy": True}

# `config show` prints tab-indented "Key: value" lines, e.g. "\tMode: tun".
_FIELD_RE = re.compile(r"^\s*(mode|socks port|socks host)\s*:[ \t]*(\S*)[ \t]*$", re.I | re.M)
_LINK_RE = re.compile(r"https://\S+(?=\s)")     # complete only once whitespace follows
# "You can ... by running `adguardvpn-cli ...`": terminal advice, with the path the CLI was started as.
_HINT_RE = re.compile(rf"`[^`]*{BINARY}\b")
# list-locations: ISO, country, city and ping, at least two spaces apart.
_LOCATION_RE = re.compile(r"^([A-Z]{2})\s{2,}(.+?)\s{2,}(.+?)(?:\s{2,}(\S+))?\s*$")
NOT_LOGGED_IN = 11          # exit code of every command when logged out
NOT_RUNNING = 14            # disconnect when nothing is connected
# "VPN active, but status unavailable": while the service starts, or when its socket is not accessible.
STATUS_UNAVAILABLE = 10
DISCONNECTED = "VPN is disconnected"
_NOISE = ("Log is being written to:", "Config has been updated", "Disconnecting from current location")

# Two calls at once can log the user out (AdGuardVPNCLI#98).
_lock = threading.Lock()


@dataclass
class VpnConfig:
    mode: str = ""              # "tun", "socks", or "" when the output was not understood
    socks_host: str = "127.0.0.1"
    socks_port: int = 1080


@dataclass
class VpnStatus:
    logged_in: bool
    text: str = ""              # the CLI's status lines without terminal hints
    error: str = ""             # "" when the call worked


@dataclass
class Location:
    iso: str
    country: str
    city: str
    ping: str = ""              # as printed; other plans may print something else than ms


def find() -> str:
    """Path of adguardvpn-cli, or "" when it is not installed."""
    path = shutil.which(BINARY)
    if path:
        return path
    return _OPT_BINARY if os.access(_OPT_BINARY, os.X_OK) else ""


def _call(args: list[str], timeout: int = 15) -> tuple[int, str, str]:
    with _lock:
        return _run(args, timeout=timeout)


def _noise(line: str) -> bool:
    return bool(_HINT_RE.search(line)) or line.startswith(_NOISE) or "Upgrade at http" in line


def _text(out: str) -> str:
    return "\n".join(line for line in out.splitlines() if not _noise(line)).strip()


def _error(code: int, out: str, err: str) -> str:
    return _cli_error(err, _text(out)) or _t("adguardvpn-cli failed with exit code {}", code)


def is_disconnected(text: str) -> bool:
    return any(line.startswith(DISCONNECTED) for line in text.splitlines())


def is_connected(text: str) -> bool:
    return any(line.startswith("Connected to") for line in text.splitlines())


def parse_config(text: str) -> VpnConfig:
    config = VpnConfig()
    for key, value in _FIELD_RE.findall(text):
        key = key.lower()
        if key == "mode":
            config.mode = value.lower()
        elif key == "socks host" and value:
            # A VPN listening on every interface is still reached locally.
            config.socks_host = "127.0.0.1" if value in ("0.0.0.0", "::", "[::]") else value
        elif key == "socks port" and value.isdigit():
            config.socks_port = int(value)
    return config


def _config(args: list[str]) -> tuple[VpnConfig | None, str]:
    code, out, err = _call(args)
    config = parse_config(out) if code == 0 else None
    if config is None or not config.mode:
        return None, _error(code, out, err)
    return config, ""


def read_config(binary: str) -> tuple[VpnConfig | None, str]:
    """The VPN's mode and SOCKS5 address. Works without logging in."""
    return _config([binary, "config", "show"])


def set_mode(binary: str, mode: str) -> tuple[VpnConfig | None, str]:
    """Switch the VPN to "socks" or "tun"; it applies the next time the VPN connects."""
    # What set-mode prints is not documented; the SOCKS address comes from show.
    code, out, err = _call([binary, "config", "set-mode", mode])
    if code != 0:
        return None, _error(code, out, err)
    config, error = read_config(binary)
    if config is not None and config.mode != mode:
        # Exit 0 without switching, e.g. when it wants a login first.
        return None, _error(code, out, err)
    return config, error


def change_mode(binary: str, mode: str) -> tuple[VpnConfig | None, str, bool]:
    """set_mode on a disconnected VPN; the bool says whether it had to disconnect.
    set-mode on a connected VPN restarts it in the new mode, and a TUN restart fails without a terminal."""
    current = status(binary)
    stopped = current.logged_in and not is_disconnected(current.text)
    if stopped:
        ok, message = disconnect(binary)
        if not ok:
            return None, message, False
    config, error = set_mode(binary, mode)
    return config, error, stopped


def status(binary: str) -> VpnStatus:
    """Whether the user is logged in, and what the CLI says about the connection."""
    code, out, err = _call([binary, "status"])
    if code in (0, STATUS_UNAVAILABLE):
        return VpnStatus(True, _text(out))
    if code == NOT_LOGGED_IN:
        return VpnStatus(False, _text(out))
    return VpnStatus(False, _text(out), _error(code, out, err))


def logout(binary: str) -> tuple[bool, str]:
    code, out, err = _call([binary, "logout"])
    if code in (0, NOT_LOGGED_IN):
        return True, ""
    return False, _error(code, out, err)


def license_info(binary: str) -> tuple[str, str]:
    """The account lines of `license`, e.g. the plan and the traffic left, e-mail masked."""
    code, out, err = _call([binary, "license"])
    # Connected, it may fail (exit 12) after "Logged in as ..." and say so in its text.
    text = mask_license(_text(out))
    return (text, "") if text else ("", _error(code, out, err))


def locations(binary: str) -> tuple[list[Location], str]:
    code, out, err = _call([binary, "list-locations"])
    if code != 0:
        return [], _error(code, out, err)
    return [Location(*m.groups("")) for m in map(_LOCATION_RE.match, out.splitlines()) if m], ""


def connect_command(binary: str, location: str | None) -> list[str]:
    """None: the fastest location; else a city, country or ISO code."""
    return [binary, "connect", "-l", location] if location else [binary, "connect", "-f"]


def connect(binary: str, location: str | None) -> tuple[bool, str]:
    """Connect or switch location. Read status afterwards either way: a failed
    switch leaves the VPN disconnected."""
    code, out, err = _call(connect_command(binary, location), timeout=60)
    return (True, _text(out)) if code == 0 else (False, _error(code, out, err))


def disconnect(binary: str) -> tuple[bool, str]:
    code, out, err = _call([binary, "disconnect"])
    return (True, _text(out)) if code in (0, NOT_RUNNING) else (False, _error(code, out, err))


def login_error(code: int, output: str) -> str:
    """What a failed `login` printed, or its exit code."""
    return _error(code, _strip_ansi(output), "")


def login_link(output: str) -> str | None:
    """The device-code link `login` prints, or None while it has not come yet."""
    match = _LINK_RE.search(_strip_ansi(output))
    return match.group(0) if match else None


def skips_outbound_proxy(apps, names: tuple[str, ...]) -> bool:
    """Whether the first app rule matching the VPN keeps it off the outbound proxy."""
    for rule in apps if isinstance(apps, list) else []:
        if not isinstance(rule, dict):
            continue
        pattern = str(rule.get("name", "")).lower()
        if pattern and any(fnmatch.fnmatchcase(name.lower(), pattern) for name in names):
            return get(rule, "skip_outbound_proxy", default=False)
    return False


def route_through(settings, config: VpnConfig, binary: str) -> None:
    """Point adguard-cli's outbound proxy at the VPN's SOCKS5 port, as pending edits."""
    settings.set((OUTBOUND, "enabled"), True, False)
    settings.set((OUTBOUND, "mode"), "SOCKS5", "HTTP")
    settings.set((OUTBOUND, "host"), config.socks_host, "localhost")
    settings.set((OUTBOUND, "port"), config.socks_port, 3128)
    # Without this rule the VPN's own traffic would go into the proxy it is.
    apps = settings.value(("apps",), [])
    if not skips_outbound_proxy(apps, (BINARY, binary)):
        settings.set(("apps",), [dict(VPN_RULE), *apps], [])


def stop_routing(settings) -> None:
    settings.set((OUTBOUND, "enabled"), False, False)


def routed(settings, config: VpnConfig | None) -> bool:
    """Whether adguard-cli's outbound proxy is the VPN's SOCKS5 port."""
    return (config is not None and config.mode == "socks"
            and settings.value((OUTBOUND, "enabled"), False) is True
            and settings.value((OUTBOUND, "mode"), "HTTP") == "SOCKS5"
            and settings.value((OUTBOUND, "host"), "localhost") == config.socks_host
            and settings.value((OUTBOUND, "port"), 3128) == config.socks_port)


def loops(settings, config: VpnConfig | None) -> bool:
    """The VPN in TUN mode while adguard-cli filters in automatic mode."""
    return (config is not None and config.mode == "tun" and settings.available
            and settings.value(("proxy_mode",), "auto") == "auto")
