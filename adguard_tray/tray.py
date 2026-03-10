"""
Main tray application.

Menu structure:
  ● Status: <text>
  ─────────────────────────────────────
  ↺  Umschalten
  ▶  Aktivieren          (only when inactive)
  ■  Deaktivieren        (only when active)
  ↺  Neu starten         (only when active)
  ─────────────────────────────────────
  ▸  Filter              ► (submenu, lazy-loaded)
       [✓] AdGuard Base filter
       [✓] Tracking Protection
       …
       ─────────
       Filter verwalten…
  ▸  Userscripts         ► (submenu, lazy-loaded)
       [✓] AdGuard Extra
       [✓] AdGuard Popup Blocker
       ─────────
       Userscripts verwalten…
  ─────────────────────────────────────
  ⟳  Status aktualisieren
  ─────────────────────────────────────
  ⚙  Einstellungen…
  [✓] Autostart beim Login
  ─────────────────────────────────────
  ✕  Beenden

Left-click → immediate status refresh.
"""

import logging
from pathlib import Path

from PyQt6.QtCore import QObject, QRunnable, QThread, QThreadPool, QTimer, pyqtSignal, pyqtSlot, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from .cli import (
    AdGuardCLI, AdGuardStatus, FilterListResult, StatusResult, UserscriptListResult,
)
from .config import Config
from .icons import icon_active, icon_error, icon_inactive, icon_unknown
from .notifications import notify
from .worker import StatusWorker

logger = logging.getLogger(__name__)

_AUTOSTART_FILE = Path.home() / ".config" / "autostart" / "adguard-tray.desktop"

_STATUS_LABEL: dict[AdGuardStatus, str] = {
    AdGuardStatus.ACTIVE:        "Aktiv  –  Schutz läuft",
    AdGuardStatus.INACTIVE:      "Inaktiv  –  Schutz gestoppt",
    AdGuardStatus.ERROR:         "Fehler beim Statusabruf",
    AdGuardStatus.NOT_INSTALLED: "adguard-cli nicht gefunden",
    AdGuardStatus.UNKNOWN:       "Status unbekannt",
}

_STATUS_ICON = {
    AdGuardStatus.ACTIVE:        icon_active,
    AdGuardStatus.INACTIVE:      icon_inactive,
    AdGuardStatus.ERROR:         icon_error,
    AdGuardStatus.NOT_INSTALLED: icon_error,
    AdGuardStatus.UNKNOWN:       icon_unknown,
}


# ── Async helpers ──────────────────────────────────────────────────────────

class _ActionSignals(QObject):
    done = pyqtSignal(bool, str)

class _ActionRunnable(QRunnable):
    def __init__(self, fn, signals: _ActionSignals) -> None:
        super().__init__()
        self._fn = fn
        self.signals = signals
        self.setAutoDelete(True)

    @pyqtSlot()
    def run(self) -> None:
        try:
            ok, msg = self._fn()
        except Exception as exc:
            logger.exception("Unexpected error in action runnable")
            ok, msg = False, str(exc)
        self.signals.done.emit(ok, msg)


class _FilterLoader(QThread):
    done = pyqtSignal(object)  # FilterListResult
    def __init__(self, cli): super().__init__(); self.cli = cli
    def run(self): self.done.emit(self.cli.get_filters())

class _FilterToggle(QThread):
    done = pyqtSignal(bool, str, int, bool)
    def __init__(self, cli, fid, enable):
        super().__init__(); self.cli = cli; self.fid = fid; self.enable = enable
    def run(self):
        fn = self.cli.enable_filter if self.enable else self.cli.disable_filter
        ok, msg = fn(self.fid)
        self.done.emit(ok, msg, self.fid, self.enable)

class _UserscriptLoader(QThread):
    done = pyqtSignal(object)  # UserscriptListResult
    def __init__(self, cli): super().__init__(); self.cli = cli
    def run(self): self.done.emit(self.cli.get_userscripts())

class _UserscriptToggle(QThread):
    done = pyqtSignal(bool, str, str, bool)
    def __init__(self, cli, name, enable):
        super().__init__(); self.cli = cli; self.name = name; self.enable = enable
    def run(self):
        fn = self.cli.enable_userscript if self.enable else self.cli.disable_userscript
        ok, msg = fn(self.name)
        self.done.emit(ok, msg, self.name, self.enable)


