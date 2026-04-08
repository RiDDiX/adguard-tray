"""
Exceptions tab for the Manager window.

Reuses the core logic from exceptions_dialog as a QWidget tab page.
"""

import logging
import re
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .i18n import _t

logger = logging.getLogger(__name__)

_USER_RULES_FILE = Path.home() / ".local" / "share" / "adguard-cli" / "user.txt"
_ALLOWLIST_RE = re.compile(r"^@@\|\|(.+?)\^\$important,document\s*$")
_DOMAIN_RE = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?\.)*"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?$"
)
_IP_RE = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")


def _is_valid_domain(text: str) -> bool:
    return bool(_DOMAIN_RE.match(text) or _IP_RE.match(text))


def _domain_to_rule(domain: str) -> str:
    return f"@@||{domain}^$important,document"


def _load_user_rules() -> tuple[list[str], list[str]]:
    domains: list[str] = []
    other_lines: list[str] = []
    if not _USER_RULES_FILE.exists():
        return domains, other_lines
    try:
        for line in _USER_RULES_FILE.read_text(encoding="utf-8").splitlines():
            m = _ALLOWLIST_RE.match(line)
            if m:
                domains.append(m.group(1))
            else:
                other_lines.append(line)
    except OSError as exc:
        logger.error("Failed to read user rules: %s", exc)
    return domains, other_lines


def _save_user_rules(domains: list[str], other_lines: list[str]) -> tuple[bool, str]:
    try:
        lines = list(other_lines)
        for d in sorted(domains):
            lines.append(_domain_to_rule(d))
        text = "\n".join(lines)
        if text and not text.endswith("\n"):
            text += "\n"
        _USER_RULES_FILE.write_text(text, encoding="utf-8")
        return True, ""
    except OSError as exc:
        logger.error("Failed to save user rules: %s", exc)
        return False, str(exc)


class ExceptionsTab(QWidget):
    def __init__(self, on_change=None, parent=None) -> None:
        super().__init__(parent)
        self._on_change = on_change
        self._changed = False
        self._other_lines: list[str] = []

        self._build_ui()
        self._load()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        desc = QLabel(_t(
            "<small>Websites listed here will not have ads or trackers blocked.<br>"
            "Enter a domain (e.g. <code>example.com</code>) without <code>https://</code>.</small>"
        ))
        desc.setTextFormat(Qt.TextFormat.RichText)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        input_row = QHBoxLayout()
        self.input_domain = QLineEdit()
        self.input_domain.setPlaceholderText(_t("example.com"))
        self.input_domain.returnPressed.connect(self._add)
        input_row.addWidget(self.input_domain)

        self.btn_add = QPushButton(_t("Add"))
        self.btn_add.clicked.connect(self._add)
        input_row.addWidget(self.btn_add)
        layout.addLayout(input_row)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(_t("Search exceptions…"))
        self.search_box.setClearButtonEnabled(True)
        self.search_box.textChanged.connect(self._apply_filter)
        layout.addWidget(self.search_box)

        self.domain_list = QListWidget()
        self.domain_list.setAlternatingRowColors(True)
        self.domain_list.setSortingEnabled(True)
        layout.addWidget(self.domain_list)

        self.lbl_status = QLabel("")
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

        btn_row = QHBoxLayout()
        self.btn_remove = QPushButton(_t("Remove selected"))
        self.btn_remove.clicked.connect(self._remove_selected)
        btn_row.addWidget(self.btn_remove)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    def _load(self) -> None:
        domains, self._other_lines = _load_user_rules()
        self.domain_list.clear()
        for d in sorted(domains):
            self.domain_list.addItem(d)
        self._update_status()

    def _update_status(self) -> None:
        self.lbl_status.setText(_t("{} exception(s)", self.domain_list.count()))

    def _add(self) -> None:
        raw = self.input_domain.text().strip()
        if not raw:
            return
        for prefix in ("https://", "http://", "www."):
            if raw.lower().startswith(prefix):
                raw = raw[len(prefix):]
        raw = raw.split("/")[0].strip()

        if not _is_valid_domain(raw):
            QMessageBox.warning(
                self, _t("Invalid domain"),
                _t("'{}' is not a valid domain or IP address.", raw),
            )
            return

        existing = {self.domain_list.item(i).text() for i in range(self.domain_list.count())}
        if raw in existing:
            self.lbl_status.setText(_t("'{}' is already in the list.", raw))
            self.input_domain.clear()
            return

        self.domain_list.addItem(raw)
        self.input_domain.clear()
        self._save_and_mark()

    def _remove_selected(self) -> None:
        for item in self.domain_list.selectedItems():
            self.domain_list.takeItem(self.domain_list.row(item))
        self._save_and_mark()

    def _save_and_mark(self) -> None:
        domains = [self.domain_list.item(i).text() for i in range(self.domain_list.count())]
        ok, err = _save_user_rules(domains, self._other_lines)
        if ok:
            self._changed = True
            self._update_status()
        else:
            QMessageBox.critical(self, _t("Save failed"), _t("Could not save exceptions:\n{}", err))

    def _apply_filter(self, text: str) -> None:
        needle = text.strip().lower()
        for i in range(self.domain_list.count()):
            item = self.domain_list.item(i)
            item.setHidden(bool(needle) and needle not in item.text().lower())
