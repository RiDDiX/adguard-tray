"""Building blocks for the Manager pages: cards, rows, switches, banners.

Surfaces paint themselves instead of being styled. A stylesheet background on
a container leaks into its child buttons' palette and turns them flat, and an
app-wide stylesheet changes the metrics of every native widget. So cards,
rows, badges and switches paint from theme.tokens(), and every native control
keeps the desktop's own look.
"""

from PyQt6.QtCore import QEvent, QObject, QPointF, QRectF, QSize, Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QColor, QFont, QFontMetrics, QIcon, QPainter, QPalette, QPen, QPixmap
from PyQt6.QtWidgets import (
    QAbstractButton,
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QStyledItemDelegate,
    QToolButton,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
)

from . import theme
from .i18n import _t

R = QPalette.ColorRole
G = QPalette.ColorGroup

RADIUS = 8
CONTENT_WIDTH = 760      # settings pages are a centred column this wide


def scaled_font(widget: QWidget, factor: float = 1.0, bold: bool = False) -> QFont:
    font = QFont(widget.font())
    if factor != 1.0:
        font.setPointSizeF(max(8.0, QApplication.font().pointSizeF() * factor))
    font.setBold(bold)
    return font


# ── Labels ───────────────────────────────────────────────────────────────────

class ToneLabel(QLabel):
    """A label in a derived colour: "secondary" or a status tone."""

    def __init__(self, text: str = "", tone: str = "secondary", parent=None) -> None:
        super().__init__(text, parent)
        # Plain text: these show CLI output, filter titles and paths, which
        # must not turn into live links or images.
        self.setTextFormat(Qt.TextFormat.PlainText)
        self._tone = tone
        self._recolor()

    def set_tone(self, tone: str) -> None:
        if tone != self._tone:
            self._tone = tone
            self._recolor()

    def _recolor(self) -> None:
        tok = theme.tokens()
        color = tok.secondary if self._tone == "secondary" else tok.tone_text.get(self._tone, tok.text)
        pal = self.palette()
        if pal.color(G.Active, R.WindowText) == color:
            return        # also ends the PaletteChange this setPalette sends
        for group in (G.Active, G.Inactive):   # Disabled keeps the style's own grey
            pal.setColor(group, R.WindowText, color)
            pal.setColor(group, R.Text, color)
        self.setPalette(pal)

    def changeEvent(self, event) -> None:
        super().changeEvent(event)
        if event.type() == QEvent.Type.PaletteChange:
            self._recolor()


class Caption(ToneLabel):
    """Secondary text under a title: wraps, slightly smaller, never below 8 pt."""

    def __init__(self, text: str = "", parent=None, tone: str = "secondary") -> None:
        super().__init__(text, tone, parent)
        self.setWordWrap(True)
        self.setFont(scaled_font(self, 0.92))
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)


def heading(text: str, factor: float = 1.0) -> QLabel:
    label = QLabel(text)
    label.setTextFormat(Qt.TextFormat.PlainText)
    label.setFont(scaled_font(label, factor, bold=True))
    label.setWordWrap(True)
    return label


# ── Switch ───────────────────────────────────────────────────────────────────

class Switch(QCheckBox):
    """An on/off switch. A QCheckBox underneath: Space, toggled(), buddies and
    the check-box accessibility role all keep working."""

    _W, _H = 40, 22

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def sizeHint(self) -> QSize:
        return QSize(self._W + 4, self._H + 4)

    def minimumSizeHint(self) -> QSize:
        return self.sizeHint()

    def hitButton(self, pos) -> bool:
        return self.rect().contains(pos)

    def paintEvent(self, _event) -> None:
        tok = theme.tokens()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        track = QRectF(2, (self.height() - self._H) / 2, self._W, self._H)
        color = QColor(tok.accent if self.isChecked() else tok.switch_off)
        if not self.isEnabled():
            color.setAlphaF(0.4)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(color)
        p.drawRoundedRect(track, self._H / 2, self._H / 2)
        knob = self._H - 6
        x = track.right() - knob - 3 if self.isChecked() else track.left() + 3
        knob_color = QColor("#ffffff")
        if not self.isEnabled():
            knob_color.setAlphaF(0.55)
        p.setBrush(knob_color)
        p.drawEllipse(QRectF(x, track.top() + 3, knob, knob))
        if self.hasFocus():
            p.setPen(QPen(tok.accent, 2))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(track.adjusted(-1.5, -1.5, 1.5, 1.5), self._H / 2 + 1.5, self._H / 2 + 1.5)


