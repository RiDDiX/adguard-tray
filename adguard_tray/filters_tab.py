"""
Filters page – the ad blocking switch and AdGuard's filter lists.

The list part (toolbar, grouped list, row actions) is FilterList, which the
DNS page reuses for `adguard-cli dns filters`.
"""

import logging
import re

from PyQt6.QtCore import QEvent, QPoint, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from . import ui
from .cli import FilterEntry, FilterListResult
from .i18n import _t
from .proxy_settings import PROXY_YAML, add_switch, guard, unavailable_message
from .worker import safe_call, safe_result

logger = logging.getLogger(__name__)

_ID = Qt.ItemDataRole.UserRole
_URL_RE = re.compile(r"^https?://\S+$", re.IGNORECASE)


def _trust_risk() -> str:
    return _t("A trusted filter can run scripts in the pages you visit. "
              "Only trust lists from sources you know.")


def _ask(parent, title: str, label: str, text: str = "") -> str:
    """QInputDialog.getText with translated buttons; "" when cancelled."""
    dlg = QInputDialog(parent)
    dlg.setWindowTitle(title)
    dlg.setLabelText(label)
    dlg.setTextValue(text)
    dlg.setOkButtonText(_t("OK"))
    dlg.setCancelButtonText(_t("Cancel"))
    ok = dlg.exec() == QDialog.DialogCode.Accepted
    value = dlg.textValue().strip()
    dlg.deleteLater()
    return value if ok else ""


class _Worker(QThread):
    done = pyqtSignal(object)

    def __init__(self, fn) -> None:
        super().__init__()
        self._fn = fn

    def run(self) -> None:
        # fn is always wrapped in safe_call/safe_result: an exception leaving
        # QThread.run() aborts the process.
        self.done.emit(self._fn())


class _Banner(ui.Banner):
    """The list's own banner, right above its toolbar. `anchor` wraps every
    show and hide so the rows below don't move."""

    anchor = None

    def setVisible(self, visible: bool) -> None:
        if self.anchor is None or visible != self.isHidden():
            super().setVisible(visible)
        else:
            self.anchor(lambda: super(_Banner, self).setVisible(visible))


# ── The list ─────────────────────────────────────────────────────────────────

