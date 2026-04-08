"""
Configuration tab for the Manager window.

Opens the existing ProxyConfigDialog via a button.
"""

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .i18n import _t

logger = logging.getLogger(__name__)


class ConfigTab(QWidget):
    def __init__(self, on_restart=None, parent=None) -> None:
        super().__init__(parent)
        self._on_restart = on_restart
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        info = QLabel(
            _t("<small>Edit the full AdGuard CLI configuration (proxy.yaml).</small>")
        )
        info.setTextFormat(Qt.TextFormat.RichText)
        info.setWordWrap(True)
        layout.addWidget(info)

        self.btn_open = QPushButton(_t("Open Configuration Editor…"))
        self.btn_open.clicked.connect(self._open_editor)
        layout.addWidget(self.btn_open)

        self.lbl_status = QLabel("")
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

        layout.addStretch()

    def _open_editor(self) -> None:
        from .proxy_config_dialog import ProxyConfigDialog
        dlg = ProxyConfigDialog(self)
        if dlg.exec():
            self.lbl_status.setText(_t("Configuration saved. Restart AdGuard to apply changes."))
            if self._on_restart:
                self._on_restart()
