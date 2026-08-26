"""
Main tray application.

Menu structure (English default – translated at runtime via i18n):
  ● Status: <text>
  ─────────────────────────────────────
  ↺  Toggle
  ▶  Enable              (only when inactive)
  ■  Disable             (only when active)
  ↺  Restart             (only when active)
  ─────────────────────────────────────
  ▸  Filters             ► (submenu, lazy-loaded)
       [✓] AdGuard Base filter
       [✓] Tracking Protection
       …
       ─────────
       Manage filters…
  ▸  Userscripts         ► (submenu, lazy-loaded)
       [✓] AdGuard Extra
       [✓] AdGuard Popup Blocker
       ─────────
       Manage userscripts…
  ─────────────────────────────────────
  ⟳  Refresh status
  ─────────────────────────────────────
  Open Manager…          (tabbed GUI)
  AdGuard Configuration… (proxy.yaml editor)
  Website Exceptions…
  ⚙  Settings…
  [✓] Autostart on login
  ─────────────────────────────────────
  adguard-tray vX.Y.Z · CLI vA.B.C
  ✕  Quit

Left-click → immediate status refresh.
"""

import logging
import time
from pathlib import Path

from PyQt6.QtCore import QObject, QRunnable, QThread, QThreadPool, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from .cli import (
    AdGuardCLI,
    AdGuardStatus,
    FilterListResult,
    StatusResult,
    UserscriptListResult,
)
from .config import Config
from .i18n import _t
from .icons import icon_active, icon_error, icon_inactive, icon_unknown
from .notifications import notify
from .worker import StatusWorker, safe_call, safe_result

logger = logging.getLogger(__name__)

_AUTOSTART_FILE = Path.home() / ".config" / "autostart" / "adguard-tray.desktop"

# How long a failed command stays in the menu line / tooltip when the service
# state itself doesn't change (a cancelled polkit prompt, a rejected toggle).
_ERROR_STICKY_S = 120.0


def autostart_enabled() -> bool:
    """True when the XDG autostart entry exists and isn't disabled in place.

    KDE's and GNOME's autostart tools keep the file and set Hidden=true /
    X-GNOME-Autostart-enabled=false instead of deleting it.
    """
    try:
        text = _AUTOSTART_FILE.read_text(encoding="utf-8")
    except (OSError, ValueError):
        return False
    lowered = text.lower()
    return "hidden=true" not in lowered and "x-gnome-autostart-enabled=false" not in lowered

_STATUS_LABELS: dict[AdGuardStatus, str] | None = None


def _status_label(status: AdGuardStatus) -> str:
    global _STATUS_LABELS
    if _STATUS_LABELS is None:
        _STATUS_LABELS = {
            AdGuardStatus.ACTIVE:        _t("Active – Protection running"),
            AdGuardStatus.INACTIVE:      _t("Inactive – Protection stopped"),
            AdGuardStatus.ERROR:         _t("Error retrieving status"),
            AdGuardStatus.NOT_INSTALLED: _t("adguard-cli not found"),
            AdGuardStatus.UNKNOWN:       _t("Unknown status"),
        }
    return _STATUS_LABELS.get(status, _t("Unknown status"))

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

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

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
    def run(self): self.done.emit(safe_result(self.cli.get_filters, FilterListResult))

class _FilterToggle(QThread):
    done = pyqtSignal(bool, str, int, bool)
    def __init__(self, cli, fid, enable):
        super().__init__(); self.cli = cli; self.fid = fid; self.enable = enable
    def run(self):
        fn = self.cli.enable_filter if self.enable else self.cli.disable_filter
        ok, msg = safe_call(fn, self.fid)
        self.done.emit(ok, msg, self.fid, self.enable)

class _UserscriptLoader(QThread):
    done = pyqtSignal(object)  # UserscriptListResult
    def __init__(self, cli): super().__init__(); self.cli = cli
    def run(self): self.done.emit(safe_result(self.cli.get_userscripts, UserscriptListResult))

