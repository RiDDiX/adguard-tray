"""
Userscripts tab for the Manager window.

Reuses the core logic from userscripts_dialog but as a QWidget tab page
instead of a QDialog.
"""

import logging

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
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

from .cli import AdGuardCLI, UserscriptEntry, UserscriptListResult
from .i18n import _t

logger = logging.getLogger(__name__)

_COL_NAME = 0
_COL_ID = 1
_COL_UPDATED = 2


class _LoadWorker(QThread):
    done = pyqtSignal(object)
    def __init__(self, cli): super().__init__(); self.cli = cli
    def run(self): self.done.emit(self.cli.get_userscripts())

class _ToggleWorker(QThread):
    done = pyqtSignal(bool, str, str, bool)
    def __init__(self, cli, name, enable):
        super().__init__(); self.cli = cli; self.name = name; self.enable = enable
    def run(self):
        fn = self.cli.enable_userscript if self.enable else self.cli.disable_userscript
        ok, msg = fn(self.name)
        self.done.emit(ok, msg, self.name, self.enable)

class _RemoveWorker(QThread):
    done = pyqtSignal(bool, str, str)
    def __init__(self, cli, name): super().__init__(); self.cli = cli; self.name = name
    def run(self): self.done.emit(*self.cli.remove_userscript(self.name), self.name)

class _InstallWorker(QThread):
    done = pyqtSignal(bool, str)
    def __init__(self, cli, url): super().__init__(); self.cli = cli; self.url = url
    def run(self): self.done.emit(*self.cli.install_userscript(self.url))