# ── Main tray class ────────────────────────────────────────────────────────

class AdGuardTray(QSystemTrayIcon):
    def __init__(
        self,
        app: QApplication,
        cli: AdGuardCLI,
        config: Config,
        exec_path: str,
    ) -> None:
        super().__init__()
        self.app = app
        self.cli = cli
        self.config = config
        self.exec_path = exec_path

        self._last_status: AdGuardStatus | None = None
        self._busy = False
        self._bg_threads: list[QThread] = []  # keep refs alive

        self._setup_icons()
        self._build_menu()
        self.activated.connect(self._on_activated)
        self.setVisible(True)

        self.worker = StatusWorker(self.cli, config.refresh_interval)
        self.worker.status_updated.connect(self._on_status_result)
        self.worker.start()

    # ── Icons ──────────────────────────────────────────────────────────────

    def _setup_icons(self) -> None:
        self._icon_map = {s: fn() for s, fn in _STATUS_ICON.items()}
        self.setIcon(self._icon_map[AdGuardStatus.UNKNOWN])

    # ── Menu construction ──────────────────────────────────────────────────

    def _build_menu(self) -> None:
        menu = QMenu()

        # Status label (non-clickable)
        self._act_status = QAction("Status wird abgefragt…")
        self._act_status.setEnabled(False)
        menu.addAction(self._act_status)

        menu.addSeparator()

        # Protection controls
        self._act_toggle = QAction("Umschalten")
        self._act_toggle.triggered.connect(self._do_toggle)
        menu.addAction(self._act_toggle)

        self._act_enable = QAction("Aktivieren")
        self._act_enable.triggered.connect(self._do_enable)
        menu.addAction(self._act_enable)

        self._act_disable = QAction("Deaktivieren")
        self._act_disable.triggered.connect(self._do_disable)
        menu.addAction(self._act_disable)

        self._act_restart = QAction("Neu starten")
        self._act_restart.triggered.connect(self._do_restart)
        menu.addAction(self._act_restart)

        menu.addSeparator()

        # Filter submenu
        self._filter_menu = QMenu("Filter")
        self._filter_menu.aboutToShow.connect(self._load_filter_submenu)
        menu.addMenu(self._filter_menu)

        # Userscript submenu
        self._us_menu = QMenu("Userscripts")
        self._us_menu.aboutToShow.connect(self._load_userscript_submenu)
        menu.addMenu(self._us_menu)

        menu.addSeparator()

        act_refresh = QAction("Status aktualisieren")
        act_refresh.triggered.connect(lambda: self.worker.refresh())
        menu.addAction(act_refresh)

        menu.addSeparator()

        act_settings = QAction("Einstellungen…")
        act_settings.triggered.connect(self._show_settings)
        menu.addAction(act_settings)

        self._act_autostart = QAction("Autostart beim Login")
        self._act_autostart.setCheckable(True)
        self._act_autostart.setChecked(_AUTOSTART_FILE.exists())
        self._act_autostart.triggered.connect(self._toggle_autostart)
        menu.addAction(self._act_autostart)

        menu.addSeparator()

        act_quit = QAction("Beenden")
        act_quit.triggered.connect(self.app.quit)
        menu.addAction(act_quit)

        self.setContextMenu(menu)
        self._update_menu_state(None)

    def _update_menu_state(self, status: AdGuardStatus | None) -> None:
        is_active = status == AdGuardStatus.ACTIVE
        is_inactive = status in (AdGuardStatus.INACTIVE, AdGuardStatus.UNKNOWN, None)
        not_installed = status == AdGuardStatus.NOT_INSTALLED
        not_busy = not self._busy

        self._act_toggle.setEnabled(not_busy and not not_installed)
        self._act_enable.setVisible(not is_active)
        self._act_enable.setEnabled(not_busy and is_inactive)
        self._act_disable.setVisible(is_active)
        self._act_disable.setEnabled(not_busy)
        self._act_restart.setEnabled(not_busy and is_active)

    # ── Filter submenu (lazy) ──────────────────────────────────────────────

    def _load_filter_submenu(self) -> None:
        self._filter_menu.clear()
        placeholder = self._filter_menu.addAction("Wird geladen…")
        placeholder.setEnabled(False)

        w = _FilterLoader(self.cli)
        w.done.connect(self._populate_filter_submenu)
        w.finished.connect(lambda: self._bg_threads.remove(w))
        self._bg_threads.append(w)
        w.start()

    def _populate_filter_submenu(self, result: FilterListResult) -> None:
        self._filter_menu.clear()

        if result.error:
            err = self._filter_menu.addAction(f"Fehler: {result.error}")
            err.setEnabled(False)
        else:
            for group_name, filters in result.groups.items():
                # Group header
                grp_action = self._filter_menu.addAction(f"── {group_name} ──")
                grp_action.setEnabled(False)
                font = grp_action.font()
                font.setBold(True)
                grp_action.setFont(font)

                for f in filters:
                    act = QAction(f.title, self._filter_menu)
                    act.setCheckable(True)
                    act.setChecked(f.enabled)
                    # capture by value
                    act.triggered.connect(
                        lambda checked, fid=f.id: self._toggle_filter(fid, checked)
                    )
                    self._filter_menu.addAction(act)

        self._filter_menu.addSeparator()
        act_manage = self._filter_menu.addAction("Filter verwalten…")
        act_manage.triggered.connect(self._show_filters_dialog)

    def _toggle_filter(self, fid: int, enable: bool) -> None:
        w = _FilterToggle(self.cli, fid, enable)
        w.done.connect(self._on_filter_toggle_done)
        w.finished.connect(lambda: self._bg_threads.remove(w))
        self._bg_threads.append(w)
        w.start()

    def _on_filter_toggle_done(self, ok: bool, msg: str, fid: int, new_enabled: bool) -> None:
        if not ok and self.config.notifications_enabled:
            notify("AdGuard Tray – Fehler", msg, urgency="critical", tray=self)

    # ── Userscript submenu (lazy) ──────────────────────────────────────────

    def _load_userscript_submenu(self) -> None:
        self._us_menu.clear()
        placeholder = self._us_menu.addAction("Wird geladen…")
        placeholder.setEnabled(False)

        w = _UserscriptLoader(self.cli)
        w.done.connect(self._populate_userscript_submenu)
        w.finished.connect(lambda: self._bg_threads.remove(w))
        self._bg_threads.append(w)
        w.start()

    def _populate_userscript_submenu(self, result: UserscriptListResult) -> None:
        self._us_menu.clear()

        if result.error:
            err = self._us_menu.addAction(f"Fehler: {result.error}")
            err.setEnabled(False)
        elif not result.scripts:
            none_act = self._us_menu.addAction("Keine Userscripts installiert")
            none_act.setEnabled(False)
        else:
            for s in result.scripts:
                act = QAction(s.title, self._us_menu)
                act.setCheckable(True)
                act.setChecked(s.enabled)
                act.triggered.connect(
                    lambda checked, name=s.name: self._toggle_userscript(name, checked)
                )
                self._us_menu.addAction(act)

        self._us_menu.addSeparator()
        act_manage = self._us_menu.addAction("Userscripts verwalten…")
        act_manage.triggered.connect(self._show_userscripts_dialog)

    def _toggle_userscript(self, name: str, enable: bool) -> None:
        w = _UserscriptToggle(self.cli, name, enable)
        w.done.connect(self._on_userscript_toggle_done)
        w.finished.connect(lambda: self._bg_threads.remove(w))
        self._bg_threads.append(w)
        w.start()

    def _on_userscript_toggle_done(self, ok: bool, msg: str, name: str, new_enabled: bool) -> None:
        if not ok and self.config.notifications_enabled:
            notify("AdGuard Tray – Fehler", msg, urgency="critical", tray=self)

    # ── Status updates ─────────────────────────────────────────────────────

    def _on_status_result(self, result: StatusResult) -> None:
        old = self._last_status
        self._last_status = result.status

        self.setIcon(self._icon_map[result.status])

        lines = [_STATUS_LABEL[result.status]]
        if result.proxy_port:
            lines.append(f"HTTP-Proxy: 127.0.0.1:{result.proxy_port}")
        if result.status == AdGuardStatus.ACTIVE:
            state = "aktiv" if result.filtering_enabled else "inaktiv"
            lines.append(f"Systemweites Filtern: {state}")
        if result.status == AdGuardStatus.ERROR and result.message:
            lines.append(f"Fehler: {result.message}")
        self.setToolTip("\n".join(lines))

        self._act_status.setText(_STATUS_LABEL[result.status])
        self._update_menu_state(result.status)

        if old is not None and old != result.status and self.config.notifications_enabled:
            self._notify_change(old, result.status)

    def _notify_change(self, old: AdGuardStatus, new: AdGuardStatus) -> None:
        if new == AdGuardStatus.ACTIVE:
            notify("AdGuard Tray", "AdGuard ist jetzt aktiv – Schutz läuft.", tray=self)
        elif new == AdGuardStatus.INACTIVE:
            notify("AdGuard Tray", "AdGuard wurde gestoppt.", urgency="low", tray=self)
        elif new == AdGuardStatus.ERROR:
            notify("AdGuard Tray – Fehler", "Status konnte nicht abgerufen werden.",
                   urgency="critical", tray=self)

    # ── Protection actions ─────────────────────────────────────────────────

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        self._update_menu_state(self._last_status)

    def _do_toggle(self) -> None:
        if self._busy: return
        self._set_busy(True)
        self._run_async(self.cli.stop if self._last_status == AdGuardStatus.ACTIVE else self.cli.start)

    def _do_enable(self) -> None:
        if self._busy: return
        self._set_busy(True)
        self._run_async(self.cli.start)

    def _do_disable(self) -> None:
        if self._busy: return
        self._set_busy(True)
        self._run_async(self.cli.stop)

    def _do_restart(self) -> None:
        if self._busy: return
        self._set_busy(True)
        self._run_async(self.cli.restart)

    def _run_async(self, fn) -> None:
        sig = _ActionSignals()
        sig.done.connect(self._on_action_done)
        QThreadPool.globalInstance().start(_ActionRunnable(fn, sig))

    def _on_action_done(self, ok: bool, msg: str) -> None:
        self._set_busy(False)
        if not ok and self.config.notifications_enabled:
            notify("AdGuard Tray – Fehler", msg or "Befehl fehlgeschlagen",
                   urgency="critical", tray=self)
        QTimer.singleShot(1500, self.worker.refresh)

    # ── Autostart ──────────────────────────────────────────────────────────

    def _toggle_autostart(self, enable: bool) -> None:
        from .settings_dialog import _AUTOSTART_DIR, _DESKTOP_TEMPLATE
        if enable:
            try:
                _AUTOSTART_DIR.mkdir(parents=True, exist_ok=True)
                _AUTOSTART_FILE.write_text(
                    _DESKTOP_TEMPLATE.format(exec=self.exec_path), encoding="utf-8"
                )
                logger.info("Autostart enabled")
            except OSError as exc:
                logger.error("Autostart enable failed: %s", exc)
                self._act_autostart.setChecked(False)
        else:
            try:
                _AUTOSTART_FILE.unlink(missing_ok=True)
                logger.info("Autostart disabled")
            except OSError as exc:
                logger.error("Autostart disable failed: %s", exc)
                self._act_autostart.setChecked(True)

    # ── Dialogs ────────────────────────────────────────────────────────────

    def _show_settings(self) -> None:
        from .settings_dialog import SettingsDialog
        dlg = SettingsDialog(self.config, self.exec_path)
        if dlg.exec():
            self.worker.set_interval(self.config.refresh_interval)
            # Sync autostart checkbox with whatever settings dialog did
            self._act_autostart.setChecked(_AUTOSTART_FILE.exists())

    def _show_filters_dialog(self) -> None:
        from .filters_dialog import FiltersDialog
        FiltersDialog(self.cli, parent=None).exec()

    def _show_userscripts_dialog(self) -> None:
        from .userscripts_dialog import UserscriptsDialog
        UserscriptsDialog(self.cli, parent=None).exec()

    # ── Tray click ─────────────────────────────────────────────────────────

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.worker.refresh()
