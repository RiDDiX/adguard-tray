"""
Desktop notifications via notify-send (libnotify).
Falls back to QSystemTrayIcon.showMessage() if notify-send is unavailable
or reports an error.

notify-send works on KDE Plasma (via plasma-integration) and Hyprland
(via dunst, mako, or any notification daemon).
"""

import logging
import subprocess
import threading

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QSystemTrayIcon

logger = logging.getLogger(__name__)

APP_NAME = "AdGuard Tray"
APP_ICON = "security-high"  # XDG icon name, available in Breeze and most themes

_QT_ICON = {
    "low":      QSystemTrayIcon.MessageIcon.Information,
    "normal":   QSystemTrayIcon.MessageIcon.Information,
    "critical": QSystemTrayIcon.MessageIcon.Critical,
}


class _Relay(QObject):
    """Hops the fallback from the notify-send watcher thread to the GUI thread."""
    fallback = pyqtSignal(object, str, str, str)  # tray, title, body, urgency


_relay: _Relay | None = None


def _qt_bubble(tray: QSystemTrayIcon, title: str, body: str, urgency: str) -> None:
    if tray.isVisible():
        tray.showMessage(title, body, _QT_ICON.get(urgency, _QT_ICON["normal"]), 5000)


def notify(
    title: str,
    body: str,
    urgency: str = "normal",          # low | normal | critical
    tray: QSystemTrayIcon | None = None,
) -> None:
    """Send a desktop notification. Never raises, never blocks the caller (GUI thread)."""
    global _relay
    if _relay is None:
        _relay = _Relay()
        _relay.fallback.connect(_qt_bubble)

    def fallback() -> None:
        if tray is not None:
            _relay.fallback.emit(tray, title, body, urgency)

    try:
        proc = subprocess.Popen(
            [
                "notify-send",
                "--app-name", APP_NAME,
                "--icon", APP_ICON,
                "--urgency", urgency,
                title,
                body,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        logger.debug("notify-send not found – falling back to Qt tray bubble")
        fallback()
        return
    except OSError as exc:
        logger.warning("notify-send failed: %s – falling back", exc)
        fallback()
        return

    def watch() -> None:
        # A stalled daemon must not freeze the GUI, so wait off-thread and
        # only then decide about the fallback.
        try:
            _, err = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            logger.warning("notify-send timed out – falling back")
            fallback()
            return
        if proc.returncode != 0:
            logger.debug("notify-send exited %d (%s) – falling back",
                         proc.returncode, err.decode("utf-8", errors="replace").strip())
            fallback()

    threading.Thread(target=watch, name="notify-send", daemon=True).start()
