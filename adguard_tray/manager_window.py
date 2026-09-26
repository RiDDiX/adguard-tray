"""
Manager window – everything adguard-tray can show or change, one page each.

A sidebar picks the page. Pages are built the first time they are opened, so
opening the window starts one page's workers, not twelve.

Settings that live in adguard-cli's proxy.yaml are edited through one shared
model (proxy_settings.ProxySettings) on whichever page they belong to. Their
edits collect in the Apply bar at the bottom, and applying them costs a single
restart of AdGuard. Lists (filters, userscripts, exceptions) apply at once.
"""

import logging
import time
from dataclasses import dataclass, field

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from . import theme, ui
from .cli import AdGuardCLI, AdGuardStatus
from .config import Config
from .i18n import _t
from .proxy_settings import ProxySettings

logger = logging.getLogger(__name__)

# Page indices used by callers that want to open a specific page.
(PAGE_OVERVIEW, PAGE_ACTIVITY, PAGE_FILTERS, PAGE_DNS, PAGE_USERSCRIPTS, PAGE_EXCEPTIONS,
 PAGE_HTTPS, PAGE_STEALTH, PAGE_NETWORK, PAGE_MAINTENANCE, PAGE_SETTINGS, PAGE_ABOUT) = range(12)


def _pages():
    """(group, key, title, icon names, module, class) in sidebar order."""
    protection, system = _t("Protection"), _t("System")
    return [
        (None, "overview", _t("Overview"),
         ("go-home-symbolic", "go-home"), "overview_tab", "OverviewTab"),
        (None, "activity", _t("Activity"),
         ("view-statistics", "document-open-recent-symbolic"),
         "activity_tab", "ActivityTab"),
        (protection, "filters", _t("Filters"),
         ("view-filter", "view-list-bullet-symbolic"), "filters_tab", "FiltersTab"),
        (protection, "dns", _t("DNS"),
         ("preferences-system-network-symbolic", "preferences-system-network"), "dns_filters_tab", "DnsFiltersTab"),
        (protection, "userscripts", _t("Userscripts"),
         ("code-context", "accessories-text-editor-symbolic"),
         "userscripts_tab", "UserscriptsTab"),
        (protection, "exceptions", _t("Exceptions"),
         ("object-select-symbolic", "checkmark", "dialog-ok-apply", "security-low-symbolic"),
         "exceptions_tab", "ExceptionsTab"),
        (protection, "https", _t("HTTPS"),
         ("channel-secure-symbolic", "document-encrypt", "security-medium"), "https_tab", "HttpsTab"),
        (protection, "stealth", _t("Stealth mode"),
         ("view-private", "security-medium-symbolic"), "stealth_tab", "StealthTab"),
        (system, "network", _t("Network"),
         ("network-wired-symbolic", "network-wired"), "network_tab", "NetworkTab"),
        (system, "maintenance", _t("Maintenance"),
         ("system-run-symbolic", "tools-report-bug", "applications-engineering-symbolic"),
         "diagnostics_tab", "DiagnosticsTab"),
        (system, "settings", _t("Settings"),
         ("configure", "applications-system-symbolic"),
         "preferences_tab", "PreferencesTab"),
        (system, "about", _t("About"),
         ("dialog-information-symbolic", "help-about"), "about_tab", "AboutTab"),
    ]


@dataclass
class Context:
    """What every page gets: the CLI, the configs, and ways to reach the rest."""
    cli: AdGuardCLI
    config: Config
    settings: ProxySettings
    exec_path: list = field(default_factory=list)
    on_restart: object = None          # debounced AdGuard restart (tray)
    on_status_change: object = None   # ask the tray to re-poll soon
    on_config_change: object = None    # the app's own config.json was saved
    status: object = None              # () -> last known AdGuardStatus or None
    navigate: object = None            # (page index) -> None
    window: object = None

    def restart_adguard(self) -> str:
        """Queue the restart that applies a change; say what will happen."""
        if self.on_restart:
            self.on_restart()
        status = self.status() if self.status else None
        if status in (AdGuardStatus.INACTIVE, AdGuardStatus.NOT_INSTALLED):
            return _t("Saved. The change applies when protection is turned on.")
        return _t("Saved. AdGuard restarts to apply the change.")


