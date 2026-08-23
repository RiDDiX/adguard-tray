"""
Website exceptions dialog.

Manages allowlist entries in AdGuard CLI's user.txt file.
Each exception is stored as an AdBlock-style rule:
  @@||example.com^$important,document

This tells AdGuard to skip content filtering on the specified domain.
"""

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from ._allowlist import is_valid_domain, load_user_rules, save_user_rules
from .i18n import _t

logger = logging.getLogger(__name__)


class ExceptionsDialog(QDialog):
    def __init__(self, on_change=None, parent=None) -> None:
        super().__init__(parent)
        self._on_change = on_change
        self._changed = False
        self._other_lines: list[str] | None = []

        self.setWindowTitle(_t("AdGuard Tray – Website Exceptions"))
        self.setMinimumSize(520, 420)
        self.resize(560, 460)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self._build_ui()
        self._load()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # Description
        desc = QLabel(
            _t(
                "<small>Websites listed here will not have ads or trackers blocked.<br>"
                "Enter a domain (e.g. <code>example.com</code>) without <code>https://</code>.</small>"
            )
        )
        desc.setTextFormat(Qt.TextFormat.RichText)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Input row
        input_row = QHBoxLayout()
        self.input_domain = QLineEdit()
        self.input_domain.setPlaceholderText(_t("example.com"))
        self.input_domain.returnPressed.connect(self._add)
        input_row.addWidget(self.input_domain)

        self.btn_add = QPushButton(_t("Add"))
        self.btn_add.clicked.connect(self._add)
        input_row.addWidget(self.btn_add)
        layout.addLayout(input_row)

        # Search
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(_t("Search exceptions…"))
        self.search_box.setClearButtonEnabled(True)
        self.search_box.textChanged.connect(self._apply_filter)
        layout.addWidget(self.search_box)

        # List
        self.domain_list = QListWidget()
        self.domain_list.setAlternatingRowColors(True)
        self.domain_list.setSortingEnabled(True)
        layout.addWidget(self.domain_list)

        # Status
        self.lbl_status = QLabel("")
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

        # Bottom buttons
        btn_row = QHBoxLayout()
        self.btn_remove = QPushButton(_t("Remove selected"))
        self.btn_remove.clicked.connect(self._remove_selected)
        btn_row.addWidget(self.btn_remove)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        # finished() fires for Close button, Escape and the window X alike.
        self.finished.connect(self._on_finished)

    def _load(self) -> None:
        try:
            domains, self._other_lines = load_user_rules()
        except (OSError, ValueError) as exc:  # ValueError: not UTF-8
            self._other_lines = None  # never save over a file we couldn't read
            logger.error("Failed to read user rules: %s", exc)
            self.lbl_status.setText(_t("Error: {}", exc))
            self.btn_add.setEnabled(False)
            self.btn_remove.setEnabled(False)
            self.input_domain.setEnabled(False)
            return
        self.domain_list.clear()
        for d in sorted(domains):
            self.domain_list.addItem(d)
        self._update_status()

    def _update_status(self) -> None:
        count = self.domain_list.count()
        key = "1 exception" if count == 1 else "{} exceptions"
        self.lbl_status.setText(_t(key, count))

    def _add(self) -> None:
        raw = self.input_domain.text().strip()
        if not raw:
            return

        # Strip protocol if user pastes a URL
        for prefix in ("https://", "http://", "www."):
            if raw.lower().startswith(prefix):
                raw = raw[len(prefix):]
        # Strip trailing path/slash
        raw = raw.split("/")[0].strip()

        if not is_valid_domain(raw):
            QMessageBox.warning(
                self,
                _t("Invalid domain"),
                _t("'{}' is not a valid domain or IP address.", raw),
            )
            return

        # Check duplicate
        existing = {self.domain_list.item(i).text() for i in range(self.domain_list.count())}
        if raw in existing:
            self.lbl_status.setText(_t("'{}' is already in the list.", raw))
            self.input_domain.clear()
            return

        self.domain_list.addItem(raw)
        self.input_domain.clear()
        self._save_and_mark_changed()

    def _remove_selected(self) -> None:
        selected = self.domain_list.selectedItems()
        if not selected:
            return
        for item in selected:
            self.domain_list.takeItem(self.domain_list.row(item))
        self._save_and_mark_changed()

    def _save_and_mark_changed(self) -> None:
        if self._other_lines is None:
            return
        domains = [self.domain_list.item(i).text() for i in range(self.domain_list.count())]
        ok, err = save_user_rules(domains, self._other_lines)
        if ok:
            self._changed = True
            self._update_status()
        else:
            QMessageBox.critical(
                self,
                _t("Save failed"),
                _t("Could not save exceptions:\n{}", err),
            )

    def _apply_filter(self, text: str) -> None:
        needle = text.strip().lower()
        for i in range(self.domain_list.count()):
            item = self.domain_list.item(i)
            item.setHidden(bool(needle) and needle not in item.text().lower())

    def _on_finished(self, _result: int) -> None:
        if self._changed and self._on_change:
            self._on_change()
