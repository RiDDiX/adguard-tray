"""
Overview tab for the Manager window.

Shows status, version, license info, and quick actions:
  - Enable / Disable / Restart
  - Check for CLI update
  - Reset license (with confirmation)
  - Generate HTTPS certificate
"""

import html
import logging
import re

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .cli import AdGuardCLI, AdGuardStatus, StatusResult
from .i18n import _t

logger = logging.getLogger(__name__)


def _mask_license(raw: str) -> str:
    """Mask email addresses and license keys in license output."""
    def _mask_email(m: re.Match) -> str:
        email = m.group(0)
        local, domain = email.rsplit("@", 1)
        return local[0] + "***@" + domain

    # Mask emails: show first char + *** + @domain
    out = re.sub(r"[\w.+-]+@[\w.-]+", _mask_email, raw)
    # Mask license key: show first 4 chars + ****
    out = re.sub(r"(?<=License key: )(\w{4})\w+", r"\1****", out)
    return out


class _Worker(QThread):
    done = pyqtSignal(bool, str)

    def __init__(self, fn):
        super().__init__()
        self._fn = fn

    def run(self):
        try:
            ok, msg = self._fn()
        except Exception as exc:
            ok, msg = False, str(exc)
        self.done.emit(ok, msg)


class _CertWorker(QThread):
    """Imports the AdGuard CA into the browsers' certificate stores."""
    done = pyqtSignal(bool, str, object)

    def run(self):
        from .certs import install_into_browsers
        try:
            ok, msg, targets = install_into_browsers()
        except Exception as exc:  # never abort the app from a worker
            logger.exception("Certificate install failed")
            ok, msg, targets = False, str(exc), []
        self.done.emit(ok, msg, targets)


class _RefreshWorker(QThread):
    done = pyqtSignal(object)  # dict with status, version, license

    def __init__(self, cli):
        super().__init__()
        self.cli = cli

    def run(self):
        try:
            data = {
                "status": self.cli.get_status(),
                "version": self.cli.get_version(),
                "channel": self.cli.get_update_channel(),
            }
            ok, lic = self.cli.get_license()
        except Exception as exc:  # would otherwise abort the process (qFatal)
            logger.exception("Overview refresh failed")
            data = {"status": StatusResult(AdGuardStatus.ERROR, str(exc)), "version": "", "channel": ""}
            ok, lic = False, str(exc)
        data["license_ok"] = ok
        data["license"] = lic
        self.done.emit(data)