class ManagerWindow(QMainWindow):
    def __init__(
        self,
        cli: AdGuardCLI,
        config: Config,
        on_restart=None,
        on_status_change=None,
        parent=None,
        initial_tab: int = 0,
        exec_path=None,
        status=None,
        on_config_change=None,
    ) -> None:
        super().__init__(parent)
        self.cli = cli
        self.config = config
        self._on_restart = on_restart
        self._on_status_change = on_status_change

        self.setWindowTitle(_t("AdGuard Tray"))
        self.setMinimumSize(900, 600)
        self.resize(1080, 720)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        self.settings = ProxySettings(self)
        self.ctx = Context(
            cli=cli, config=config, settings=self.settings, exec_path=exec_path or [],
            on_restart=on_restart, on_status_change=on_status_change,
            on_config_change=on_config_change, status=status,
            navigate=self.set_current_tab, window=self,
        )
        self._defs = _pages()
        self.page_names = [key for _, key, *_ in self._defs]
        self._pages: dict[int, QWidget] = {}
        self._rows: list[int] = []        # sidebar row → page index (-1 = header)
        self._shown_before = False
        self.ask_on_close = False       # set by the tray's Quit, which can wait for an answer

        self._build_ui()
        theme.watcher().changed.connect(self._restyle)
        self._restyle()
        self.set_current_tab(initial_tab)

    # ── Layout ─────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        central = QWidget()
        outer = QHBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self.sidebar = QListWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(212)
        self.sidebar.setAccessibleName(_t("Pages"))
        self.sidebar.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        last_group = None
        for index, (group, _key, title, _icons, _mod, _cls) in enumerate(self._defs):
            if group and group != last_group:
                header = QListWidgetItem(group.upper())
                header.setFlags(Qt.ItemFlag.NoItemFlags)
                header.setFont(ui.scaled_font(self.sidebar, 0.8, bold=True))
                self.sidebar.addItem(header)
                self._rows.append(-1)
                last_group = group
            self.sidebar.addItem(QListWidgetItem(title))
            self._rows.append(index)
        self.sidebar.currentRowChanged.connect(self._on_row)
        outer.addWidget(self.sidebar)

        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(0)

        header = QHBoxLayout()
        header.setContentsMargins(24, 14, 16, 4)
        self.lbl_title = ui.heading("", 1.35)
        header.addWidget(self.lbl_title, 1)
        self.btn_refresh = QToolButton()
        self.btn_refresh.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btn_refresh.setAutoRaise(True)
        self.btn_refresh.setText(_t("Refresh"))
        self.btn_refresh.setToolTip(_t("Refresh this page (F5)"))
        self.btn_refresh.clicked.connect(self.refresh_current)
        header.addWidget(self.btn_refresh)
        # Every page can refresh (proxy.yaml at least), so the header never changes height.
        rl.addLayout(header)

        self.stack = QStackedWidget()
        for _ in self._defs:
            self.stack.addWidget(QWidget())      # placeholders, built on first visit
        rl.addWidget(self.stack, 1)

        self.apply_bar = self._build_apply_bar()
        rl.addWidget(self.apply_bar)
        outer.addWidget(right, 1)
        self.setCentralWidget(central)

        QShortcut(QKeySequence(QKeySequence.StandardKey.Refresh), self, self.refresh_current)
        QShortcut(QKeySequence(QKeySequence.StandardKey.Find), self, self._focus_search)
        for number in range(1, 10):
            QShortcut(QKeySequence(f"Alt+{number}"), self,
                      lambda n=number - 1: self.set_current_tab(n))

    def _build_apply_bar(self) -> QWidget:
        wrap = QWidget()
        lay = QHBoxLayout(wrap)
        lay.setContentsMargins(24, 6, 24, 12)
        bar = ui.Card(tone="info")
        row = QHBoxLayout()
        row.setContentsMargins(14, 8, 10, 8)
        text = QVBoxLayout()
        text.setSpacing(0)
        self.lbl_pending = QLabel("")
        self.lbl_pending.setWordWrap(True)
        self.lbl_pending.setFont(ui.scaled_font(self.lbl_pending, 1.0, bold=True))
        text.addWidget(self.lbl_pending)
        text.addWidget(ui.Caption(_t("Applying them restarts AdGuard if protection is on.")))
        row.addLayout(text, 1)
        btn_discard = QPushButton(_t("Discard"))
        btn_discard.clicked.connect(self.settings.discard)
        row.addWidget(btn_discard)
        self.btn_apply = QPushButton(_t("Apply"))
        self.btn_apply.setDefault(True)
        self.btn_apply.clicked.connect(self.apply_settings)
        row.addWidget(self.btn_apply)
        bar.layout_.addLayout(row)
        lay.addWidget(bar)
        wrap.hide()
        self.settings.dirty_changed.connect(self._on_dirty)
        return wrap

    def _on_dirty(self, count: int) -> None:
        self.lbl_pending.setText(
            _t("1 unsaved change to AdGuard's settings") if count == 1
            else _t("{} unsaved changes to AdGuard's settings", count))
        self.apply_bar.setVisible(count > 0)

    def apply_settings(self) -> bool:
        ok, err = self.settings.apply()
        page = self.stack.currentWidget()
        banner = getattr(page, "banner", None)
        if ok:
            message = self.ctx.restart_adguard()
            if banner is not None:
                banner.show_message(message, "success", timeout_ms=6000)
            return True
        if banner is not None:
            banner.show_message(_t("Could not save proxy.yaml:\n{}", err), "danger")
        else:
            QMessageBox.critical(self, _t("Save failed"), _t("Could not save proxy.yaml:\n{}", err))
        return False

    # ── Pages ──────────────────────────────────────────────────────────────

    def set_current_tab(self, index: int) -> None:
        if not 0 <= index < len(self._defs):
            return
        row = self._rows.index(index)
        if self.sidebar.currentRow() == row:
            self._on_row(row)       # no signal for the current row, but callers expect on_shown()
        else:
            self.sidebar.setCurrentRow(row)

    def current_page(self) -> QWidget | None:
        return self._pages.get(self.stack.currentIndex())

    def _on_row(self, row: int) -> None:
        if row < 0 or self._rows[row] < 0:
            return
        index = self._rows[row]
        page = self._page(index)
        self.stack.setCurrentIndex(index)
        self.lbl_title.setText(self._defs[index][2])
        shown = getattr(page, "on_shown", None)
        if shown:
            shown()

    def _page(self, index: int) -> QWidget:
        page = self._pages.get(index)
        if page is not None:
            return page
        _group, _key, _title, _icons, module, cls = self._defs[index]
        import importlib
        page = getattr(importlib.import_module(f".{module}", __package__), cls)(self.ctx)
        old = self.stack.widget(index)
        self.stack.removeWidget(old)
        old.deleteLater()
        self.stack.insertWidget(index, page)
        self._pages[index] = page
        return page

    def refresh_current(self) -> None:
        if not self.settings.dirty():
            self.settings.load()     # proxy.yaml may have been created or changed meanwhile
        page = self.current_page()
        if page is not None and hasattr(page, "refresh"):
            page.refresh()

    def _focus_search(self) -> None:
        page = self.current_page()
        if page is not None and hasattr(page, "focus_search"):
            page.focus_search()

    # ── Theme ──────────────────────────────────────────────────────────────

    def _restyle(self) -> None:
        tok = theme.tokens()
        # Scoped to the sidebar: an app-wide sheet would change every native
        # widget's metrics, and a container background leaks into buttons.
        self.sidebar.setStyleSheet(f"""
            QListWidget#sidebar {{
                background: {tok.sidebar.name()}; border: none;
                border-right: 1px solid {tok.border.name()}; outline: 0; padding: 10px 8px;
            }}
            QListWidget#sidebar::item {{
                padding: 7px 10px; margin: 1px 0; border-radius: 6px; color: {tok.text.name()};
            }}
            QListWidget#sidebar::item:hover {{ background: {tok.sidebar_hover.name()}; }}
            QListWidget#sidebar::item:selected {{
                background: {tok.sidebar_selected.name()}; color: {tok.text.name()};
            }}
            QListWidget#sidebar::item:disabled {{
                color: {tok.secondary.name()}; background: transparent; padding: 14px 10px 4px 10px;
            }}
        """)
        icons = [ui.theme_icon(names, tok.text, 16) for _g, _k, _t, names, _m, _c in self._defs]
        if any(icon is None for icon in icons):
            icons = [None] * len(icons)           # all or none: never a ragged column
        for row, index in enumerate(self._rows):
            if index >= 0:
                item = self.sidebar.item(row)
                item.setIcon(icons[index] if icons[index] is not None else ui.QIcon())
        refresh = ui.theme_icon(("view-refresh-symbolic", "view-refresh"), tok.text, 16)
        self.btn_refresh.setIcon(refresh if refresh is not None else ui.QIcon())

    def showEvent(self, event) -> None:
        # Reopened after a while: adguard-cli may have rewritten proxy.yaml.
        if self._shown_before and not self.settings.dirty():
            self.settings.load()
        self._shown_before = True
        super().showEvent(event)

    # ── Closing ────────────────────────────────────────────────────────────

    def closeEvent(self, event) -> None:
        self.setFocus()     # an open cell editor commits before the check below
        if self.settings.dirty():
            if self.ask_on_close or event.spontaneous():
                box = QMessageBox(self)
                box.setIcon(QMessageBox.Icon.Question)
                box.setWindowTitle(_t("Unsaved changes"))
                box.setText(_t("Apply your changes to AdGuard's settings before closing?"))
                apply = box.addButton(_t("Apply"), QMessageBox.ButtonRole.AcceptRole)
                discard = box.addButton(_t("Discard"), QMessageBox.ButtonRole.DestructiveRole)
                cancel = box.addButton(_t("Cancel"), QMessageBox.ButtonRole.RejectRole)
                box.setDefaultButton(apply)
                box.setEscapeButton(cancel)
                box.exec()
                clicked = box.clickedButton()
                if clicked is cancel or (clicked is apply and not self.apply_settings()):
                    event.ignore()
                    return
                if clicked is discard:
                    self.settings.discard()
            else:
                # A quit nobody can answer (SIGTERM at logout, restart after an
                # update) must not hang on a question; nothing gets written.
                logger.warning("Quitting with %d unapplied AdGuard setting(s)", self.settings.dirty())
        super().closeEvent(event)

    def _wait_for_workers(self, budget_ms: int = 1000) -> None:
        # Page workers hold a reference to their page; give running CLI calls a
        # moment to finish before the window is deleted, but never hang quitting.
        deadline = time.monotonic() + budget_ms / 1000
        for page in self._pages.values():
            for worker in list(getattr(page, "_workers", [])):
                left = int((deadline - time.monotonic()) * 1000)
                if left <= 0:
                    return
                if worker.isRunning():
                    worker.wait(left)

    def dispose(self) -> None:
        """Delete the window now, while the application is still intact."""
        from PyQt6 import sip
        self.hide()
        self._wait_for_workers()
        sip.delete(self)