# ── Surfaces ─────────────────────────────────────────────────────────────────

class Card(QFrame):
    """A rounded surface. Rows added with add_row() get separators between them.

    tone: None for a plain card, or "success"/"warning"/"danger"/"info" for a
    tinted one (hero, banner).
    """

    def __init__(self, tone: str | None = None, padding: int = 0, parent=None) -> None:
        super().__init__(parent)
        self._tone = tone
        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(padding, padding, padding, padding)
        self.layout_.setSpacing(0 if not padding else 8)
        self._rows: list[QWidget] = []

    def set_tone(self, tone: str | None) -> None:
        self._tone = tone
        self.update()

    def add_row(self, row: QWidget) -> QWidget:
        self._rows.append(row)
        self.layout_.addWidget(row)
        return row

    def add(self, widget: QWidget) -> QWidget:
        self.layout_.addWidget(widget)
        return widget

    def clear_rows(self) -> None:
        for row in self._rows:
            row.setParent(None)
            row.deleteLater()
        self._rows.clear()

    def paintEvent(self, _event) -> None:
        tok = theme.tokens()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        if self._tone:
            bg = tok.tint[self._tone]
            border = theme.mix(bg, tok.fill[self._tone], 0.35)
        else:
            bg, border = tok.card, tok.border
        p.setPen(QPen(border, 1))
        p.setBrush(bg)
        p.drawRoundedRect(rect, RADIUS, RADIUS)
        p.setPen(QPen(tok.separator, 1))
        first = True
        for row in self._rows:
            if row.isHidden():
                continue
            if not first:
                y = row.geometry().top() + 0.5
                p.drawLine(QPointF(12, y), QPointF(self.width() - 1, y))
            first = False