class UserscriptsTab(QWidget):
    def __init__(self, cli: AdGuardCLI, on_change=None, parent=None) -> None:
        super().__init__(parent)
        self.cli = cli
        self._on_change = on_change
        self._workers: list[QThread] = []
        self._script_map: dict[str, UserscriptEntry] = {}
        self._changed = False

        self._build_ui()
        self._load()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        bar = QHBoxLayout()
        self.btn_add = QPushButton(_t("Install (URL)…"))
        self.btn_add.setToolTip(_t("Install userscript from a direct .js URL"))
        self.btn_add.clicked.connect(self._install)
        bar.addWidget(self.btn_add)
        bar.addStretch()
        self.btn_reload = QPushButton(_t("↺ Reload"))
        self.btn_reload.clicked.connect(self._load)
        bar.addWidget(self.btn_reload)
        layout.addLayout(bar)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setMaximumHeight(4)
        self.progress.hide()
        layout.addWidget(self.progress)

        self.lbl_status = QLabel("")
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(_t("Search userscripts…"))
        self.search_box.setClearButtonEnabled(True)
        self.search_box.textChanged.connect(self._apply_search)
        layout.addWidget(self.search_box)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels([_t("Userscript"), _t("ID / Name"), _t("Last updated")])
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.setAlternatingRowColors(True)
        self.tree.setUniformRowHeights(True)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._on_context_menu)
        layout.addWidget(self.tree)

        info = QLabel(_t(
            "<small>Right-click a userscript to remove it.<br>"
            "Userscripts are automatically updated when running "
            "<i>Update filters</i>.</small>"
        ))
        info.setTextFormat(Qt.TextFormat.RichText)
        info.setWordWrap(True)
        layout.addWidget(info)

    def _load(self) -> None:
        self._set_busy(True)
        self.lbl_status.setText(_t("Loading userscripts…"))
        w = _LoadWorker(self.cli)
        w.done.connect(self._on_loaded)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_loaded(self, result: UserscriptListResult) -> None:
        self._set_busy(False)
        try:
            self.tree.itemChanged.disconnect(self._on_item_changed)
        except TypeError:
            pass
        self.tree.clear()
        self._script_map.clear()

        if result.error:
            self.lbl_status.setText(_t("Error: {}", result.error))
            return
        if not result.scripts:
            self.lbl_status.setText(_t("No userscripts installed."))
            return

        active = sum(1 for s in result.scripts if s.enabled)
        self.lbl_status.setText(_t("{} of {} userscripts active", active, len(result.scripts)))

        for s in result.scripts:
            self._script_map[s.name] = s
            item = QTreeWidgetItem(self.tree)
            item.setData(0, Qt.ItemDataRole.UserRole, s.name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(0, Qt.CheckState.Checked if s.enabled else Qt.CheckState.Unchecked)
            item.setText(_COL_NAME, s.title)
            item.setText(_COL_ID, s.name)
            item.setText(_COL_UPDATED, s.last_update)
            item.setToolTip(0, f"{s.title} ({s.name})")

        self.tree.itemChanged.connect(self._on_item_changed)

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        if column != 0:
            return
        name = item.data(0, Qt.ItemDataRole.UserRole)
        if not name:
            return
        enable = item.checkState(0) == Qt.CheckState.Checked
        self._set_busy(True)
        self.tree.itemChanged.disconnect(self._on_item_changed)
        w = _ToggleWorker(self.cli, name, enable)
        w.done.connect(self._on_toggle_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_toggle_done(self, ok: bool, msg: str, name: str, new_enabled: bool) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            if name in self._script_map:
                self._script_map[name].enabled = new_enabled
            self.lbl_status.setText(
                _t("Userscript '{}' enabled.", name) if new_enabled
                else _t("Userscript '{}' disabled.", name)
            )
        else:
            for i in range(self.tree.topLevelItemCount()):
                child = self.tree.topLevelItem(i)
                if child.data(0, Qt.ItemDataRole.UserRole) == name:
                    child.setCheckState(
                        0, Qt.CheckState.Checked if not new_enabled else Qt.CheckState.Unchecked
                    )
                    break
            self.lbl_status.setText(_t("Error: {}", msg))
        self.tree.itemChanged.connect(self._on_item_changed)

    def _install(self) -> None:
        url, ok = QInputDialog.getText(
            self, _t("Install Userscript"), _t("Userscript URL (direct .js URL):"),
            QLineEdit.EchoMode.Normal,
        )
        if not ok or not url.strip():
            return
        self._set_busy(True)
        self.lbl_status.setText(_t("Installing: {}", url.strip()))
        w = _InstallWorker(self.cli, url.strip())
        w.done.connect(self._on_install_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_install_done(self, ok: bool, msg: str) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            self.lbl_status.setText(_t("Userscript installed."))
            self._load()
        else:
            self.lbl_status.setText(_t("Error: {}", msg))

    def _on_context_menu(self, pos) -> None:
        from PyQt6.QtWidgets import QMenu
        item = self.tree.itemAt(pos)
        if item is None:
            return
        name = item.data(0, Qt.ItemDataRole.UserRole)
        if not name:
            return
        menu = QMenu(self)
        act = menu.addAction(_t('Remove "{}"', name))
        act.triggered.connect(lambda: self._remove(name))
        menu.exec(self.tree.viewport().mapToGlobal(pos))

    def _remove(self, name: str) -> None:
        s = self._script_map.get(name)
        display = s.title if s else name
        reply = QMessageBox.question(
            self, _t("Remove userscript"), _t('Really remove userscript "{}"?', display),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        self._set_busy(True)
        w = _RemoveWorker(self.cli, name)
        w.done.connect(self._on_remove_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_remove_done(self, ok: bool, msg: str, name: str) -> None:
        self._set_busy(False)
        if ok:
            self._changed = True
            self.lbl_status.setText(_t("'{}' removed.", name))
            self._load()
        else:
            self.lbl_status.setText(_t("Error: {}", msg))

    def _apply_search(self, text: str) -> None:
        needle = text.strip().lower()
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            match = not needle or needle in item.text(0).lower() or needle in item.text(1).lower()
            item.setHidden(not match)

    def _set_busy(self, busy: bool) -> None:
        self.btn_add.setEnabled(not busy)
        self.btn_reload.setEnabled(not busy)
        self.tree.setEnabled(not busy)
        self.progress.setVisible(busy)
