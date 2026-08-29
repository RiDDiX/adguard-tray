"""
Entry point for adguard-tray.

Wayland / platform notes:
  - Qt6 auto-detects Wayland via WAYLAND_DISPLAY (no manual override needed).
  - QSystemTrayIcon uses the StatusNotifierItem (SNI) DBus protocol on Wayland,
    which KDE Plasma supports natively.
  - On Hyprland, SNI works with waybar (tray module) or sfwbar.
  - On X11, classic XEMBED tray is used transparently by Qt.
"""

import logging
import logging.handlers
import shutil
import signal
import sys
from pathlib import Path

from PyQt6.QtCore import QLockFile, QTimer
from PyQt6.QtWidgets import QApplication, QMessageBox, QPushButton, QSystemTrayIcon

from .cli import AdGuardCLI
from .config import load_config
from .i18n import _t
from .icons import icon_active
from .notifications import notify
from .tray import AdGuardTray

LOG_DIR = Path.home() / ".local" / "share" / "adguard-tray"
LOG_FILE = LOG_DIR / "adguard-tray.log"

CONFIG_DIR = Path.home() / ".config" / "adguard-tray"
LOCK_FILE = CONFIG_DIR / "adguard-tray.lock"


def _setup_logging(level: str) -> None:
    numeric = getattr(logging, level.upper(), logging.INFO)
    fmt = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]

    # Best-effort file logging — read-only home or full disk shouldn't kill
    # the tray before the user even sees the icon.
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        handlers.append(
            logging.handlers.RotatingFileHandler(
                LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
            )
        )
    except OSError as exc:
        print(f"adguard-tray: could not open log file ({exc}); stdout only", file=sys.stderr)

    logging.basicConfig(level=numeric, format=fmt, datefmt=datefmt, handlers=handlers)


USAGE = """\
Usage: adguard-tray [options]

System tray monitor and controller for adguard-cli.

Options:
  -V, --version   print the version and exit
  --check-update  check whether a newer release exists and exit
  --update        install a newer release (only for ~/.local installations)
  -h, --help      print this help and exit

Config:  ~/.config/adguard-tray/config.json
Log:     ~/.local/share/adguard-tray/adguard-tray.log
"""


def main() -> None:
    if "--version" in sys.argv or "-V" in sys.argv:
        print(f"adguard-tray {_get_version()}")
        sys.exit(0)
    if "--help" in sys.argv or "-h" in sys.argv:
        print(USAGE, end="")
        sys.exit(0)
    if "--check-update" in sys.argv or "--update" in sys.argv:
        sys.exit(_run_update("--update" in sys.argv))

    # Logging first: a broken config.json must end up in the log file, not in
    # a stderr nobody reads under autostart.
    _setup_logging("INFO")
    logger = logging.getLogger(__name__)
    config = load_config()
    logging.getLogger().setLevel(getattr(logging, config.log_level.upper(), logging.INFO))
    logger.info("AdGuard Tray v%s starting", _get_version())
    logger.debug("Log file: %s", LOG_FILE)

    # PyQt turns an unhandled exception in a slot into qFatal(), i.e. the tray
    # dies on the first hiccup. Log it and keep running instead.
    sys.excepthook = lambda exc_type, exc, tb: logger.error(
        "Unhandled exception", exc_info=(exc_type, exc, tb)
    )

    # Qt application
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("AdGuard Tray")
    app.setApplicationDisplayName("AdGuard Tray")
    app.setApplicationVersion(_get_version())
    # Lets the compositor match windows to the .desktop file (icon, grouping,
    # window rules); without it Wayland falls back to "python3".
    app.setDesktopFileName("adguard-tray")
    app.setWindowIcon(icon_active())
    # Stay alive when all windows are closed (tray-only app)
    app.setQuitOnLastWindowClosed(False)

    # Single-instance guard – refuse to start a second tray
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        logger.warning("Could not create %s: %s", CONFIG_DIR, exc)
    lock = QLockFile(str(LOCK_FILE))
    lock.setStaleLockTime(0)  # treat only live PIDs as holders
    # Waiting a few seconds instead of failing at once: after an in-app update
    # the new process starts while the old one is still shutting down.
    if not lock.tryLock(5000):
        logger.warning("Another adguard-tray instance is already running")
        _info_dialog(
            _t("AdGuard Tray is already running"),
            _t("Only one instance can run at a time. Check your system tray."),
        )
        sys.exit(0)
    # Keep the lock object alive for the app's lifetime
    app._adguard_lock = lock  # type: ignore[attr-defined]

    # System tray availability is checked but not enforced. Some bars
    # (quickshell, niri's, occasionally waybar) register the SNI host a few
    # seconds after the user session starts. Qt's QSystemTrayIcon registers
    # itself over D-Bus, so the icon will appear once the host shows up —
    # we just need to not exit before then. See issue #3.
    if not QSystemTrayIcon.isSystemTrayAvailable():
        logger.warning(
            "System tray host not registered yet — bar may still be loading. "
            "Tray icon will appear once a host (waybar tray, plasmashell, "
            "GNOME AppIndicator, …) shows up."
        )

        def _late_check() -> None:
            if not QSystemTrayIcon.isSystemTrayAvailable():
                logger.warning(
                    "Still no system tray host after 30s — check that your "
                    "bar exposes one (waybar tray module, GNOME AppIndicator "
                    "extension, …)."
                )
                # No icon to click, so the notification daemon is the only way
                # left to tell the user the app is running at all.
                notify(
                    "AdGuard Tray",
                    _t("No system tray found. AdGuard Tray is running without "
                       "an icon — enable a tray/AppIndicator in your panel."),
                )

        QTimer.singleShot(30_000, _late_check)

    # Resolve executable path for autostart .desktop generation
    exec_path = _resolve_exec()
    logger.debug("Resolved exec path: %s", exec_path)

    cli = AdGuardCLI(binary=config.adguard_cli_path)
    tray = AdGuardTray(app, cli, config, exec_path)

    # Clean shutdown: stop polling timer before Qt tears things down
    app.aboutToQuit.connect(tray.shutdown)

    # Let Ctrl+C in the terminal quit the app instead of being swallowed by Qt
    signal.signal(signal.SIGINT, lambda *_: app.quit())
    signal.signal(signal.SIGTERM, lambda *_: app.quit())
    # Kick the Python interpreter periodically so signal handlers run
    _sigtick = QTimer()
    _sigtick.start(500)
    _sigtick.timeout.connect(lambda: None)

    _dependency_doctor(cli)

    logger.info("Entering event loop")
    sys.exit(app.exec())


