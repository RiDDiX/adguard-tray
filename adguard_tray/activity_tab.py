"""Activity tab – what AdGuard actually did, read from its access log.

The access log is the only per-request record adguard-cli keeps, and it is
rotated away at 10 MiB, so the numbers live in a small database that ingests
the log forward (see store.py). The layout follows AdGuard's own activity
screens: counters at the top, a chart over time, the "most blocked" / "most
active" lists beside each other, and the request list underneath. Clicking a
domain drills into it.

If the database cannot be used at all, the tab falls back to reading the tail
of the log directly – fewer numbers, but not an empty screen.
"""

import logging
from datetime import datetime

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
    QTabWidget,
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
MODIFIED_COLOR = "#d97706"
TOTAL_LEGEND = "#7fa8d0"        # matches the translucent highlight the chart paints

# (label, hours of history, hours of chart)
RANGES = (
    (lambda: _t("Last 24 hours"), 24, 24),
    (lambda: _t("Last 7 days"), 24 * 7, 24 * 7),
    (lambda: _t("Last 30 days"), 24 * 30, 24 * 30),
    (lambda: _t("All time"), None, 24 * 30),
)


class _ActivityWorker(QThread):
    """Ingests new log lines and answers every query the tab needs."""
    done = pyqtSignal(object)

    def __init__(self, hours, chart_hours, host="", generation=0):
        super().__init__()
        self._hours = hours
        self._chart_hours = chart_hours
        self._host = host
        self.generation = generation

    def run(self):
        from . import store
        data = {"host": self._host, "generation": self.generation,
                "problem": "", "fallback": None}
        try:
            result = store.ingest()
            data["ingest"] = result
            try:
                data.update(store.dashboard(self._hours, self._chart_hours,
                                            host=self._host, limit=TOP_N, rows=MAX_ROWS))
                data["db_bytes"] = store.db_size()
            except Exception:
                # The database is unusable. Say why and still read the log, so
                # a broken store is not a blank screen.
                logger.exception("Reading the activity store failed")
                data["problem"] = _describe_problem(result.error)
                data["fallback"] = _tail_fallback()
                self.done.emit(data)
                return
            if result.error:
                # Stored data still renders, but the history stopped updating.
                data["problem"] = _t("History is not being updated: {}", result.error)
        except Exception as exc:
            logger.exception("Activity refresh failed")
            data["problem"] = str(exc)
            data["fallback"] = _tail_fallback()
        self.done.emit(data)


def _describe_problem(error: str) -> str:
    from .stats import read_activity
    activity = read_activity(max_lines=1)
    return activity.problem or _t("Could not read the access log.") + f" ({error})"


def _tail_fallback():
    """Whatever the log itself still holds, when the store is unusable."""
    from .stats import read_activity
    try:
        return read_activity()
    except Exception:
        logger.exception("Fallback read failed")
        return None