class OverviewTab(QWidget):
    def __init__(self, cli: AdGuardCLI, on_status_change=None, parent=None) -> None:
        super().__init__(parent)
        self.cli = cli
        # Enable/Disable/Restart here change the run state, not the config, so
        # the tray only needs to re-poll – restarting would fight the user.
        self._on_status_change = on_status_change
        self._workers: list[QThread] = []
        self._refreshing = False
        self._acting = False
        self._build_ui()
        self._refresh()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Status section
        grp_status = QGroupBox(_t("Status"))
        sl = QVBoxLayout(grp_status)
        self.lbl_status = QLabel(_t("Checking status…"))
        self.lbl_status.setWordWrap(True)
        sl.addWidget(self.lbl_status)

        btn_row = QHBoxLayout()
        self.btn_enable = QPushButton(_t("Enable"))
        self.btn_enable.clicked.connect(self._do_enable)
        btn_row.addWidget(self.btn_enable)

        self.btn_disable = QPushButton(_t("Disable"))
        self.btn_disable.clicked.connect(self._do_disable)
        btn_row.addWidget(self.btn_disable)

        self.btn_restart = QPushButton(_t("Restart"))
        self.btn_restart.clicked.connect(self._do_restart)
        btn_row.addWidget(self.btn_restart)

        self.btn_refresh = QPushButton(_t("↺ Refresh"))
        self.btn_refresh.clicked.connect(self._refresh)
        btn_row.addWidget(self.btn_refresh)

        btn_row.addStretch()
        sl.addLayout(btn_row)
        layout.addWidget(grp_status)

        # Version & License
        grp_info = QGroupBox(_t("Version & License"))
        il = QVBoxLayout(grp_info)
        self.lbl_version = QLabel("")
        self.lbl_version.setWordWrap(True)
        self.lbl_version.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        il.addWidget(self.lbl_version)
        self.lbl_license = QLabel("")
        self.lbl_license.setWordWrap(True)
        self.lbl_license.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        il.addWidget(self.lbl_license)

        info_btns = QHBoxLayout()
        self.btn_update = QPushButton(_t("Check for CLI update"))
        self.btn_update.clicked.connect(self._do_update)
        info_btns.addWidget(self.btn_update)

        self.btn_reset_license = QPushButton(_t("Reset license"))
        self.btn_reset_license.clicked.connect(self._do_reset_license)
        info_btns.addWidget(self.btn_reset_license)

        info_btns.addStretch()
        il.addLayout(info_btns)
        layout.addWidget(grp_info)

        # Update channel
        grp_channel = QGroupBox(_t("Update channel"))
        chl = QVBoxLayout(grp_channel)
        ch_hint = QLabel(_t(
            "<small>Controls which AdGuard CLI build <i>Check for CLI update</i> "
            "will pull. Changes take effect on the next update run.</small>"
        ))
        ch_hint.setTextFormat(Qt.TextFormat.RichText)
        ch_hint.setWordWrap(True)
        chl.addWidget(ch_hint)

        ch_row = QHBoxLayout()
        ch_row.addWidget(QLabel(_t("Channel:")))
        self.combo_channel = QComboBox()
        for ch in self.cli.UPDATE_CHANNELS:
            self.combo_channel.addItem(ch)
        self.combo_channel.setEnabled(False)  # enabled after first refresh
        self._channel_loaded = False
        self.combo_channel.currentTextChanged.connect(self._on_channel_changed)
        ch_row.addWidget(self.combo_channel)
        ch_row.addStretch()
        chl.addLayout(ch_row)
        layout.addWidget(grp_channel)

        # HTTPS Certificate
        grp_cert = QGroupBox(_t("HTTPS Certificate"))
        cl = QVBoxLayout(grp_cert)
        cert_info = QLabel("<small>" + _t(
            "Generate a root CA certificate for HTTPS filtering. "
            "The certificate must be installed and trusted on your system."
        ) + "</small>")
        cert_info.setTextFormat(Qt.TextFormat.RichText)
        cert_info.setWordWrap(True)
        cl.addWidget(cert_info)

        from PyQt6.QtWidgets import QFormLayout, QLineEdit
        cert_form = QFormLayout()
        self.edit_firefox_profile = QLineEdit()
        self.edit_firefox_profile.setPlaceholderText(_t("(optional) e.g. abcd1234.MyProfile"))
        cert_form.addRow(_t("Firefox profile:"), self.edit_firefox_profile)
        cl.addLayout(cert_form)

        self.btn_cert = QPushButton(_t("Generate certificate"))
        self.btn_cert.clicked.connect(self._do_gen_cert)
        cl.addWidget(self.btn_cert)

        browser_info = QLabel("<small>" + _t(
            "Chromium-based browsers (Brave, Chrome, ungoogled-chromium, Vivaldi, …) "
            "keep their own certificate store and ignore the system one. "
            "This adds AdGuard's certificate to every browser profile found, "
            "which lets AdGuard read those browsers' HTTPS traffic."
        ) + "</small>")
        browser_info.setTextFormat(Qt.TextFormat.RichText)
        browser_info.setWordWrap(True)
        cl.addWidget(browser_info)

        self.btn_cert_browsers = QPushButton(_t("Install certificate in browsers…"))
        self.btn_cert_browsers.clicked.connect(self._do_install_cert_browsers)
        cl.addWidget(self.btn_cert_browsers)

        self.lbl_cert_targets = QLabel("")
        self.lbl_cert_targets.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_cert_targets.setWordWrap(True)
        self.lbl_cert_targets.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.lbl_cert_targets.hide()
        cl.addWidget(self.lbl_cert_targets)
        layout.addWidget(grp_cert)

        # Result label
        self.lbl_result = QLabel("")
        self.lbl_result.setWordWrap(True)
        self.lbl_result.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.lbl_result)

        layout.addStretch()

    def _refresh(self) -> None:
        if self._refreshing or self._acting:
            return
        self._refreshing = True
        self._set_busy(True)
        self.lbl_status.setText(_t("Checking status…"))
        w = _RefreshWorker(self.cli)
        w.done.connect(self._on_refresh_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_refresh_done(self, data: dict) -> None:
        self._refreshing = False
        self._set_busy(False)

        # Status
        result = data["status"]
        status_map = {
            AdGuardStatus.ACTIVE: _t("Active – Protection running"),
            AdGuardStatus.INACTIVE: _t("Inactive – Protection stopped"),
            AdGuardStatus.ERROR: _t("Error retrieving status"),
            AdGuardStatus.NOT_INSTALLED: _t("adguard-cli not found"),
            AdGuardStatus.UNKNOWN: _t("Unknown status"),
        }
        self.lbl_status.setText(status_map.get(result.status, _t("Unknown status")))
        is_active = result.status == AdGuardStatus.ACTIVE
        self.btn_enable.setEnabled(not is_active)
        self.btn_disable.setEnabled(is_active)
        self.btn_restart.setEnabled(is_active)

        # Version
        from . import __version__
        cli_ver = data["version"]
        ver_text = f"adguard-tray v{__version__}"
        if cli_ver:
            ver_text += f" · AdGuard CLI v{cli_ver}"
        self.lbl_version.setText(ver_text)

        # License (mask sensitive fields)
        if data["license_ok"]:
            self.lbl_license.setText(_mask_license(data["license"]))
        else:
            self.lbl_license.setText(_t("License: {}",
                                        data["license"] or _t("Could not retrieve")))

        # Update channel – load without firing currentTextChanged
        channel = data.get("channel") or ""
        self.combo_channel.blockSignals(True)
        self._channel_loaded = bool(channel) and self.combo_channel.findText(channel) >= 0
        if self._channel_loaded:
            self.combo_channel.setCurrentText(channel)
        # Unknown or unreadable channel keeps the combo disabled.
        self.combo_channel.setEnabled(self._channel_loaded)
        self.combo_channel.blockSignals(False)

    def _run_action(self, fn) -> None:
        self._acting = True
        self._set_busy(True)
        w = _Worker(fn)

        def _done(ok, msg):
            self._acting = False
            self._set_busy(False)
            self.lbl_result.setText(msg)
            if ok and self._on_status_change:
                self._on_status_change()
            self._refresh()

        w.done.connect(_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _set_busy(self, busy: bool) -> None:
        busy = busy or self._acting
        for btn in (self.btn_enable, self.btn_disable, self.btn_restart,
                    self.btn_refresh, self.btn_cert_browsers,
                    self.btn_update, self.btn_reset_license, self.btn_cert):
            btn.setEnabled(not busy)
        # Only (re)enable the channel combo when we actually loaded a value
        self.combo_channel.setEnabled(not busy and self._channel_loaded)

    def _do_enable(self) -> None:
        self._run_action(self.cli.start)

    def _do_disable(self) -> None:
        self._run_action(self.cli.stop)

    def _do_restart(self) -> None:
        self._run_action(self.cli.restart)

    def _do_update(self) -> None:
        self.lbl_result.setText(_t("Checking for updates…"))
        self._run_action(self.cli.check_cli_update)

    def _do_reset_license(self) -> None:
        reply = QMessageBox.question(
            self,
            _t("Reset license"),
            _t("Are you sure you want to reset the AdGuard license?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        self._run_action(self.cli.reset_license)

    def _do_gen_cert(self) -> None:
        self.lbl_result.setText(_t("Generating certificate…"))
        profile = self.edit_firefox_profile.text().strip()
        self._run_action(lambda: self.cli.generate_cert(firefox_profile=profile))

    def _do_install_cert_browsers(self) -> None:
        reply = QMessageBox.question(
            self,
            _t("Install certificate in browsers"),
            _t("AdGuard's certificate will be added to every browser profile found "
               "on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in "
               "those browsers. Close your browsers first – they read the "
               "certificate store at startup.\n\nContinue?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        self.lbl_cert_targets.hide()
        self.lbl_result.setText(_t("Installing certificate in browsers…"))
        self._acting = True
        self._set_busy(True)
        w = _CertWorker()
        w.done.connect(self._on_cert_browsers_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_cert_browsers_done(self, ok: bool, msg: str, targets: object) -> None:
        self._acting = False
        self._set_busy(False)
        self.lbl_result.setText(msg)
        rows = []
        for target in targets or []:
            mark = "✓" if target.ok else "✗"
            # Names and paths come from the filesystem, the label is rich text.
            name = html.escape(str(target.name))
            path = html.escape(str(target.path))
            detail = "" if target.ok else f" – {html.escape(str(target.error))}"
            rows.append(f"{mark} {name} <code>{path}</code>{detail}")
        if rows:
            hint = _t("Restart your browsers for the certificate to take effect.")
            self.lbl_cert_targets.setText(
                "<small>" + "<br>".join(rows) + (f"<br><br>{hint}" if ok else "") + "</small>"
            )
            self.lbl_cert_targets.show()

    def _on_channel_changed(self, channel: str) -> None:
        if not self._channel_loaded or not channel:
            return
        self.lbl_result.setText(_t("Switching update channel to {}…", channel))
        self._run_action(lambda c=channel: self.cli.set_update_channel(c))
