"""
DNS Filters tab for the Manager window.

Mirrors the Filters tab but uses `adguard-cli dns filters` subcommands.
"""

import logging

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .cli import AdGuardCLI, FilterEntry, FilterListResult
from .i18n import _t

logger = logging.getLogger(__name__)

_COL_NAME = 0
_COL_ID = 1
_COL_UPDATED = 2


class _LoadWorker(QThread):
    done = pyqtSignal(object)

    def __init__(self, cli, all_available):
        super().__init__()
        self.cli = cli
        self.all_available = all_available

    def run(self):
        self.done.emit(self.cli.get_dns_filters(all_available=self.all_available))


class _ToggleWorker(QThread):
    done = pyqtSignal(bool, str, int, bool)

    def __init__(self, cli, fid, enable):
        super().__init__()
        self.cli = cli
        self.fid = fid
        self.enable = enable

    def run(self):
        fn = self.cli.enable_dns_filter if self.enable else self.cli.disable_dns_filter
        ok, msg = fn(self.fid)
        self.done.emit(ok, msg, self.fid, self.enable)


class _RemoveWorker(QThread):
    done = pyqtSignal(bool, str, int)

    def __init__(self, cli, fid):
        super().__init__()
        self.cli = cli
        self.fid = fid

    def run(self):
        self.done.emit(*self.cli.remove_dns_filter(self.fid), self.fid)


class _InstallWorker(QThread):
    done = pyqtSignal(bool, str)

    def __init__(self, cli, url, title):
        super().__init__()
        self.cli = cli
        self.url = url
        self.title = title

    def run(self):
        self.done.emit(*self.cli.install_dns_filter(self.url, self.title))


class _ActionWorker(QThread):
    done = pyqtSignal(bool, str)

    def __init__(self, fn):
        super().__init__()
        self._fn = fn

    def run(self):
        self.done.emit(*self._fn())


