"""
Manager window – full GUI for managing AdGuard CLI.

Tabs:
  1. Overview     – status, version, license, quick actions
  2. Filters      – HTTP filter management (existing dialog as tab page)
  3. DNS Filters  – DNS filter management
  4. Userscripts  – userscript management (existing dialog as tab page)
  5. Exceptions   – website exceptions (existing dialog as tab page)
  6. Configuration – proxy.yaml editor (existing dialog as tab page)
  7. Diagnostics  – export logs/settings, import, benchmark
"""

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QTabWidget

from .cli import AdGuardCLI
from .config import Config
from .i18n import _t

logger = logging.getLogger(__name__)


class ManagerWindow(QMainWindow):
    def __init__(self, cli: AdGuardCLI, config: Config, on_restart=None, parent=None) -> None:
        super().__init__(parent)
        self.cli = cli
        self.config = config
        self._on_restart = on_restart

        self.setWindowTitle(_t("AdGuard Tray – Manager"))
        self.setMinimumSize(820, 620)
        self.resize(900, 680)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        self._build_ui()

    def _build_ui(self) -> None:
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tab 1: Overview
        from .overview_tab import OverviewTab
        self._overview = OverviewTab(self.cli, on_restart=self._on_restart)
        self.tabs.addTab(self._overview, _t("Overview"))

        # Tab 2: Filters
        from .filters_tab import FiltersTab
        self._filters = FiltersTab(self.cli, on_change=self._on_restart)
        self.tabs.addTab(self._filters, _t("Filters"))

        # Tab 3: DNS Filters
        from .dns_filters_tab import DnsFiltersTab
        self._dns_filters = DnsFiltersTab(self.cli, on_change=self._on_restart)
        self.tabs.addTab(self._dns_filters, _t("DNS Filters"))

        # Tab 4: Userscripts
        from .userscripts_tab import UserscriptsTab
        self._userscripts = UserscriptsTab(self.cli, on_change=self._on_restart)
        self.tabs.addTab(self._userscripts, _t("Userscripts"))

        # Tab 5: Exceptions
        from .exceptions_tab import ExceptionsTab
        self._exceptions = ExceptionsTab(on_change=self._on_restart)
        self.tabs.addTab(self._exceptions, _t("Exceptions"))

        # Tab 6: Configuration
        from .config_tab import ConfigTab
        self._config_tab = ConfigTab(on_restart=self._on_restart)
        self.tabs.addTab(self._config_tab, _t("Configuration"))

        # Tab 7: Diagnostics
        from .diagnostics_tab import DiagnosticsTab
        self._diagnostics = DiagnosticsTab(self.cli, on_restart=self._on_restart)
        self.tabs.addTab(self._diagnostics, _t("Diagnostics"))

    def closeEvent(self, event) -> None:
        # Trigger restart if any tab marked changes
        tabs_with_changes = [
            self._filters, self._dns_filters, self._userscripts, self._exceptions,
        ]
        if any(getattr(t, "_changed", False) for t in tabs_with_changes) and self._on_restart:
            self._on_restart()
        super().closeEvent(event)
