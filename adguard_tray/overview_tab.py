"""
Overview tab for the Manager window.

Shows status, version, license info, and quick actions:
  - Enable / Disable / Restart
  - Check for CLI update
  - Reset license (with confirmation)
  - Generate HTTPS certificate
"""

import logging

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .cli import AdGuardCLI, AdGuardStatus
from .i18n import _t

logger = logging.getLogger(__name__)


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


class OverviewTab(QWidget):
    def __init__(self, cli: AdGuardCLI, on_restart=None, parent=None) -> None:
        super().__init__(parent)
        self.cli = cli
        self._on_restart = on_restart
        self._workers: list[QThread] = []
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

        # HTTPS Certificate
        grp_cert = QGroupBox(_t("HTTPS Certificate"))
        cl = QVBoxLayout(grp_cert)
        cert_info = QLabel(_t(
            "<small>Generate a root CA certificate for HTTPS filtering. "
            "The certificate must be installed and trusted on your system.</small>"
        ))
        cert_info.setTextFormat(Qt.TextFormat.RichText)
        cert_info.setWordWrap(True)
        cl.addWidget(cert_info)

        self.btn_cert = QPushButton(_t("Generate certificate"))
        self.btn_cert.clicked.connect(self._do_gen_cert)
        cl.addWidget(self.btn_cert)
        layout.addWidget(grp_cert)

        # Result label
        self.lbl_result = QLabel("")
        self.lbl_result.setWordWrap(True)
        self.lbl_result.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.lbl_result)

        layout.addStretch()

    def _refresh(self) -> None:
        # Status
        result = self.cli.get_status()
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
        cli_ver = self.cli.get_version()
        ver_text = f"adguard-tray v{__version__}"
        if cli_ver:
            ver_text += f" · AdGuard CLI v{cli_ver}"
        self.lbl_version.setText(ver_text)

        # License
        ok, lic = self.cli.get_license()
        self.lbl_license.setText(lic if ok else _t("License: {}",
                                                    lic or _t("Could not retrieve")))

    def _run_action(self, fn, on_done=None) -> None:
        self._set_busy(True)
        w = _Worker(fn)

        def _done(ok, msg):
            self._set_busy(False)
            self.lbl_result.setText(msg)
            if on_done:
                on_done(ok, msg)
            self._refresh()

        w.done.connect(_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _set_busy(self, busy: bool) -> None:
        for btn in (self.btn_enable, self.btn_disable, self.btn_restart,
                    self.btn_update, self.btn_reset_license, self.btn_cert):
            btn.setEnabled(not busy)

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
        self._run_action(self.cli.generate_cert)
