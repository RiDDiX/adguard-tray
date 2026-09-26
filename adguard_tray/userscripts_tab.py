"""Userscripts – install, switch on/off and remove userscripts."""

import logging

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
)

from . import ui
from .cli import UserscriptEntry, UserscriptListResult
from .i18n import _t
from .manager_window import PAGE_ABOUT
from .worker import safe_call, safe_result

logger = logging.getLogger(__name__)

_SCHEMES = ("http://", "https://")


class _LoadWorker(QThread):
    done = pyqtSignal(object)
    def __init__(self, cli): super().__init__(); self.cli = cli
    def run(self): self.done.emit(safe_result(self.cli.get_userscripts, UserscriptListResult))

class _ToggleWorker(QThread):
    done = pyqtSignal(bool, str, str, bool)
    def __init__(self, cli, name, enable):
        super().__init__(); self.cli = cli; self.name = name; self.enable = enable
    def run(self):
        fn = self.cli.enable_userscript if self.enable else self.cli.disable_userscript
        ok, msg = safe_call(fn, self.name)
        self.done.emit(ok, msg, self.name, self.enable)

class _RemoveWorker(QThread):
    done = pyqtSignal(bool, str, str)
    def __init__(self, cli, name): super().__init__(); self.cli = cli; self.name = name
    def run(self): self.done.emit(*safe_call(self.cli.remove_userscript, self.name), self.name)

class _InstallWorker(QThread):
    done = pyqtSignal(bool, str)
    def __init__(self, cli, url): super().__init__(); self.cli = cli; self.url = url
    def run(self): self.done.emit(*safe_call(self.cli.install_userscript, self.url))