class FilterList(QWidget):
    """Search, Show, Add, More, the grouped list with a switch per filter,
    and the row actions. dns=True drives `adguard-cli dns filters`.

    fit=True sizes the list to its rows for pages that scroll as a whole.
    Such a list sits far down its page, so it reports to its own banner
    above the toolbar; otherwise it uses the page's banner.
    """

    def __init__(self, page, ctx, dns: bool = False, fit: bool = False) -> None:
        super().__init__()
        self.page, self.ctx, self.dns, self._fit = page, ctx, dns, fit
        self._workers: list[QThread] = []
        self._map: dict[int, FilterEntry] = {}
        self._busy = False
        self._again = False         # a reload asked for while busy
        self._empty = ""            # what an empty list says, once loaded
        self._held = 0              # scroll added to keep rows still under a banner
        self._content_y = 0
        cli = ctx.cli
        if dns:
            self._fn_load, self._fn_enable, self._fn_disable = (
                cli.get_dns_filters, cli.enable_dns_filter, cli.disable_dns_filter)
            self._fn_add, self._fn_remove, self._fn_rename = (
                cli.add_dns_filter, cli.remove_dns_filter, cli.set_dns_filter_title)
            self.txt = dict(
                name=_t("DNS filter lists"),
                search=_t("Search DNS filters…"),
                count=_t("{} of {} DNS filters on"), empty=_t("No DNS filters found."),
                load_error=_t("Could not retrieve DNS filter list"),
                url_title=_t("Add DNS filter from URL"), id_title=_t("Add DNS filter by ID"),
                rename_title=_t("Rename DNS filter"), remove_title=_t("Remove DNS filter"),
                installed=_t("DNS filter installed."), added=_t("DNS filter added."),
                renamed=_t("DNS filter renamed."), removed=_t("DNS filter {} removed."),
                enable_error=_t("Could not enable DNS filter {}"),
                disable_error=_t("Could not disable DNS filter {}"),
                add_error=_t("Could not add DNS filter"),
                remove_error=_t("Could not remove DNS filter {}"),
                rename_error=_t("Could not set DNS filter title"),
            )
        else:
            self._fn_load, self._fn_enable, self._fn_disable = (
                cli.get_filters, cli.enable_filter, cli.disable_filter)
            self._fn_add, self._fn_remove, self._fn_rename = (
                cli.add_filter, cli.remove_filter, cli.set_filter_title)
            self.txt = dict(
                name=_t("Filters"),
                search=_t("Search filters…"),
                count=_t("{} of {} filters on"), empty=_t("No filters found."),
                load_error=_t("Could not retrieve filter list"),
                url_title=_t("Add filter from URL"), id_title=_t("Add filter by ID"),
                rename_title=_t("Rename filter"), remove_title=_t("Remove filter"),
                installed=_t("Filter installed."), added=_t("Filter added."),
                renamed=_t("Filter renamed."), removed=_t("Filter {} removed."),
                enable_error=_t("Could not enable filter {}"),
                disable_error=_t("Could not disable filter {}"),
                add_error=_t("Could not add filter"),
                remove_error=_t("Could not remove filter {}"),
                rename_error=_t("Could not set filter title"),
            )
        self._build()

    def _build(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)
        if self._fit:
            self.banner = _Banner()
            lay.addWidget(self.banner)
        else:
            self.banner = self.page.banner
            self.page.content.installEventFilter(self)

        bar = QHBoxLayout()
        bar.setSpacing(6)
        self.search = QLineEdit()
        self.search.setMinimumWidth(120)
        self.search.setPlaceholderText(self.txt["search"])
        self.search.setAccessibleName(self.txt["search"])
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(self._apply_search)
        bar.addWidget(self.search, 1)
        bar.addSpacing(6)
        show = QLabel(_t("Show"))
        bar.addWidget(show)
        self.scope = QComboBox()
        self.scope.addItem(_t("Installed"), False)
        self.scope.addItem(_t("All available"), True)
        show.setBuddy(self.scope)
        self.scope.currentIndexChanged.connect(self.load)
        bar.addWidget(self.scope)

        add_menu = QMenu(self)
        add_menu.addAction(_t("From URL…")).triggered.connect(self._add_url)
        add_menu.addAction(_t("By ID or name…")).triggered.connect(self._add_id)
        self.btn_add = self._menu_button(_t("Add filter"), add_menu)
        bar.addWidget(self.btn_add)

        self.menu = QMenu(self)
        self.act_rename = self.menu.addAction(_t("Rename…"))
        self.act_rename.triggered.connect(self._rename)
        self.act_trust = self.act_untrust = None
        if not self.dns:
            self.act_trust = self.menu.addAction(_t("Trust…"))
            self.act_trust.triggered.connect(lambda: self._set_trusted(True))
            self.act_untrust = self.menu.addAction(_t("Don't trust"))
            self.act_untrust.triggered.connect(lambda: self._set_trusted(False))
        self.menu.addSeparator()
        self.act_remove = self.menu.addAction(_t("Remove…"))
        self.act_remove.triggered.connect(self._remove)
        self.btn_more = self._menu_button(_t("More"), self.menu)
        self.btn_more.setToolTip(_t("Actions for the selected filter"))
        bar.addWidget(self.btn_more)
        self.spinner = ui.Spinner()
        bar.addWidget(self.spinner)
        lay.addLayout(bar)

        # The page places it: it updates more than this list.
        self.btn_update = None
        if not self.dns:
            self.btn_update = QPushButton(_t("Update"))
            self.btn_update.clicked.connect(self._run_update)

        self.caption = ui.Caption("")
        self.caption.setWordWrap(False)
        # Same height while it is still empty, or the rows hop after loading.
        self.caption.setMinimumHeight(self.caption.fontMetrics().height())
        lay.addWidget(self.caption)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        ui.style_list(self.tree)
        self.tree.setAccessibleName(self.txt["name"])
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._context_menu)
        self.tree.itemChanged.connect(self._on_item_changed)
        self.tree.currentItemChanged.connect(self._update_actions)
        self.tree.viewport().installEventFilter(self)
        self.tree.installEventFilter(self)
        self.act_remove.setShortcut(QKeySequence(QKeySequence.StandardKey.Delete))
        self.act_remove.setShortcutContext(Qt.ShortcutContext.WidgetShortcut)
        self.tree.addAction(self.act_remove)
        if self._fit:
            self.tree.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.tree.currentItemChanged.connect(self._reveal)
        lay.addWidget(ui.list_card(self.tree), 1)
        self.empty = ui.EmptyState(self.tree)
        if self._fit:
            self.banner.anchor = self._keep_rows_still
        self._update_actions()

    @staticmethod
    def _menu_button(text: str, menu: QMenu) -> QPushButton:
        # A QPushButton with a menu: same height and arrow as the buttons
        # beside it, where Fusion squeezes a QToolButton's arrow into its text.
        btn = QPushButton(text)
        btn.setMenu(menu)
        return btn

    def focus_search(self) -> None:
        self.search.setFocus(Qt.FocusReason.ShortcutFocusReason)
        self.search.selectAll()

    # ── Loading ────────────────────────────────────────────────────────────

    def load(self) -> None:
        if self._busy:
            # The tray may have just toggled a filter: read the list again
            # once the running action is done.
            self._again = True
            return
        self._again = False
        self._set_busy(True)
        fn, all_available = self._fn_load, bool(self.scope.currentData())
        self._start(lambda: safe_result(fn, FilterListResult, all_available=all_available),
                    self._on_loaded)

    def _on_loaded(self, result: FilterListResult) -> None:
        self._set_busy(False)
        scroll = self.tree.verticalScrollBar().value()
        current = self.tree.currentItem()
        current_id = current.data(0, _ID) if current is not None else None
        self.tree.blockSignals(True)
        self.tree.clear()
        self._map.clear()
        if result.error:
            self.tree.blockSignals(False)
            self.caption.setText("")
            self._empty = ""
            self._fail(self.txt["load_error"], result.error)
            self._apply_search(self.search.text())
            if self._again:
                self.load()
            return

        restore = None
        for group_name, filters in result.groups.items():
            group = QTreeWidgetItem(self.tree, [_t(group_name)])
            group.setFlags(Qt.ItemFlag.ItemIsEnabled)
            for f in filters:
                self._map[f.id] = f
                item = QTreeWidgetItem(group, [f.title])
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
                              | Qt.ItemFlag.ItemIsUserCheckable)
                item.setData(0, _ID, f.id)
                item.setCheckState(0, Qt.CheckState.Checked if f.enabled else Qt.CheckState.Unchecked)
                item.setData(0, ui.SUBTITLE_ROLE, self._subtitle(f))
                item.setToolTip(0, ui.plain_tip(f.title))
                if f.is_custom:
                    item.setData(0, ui.BADGE_ROLE, (_t("Custom"), "info"))
                if f.id == current_id:
                    restore = item
        self.tree.expandAll()
        self._empty = self.txt["empty"]
        self._apply_search(self.search.text())
        if restore is not None:
            self.tree.setCurrentItem(restore)
        self.tree.blockSignals(False)

        if self.banner.text.text() == self.txt["load_error"]:
            self.banner.hide()
        filters = result.all_filters
        self.caption.setText(
            self.txt["count"].format(sum(1 for f in filters if f.enabled), len(filters))
            if filters else "")
        self._update_actions()
        # A toggle reloads the list; it must not jump back to the top.
        self.tree.doItemsLayout()
        self.tree.verticalScrollBar().setValue(scroll)
        if self._again:
            self.load()

    @staticmethod
    def _subtitle(f: FilterEntry) -> str:
        if not f.is_added:
            return _t("Not added")
        parts = []
        if f.last_update:
            parts.append(_t("Updated {}", f.last_update[:16]))
        if not f.is_custom:     # custom lists get internal negative IDs
            parts.append(_t("ID {}", f.id))
        return " · ".join(parts)

    def _apply_search(self, text: str) -> None:
        needle = text.strip().lower()
        height = rows = visible = 0
        for i in range(self.tree.topLevelItemCount()):
            group = self.tree.topLevelItem(i)
            shown = 0
            for j in range(group.childCount()):
                child = group.child(j)
                match = not needle or needle in child.text(0).lower()
                child.setHidden(not match)
                if match:
                    shown += 1
                    height += self._row_height(child)
            rows += group.childCount()
            visible += shown
            group.setHidden(not shown)
            if shown:
                height += self._row_height(group)
        self.empty.set(self._empty if not rows else
                       "" if visible else _t("Nothing matches your search."))
        if self._fit:
            self.tree.setFixedHeight(max(height, 44) + 2 * self.tree.frameWidth())
        self._update_actions()

    def _row_height(self, item: QTreeWidgetItem) -> int:
        return self.tree.sizeHintForIndex(self.tree.indexFromItem(item)).height()

    def _reveal(self, item, _previous=None) -> None:
        # A fitted list has no scroll range of its own: follow the arrow keys
        # with the page. Not on a click, the release would land on another row.
        if item is None or item.isHidden() or QApplication.mouseButtons() != Qt.MouseButton.NoButton:
            return
        rect = self.tree.visualItemRect(item)
        centre = self.tree.viewport().mapTo(self.page.widget(), rect.center())
        self.page.ensureVisible(centre.x(), centre.y(), 0, rect.height() // 2 + 8)

    # ── Toggle ─────────────────────────────────────────────────────────────

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        fid = item.data(0, _ID)
        if column != 0 or fid is None:
            return
        entry = self._map.get(fid)
        if entry is None:
            # Tree and map out of sync (late reload) – reload instead of
            # acting on a filter we no longer know.
            self.load()
            return
        enable = item.checkState(0) == Qt.CheckState.Checked
        if self._busy:
            self._set_check(fid, not enable)
            return
        if enable and not entry.is_added:
            # The CLI rejects `enable` for a filter that isn't added yet.
            fn, arg = self._fn_add, str(fid)
        else:
            fn, arg = (self._fn_enable if enable else self._fn_disable), fid
        error = (self.txt["enable_error"] if enable else self.txt["disable_error"]).format(entry.title)
        self._act(fn, arg, done="", error=error,
                  on_fail=lambda: self._set_check(fid, not enable))

    def _set_check(self, fid: int, on: bool) -> None:
        for i in range(self.tree.topLevelItemCount()):
            group = self.tree.topLevelItem(i)
            for j in range(group.childCount()):
                child = group.child(j)
                if child.data(0, _ID) == fid:
                    self.tree.blockSignals(True)
                    child.setCheckState(0, Qt.CheckState.Checked if on else Qt.CheckState.Unchecked)
                    self.tree.blockSignals(False)
                    return

    # ── Adding ─────────────────────────────────────────────────────────────

    def _add_url(self) -> None:
        if self._busy:
            return
        dlg = _UrlDialog(self, self.txt["url_title"],
                         "https://example.com/hosts.txt" if self.dns else "https://example.com/filter.txt",
                         trusted_option=not self.dns)
        accepted = dlg.exec() == QDialog.DialogCode.Accepted
        url, title, trusted = dlg.url(), dlg.title(), dlg.trusted()
        dlg.deleteLater()
        if not accepted:
            return
        if self.dns:
            self._act(self.ctx.cli.install_dns_filter, url, title,
                      done=self.txt["installed"], error=_t("Installation failed"))
        else:
            self._act(self.ctx.cli.install_filter_ext, url, trusted, title,
                      done=self.txt["installed"], error=_t("Installation failed"))

    def _add_id(self) -> None:
        if self._busy:
            return
        text = _ask(self, self.txt["id_title"], _t("Enter filter ID or name:"))
        if text:
            self._act(self._fn_add, text, done=self.txt["added"], error=self.txt["add_error"])

    # ── Row actions ────────────────────────────────────────────────────────

    def _selected(self) -> FilterEntry | None:
        item = self.tree.currentItem()
        if item is None or item.isHidden():
            return None
        return self._map.get(item.data(0, _ID))

    def _update_actions(self, *_args) -> None:
        f = self._selected()
        custom = f is not None and f.is_custom
        # Built-in filters can't be renamed, trusted or removed through the
        # CLI; built-in DNS filters can at least be taken off the list.
        removable = custom or (self.dns and f is not None and f.is_added)
        self.act_rename.setEnabled(custom)
        for act in (self.act_trust, self.act_untrust):
            if act is not None:
                act.setEnabled(custom)
        self.act_remove.setEnabled(removable)
        self.btn_more.setEnabled(removable and not self._busy)

    def _context_menu(self, pos) -> None:
        item = self.tree.itemAt(pos)
        if item is None or self._busy:
            return
        self.tree.setCurrentItem(item)
        if self.btn_more.isEnabled():
            self.menu.exec(self.tree.viewport().mapToGlobal(pos))

    def _rename(self) -> None:
        f = self._selected()
        if f is None or not f.is_custom or self._busy:
            return
        name = _ask(self, self.txt["rename_title"], _t("New title:"), f.title)
        if name and name != f.title:
            self._act(self._fn_rename, f.id, name, done=self.txt["renamed"],
                      error=self.txt["rename_error"])

    def _set_trusted(self, trusted: bool) -> None:
        f = self._selected()
        if f is None or not f.is_custom or self._busy:
            return
        # Only granting trust is risky; taking it back needs no question.
        if trusted and not ui.confirm(self, _t("Trusted filter"),
                                      _t("Trust “{}”?", f.title) + "\n\n" + _trust_risk(),
                                      _t("Trust")):
            return
        self._act(self.ctx.cli.set_filter_trusted, f.id, trusted,
                  done=_t("Filter trust updated."), error=_t("Could not update filter trust"))

    def _remove(self) -> None:
        f = self._selected()
        if f is None or not self.act_remove.isEnabled() or self._busy:
            return
        if not ui.confirm(self, self.txt["remove_title"],
                          _t("Remove “{}”?", f.title) + "\n\n"
                          + _t("To keep it but stop using it, switch it off instead."),
                          _t("Remove")):
            return
        name = f"“{f.title}”"
        self._act(self._fn_remove, f.id, done=self.txt["removed"].format(name),
                  error=self.txt["remove_error"].format(name))

    # ── Update ─────────────────────────────────────────────────────────────

    def _run_update(self) -> None:
        if self._busy:
            return
        self._set_busy(True)
        self._say(_t("Updating filters… (can take up to 2 minutes)"), "info")
        cli = self.ctx.cli
        self._start(lambda: safe_call(cli.update_filters), self._on_updated)

    def _on_updated(self, result) -> None:
        ok, msg = result
        self._set_busy(False)
        if ok:
            # Stays until closed: the output behind Details is worth reading.
            self._say(f"{_t('Update completed.')} {self.ctx.restart_adguard()}", "success", details=msg)
        else:
            self._fail(_t("Update failed."), msg)
        self.load()

    # ── Plumbing ───────────────────────────────────────────────────────────

    def _act(self, fn, *args, done: str, error: str, on_fail=None) -> None:
        """Run a CLI change; on success restart AdGuard and reload the list."""
        self._set_busy(True)
        self._start(lambda: safe_call(fn, *args),
                    lambda result: self._on_acted(result, done, error, on_fail))

    def _on_acted(self, result, done: str, error: str, on_fail) -> None:
        ok, msg = result
        self._set_busy(False)
        if not ok:
            if on_fail:
                on_fail()
            self._fail(error, msg)
            if self._again:
                self.load()
            return
        restart = self.ctx.restart_adguard()
        self._say(f"{done} {restart}".strip(), "success", timeout_ms=5000)
        # Reload so is_added / last-updated reflect the CLI's view.
        self.load()

    def _fail(self, text: str, details: str) -> None:
        self._say(text, "danger", details=details if details != text else "")

    def _say(self, text: str, tone: str, details: str = "", timeout_ms: int = 0) -> None:
        self.banner.show_message(text, tone, details=details, timeout_ms=timeout_ms)
        if self._fit and tone != "success":
            # Scrolled down to the list, the page may hide the banner above it.
            self.page.ensureWidgetVisible(self.banner, 0, 8)

    def _keep_rows_still(self, change) -> None:
        """Show or hide the fitted list's banner without moving the rows under
        the pointer: scroll the page by whatever it adds or takes above them."""
        if not self.isVisible():
            change()
            # Nobody saw the rows move: only take back what we scrolled.
            if self.banner.isHidden():
                bar = self.page.verticalScrollBar()
                bar.setValue(bar.value() - self._held)
                self._held = 0
            return
        view, bar = self.page.viewport(), self.page.verticalScrollBar()
        before = self.tree.viewport().mapTo(view, QPoint()).y()
        change()
        QApplication.sendPostedEvents(None, QEvent.Type.LayoutRequest)
        # Rows below the fold: hold the page still instead.
        if before < view.height():
            dy = self.tree.viewport().mapTo(view, QPoint()).y() - before
            bar.setValue(bar.value() + dy)
            self._held = max(0, self._held + dy)

    def _hold_rows(self, y: int, old: int) -> None:
        """The page's banner came or went and moved the list: scroll the rows
        the other way so the one under the pointer stays put."""
        last, self._content_y = self._content_y, y
        dy = y - old
        if not dy:
            # Moved while the page was hidden (Qt then reports old == new).
            # Nobody saw the rows move: only take back what we scrolled.
            dy = max(y - last, -self._held) if y < last else 0
            if not dy:
                return
        self._held = max(0, self._held + dy)
        bar = self.tree.verticalScrollBar()
        if dy > 0:
            # The view shrinks right after this move; make room for it now.
            bar.setMaximum(bar.maximum() + dy)
        bar.setValue(bar.value() + dy)

    def _start(self, fn, callback) -> None:
        w = _Worker(fn)
        w.done.connect(callback)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _set_busy(self, busy: bool) -> None:
        # The list stays enabled (no grey flash, focus and scroll stay put);
        # eventFilter swallows clicks and Space on it meanwhile.
        self._busy = busy
        for widget in (self.scope, self.btn_add, self.btn_update):
            if widget is not None:
                widget.setEnabled(not busy)
        self.spinner.set_busy(busy)
        self._update_actions()

    def eventFilter(self, obj, event) -> bool:
        if obj is self.page.content:
            if event.type() == QEvent.Type.Move:
                self._hold_rows(event.pos().y(), event.oldPos().y())
            return False
        if self._busy:
            kind = event.type()
            if kind in (QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonRelease,
                        QEvent.Type.MouseButtonDblClick):
                return True
            if kind == QEvent.Type.KeyPress and event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Select):
                return True
        return super().eventFilter(obj, event)


