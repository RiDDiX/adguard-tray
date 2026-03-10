"""
Filter management dialog.

Features:
  - Lists all active filters grouped by category (tree view)
  - Toggle enable/disable per filter via checkbox
  - Update all filters (adguard-cli check-update)
  - Install custom filter by URL
  - Remove custom filters
  - Reload filter list from CLI
"""

import logging

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QFont, QIcon
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .cli import AdGuardCLI, FilterEntry, FilterListResult

logger = logging.getLogger(__name__)

_COL_NAME = 0
_COL_ID = 1
_COL_UPDATED = 2


# ── Background workers ─────────────────────────────────────────────────────

class _LoadWorker(QThread):
    done = pyqtSignal(object)   # FilterListResult

    def __init__(self, cli: AdGuardCLI) -> None:
        super().__init__()
        self.cli = cli

    def run(self) -> None:
        self.done.emit(self.cli.get_filters())


class _UpdateWorker(QThread):
    done = pyqtSignal(bool, str)

    def __init__(self, cli: AdGuardCLI) -> None:
        super().__init__()
        self.cli = cli

    def run(self) -> None:
        ok, msg = self.cli.update_filters()
        self.done.emit(ok, msg)


class _ToggleWorker(QThread):
    done = pyqtSignal(bool, str, int, bool)  # ok, msg, filter_id, new_enabled

    def __init__(self, cli: AdGuardCLI, filter_id: int, enable: bool) -> None:
        super().__init__()
        self.cli = cli
        self.filter_id = filter_id
        self.enable = enable

    def run(self) -> None:
        if self.enable:
            ok, msg = self.cli.enable_filter(self.filter_id)
        else:
            ok, msg = self.cli.disable_filter(self.filter_id)
        self.done.emit(ok, msg, self.filter_id, self.enable)


class _RemoveWorker(QThread):
    done = pyqtSignal(bool, str, int)

    def __init__(self, cli: AdGuardCLI, filter_id: int) -> None:
        super().__init__()
        self.cli = cli
        self.filter_id = filter_id

    def run(self) -> None:
        ok, msg = self.cli.remove_filter(self.filter_id)
        self.done.emit(ok, msg, self.filter_id)


class _InstallWorker(QThread):
    done = pyqtSignal(bool, str)

    def __init__(self, cli: AdGuardCLI, url: str) -> None:
        super().__init__()
        self.cli = cli
        self.url = url

    def run(self) -> None:
        ok, msg = self.cli.install_filter(self.url)
        self.done.emit(ok, msg)


# ── Main dialog ────────────────────────────────────────────────────────────