class Row(QWidget):
    """Title and subtitle on the left, controls on the right.

    A row whose control is a Switch toggles it when clicked anywhere.
    """

    def __init__(self, title: str, subtitle: str = "", control: QWidget | None = None,
                 parent=None) -> None:
        super().__init__(parent)
        self._hover = False
        self.setMinimumHeight(48)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 8, 12, 8)
        lay.setSpacing(12)
        text = QVBoxLayout()
        text.setSpacing(1)
        self.title = QLabel(title)
        self.title.setTextFormat(Qt.TextFormat.PlainText)
        self.title.setWordWrap(True)
        text.addWidget(self.title)
        self.subtitle = Caption(subtitle)
        text.addWidget(self.subtitle)
        if not subtitle:
            self.subtitle.hide()    # hide() only: showing a parentless label makes a native window
        lay.addLayout(text, 1)
        self.controls = QHBoxLayout()
        self.controls.setSpacing(6)
        lay.addLayout(self.controls)
        self.switch: Switch | None = None
        if control is not None:
            self.add_control(control)

    def add_control(self, widget: QWidget) -> QWidget:
        self.controls.addWidget(widget, 0, Qt.AlignmentFlag.AlignVCenter)
        if isinstance(widget, Switch) and self.switch is None:
            self.switch = widget
            widget.setAccessibleName(self.title.text())
            self.title.setBuddy(widget)
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        elif not widget.accessibleName() and not isinstance(widget, (QLabel, QAbstractButton)):
            # Buttons and labels announce their own text; a field is named by its row.
            widget.setAccessibleName(self.title.text())
        return widget

    def set_subtitle(self, text: str) -> None:
        self.subtitle.setText(text)
        self.subtitle.setVisible(bool(text))

    def enterEvent(self, event) -> None:
        self._hover = self.switch is not None
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if (self.switch is not None and self.switch.isEnabled()
                and event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.switch.toggle()
            self.switch.setFocus(Qt.FocusReason.MouseFocusReason)
        super().mouseReleaseEvent(event)

    def paintEvent(self, _event) -> None:
        if self._hover and self.isEnabled():
            p = QPainter(self)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(theme.tokens().hover)
            p.drawRoundedRect(QRectF(self.rect()).adjusted(1, 1, -1, -1), RADIUS - 1, RADIUS - 1)


class Badge(QWidget):
    """A small pill with an upper-case word, e.g. ACTIVE."""

    def __init__(self, text: str = "", tone: str = "info", parent=None) -> None:
        super().__init__(parent)
        self._text, self._tone = text, tone
        self.setFont(scaled_font(self, 0.8, bold=True))
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def set(self, text: str, tone: str) -> None:
        self._text, self._tone = text, tone
        self.setAccessibleName(text)
        self.updateGeometry()
        self.update()

    def sizeHint(self) -> QSize:
        fm = self.fontMetrics()
        return QSize(fm.horizontalAdvance(self._text.upper()) + 18, fm.height() + 6)

    def paintEvent(self, _event) -> None:
        tok = theme.tokens()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(tok.badge[self._tone])
        r = QRectF(self.rect())
        p.drawRoundedRect(r, r.height() / 2, r.height() / 2)
        p.setPen(tok.tone_text[self._tone])
        p.drawText(r, Qt.AlignmentFlag.AlignCenter, self._text.upper())


class StatTile(QToolButton):
    """A big number with a caption. Clickable when it leads somewhere."""

    def __init__(self, caption: str, parent=None, tone: str | None = None) -> None:
        super().__init__(parent)
        self._value, self._caption, self._tone = "–", caption, tone
        self._hover = False
        self.setAutoRaise(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def set_value(self, value: str, hint: str = "") -> None:
        self._value = value
        self.setToolTip(hint)
        self.setAccessibleName(f"{self._caption}: {value}")
        self.update()

    def set_caption(self, caption: str) -> None:
        self._caption = caption
        self.update()

    def set_link(self, callback) -> None:
        self.clicked.connect(callback)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _fonts(self) -> tuple[QFont, QFont]:
        return scaled_font(self, 1.45, bold=True), scaled_font(self, 0.92)

    def sizeHint(self) -> QSize:
        big, small = self._fonts()
        h = QFontMetrics(big).height() + QFontMetrics(small).height() + 20
        return QSize(120, h)

    def enterEvent(self, event) -> None:
        self._hover = self.focusPolicy() != Qt.FocusPolicy.NoFocus
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, _event) -> None:
        tok = theme.tokens()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        if self._hover or self.hasFocus():
            p.setPen(QPen(tok.accent, 2) if self.hasFocus() else Qt.PenStyle.NoPen)
            p.setBrush(tok.hover)
            p.drawRoundedRect(r, RADIUS, RADIUS)
        big, small = self._fonts()
        p.setFont(big)
        p.setPen(tok.text)
        fm = p.fontMetrics()
        p.drawText(QRectF(r.left() + 12, r.top() + 8, r.width() - 24, fm.height()),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._value)
        top = r.top() + 8 + fm.height()
        p.setFont(small)
        sfm = p.fontMetrics()
        left = r.left() + 12
        if self._tone:
            # A dot in the series colour ties the tile to the chart legend.
            dot = 8
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(tok.fill.get(self._tone, tok.accent) if self._tone != "allowed" else tok.chart_allowed)
            p.drawEllipse(QRectF(left, top + (sfm.height() - dot) / 2 + 1, dot, dot))
            left += dot + 6
        p.setPen(tok.secondary)
        text = sfm.elidedText(self._caption, Qt.TextElideMode.ElideRight, int(r.right() - 12 - left))
        p.drawText(QRectF(left, top, r.right() - 12 - left, sfm.height() + 2),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)


class Banner(Card):
    """An inline message at the top of a page: info, success, warning or error.

    Errors stay until closed; long raw output goes behind "Details".
    """

    def __init__(self, parent=None) -> None:
        super().__init__(tone="info", padding=0, parent=parent)
        row = QHBoxLayout()
        row.setContentsMargins(14, 8, 8, 8)
        row.setSpacing(10)
        self.text = QLabel("")
        self.text.setWordWrap(True)
        self.text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.text.setTextFormat(Qt.TextFormat.PlainText)
        row.addWidget(self.text, 1)
        self.action = QPushButton()
        self.action.hide()
        row.addWidget(self.action, 0, Qt.AlignmentFlag.AlignVCenter)
        self.btn_details = QPushButton(_t("Details"))
        self.btn_details.setCheckable(True)
        self.btn_details.hide()
        row.addWidget(self.btn_details, 0, Qt.AlignmentFlag.AlignVCenter)
        close = QToolButton()
        close.setAutoRaise(True)
        close.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton))
        close.setToolTip(_t("Close"))
        close.setAccessibleName(_t("Close"))
        close.clicked.connect(self.hide)
        row.addWidget(close, 0, Qt.AlignmentFlag.AlignTop)
        self.layout_.addLayout(row)
        self.details = QPlainTextEdit()
        self.details.setReadOnly(True)
        self.details.setMaximumHeight(160)
        self.details.hide()
        self.layout_.addWidget(self.details)
        self.btn_details.toggled.connect(self.details.setVisible)
        # Someone reading the details keeps the message up.
        self.btn_details.toggled.connect(lambda on: self._timer.stop() if on else None)
        self._callback = None
        self.action.clicked.connect(self._on_action)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)
        self.hide()

    def show_message(self, text: str, tone: str = "info", details: str = "",
                     action: str = "", callback=None, timeout_ms: int = 0) -> None:
        self.set_tone({"error": "danger"}.get(tone, tone))
        self.text.setText(text)
        self.details.setPlainText(details)
        lines = min(details.count("\n") + 1, 10)
        self.details.setFixedHeight(self.details.fontMetrics().lineSpacing() * lines + 14)
        self.btn_details.setVisible(bool(details))
        self.btn_details.setChecked(False)
        self.action.setText(action)
        self.action.setVisible(bool(action))
        self._callback = callback
        self._timer.stop()
        if timeout_ms:
            self._timer.start(timeout_ms)
        self.show()

    def _on_action(self) -> None:
        callback = self._callback
        self.hide()
        if callback:
            callback()


