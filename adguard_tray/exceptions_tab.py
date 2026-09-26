"""Exceptions – what AdGuard leaves alone.

Websites are allowlist rules in user.txt and apply at once. App rules are
proxy.yaml's `apps` list and go through the window's Apply bar.
"""

import copy
import logging
from urllib.parse import urlsplit

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QPalette, QShortcut
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QMenu,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)

from . import theme, ui
from ._allowlist import is_valid_domain, load_user_rules, save_user_rules
from .i18n import _t
from .proxy_settings import guard

logger = logging.getLogger(__name__)

APPS = ("apps",)
_INDEX = Qt.ItemDataRole.UserRole


def _delete_key(widget: QWidget, callback) -> None:
    shortcut = QShortcut(QKeySequence(QKeySequence.StandardKey.Delete), widget, callback)
    shortcut.setContext(Qt.ShortcutContext.WidgetShortcut)


class ExceptionsTab(ui.Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(parent=parent)
        self.ctx = ctx
        self._other_lines: list[str] | None = []
        self._loaded_domains: list[str] = []
        self._load_failed = False
        self._filling = False
        self._writing = False
        self._apps_stale = False

        self._build_websites()
        self._build_apps()
        self.finish()
        self._load()

    # ── Websites ──────────────────────────────────────────────────────────

    def _build_websites(self) -> None:
        self.add(ui.heading(_t("Websites")))
        self.add(ui.Caption(_t("AdGuard doesn't filter these websites.")))
        self.body.addSpacing(4)

        add_row = QHBoxLayout()
        self.input_domain = QLineEdit()
        self.input_domain.setPlaceholderText(_t("example.com or a link"))
        self.input_domain.setAccessibleName(_t("Add website"))
        self.input_domain.setClearButtonEnabled(True)
        self.input_domain.returnPressed.connect(self._add)
        add_row.addWidget(self.input_domain, 1)
        self.btn_add = QPushButton(_t("Add"))
        self.btn_add.clicked.connect(self._add)
        add_row.addWidget(self.btn_add)
        self.body.addLayout(add_row)

        tools = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(_t("Search exceptions…"))
        self.search_box.setAccessibleName(_t("Search exceptions…").rstrip("…"))
        self.search_box.setClearButtonEnabled(True)
        self.search_box.setMaximumWidth(320)
        self.search_box.textChanged.connect(self._apply_filter)
        tools.addWidget(self.search_box, 1)
        tools.addStretch()
        self.btn_remove = QPushButton(_t("Remove"))
        self.btn_remove.setEnabled(False)
        self.btn_remove.clicked.connect(self._remove_selected)
        tools.addWidget(self.btn_remove)
        self.body.addLayout(tools)

        self.lbl_count = ui.Caption("")
        self.add(self.lbl_count)

        self.domain_list = QTreeWidget()
        self.domain_list.setAccessibleName(_t("Websites"))
        ui.style_list(self.domain_list, headings=False)
        self.domain_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.domain_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.domain_list.itemSelectionChanged.connect(self._update_remove)
        self.domain_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.domain_list.customContextMenuRequested.connect(self._on_context_menu)
        _delete_key(self.domain_list, self._remove_selected)
        self.empty = ui.EmptyState(self.domain_list)
        self.add(ui.list_card(self.domain_list))

    def on_shown(self) -> None:
        # Activity's "Allow" and the tray write user.txt as well.
        self._load()

    def refresh(self) -> None:
        self._load()

    def focus_search(self) -> None:
        self.search_box.setFocus()
        self.search_box.selectAll()

    def _load(self) -> None:
        try:
            domains, self._other_lines = load_user_rules()
        except (OSError, ValueError) as exc:  # ValueError: not UTF-8
            self._other_lines = None  # never save over a file we couldn't read
            logger.error("Failed to read user rules: %s", exc)
            self._load_failed = True
            self.banner.show_message(_t("Error: {}", exc), "danger")
            self._set_websites_enabled(False)
            return
        if self._load_failed:
            self._load_failed = False
            self.banner.hide()
        self._set_websites_enabled(True)
        self._loaded_domains = list(domains)
        current = self.domain_list.currentItem()
        keep = current.text(0) if current is not None and current.isSelected() else None
        self.domain_list.clear()
        for d in sorted(set(domains)):
            item = QTreeWidgetItem(self.domain_list, [d])
            if d == keep:
                self.domain_list.setCurrentItem(item)
        self._apply_filter(self.search_box.text())

    def _set_websites_enabled(self, on: bool) -> None:
        for widget in (self.input_domain, self.btn_add, self.search_box, self.domain_list):
            widget.setEnabled(on)
        self._update_remove()

    def _add(self) -> None:
        raw = self.input_domain.text().strip()
        if not raw or self._other_lines is None:
            return
        # A pasted link counts as its host.
        try:
            host = urlsplit(raw if "://" in raw else "//" + raw).hostname or ""
        except ValueError:
            host = ""
        host = host.rstrip(".")
        # "www.test.de" is saved as "test.de", which covers www. and the site's
        # other subdomains – what people mean when they allow a website.
        if host.startswith("www.") and "." in host[4:] and not _public_suffix(host[4:]):
            host = host[4:]
        if not is_valid_domain(host):
            self.banner.show_message(_t("'{}' is not a valid domain or IP address.", host or raw),
                                     "warning")
            return
        if host in self._loaded_domains:
            self.banner.show_message(_t("'{}' is already in the list.", host), "info",
                                     timeout_ms=5000)
            self.input_domain.clear()
            return
        if self._save(self._loaded_domains + [host]):
            self.input_domain.clear()
            self._select(host)

    def _remove_selected(self) -> None:
        items = [i for i in self.domain_list.selectedItems() if not i.isHidden()]
        if not items or self._other_lines is None:
            return
        gone = {i.text(0) for i in items}
        self._save([d for d in self._loaded_domains if d not in gone],
                   undo=lambda: self._save(sorted(set(self._loaded_domains) | gone)))

    def _save(self, domains: list[str], undo=None) -> bool:
        if self._other_lines is None:
            return False
        ok, err = save_user_rules(domains, self._other_lines, self._loaded_domains)
        if not ok:
            self.banner.show_message(_t("Could not save exceptions:\n{}", err), "danger")
            return False
        self._load()      # shows what is on disk now, including entries added elsewhere
        self.banner.show_message(self.ctx.restart_adguard(), "success",
                                 action=_t("Undo") if undo else "", callback=undo,
                                 timeout_ms=8000 if undo else 5000)
        return True

    def _select(self, domain: str) -> None:
        for i in range(self.domain_list.topLevelItemCount()):
            item = self.domain_list.topLevelItem(i)
            if item.text(0) == domain and not item.isHidden():
                self.domain_list.setCurrentItem(item)

    def _on_context_menu(self, pos) -> None:
        item = self.domain_list.itemAt(pos)
        if item is None or self._other_lines is None:
            return
        self.domain_list.setCurrentItem(item)
        menu = QMenu(self)
        menu.addAction(_t('Remove "{}"', item.text(0)), self._remove_selected)
        menu.exec(self.domain_list.viewport().mapToGlobal(pos))

    def _apply_filter(self, text: str) -> None:
        needle = text.strip().lower()
        shown = 0
        for i in range(self.domain_list.topLevelItemCount()):
            item = self.domain_list.topLevelItem(i)
            item.setHidden(bool(needle) and needle not in item.text(0).lower())
            shown += not item.isHidden()
        count = self.domain_list.topLevelItemCount()
        self.lbl_count.setText(_t("1 exception") if count == 1 else _t("{} exceptions", count))
        self.lbl_count.setVisible(count > 0)
        self.empty.set("" if shown else _t("Nothing matches your search.") if count
                       else _t("No exceptions."))
        # The page scrolls, so the list shows every row instead of scrolling itself.
        rows = sum(self.domain_list.sizeHintForRow(i) for i in range(count)
                   if not self.domain_list.topLevelItem(i).isHidden())
        self.domain_list.setFixedHeight(max(rows, 44) + 2 * self.domain_list.frameWidth() + 2)
        self._update_remove()

    def _update_remove(self) -> None:
        items = self.domain_list.selectedItems()
        self.btn_remove.setEnabled(self._other_lines is not None and bool(items)
                                   and not items[0].isHidden())

    # ── Apps ──────────────────────────────────────────────────────────────

    def _build_apps(self) -> None:
        self.body.addSpacing(16)
        self.add(ui.heading(_t("Apps")))
        self.add(ui.Caption(_t(
            "Rules apply only in automatic proxy mode. The first matching rule wins, "
            "so keep \"*\" last.")))
        self.body.addSpacing(4)

        # Row actions sit above the list, as on every list page.
        self.apps_tools = QWidget()
        tools = QHBoxLayout(self.apps_tools)
        tools.setContentsMargins(0, 0, 0, 0)
        tools.addStretch()
        self.btn_app_add = QPushButton(_t("Add rule"))
        self.btn_app_add.clicked.connect(self._add_app)
        self.btn_app_remove = QPushButton(_t("Remove rule"))
        self.btn_app_remove.clicked.connect(self._remove_app)
        self.btn_app_up = QPushButton(_t("Move up"))
        self.btn_app_up.clicked.connect(lambda: self._move_app(-1))
        self.btn_app_down = QPushButton(_t("Move down"))
        self.btn_app_down.clicked.connect(lambda: self._move_app(1))
        for button in (self.btn_app_add, self.btn_app_remove, self.btn_app_up, self.btn_app_down):
            tools.addWidget(button)
        self.add(self.apps_tools)

        card = self.apps_card = ui.Card(padding=4)
        self.add(card)

        t = self.app_table = QTableWidget(0, 3)
        t.setAccessibleName(_t("Apps"))
        t.setHorizontalHeaderLabels([_t("App pattern"), _t("Filtering"), _t("Skip outbound proxy")])
        t.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        t.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        t.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        t.horizontalHeader().setHighlightSections(False)
        t.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft
                                                 | Qt.AlignmentFlag.AlignVCenter)
        t.verticalHeader().hide()
        t.verticalHeader().setDefaultSectionSize(max(QComboBox().sizeHint().height() + 10, 40))
        ui.style_table(t)
        t.setShowGrid(False)
        t.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        t.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        t.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked
                          | QAbstractItemView.EditTrigger.EditKeyPressed
                          | QAbstractItemView.EditTrigger.AnyKeyPressed)
        t.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        t.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        t.itemChanged.connect(self._on_app_item_changed)
        t.itemSelectionChanged.connect(self._update_app_buttons)
        # A rebuild waits while a pattern is being typed, and runs once it is committed.
        t.itemDelegate().closeEditor.connect(self._on_editor_closed)
        _delete_key(t, self._remove_app)
        theme.watcher().changed.connect(self._restyle_table)
        self._restyle_table()
        card.add(t)

        s = self.ctx.settings
        s.changed.connect(self._on_settings_changed)
        # Websites don't need proxy.yaml: only the apps part waits for it.
        guard(self, s, self.apps_tools, self.apps_card)
        s.reloaded.connect(self._fill_apps)
        self._fill_apps()

    def _restyle_table(self) -> None:
        # The lists' soft selection instead of the accent: a switch that is on
        # would vanish in an accent-filled row.
        tok = theme.tokens()
        pal = self.app_table.palette()
        for group in (QPalette.ColorGroup.Active, QPalette.ColorGroup.Inactive):
            pal.setColor(group, QPalette.ColorRole.Highlight, tok.selected)
            pal.setColor(group, QPalette.ColorRole.HighlightedText, tok.text)
        self.app_table.setPalette(pal)

    def _on_settings_changed(self, key: tuple) -> None:
        if key == APPS and not self._writing:
            self._fill_apps()

    def _on_editor_closed(self, *_args) -> None:
        if self._apps_stale:
            self._fill_apps()

    def _apps(self) -> list:
        # A copy: the list the model hands out is its own loaded data.
        return copy.deepcopy(self.ctx.settings.value(APPS, []))

    def _write_apps(self, apps: list, select: int | None = None) -> None:
        """Hand the whole list to the model; with *select* the table is rebuilt
        and that list index selected."""
        self._writing = True
        try:
            self.ctx.settings.set(APPS, apps, [])
        finally:
            self._writing = False
        if select is not None:
            self._fill_apps(select)

    def _fill_apps(self, select: int | None = None) -> None:
        t = self.app_table
        if t.state() == QAbstractItemView.State.EditingState:
            self._apps_stale = True
            return
        self._apps_stale = False
        if select is None:
            select = self._index_of(t.currentRow())
        self._filling = True
        t.setRowCount(0)
        labels = {"default": _t("Filter everything"), "bypass_https": _t("Skip HTTPS filtering"),
                  "bypass": _t("Don't filter")}
        for index, entry in enumerate(self.ctx.settings.value(APPS, [])):
            if not isinstance(entry, dict):
                continue
            row = t.rowCount()
            t.insertRow(row)
            if "include-list" in entry:
                source = str(entry["include-list"])
                cells = [_t("Browser list ({})", source), _t("Included"), ""]
                for column, text in enumerate(cells):
                    item = QTableWidgetItem(text)
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setToolTip(_t("Browser list included from {}", source))
                    t.setItem(row, column, item)
                t.item(row, 0).setData(_INDEX, index)
                continue

            name = QTableWidgetItem(str(entry.get("name", "")))
            name.setData(_INDEX, index)
            t.setItem(row, 0, name)
            for column in (1, 2):
                filler = QTableWidgetItem("")
                filler.setFlags(filler.flags() & ~Qt.ItemFlag.ItemIsEditable)
                t.setItem(row, column, filler)

            combo = ui.ignore_idle_wheel(QComboBox())
            for value, label in labels.items():
                combo.addItem(label, value)
            action = str(entry.get("action") or "default")
            if combo.findData(action) < 0:
                combo.addItem(action, action)      # a value this version doesn't know stays
            combo.setCurrentIndex(combo.findData(action))
            combo.setAccessibleName(_t("Filtering"))
            combo.setProperty("app_index", index)
            combo.currentIndexChanged.connect(self._on_action_changed)
            t.setCellWidget(row, 1, self._centered(combo, Qt.AlignmentFlag.AlignLeft))

            switch = ui.Switch()
            switch.setChecked(bool(entry.get("skip_outbound_proxy", False)))
            switch.setAccessibleName(_t("Skip outbound proxy"))
            switch.setToolTip(_t("Don't route this app's traffic through outbound proxy"))
            switch.setProperty("app_index", index)
            switch.toggled.connect(self._on_skip_toggled)
            t.setCellWidget(row, 2, self._centered(switch, Qt.AlignmentFlag.AlignCenter))
        self._filling = False

        rows = sum(t.rowHeight(r) for r in range(t.rowCount()))
        t.setFixedHeight(t.horizontalHeader().sizeHint().height() + rows + 2 * t.frameWidth() + 2)
        row = self._row_of(select)
        if row >= 0:
            t.setCurrentCell(row, 0)
        self._update_app_buttons()

    @staticmethod
    def _centered(widget: QWidget, align) -> QWidget:
        box = QWidget()
        lay = QHBoxLayout(box)
        lay.setContentsMargins(3, 0, 8, 0)
        lay.addWidget(widget, 0, align | Qt.AlignmentFlag.AlignVCenter)
        return box

    def _index_of(self, row: int) -> int | None:
        item = self.app_table.item(row, 0) if row >= 0 else None
        return item.data(_INDEX) if item is not None else None

    def _row_of(self, index: int | None) -> int:
        for row in range(self.app_table.rowCount()):
            if index is not None and self._index_of(row) == index:
                return row
        return -1

    def _entry(self, apps: list, index) -> dict | None:
        if isinstance(index, int) and 0 <= index < len(apps) and isinstance(apps[index], dict):
            return apps[index]
        return None

    def _on_app_item_changed(self, item: QTableWidgetItem) -> None:
        if self._filling or item.column() != 0:
            return
        apps = self._apps()
        entry = self._entry(apps, item.data(_INDEX))
        name = item.text().strip()
        if self._apps_stale or entry is None or "include-list" in entry or not name:
            # An empty pattern is not a rule: show the stored one again.
            self._apps_stale = True
            self._fill_apps()
            return
        entry["name"] = name
        if item.text() != name:
            self._filling = True
            item.setText(name)
            self._filling = False
        self._write_apps(apps)

    def _on_action_changed(self, _index: int) -> None:
        combo = self.sender()
        self._set_field(combo.property("app_index"), "action", combo.currentData())

    def _on_skip_toggled(self, on: bool) -> None:
        self._set_field(self.sender().property("app_index"), "skip_outbound_proxy", on)

    def _set_field(self, index: int, key: str, value) -> None:
        if self._filling:
            return
        apps = self._apps()
        entry = self._entry(apps, index)
        if entry is None:
            return
        if key == "skip_outbound_proxy" and not value:
            entry.pop(key, None)
        else:
            entry[key] = value
        self._write_apps(apps)
        row = self._row_of(index)
        if row >= 0 and row != self.app_table.currentRow():
            self.app_table.setCurrentCell(row, 0)

    def _add_app(self) -> None:
        dialog = _AppRuleDialog(self)
        accepted = dialog.exec() == QDialog.DialogCode.Accepted
        pattern = dialog.pattern.text().strip()
        action, skip = dialog.action.currentData(), dialog.skip.isChecked()
        dialog.deleteLater()
        if not accepted:
            return
        apps = self._apps()
        existing = next((i for i, e in enumerate(apps)
                         if isinstance(e, dict) and e.get("name") == pattern), None)
        if existing is not None:
            self.banner.show_message(_t("There is already a rule for '{}'.", pattern), "info",
                                     timeout_ms=5000)
            self.app_table.setCurrentCell(self._row_of(existing), 0)
            return
        entry = {"name": pattern, "action": action}
        if skip:
            entry["skip_outbound_proxy"] = True
        # Rules match top to bottom, and "*" has to stay last.
        at = next((i for i, e in enumerate(apps) if isinstance(e, dict) and e.get("name") == "*"),
                  len(apps))
        apps.insert(at, entry)
        self._write_apps(apps, select=at)

    def _remove_app(self) -> None:
        row = self.app_table.currentRow()
        apps = self._apps()
        index = self._index_of(row)
        entry = self._entry(apps, index)
        if entry is None:
            return
        if "include-list" in entry or entry.get("name") == "*":
            self.banner.show_message(
                _t("The browser include-list and wildcard (*) rule cannot be removed."), "info",
                timeout_ms=5000)
            return
        del apps[index]
        after = self._index_of(row + 1)
        self._write_apps(apps, select=(after - 1) if after is not None else self._index_of(row - 1))

    def _move_app(self, step: int) -> None:
        row = self.app_table.currentRow()
        a, b = self._index_of(row), self._index_of(row + step)
        if a is None or b is None:
            return
        apps = self._apps()
        apps[a], apps[b] = apps[b], apps[a]
        self._write_apps(apps, select=b)

    def _update_app_buttons(self) -> None:
        row = self.app_table.currentRow()
        selected = bool(self.app_table.selectedItems()) and row >= 0
        self.btn_app_remove.setEnabled(selected)
        self.btn_app_up.setEnabled(selected and row > 0)
        self.btn_app_down.setEnabled(selected and row < self.app_table.rowCount() - 1)