# ── Add from URL ─────────────────────────────────────────────────────────────

class _UrlDialog(QDialog):
    """URL, optional title and (for content filters) trust. OK stays disabled
    until the URL is usable, so a typo never costs what was typed."""

    def __init__(self, parent, title: str, placeholder: str, trusted_option: bool) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(480)
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self._url = QLineEdit()
        self._url.setPlaceholderText(placeholder)
        self._error = ui.Caption(_t("URL must start with http:// or https://"), tone="danger")
        self._error.hide()
        url_box = QVBoxLayout()
        url_box.setSpacing(2)
        url_box.addWidget(self._url)
        url_box.addWidget(self._error)
        form.addRow(_t("Filter URL:"), url_box)
        self._title = QLineEdit()
        self._title.setPlaceholderText(_t("(optional)"))
        form.addRow(_t("Title:"), self._title)
        layout.addLayout(form)

        self._trusted = None
        if trusted_option:
            self._trusted = ui.Switch()
            card = ui.Card()
            card.add_row(ui.Row(_t("Trusted filter"), _trust_risk(), self._trusted))
            layout.addSpacing(4)
            layout.addWidget(card)

        self._buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self._buttons.button(QDialogButtonBox.StandardButton.Ok).setText(_t("OK"))
        self._buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(_t("Cancel"))
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        layout.addStretch(1)
        layout.addSpacing(6)
        layout.addWidget(self._buttons)
        self._url.textChanged.connect(self._check)
        self._check("")

    def _valid(self) -> bool:
        return bool(_URL_RE.match(self.url()))

    def _check(self, _text: str) -> None:
        text = self.url().lower()
        typing_scheme = "http://".startswith(text) or "https://".startswith(text)
        self._error.setVisible(bool(text) and not self._valid() and not typing_scheme)
        self._buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(self._valid())

    def accept(self) -> None:
        if self._valid():
            super().accept()

    def url(self) -> str:
        return self._url.text().strip()

    def title(self) -> str:
        return self._title.text().strip()

    def trusted(self) -> bool:
        return self._trusted is not None and self._trusted.isChecked()