# ── Pages ────────────────────────────────────────────────────────────────────

class Page(QScrollArea):
    """A scrolling page with a centred column of sections.

    wide=True gives list pages (activity, filters) the full width and no outer
    scroll bar, so their own view fills the height instead of nesting.
    """

    def __init__(self, wide: bool = False, parent=None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)   # not a silent Tab stop
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        if wide:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        outer = QWidget()
        outer.setAutoFillBackground(False)
        h = QHBoxLayout(outer)
        h.setContentsMargins(24, 16, 24, 20)
        self._outer = h
        # Reserve the scroll bar's width while it is hidden, so the centred
        # column doesn't shift between pages that scroll and pages that don't.
        self.verticalScrollBar().installEventFilter(self)
        column = QWidget()
        if not wide:
            column.setMaximumWidth(CONTENT_WIDTH)
        col = QVBoxLayout(column)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(10)
        h.addStretch(1)
        h.addWidget(column, 1000)
        h.addStretch(1)
        self.setWidget(outer)
        self.viewport().setAutoFillBackground(False)
        # The banner sits outside `content`, so it stays usable when the
        # content is disabled (e.g. proxy.yaml missing).
        self.banner = Banner()
        col.addWidget(self.banner)
        self.content = QWidget()
        self.body = QVBoxLayout(self.content)
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setSpacing(6)
        col.addWidget(self.content, 1)
        self._wide = wide
        self._finished = False

    def section(self, title: str = "", description: str = "") -> Card:
        """Heading, optional description, and a card for rows.

        No title for a page's first card when the page title already says it.
        """
        if self.body.count():
            self.body.addSpacing(16)
        if title:
            self.body.addWidget(heading(title))
        if description:
            self.body.addWidget(Caption(description))
        self.body.addSpacing(4)
        card = Card()
        self.body.addWidget(card)
        return card

    def add(self, widget: QWidget, stretch: int = 0) -> QWidget:
        self.body.addWidget(widget, stretch)
        return widget

    def finish(self) -> None:
        """Push content to the top on settings pages."""
        if not self._wide and not self._finished:
            self.body.addStretch(1)
            self._finished = True

    def eventFilter(self, obj, event) -> bool:
        if obj is self.verticalScrollBar() and event.type() in (QEvent.Type.Show, QEvent.Type.Hide):
            extent = 0 if self._wide or obj.isVisible() else obj.sizeHint().width()
            self._outer.setContentsMargins(24, 16, 24 + extent, 20)
        return super().eventFilter(obj, event)