class _Card(QFrame):
    """One big number with a caption."""

    def __init__(self, caption: str, color: str = "", parent=None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        # Without this the row of cards eats the height the tables need.
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
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
        self._data = {}
        self._host = ""
        self._generation = 0
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
        self.card_modified = _Card(_t("Modified"), MODIFIED_COLOR)
        self.card_traffic = _Card(_t("Traffic"))
        for card in (self.card_total, self.card_blocked, self.card_allowed,
                     self.card_modified, self.card_traffic):
            cards.addWidget(card)

        self.combo_range = QComboBox()
        for label, hours, chart_hours in RANGES:
            self.combo_range.addItem(label(), (hours, chart_hours))
        self.combo_range.currentIndexChanged.connect(self.refresh)
        # Aligned, not padded with a stretch – a greedy stretch here would
        # steal the height the tables need.
        cards.addWidget(self.combo_range, 0, Qt.AlignmentFlag.AlignBottom)
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

        self.btn_clear_host = QPushButton("")
        self.btn_clear_host.setVisible(False)
        self.btn_clear_host.clicked.connect(lambda: self.drill_into(""))
        row.addWidget(self.btn_clear_host)

        self.btn_refresh = QPushButton(_t("Refresh"))
        self.btn_refresh.clicked.connect(self.refresh)
        row.addWidget(self.btn_refresh)

        self.btn_reset = QPushButton(_t("Reset history"))
        self.btn_reset.setToolTip(_t("Delete the stored history and read the log again."))
        self.btn_reset.clicked.connect(self._reset_history)
        row.addWidget(self.btn_reset)
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

        self.side = QTabWidget()
        self.top_table = self._make_top_table(_t("Most blocked domains"))
        self.active_table = self._make_top_table(_t("Most active domains"))
        self.traffic_table = self._make_top_table(_t("Most traffic"))
        self.rules_table = self._make_top_table(_t("Top rules"))
        for table, title in ((self.top_table, _t("Blocked")),
                             (self.active_table, _t("Requests")),
                             (self.traffic_table, _t("Traffic")),
                             (self.rules_table, _t("Rules"))):
            self.side.addTab(table, title)
        for table in (self.top_table, self.active_table, self.traffic_table):
            table.itemSelectionChanged.connect(self._drill_from_side)
        body.addWidget(self.side, 2)
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
        hours, chart_hours = self.combo_range.currentData() or (24, 24)
        self._generation += 1
        worker = _ActivityWorker(hours, chart_hours, self._host, self._generation)
        worker.done.connect(self._on_loaded)
        self._workers.append(worker)
        worker.start()

    def drill_into(self, host: str) -> None:
        """Show only this domain in the request list, or all of them again."""
        self._host = host
        self.btn_clear_host.setVisible(bool(host))
        self.btn_clear_host.setText(_t("Showing {} – show all", host) if host else "")
        if not host:
            for table in (self.top_table, self.active_table, self.traffic_table):
                # Clearing fires itemSelectionChanged, which would drill back in.
                table.blockSignals(True)
                table.clearSelection()
                table.setCurrentCell(-1, -1)
                table.blockSignals(False)
        self.refresh()

    def _drill_from_side(self) -> None:
        table = self.side.currentWidget()
        if table is self.rules_table:
            return
        selected = table.selectedItems()
        item = selected[0] if selected else None
        if item and item.text() and item.text() != self._host:
            self.drill_into(item.text())

    def _on_loaded(self, data) -> None:
        # Workers are dropped here, on the GUI thread: doing it from the
        # thread's own finished signal deletes the QThread from inside itself.
        for worker in [w for w in self._workers if w.isFinished()]:
            self._workers.remove(worker)
            worker.deleteLater()
        if isinstance(data, dict) and data.get("generation", 0) < self._generation:
            return          # a slower older refresh; the newer one owns the view
        self.btn_refresh.setEnabled(True)
        if not isinstance(data, dict):
            self.lbl_problem.setVisible(True)
            self.lbl_problem.setText(_t("Could not read the access log."))
            return
        self._data = data
        problem = data.get("problem", "")
        self.lbl_problem.setVisible(bool(problem))
        self.lbl_problem.setText(problem)
        if data.get("fallback") is not None:
            hours = (self.combo_range.currentData() or (24, 24))[0]
            self._render_fallback(data["fallback"], hours)
            return
        if "summary" not in data:
            self._clear()
            return
        self._render(data)

    def _clear(self) -> None:
        for card in self._cards():
            card.set_value("–")
        self.table.setRowCount(0)
        for table in (self.top_table, self.active_table, self.traffic_table, self.rules_table):
            table.setRowCount(0)
        self.chart.set_data([])
        self.lbl_chart.setVisible(False)
        self.lbl_summary.setText(_t("No activity to show."))

    def _cards(self):
        return (self.card_total, self.card_blocked, self.card_allowed,
                self.card_modified, self.card_traffic)

    def _render(self, data: dict) -> None:
        summary = data["summary"]
        total, blocked = summary["total"], summary["blocked"]
        if not total:
            self._clear()
            self.lbl_summary.setText(self._source_line(data))
            return

        share = f"{blocked * 100 / total:.0f} %" if total else ""
        self.card_total.set_value(_number(total))
        self.card_blocked.set_value(_number(blocked), share)
        self.card_allowed.set_value(_number(total - blocked))
        self.card_modified.set_value(_number(summary["modified"]))
        self.card_traffic.set_value(_format_size(summary["bytes"]))

        self.lbl_summary.setText(self._source_line(data))
        self._fill_chart(data["hours"])
        self._fill_counts(self.top_table, data["blocked"], BLOCKED_COLOR)
        self._fill_counts(self.active_table, data["active"], "")
        self._fill_counts(self.traffic_table, data["traffic"], "", as_size=True)
        self._fill_counts(self.rules_table, data["rules"], BLOCKED_COLOR)
        self._fill_table(data["recent"])

    def _source_line(self, data: dict) -> str:
        from .stats import access_log_path
        parts = [_t("Source: {}", str(access_log_path()))]
        ingest = data.get("ingest")
        if ingest is not None and ingest.unparsed:
            parts.append(_t("{} lines not understood", ingest.unparsed))
        if data.get("db_bytes"):
            parts.append(_t("history {}", _format_size(data["db_bytes"])))
        return "<small>" + " · ".join(parts) + "</small>"

    def _render_fallback(self, activity, hours) -> None:
        """Show what the log alone can give when the database is unusable."""
        if activity is not None:
            activity = activity.window(hours)
        if activity is None or not activity.total:
            self._clear()
            return
        share = f"{activity.blocked * 100 / activity.total:.0f} %"
        self.card_total.set_value(_number(activity.total))
        self.card_blocked.set_value(_number(activity.blocked), share)
        self.card_allowed.set_value(_number(activity.allowed))
        self.card_modified.set_value("–")
        self.card_traffic.set_value(_format_size(activity.bytes_total))
        self._fill_chart(activity.per_hour(limit=24))
        self._fill_counts(self.top_table, activity.top_hosts(TOP_N, blocked_only=True), BLOCKED_COLOR)
        self._fill_counts(self.active_table, activity.top_hosts(TOP_N), "")
        self._fill_counts(self.traffic_table, [], "")
        self._fill_counts(self.rules_table, activity.top_rules(TOP_N), BLOCKED_COLOR)
        self._fill_table([_row_of(r) for r in reversed(activity.requests[-MAX_ROWS:])])

    def _fill_chart(self, hours) -> None:
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

    @staticmethod
    def _fill_counts(table: QTableWidget, rows, color: str, as_size: bool = False) -> None:
        table.blockSignals(True)
        table.setRowCount(len(rows))
        for row, (name, count) in enumerate(rows):
            table.setItem(row, 0, QTableWidgetItem(name))
            item = QTableWidgetItem(_format_size(count) if as_size else _number(count))
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if color:
                item.setForeground(QColor(color))
            table.setItem(row, 1, item)
        table.blockSignals(False)

    def _fill_table(self, rows) -> None:
        self.table.setRowCount(len(rows))
        for row, request in enumerate(rows):
            when = datetime.fromtimestamp(request["ts"]).strftime("%d.%m. %H:%M:%S")
            blocked = bool(request["blocked"])
            if blocked:
                result, color = _t("Blocked"), BLOCKED_COLOR
            elif request["modified"]:
                result, color = _t("Modified"), MODIFIED_COLOR
            else:
                result, color = _t("Allowed"), ALLOWED_COLOR
            tooltip = request["url"] or request["host"]
            if request["filter_id"] >= 0:
                tooltip += "\n" + _t("Filter list ID: {}", request["filter_id"])
            for extra, value in ((_t("App"), request["app"]),
                                 (_t("Protocol"), request["protocol"]),
                                 (_t("Type"), request["content_type"])):
                if value:
                    tooltip += f"\n{extra}: {value}"
            for col, text in (
                (COL_TIME, when),
                (COL_DOMAIN, request["host"]),
                (COL_RESULT, result),
                (COL_RULE, request["rule"]),
                (COL_SIZE, _format_size(request["size"])),
                (COL_MS, str(request["duration"]) if request["duration"] >= 0 else ""),
            ):
                item = QTableWidgetItem(text)
                item.setToolTip(tooltip)
                item.setData(Qt.ItemDataRole.UserRole, blocked)
                if col == COL_RESULT:
                    item.setForeground(QColor(color))
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

    def _reset_history(self) -> None:
        from . import store

        confirm = QMessageBox.question(
            self, _t("Activity"),
            _t("Delete the stored history? Only what the log still holds can be read back."),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if confirm != QMessageBox.StandardButton.Yes:
            return
        ok, error = store.reset()
        if not ok:
            QMessageBox.critical(self, _t("Activity"), error)
            return
        self.drill_into("")

    # ── Actions ────────────────────────────────────────────────────────────

    def _selected_domain(self) -> str:
        tables = [(self.table, COL_DOMAIN), (self.top_table, 0),
                  (self.active_table, 0), (self.traffic_table, 0)]
        # Whichever list the user is working in wins; the request list is the default.
        focused = [entry for entry in tables if entry[0].hasFocus()]
        for table, column in focused + [(self.table, COL_DOMAIN)]:
            row = table.currentRow()
            if row < 0 or table.isRowHidden(row):
                continue
            item = table.item(row, column)
            if item and item.text():
                return item.text()
        return self._host

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


def _number(value: int) -> str:
    """Thin spaces between thousands – easier to read at a glance."""
    return f"{value:,}".replace(",", "\u2009")


def _row_of(request) -> dict:
    """A parsed request in the shape the request table expects."""
    return {
        "ts": int(request.when.timestamp()) if request.when else 0,
        "host": request.host, "url": request.url, "rule": request.rule,
        "size": request.size, "duration": request.duration_ms,
        "blocked": int(request.blocked), "modified": int(request.modified),
        "filter_id": request.filter_id, "app": request.app,
        "protocol": request.protocol, "content_type": request.content_type,
    }


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
