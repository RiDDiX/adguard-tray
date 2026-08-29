"""Activity tab – what AdGuard actually did, read from its access log.

The access log is the only per-request record adguard-cli keeps, so this tab
shows what can be read from it and says plainly when it cannot be read. The
layout follows AdGuard's own activity screens: counters at the top, a chart
over time, "most active" and "most blocked" beside each other, and the request
list underneath.
"""

import logging

from PyQt6.QtCore import QRectF, Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPalette
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .i18n import _t

logger = logging.getLogger(__name__)

COL_TIME, COL_DOMAIN, COL_RESULT, COL_RULE, COL_SIZE, COL_MS = range(6)
MAX_ROWS = 500          # what the table shows; the counters use every line read
TOP_N = 10

# Same palette as the tray icon, so blocked/allowed read the same everywhere.
BLOCKED_COLOR = "#dc2626"
ALLOWED_COLOR = "#16a34a"
TOTAL_LEGEND = "#7fa8d0"        # matches the translucent highlight the chart paints

# (label, hours of history, hours of chart)
RANGES = (
    (lambda: _t("Last 24 hours"), 24, 24),
    (lambda: _t("Last 7 days"), 24 * 7, 24 * 7),
    (lambda: _t("Everything in the log"), None, 24 * 7),
)


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


