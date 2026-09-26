"""Maintenance page: export and import AdGuard's settings, logs, benchmark."""

import json
import logging
import zipfile
from pathlib import Path

from PyQt6.QtCore import QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QFileDialog, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget

from . import ui
from .i18n import _t
from .main import LOG_FILE
from .network_tab import open_folder
from .ui import Page, Row, Spinner

logger = logging.getLogger(__name__)


class _Worker(QThread):
    done = pyqtSignal(bool, str)

    def __init__(self, fn):
        super().__init__()
        self._fn = fn

    def run(self):
        try:
            ok, msg = self._fn()
        except Exception as exc:
            ok, msg = False, str(exc)
        self.done.emit(ok, msg)


def _pretty(text: str) -> str:
    try:
        return json.dumps(json.loads(text), indent=2, ensure_ascii=False)
    except ValueError:
        return text      # not JSON, or cut short by the CLI wrapper


def _button(label: str, about: str, slot) -> QPushButton:
    button = QPushButton(label)
    button.setAccessibleName(label)          # a Row would name it after its title
    button.setAccessibleDescription(about)
    button.clicked.connect(slot)
    return button


class DiagnosticsTab(Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(parent=parent)
        self.ctx = ctx
        self.cli = ctx.cli
        self._workers: list[QThread] = []
        self._actions: list[QPushButton] = []

        io = self.section(_t("Export and import"))
        self.btn_export_settings, self.btn_import_settings, self.spin_settings = self._action_row(
            io, _t("AdGuard settings"),
            _t("Save filters, rules and configuration to a zip file, or load them from one."),
            (_t("Export…"), self._export_settings), (_t("Import…"), self._import_settings))
        self.btn_export_settings.setAccessibleName(_t("Export settings…"))
        self.btn_import_settings.setAccessibleName(_t("Import settings…"))

        logs = self.section(_t("Logs"))
        self.btn_export_logs, self.spin_export_logs = self._action_row(
            logs, _t("AdGuard CLI logs"), _t("Export AdGuard CLI logs to a zip file"),
            (_t("Export…"), self._export_logs))
        self.btn_export_logs.setAccessibleName(_t("Export logs…"))
        tray_log = _t("AdGuard Tray log")
        log_row = logs.add_row(Row(tray_log, str(LOG_FILE)))
        log_row.add_control(_button(_t("Show recent entries"), tray_log, self._view_log))
        log_row.add_control(_button(_t("Open folder"), tray_log, lambda: open_folder(self, LOG_FILE.parent)))
        self.log_view = self._viewer(logs, tray_log)

        perf = self.section(_t("Performance"))
        self.btn_benchmark, self.spin_benchmark = self._action_row(
            perf, _t("Benchmark"), _t("Run a cryptographic and HTTPS filtering benchmark."),
            (_t("Run benchmark"), self._run_benchmark))
        self.output = self._viewer(perf, _t("Benchmark"))

        self.finish()

    def _action_row(self, card, title: str, subtitle: str, *actions):
        """A row with a spinner and one button per (label, slot); returns the buttons, then the spinner."""
        row = card.add_row(Row(title, subtitle))
        spinner = row.add_control(Spinner())
        buttons = [row.add_control(_button(label, title, slot)) for label, slot in actions]
        self._actions += buttons
        return (*buttons, spinner)

    @staticmethod
    def _viewer(card, name: str) -> QPlainTextEdit:
        """A read-only text box under the card's last row, hidden until filled."""
        view = QPlainTextEdit()
        view.setReadOnly(True)
        view.setAccessibleName(name)
        view.setFont(QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont))
        view.setMinimumHeight(160)
        view.setMaximumHeight(260)
        box = QWidget()
        lay = QVBoxLayout(box)
        lay.setContentsMargins(14, 0, 12, 12)
        lay.addWidget(view)
        box.hide()
        card.add(box)
        view.box = box
        return view

    def _reveal(self, view: QPlainTextEdit) -> None:
        view.box.show()
        # After the layout has placed it.
        QTimer.singleShot(0, lambda: self.ensureWidgetVisible(view.box, 0, 0))

    # ── Running CLI calls ─────────────────────────────────────────────────

    def _set_busy(self, busy: bool) -> None:
        for btn in self._actions:
            btn.setEnabled(not busy)

    def _run_action(self, fn, spinner: Spinner, on_done) -> None:
        self._set_busy(True)
        spinner.set_busy(True)      # the row's spinner is the progress message
        self.banner.hide()
        w = _Worker(fn)

        def _done(ok, msg):
            self._set_busy(False)
            spinner.set_busy(False)
            on_done(ok, msg)

        w.done.connect(_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _report(self, ok: bool, msg: str, failed: str) -> None:
        if ok:
            self.banner.show_message(msg, "success", timeout_ms=5000)
        else:
            self.banner.show_message(failed, "danger", details="" if msg == failed else msg)

    # ── Export and import ─────────────────────────────────────────────────

    def _export_settings(self) -> None:
        path = QFileDialog.getExistingDirectory(self, _t("Export settings to…"))
        if not path:
            return
        self._run_action(lambda: self.cli.export_settings(path), self.spin_settings,
                         lambda ok, msg: self._report(ok, msg, _t("Could not export the settings.")))

    def _import_settings(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, _t("Import settings from…"), "", _t("Zip files (*.zip);;All files (*)")
        )
        if not path:
            return
        try:
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
        except (zipfile.BadZipFile, OSError) as exc:
            self.banner.show_message(_t("Could not read {}", path), "danger", details=str(exc))
            return
        # A logs export has the same file name and imports "successfully" too,
        # leaving a partial install behind.
        if not any(name.rsplit("/", 1)[-1] == "filters.yaml" for name in names):
            self.banner.show_message(_t("{} is not a settings export. Choose a file saved with "
                                        "Export under AdGuard settings.", Path(path).name), "warning")
            return
        if not ui.confirm(self, _t("Import settings"),
                          _t("Replace the current AdGuard settings with the ones in {}?\n\n"
                             "AdGuard restarts to apply them.", path),
                          _t("Import settings")):
            return

        def _done(ok, msg):
            if ok:
                # The import rewrote proxy.yaml: show it and drop edits made to the old one.
                self.ctx.settings.load()
                self.banner.show_message(self.ctx.restart_adguard(), "success", timeout_ms=5000)
            else:
                self._report(ok, msg, _t("Could not import the settings."))

        self._run_action(lambda: self.cli.import_settings(path), self.spin_settings, _done)

    # ── Logs ──────────────────────────────────────────────────────────────

    def _export_logs(self) -> None:
        path = QFileDialog.getExistingDirectory(self, _t("Export logs to…"))
        if not path:
            return
        self._run_action(lambda: self.cli.export_logs(path), self.spin_export_logs,
                         lambda ok, msg: self._report(ok, msg, _t("Could not export the logs.")))

    def _view_log(self) -> None:
        try:
            if not LOG_FILE.exists():
                self.log_view.box.hide()
                self.banner.show_message(_t("Log file not found."), "warning")
                return
            text = LOG_FILE.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            self.banner.show_message(_t("Could not read {}", str(LOG_FILE)), "danger", details=str(exc))
            return
        self.log_view.setPlainText("\n".join(text.splitlines()[-100:]))
        self._reveal(self.log_view)
        cursor = self.log_view.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_view.setTextCursor(cursor)

    # ── Benchmark ─────────────────────────────────────────────────────────

    def _run_benchmark(self) -> None:
        self.output.box.hide()

        def _done(ok, msg):
            if ok:
                self.banner.show_message(_t("Done."), "success", timeout_ms=5000)
                self.output.setPlainText(_pretty(msg))
                self._reveal(self.output)
            else:
                self._report(ok, msg, _t("Could not run the benchmark."))

        self._run_action(self.cli.run_speed_benchmark, self.spin_benchmark, _done)