# ── Dialogs ──────────────────────────────────────────────────────────────────

def confirm(parent, title: str, text: str, action: str, destructive: bool = True) -> bool:
    """Ask before something costly; Cancel is preselected and Esc cancels."""
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Warning if destructive else QMessageBox.Icon.Question)
    box.setWindowTitle(title)
    box.setText(text)
    box.setTextFormat(Qt.TextFormat.PlainText)   # names in the text come from filter lists
    go = box.addButton(action, QMessageBox.ButtonRole.DestructiveRole if destructive
                       else QMessageBox.ButtonRole.AcceptRole)
    cancel = box.addButton(_t("Cancel"), QMessageBox.ButtonRole.RejectRole)
    box.setDefaultButton(cancel)
    box.setEscapeButton(cancel)
    box.exec()
    return box.clickedButton() is go


# ── Icons ────────────────────────────────────────────────────────────────────

def theme_icon(names, color: QColor | None = None, size: int = 16) -> QIcon | None:
    """The first icon the desktop's theme has, tinted to *color*; None if none.

    Symbolic icons from Adwaita come out near-black whatever the palette, so
    they are recoloured; Breeze's monochrome icons take the tint the same way.
    """
    for name in names:
        if not QIcon.hasThemeIcon(name):
            continue
        icon = QIcon.fromTheme(name)
        if color is None:
            return icon
        tinted = QIcon()
        for scale in (1, 2):
            pm = icon.pixmap(size * scale, size * scale)
            if pm.isNull():
                continue
            out = QPixmap(pm.size())
            out.fill(Qt.GlobalColor.transparent)
            painter = QPainter(out)
            painter.drawPixmap(0, 0, pm)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            painter.fillRect(out.rect(), color)
            painter.end()
            out.setDevicePixelRatio(scale)
            tinted.addPixmap(out)
        return tinted
    return None


