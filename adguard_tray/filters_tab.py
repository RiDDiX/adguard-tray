"""
Filters tab for the Manager window.

Enhanced version of filters_dialog with:
  - "Show all available" toggle
  - "Add by ID/name" button
  - Context menu: set-trusted, rename (set-title) for custom filters
  - Install with --trusted and --title options
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


# ── Background workers ─────────────────────────────────────────────────────

class _LoadWorker(QThread):
    done = pyqtSignal(object)

    def __init__(self, cli, all_available):
        super().__init__()
        self.cli = cli
        self.all_available = all_available

    def run(self):
        self.done.emit(self.cli.get_filters(all_available=self.all_available))


class _UpdateWorker(QThread):
    done = pyqtSignal(bool, str)

    def __init__(self, cli):
        super().__init__()
        self.cli = cli

    def run(self):
        self.done.emit(*self.cli.update_filters())


class _ToggleWorker(QThread):
    done = pyqtSignal(bool, str, int, bool)

    def __init__(self, cli, fid, enable):
        super().__init__()
        self.cli = cli
        self.fid = fid
        self.enable = enable

    def run(self):
        fn = self.cli.enable_filter if self.enable else self.cli.disable_filter
        ok, msg = fn(self.fid)
        self.done.emit(ok, msg, self.fid, self.enable)


class _RemoveWorker(QThread):
    done = pyqtSignal(bool, str, int)

    def __init__(self, cli, fid):
        super().__init__()
        self.cli = cli
        self.fid = fid

    def run(self):
        self.done.emit(*self.cli.remove_filter(self.fid), self.fid)


class _InstallWorker(QThread):
    done = pyqtSignal(bool, str)

    def __init__(self, cli, url, trusted, title):
        super().__init__()
        self.cli = cli
        self.url = url
        self.trusted = trusted
        self.title = title

    def run(self):
        self.done.emit(*self.cli.install_filter_ext(self.url, self.trusted, self.title))


class _ActionWorker(QThread):
    done = pyqtSignal(bool, str)

    def __init__(self, fn):
        super().__init__()
        self._fn = fn

    def run(self):
        self.done.emit(*self._fn())


# ── Tab widget ────────────────────────────────────────────────────────────

class FiltersTab(QWidget):
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

        # Toolbar
        toolbar = QHBoxLayout()

        self.btn_update = QPushButton(_t("Update filters"))
        self.btn_update.setToolTip(_t(
            "Updates all filters, DNS filters, userscripts,\n"
            "SafebrowsingV2, CRLite and checks for app updates."
        ))
        self.btn_update.clicked.connect(self._run_update)
        toolbar.addWidget(self.btn_update)

        self.btn_add = QPushButton(_t("Add custom filter…"))
        self.btn_add.setToolTip(_t("Install custom filter by URL"))
        self.btn_add.clicked.connect(self._add_custom_filter)
        toolbar.addWidget(self.btn_add)

        self.btn_add_id = QPushButton(_t("Add by ID…"))
        self.btn_add_id.setToolTip(_t("Add internal filter by ID or name"))
        self.btn_add_id.clicked.connect(self._add_by_id)
        toolbar.addWidget(self.btn_add_id)

        toolbar.addStretch()

        self.cb_show_all = QCheckBox(_t("Show all available"))
        self.cb_show_all.setToolTip(_t("Show all available filters, not just installed ones"))
        self.cb_show_all.toggled.connect(self._load_filters)
        toolbar.addWidget(self.cb_show_all)

        self.btn_reload = QPushButton(_t("↺ Reload"))
        self.btn_reload.clicked.connect(self._load_filters)
        toolbar.addWidget(self.btn_reload)

        layout.addLayout(toolbar)

        # Progress
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setMaximumHeight(4)
        self.progress.hide()
        layout.addWidget(self.progress)

        self.lbl_status = QLabel("")
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

        # Search
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(_t("Search filters…"))
        self.search_box.setClearButtonEnabled(True)
        self.search_box.textChanged.connect(self._apply_search_filter)
        layout.addWidget(self.search_box)

        # Tree
        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels([_t("Filter"), _t("ID"), _t("Last updated")])
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.setAlternatingRowColors(True)
        self.tree.setAnimated(True)
        self.tree.setUniformRowHeights(True)
        self.tree.setSortingEnabled(False)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._on_context_menu)
        layout.addWidget(self.tree)

        # Update output
        self.update_output = QLabel("")
        self.update_output.setWordWrap(True)
        self.update_output.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.update_output.hide()
        layout.addWidget(self.update_output)

    # ── Loading ───────────────────────────────────────────────────────────

    def _load_filters(self) -> None:
        self._set_busy(True)
        self.lbl_status.setText(_t("Loading filters…"))
        show_all = self.cb_show_all.isChecked()
        w = _LoadWorker(self.cli, show_all)
        w.done.connect(self._on_filters_loaded)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_filters_loaded(self, result: FilterListResult) -> None:
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

        if not result.groups:
            self.lbl_status.setText(_t("No filters found."))
            self.tree.itemChanged.connect(self._on_item_changed)
            return

        total = sum(len(v) for v in result.groups.values())
        active = sum(1 for f in result.all_filters if f.enabled)
        self.lbl_status.setText(_t("{} of {} filters active", active, total))

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
                item.setToolTip(0, f.title)
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
        self.lbl_status.setText(
            _t("Enabling filter {}…", fid) if enable else _t("Disabling filter {}…", fid)
        )
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
                _t("Filter {} enabled.", fid) if new_enabled else _t("Filter {} disabled.", fid)
            )
        else:
            self._revert_checkbox(fid, not new_enabled)
            self.lbl_status.setText(_t("Error: {}", msg))
        self.tree.itemChanged.connect(self._on_item_changed)

    def _revert_checkbox(self, fid: int, revert_to: bool) -> None:
        for i in range(self.tree.topLevelItemCount()):
            group = self.tree.topLevelItem(i)
            for j in range(group.childCount()):
                child = group.child(j)
                if child.data(0, Qt.ItemDataRole.UserRole) == fid:
                    child.setCheckState(0, Qt.CheckState.Checked if revert_to else Qt.CheckState.Unchecked)
                    return

    # ── Update all ────────────────────────────────────────────────────────

    def _run_update(self) -> None:
        self._set_busy(True)
        self.lbl_status.setText(_t("Updating filters…"))
        self.update_output.hide()
        w = _UpdateWorker(self.cli)
        w.done.connect(self._on_update_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_update_done(self, ok: bool, msg: str) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            self.lbl_status.setText(_t("Update completed."))
        else:
            self.lbl_status.setText(_t("Update failed."))
        self.update_output.setText(msg)
        self.update_output.show()
        self._load_filters()

    # ── Custom filter install (enhanced) ──────────────────────────────────

    def _add_custom_filter(self) -> None:
        dlg = _InstallFilterDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        url = dlg.url.strip()
        if not url:
            return
        trusted = dlg.trusted
        title = dlg.title.strip()

        self._set_busy(True)
        self.lbl_status.setText(_t("Installing: {}", url))
        w = _InstallWorker(self.cli, url, trusted, title)
        w.done.connect(self._on_install_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_install_done(self, ok: bool, msg: str) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            self.lbl_status.setText(_t("Filter installed."))
            self._load_filters()
        else:
            self.lbl_status.setText(_t("Error: {}", msg))

    # ── Add by ID ─────────────────────────────────────────────────────────

    def _add_by_id(self) -> None:
        text, ok = QInputDialog.getText(
            self,
            _t("Add Filter by ID"),
            _t("Enter filter ID or name:"),
            QLineEdit.EchoMode.Normal,
        )
        if not ok or not text.strip():
            return
        val = text.strip()
        self._set_busy(True)
        self.lbl_status.setText(_t("Adding filter: {}", val))
        w = _ActionWorker(lambda t=val: self.cli.add_filter(t))
        w.done.connect(self._on_add_id_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_add_id_done(self, ok: bool, msg: str) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            self.lbl_status.setText(_t("Filter added."))
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
        if f.is_custom:
            act_remove = menu.addAction(_t("Remove"))
            act_remove.triggered.connect(lambda: self._remove_filter(fid))
            act_rename = menu.addAction(_t("Rename…"))
            act_rename.triggered.connect(lambda: self._rename_filter(fid))
            act_trust = menu.addAction(_t("Set trusted"))
            act_trust.triggered.connect(lambda: self._set_trusted(fid, True))
            act_untrust = menu.addAction(_t("Set untrusted"))
            act_untrust.triggered.connect(lambda: self._set_trusted(fid, False))
        else:
            act_remove = menu.addAction(_t("Remove"))
            act_remove.triggered.connect(lambda: self._remove_filter(fid))
        menu.exec(self.tree.viewport().mapToGlobal(pos))

    def _remove_filter(self, fid: int) -> None:
        f = self._filter_map.get(fid)
        name = f.title if f else str(fid)
        reply = QMessageBox.question(
            self, _t("Remove filter"), _t('Really remove filter "{}"?', name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        self._set_busy(True)
        self.lbl_status.setText(_t("Removing filter {}…", fid))
        w = _RemoveWorker(self.cli, fid)
        w.done.connect(self._on_remove_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_remove_done(self, ok: bool, msg: str, fid: int) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            self.lbl_status.setText(_t("Filter {} removed.", fid))
            self._load_filters()
        else:
            self.lbl_status.setText(_t("Error: {}", msg))

    def _rename_filter(self, fid: int) -> None:
        f = self._filter_map.get(fid)
        old_name = f.title if f else ""
        new_name, ok = QInputDialog.getText(
            self, _t("Rename filter"), _t("New title:"),
            QLineEdit.EchoMode.Normal, old_name,
        )
        if not ok or not new_name.strip():
            return
        self._set_busy(True)
        self.lbl_status.setText(_t("Renaming filter {}…", fid))
        w = _ActionWorker(lambda: self.cli.set_filter_title(fid, new_name.strip()))
        w.done.connect(lambda ok, msg: self._on_action_done(ok, msg, _t("Filter renamed.")))
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _set_trusted(self, fid: int, trusted: bool) -> None:
        self._set_busy(True)
        label = _t("trusted") if trusted else _t("untrusted")
        self.lbl_status.setText(_t("Setting filter {} as {}…", fid, label))
        w = _ActionWorker(lambda: self.cli.set_filter_trusted(fid, trusted))
        w.done.connect(lambda ok, msg: self._on_action_done(ok, msg, _t("Filter trust updated.")))
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_action_done(self, ok: bool, msg: str, success_msg: str) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            self.lbl_status.setText(success_msg)
            self._load_filters()
        else:
            self.lbl_status.setText(_t("Error: {}", msg))

    # ── Search ────────────────────────────────────────────────────────────

    def _apply_search_filter(self, text: str) -> None:
        needle = text.strip().lower()
        for i in range(self.tree.topLevelItemCount()):
            group = self.tree.topLevelItem(i)
            visible_children = 0
            for j in range(group.childCount()):
                child = group.child(j)
                match = not needle or needle in child.text(0).lower()
                child.setHidden(not match)
                if match:
                    visible_children += 1
            group.setHidden(visible_children == 0)

    # ── Helpers ───────────────────────────────────────────────────────────

    def _set_busy(self, busy: bool) -> None:
        self.btn_update.setEnabled(not busy)
        self.btn_add.setEnabled(not busy)
        self.btn_add_id.setEnabled(not busy)
        self.btn_reload.setEnabled(not busy)
        self.tree.setEnabled(not busy)
        self.progress.setVisible(busy)


# ── Install filter dialog (with trusted + title) ─────────────────────────

class _InstallFilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_t("Add Custom Filter"))
        self.setMinimumWidth(480)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self._url_edit = QLineEdit()
        self._url_edit.setPlaceholderText("https://example.com/filter.txt")
        form.addRow(_t("Filter URL:"), self._url_edit)

        self._title_edit = QLineEdit()
        self._title_edit.setPlaceholderText(_t("(optional)"))
        form.addRow(_t("Title:"), self._title_edit)

        self._trusted_cb = QCheckBox(_t("Trusted filter"))
        self._trusted_cb.setToolTip(_t(
            "Trusted filters can use advanced rules (JS scriptlets, etc.)"
        ))
        form.addRow("", self._trusted_cb)

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

    @property
    def trusted(self) -> bool:
        return self._trusted_cb.isChecked()