def _public_suffix(domain: str) -> bool:
    """A two-part suffix such as gov.uk or co.jp: allowing it would allow
    every site under it, so "www.gov.uk" keeps its www. (no suffix list in
    the stdlib; this covers the common second-level ones)."""
    first, _, tld = domain.partition(".")
    return "." not in tld and len(tld) == 2 and first in {
        "co", "com", "gov", "ac", "org", "net", "edu", "or", "ne", "go", "gob", "nic"}


class _AppRuleDialog(QDialog):
    """Pattern and treatment of a new app rule, chosen before the rule exists."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(_t("Add app rule"))
        self.setMinimumWidth(420)
        form = QFormLayout(self)
        self.pattern = QLineEdit()
        self.pattern.setPlaceholderText("*steam*")
        form.addRow(_t("App pattern"), self.pattern)
        self.action = QComboBox()
        # Most rules exist to take an app out of filtering, e.g. a game with anti-cheat.
        for value, label in (("bypass", _t("Don't filter")),
                             ("bypass_https", _t("Skip HTTPS filtering")),
                             ("default", _t("Filter everything"))):
            self.action.addItem(label, value)
        form.addRow(_t("Filtering"), self.action)
        self.skip = ui.Switch()
        form.addRow(_t("Skip outbound proxy"), self.skip)
        form.addRow(ui.Caption(_t("Wildcards work, e.g. *steam* or *EasyAntiCheat*.")))
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                                   | QDialogButtonBox.StandardButton.Cancel)
        ok = buttons.button(QDialogButtonBox.StandardButton.Ok)
        ok.setText(_t("Add"))
        ok.setEnabled(False)
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(_t("Cancel"))
        self.pattern.textChanged.connect(lambda text: ok.setEnabled(bool(text.strip())))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)
