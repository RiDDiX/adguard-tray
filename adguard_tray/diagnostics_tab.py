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

from PyQt6.QtCore import Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
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


class _QuicWorker(QThread):
    """Reads proxy.yaml, browser policies and profiles – all off the GUI thread."""
    done = pyqtSignal(object)

    def __init__(self, cli):
        super().__init__()
        self.cli = cli

    def run(self):
        from .cli import AdGuardStatus
        from .quic import status
        try:
            running = self.cli.get_status().status == AdGuardStatus.ACTIVE
            self.done.emit(status(running=running))
        except Exception:
            logger.exception("QUIC check failed")
            self.done.emit(None)


class DiagnosticsTab(QWidget):
    def __init__(self, cli: AdGuardCLI, on_restart=None, parent=None) -> None:
        super().__init__(parent)
        self.cli = cli
        self._on_restart = on_restart
        self._workers: list[QThread] = []
        self._quic_state = None
        self._build_ui()
        QTimer.singleShot(0, self._check_quic)

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

        # HTTP/3 (QUIC)
        grp_quic = QGroupBox(_t("HTTP/3 (QUIC)"))
        ql = QVBoxLayout(grp_quic)
        quic_info = QLabel("<small>" + _t(
            "Browsers prefer HTTP/3 over UDP port 443. AdGuard only sees that "
            "traffic in <i>auto</i> proxy mode; otherwise those requests reach "
            "the site directly and are not filtered."
        ) + "</small>")
        quic_info.setTextFormat(Qt.TextFormat.RichText)
        quic_info.setWordWrap(True)
        ql.addWidget(quic_info)

        self.lbl_quic = QLabel(_t("Checking…"))
        self.lbl_quic.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_quic.setWordWrap(True)
        ql.addWidget(self.lbl_quic)

        quic_row = QHBoxLayout()
        self.btn_quic_check = QPushButton(_t("↺ Re-check"))
        self.btn_quic_check.clicked.connect(self._check_quic)
        quic_row.addWidget(self.btn_quic_check)

        self.btn_quic_firefox = QPushButton(_t("Disable HTTP/3 in Firefox profiles"))
        self.btn_quic_firefox.clicked.connect(self._toggle_firefox_http3)
        self.btn_quic_firefox.hide()
        quic_row.addWidget(self.btn_quic_firefox)
        quic_row.addStretch()
        ql.addLayout(quic_row)
        layout.addWidget(grp_quic)

        # Benchmark
        grp_bench = QGroupBox(_t("Performance Benchmark"))
        bl = QVBoxLayout(grp_bench)
        bench_info = QLabel("<small>" + _t(
            "Run a cryptographic and HTTPS filtering benchmark."
        ) + "</small>")
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
                    self.btn_import_settings, self.btn_benchmark,
                    self.btn_quic_check, self.btn_quic_firefox):
            btn.setEnabled(not busy)

    # ── HTTP/3 (QUIC) ─────────────────────────────────────────────────────

    def _check_quic(self) -> None:
        self.lbl_quic.setText(_t("Checking…"))
        w = _QuicWorker(self.cli)
        w.done.connect(self._on_quic_checked)
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_quic_checked(self, state: object) -> None:
        if state is None:
            self.lbl_quic.setText(_t("Error: {}", _t("HTTP/3 state unknown")))
            return
        self._quic_state = state
        mark = "✅" if state.filtered else "⚠️"
        lines = [f"{mark} <b>{state.headline}</b>", *state.details]
        self.lbl_quic.setText("<small>" + "<br>".join(lines) + "</small>")

        if state.firefox_profiles:
            all_off = state.firefox_disabled == len(state.firefox_profiles)
            self.btn_quic_firefox.setText(
                _t("Re-enable HTTP/3 in Firefox profiles") if all_off
                else _t("Disable HTTP/3 in Firefox profiles")
            )
            self.btn_quic_firefox.show()
        else:
            self.btn_quic_firefox.hide()

    def _toggle_firefox_http3(self) -> None:
        from .quic import set_firefox_http3
        state = getattr(self, "_quic_state", None)
        if not state or not state.firefox_profiles:
            return
        enable = state.firefox_disabled == len(state.firefox_profiles)
        if not enable:
            reply = QMessageBox.question(
                self, _t("HTTP/3 (QUIC)"),
                _t("Switch HTTP/3 off in {} Firefox-family profile(s)?\n\n"
                   "Their traffic then uses HTTP/2, which AdGuard can filter. "
                   "Restart the browser afterwards.", len(state.firefox_profiles)),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        failed = []
        for profile in state.firefox_profiles:
            ok, err = set_firefox_http3(profile, enable)
            if not ok:
                failed.append(f"{profile.name}: {err}")
        if failed:
            self.lbl_status.setText(_t("Error: {}", "; ".join(failed)[:200]))
        else:
            self.lbl_status.setText(
                _t("HTTP/3 re-enabled in Firefox profiles – restart the browser.") if enable
                else _t("HTTP/3 switched off in Firefox profiles – restart the browser.")
            )
        self._check_quic()

    def _run_action(self, fn, show_output: bool = False, on_done=None) -> None:
        self._set_busy(True)
        self.output.hide()
        w = _Worker(fn)

        def _done(ok, msg):
            self._set_busy(False)
            self.lbl_status.setText(msg if not show_output else (_t("Done.") if ok else _t("Failed.")))
            if show_output and msg:
                self.output.setPlainText(msg)
                self.output.show()
            if on_done:
                on_done(ok, msg)

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

        def _on_import_done(ok, msg):
            if ok and self._on_restart:
                self._on_restart()

        self._run_action(_do, on_done=_on_import_done)

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