def _run_update(install: bool) -> int:
    """`--check-update` / `--update`, without starting the GUI."""
    from .i18n import _t
    from .updates import check, detect_install, self_update, update_command

    release, newer, error = check()
    if release is None:
        print(error or _t("Could not check for updates."))
        return 1
    if not newer:
        print(_t("You are running the latest version ({}).", _get_version()))
        return 0
    print(_t("Version {} is available (you have {}).", release.version, _get_version()))

    where = detect_install()
    command = update_command(where)
    if not install:
        print(_t("Update with: {}", command) if command else release.url)
        return 0
    if not where.can_self_update:
        print(_t("This installation is managed elsewhere: {}", command or release.url))
        return 1
    ok, message = self_update(release, where)
    print(message)
    return 0 if ok else 1


def _get_version() -> str:
    from . import __version__
    return __version__


def _resolve_exec() -> list[str]:
    """Best-effort argv of how this app was launched (for the autostart entry)."""
    ep = Path(sys.argv[0])
    if ep.exists() and ep.suffix != ".py":
        # Installed console script / launcher – directly executable
        return [str(ep.resolve())]
    script = ep.resolve() if ep.exists() else Path(__file__).parent.parent / "adguard-tray.py"
    return [sys.executable, str(script)]


_INSTALL_CMD = "curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v"


_doctor_box: QMessageBox | None = None


def _dependency_doctor(cli: AdGuardCLI) -> None:
    """Show a dialog if adguard-cli is missing.

    Non-modal on purpose: a nested exec() loop would swallow app.quit(),
    so Quit / Ctrl+C would be dead while the box is open.
    """
    global _doctor_box
    binary = cli.BINARY
    if shutil.which(binary):
        return
    logger = logging.getLogger(__name__)
    logger.warning("adguard-cli binary not found: %r", binary)

    msg = QMessageBox()
    msg.setWindowTitle(_t("adguard-cli not found"))
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setText(_t(
        "adguard-cli could not be found on this system.\n\n"
        "Recommended install method (official):\n"
        "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
        "Alternative (Arch Linux AUR):\n"
        "  paru -S adguard-cli-bin\n\n"
        "Tray loads, but start/stop won't work until adguard-cli is installed."
    ))
    btn_copy = QPushButton(_t("Copy install command"))
    btn_continue = QPushButton(_t("Continue"))
    msg.addButton(btn_copy, QMessageBox.ButtonRole.ActionRole)
    msg.addButton(btn_continue, QMessageBox.ButtonRole.AcceptRole)
    msg.setDefaultButton(btn_continue)
    # Without an escape button QMessageBox refuses closeEvent, and Qt 6's
    # quit() gives up when a window refuses to close.
    msg.setEscapeButton(btn_continue)

    def _clicked(btn) -> None:
        global _doctor_box
        if btn is btn_copy:
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText(_INSTALL_CMD)
        _doctor_box = None

    msg.buttonClicked.connect(_clicked)
    _doctor_box = msg  # keep alive – nothing else references the box
    msg.show()


def _info_dialog(title: str, message: str) -> None:
    try:
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
    except Exception:
        print(f"{title}: {message}", file=sys.stderr)