class Spinner(QWidget):
    """A small busy indicator; hidden while idle."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._angle = 0
        self._timer = QTimer(self)
        self._timer.setInterval(80)
        self._timer.timeout.connect(self._tick)
        self.setFixedSize(18, 18)
        policy = self.sizePolicy()
        policy.setRetainSizeWhenHidden(True)   # rows don't jump when it shows
        self.setSizePolicy(policy)
        self.hide()

    def set_busy(self, busy: bool) -> None:
        self.setVisible(busy)
        if busy:
            self._timer.start()
        else:
            self._timer.stop()

    def _tick(self) -> None:
        self._angle = (self._angle + 30) % 360
        self.update()

    def paintEvent(self, _event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(theme.tokens().accent, 2.2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        p.drawArc(QRectF(2, 2, 14, 14), -self._angle * 16, 270 * 16)


class LinkButton(QPushButton):
    """A flat button in the accent colour that navigates, e.g. "Details"."""

    def __init__(self, text: str, callback=None, parent=None) -> None:
        super().__init__(text, parent)
        self.setFlat(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if callback:
            self.clicked.connect(callback)
        self._recolor()

    def _recolor(self) -> None:
        color = theme.tokens().accent_text
        pal = self.palette()
        if pal.color(G.Active, R.ButtonText) == color:
            return
        for group in (G.Active, G.Inactive):
            pal.setColor(group, R.ButtonText, color)
        self.setPalette(pal)

    def changeEvent(self, event) -> None:
        super().changeEvent(event)
        if event.type() == QEvent.Type.PaletteChange:
            self._recolor()


class _IdleWheel(QObject):
    def eventFilter(self, obj, event) -> bool:
        if event.type() == QEvent.Type.Wheel and not obj.hasFocus():
            event.ignore()      # handled here, but ignored: the page scrolls instead
            return True
        return False


_idle_wheel: _IdleWheel | None = None


def ignore_idle_wheel(widget):
    """Let the wheel scroll the page over a combo or spin box that the user
    hasn't clicked into, instead of silently changing its value."""
    global _idle_wheel
    if _idle_wheel is None:
        _idle_wheel = _IdleWheel(QApplication.instance())
    widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    widget.installEventFilter(_idle_wheel)
    return widget


# ── Lists ────────────────────────────────────────────────────────────────────

SUBTITLE_ROLE = Qt.ItemDataRole.UserRole + 1   # second line under the title
BADGE_ROLE = Qt.ItemDataRole.UserRole + 2      # (text, tone), e.g. ("Custom", "info")


