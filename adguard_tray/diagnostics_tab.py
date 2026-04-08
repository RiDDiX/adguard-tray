"""
Diagnostics tab for the Manager window.

Features:
  - Export logs (adguard-cli export-logs)
  - Export settings (adguard-cli export-settings)
  - Import settings (adguard-cli import-settings)
  - Run speed benchmark (adguard-cli speed --json)
  - View application log file
"""

import logging

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .cli import AdGuardCLI
from .i18n import _t
from .main import LOG_FILE

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


class DiagnosticsTab(QWidget):
    def __init__(self, cli: AdGuardCLI, on_restart=None, parent=None) -> None:
        super().__init__(parent)
        self.cli = cli
        self._on_restart = on_restart
        self._workers: list[QThread] = []
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Export / Import
        grp_export = QGroupBox(_t("Export & Import"))
        el = QVBoxLayout(grp_export)

        btn_row1 = QHBoxLayout()
        self.btn_export_logs = QPushButton(_t("Export logs…"))
        self.btn_export_logs.setToolTip(_t("Export AdGuard CLI logs to a zip file"))
        self.btn_export_logs.clicked.connect(self._export_logs)
        btn_row1.addWidget(self.btn_export_logs)

        self.btn_export_settings = QPushButton(_t("Export settings…"))
        self.btn_export_settings.setToolTip(_t("Export all AdGuard CLI settings to a zip file"))
        self.btn_export_settings.clicked.connect(self._export_settings)
        btn_row1.addWidget(self.btn_export_settings)

        self.btn_import_settings = QPushButton(_t("Import settings…"))
        self.btn_import_settings.setToolTip(_t("Import settings from a previously exported zip file"))
        self.btn_import_settings.clicked.connect(self._import_settings)
        btn_row1.addWidget(self.btn_import_settings)

        btn_row1.addStretch()
        el.addLayout(btn_row1)
        layout.addWidget(grp_export)

        # Benchmark
        grp_bench = QGroupBox(_t("Performance Benchmark"))
        bl = QVBoxLayout(grp_bench)
        bench_info = QLabel(_t(
            "<small>Run a cryptographic and HTTPS filtering benchmark.</small>"
        ))
        bench_info.setTextFormat(Qt.TextFormat.RichText)
        bench_info.setWordWrap(True)
        bl.addWidget(bench_info)

        self.btn_benchmark = QPushButton(_t("Run benchmark"))
        self.btn_benchmark.clicked.connect(self._run_benchmark)
        bl.addWidget(self.btn_benchmark)
        layout.addWidget(grp_bench)

        # Result area
        self.lbl_status = QLabel("")
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumHeight(200)
        self.output.hide()
        layout.addWidget(self.output)

        # App log viewer
        grp_log = QGroupBox(_t("Application Log"))
        ll = QVBoxLayout(grp_log)

        log_path_lbl = QLabel(f"<small><code>{LOG_FILE}</code></small>")
        log_path_lbl.setTextFormat(Qt.TextFormat.RichText)
        log_path_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        ll.addWidget(log_path_lbl)

        self.btn_view_log = QPushButton(_t("View recent log entries"))
        self.btn_view_log.clicked.connect(self._view_log)
        ll.addWidget(self.btn_view_log)

        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumHeight(200)
        self.log_view.hide()
        ll.addWidget(self.log_view)
        layout.addWidget(grp_log)

        layout.addStretch()

    def _set_busy(self, busy: bool) -> None:
        for btn in (self.btn_export_logs, self.btn_export_settings,
                    self.btn_import_settings, self.btn_benchmark):
            btn.setEnabled(not busy)

    def _run_action(self, fn, show_output: bool = False) -> None:
        self._set_busy(True)
        self.output.hide()
        w = _Worker(fn)

        def _done(ok, msg):
            self._set_busy(False)
            self.lbl_status.setText(msg if not show_output else (_t("Done.") if ok else _t("Failed.")))
            if show_output and msg:
                self.output.setPlainText(msg)
                self.output.show()

        w.done.connect(_done)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _export_logs(self) -> None:
        path = QFileDialog.getExistingDirectory(self, _t("Export logs to…"))
        if not path:
            return
        self.lbl_status.setText(_t("Exporting logs…"))
        self._run_action(lambda: self.cli.export_logs(path))

    def _export_settings(self) -> None:
        path = QFileDialog.getExistingDirectory(self, _t("Export settings to…"))
        if not path:
            return
        self.lbl_status.setText(_t("Exporting settings…"))
        self._run_action(lambda: self.cli.export_settings(path))

    def _import_settings(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, _t("Import settings from…"), "", _t("Zip files (*.zip);;All files (*)")
        )
        if not path:
            return
        self.lbl_status.setText(_t("Importing settings…"))

        def _do():
            ok, msg = self.cli.import_settings(path)
            return ok, msg

        self._run_action(_do)

    def _run_benchmark(self) -> None:
        self.lbl_status.setText(_t("Running benchmark…"))
        self._run_action(self.cli.run_speed_benchmark, show_output=True)

    def _view_log(self) -> None:
        try:
            if LOG_FILE.exists():
                text = LOG_FILE.read_text(encoding="utf-8", errors="replace")
                # Show last 100 lines
                lines = text.splitlines()
                tail = "\n".join(lines[-100:])
                self.log_view.setPlainText(tail)
                self.log_view.show()
                # Scroll to bottom
                cursor = self.log_view.textCursor()
                cursor.movePosition(cursor.MoveOperation.End)
                self.log_view.setTextCursor(cursor)
            else:
                self.lbl_status.setText(_t("Log file not found."))
        except OSError as exc:
            self.lbl_status.setText(_t("Error: {}", str(exc)))