class FiltersDialog(QDialog):
    def __init__(self, cli: AdGuardCLI, parent=None) -> None:
        super().__init__(parent)
        self.cli = cli
        self._workers: list[QThread] = []  # keep refs alive
        self._filter_map: dict[int, FilterEntry] = {}

        self.setWindowTitle("AdGuard Tray – Filter verwalten")
        self.setMinimumSize(700, 520)
        self.resize(760, 580)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self._build_ui()
        self._load_filters()

    # ── UI construction ────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # ── Toolbar ────────────────────────────────────────────────────────
        toolbar = QHBoxLayout()

        self.btn_update = QPushButton("Filter aktualisieren")
        self.btn_update.setToolTip(
            "Aktualisiert alle Filter, DNS-Filter, Userscripts,\n"
            "SafebrowsingV2, CRLite und prüft auf App-Updates."
        )
        self.btn_update.clicked.connect(self._run_update)
        toolbar.addWidget(self.btn_update)

        self.btn_add = QPushButton("Eigenen Filter hinzufügen…")
        self.btn_add.setToolTip("Custom-Filter per URL installieren")
        self.btn_add.clicked.connect(self._add_custom_filter)
        toolbar.addWidget(self.btn_add)

        toolbar.addStretch()

        self.btn_reload = QPushButton("↺ Neu laden")
        self.btn_reload.clicked.connect(self._load_filters)
        toolbar.addWidget(self.btn_reload)

        layout.addLayout(toolbar)

        # ── Progress / status bar ──────────────────────────────────────────
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)   # indeterminate
        self.progress.setMaximumHeight(4)
        self.progress.hide()
        layout.addWidget(self.progress)

        self.lbl_status = QLabel("")
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

        # ── Filter tree ────────────────────────────────────────────────────
        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Filter", "ID", "Zuletzt aktualisiert"])
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.setAlternatingRowColors(True)
        self.tree.setAnimated(True)
        self.tree.setUniformRowHeights(True)
        self.tree.setExpandsOnDoubleClick(True)
        self.tree.setSortingEnabled(False)
        layout.addWidget(self.tree)

        # ── Update output box ──────────────────────────────────────────────
        self.update_output = QLabel("")
        self.update_output.setWordWrap(True)
        self.update_output.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.update_output.hide()
        layout.addWidget(self.update_output)

        # ── Close button ───────────────────────────────────────────────────
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # ── Filter loading ─────────────────────────────────────────────────────

    def _load_filters(self) -> None:
        self._set_busy(True)
        self.lbl_status.setText("Filter werden geladen…")
        w = _LoadWorker(self.cli)
        w.done.connect(self._on_filters_loaded)
        w.finished.connect(lambda: self._workers.remove(w))
        self._workers.append(w)
        w.start()

    def _on_filters_loaded(self, result: FilterListResult) -> None:
        self._set_busy(False)
        self.tree.clear()
        self._filter_map.clear()

        if result.error:
            self.lbl_status.setText(f"Fehler: {result.error}")
            return

        if not result.groups:
            self.lbl_status.setText("Keine Filter gefunden.")
            return

        total = sum(len(v) for v in result.groups.values())
        active = sum(1 for f in result.all_filters if f.enabled)
        self.lbl_status.setText(f"{active} von {total} Filtern aktiv")

        for group_name, filters in result.groups.items():
            group_item = QTreeWidgetItem(self.tree)
            group_item.setText(0, group_name)
            group_item.setFlags(group_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
            group_item.setExpanded(True)

            # Bold group header
            font = group_item.font(0)
            font.setBold(True)
            group_item.setFont(0, font)
            group_item.setForeground(0, QColor("#5b9bd5"))

            for f in filters:
                self._filter_map[f.id] = f
                self._add_filter_item(group_item, f)

        self.tree.expandAll()

    def _add_filter_item(self, parent: QTreeWidgetItem, f: FilterEntry) -> QTreeWidgetItem:
        item = QTreeWidgetItem(parent)
        item.setData(0, Qt.ItemDataRole.UserRole, f.id)

        # Checkbox via item check state
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(
            0,
            Qt.CheckState.Checked if f.enabled else Qt.CheckState.Unchecked,
        )
        item.setText(0, f.title)
        item.setText(_COL_ID, str(f.id))
        item.setText(_COL_UPDATED, f.last_update)
        item.setToolTip(0, f.title)

        # Remove button for custom filters (id < 0)
        if f.is_custom:
            item.setForeground(0, QColor("#f59e0b"))

        return item

    # ── Checkbox toggle ────────────────────────────────────────────────────

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        if column != 0:
            return
        fid = item.data(0, Qt.ItemDataRole.UserRole)
        if fid is None:
            return

        enable = item.checkState(0) == Qt.CheckState.Checked
        self._set_busy(True)
        self.lbl_status.setText(
            f"Filter {fid} wird {'aktiviert' if enable else 'deaktiviert'}…"
        )

        # Disconnect during operation to avoid recursive signals
        self.tree.itemChanged.disconnect(self._on_item_changed)

        w = _ToggleWorker(self.cli, fid, enable)
        w.done.connect(self._on_toggle_done)
        w.finished.connect(lambda: self._workers.remove(w))
        self._workers.append(w)
        w.start()

    def _on_toggle_done(self, ok: bool, msg: str, fid: int, new_enabled: bool) -> None:
        self._set_busy(False)
        if ok:
            if fid in self._filter_map:
                self._filter_map[fid].enabled = new_enabled
            state = "aktiviert" if new_enabled else "deaktiviert"
            self.lbl_status.setText(f"Filter {fid} {state}.")
        else:
            # Revert checkbox
            self._revert_checkbox(fid, not new_enabled)
            self.lbl_status.setText(f"Fehler: {msg}")

        self.tree.itemChanged.connect(self._on_item_changed)

    def _revert_checkbox(self, fid: int, revert_to: bool) -> None:
        for i in range(self.tree.topLevelItemCount()):
            group = self.tree.topLevelItem(i)
            for j in range(group.childCount()):
                child = group.child(j)
                if child.data(0, Qt.ItemDataRole.UserRole) == fid:
                    self.tree.itemChanged.disconnect(self._on_item_changed)
                    child.setCheckState(
                        0,
                        Qt.CheckState.Checked if revert_to else Qt.CheckState.Unchecked,
                    )
                    self.tree.itemChanged.connect(self._on_item_changed)
                    return

    # ── Update all filters ─────────────────────────────────────────────────

    def _run_update(self) -> None:
        self._set_busy(True)
        self.lbl_status.setText("Filter werden aktualisiert…")
        self.update_output.hide()
        w = _UpdateWorker(self.cli)
        w.done.connect(self._on_update_done)
        w.finished.connect(lambda: self._workers.remove(w))
        self._workers.append(w)
        w.start()

    def _on_update_done(self, ok: bool, msg: str) -> None:
        self._set_busy(False)
        if ok:
            self.lbl_status.setText("Aktualisierung abgeschlossen.")
        else:
            self.lbl_status.setText("Aktualisierung fehlgeschlagen.")

        # Show full output in the collapsible label
        self.update_output.setText(msg)
        self.update_output.show()

        # Reload list so last-update timestamps refresh
        self._load_filters()

    # ── Custom filter install ──────────────────────────────────────────────

    def _add_custom_filter(self) -> None:
        url, ok = QInputDialog.getText(
            self,
            "Eigenen Filter hinzufügen",
            "Filter-URL (direkte .txt-URL der Filterliste):",
            QLineEdit.EchoMode.Normal,
        )
        if not ok or not url.strip():
            return

        url = url.strip()
        self._set_busy(True)
        self.lbl_status.setText(f"Installiere: {url}")
        w = _InstallWorker(self.cli, url)
        w.done.connect(self._on_install_done)
        w.finished.connect(lambda: self._workers.remove(w))
        self._workers.append(w)
        w.start()

    def _on_install_done(self, ok: bool, msg: str) -> None:
        self._set_busy(False)
        if ok:
            self.lbl_status.setText("Filter installiert.")
            self._load_filters()
        else:
            self.lbl_status.setText(f"Fehler: {msg}")

    # ── Context menu (right-click) ─────────────────────────────────────────

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
            act_remove = menu.addAction("Entfernen")
            act_remove.triggered.connect(lambda: self._remove_filter(fid))
        menu.exec(self.tree.viewport().mapToGlobal(pos))

    def _remove_filter(self, fid: int) -> None:
        f = self._filter_map.get(fid)
        name = f.title if f else str(fid)
        reply = QMessageBox.question(
            self,
            "Filter entfernen",
            f"Filter «{name}» wirklich entfernen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self._set_busy(True)
        self.lbl_status.setText(f"Filter {fid} wird entfernt…")
        w = _RemoveWorker(self.cli, fid)
        w.done.connect(self._on_remove_done)
        w.finished.connect(lambda: self._workers.remove(w))
        self._workers.append(w)
        w.start()

    def _on_remove_done(self, ok: bool, msg: str, fid: int) -> None:
        self._set_busy(False)
        if ok:
            self.lbl_status.setText(f"Filter {fid} entfernt.")
            self._load_filters()
        else:
            self.lbl_status.setText(f"Fehler: {msg}")

    # ── Helpers ────────────────────────────────────────────────────────────

    def _set_busy(self, busy: bool) -> None:
        self.btn_update.setEnabled(not busy)
        self.btn_add.setEnabled(not busy)
        self.btn_reload.setEnabled(not busy)
        self.tree.setEnabled(not busy)
        if busy:
            self.progress.show()
        else:
            self.progress.hide()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        # Connect itemChanged here (after tree is shown) to avoid signals during build
        self.tree.itemChanged.connect(self._on_item_changed)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._on_context_menu)