class ListDelegate(QStyledItemDelegate):
    """Rows for QTreeWidget lists: title, subtitle, optional badge, and a switch
    in place of the check box. Top-level items without a check state draw as
    group headings.

    The item's check state is still the source of truth, so itemChanged and the
    existing toggle code keep working. Only a click on the switch (or Space)
    toggles; a click elsewhere just selects the row.
    """

    SW_W, SW_H = 40, 22

    def __init__(self, parent=None, headings: bool = True) -> None:
        super().__init__(parent)
        self._headings = headings

    @staticmethod
    def _checked(index) -> bool:
        # QTreeWidgetItem hands the state back as an int, setData() as an enum.
        value = index.data(Qt.ItemDataRole.CheckStateRole)
        return getattr(value, "value", value) == Qt.CheckState.Checked.value

    def _is_heading(self, index) -> bool:
        return self._headings and not index.parent().isValid() and index.data(Qt.ItemDataRole.CheckStateRole) is None

    def _switch_rect(self, rect) -> QRectF:
        return QRectF(rect.right() - self.SW_W - 12, rect.center().y() - self.SW_H / 2 + 1,
                      self.SW_W, self.SW_H)

    def sizeHint(self, option, index) -> QSize:
        fm = option.fontMetrics
        if self._is_heading(index):
            return QSize(100, fm.height() + 22)
        lines = 2 if index.data(SUBTITLE_ROLE) else 1
        return QSize(100, max(44, fm.height() * lines + 18))

    def paint(self, painter, option, index) -> None:
        tok = theme.tokens()
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(option.rect)
        font = QFont(option.font)
        if self._is_heading(index):
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(tok.text)
            painter.drawText(rect.adjusted(12, 10, -12, -2),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                             str(index.data() or ""))
            painter.restore()
            return
        enabled = bool(option.state & QStyle.StateFlag.State_Enabled)
        if option.state & QStyle.StateFlag.State_Selected:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(tok.selected)
            painter.drawRoundedRect(rect.adjusted(2, 1, -2, -1), 6, 6)
        elif option.state & QStyle.StateFlag.State_MouseOver:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(tok.hover)
            painter.drawRoundedRect(rect.adjusted(2, 1, -2, -1), 6, 6)
        checkable = index.data(Qt.ItemDataRole.CheckStateRole) is not None
        right = self._switch_rect(option.rect).left() - 12 if checkable else rect.right() - 12
        text_rect = QRectF(rect.left() + 14, rect.top(), right - rect.left() - 14, rect.height())
        subtitle = index.data(SUBTITLE_ROLE)
        fm = option.fontMetrics
        title_h = fm.height()
        top = rect.center().y() - (title_h * (2 if subtitle else 1)) / 2
        title = str(index.data() or "")
        painter.setFont(font)
        painter.setPen(tok.text if enabled else tok.secondary)
        badge = index.data(BADGE_ROLE)
        badge_w = 0
        if badge:
            small = scaled_font(option.widget, 0.8, bold=True) if option.widget else font
            badge_w = QFontMetrics(small).horizontalAdvance(str(badge[0]).upper()) + 18
        shown = fm.elidedText(title, Qt.TextElideMode.ElideRight, int(text_rect.width() - badge_w - 8))
        painter.drawText(QRectF(text_rect.left(), top, text_rect.width(), title_h),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, shown)
        if badge:
            text, tone = badge
            bx = text_rect.left() + fm.horizontalAdvance(shown) + 8
            small = scaled_font(option.widget, 0.8, bold=True) if option.widget else font
            bh = QFontMetrics(small).height() + 4
            brect = QRectF(bx, top + (title_h - bh) / 2, badge_w, bh)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(tok.badge[tone])
            painter.drawRoundedRect(brect, bh / 2, bh / 2)
            painter.setFont(small)
            painter.setPen(tok.tone_text[tone])
            painter.drawText(brect, Qt.AlignmentFlag.AlignCenter, str(text).upper())
            painter.setFont(font)
        if subtitle:
            small = QFont(font)
            small.setPointSizeF(max(8.0, font.pointSizeF() * 0.92))
            painter.setFont(small)
            painter.setPen(tok.secondary)
            sfm = QFontMetrics(small)
            painter.drawText(QRectF(text_rect.left(), top + title_h, text_rect.width(), sfm.height() + 2),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                             sfm.elidedText(str(subtitle), Qt.TextElideMode.ElideRight,
                                            int(text_rect.width())))
        if checkable:
            on = self._checked(index)
            sw = self._switch_rect(option.rect)
            color = QColor(tok.accent if on else tok.switch_off)
            if not enabled:
                color.setAlphaF(0.4)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            painter.drawRoundedRect(sw, self.SW_H / 2, self.SW_H / 2)
            knob = self.SW_H - 6
            x = sw.right() - knob - 3 if on else sw.left() + 3
            knob_color = QColor("#ffffff")
            if not enabled:
                knob_color.setAlphaF(0.55)
            painter.setBrush(knob_color)
            painter.drawEllipse(QRectF(x, sw.top() + 3, knob, knob))
            if option.state & QStyle.StateFlag.State_HasFocus:
                painter.setPen(QPen(tok.accent, 2))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawRoundedRect(sw.adjusted(-1.5, -1.5, 1.5, 1.5), 12.5, 12.5)
        painter.restore()

    def editorEvent(self, event, model, option, index) -> bool:
        if index.data(Qt.ItemDataRole.CheckStateRole) is None:
            return False
        if not (index.flags() & Qt.ItemFlag.ItemIsUserCheckable and index.flags() & Qt.ItemFlag.ItemIsEnabled):
            return False
        toggle = False
        if event.type() == QEvent.Type.MouseButtonRelease:
            toggle = self._switch_rect(option.rect).contains(event.position())
        elif event.type() == QEvent.Type.MouseButtonPress:
            # Keep the press from starting a drag-select on the switch.
            return self._switch_rect(option.rect).contains(event.position())
        elif event.type() == QEvent.Type.KeyPress:
            toggle = event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Select)
        if not toggle:
            return False
        on = self._checked(index)
        return model.setData(index, Qt.CheckState.Unchecked if on else Qt.CheckState.Checked,
                             Qt.ItemDataRole.CheckStateRole)


