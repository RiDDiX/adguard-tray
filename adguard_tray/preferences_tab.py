"""Settings – adguard-tray's own options (config.json). Every change is saved at once."""

import logging
import os
import shlex
import shutil
import subprocess
import time

from PyQt6.QtCore import QThread, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication, QComboBox, QFileDialog, QLineEdit, QPushButton, QSpinBox

from . import installer, theme, ui
from .autostart import autostart_enabled, set_autostart
from .config import save_config
from .i18n import LANGUAGES, _t
from .ui import Page, Row, Switch
from .worker import FnWorker

logger = logging.getLogger(__name__)

_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")
POLL_MS = 3000          # boot service state while the user types the password
POLL_FOR = 120          # seconds


def _looks_like_adguard_cli(path: str) -> bool:
    try:
        r = subprocess.run([path, "--version"], capture_output=True, stdin=subprocess.DEVNULL, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return False
    out = (r.stdout + r.stderr).decode("utf-8", errors="replace").lower()
    return "adguard cli" in out


def _password_hint() -> str:
    return _t("AdGuard CLI asks for your password in the terminal window.")


def _quietly(widget, setter, value) -> None:
    """Put a control back without firing its change signal again."""
    widget.blockSignals(True)
    setter(value)
    widget.blockSignals(False)


class _ProbeWorker(QThread):
    done = pyqtSignal(str, bool)

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

    def run(self) -> None:
        try:
            ok = _looks_like_adguard_cli(self.path)
        except Exception:
            logger.exception("Could not run %s --version", self.path)
            ok = False
        self.done.emit(self.path, ok)


class PreferencesTab(Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(parent=parent)
        self.ctx = ctx
        cfg = ctx.config
        self._workers: list[QThread] = []
        restart_note = _t("Applies after AdGuard Tray restarts.")

        look = self.section(_t("Appearance"))
        self.combo_theme = self._add_combo(
            look, "appearance", cfg.appearance if cfg.appearance in theme.APPEARANCES else "",
            _t("Theme"), _t("“Follow system” uses your desktop's light or dark setting."),
            [(_t("Follow system"), ""), (_t("Light"), "light"), (_t("Dark"), "dark")],
            theme.set_appearance)
        self.combo_language = self._add_combo(
            look, "language", cfg.language, _t("Language"), restart_note,
            [(_t("Automatic"), "")] + [(name, code) for code, name in LANGUAGES.items()],
            lambda _code: self._saved_for_restart())

        notify_card = self.section(_t("Notifications"))
        self.sw_notify = Switch()
        self.sw_notify.setChecked(cfg.notifications_enabled)
        self.sw_notify.toggled.connect(lambda on: self._commit(
            "notifications_enabled", on, lambda: _quietly(self.sw_notify, self.sw_notify.setChecked, not on)))
        notify_card.add_row(Row(
            _t("Notify me when protection turns on or off"),
            _t("Also on restarts and errors. Needs notify-send (libnotify) or a running "
               "notification service such as dunst, mako or KDE's."),
            self.sw_notify))

        startup = self.section(_t("Startup"))
        self.sw_autostart = Switch()
        self.sw_autostart.setChecked(autostart_enabled())
        self.sw_autostart.toggled.connect(self._set_autostart)
        startup.add_row(Row(_t("Start AdGuard Tray when I log in"),
                            _t("Uses XDG autostart (~/.config/autostart)."), self.sw_autostart))
        self.sw_boot = Switch()
        self.sw_boot.toggled.connect(self._set_boot)
        self.boot_row = startup.add_row(Row(
            _t("Start AdGuard CLI at boot"),
            _t("Uses the system service that adguard-cli installs itself. "
               "Asks for your password in a terminal window."),
            self.sw_boot))
        self.boot_row.setHidden(not shutil.which("systemctl"))
        self._boot_worker: FnWorker | None = None
        self._boot_want = False
        self._boot_end = 0.0
        self._boot_poll = QTimer(self)
        self._boot_poll.timeout.connect(self._sync_boot)
        self._sync_boot()

        checks = self.section(_t("Status checks"))
        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(5, 300)
        self.spin_interval.setSingleStep(5)
        self.spin_interval.setSuffix(_t(" seconds"))
        self.spin_interval.setValue(cfg.refresh_interval)
        # Typing "120" must not save 12 on the way.
        self.spin_interval.setKeyboardTracking(False)
        self.spin_interval.valueChanged.connect(self._set_interval)
        ui.ignore_idle_wheel(self.spin_interval)   # every step is saved at once
        self._interval = self.spin_interval.value()
        checks.add_row(Row(_t("Check every"), _t("How often adguard-cli status is checked automatically."),
                           self.spin_interval))

        advanced = self.section(_t("Advanced"))
        self.combo_log = self._add_combo(
            advanced, "log_level", cfg.log_level.upper(), _t("Log level:").rstrip(":："),
            _t("How much detail AdGuard Tray writes to its own log."),
            [(level, level) for level in _LOG_LEVELS],
            lambda level: logging.getLogger().setLevel(getattr(logging, level, logging.INFO)))

        self.edit_cli = QLineEdit(cfg.adguard_cli_path)
        self.edit_cli.setPlaceholderText(_t("auto-detect via PATH"))
        self.edit_cli.setMinimumWidth(240)
        self.edit_cli.editingFinished.connect(lambda: self._commit_cli(self.edit_cli.text().strip()))
        self.btn_browse = QPushButton(_t("Browse…"))
        self.btn_browse.setAccessibleName(self.btn_browse.text())
        self.btn_browse.clicked.connect(self._browse_cli)
        self.cli_spinner = ui.Spinner()
        cli_row = advanced.add_row(Row(_t("adguard-cli path:").rstrip(":："), restart_note, self.edit_cli))
        cli_row.add_control(self.btn_browse)
        cli_row.add_control(self.cli_spinner)
        self._checking = False

        self.finish()


    def on_shown(self) -> None:
        # The desktop's own autostart settings may have changed the entry.
        _quietly(self.sw_autostart, self.sw_autostart.setChecked, autostart_enabled())
        if not self._boot_poll.isActive():     # mid-install it would flip the switch back
            self._sync_boot()

    # ── Saving ─────────────────────────────────────────────────────────────

    def _commit(self, field: str, value, undo) -> bool:
        """Save one config.json field; if that fails, put it and its control back."""
        cfg = self.ctx.config
        old = getattr(cfg, field)
        setattr(cfg, field, value)
        ok, err = save_config(cfg)
        if not ok:
            setattr(cfg, field, old)
            undo()
            self.banner.show_message(_t("Could not save the settings."), "danger", details=err)
            return False
        if self.ctx.on_config_change:
            self.ctx.on_config_change()
        return True

    def _add_combo(self, card, field, current, title, subtitle, choices, apply) -> QComboBox:
        combo = QComboBox()
        for label, value in choices:
            combo.addItem(label, value)
        if combo.findData(current) < 0:     # a hand-edited value: show it as it is
            combo.addItem(current, current)
        combo.setCurrentIndex(combo.findData(current))
        last = [combo.currentIndex()]

        def changed(index: int) -> None:
            value = combo.currentData()
            if self._commit(field, value, lambda: _quietly(combo, combo.setCurrentIndex, last[0])):
                last[0] = index
                apply(value)
        combo.currentIndexChanged.connect(changed)
        ui.ignore_idle_wheel(combo)
        card.add_row(Row(title, subtitle, combo))
        return combo

    def _saved_for_restart(self) -> None:
        self.banner.show_message(_t("Saved. Applies after AdGuard Tray restarts."), "success",
                                 timeout_ms=5000)

    def _set_interval(self, seconds: int) -> None:
        old = self._interval
        if self._commit("refresh_interval", seconds,
                        lambda: _quietly(self.spin_interval, self.spin_interval.setValue, old)):
            self._interval = seconds

    def _set_autostart(self, on: bool) -> None:
        ok, err = set_autostart(on, self.ctx.exec_path)
        if not ok:
            _quietly(self.sw_autostart, self.sw_autostart.setChecked, autostart_enabled())
            self.banner.show_message(_t("Could not change the autostart entry."), "danger", details=err)

    # ── adguard-cli boot service ───────────────────────────────────────────

    def _set_boot(self, on: bool) -> None:
        # install-service runs sudo itself, which needs a terminal; its exit code says nothing.
        command = shlex.join(self.ctx.cli.service_command(on))
        if not installer.open_in_terminal(command):
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText(command)
            self.banner.show_message(
                _t("No terminal app was found. The command is on the clipboard: paste it into a terminal."),
                "warning", details=command)
            _quietly(self.sw_boot, self.sw_boot.setChecked, not on)
            return
        self.banner.show_message(_password_hint(), "info", details=command)
        # A second terminal before the first one is done would race it.
        self.sw_boot.setEnabled(False)
        self._boot_want = on
        self._boot_end = time.monotonic() + POLL_FOR
        self._boot_poll.start(POLL_MS)

    def _sync_boot(self) -> None:
        if self._boot_worker is not None or self.boot_row.isHidden():
            return
        self.sw_boot.setEnabled(False)      # until the read shows the real state
        w = self._boot_worker = FnWorker(lambda: (self.ctx.cli.service_enabled(), ""))
        w.done.connect(self._boot_read)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _boot_read(self, on: bool, _msg: str) -> None:
        self._boot_worker = None
        if self._boot_poll.isActive():
            if on != self._boot_want and time.monotonic() < self._boot_end:
                return
            self._boot_poll.stop()
            if self.banner.text.text() == _password_hint():     # done, or nobody typed one in time
                self.banner.hide()
        _quietly(self.sw_boot, self.sw_boot.setChecked, on)
        self.sw_boot.setEnabled(True)

    # ── adguard-cli path ───────────────────────────────────────────────────

    def _browse_cli(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, _t("Select adguard-cli binary"), "/usr/local/bin")
        if path:
            self.edit_cli.setText(path)
            self._commit_cli(path)

    def _commit_cli(self, path: str) -> None:
        # A confirmation dialog takes the focus away, which fires editingFinished again.
        if self._checking or path == self.ctx.config.adguard_cli_path:
            return
        if not path:
            self._save_cli(path)
        elif not (os.path.isfile(path) and os.access(path, os.X_OK)):
            self._confirm_cli(path, _t("adguard-cli path does not exist or is not executable."))
        else:
            self._set_checking(True)
            w = _ProbeWorker(path)
            w.done.connect(self._on_probe)
            w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
            self._workers.append(w)
            w.start()

    def _on_probe(self, path: str, ok: bool) -> None:
        self._set_checking(False)
        if ok:
            self._save_cli(path)
        else:
            self._confirm_cli(path, _t("That binary does not identify as adguard-cli. Save anyway?"))

    def _confirm_cli(self, path: str, text: str) -> None:
        # Closed while probing, or the close itself ended the edit: nobody to ask.
        # (isVisible() is still true while Qt hides the window, and closing
        # first gives the window itself the focus to commit open edits.)
        if self.window().isHidden() or QApplication.focusWidget() is self.window():
            self._revert_cli()
            return
        self._checking = True
        try:
            go = ui.confirm(self, _t("Save adguard-cli path"), text, _t("Save anyway"))
        finally:
            self._checking = False
        if go:
            self._save_cli(path)
        else:
            self._revert_cli()

    def _set_checking(self, busy: bool) -> None:
        self._checking = busy
        self.edit_cli.setEnabled(not busy)
        self.btn_browse.setEnabled(not busy)
        self.cli_spinner.set_busy(busy)

    def _save_cli(self, path: str) -> None:
        self.edit_cli.setText(path)
        if self._commit("adguard_cli_path", path, self._revert_cli):
            self._saved_for_restart()

    def _revert_cli(self) -> None:
        self.edit_cli.setText(self.ctx.config.adguard_cli_path)