class DnsFiltersTab(QWidget):
    def __init__(self, cli: AdGuardCLI, on_change=None, parent=None) -> None:
        super().__init__(parent)
        self.cli = cli
        self._on_change = on_change
        self._workers: list[QThread] = []
        self._filter_map: dict[int, FilterEntry] = {}
        self._changed = False

        self._build_ui()
        self._load_filters()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        toolbar = QHBoxLayout()

        self.btn_add = QPushButton(_t("Add custom DNS filter…"))
        self.btn_add.clicked.connect(self._add_custom_filter)
        toolbar.addWidget(self.btn_add)

        self.btn_add_id = QPushButton(_t("Add by ID…"))
        self.btn_add_id.clicked.connect(self._add_by_id)
        toolbar.addWidget(self.btn_add_id)

        toolbar.addStretch()

        self.cb_show_all = QCheckBox(_t("Show all available"))
        self.cb_show_all.toggled.connect(self._load_filters)
        toolbar.addWidget(self.cb_show_all)

        self.btn_reload = QPushButton(_t("↺ Reload"))
        self.btn_reload.clicked.connect(self._load_filters)
        toolbar.addWidget(self.btn_reload)

        layout.addLayout(toolbar)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setMaximumHeight(4)
        self.progress.hide()
        layout.addWidget(self.progress)

        self.lbl_status = QLabel("")
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(_t("Search DNS filters…"))
        self.search_box.setClearButtonEnabled(True)
        self.search_box.textChanged.connect(self._apply_search)
        layout.addWidget(self.search_box)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels([_t("Filter"), _t("ID"), _t("Last updated")])
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.setAlternatingRowColors(True)
        self.tree.setAnimated(True)
        self.tree.setUniformRowHeights(True)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._on_context_menu)
        layout.addWidget(self.tree)

        info = QLabel(_t(
            "<small>DNS filters block domains at the DNS level. "
            "Requires DNS filtering to be enabled in Configuration → DNS.</small>"
        ))
        info.setTextFormat(Qt.TextFormat.RichText)
        info.setWordWrap(True)
        layout.addWidget(info)

    # ── Loading ───────────────────────────────────────────────────────────

    def _load_filters(self) -> None:
        self._set_busy(True)
        self.lbl_status.setText(_t("Loading DNS filters…"))
        w = _LoadWorker(self.cli, self.cb_show_all.isChecked())
        w.done.connect(self._on_loaded)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_loaded(self, result: FilterListResult) -> None:
        self._set_busy(False)
        try:
            self.tree.itemChanged.disconnect(self._on_item_changed)
        except TypeError:
            pass
        self.tree.clear()
        self._filter_map.clear()

        if result.error:
            self.lbl_status.setText(_t("Error: {}", result.error))
            self.tree.itemChanged.connect(self._on_item_changed)
            return

        all_filters = result.all_filters
        if not all_filters:
            self.lbl_status.setText(_t("No DNS filters found."))
            self.tree.itemChanged.connect(self._on_item_changed)
            return

        active = sum(1 for f in all_filters if f.enabled)
        self.lbl_status.setText(_t("{} of {} DNS filters active", active, len(all_filters)))

        for group_name, filters in result.groups.items():
            group_item = QTreeWidgetItem(self.tree)
            group_item.setText(0, group_name)
            group_item.setFlags(group_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
            group_item.setExpanded(True)
            font = group_item.font(0)
            font.setBold(True)
            group_item.setFont(0, font)
            group_item.setForeground(0, QColor("#5b9bd5"))

            for f in filters:
                self._filter_map[f.id] = f
                item = QTreeWidgetItem(group_item)
                item.setData(0, Qt.ItemDataRole.UserRole, f.id)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(0, Qt.CheckState.Checked if f.enabled else Qt.CheckState.Unchecked)
                item.setText(0, f.title)
                item.setText(_COL_ID, str(f.id))
                item.setText(_COL_UPDATED, f.last_update)
                if f.is_custom:
                    item.setForeground(0, QColor("#f59e0b"))

        self.tree.expandAll()
        self.tree.itemChanged.connect(self._on_item_changed)

    # ── Toggle ────────────────────────────────────────────────────────────

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        if column != 0:
            return
        fid = item.data(0, Qt.ItemDataRole.UserRole)
        if fid is None:
            return
        enable = item.checkState(0) == Qt.CheckState.Checked
        self._set_busy(True)
        self.tree.itemChanged.disconnect(self._on_item_changed)
        w = _ToggleWorker(self.cli, fid, enable)
        w.done.connect(self._on_toggle_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_toggle_done(self, ok: bool, msg: str, fid: int, new_enabled: bool) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            if fid in self._filter_map:
                self._filter_map[fid].enabled = new_enabled
            self.lbl_status.setText(
                _t("DNS filter {} enabled.", fid) if new_enabled else _t("DNS filter {} disabled.", fid)
            )
        else:
            # Revert
            for i in range(self.tree.topLevelItemCount()):
                group = self.tree.topLevelItem(i)
                for j in range(group.childCount()):
                    child = group.child(j)
                    if child.data(0, Qt.ItemDataRole.UserRole) == fid:
                        child.setCheckState(
                            0, Qt.CheckState.Checked if not new_enabled else Qt.CheckState.Unchecked
                        )
                        break
            self.lbl_status.setText(_t("Error: {}", msg))
        self.tree.itemChanged.connect(self._on_item_changed)

    # ── Install / Add ─────────────────────────────────────────────────────

    def _add_custom_filter(self) -> None:
        dlg = _InstallDnsFilterDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        url = dlg.url.strip()
        if not url:
            return
        self._set_busy(True)
        self.lbl_status.setText(_t("Installing: {}", url))
        w = _InstallWorker(self.cli, url, dlg.title.strip())
        w.done.connect(self._on_install_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_install_done(self, ok: bool, msg: str) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            self.lbl_status.setText(_t("DNS filter installed."))
            self._load_filters()
        else:
            self.lbl_status.setText(_t("Error: {}", msg))

    def _add_by_id(self) -> None:
        text, ok = QInputDialog.getText(
            self, _t("Add DNS Filter by ID"), _t("Enter filter ID or name:"),
            QLineEdit.EchoMode.Normal,
        )
        if not ok or not text.strip():
            return
        val = text.strip()
        self._set_busy(True)
        self.lbl_status.setText(_t("Adding DNS filter: {}", val))
        w = _ActionWorker(lambda t=val: self.cli.add_dns_filter(t))
        w.done.connect(self._on_add_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_add_done(self, ok: bool, msg: str) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            self.lbl_status.setText(_t("DNS filter added."))
            self._load_filters()
        else:
            self.lbl_status.setText(_t("Error: {}", msg))

    # ── Context menu ──────────────────────────────────────────────────────

    def _on_context_menu(self, pos) -> None:
        from PyQt6.QtWidgets import QMenu
        item = self.tree.itemAt(pos)
        if item is None:
            return
        fid = item.data(0, Qt.ItemDataRole.UserRole)
        if fid is None:
            return
        f = self._filter_map.get(fid)
        if f is None:
            return

        menu = QMenu(self)
        act_remove = menu.addAction(_t("Remove"))
        act_remove.triggered.connect(lambda: self._remove_filter(fid))
        if f.is_custom:
            act_rename = menu.addAction(_t("Rename…"))
            act_rename.triggered.connect(lambda: self._rename_filter(fid))
        menu.exec(self.tree.viewport().mapToGlobal(pos))

    def _remove_filter(self, fid: int) -> None:
        f = self._filter_map.get(fid)
        name = f.title if f else str(fid)
        reply = QMessageBox.question(
            self, _t("Remove DNS filter"), _t('Really remove DNS filter "{}"?', name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        self._set_busy(True)
        w = _RemoveWorker(self.cli, fid)
        w.done.connect(self._on_remove_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_remove_done(self, ok: bool, msg: str, fid: int) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            self.lbl_status.setText(_t("DNS filter {} removed.", fid))
            self._load_filters()
        else:
            self.lbl_status.setText(_t("Error: {}", msg))

    def _rename_filter(self, fid: int) -> None:
        f = self._filter_map.get(fid)
        old_name = f.title if f else ""
        new_name, ok = QInputDialog.getText(
            self, _t("Rename DNS filter"), _t("New title:"),
            QLineEdit.EchoMode.Normal, old_name,
        )
        if not ok or not new_name.strip():
            return
        self._set_busy(True)
        w = _ActionWorker(lambda: self.cli.set_dns_filter_title(fid, new_name.strip()))
        w.done.connect(lambda ok, msg: self._on_generic_done(ok, msg, _t("DNS filter renamed.")))
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_generic_done(self, ok: bool, msg: str, success_msg: str) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            self.lbl_status.setText(success_msg)
            self._load_filters()
        else:
            self.lbl_status.setText(_t("Error: {}", msg))

    # ── Search ────────────────────────────────────────────────────────────

    def _apply_search(self, text: str) -> None:
        needle = text.strip().lower()
        for i in range(self.tree.topLevelItemCount()):
            group = self.tree.topLevelItem(i)
            visible = 0
            for j in range(group.childCount()):
                child = group.child(j)
                match = not needle or needle in child.text(0).lower()
                child.setHidden(not match)
                if match:
                    visible += 1
            group.setHidden(visible == 0)

    def _set_busy(self, busy: bool) -> None:
        self.btn_add.setEnabled(not busy)
        self.btn_add_id.setEnabled(not busy)
        self.btn_reload.setEnabled(not busy)
        self.tree.setEnabled(not busy)
        self.progress.setVisible(busy)


class _InstallDnsFilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_t("Add Custom DNS Filter"))
        self.setMinimumWidth(480)
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self._url_edit = QLineEdit()
        self._url_edit.setPlaceholderText("https://example.com/hosts.txt")
        form.addRow(_t("Filter URL:"), self._url_edit)

        self._title_edit = QLineEdit()
        self._title_edit.setPlaceholderText(_t("(optional)"))
        form.addRow(_t("Title:"), self._title_edit)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    @property
    def url(self) -> str:
        return self._url_edit.text()

    @property
    def title(self) -> str:
        return self._title_edit.text()