class _UrlDialog(QDialog):
    """Asks for the script's URL. Add stays off until it is an http(s) URL, so
    nothing typed is lost to a warning after the dialog has closed."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(_t("Add userscript"))
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        lay = QVBoxLayout(self)
        label = QLabel(_t("Userscript URL (direct .js URL):"))
        lay.addWidget(label)
        self.edit = QLineEdit()
        self.edit.setMinimumWidth(440)
        self.edit.setPlaceholderText("https://")
        label.setBuddy(self.edit)
        lay.addWidget(self.edit)
        self.hint = ui.Caption(_t("URL must start with http:// or https://"), tone="warning")
        lay.addWidget(self.hint)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                                   | QDialogButtonBox.StandardButton.Cancel)
        self.ok = buttons.button(QDialogButtonBox.StandardButton.Ok)
        self.ok.setText(_t("Add"))
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(_t("Cancel"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)
        self.edit.textChanged.connect(self._check)
        self._check()

    def url(self) -> str:
        return self.edit.text().strip()

    def _check(self, *_args) -> None:
        url = self.url().lower()
        valid = url.startswith(_SCHEMES) and not url.endswith("://")
        self.ok.setEnabled(valid)
        # No warning while the scheme is still being typed.
        self.hint.setVisible(bool(url) and not valid and not any(s.startswith(url) for s in _SCHEMES))


class UserscriptsTab(ui.Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(wide=True, parent=parent)
        self.ctx = ctx
        self.cli = ctx.cli
        self._workers: list[QThread] = []
        self._script_map: dict[str, UserscriptEntry] = {}
        self._busy = False
        self._again = False

        self._build_ui()        # the shell's on_shown() does the first load

    def _build_ui(self) -> None:
        bar = QHBoxLayout()
        bar.setSpacing(8)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(_t("Search userscripts…"))
        self.search_box.setAccessibleName(_t("Search userscripts…").rstrip("…"))
        self.search_box.setClearButtonEnabled(True)
        self.search_box.setMaximumWidth(360)
        self.search_box.textChanged.connect(self._apply_search)
        bar.addWidget(self.search_box, 1)
        bar.addStretch()
        self.btn_add = QPushButton(_t("Add userscript…"))
        self.btn_add.setToolTip(_t("Install userscript from a direct .js URL"))
        self.btn_add.clicked.connect(self._install)
        bar.addWidget(self.btn_add)
        self.btn_remove = QPushButton(_t("Remove…"))
        self.btn_remove.setEnabled(False)
        self.btn_remove.clicked.connect(self._remove_current)
        bar.addWidget(self.btn_remove)
        self.body.addLayout(bar)

        status = QHBoxLayout()
        status.setSpacing(8)
        self.lbl_count = ui.Caption("")
        self.lbl_count.setWordWrap(False)
        status.addWidget(self.lbl_count)
        self.spinner = ui.Spinner()
        status.addWidget(self.spinner)
        status.addStretch(1)
        self.body.addLayout(status)

        self.tree = QTreeWidget()
        self.tree.setAccessibleName(_t("Userscripts"))
        ui.style_list(self.tree)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._on_context_menu)
        self.tree.itemSelectionChanged.connect(self._update_buttons)
        delete = QShortcut(QKeySequence(QKeySequence.StandardKey.Delete), self.tree, self._remove_current)
        delete.setContext(Qt.ShortcutContext.WidgetShortcut)
        self.empty = ui.EmptyState(self.tree)
        self.add(ui.list_card(self.tree), 1)

        foot = QHBoxLayout()
        foot.setSpacing(4)
        foot.addStretch(1)
        note = ui.Caption(_t("Userscripts update together with filters."))
        note.setWordWrap(False)
        foot.addWidget(note)
        foot.addWidget(ui.LinkButton(_t("Go to updates"), lambda: self.ctx.navigate(PAGE_ABOUT)))
        self.body.addLayout(foot)

    # ── Shell hooks ───────────────────────────────────────────────────────

    def refresh(self) -> None:
        if self._busy:
            self._again = True      # reloaded once the running action ends
        else:
            self._load()

    def on_shown(self) -> None:
        # The tray's submenu toggles userscripts too.
        self.refresh()

    def focus_search(self) -> None:
        self.search_box.setFocus()
        self.search_box.selectAll()

    # ── Loading ───────────────────────────────────────────────────────────

    def _start(self, w: QThread) -> None:
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _load(self) -> None:
        self._again = False
        self._set_busy(True)
        w = _LoadWorker(self.cli)
        w.done.connect(self._on_loaded)
        self._start(w)

    def _on_loaded(self, result: UserscriptListResult) -> None:
        self._set_busy(False)
        if self._again:             # the tray changed something while this ran
            self._load()
            return
        try:
            self.tree.itemChanged.disconnect(self._on_item_changed)
        except TypeError:
            pass
        self.tree.clear()
        self._script_map.clear()

        if result.error:
            self.lbl_count.setText("")
            self.empty.set("")
            self.banner.show_message(_t("Could not retrieve userscript list"), "danger",
                                     details=result.error)
            return

        active = sum(1 for s in result.scripts if s.enabled)
        self.lbl_count.setText(_t("{} of {} userscripts on", active, len(result.scripts))
                               if result.scripts else "")

        for s in result.scripts:
            self._script_map[s.name] = s
            item = QTreeWidgetItem(self.tree)
            item.setData(0, Qt.ItemDataRole.UserRole, s.name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(0, Qt.CheckState.Checked if s.enabled else Qt.CheckState.Unchecked)
            item.setText(0, s.title)
            updated = _t("Updated {}", s.last_update) if s.last_update else ""
            item.setData(0, ui.SUBTITLE_ROLE, " · ".join(x for x in (updated, s.name) if x))
            item.setToolTip(0, ui.plain_tip(f"{s.title} ({s.name})"))

        self._apply_search(self.search_box.text())
        self._update_buttons()
        self.tree.itemChanged.connect(self._on_item_changed)

    # ── Toggle ────────────────────────────────────────────────────────────

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        if column != 0:
            return
        name = item.data(0, Qt.ItemDataRole.UserRole)
        if not name:
            return
        enable = item.checkState(0) == Qt.CheckState.Checked
        self._set_busy(True)
        try:
            self.tree.itemChanged.disconnect(self._on_item_changed)
        except TypeError:
            pass
        w = _ToggleWorker(self.cli, name, enable)
        w.done.connect(self._on_toggle_done)
        self._start(w)

    def _on_toggle_done(self, ok: bool, msg: str, name: str, new_enabled: bool) -> None:
        self._set_busy(False)
        if ok:
            self.banner.show_message(self.ctx.restart_adguard(), "success", timeout_ms=5000)
            self._load()
            return
        for i in range(self.tree.topLevelItemCount()):
            child = self.tree.topLevelItem(i)
            if child.data(0, Qt.ItemDataRole.UserRole) == name:
                child.setCheckState(
                    0, Qt.CheckState.Checked if not new_enabled else Qt.CheckState.Unchecked
                )
                break
        self._fail(msg)
        self.tree.itemChanged.connect(self._on_item_changed)

    # ── Install ───────────────────────────────────────────────────────────

    def _install(self) -> None:
        if self._busy:
            return
        dlg = _UrlDialog(self)
        accepted = dlg.exec() == QDialog.DialogCode.Accepted
        url = dlg.url()
        dlg.deleteLater()
        if not accepted:
            return
        self._set_busy(True)
        self.banner.show_message(_t("Installing: {}", url), "info")
        w = _InstallWorker(self.cli, url)
        w.done.connect(self._on_install_done)
        self._start(w)

    def _on_install_done(self, ok: bool, msg: str) -> None:
        self._set_busy(False)
        if ok:
            self.banner.show_message(f"{_t('Userscript installed.')} {self.ctx.restart_adguard()}",
                                     "success", timeout_ms=5000)
            self._load()
        else:
            self._fail(msg)

    # ── Remove ────────────────────────────────────────────────────────────

    def _on_context_menu(self, pos) -> None:
        item = self.tree.itemAt(pos)
        if item is None or self._busy:
            return
        name = item.data(0, Qt.ItemDataRole.UserRole)
        if not name:
            return
        menu = QMenu(self)
        act = menu.addAction(_t('Remove "{}"', item.text(0)))
        act.triggered.connect(lambda: self._remove(name))
        menu.exec(self.tree.viewport().mapToGlobal(pos))

    def _remove_current(self) -> None:
        items = self.tree.selectedItems()
        if items and not self._busy and not items[0].isHidden():
            self._remove(items[0].data(0, Qt.ItemDataRole.UserRole))

    def _remove(self, name: str) -> None:
        s = self._script_map.get(name)
        display = s.title if s else name
        body = (_t("Remove “{}”?", display) + "\n\n"
                + _t("To keep it but stop using it, switch it off instead."))
        if not ui.confirm(self, _t("Remove userscript"), body, _t("Remove")):
            return
        self._set_busy(True)
        w = _RemoveWorker(self.cli, name)
        w.done.connect(self._on_remove_done)
        self._start(w)

    def _on_remove_done(self, ok: bool, msg: str, name: str) -> None:
        self._set_busy(False)
        if ok:
            s = self._script_map.get(name)
            removed = _t("'{}' removed.", s.title if s else name)
            self.banner.show_message(f"{removed} {self.ctx.restart_adguard()}", "success",
                                     timeout_ms=5000)
            self._load()
        else:
            self._fail(msg)

    # ── Helpers ───────────────────────────────────────────────────────────

    def _apply_search(self, text: str) -> None:
        needle = text.strip().lower()
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            name = str(item.data(0, Qt.ItemDataRole.UserRole) or "")
            item.setHidden(bool(needle) and needle not in item.text(0).lower()
                           and needle not in name.lower())
        count = self.tree.topLevelItemCount()
        shown = sum(not self.tree.topLevelItem(i).isHidden() for i in range(count))
        self.empty.set("" if shown else _t("Nothing matches your search.") if count
                       else _t("No userscripts installed."))
        self._update_buttons()

    def _update_buttons(self) -> None:
        items = self.tree.selectedItems()
        self.btn_remove.setEnabled(not self._busy and bool(items) and not items[0].isHidden())

    def _fail(self, msg: str) -> None:
        lines = msg.splitlines() or [""]
        self.banner.show_message(_t("Error: {}", lines[0]), "danger",
                                 details=msg if len(lines) > 1 else "")
        if self._again:
            self._load()

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        self.btn_add.setEnabled(not busy)
        self.tree.setEnabled(not busy)
        self.spinner.set_busy(busy)
        self._update_buttons()
