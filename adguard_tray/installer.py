"""Install AdGuard's CLIs from the user's own terminal.

Never as root from here: AdGuard's scripts ask questions and call sudo
themselves, which needs a terminal, and AUR helpers refuse to run as root.
The window only opens a terminal with the command; the user sees every prompt.
"""

import os
import platform
import shlex
import shutil

from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QApplication

from . import vpn
from .i18n import _t
from .updates import aur_helper

# product: (official install script, AUR package)
PRODUCTS = {
    "adguard-cli": ("https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh",
                    "adguard-cli-bin"),
    vpn.BINARY: (vpn.INSTALL_SCRIPT, vpn.AUR_PACKAGE),
}

# Terminal, and the arguments that make it run a command (each checked by a real run).
# $TERMINAL comes first, then the desktop's own, then xdg-terminal-exec, then whatever
# is installed. ghostty: never "-e --", it would run "--".
_TERMINALS = {
    "xdg-terminal-exec": ["--"],
    "konsole": ["-e"],
    "ptyxis": ["--"],
    "kgx": ["--"],
    "gnome-terminal": ["--"],
    "xfce4-terminal": ["-x"],
    "ghostty": ["-e"],
    "kitty": ["--"],
    "alacritty": ["-e"],
    "foot": [],
    "wezterm": ["start", "--"],
    "xterm": ["-e"],
}
_DESKTOP_FIRST = {"KDE": ["konsole"], "GNOME": ["ptyxis", "kgx", "gnome-terminal"], "XFCE": ["xfce4-terminal"]}


def _is_arch() -> bool:
    try:
        info = platform.freedesktop_os_release()
    except OSError:
        return False
    return "arch" in {info.get("ID", ""), *info.get("ID_LIKE", "").split()}


def install_command(product: str) -> str:
    script, package = PRODUCTS[product]
    # The AUR packages are x86_64 only; pacman then owns the files and updates them.
    helper = aur_helper() if _is_arch() and platform.machine() == "x86_64" else ""
    if helper:
        return f"{helper} -S {package}"
    return f"curl -fsSL {script} | sh -s -- -v"


def terminal_argv(script: str) -> list[str]:
    """argv that runs *script* with sh in a new terminal window, or [] if none is found."""
    names = []
    chosen = os.environ.get("TERMINAL", "").strip()
    # Only a terminal whose arguments are known: several take -e as ONE string.
    if os.path.basename(chosen) in _TERMINALS:
        names.append(chosen)
    for desktop in os.environ.get("XDG_CURRENT_DESKTOP", "").upper().split(":"):
        names += _DESKTOP_FIRST.get(desktop, [])
    names += list(_TERMINALS)
    for name in names:
        path = shutil.which(name)
        if path:
            return [path, *_TERMINALS[os.path.basename(name)], "sh", "-c", script]
    return []


def open_in_terminal(command: str) -> bool:
    # Keep the window open: the user has to read how it went.
    done = _t("Press Enter to close this window.")
    argv = terminal_argv(f"{command}; echo; printf '%s ' {shlex.quote(done)}; read _")
    return bool(argv) and QProcess.startDetached(argv[0], argv[1:])[0]


def start_install(page, product: str) -> None:
    """Open a terminal with the install command, or put it on the clipboard."""
    command = install_command(product)
    if open_in_terminal(command):
        # The command under Details too, in case no window shows up.
        page.banner.show_message(_t("Finish the installation in the terminal, then press Refresh."), "info",
                                 details=command)
        return
    clipboard = QApplication.clipboard()
    if clipboard:
        clipboard.setText(command)
    page.banner.show_message(
        _t("No terminal app was found. The install command is on the clipboard: paste it into a terminal."),
        "warning", details=command)
