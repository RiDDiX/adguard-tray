"""Activity page – what AdGuard actually did, read from its access log.

The access log is the only per-request record adguard-cli keeps, and it is
rotated away at 10 MiB, so the numbers live in a small database that ingests
the log forward (see store.py). The layout follows AdGuard's own activity
screens: counters and a chart over time at the top, the request list with the
"most blocked" / "most active" lists beside it underneath. Clicking a domain
drills into it.

If the database cannot be used at all, the page falls back to reading the tail
of the log directly – fewer numbers, but not an empty screen.
"""

import logging
from datetime import datetime, timedelta

from PyQt6.QtCore import QEvent, QLocale, QPointF, QRectF, QSize, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QFontMetrics, QPainter, QPalette, QPen
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QMenu,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QStackedWidget,
    QStyledItemDelegate,
    QTableWidget,
    QTableWidgetItem,
    QToolTip,
    QWidget,
)

from . import i18n, theme, ui
from .i18n import _t
from .manager_window import PAGE_EXCEPTIONS
from .ui import Page

logger = logging.getLogger(__name__)

COL_TIME, COL_DOMAIN, COL_RESULT, COL_RULE, COL_SIZE, COL_MS = range(6)
MAX_ROWS = 500          # what the table shows; the counters use every line read
TOP_N = 10
TONE_ROLE = Qt.ItemDataRole.UserRole + 1
HOUR_FORMAT = "%Y-%m-%d %H:%M"   # ISO, as the other pages show dates
DOMAIN_MAX = 200        # the domain column never takes more than this
DOMAIN_MIN = 110        # below these the columns elide no further; size and
RULE_MIN = 80           # duration leave the view instead (the tooltip has them)

# (label, hours of history, hours of chart)
RANGES = (
    (lambda: _t("Last 24 hours"), 24, 24),
    (lambda: _t("Last 7 days"), 24 * 7, 24 * 7),
    (lambda: _t("Last 30 days"), 24 * 30, 24 * 30),
    (lambda: _t("All time"), None, 24 * 30),
)


class _ActivityWorker(QThread):
    """Ingests new log lines and answers every query the page needs."""
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
                # A missing or unreadable log gets its own explanation, not errno.
                from .stats import read_activity
                data["problem"] = (read_activity(max_lines=1).problem
                                   or _t("History is not being updated: {}", result.error))
        except Exception as exc:
            logger.exception("Activity refresh failed")
            data["problem"] = str(exc)
            data["fallback"] = _tail_fallback()
        self.done.emit(data)


class _ResetWorker(QThread):
    """Deletes the stored history. It waits for any ingest that holds the
    store's lock (the Overview reads the log too), so not on the GUI thread."""
    done = pyqtSignal(bool, str)

    def run(self):
        from . import store
        try:
            ok, error = store.reset()
        except Exception as exc:
            logger.exception("Resetting the history failed")
            ok, error = False, str(exc)
        self.done.emit(ok, error)


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


class _ToneDelegate(QStyledItemDelegate):
    """Text in the status colour of the palette in use at paint time, so a
    light/dark switch recolours the list without reloading it."""

    def initStyleOption(self, option, index) -> None:
        super().initStyleOption(option, index)
        tone = index.data(TONE_ROLE)
        if tone:
            palette = QPalette(option.palette)
            palette.setColor(QPalette.ColorRole.Text, theme.tokens().tone_text[tone])
            option.palette = palette


def _column(painter: QPainter, rect: QRectF, color, rounded: bool = True) -> None:
    """A bar segment: rounded at its top end, square at the bottom."""
    painter.setBrush(color)
    radius = min(4.0, rect.width() / 2, rect.height() / 2) if rounded else 0.0
    if radius >= 1:
        painter.drawRoundedRect(rect, radius, radius)
        painter.drawRect(rect.adjusted(0, radius, 0, 0))
    else:
        painter.drawRect(rect)