class _Card(QFrame):
    """One big number with a caption."""

    def __init__(self, caption: str, color: str = "", parent=None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        box = QVBoxLayout(self)
        box.setContentsMargins(12, 8, 12, 8)
        box.setSpacing(0)

        self.value = QLabel("–")
        font = self.value.font()
        font.setPointSizeF(font.pointSizeF() * 1.9)
        font.setBold(True)
        self.value.setFont(font)
        if color:
            self.value.setStyleSheet(f"color: {color};")
        box.addWidget(self.value)

        self.caption = QLabel(caption)
        self.caption.setEnabled(False)          # muted, palette-aware
        box.addWidget(self.caption)

    def set_value(self, text: str, hint: str = "") -> None:
        self.value.setText(text)
        self.setToolTip(hint)


class _BarChart(QWidget):
    """Requests per hour: total bars with the blocked share drawn over them."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._data: list = []
        self.setMinimumHeight(96)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(True)

    def set_data(self, data: list) -> None:
        self._data = list(data)
        self.setToolTip("")
        self.update()

    def _plot_rect(self) -> QRectF:
        return QRectF(self.rect().adjusted(0, 4, -1, -16))

    def _bar_width(self, plot: QRectF) -> tuple[float, float]:
        count = len(self._data)
        gap = 2.0 if count <= 48 else 1.0
        width = max(1.0, (plot.width() - gap * (count - 1)) / count)
        return width, gap

    def paintEvent(self, event) -> None:
        if not self._data:
            return
        painter = QPainter(self)
        plot = self._plot_rect()
        peak = max(total for _, total, _ in self._data) or 1
        width, gap = self._bar_width(plot)
        base = plot.bottom()
        total_color = self.palette().color(QPalette.ColorRole.Highlight)
        total_color.setAlpha(150)
        blocked_color = QColor(BLOCKED_COLOR)

        for index, (_hour, total, blocked) in enumerate(self._data):
            left = plot.left() + index * (width + gap)
            if total:
                height = max(2.0, total / peak * plot.height())
                painter.fillRect(QRectF(left, base - height, width, height), total_color)
            if blocked:
                height = max(2.0, blocked / peak * plot.height())
                painter.fillRect(QRectF(left, base - height, width, height), blocked_color)

        painter.setPen(self.palette().color(QPalette.ColorRole.Mid))
        painter.drawLine(int(plot.left()), int(base), int(plot.right()), int(base))

        painter.setPen(self.palette().color(QPalette.ColorRole.PlaceholderText))
        font = painter.font()
        font.setPointSizeF(max(7.0, font.pointSizeF() - 1.5))
        painter.setFont(font)
        bottom = self.height() - 3
        painter.drawText(int(plot.left()), bottom, self._data[0][0].strftime("%d.%m. %H:%M"))
        last = self._data[-1][0].strftime("%d.%m. %H:%M")
        painter.drawText(int(plot.right() - painter.fontMetrics().horizontalAdvance(last)),
                         bottom, last)

    def mouseMoveEvent(self, event) -> None:
        if not self._data:
            return
        plot = self._plot_rect()
        width, gap = self._bar_width(plot)
        index = int((event.position().x() - plot.left()) // (width + gap))
        if 0 <= index < len(self._data):
            hour, total, blocked = self._data[index]
            self.setToolTip(f"{hour.strftime('%d.%m. %H:%M')}\n"
                            f"{total} · {blocked} " + _t("Blocked"))
        else:
            self.setToolTip("")


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
        layout.setSpacing(10)

        cards = QHBoxLayout()
        cards.setSpacing(8)
        self.card_total = _Card(_t("Requests"))
        self.card_blocked = _Card(_t("Blocked"), BLOCKED_COLOR)
        self.card_allowed = _Card(_t("Allowed"), ALLOWED_COLOR)
        self.card_traffic = _Card(_t("Traffic"))
        for card in (self.card_total, self.card_blocked, self.card_allowed, self.card_traffic):
            cards.addWidget(card)

        self.combo_range = QComboBox()
        for label, hours, chart_hours in RANGES:
            self.combo_range.addItem(label(), (hours, chart_hours))
        self.combo_range.currentIndexChanged.connect(self._render)
        range_box = QVBoxLayout()
        range_box.addStretch()
        range_box.addWidget(self.combo_range)
        cards.addLayout(range_box)
        layout.addLayout(cards)

        self.chart = _BarChart()
        layout.addWidget(self.chart)
        self.lbl_chart = QLabel("")
        self.lbl_chart.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_chart.setVisible(False)
        layout.addWidget(self.lbl_chart)

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
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(False)          # one line per request, elided
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(24)
        self.table.horizontalHeader().setSectionResizeMode(COL_RULE, QHeaderView.ResizeMode.Stretch)
        body.addWidget(self.table, 3)

        side = QVBoxLayout()
        side.setSpacing(8)
        self.top_table = self._make_top_table(_t("Most blocked domains"))
        self.active_table = self._make_top_table(_t("Most active domains"))
        side.addWidget(self.top_table)
        side.addWidget(self.active_table)
        body.addLayout(side, 2)
        layout.addLayout(body)

        actions = QHBoxLayout()
        self.lbl_summary = QLabel("")
        self.lbl_summary.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_summary.setWordWrap(True)
        actions.addWidget(self.lbl_summary, 1)
        self.btn_allow = QPushButton(_t("Allow selected domain"))
        self.btn_allow.clicked.connect(lambda: self._add_rule(allow=True))
        actions.addWidget(self.btn_allow)
        self.btn_block = QPushButton(_t("Block selected domain"))
        self.btn_block.clicked.connect(lambda: self._add_rule(allow=False))
        actions.addWidget(self.btn_block)
        layout.addLayout(actions)

    def _make_top_table(self, title: str) -> QTableWidget:
        table = QTableWidget(0, 2)
        table.setHorizontalHeaderLabels([title, _t("Count")])
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(True)
        table.setWordWrap(False)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(22)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        return table

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
            self.lbl_problem.setVisible(True)
            self.lbl_problem.setText(_t("Could not read the access log."))
            return
        self.lbl_problem.setVisible(bool(activity.problem))
        self.lbl_problem.setText(activity.problem)
        self._render()

    def _render(self) -> None:
        activity = self._activity
        if activity is None:
            return
        hours, chart_hours = self.combo_range.currentData() or (None, 24)
        view = activity.window(hours)

        if activity.problem and not activity.total:
            for card in (self.card_total, self.card_blocked, self.card_allowed, self.card_traffic):
                card.set_value("–")
            self.lbl_summary.setText(_t("No activity to show."))
            self.table.setRowCount(0)
            self.top_table.setRowCount(0)
            self.active_table.setRowCount(0)
            self.chart.set_data([])
            self.lbl_chart.setVisible(False)
            return

        share = f"{view.blocked * 100 / view.total:.0f} %" if view.total else ""
        self.card_total.set_value(f"{view.total:,}".replace(",", " "))
        self.card_blocked.set_value(f"{view.blocked:,}".replace(",", " "), share)
        self.card_allowed.set_value(f"{view.allowed:,}".replace(",", " "))
        self.card_traffic.set_value(_format_size(view.bytes_total))

        source = _t("Source: {}", str(activity.log_path or ""))
        if activity.unparsed:
            source += " · " + _t("{} lines not understood", activity.unparsed)
        self.lbl_summary.setText("<small>" + source + "</small>")

        self._fill_chart(view, chart_hours)
        self._fill_top(view)
        self._fill_table(view)

    def _fill_chart(self, view, chart_hours: int) -> None:
        hours = view.per_hour(limit=chart_hours)
        self.chart.set_data(hours)
        self.lbl_chart.setVisible(bool(hours))
        if not hours:
            return
        legend = (f"<span style='color:{TOTAL_LEGEND}'>&#9632;</span> " + _t("Requests")
                  + f" &nbsp;<span style='color:{BLOCKED_COLOR}'>&#9632;</span> " + _t("Blocked"))
        self.lbl_chart.setText("<small>" + legend + " &nbsp;·&nbsp; " + _t(
            "Requests per hour, {} to {} · busiest hour: {}",
            hours[0][0].strftime("%d.%m. %H:%M"), hours[-1][0].strftime("%d.%m. %H:%M"),
            max(total for _, total, _ in hours)) + "</small>")

    def _fill_top(self, view) -> None:
        blocked = view.top_hosts(limit=TOP_N, blocked_only=True)
        # Without a single blocked request "top blocked" would be a lie.
        self.top_table.setHorizontalHeaderLabels(
            [_t("Most blocked domains") if blocked else _t("Top domains"), _t("Count")])
        self._fill_counts(self.top_table, blocked or view.top_hosts(limit=TOP_N), BLOCKED_COLOR)
        self._fill_counts(self.active_table, view.top_hosts(limit=TOP_N), "")

    @staticmethod
    def _fill_counts(table: QTableWidget, rows: list, color: str) -> None:
        table.setRowCount(len(rows))
        for row, (host, count) in enumerate(rows):
            table.setItem(row, 0, QTableWidgetItem(host))
            item = QTableWidgetItem(str(count))
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if color:
                item.setForeground(QColor(color))
            table.setItem(row, 1, item)

    def _fill_table(self, view) -> None:
        requests = list(reversed(view.requests))[:MAX_ROWS]
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
                if col == COL_RESULT:
                    item.setForeground(QColor(BLOCKED_COLOR if req.blocked else ALLOWED_COLOR))
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
        tables = [(self.table, COL_DOMAIN), (self.top_table, 0), (self.active_table, 0)]
        # Whichever list the user is working in wins; the request list is the default.
        focused = [entry for entry in tables if entry[0].hasFocus()]
        for table, column in focused + [(self.table, COL_DOMAIN)]:
            row = table.currentRow()
            if row < 0 or table.isRowHidden(row):
                continue
            item = table.item(row, column)
            if item and item.text():
                return item.text()
        return ""

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
    if size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    return f"{size / (1024 * 1024 * 1024):.1f} GB"
