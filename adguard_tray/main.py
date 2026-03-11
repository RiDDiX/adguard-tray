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
import os
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon

from .cli import AdGuardCLI
from .config import load_config
from .i18n import _t
from .tray import AdGuardTray

LOG_DIR = Path.home() / ".local" / "share" / "adguard-tray"
LOG_FILE = LOG_DIR / "adguard-tray.log"


def _setup_logging(level: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    numeric = getattr(logging, level.upper(), logging.INFO)
    fmt = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    handlers: list[logging.Handler] = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ]
    logging.basicConfig(level=numeric, format=fmt, datefmt=datefmt, handlers=handlers)


def main() -> None:
    config = load_config()
    _setup_logging(config.log_level)
    logger = logging.getLogger(__name__)
    logger.info("AdGuard Tray v%s starting", _get_version())
    logger.debug("Log file: %s", LOG_FILE)

    # Qt application
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("AdGuard Tray")
    app.setApplicationDisplayName("AdGuard Tray")
    app.setApplicationVersion(_get_version())
    # Stay alive when all windows are closed (tray-only app)
    app.setQuitOnLastWindowClosed(False)

    # Check system tray availability
    if not QSystemTrayIcon.isSystemTrayAvailable():
        logger.error("System tray not available")
        _fatal_dialog(
            _t("System tray not available"),
            _t(
                "The system tray is not available in this desktop environment.\n\n"
                "On Hyprland: waybar with the [tray] module enabled or sfwbar is required.\n"
                "On KDE Plasma it should work out of the box."
            ),
        )
        sys.exit(1)

    # Resolve executable path for autostart .desktop generation
    exec_path = _resolve_exec()
    logger.debug("Resolved exec path: %s", exec_path)

    cli = AdGuardCLI()
    tray = AdGuardTray(app, cli, config, exec_path)  # noqa: F841 (kept alive by app)

    logger.info("Entering event loop")
    sys.exit(app.exec())


def _get_version() -> str:
    from . import __version__
    return __version__


def _resolve_exec() -> str:
    """Best-effort: find how this script was launched."""
    # Installed via pipx / venv entry point
    if (ep := Path(sys.argv[0])).exists():
        return str(ep.resolve())
    # Fallback
    return f"{sys.executable} {Path(__file__).parent.parent / 'adguard-tray.py'}"


def _fatal_dialog(title: str, message: str) -> None:
    """Show a modal error dialog when the tray can't start."""
    try:
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.exec()
    except Exception:
        print(f"FATAL: {title}\n{message}", file=sys.stderr)