# ── Page ─────────────────────────────────────────────────────────────────────

class FiltersTab(ui.Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(wide=True, parent=parent)
        top = self.section()
        self._ad = add_switch(top, ctx.settings, ("ad_blocking_enabled",), True, _t("Ad blocking"))
        self._ad.switch.toggled.connect(self._ad_hint)
        self._ad_hint(self._ad.switch.isChecked())
        self._settings = ctx.settings
        guard(self, ctx.settings, self._ad)     # the lists work without proxy.yaml
        self.banner.installEventFilter(self)

        self.body.addSpacing(10)
        self.lists = FilterList(self, ctx)
        top.add_row(ui.Row(_t("Update filters"), ui.one_line(_t(
            "Updates all filters, DNS filters, userscripts,\n"
            "SafebrowsingV2, CRLite and checks for app updates.")), self.lists.btn_update))
        self.add(self.lists, 1)
        self._workers = self.lists._workers
        self.lists.load()

    def _ad_hint(self, on: bool) -> None:
        self._ad.subtitle.set_tone("secondary" if on else "warning")
        self._ad.set_subtitle(
            ui.one_line(_t("Apply ad-blocking filter rules to HTTP/HTTPS requests.")) if on
            else _t("Ad blocking is off, so the filter lists below have no effect."))

    def eventFilter(self, obj, event) -> bool:
        if event.type() == QEvent.Type.HideToParent and isinstance(obj, ui.Banner):
            # The list shares this banner. When one of its messages goes while
            # proxy.yaml is unusable, say again why Ad blocking is greyed out.
            s = self._settings
            if not s.available and self.banner.text.text() not in (
                    unavailable_message(True), unavailable_message(False)):
                self.banner.show_message(unavailable_message(PROXY_YAML.exists()),
                                         "warning" if s.error == "missing" else "danger")
        return super().eventFilter(obj, event)

    def refresh(self) -> None:
        self.lists.load()

    def on_shown(self) -> None:
        # The tray's Filters submenu toggles filters too.
        self.lists.load()

    def focus_search(self) -> None:
        self.lists.focus_search()