def style_list(tree: QTreeWidget, headings: bool = True) -> ListDelegate:
    """Make a QTreeWidget look like the rest: one column of rows with switches,
    group headings, no header, no expander arrows, inside a Card.

    headings=False for a flat list whose top-level items are rows.
    """
    delegate = ListDelegate(tree, headings)
    # The card paints the surface; the view only draws rows on it.
    tree.viewport().setAutoFillBackground(False)
    tree.setItemDelegate(delegate)
    tree.setHeaderHidden(True)
    tree.setRootIsDecorated(False)
    tree.setIndentation(0)
    tree.setUniformRowHeights(False)
    tree.setAlternatingRowColors(False)
    tree.setMouseTracking(True)
    tree.setFrameShape(QFrame.Shape.NoFrame)
    tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    tree.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
    tree.setItemsExpandable(False)
    return delegate


def list_card(tree: QTreeWidget) -> Card:
    """The tree inside a card, with a little padding so its square corners sit
    inside the card's rounded border."""
    card = Card(padding=4)
    card.add(tree)
    return card


def one_line(text: str) -> str:
    """A former multi-line tooltip as one line of row description.

    A line break next to CJK text or full-width punctuation just goes away;
    elsewhere it becomes a space.
    """
    import re
    text = re.sub(r"(?<=[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef])\n|\n(?=[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef])",
                  "", text)
    return text.replace("\n", " ")


class _TableTint(QObject):
    """Keeps a styled table's surface in step with the theme."""

    def __init__(self, table) -> None:
        super().__init__(table)
        self._table = table
        theme.watcher().changed.connect(self.apply)
        self.apply()

    @pyqtSlot()     # a real slot: Qt drops the connection when the table goes
    def apply(self) -> None:
        tok = theme.tokens()
        pal = self._table.palette()
        for group in (G.Active, G.Inactive):
            pal.setColor(group, R.Base, tok.card)
            pal.setColor(group, R.AlternateBase, theme.mix(tok.card, tok.text, 0.03))
        self._table.setPalette(pal)


def style_table(table) -> None:
    """A QTableWidget on a card: card-coloured surface (not a dark well), no
    frame, and Tab leaves the table instead of walking its cells."""
    table.setFrameShape(QFrame.Shape.NoFrame)
    table.setTabKeyNavigation(False)
    _TableTint(table)


class EmptyState(QLabel):
    """A centred message over a list's viewport: "No filters installed."."""

    def __init__(self, view) -> None:
        super().__init__(view.viewport())
        self._view = view
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWordWrap(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setFont(scaled_font(self, 0.95))
        view.viewport().installEventFilter(self)
        self.hide()

    def set(self, text: str) -> None:
        """Show *text*, or hide the message when it is empty."""
        self.setText(text)
        self._place()
        self.setVisible(bool(text))

    def _place(self) -> None:
        self.setGeometry(self._view.viewport().rect().adjusted(24, 12, -24, -12))
        tok = theme.tokens()
        pal = self.palette()
        if pal.color(G.Active, R.WindowText) != tok.secondary:
            for group in (G.Active, G.Inactive):
                pal.setColor(group, R.WindowText, tok.secondary)
            self.setPalette(pal)

    def eventFilter(self, obj, event) -> bool:
        if event.type() == QEvent.Type.Resize:
            self._place()
        return False

    def changeEvent(self, event) -> None:
        super().changeEvent(event)
        if event.type() == QEvent.Type.PaletteChange and self.isVisible():
            self._place()


def plain_tip(text: str) -> str:
    """A tooltip that shows *text* literally. Tooltips guess rich text, and
    these carry URLs, filter titles and script names from the outside."""
    import html
    return "<p>" + html.escape(text).replace("\n", "<br>") + "</p>" if text else ""
