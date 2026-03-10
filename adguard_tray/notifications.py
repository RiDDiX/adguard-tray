"""
Desktop notifications via notify-send (libnotify).
Falls back to QSystemTrayIcon.showMessage() if notify-send is unavailable.

notify-send works on KDE Plasma (via plasma-integration) and Hyprland
(via dunst, mako, or any notification daemon).
"""

import logging
import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QSystemTrayIcon

logger = logging.getLogger(__name__)

APP_NAME = "AdGuard Tray"
APP_ICON = "security-high"  # XDG icon name, available in Breeze and most themes


def notify(
    title: str,
    body: str,
    urgency: str = "normal",          # low | normal | critical
    tray: "QSystemTrayIcon | None" = None,
) -> None:
    """Send a desktop notification. Never raises."""
    try:
        subprocess.run(
            [
                "notify-send",
                "--app-name", APP_NAME,
                "--icon", APP_ICON,
                "--urgency", urgency,
                title,
                body,
            ],
            check=False,
            capture_output=True,
            timeout=5,
        )
        return
    except FileNotFoundError:
        logger.debug("notify-send not found – falling back to Qt tray bubble")
    except (subprocess.TimeoutExpired, OSError) as exc:
        logger.warning("notify-send failed: %s – falling back", exc)

    # Qt fallback
    if tray is not None and tray.isVisible():
        from PyQt6.QtWidgets import QSystemTrayIcon as _QSTi
        icon_map = {
            "low":      _QSTi.MessageIcon.Information,
            "normal":   _QSTi.MessageIcon.Information,
            "critical": _QSTi.MessageIcon.Critical,
        }
        tray.showMessage(
            title,
            body,
            icon_map.get(urgency, _QSTi.MessageIcon.Information),
            5000,
        )