class _UserscriptToggle(QThread):
    done = pyqtSignal(bool, str, str, bool)
    def __init__(self, cli, name, enable):
        super().__init__(); self.cli = cli; self.name = name; self.enable = enable
    def run(self):
        fn = self.cli.enable_userscript if self.enable else self.cli.disable_userscript
        ok, msg = safe_call(fn, self.name)
        self.done.emit(ok, msg, self.name, self.enable)


# ── Main tray class ────────────────────────────────────────────────────────

class AdGuardTray(QSystemTrayIcon):
    def __init__(
        self,
        app: QApplication,
        cli: AdGuardCLI,
        config: Config,
        exec_path: list[str] | str,
    ) -> None:
        super().__init__()
        self.app = app
        self.cli = cli
        self.config = config
        self.exec_path = exec_path

        self._last_status: AdGuardStatus | None = None
        self._busy = False
        self._bg_threads: list[QThread] = []  # keep refs alive
        self._loading_filters = False
        self._loading_userscripts = False
        self._filter_sig: tuple | None = None
        self._us_sig: tuple | None = None
        self._filter_placeholder: QAction | None = None
        self._us_placeholder: QAction | None = None
        self._last_notify: tuple[AdGuardStatus, AdGuardStatus, float] | None = None
        self._last_error = ""
        self._last_error_at = 0.0
        self._cli_version: str = ""

        # Coalesce rapid-fire restart triggers (e.g. user flips 4 filters in a
        # row → one pkexec prompt instead of four).
        self._restart_pending = False
        self._restart_debouncer = QTimer(self)
        self._restart_debouncer.setSingleShot(True)
        self._restart_debouncer.setInterval(500)
        self._restart_debouncer.timeout.connect(self._fire_pending_restart)

        self._setup_icons()
        self._build_menu()
        self.activated.connect(self._on_activated)
        self.setVisible(True)
        # Fetch CLI version off-thread so a slow `adguard-cli --version`
        # doesn't stall the menu construction.
        self._refresh_version_label_async()

        self.worker = StatusWorker(self.cli, config.refresh_interval)
        self.worker.status_updated.connect(self._on_status_result)
        self.worker.start()

        # Fill the submenus up front: on Wayland panels the menu is exported
        # over D-Bus, and the first popup shows whatever is there right then.
        QTimer.singleShot(0, self._load_filter_submenu)
        QTimer.singleShot(0, self._load_userscript_submenu)

    # ── Icons ──────────────────────────────────────────────────────────────

    def _setup_icons(self) -> None:
        self._icon_map = {s: fn() for s, fn in _STATUS_ICON.items()}
        self.setIcon(self._icon_map[AdGuardStatus.UNKNOWN])

    # ── Menu construction ──────────────────────────────────────────────────

    def _build_menu(self) -> None:
        menu = QMenu()

        # Status label (non-clickable)
        self._act_status = QAction(_t("Checking status…"))
        self._act_status.setEnabled(False)
        menu.addAction(self._act_status)

        menu.addSeparator()

        # Protection controls
        self._act_toggle = QAction(_t("Toggle"))
        self._act_toggle.triggered.connect(self._do_toggle)
        menu.addAction(self._act_toggle)

        self._act_enable = QAction(_t("Enable"))
        self._act_enable.triggered.connect(self._do_enable)
        menu.addAction(self._act_enable)

        self._act_disable = QAction(_t("Disable"))
        self._act_disable.triggered.connect(self._do_disable)
        menu.addAction(self._act_disable)

        self._act_restart = QAction(_t("Restart"))
        self._act_restart.triggered.connect(self._do_restart)
        menu.addAction(self._act_restart)

        menu.addSeparator()

        # Filter submenu
        self._filter_menu = QMenu(_t("Filters"))
        self._filter_menu.aboutToShow.connect(self._load_filter_submenu)
        self._filter_tail = self._seed_submenu(
            self._filter_menu, _t("Manage filters…"), self._show_filters_dialog
        )
        menu.addMenu(self._filter_menu)

        # Userscript submenu
        self._us_menu = QMenu(_t("Userscripts"))
        self._us_menu.aboutToShow.connect(self._load_userscript_submenu)
        self._us_tail = self._seed_submenu(
            self._us_menu, _t("Manage userscripts…"), self._show_userscripts_dialog
        )
        menu.addMenu(self._us_menu)

        menu.addSeparator()

        self._act_refresh = QAction(_t("Refresh status"))
        self._act_refresh.triggered.connect(lambda: self.worker.refresh())
        menu.addAction(self._act_refresh)

        menu.addSeparator()

        self._act_manager = QAction(_t("Open Manager…"))
        self._act_manager.triggered.connect(self._show_manager)
        menu.addAction(self._act_manager)

        self._act_proxy_config = QAction(_t("AdGuard Configuration…"))
        self._act_proxy_config.triggered.connect(self._show_proxy_config)
        menu.addAction(self._act_proxy_config)

        self._act_exceptions = QAction(_t("Website Exceptions…"))
        self._act_exceptions.triggered.connect(self._show_exceptions_dialog)
        menu.addAction(self._act_exceptions)

        self._act_settings = QAction(_t("Settings…"))
        self._act_settings.triggered.connect(self._show_settings)
        menu.addAction(self._act_settings)

        self._act_autostart = QAction(_t("Autostart on login"))
        self._act_autostart.setCheckable(True)
        self._act_autostart.setChecked(autostart_enabled())
        self._act_autostart.triggered.connect(self._toggle_autostart)
        menu.addAction(self._act_autostart)

        menu.addSeparator()

        # Version info (non-clickable)
        self._act_version = QAction(self._version_label())
        self._act_version.setEnabled(False)
        menu.addAction(self._act_version)

        self._act_quit = QAction(_t("Quit"))
        self._act_quit.triggered.connect(self.app.quit)
        menu.addAction(self._act_quit)

        # Refresh the autostart checkbox each time the menu opens — picks up
        # external changes (e.g. user removed the .desktop file by hand).
        menu.aboutToShow.connect(self._refresh_dynamic_menu_state)

        self.setContextMenu(menu)
        self._update_menu_state(None)

    def _drop_placeholder(self, menu: QMenu, attr: str) -> None:
        """Remove the "Loading…" entry, including on the unchanged-list path."""
        placeholder = getattr(self, attr, None)
        if placeholder is not None:
            menu.removeAction(placeholder)
            placeholder.setParent(None)
            placeholder.deleteLater()
            setattr(self, attr, None)

    @staticmethod
    def _submenu_is_empty(menu: QMenu, tail: list[QAction]) -> bool:
        return all(act in tail for act in menu.actions())

    @staticmethod
    def _replace_submenu_items(
        menu: QMenu, tail: list[QAction], new_actions: list[QAction], anchor: QAction
    ) -> None:
        """Swap a submenu's items without it ever being empty.

        New items go in above the permanent tail first, the old ones are
        removed afterwards – dropping to zero children would make
        libdbusmenu-gtk destroy the submenu for the rest of the session.
        """
        old = [act for act in menu.actions() if act not in tail]
        for act in new_actions:
            menu.insertAction(anchor, act)
        for act in old:
            # removeAction only detaches – without deleting, every rebuild
            # would leave its actions behind for the life of the process.
            menu.removeAction(act)
            act.setParent(None)
            act.deleteLater()

    def _seed_submenu(self, menu: QMenu, manage_text: str, manage_slot) -> list[QAction]:
        """Give a submenu its permanent tail.

        A submenu that is exported empty (or drops back to zero children) is
        destroyed for good by libdbusmenu-gtk, which is what waybar uses – so
        these two entries stay in place and new items are inserted above them.
        """
        separator = menu.addSeparator()
        act_manage = menu.addAction(manage_text)
        act_manage.triggered.connect(manage_slot)
        return [separator, act_manage]

    def _refresh_dynamic_menu_state(self) -> None:
        self._act_autostart.setChecked(autostart_enabled())
        # waybar's dbusmenu client never sends AboutToShow for a submenu (GTK
        # doesn't emit "activate" for items that have one), so the submenus
        # would stay empty forever on Hyprland. Refresh them from here, where
        # AboutToShow does arrive. No-op on KDE, which asks per submenu.
        self._load_filter_submenu()
        self._load_userscript_submenu()

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

    def _discard_thread(self, thread: QThread) -> None:
        try:
            self._bg_threads.remove(thread)
        except ValueError:
            pass

    # ── Filter submenu (lazy) ──────────────────────────────────────────────

    def _load_filter_submenu(self) -> None:
        if self._loading_filters:
            return
        self._loading_filters = True
        if self._submenu_is_empty(self._filter_menu, self._filter_tail):
            self._filter_placeholder = QAction(_t("Loading…"), self._filter_menu)
            self._filter_placeholder.setEnabled(False)
            self._filter_menu.insertAction(self._filter_tail[0], self._filter_placeholder)

        w = _FilterLoader(self.cli)
        w.done.connect(self._populate_filter_submenu)
        w.finished.connect(lambda: self._discard_thread(w))
        self._bg_threads.append(w)
        w.start()

    def _populate_filter_submenu(self, result: FilterListResult) -> None:
        self._loading_filters = False
        self._drop_placeholder(self._filter_menu, "_filter_placeholder")
        signature = (
            result.error,
            tuple((group, tuple((f.id, f.title) for f in filters))
                  for group, filters in result.groups.items()),
        )
        if signature == self._filter_sig:
            # Same list – just sync the check marks instead of rebuilding the
            # menu (every rebuild is a round of dbusmenu layout churn).
            states = {f.id: f.enabled for f in result.all_filters}
            for act in self._filter_menu.actions():
                if act.data() in states:
                    act.blockSignals(True)
                    act.setChecked(states[act.data()])
                    act.blockSignals(False)
            return
        self._filter_sig = signature

        anchor = self._filter_tail[0]
        new_actions: list[QAction] = []
        if result.error:
            err = QAction(_t("Error: {}", result.error), self._filter_menu)
            err.setEnabled(False)
            new_actions.append(err)
        elif not result.groups:
            none_act = QAction(_t("No filters installed"), self._filter_menu)
            none_act.setEnabled(False)
            new_actions.append(none_act)
        else:
            for group_name, filters in result.groups.items():
                grp_action = QAction(f"── {group_name} ──", self._filter_menu)
                grp_action.setEnabled(False)
                font = grp_action.font()
                font.setBold(True)
                grp_action.setFont(font)
                new_actions.append(grp_action)

                for f in filters:
                    act = QAction(f.title, self._filter_menu)
                    act.setCheckable(True)
                    act.setChecked(f.enabled)
                    act.setData(f.id)
                    # capture by value
                    act.triggered.connect(
                        lambda checked, fid=f.id: self._toggle_filter(fid, checked)
                    )
                    new_actions.append(act)

        self._replace_submenu_items(self._filter_menu, self._filter_tail, new_actions, anchor)

    def _toggle_filter(self, fid: int, enable: bool) -> None:
        w = _FilterToggle(self.cli, fid, enable)
        w.done.connect(self._on_filter_toggle_done)
        w.finished.connect(lambda: self._discard_thread(w))
        self._bg_threads.append(w)
        w.start()

    def _on_filter_toggle_done(self, ok: bool, msg: str, fid: int, new_enabled: bool) -> None:
        if ok:
            self._restart_cli_async()
            return
        # Revert the checkbox in the submenu so it matches reality
        for act in self._filter_menu.actions():
            if act.data() == fid:
                act.blockSignals(True)
                act.setChecked(not new_enabled)
                act.blockSignals(False)
                break
        self._report_error(msg)

    # ── Userscript submenu (lazy) ──────────────────────────────────────────

    def _load_userscript_submenu(self) -> None:
        if self._loading_userscripts:
            return
        self._loading_userscripts = True
        if self._submenu_is_empty(self._us_menu, self._us_tail):
            self._us_placeholder = QAction(_t("Loading…"), self._us_menu)
            self._us_placeholder.setEnabled(False)
            self._us_menu.insertAction(self._us_tail[0], self._us_placeholder)

        w = _UserscriptLoader(self.cli)
        w.done.connect(self._populate_userscript_submenu)
        w.finished.connect(lambda: self._discard_thread(w))
        self._bg_threads.append(w)
        w.start()

    def _populate_userscript_submenu(self, result: UserscriptListResult) -> None:
        self._loading_userscripts = False
        self._drop_placeholder(self._us_menu, "_us_placeholder")
        signature = (result.error, tuple((s.name, s.title) for s in result.scripts))
        if signature == self._us_sig:
            states = {s.name: s.enabled for s in result.scripts}
            for act in self._us_menu.actions():
                if act.data() in states:
                    act.blockSignals(True)
                    act.setChecked(states[act.data()])
                    act.blockSignals(False)
            return
        self._us_sig = signature

        anchor = self._us_tail[0]
        new_actions: list[QAction] = []
        if result.error:
            err = QAction(_t("Error: {}", result.error), self._us_menu)
            err.setEnabled(False)
            new_actions.append(err)
        elif not result.scripts:
            none_act = QAction(_t("No userscripts installed"), self._us_menu)
            none_act.setEnabled(False)
            new_actions.append(none_act)
        else:
            for s in result.scripts:
                act = QAction(s.title, self._us_menu)
                act.setCheckable(True)
                act.setChecked(s.enabled)
                act.setData(s.name)
                act.triggered.connect(
                    lambda checked, name=s.name: self._toggle_userscript(name, checked)
                )
                new_actions.append(act)

        self._replace_submenu_items(self._us_menu, self._us_tail, new_actions, anchor)

    def _toggle_userscript(self, name: str, enable: bool) -> None:
        w = _UserscriptToggle(self.cli, name, enable)
        w.done.connect(self._on_userscript_toggle_done)
        w.finished.connect(lambda: self._discard_thread(w))
        self._bg_threads.append(w)
        w.start()

    def _on_userscript_toggle_done(self, ok: bool, msg: str, name: str, new_enabled: bool) -> None:
        if ok:
            self._restart_cli_async()
            return
        for act in self._us_menu.actions():
            if act.data() == name:
                act.blockSignals(True)
                act.setChecked(not new_enabled)
                act.blockSignals(False)
                break
        self._report_error(msg)

    # ── Status updates ─────────────────────────────────────────────────────

    def _on_status_result(self, result: StatusResult) -> None:
        old = self._last_status
        self._last_status = result.status
        if (old is not None and old != result.status) or (
            self._last_error and time.monotonic() - self._last_error_at > _ERROR_STICKY_S
        ):
            # State moved on, or the failure had its time on screen.
            self._last_error = ""

        self.setIcon(self._icon_map[result.status])

        lines = [_status_label(result.status)]
        if result.proxy_port:
            lines.append(f"HTTP Proxy: 127.0.0.1:{result.proxy_port}")
        if result.status == AdGuardStatus.ACTIVE:
            state = _t("active") if result.filtering_enabled else _t("inactive")
            lines.append(_t("System-wide filtering: {}", state))
        if result.status == AdGuardStatus.ERROR and result.message:
            lines.append(_t("Error: {}", result.message))
        if self._last_error:
            lines.append(_t("Error: {}", self._last_error))
        self.setToolTip("\n".join(lines))

        if self._last_error:
            # Keep the failure visible; the refresh right after an error would
            # otherwise wipe it before the user can read it.
            self._act_status.setText(_t("Error: {}", self._last_error))
        else:
            self._act_status.setText(_status_label(result.status))
        self._update_menu_state(result.status)

        if old is not None and old != result.status and self.config.notifications_enabled:
            # Dedup keyed on the (old, new) transition pair, not a single
            # timestamp — that way ACTIVE→ERROR doesn't suppress a follow-up
            # ERROR→INACTIVE within the window.
            now = time.monotonic()
            last = self._last_notify
            same_transition = (
                last is not None
                and last[0] == old
                and last[1] == result.status
                and now - last[2] < 10.0
            )
            if not same_transition:
                self._last_notify = (old, result.status, now)
                self._notify_change(old, result.status)

        # If the CLI just (re)appeared, refresh the version label.
        if (old == AdGuardStatus.NOT_INSTALLED) ^ (result.status == AdGuardStatus.NOT_INSTALLED):
            self._refresh_version_label_async()

    def _notify_change(self, old: AdGuardStatus, new: AdGuardStatus) -> None:
        tag = "adguard-tray-status"  # status popups replace each other
        if new == AdGuardStatus.ACTIVE:
            notify("AdGuard Tray", _t("AdGuard is now active – protection running."),
                   tray=self, replace_tag=tag)
        elif new == AdGuardStatus.INACTIVE:
            notify("AdGuard Tray", _t("AdGuard has been stopped."), urgency="low",
                   tray=self, replace_tag=tag)
        elif new == AdGuardStatus.ERROR:
            notify(_t("AdGuard Tray – Error"), _t("Could not retrieve status."),
                   tray=self, replace_tag=tag)

    # ── Protection actions ─────────────────────────────────────────────────

    def _report_error(self, msg: str) -> None:
        """Surface a failed command.

        Notifications can be switched off, so the last error also goes into the
        menu's status line and the tooltip – otherwise a failed start is
        completely invisible.
        """
        logger.error("Action failed: %s", msg)
        first_line = msg.strip().splitlines()[0] if msg.strip() else ""
        self._last_error = first_line[:120]
        self._last_error_at = time.monotonic()
        if first_line:
            self._act_status.setText(_t("Error: {}", self._last_error))
            self.setToolTip(f"{_status_label(self._last_status)}\n{first_line[:300]}")
        if self.config.notifications_enabled:
            # Not "critical": those never expire and bypass do-not-disturb on
            # KDE and dunst, which is too much for a cancelled prompt.
            notify(_t("AdGuard Tray – Error"), msg, tray=self)

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        self._update_menu_state(self._last_status)

    def _do_toggle(self) -> None:
        if self._busy: return
        self._set_busy(True)
        # cli.toggle() re-reads live status before deciding, so a stale
        # _last_status doesn't push us in the wrong direction.
        self._run_async(self.cli.toggle)

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

    def _run_async(self, fn, slot=None) -> None:
        # Parent the signals object to self so its lifetime is tied to the
        # tray, not just to the runnable that's about to autodelete; drop it
        # once the result has been delivered.
        sig = _ActionSignals(self)
        sig.done.connect(slot or self._on_action_done)
        sig.done.connect(sig.deleteLater)
        QThreadPool.globalInstance().start(_ActionRunnable(fn, sig))

    def _refresh_version_label_async(self) -> None:
        def _fetch() -> tuple[bool, str]:
            try:
                return True, self.cli.get_version()
            except Exception as exc:  # noqa: BLE001
                return False, str(exc)

        self._run_async(_fetch, self._on_version_fetched)

    def _on_version_fetched(self, ok: bool, version: str) -> None:
        if ok:
            self._cli_version = version or ""
        self._act_version.setText(self._version_label())

    def _on_action_done(self, ok: bool, msg: str) -> None:
        self._set_busy(False)
        if ok:
            self._last_error = ""
        else:
            self._report_error(msg or _t("Command failed"))
        # Refresh immediately – cli.stop() already verified the state
        self.worker.refresh()
        # Second check to catch delayed state changes
        QTimer.singleShot(2000, self.worker.refresh)

    def _refresh_status_soon(self) -> None:
        """Re-poll now and once more after the CLI settled."""
        self.worker.refresh()
        QTimer.singleShot(2000, self.worker.refresh)

    def _restart_cli_async(self) -> None:
        """Schedule a debounced restart so rapid filter toggles coalesce."""
        self._restart_pending = True
        # Re-arm the timer on each call: as long as toggles keep coming in
        # under 500ms, only one restart fires after the burst settles.
        self._restart_debouncer.start()

    def _fire_pending_restart(self) -> None:
        if self._restart_pending and self._last_status in (
            AdGuardStatus.INACTIVE, AdGuardStatus.NOT_INSTALLED
        ):
            # Protection was stopped after the change was queued – restarting
            # would silently turn it back on. Ambiguous states (UNKNOWN/ERROR)
            # still restart: dropping a config change is worse there.
            logger.info("Skipping queued restart, AdGuard is not running")
            self._restart_pending = False
            return
        if not self._restart_pending or self._busy:
            # If something else is in flight, push it out a bit instead of
            # racing — the next config change will re-arm us anyway.
            if self._restart_pending and self._busy:
                self._restart_debouncer.start()
            return
        self._restart_pending = False
        self._set_busy(True)
        if self.config.notifications_enabled:
            notify("AdGuard Tray", _t("Restarting AdGuard…"), tray=self)
        self._run_async(self.cli.restart, self._on_restart_done)

    def _on_restart_done(self, ok: bool, msg: str) -> None:
        self._set_busy(False)
        if ok:
            self._last_error = ""
            if self.config.notifications_enabled:
                notify("AdGuard Tray", _t("AdGuard restarted."), tray=self)
        else:
            self._report_error(_t("Restart failed: {}", msg or _t("Unknown error")))
        self.worker.refresh()
        QTimer.singleShot(2000, self.worker.refresh)

    # ── Autostart ──────────────────────────────────────────────────────────

    def _toggle_autostart(self, enable: bool) -> None:
        from .settings_dialog import _AUTOSTART_DIR, desktop_entry
        if enable:
            try:
                _AUTOSTART_DIR.mkdir(parents=True, exist_ok=True)
                _AUTOSTART_FILE.write_text(desktop_entry(self.exec_path), encoding="utf-8")
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

    # ── Manager window ────────────────────────────────────────────────────

    _manager_win = None

    def _show_manager(self, initial_tab: int = 0) -> None:
        from .manager_window import ManagerWindow
        if self._manager_win is not None and self._manager_win.isVisible():
            self._manager_win.set_current_tab(initial_tab)
            self._manager_win.raise_()
            self._manager_win.activateWindow()
            return
        self._manager_win = ManagerWindow(
            self.cli, self.config, on_restart=self._restart_cli_async,
            on_status_change=self._refresh_status_soon,
            initial_tab=initial_tab,
        )
        self._manager_win.show()

    # ── Dialogs ────────────────────────────────────────────────────────────

    def _version_label(self) -> str:
        from . import __version__
        if self._cli_version:
            return f"adguard-tray v{__version__} · CLI v{self._cli_version}"
        return f"adguard-tray v{__version__}"

    def _show_proxy_config(self) -> None:
        from .proxy_config_dialog import ProxyConfigDialog
        dlg = ProxyConfigDialog()
        if dlg.exec():
            self._restart_cli_async()

    def _show_settings(self) -> None:
        from .settings_dialog import SettingsDialog
        dlg = SettingsDialog(self.config, self.exec_path)
        if dlg.exec():
            self.worker.set_interval(self.config.refresh_interval)
            # Sync autostart checkbox with whatever settings dialog did
            self._act_autostart.setChecked(autostart_enabled())

    def _show_filters_dialog(self) -> None:
        # Route to the Manager's Filters tab. The legacy modal lacked
        # add-by-id, --trusted/--title, set-trusted, set-title, and --all.
        from .manager_window import TAB_FILTERS
        self._show_manager(initial_tab=TAB_FILTERS)

    def _show_userscripts_dialog(self) -> None:
        from .manager_window import TAB_USERSCRIPTS
        self._show_manager(initial_tab=TAB_USERSCRIPTS)

    def _show_exceptions_dialog(self) -> None:
        from .exceptions_dialog import ExceptionsDialog
        dlg = ExceptionsDialog(on_change=self._restart_cli_async, parent=None)
        dlg.exec()

    # ── Tray click ─────────────────────────────────────────────────────────

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.worker.refresh()

    # ── Shutdown ───────────────────────────────────────────────────────────

    def shutdown(self) -> None:
        """Stop the status timer and wait briefly for pending QThreads."""
        logger.debug("Shutting down tray")
        try:
            self.worker.stop()
        except Exception:
            logger.exception("Error stopping worker")
        # Hide the icon up-front so the user sees the tray go away even if
        # threads take a moment to settle.
        try:
            self.setVisible(False)
        except Exception:
            pass
        # These threads block in subprocess.run, so quit() can't interrupt
        # them – just bound the wait.
        for t in list(self._bg_threads):
            if t.isRunning():
                t.wait(500)
        QThreadPool.globalInstance().waitForDone(500)
