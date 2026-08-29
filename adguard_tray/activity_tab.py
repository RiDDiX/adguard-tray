"""Activity tab – what AdGuard actually did, read from its access log.

The access log is the only per-request record adguard-cli keeps, so this tab
shows what can be read from it and says plainly when it cannot be read.
"""

import logging

from PyQt6.QtCore import Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .i18n import _t

logger = logging.getLogger(__name__)

COL_TIME, COL_DOMAIN, COL_RESULT, COL_RULE, COL_SIZE, COL_MS = range(6)
MAX_ROWS = 500          # what the table shows; the counters use every line read
HOURS = 24
_BLOCKS = "▁▂▃▄▅▆▇█"


class _ActivityWorker(QThread):
    """Reads and parses the access log off the GUI thread."""
    done = pyqtSignal(object)

    def run(self):
        from .stats import read_activity
        try:
            self.done.emit(read_activity())
        except Exception:
            logger.exception("Reading the access log failed")
            self.done.emit(None)


class ActivityTab(QWidget):
    def __init__(self, on_change=None, parent=None) -> None:
        super().__init__(parent)
        self._on_change = on_change
        self._workers: list[QThread] = []
        self._activity = None
        self._build_ui()
        QTimer.singleShot(0, self.refresh)

    # ── UI ─────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        self.lbl_summary = QLabel(_t("Reading the access log…"))
        self.lbl_summary.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_summary.setWordWrap(True)
        layout.addWidget(self.lbl_summary)

        self.lbl_timeline = QLabel("")
        self.lbl_timeline.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_timeline.setVisible(False)
        layout.addWidget(self.lbl_timeline)

        self.lbl_problem = QLabel("")
        self.lbl_problem.setWordWrap(True)
        self.lbl_problem.setVisible(False)
        layout.addWidget(self.lbl_problem)

        row = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(_t("Filter by domain or rule…"))
        self.search_box.textChanged.connect(self._apply_filter)
        row.addWidget(self.search_box)

        self.chk_blocked = QCheckBox(_t("Blocked only"))
        self.chk_blocked.stateChanged.connect(self._apply_filter)
        row.addWidget(self.chk_blocked)

        self.btn_refresh = QPushButton(_t("Refresh"))
        self.btn_refresh.clicked.connect(self.refresh)
        row.addWidget(self.btn_refresh)
        layout.addLayout(row)

        body = QHBoxLayout()
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            _t("Time"), _t("Domain"), _t("Result"), _t("Rule"), _t("Size"), _t("Time (ms)"),
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(COL_RULE, QHeaderView.ResizeMode.Stretch)
        body.addWidget(self.table, 3)

        self.top_table = QTableWidget(0, 2)
        self.top_table.setHorizontalHeaderLabels([_t("Top blocked domains"), _t("Count")])
        self.top_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.top_table.verticalHeader().setVisible(False)
        self.top_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        body.addWidget(self.top_table, 2)
        layout.addLayout(body)

        actions = QHBoxLayout()
        actions.addStretch()
        self.btn_allow = QPushButton(_t("Allow selected domain"))
        self.btn_allow.clicked.connect(lambda: self._add_rule(allow=True))
        actions.addWidget(self.btn_allow)
        self.btn_block = QPushButton(_t("Block selected domain"))
        self.btn_block.clicked.connect(lambda: self._add_rule(allow=False))
        actions.addWidget(self.btn_block)
        layout.addLayout(actions)

    # ── Loading ────────────────────────────────────────────────────────────

    def refresh(self) -> None:
        self.btn_refresh.setEnabled(False)
        worker = _ActivityWorker()
        worker.done.connect(self._on_loaded)
        worker.finished.connect(lambda: self._workers.remove(worker) if worker in self._workers else None)
        self._workers.append(worker)
        worker.start()

    def _on_loaded(self, activity) -> None:
        self.btn_refresh.setEnabled(True)
        self._activity = activity
        if activity is None:
            self.lbl_summary.setText(_t("Could not read the access log."))
            return

        self.lbl_problem.setVisible(bool(activity.problem))
        self.lbl_problem.setText(activity.problem)

        if activity.problem and not activity.total:
            self.lbl_summary.setText(_t("No activity to show."))
            self.table.setRowCount(0)
            self.top_table.setRowCount(0)
            self.lbl_timeline.setVisible(False)
            return

        summary = _t("{} requests · {} blocked · {} allowed",
                     activity.total, activity.blocked, activity.allowed)
        if activity.unparsed:
            summary += " · " + _t("{} lines not understood", activity.unparsed)
        self.lbl_summary.setText(
            "<b>" + summary + "</b><br><small>" +
            _t("Source: {}", str(activity.log_path or "")) + "</small>")

        self._fill_timeline(activity)
        self._fill_top(activity)
        self._fill_table(activity)

    def _fill_timeline(self, activity) -> None:
        """Requests per hour as bars – a chart without a charting dependency."""
        hours = activity.per_hour(limit=HOURS)
        self.lbl_timeline.setVisible(bool(hours))
        if not hours:
            return
        peak = max(total for _, total, _ in hours)
        scale = len(_BLOCKS) - 1
        bars = "".join(
            _BLOCKS[0] if not total else _BLOCKS[max(1, round(total * scale / peak))]
            for _, total, _ in hours
        )
        self.lbl_timeline.setToolTip("\n".join(
            f"{hour.strftime('%d.%m. %H:%M')}  {total}  ({blocked} " + _t("Blocked") + ")"
            for hour, total, blocked in hours))
        self.lbl_timeline.setText(
            "<span style='font-family:monospace;font-size:14pt'>" + bars + "</span>"
            + "<br><small>" + _t("Requests per hour, {} to {} · busiest hour: {}",
                                 hours[0][0].strftime("%d.%m. %H:%M"),
                                 hours[-1][0].strftime("%d.%m. %H:%M"), peak)
            + "</small>")

    def _fill_top(self, activity) -> None:
        top = activity.top_hosts(limit=15, blocked_only=True)
        # Without a single blocked request "top blocked" would be a lie.
        self.top_table.setHorizontalHeaderLabels(
            [_t("Top blocked domains") if top else _t("Top domains"), _t("Count")])
        top = top or activity.top_hosts(limit=15)
        self.top_table.setRowCount(len(top))
        for row, (host, count) in enumerate(top):
            self.top_table.setItem(row, 0, QTableWidgetItem(host))
            self.top_table.setItem(row, 1, QTableWidgetItem(str(count)))

    def _fill_table(self, activity) -> None:
        requests = list(reversed(activity.requests))[:MAX_ROWS]
        self.table.setRowCount(len(requests))
        for row, req in enumerate(requests):
            when = req.when.strftime("%d.%m. %H:%M:%S") if req.when else ""
            result = _t("Blocked") if req.blocked else (
                _t("Allowed by rule") if req.allowed_by_rule else _t("Allowed"))
            for col, text in (
                (COL_TIME, when),
                (COL_DOMAIN, req.host),
                (COL_RESULT, result),
                (COL_RULE, req.rule),
                (COL_SIZE, _format_size(req.size)),
                (COL_MS, str(req.duration_ms) if req.duration_ms >= 0 else ""),
            ):
                item = QTableWidgetItem(text)
                item.setToolTip(req.url or req.raw)
                # The filter must not depend on the translated result text.
                item.setData(Qt.ItemDataRole.UserRole, req.blocked)
                self.table.setItem(row, col, item)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(COL_RULE, QHeaderView.ResizeMode.Stretch)
        self._apply_filter()

    def _apply_filter(self) -> None:
        needle = self.search_box.text().strip().lower()
        blocked_only = self.chk_blocked.isChecked()
        for row in range(self.table.rowCount()):
            domain = self.table.item(row, COL_DOMAIN)
            rule = self.table.item(row, COL_RULE)
            haystack = f"{domain.text() if domain else ''} {rule.text() if rule else ''}".lower()
            hide = bool(needle) and needle not in haystack
            if blocked_only and not (domain and domain.data(Qt.ItemDataRole.UserRole)):
                hide = True
            self.table.setRowHidden(row, hide)

    # ── Actions ────────────────────────────────────────────────────────────

    def _selected_domain(self) -> str:
        row = self.table.currentRow()
        if row < 0 or self.table.isRowHidden(row):
            return ""
        item = self.table.item(row, COL_DOMAIN)
        return item.text() if item else ""

    def _add_rule(self, allow: bool) -> None:
        from ._allowlist import (
            add_rule_line,
            domain_to_rule,
            is_valid_domain,
            load_user_rules,
            save_user_rules,
        )

        domain = self._selected_domain()
        if not domain:
            QMessageBox.information(self, _t("Activity"), _t("Select a request first."))
            return
        if not is_valid_domain(domain):
            QMessageBox.warning(self, _t("Activity"), _t("Not a valid domain: {}", domain))
            return

        if allow:
            try:
                domains, other = load_user_rules()
            except (OSError, ValueError) as exc:
                QMessageBox.critical(self, _t("Activity"), str(exc))
                return
            if domain in domains:
                ok, err = True, ""
            else:
                ok, err = save_user_rules(domains + [domain], other, loaded=domains)
            rule = domain_to_rule(domain)
        else:
            rule = f"||{domain}^"
            ok, err = add_rule_line(rule)

        if not ok:
            QMessageBox.critical(self, _t("Activity"), err)
            return
        QMessageBox.information(
            self, _t("Activity"),
            _t("Added rule: {}", rule) + "\n\n" + _t("Restart AdGuard to apply changes."))
        if self._on_change:
            self._on_change()


def _format_size(size: int) -> str:
    if size < 0:
        return ""
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.1f} MB"
