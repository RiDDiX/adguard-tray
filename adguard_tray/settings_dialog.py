"""
Settings dialog.

Manages:
  - Refresh interval (5–300 s)
  - Desktop notifications toggle
  - Autostart via ~/.config/autostart/adguard-tray.desktop (XDG spec)
"""

import logging
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QSpinBox,
    QVBoxLayout,
)

from .config import Config, save_config

logger = logging.getLogger(__name__)

_AUTOSTART_DIR = Path.home() / ".config" / "autostart"
_AUTOSTART_FILE = _AUTOSTART_DIR / "adguard-tray.desktop"

_DESKTOP_TEMPLATE = """\
[Desktop Entry]
Type=Application
Name=AdGuard Tray
GenericName=AdGuard CLI Monitor
Comment=System tray monitor for adguard-cli
Exec={exec}
Icon=security-high
Categories=Network;Security;System;
Keywords=adguard;dns;privacy;security;
StartupNotify=false
X-GNOME-Autostart-enabled=true
"""


class SettingsDialog(QDialog):
    def __init__(self, config: Config, exec_path: str, parent=None) -> None:
        super().__init__(parent)
        self.config = config
        self.exec_path = exec_path
        self.setWindowTitle("AdGuard Tray – Einstellungen")
        self.setMinimumWidth(400)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # ── Polling ────────────────────────────────────────────────────────
        grp_poll = QGroupBox("Status-Aktualisierung")
        form = QFormLayout(grp_poll)

        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(5, 300)
        self.spin_interval.setSingleStep(5)
        self.spin_interval.setSuffix(" Sekunden")
        self.spin_interval.setValue(self.config.refresh_interval)
        self.spin_interval.setToolTip(
            "Wie häufig der Status von adguard-cli automatisch abgefragt wird."
        )
        form.addRow("Intervall:", self.spin_interval)
        layout.addWidget(grp_poll)

        # ── Notifications ──────────────────────────────────────────────────
        grp_notify = QGroupBox("Benachrichtigungen")
        notify_layout = QVBoxLayout(grp_notify)

        self.cb_notify = QCheckBox("Desktop-Benachrichtigung bei Statusänderung")
        self.cb_notify.setChecked(self.config.notifications_enabled)
        notify_layout.addWidget(self.cb_notify)

        hint = QLabel(
            "<small>Benötigt <i>libnotify</i> / <i>notify-send</i> oder einen "
            "aktiven Benachrichtigungsdienst (dunst, mako, KDE).</small>"
        )
        hint.setWordWrap(True)
        hint.setTextFormat(Qt.TextFormat.RichText)
        notify_layout.addWidget(hint)
        layout.addWidget(grp_notify)

        # ── Autostart ──────────────────────────────────────────────────────
        grp_auto = QGroupBox("Autostart")
        auto_layout = QVBoxLayout(grp_auto)

        self.cb_autostart = QCheckBox(
            "Beim Desktop-Login automatisch starten (XDG Autostart)"
        )
        self.cb_autostart.setChecked(_AUTOSTART_FILE.exists())
        auto_layout.addWidget(self.cb_autostart)

        autostart_hint = QLabel(
            "<small>Erstellt <i>~/.config/autostart/adguard-tray.desktop</i>.<br>"
            "Funktioniert auf KDE Plasma, GNOME, Hyprland (mit xdg-autostart-impl) "
            "und anderen XDG-konformen Umgebungen.</small>"
        )
        autostart_hint.setWordWrap(True)
        autostart_hint.setTextFormat(Qt.TextFormat.RichText)
        auto_layout.addWidget(autostart_hint)
        layout.addWidget(grp_auto)

        # ── Buttons ────────────────────────────────────────────────────────
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._apply)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _apply(self) -> None:
        self.config.refresh_interval = self.spin_interval.value()
        self.config.notifications_enabled = self.cb_notify.isChecked()
        save_config(self.config)
        self._manage_autostart(self.cb_autostart.isChecked())
        self.accept()

    def _manage_autostart(self, enable: bool) -> None:
        if enable:
            try:
                _AUTOSTART_DIR.mkdir(parents=True, exist_ok=True)
                _AUTOSTART_FILE.write_text(
                    _DESKTOP_TEMPLATE.format(exec=self.exec_path),
                    encoding="utf-8",
                )
                logger.info("Autostart entry created: %s", _AUTOSTART_FILE)
            except OSError as exc:
                logger.error("Could not create autostart entry: %s", exc)
        else:
            try:
                _AUTOSTART_FILE.unlink(missing_ok=True)
                logger.info("Autostart entry removed")
            except OSError as exc:
                logger.error("Could not remove autostart entry: %s", exc)
