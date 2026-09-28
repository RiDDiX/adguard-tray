"""AdGuard VPN CLI next to AdGuard CLI: find it, read its mode, switch it to SOCKS5.

AdGuard Tray never connects the VPN, logs in or runs it as root. It only
watches the one combination AdGuard documents as unsupported – the VPN in TUN
mode while adguard-cli filters in automatic mode, a routing loop – and offers
AdGuard's own fix: the VPN in SOCKS5 mode as adguard-cli's outbound proxy.
https://adguard.com/kb/adguard-for-linux/vpn-cli-interaction/
"""

import fnmatch
import os
import re
import shutil
from dataclasses import dataclass

from .cli import _run

BINARY = "adguardvpn-cli"
_OPT_BINARY = "/opt/adguardvpn_cli/adguardvpn-cli"   # official script without the symlink
INSTALL_SCRIPT = "https://raw.githubusercontent.com/AdguardTeam/AdGuardVPNCLI/HEAD/scripts/release/install.sh"
AUR_PACKAGE = "adguardvpn-cli-bin"

# adguard-cli's own default rule: apps with "vpn" in the name skip the outbound
# proxy, so the VPN's traffic does not loop back into itself.
VPN_RULE = {"name": "*vpn*", "action": "bypass", "skip_outbound_proxy": True}

# `config show` prints tab-indented "Key: value" lines, e.g. "\tMode: tun".
_FIELD_RE = re.compile(r"^\s*(mode|socks port|socks host)\s*:[ \t]*(\S*)[ \t]*$", re.I | re.M)


@dataclass
class VpnConfig:
    mode: str = ""              # "tun", "socks", or "" when the output was not understood
    socks_host: str = "127.0.0.1"
    socks_port: int = 1080


def find() -> str:
    """Path of adguardvpn-cli, or "" when it is not installed."""
    path = shutil.which(BINARY)
    if path:
        return path
    return _OPT_BINARY if os.access(_OPT_BINARY, os.X_OK) else ""


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
    # Empty stdin: a question it might ask ends at once instead of waiting 15 s.
    code, out, err = _run(args, timeout=15, stdin_data="")
    config = parse_config(out) if code == 0 else None
    if config is None or not config.mode:
        return None, (err or out).strip()
    return config, ""


def read_config(binary: str) -> tuple[VpnConfig | None, str]:
    """The VPN's mode and SOCKS5 address. Works without logging in."""
    return _config([binary, "config", "show"])


def set_socks_mode(binary: str) -> tuple[VpnConfig | None, str]:
    """Switch the VPN to SOCKS5 mode; it applies the next time the VPN connects."""
    return _config([binary, "config", "set-mode", "socks"])


def skips_outbound_proxy(apps, names: tuple[str, ...]) -> bool:
    """Whether the first app rule matching the VPN keeps it off the outbound proxy."""
    for rule in apps if isinstance(apps, list) else []:
        if not isinstance(rule, dict):
            continue
        pattern = str(rule.get("name", "")).lower()
        if pattern and any(fnmatch.fnmatchcase(name.lower(), pattern) for name in names):
            return bool(rule.get("skip_outbound_proxy", False))
    return False
