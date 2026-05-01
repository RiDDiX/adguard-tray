"""
Settings dialog.

Manages:
  - Refresh interval (5–300 s)
  - Desktop notifications toggle
  - Autostart via ~/.config/autostart/adguard-tray.desktop (XDG spec)
"""

import logging
import os
import subprocess
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from .config import Config, save_config
from .i18n import _CURRENT, _TRANSLATIONS, _t

logger = logging.getLogger(__name__)


def _looks_like_adguard_cli(path: str) -> bool:
    try:
        r = subprocess.run([path, "--version"], capture_output=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return False
    out = (r.stdout + r.stderr).decode("utf-8", errors="replace").lower()
    return "adguard cli" in out


_AUTOSTART_DIR = Path.home() / ".config" / "autostart"
_AUTOSTART_FILE = _AUTOSTART_DIR / "adguard-tray.desktop"

_DESKTOP_TEMPLATE = """\
[Desktop Entry]
Type=Application
Name=AdGuard Tray
GenericName=AdGuard CLI Monitor
GenericName[de]=AdGuard CLI Überwachung
GenericName[zh_CN]=AdGuard CLI 监视器
Comment=System tray monitor and controller for adguard-cli
Comment[de]=System tray Überwachung und Steuerung für adguard-cli
Comment[zh_CN]=adguard-cli 的系统托盘监视器和控制器
Exec={exec}
Icon=security-high
Categories=Network;Security;System;
Keywords=adguard;dns;privacy;security;ad-blocker;filter;
Keywords[de]=adguard;dns;privatsphäre;sicherheit;werbeblocker;filter;steuerung
Keywords[zh_CN]=adguard;dns;隐私;安全;广告拦截;过滤器;控制器
StartupNotify=false
X-GNOME-Autostart-enabled=true
"""


class SettingsDialog(QDialog):
    def __init__(self, config: Config, exec_path: str, parent=None) -> None:
        super().__init__(parent)
        self.config = config
        self.exec_path = exec_path
        self.setWindowTitle(_t("AdGuard Tray – Settings"))
        self.setMinimumWidth(400)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # ── Polling ────────────────────────────────────────────────────────
        grp_poll = QGroupBox(_t("Status Refresh"))
        form = QFormLayout(grp_poll)

        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(5, 300)
        self.spin_interval.setSingleStep(5)
        self.spin_interval.setSuffix(_t(" seconds"))
        self.spin_interval.setValue(self.config.refresh_interval)
        self.spin_interval.setToolTip(
            _t("How often adguard-cli status is checked automatically.")
        )
        form.addRow(_t("Interval:"), self.spin_interval)

        self.combo_log = QComboBox()
        self.combo_log.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        idx = self.combo_log.findText(self.config.log_level.upper())
        if idx >= 0:
            self.combo_log.setCurrentIndex(idx)
        form.addRow(_t("Log level:"), self.combo_log)

        cli_row = QHBoxLayout()
        self.edit_cli_path = QLineEdit(self.config.adguard_cli_path)
        self.edit_cli_path.setPlaceholderText(_t("auto-detect via PATH"))
        cli_row.addWidget(self.edit_cli_path)
        btn_browse = QPushButton(_t("Browse…"))
        btn_browse.clicked.connect(self._browse_cli)
        cli_row.addWidget(btn_browse)
        form.addRow(_t("adguard-cli path:"), cli_row)

        restart_hint = QLabel(
            _t("<small>Log level and CLI path changes apply after a restart.</small>")
        )
        restart_hint.setTextFormat(Qt.TextFormat.RichText)
        restart_hint.setWordWrap(True)
        form.addRow(restart_hint)

        layout.addWidget(grp_poll)

        # ── Notifications ──────────────────────────────────────────────────
        grp_notify = QGroupBox(_t("Notifications"))
        notify_layout = QVBoxLayout(grp_notify)

        self.cb_notify = QCheckBox(_t("Desktop notification on status change"))
        self.cb_notify.setChecked(self.config.notifications_enabled)
        notify_layout.addWidget(self.cb_notify)

        hint = QLabel(
            _t(
                "<small>Requires <i>libnotify</i> / <i>notify-send</i> or an "
                "active notification service (dunst, mako, KDE).</small>"
            )
        )
        hint.setWordWrap(True)
        hint.setTextFormat(Qt.TextFormat.RichText)
        notify_layout.addWidget(hint)
        layout.addWidget(grp_notify)

        # ── Autostart ──────────────────────────────────────────────────────
        grp_auto = QGroupBox(_t("Autostart"))
        auto_layout = QVBoxLayout(grp_auto)

        self.cb_autostart = QCheckBox(
            _t("Start automatically on desktop login (XDG Autostart)")
        )
        self.cb_autostart.setChecked(_AUTOSTART_FILE.exists())
        auto_layout.addWidget(self.cb_autostart)

        autostart_hint = QLabel(
            _t(
                "<small>Creates <i>~/.config/autostart/adguard-tray.desktop</i>.<br>"
                "Works on KDE Plasma, GNOME, Hyprland (with xdg-autostart-impl) "
                "and other XDG-compliant environments.</small>"
            )
        )
        autostart_hint.setWordWrap(True)
        autostart_hint.setTextFormat(Qt.TextFormat.RichText)
        auto_layout.addWidget(autostart_hint)
        layout.addWidget(grp_auto)

        # ── Language ──────────────────────────────────────────────────
        grp_lang = QGroupBox(_t("Language"))
        lang_layout = QVBoxLayout(grp_lang)

        self.combo_language = QComboBox()
        # Map language codes to translation keys
        self._lang_code_to_key = {
            "en": "English",
            "zh": "Simplified Chinese",
            "de": "German",
        }
        # Add available languages
        available_languages = ["en"] + list(_TRANSLATIONS.keys())
        # Remove duplicates
        available_languages = list(dict.fromkeys(available_languages))
        for lang_code in available_languages:
            key = self._lang_code_to_key.get(lang_code, lang_code)
            display_name = _t(key)
            self.combo_language.addItem(display_name, lang_code)

        # Set current language
        current_lang = self.config.language or ""
        if not current_lang:
            # Auto-detect: find the language that matches current _CURRENT
            for code, trans_dict in _TRANSLATIONS.items():
                if trans_dict is _CURRENT:
                    current_lang = code
                    break
            if not current_lang:
                current_lang = "en"
        idx = self.combo_language.findData(current_lang)
        if idx >= 0:
            self.combo_language.setCurrentIndex(idx)

        lang_layout.addWidget(self.combo_language)

        hint = QLabel(_t("<small>Requires application restart to take effect.</small>"))
        hint.setWordWrap(True)
        hint.setTextFormat(Qt.TextFormat.RichText)
        lang_layout.addWidget(hint)

        layout.addWidget(grp_lang)

        # ── Buttons ────────────────────────────────────────────────────────
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._apply)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _browse_cli(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, _t("Select adguard-cli binary"), "/usr/local/bin"
        )
        if path:
            self.edit_cli_path.setText(path)

    def _apply(self) -> None:
        cli_path = self.edit_cli_path.text().strip()
        if cli_path and not (os.path.isfile(cli_path) and os.access(cli_path, os.X_OK)):
            reply = QMessageBox.warning(
                self,
                _t("AdGuard Tray – Settings"),
                _t("adguard-cli path does not exist or is not executable."),
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel,
            )
            if reply != QMessageBox.StandardButton.Save:
                return
        elif cli_path and not _looks_like_adguard_cli(cli_path):
            reply = QMessageBox.warning(
                self,
                _t("AdGuard Tray – Settings"),
                _t("That binary does not identify as adguard-cli. Save anyway?"),
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel,
            )
            if reply != QMessageBox.StandardButton.Save:
                return

        self.config.refresh_interval = self.spin_interval.value()
        self.config.notifications_enabled = self.cb_notify.isChecked()
        self.config.log_level = self.combo_log.currentText()
        self.config.adguard_cli_path = cli_path
        self.config.language = self.combo_language.currentData() or ""
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