class _BarChart(QWidget):
    """Requests over time: blocked at the baseline, the allowed rest on top.

    Hours are grouped into longer bars once they would get too thin to see or
    to point at (30 days are 720 hours).
    """

    STEPS = (1, 2, 3, 4, 6, 8, 12, 24)
    PITCH = 6           # narrowest bar plus gap, in pixels
    GAP = 2.0

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._data: list = []
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(True)

    def set_data(self, data: list) -> None:
        self._data = list(data)
        self.update()

    def _font(self) -> QFont:
        return ui.scaled_font(self, 0.92)

    def sizeHint(self) -> QSize:
        return QSize(400, 104 + QFontMetrics(self._font()).height())

    def _plot(self) -> QRectF:
        label = QFontMetrics(self._font()).height()
        return QRectF(self.rect()).adjusted(12, 6, -12, -(label + 8))

    def _bars(self, plot: QRectF) -> tuple[list, float]:
        """(first hour, last hour, total, blocked) per bar, and the bar pitch."""
        count = len(self._data)
        step = next((s for s in self.STEPS if -(-count // s) * self.PITCH <= plot.width()),
                    self.STEPS[-1])
        bars = []
        for end in range(count, 0, -step):      # from the end: the newest bar is whole
            chunk = self._data[max(0, end - step):end]
            bars.append((chunk[0][0], chunk[-1][0],
                         sum(c[1] for c in chunk), sum(c[2] for c in chunk)))
        bars.reverse()
        return bars, plot.width() / len(bars)

    def paintEvent(self, _event) -> None:
        if not self._data:
            return
        tok = theme.tokens()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)
        plot = self._plot()
        bars, pitch = self._bars(plot)
        peak = max(bar[2] for bar in bars) or 1
        width = max(1.0, min(24.0, pitch - self.GAP))
        base = round(plot.bottom())
        for index, (_first, _last, total, blocked) in enumerate(bars):
            if not total:
                continue
            left = plot.left() + index * pitch + (pitch - width) / 2
            height = max(2.0, total / peak * plot.height())
            low = min(height, max(2.0, blocked / peak * plot.height())) if blocked else 0.0
            high = height - low - (self.GAP if low else 0.0)
            if high >= 1:
                _column(p, QRectF(left, base - height, width, high), tok.chart_allowed)
            if low:
                _column(p, QRectF(left, base - low, width, low), tok.chart_blocked, rounded=high < 1)

        p.setPen(QPen(tok.border, 1))
        p.drawLine(QPointF(plot.left(), base + 0.5), QPointF(plot.right(), base + 0.5))

        p.setFont(self._font())
        fm = p.fontMetrics()
        row = QRectF(plot.left(), base + 5, plot.width(), fm.height())
        left_aligned = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        p.setPen(tok.secondary)
        p.drawText(row, left_aligned, self._data[0][0].strftime(HOUR_FORMAT))
        p.drawText(row, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                   self._data[-1][0].strftime(HOUR_FORMAT))
        legend = ((tok.chart_allowed, _t("Allowed")), (tok.chart_blocked, _t("Blocked")))
        widths = [13 + fm.horizontalAdvance(text) for _color, text in legend]
        x = row.center().x() - (sum(widths) + 16) / 2
        for (color, text), item_width in zip(legend, widths, strict=True):
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(color)
            p.drawRoundedRect(QRectF(x, row.center().y() - 4, 8, 8), 2, 2)
            p.setPen(tok.secondary)
            p.drawText(QRectF(x + 13, row.top(), item_width, row.height()), left_aligned, text)
            x += item_width + 16

    def mouseMoveEvent(self, event) -> None:
        if not self._data:
            return
        plot = self._plot()
        bars, pitch = self._bars(plot)
        index = int((event.position().x() - plot.left()) // pitch)
        if not 0 <= index < len(bars):
            QToolTip.hideText()
            return
        first, last, total, blocked = bars[index]
        when = first.strftime(HOUR_FORMAT)
        if last != first:
            when += " – " + (last + timedelta(hours=1)).strftime(HOUR_FORMAT)
        QToolTip.showText(event.globalPosition().toPoint(),
                          f"{when}\n{_number(total)} {_t('Requests')} · "
                          f"{_number(blocked)} {_t('Blocked')}", self)


class ActivityTab(Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(wide=True, parent=parent)
        self.ctx = ctx
        self._workers: list[QThread] = []
        self._data = {}
        self._host = ""
        self._domain = ""           # what Allow / Block act on
        self._generation = 0
        self._busy = False
        self._again = False         # asked for while a load was running
        self._loaded_at = None      # when the data on screen was read
        self._load_message = False  # the banner shows a problem from loading
        self._natural = {}          # column -> width of its content
        self._shown = (0, "")       # range index and domain of the data on screen
        self._build_ui()

    # ── UI ─────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # What the whole page shows: the time range and, drilled in, one domain.
        # The request list has its own toolbar further down; one row for both
        # does not fit a narrow window.
        bar = QHBoxLayout()
        bar.setSpacing(8)
        self.combo_range = QComboBox()
        self.combo_range.setAccessibleName(_t("Time range"))
        for label, hours, chart_hours in RANGES:
            self.combo_range.addItem(label(), (hours, chart_hours))
        self.combo_range.currentIndexChanged.connect(self.refresh)
        bar.addWidget(self.combo_range)
        self.spinner = ui.Spinner()         # next to the range it locks
        bar.addWidget(self.spinner)
        self.btn_clear_host = QPushButton("")
        self.btn_clear_host.setVisible(False)
        self.btn_clear_host.clicked.connect(lambda: self.drill_into(""))
        bar.addWidget(self.btn_clear_host)
        bar.addStretch(1)
        self.body.addLayout(bar)
        self.body.addSpacing(4)

        summary = ui.Card(padding=6)
        tiles = QHBoxLayout()
        tiles.setSpacing(2)
        self.card_total = ui.StatTile(_t("Requests"))
        self.card_blocked = ui.StatTile(_t("Blocked"), tone="danger")
        self.card_allowed = ui.StatTile(_t("Allowed"), tone="allowed")
        self.card_modified = ui.StatTile(_t("Modified"), tone="warning")
        self.card_traffic = ui.StatTile(_t("Traffic"))
        for card in self._cards():
            tiles.addWidget(card)
        summary.layout_.addLayout(tiles)
        self.chart = _BarChart()
        self.chart.setVisible(False)
        summary.add(self.chart)
        self.add(summary)
        self.body.addSpacing(4)

        tools = QHBoxLayout()
        tools.setSpacing(8)
        self.search_box = QLineEdit()
        self.search_box.setClearButtonEnabled(True)
        self.search_box.setPlaceholderText(_t("Search domains or rules…"))
        self.search_box.setAccessibleName(_t("Search domains or rules…").rstrip("…."))
        self.search_box.textChanged.connect(self._apply_filter)
        tools.addWidget(self.search_box, 1)

        self.btn_blocked = QPushButton(_t("Blocked only"))
        self.btn_blocked.setCheckable(True)
        self.btn_blocked.toggled.connect(self._apply_filter)
        tools.addWidget(self.btn_blocked)

        # Short labels: the domain they act on is the selected row (or the one
        # drilled into), and the tooltip names it.
        self.btn_allow = QPushButton(_t("Allow"))
        self.btn_allow.clicked.connect(lambda: self._add_rule(allow=True))
        tools.addWidget(self.btn_allow)
        self.btn_block = QPushButton(_t("Block"))
        self.btn_block.clicked.connect(lambda: self._add_rule(allow=False))
        tools.addWidget(self.btn_block)

        # A push button with a menu: Fusion squeezes a tool button's menu
        # arrow into its corner.
        self.btn_more = QPushButton(_t("More"))
        menu = QMenu(self.btn_more)
        menu.setToolTipsVisible(True)
        self.act_reset = menu.addAction(_t("Reset history…"))
        self.act_reset.setToolTip(_t("Delete the stored history and read the log again."))
        self.act_reset.triggered.connect(self._reset_history)
        menu.addSeparator()
        self.act_source = menu.addAction("")
        self.act_source.setEnabled(False)
        self.btn_more.setMenu(menu)
        tools.addWidget(self.btn_more)
        self.body.addLayout(tools)
        self.body.addSpacing(4)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            _t("Time"), _t("Domain"), _t("Result"), _t("Rule"), _t("Size"), _t("Duration"),
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(False)          # one line per request, elided
        self.table.verticalHeader().setVisible(False)
        ui.style_table(self.table)
        self.table.viewport().installEventFilter(self)
        self.table.setItemDelegateForColumn(COL_RESULT, _ToneDelegate(self.table))
        self.table.currentCellChanged.connect(self._on_request_selected)

        self.empty = ui.EmptyState(self.table)
        requests = ui.Card(padding=4)
        requests.add(self.table)

        # A picker, not tabs: four tab labels would set the pane's width, and
        # that width is what the request list needs. QComboBox clips rather
        # than elides, hence the one-word labels.
        self.side_pick = QComboBox()
        self.side_pick.setAccessibleName(_t("Top lists"))
        self.side = QStackedWidget()
        # Short headers too: the header view clips a long title, it does not elide.
        self.top_table = self._make_top_table(_t("Domain"))
        self.active_table = self._make_top_table(_t("Domain"))
        self.traffic_table = self._make_top_table(_t("Domain"), _t("Traffic"))
        self.rules_table = self._make_top_table(_t("Rule"))
        for table, title in ((self.top_table, _t("Blocked")),
                             (self.active_table, _t("Requests")),
                             (self.traffic_table, _t("Traffic")),
                             (self.rules_table, _t("Rules"))):
            self.side_pick.addItem(title)
            self.side.addWidget(table)
        self.side_pick.currentIndexChanged.connect(self.side.setCurrentIndex)
        self.side.currentChanged.connect(self.side_pick.setCurrentIndex)
        for table in (self.top_table, self.active_table, self.traffic_table):
            table.itemSelectionChanged.connect(self._drill_from_side)
        tops = ui.Card(padding=4)
        tops.layout_.addWidget(self.side_pick, 0, Qt.AlignmentFlag.AlignLeft)
        tops.add(self.side)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setHandleWidth(10)
        self.splitter.addWidget(requests)
        self.splitter.addWidget(tops)
        # Both panes scale with the window, the request list three times as much.
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([3000, 1000])
        self.add(self.splitter, 1)

        self._fit_rows()
        self._measure_columns()
        self._set_domain("")

    def _make_top_table(self, title: str, count: str = "") -> QTableWidget:
        table = QTableWidget(0, 2)
        table.setHorizontalHeaderLabels([title, count or _t("Count")])
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(True)
        table.setWordWrap(False)
        table.verticalHeader().setVisible(False)
        ui.style_table(table)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        return table

    def _tables(self):
        return (self.table, self.top_table, self.active_table, self.traffic_table, self.rules_table)

    def _fit_rows(self) -> None:
        height = self.fontMetrics().height() + 10
        for table in self._tables():
            table.verticalHeader().setDefaultSectionSize(height)

    def _fit_columns(self) -> None:
        # Domain and rule share what the other columns leave and elide. Only
        # when even that is too tight do duration, then size, leave the view:
        # a horizontal scroll bar would hide them just the same. Tighter
        # still, the list does scroll.
        if not self._natural:
            return
        width = self._natural
        domain_min = min(width[COL_DOMAIN], DOMAIN_MIN)
        rule_min = min(width[COL_RULE], RULE_MIN)
        free = self.table.viewport().width() - sum(
            width[col] for col in (COL_TIME, COL_RESULT, COL_SIZE, COL_MS))
        for col in (COL_MS, COL_SIZE):
            hide = free < domain_min + rule_min
            self.table.setColumnHidden(col, hide)
            if hide:
                free += width[col]
        domain = min(width[COL_DOMAIN], max(domain_min, free - rule_min))
        header = self.table.horizontalHeader()
        header.resizeSection(COL_DOMAIN, domain)
        header.resizeSection(COL_RULE, max(rule_min, free - domain))

    def eventFilter(self, obj, event) -> bool:
        # The scroll area filters its own events through here from the start.
        table = getattr(self, "table", None)
        if table is not None and obj is table.viewport() and event.type() == QEvent.Type.Resize:
            self._fit_columns()
        return super().eventFilter(obj, event)

    def changeEvent(self, event) -> None:
        super().changeEvent(event)
        if event.type() == QEvent.Type.FontChange:
            self._fit_rows()

    def focus_search(self) -> None:
        self.search_box.setFocus(Qt.FocusReason.ShortcutFocusReason)
        self.search_box.selectAll()

    def on_shown(self) -> None:
        self.refresh()

    # ── Loading ────────────────────────────────────────────────────────────

    def refresh(self) -> None:
        if self._busy:
            # One read at a time; the newest request runs once this one is in.
            self._again = True
            return
        self._set_busy(True)
        self._again = False
        hours, chart_hours = self.combo_range.currentData() or (24, 24)
        self._generation += 1
        worker = _ActivityWorker(hours, chart_hours, self._host, self._generation)
        worker.done.connect(self._on_loaded)
        self._workers.append(worker)
        worker.start()

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        self.combo_range.setEnabled(not busy)
        self.act_reset.setEnabled(not busy)
        self.spinner.set_busy(busy)

    def drill_into(self, host: str) -> None:
        """Show only this domain in the request list, or all of them again."""
        self._set_domain(host)
        self._show_host(host)
        if not host:
            self._mark_host()
        self.refresh()

    def _show_host(self, host: str) -> None:
        self._host = host
        self.btn_clear_host.setVisible(bool(host))
        short = self.btn_clear_host.fontMetrics().elidedText(host, Qt.TextElideMode.ElideMiddle, 260)
        self.btn_clear_host.setText(_t("Showing {} – show all", short) if host else "")
        self.btn_clear_host.setToolTip(ui.plain_tip(host))

    def _mark_host(self) -> None:
        """Select the drilled-into domain in the top lists, or nothing."""
        for table in (self.top_table, self.active_table, self.traffic_table):
            # Selecting fires itemSelectionChanged, which would drill in again.
            table.blockSignals(True)
            table.clearSelection()
            table.setCurrentCell(-1, -1)
            for row in range(table.rowCount()):
                if self._host and table.item(row, 0).text() == self._host:
                    table.selectRow(row)
            table.blockSignals(False)

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
        self._busy = False
        if self._again:
            self.refresh()  # the range or the domain changed meanwhile
            return
        self._set_busy(False)
        if not isinstance(data, dict):
            data = {"problem": _t("Could not read the access log."), "fallback": None}
        problem = data.get("problem", "")
        if data.get("fallback") is None and "summary" not in data:
            self._show_failure(problem)
            return
        self._data = data
        self._loaded_at = datetime.now()
        self._shown = (self.combo_range.currentIndex(), self._host)
        self.act_source.setText(self._source_line(data))
        if problem:
            self.banner.show_message(problem, "warning")
            self._load_message = True
        elif self._load_message:
            self.banner.hide()
            self._load_message = False
        if data.get("fallback") is not None:
            hours = (self.combo_range.currentData() or (24, 24))[0]
            self._render_fallback(data["fallback"], hours)
            return
        self._render(data)

    def _show_failure(self, problem: str) -> None:
        """Nothing came back: keep what is on screen, but say how old it is."""
        if self._loaded_at is None:
            self._clear()
            text = _t("Could not read the access log.")
        else:
            # Put the range and the domain back to what the old data shows.
            index, host = self._shown
            self.combo_range.blockSignals(True)
            self.combo_range.setCurrentIndex(index)
            self.combo_range.blockSignals(False)
            if host != self._host:
                self._show_host(host)
                self._mark_host()
            text = _t("Could not refresh. Showing data from {}.", self._loaded_at.strftime("%H:%M"))
        self.banner.show_message(text, "danger", details=problem)
        self._load_message = True

    def _clear(self) -> None:
        # Caption first: set_value() puts it into the accessible name.
        self.card_blocked.set_caption(_t("Blocked"))
        for card in self._cards():
            card.set_value("–")
        for table in (self.top_table, self.active_table, self.traffic_table, self.rules_table):
            table.setRowCount(0)
        self._fill_chart([])
        self._fill_table([])

    def _cards(self):
        return (self.card_total, self.card_blocked, self.card_allowed,
                self.card_modified, self.card_traffic)

    def _show_share(self, total: int, blocked: int) -> None:
        # The share leads, so a narrow tile elides the word and not the number.
        caption = _t("{}% blocked", f"{blocked * 100 / total:.0f}")
        self.card_blocked.set_caption(caption)
        self.card_blocked.set_value(_number(blocked), caption)

    def _render(self, data: dict) -> None:
        summary = data["summary"]
        total, blocked = summary["total"], summary["blocked"]
        if not total:
            self._clear()
            return

        self.card_total.set_value(_number(total))
        self._show_share(total, blocked)
        self.card_allowed.set_value(_number(total - blocked))
        self.card_modified.set_value(_number(summary["modified"]))
        self.card_traffic.set_value(_format_size(summary["bytes"]))

        self._fill_chart(data["hours"])
        self._fill_counts(self.top_table, data["blocked"])
        self._fill_counts(self.active_table, data["active"])
        self._fill_counts(self.traffic_table, data["traffic"], as_size=True)
        self._fill_counts(self.rules_table, data["rules"])
        self._fill_table(data["recent"])

    def _source_line(self, data: dict) -> str:
        from .stats import access_log_path
        parts = [_t("Source: {}", str(access_log_path()))]
        ingest = data.get("ingest")
        if ingest is not None and ingest.unparsed:
            parts.append(_t("{} lines not understood", ingest.unparsed))
        if data.get("db_bytes"):
            parts.append(_t("history {}", _format_size(data["db_bytes"])))
        return " · ".join(parts)

    def _render_fallback(self, activity, hours) -> None:
        """Show what the log alone can give when the database is unusable."""
        if activity is not None:
            activity = activity.window(hours)
        if activity is None or not activity.total:
            self._clear()
            return
        self.card_total.set_value(_number(activity.total))
        self._show_share(activity.total, activity.blocked)
        self.card_allowed.set_value(_number(activity.allowed))
        self.card_modified.set_value("–")
        self.card_traffic.set_value(_format_size(activity.bytes_total))
        self._fill_chart(activity.per_hour(limit=24))
        self._fill_counts(self.top_table, activity.top_hosts(TOP_N, blocked_only=True))
        self._fill_counts(self.active_table, activity.top_hosts(TOP_N))
        self._fill_counts(self.traffic_table, [])
        self._fill_counts(self.rules_table, activity.top_rules(TOP_N))
        self._fill_table([_row_of(r) for r in reversed(activity.requests[-MAX_ROWS:])])

    def _fill_chart(self, hours) -> None:
        self.chart.set_data(hours)
        self.chart.setVisible(bool(hours))
        self.chart.setAccessibleName(_t(
            "Requests per hour, {} to {} · busiest hour: {}",
            hours[0][0].strftime(HOUR_FORMAT), hours[-1][0].strftime(HOUR_FORMAT),
            max(total for _, total, _ in hours)) if hours else "")

    def _fill_counts(self, table: QTableWidget, rows, as_size: bool = False) -> None:
        table.blockSignals(True)
        table.clearSelection()
        table.setRowCount(len(rows))
        for row, (name, count) in enumerate(rows):
            table.setItem(row, 0, QTableWidgetItem(name))
            item = QTableWidgetItem(_format_size(count) if as_size else _number(count))
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            table.setItem(row, 1, item)
            if name == self._host:
                table.selectRow(row)        # keep the drilled-into domain marked
        table.blockSignals(False)

    def _fill_table(self, rows) -> None:
        # Drop the current row first, or it would silently move to another request.
        self.table.setCurrentCell(-1, -1)
        self.table.setRowCount(len(rows))
        today = datetime.now().date()
        numbers = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        for row, request in enumerate(rows):
            stamp = datetime.fromtimestamp(request["ts"])
            # The time of day is enough for today; the tooltip has the date.
            when = stamp.strftime("%H:%M:%S" if stamp.date() == today else HOUR_FORMAT)
            size = _format_size(request["size"])
            duration = f"{request['duration']} ms" if request["duration"] >= 0 else ""
            blocked = bool(request["blocked"])
            if blocked:
                result, tone = _t("Blocked"), "danger"
            elif request["modified"]:
                result, tone = _t("Modified"), "warning"
            else:
                # Plain text: the green of "success" would clash with the
                # blue that stands for allowed in the chart and the tiles.
                result, tone = _t("Allowed"), None
            tooltip = stamp.strftime("%Y-%m-%d %H:%M:%S") + "\n" + (request["url"] or request["host"])
            if request["rule"]:
                tooltip += f"\n{_t('Rule')}: {request['rule']}"
            if request["filter_id"] >= 0:
                tooltip += "\n" + _t("Filter list ID: {}", request["filter_id"])
            for extra, value in ((_t("App"), request["app"]),
                                 (_t("Protocol"), request["protocol"]),
                                 (_t("Type"), request["content_type"]),
                                 (_t("Size"), size),
                                 (_t("Duration"), duration)):
                if value:
                    tooltip += f"\n{extra}: {value}"
            for col, text in (
                (COL_TIME, when),
                (COL_DOMAIN, request["host"]),
                (COL_RESULT, result),
                (COL_RULE, request["rule"]),
                (COL_SIZE, size),
                (COL_MS, duration),
            ):
                item = QTableWidgetItem(text)
                item.setToolTip(ui.plain_tip(tooltip))
                item.setData(Qt.ItemDataRole.UserRole, blocked)
                if col == COL_RESULT:
                    item.setData(TONE_ROLE, tone)
                elif col in (COL_SIZE, COL_MS):
                    item.setTextAlignment(numbers)
                self.table.setItem(row, col, item)
        self._measure_columns()
        self._set_domain(self._host)
        self._apply_filter()

    def _measure_columns(self) -> None:
        # With no rows this measures the header, so an empty list shows it whole.
        for col in (COL_SIZE, COL_MS):
            self.table.setColumnHidden(col, False)      # hidden ones measure 0
        self.table.resizeColumnsToContents()
        header = self.table.horizontalHeader()
        self._natural = {col: header.sectionSize(col) for col in range(header.count())}
        self._natural[COL_DOMAIN] = min(self._natural[COL_DOMAIN], DOMAIN_MAX)
        self._fit_columns()

    def _apply_filter(self) -> None:
        needle = self.search_box.text().strip().lower()
        blocked_only = self.btn_blocked.isChecked()
        shown = 0
        for row in range(self.table.rowCount()):
            domain = self.table.item(row, COL_DOMAIN)
            rule = self.table.item(row, COL_RULE)
            haystack = f"{domain.text() if domain else ''} {rule.text() if rule else ''}".lower()
            hide = bool(needle) and needle not in haystack
            if blocked_only and not (domain and domain.data(Qt.ItemDataRole.UserRole)):
                hide = True
            self.table.setRowHidden(row, hide)
            shown += not hide
        if shown:
            self.empty.set("")
        elif self.table.rowCount():
            self.empty.set(_t("Nothing matches your search."))
        else:
            self.empty.set(_t("No requests yet – AdGuard logs requests while protection is on."))

    def _reset_history(self) -> None:
        if not ui.confirm(self, _t("Reset history"),
                          _t("Delete the stored history? Only what the log still holds can be read back."),
                          _t("Reset history")):
            return
        self._set_busy(True)
        self._again = False
        worker = _ResetWorker()
        worker.done.connect(self._on_reset)
        self._workers.append(worker)
        worker.start()

    def _on_reset(self, ok: bool, error: str) -> None:
        self._set_busy(False)
        if not ok:
            self.banner.show_message(_t("Could not reset the history."), "danger", details=error)
            self._load_message = False
            if self._again:
                self.refresh()
            return
        self.drill_into("")

    # ── Actions ────────────────────────────────────────────────────────────

    def _on_request_selected(self, row: int, _col: int, _previous_row: int, _previous_col: int) -> None:
        # Tracked here, not looked up on click: pressing the button moves the
        # focus away from the list.
        item = self.table.item(row, COL_DOMAIN) if row >= 0 else None
        if item and item.text():
            self._set_domain(item.text())

    def _set_domain(self, domain: str) -> None:
        self._domain = domain
        allow = _t("Allow {}", domain) if domain else _t("Allow selected domain")
        block = _t("Block {}", domain) if domain else _t("Block selected domain")
        for button, text in ((self.btn_allow, allow), (self.btn_block, block)):
            button.setEnabled(bool(domain))
            button.setToolTip(text)
            button.setAccessibleName(text)

    def _add_rule(self, allow: bool) -> None:
        from ._allowlist import (
            add_rule_line,
            domain_to_rule,
            is_valid_domain,
            load_user_rules,
            save_user_rules,
        )

        domain = self._domain
        if not domain:
            return
        self._load_message = False
        if not is_valid_domain(domain):
            self.banner.show_message(_t("Not a valid domain: {}", domain), "warning")
            return

        if allow:
            try:
                domains, other = load_user_rules()
            except (OSError, ValueError) as exc:
                self.banner.show_message(_t("Could not add the rule."), "danger", details=str(exc))
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
            self.banner.show_message(_t("Could not add the rule."), "danger", details=err)
            return
        text = _t("Added rule: {}", rule) + "\n" + self.ctx.restart_adguard()
        if allow:
            self.banner.show_message(text, "success", action=_t("Open exceptions"),
                                     callback=lambda: self.ctx.navigate(PAGE_EXCEPTIONS),
                                     timeout_ms=5000)
        else:
            self.banner.show_message(text, "success", timeout_ms=5000)


def _number(value: int) -> str:
    """Thin spaces between thousands – easier to read at a glance."""
    return f"{value:,}".replace(",", " ")


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
    # Decimal comma or point as the language of the UI writes it.
    locale = QLocale(i18n._LANG)
    locale.setNumberOptions(QLocale.NumberOption.OmitGroupSeparator)    # not "1.023,9 KB"
    for unit, scale in (("KB", 1024), ("MB", 1024 ** 2)):
        if size < scale * 1024:
            return f"{locale.toString(size / scale, 'f', 1)} {unit}"
    return f"{locale.toString(size / 1024 ** 3, 'f', 1)} GB"
