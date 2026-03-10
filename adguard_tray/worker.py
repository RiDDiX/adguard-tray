"""
Background status polling.

Architecture:
  - StatusWorker lives in the main thread and owns a QTimer.
  - Each tick launches a _StatusRunnable on the global QThreadPool.
  - The runnable emits a pyqtSignal back to the main thread via Qt's
    queued connection – no manual mutex needed.
  - UI is never blocked: subprocess.run() happens off the main thread.
"""

import logging

from PyQt6.QtCore import (
    QObject,
    QRunnable,
    QThreadPool,
    QTimer,
    pyqtSignal,
    pyqtSlot,
)

from .cli import AdGuardCLI, StatusResult

logger = logging.getLogger(__name__)


class _Signals(QObject):
    result = pyqtSignal(object)  # StatusResult


class _StatusRunnable(QRunnable):
    def __init__(self, cli: AdGuardCLI) -> None:
        super().__init__()
        self.cli = cli
        self.signals = _Signals()
        self.setAutoDelete(True)

    @pyqtSlot()
    def run(self) -> None:
        try:
            result = self.cli.get_status()
        except Exception as exc:  # safety net – should never happen
            logger.exception("Unexpected error in status runnable: %s", exc)
            from .cli import AdGuardStatus
            result = StatusResult(AdGuardStatus.ERROR, str(exc))
        self.signals.result.emit(result)


class StatusWorker(QObject):
    """
    Polls adguard-cli status periodically without blocking the main thread.

    Signals:
        status_updated(StatusResult)  – emitted after each status check
    """

    status_updated = pyqtSignal(object)  # StatusResult

    def __init__(self, cli: AdGuardCLI, interval_seconds: int = 30) -> None:
        super().__init__()
        self.cli = cli
        self._interval = max(5, interval_seconds)
        self._pool = QThreadPool.globalInstance()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._enqueue)
        self._running = False

    # ── Public API ─────────────────────────────────────────────────────────

    def start(self) -> None:
        self._running = True
        self._enqueue()                         # immediate first check
        self._timer.start(self._interval * 1000)
        logger.debug("StatusWorker started, interval=%ds", self._interval)

    def stop(self) -> None:
        self._running = False
        self._timer.stop()
        logger.debug("StatusWorker stopped")

    def refresh(self) -> None:
        """Force an immediate out-of-band status check."""
        logger.debug("Manual refresh requested")
        self._enqueue()

    def set_interval(self, seconds: int) -> None:
        self._interval = max(5, seconds)
        if self._running:
            self._timer.start(self._interval * 1000)
        logger.debug("Polling interval updated to %ds", self._interval)

    # ── Internal ───────────────────────────────────────────────────────────

    def _enqueue(self) -> None:
        runnable = _StatusRunnable(self.cli)
        runnable.signals.result.connect(self.status_updated)
        self._pool.start(runnable)
