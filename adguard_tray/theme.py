"""Light/dark handling and the colours the custom widgets paint with.

The system palette stays in charge. Breeze, qt6ct and the GTK theme push their
colours into it, native widgets follow it on their own, and everything drawn
here is derived from it. This module only steps in where the palette cannot be
trusted, all of it measured with Qt 6.4 and 6.11:

* Qt's GNOME, GTK and portal themes report a colour-scheme change live but keep
  the palette they started with. A session without a Qt platform theme
  (Hyprland, sway) reports no scheme at all, and Qt 6.4 has no colour-scheme
  API. The xdg portal is therefore read directly, and when the wanted scheme
  and the palette disagree a built-in palette is installed.
* Status colours are fixed hues, moved towards the text colour until they reach
  4.5:1 on the surfaces they sit on – Breeze's own positive/negative colours
  and raw accent colours fail that on white.
"""

import logging
import os

from PyQt6.QtCore import QEvent, QObject, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QColor, QGuiApplication, QPalette

try:
    from PyQt6.QtDBus import (
        QDBusConnection,
        QDBusMessage,
        QDBusPendingCallWatcher,
        QDBusPendingReply,
        QDBusVariant,
    )
except ImportError:  # a PyQt6 build without QtDBus: no portal, the rest still works
    QDBusConnection = None

logger = logging.getLogger(__name__)

R = QPalette.ColorRole
G = QPalette.ColorGroup

APPEARANCES = ("", "light", "dark")   # "" follows the system


# ── Colour maths ─────────────────────────────────────────────────────────────

def _luminance(c: QColor) -> float:
    def ch(v: float) -> float:
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c.redF()) + 0.7152 * ch(c.greenF()) + 0.0722 * ch(c.blueF())


def contrast(a: QColor, b: QColor) -> float:
    la, lb = _luminance(a), _luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def mix(a: QColor, b: QColor, t: float) -> QColor:
    """*a* moved the fraction *t* towards *b*."""
    return QColor.fromRgbF(
        a.redF() + (b.redF() - a.redF()) * t,
        a.greenF() + (b.greenF() - a.greenF()) * t,
        a.blueF() + (b.blueF() - a.blueF()) * t,
    )


def ensure_contrast(color: QColor, surfaces, ratio: float, towards: QColor) -> QColor:
    """*color*, moved towards *towards* until it reaches *ratio* on every surface."""
    for step in range(21):
        c = mix(color, towards, step / 20)
        if all(contrast(c, s) >= ratio for s in surfaces):
            return c
    return QColor(towards)


def is_dark(palette: QPalette) -> bool:
    return palette.color(R.Window).lightness() < palette.color(R.WindowText).lightness()


# ── Tokens ───────────────────────────────────────────────────────────────────

# Fixed hues per scheme: (success, warning, danger, chart "allowed").
_HUES = {
    False: ("#16a34a", "#d97706", "#dc2626", "#5b8ec9"),
    True: ("#22c55e", "#f59e0b", "#ef4444", "#4a88c7"),
}


class Tokens:
    """Every colour the custom widgets use, derived from one palette."""

    def __init__(self, pal: QPalette) -> None:
        self.dark = is_dark(pal)
        window, text = pal.color(R.Window), pal.color(R.WindowText)
        base, accent = pal.color(R.Base), pal.color(R.Highlight)
        self.window, self.text = window, text
        # Dark cards sit a step above the window: dark palettes paint fields
        # in Base, darker than the window, and Fusion's field frame is darker
        # still – on a Base-coloured card an input would have no visible edge.
        self.card = mix(window, text, 0.05) if self.dark else base
        card = self.card
        self.border = mix(card, text, 0.14)
        self.separator = mix(card, text, 0.08)
        self.hover = mix(card, text, 0.05)
        self.selected = mix(card, accent, 0.18)
        self.sidebar = mix(window, text, 0.04)
        self.sidebar_hover = mix(self.sidebar, text, 0.06)
        self.sidebar_selected = mix(self.sidebar, accent, 0.22)
        surfaces = (card, base, window, self.sidebar, pal.color(R.AlternateBase))
        self.secondary = ensure_contrast(mix(text, card, 0.55), surfaces, 4.5, text)
        self.accent = ensure_contrast(accent, (card, base, window), 3.0, text)
        self.accent_text = ensure_contrast(accent, (card, base, window), 4.5, text)
        self.switch_off = ensure_contrast(mix(card, text, 0.3), (card,), 3.0, text)
        success, warning, danger, allowed = (QColor(h) for h in _HUES[self.dark])
        self.chart_allowed = allowed
        self.chart_blocked = danger
        self.fill = {"success": success, "warning": warning, "danger": danger, "info": self.accent}
        self.tone_text = {}
        self.tint = {}
        self.badge = {}
        for tone, fill in self.fill.items():
            tint = mix(card, fill, 0.10)
            badge = mix(card, fill, 0.18)
            self.tint[tone], self.badge[tone] = tint, badge
            self.tone_text[tone] = ensure_contrast(fill, surfaces + (tint, badge), 4.5, text)


_cache: dict[int, Tokens] = {}


def tokens(palette: QPalette | None = None) -> Tokens:
    pal = palette if palette is not None else QGuiApplication.palette()
    key = pal.cacheKey()
    tok = _cache.get(key)
    if tok is None:
        if len(_cache) > 16:
            _cache.clear()
        tok = _cache[key] = Tokens(pal)
    return tok


# ── Built-in palettes ────────────────────────────────────────────────────────

# Breeze's colours. Used only when the desktop asks for a scheme the Qt palette
# does not have (see the module docstring), or when the user picks one.
_BUILTIN = {
    False: dict(window="#eff0f1", text="#232629", base="#ffffff", alt="#f7f7f7",
                button="#fcfcfc", accent="#3daee9", accent_text="#ffffff",
                link="#2980b9", disabled="#a0a1a3", tooltip="#f7f7f7", placeholder="#707d8a"),
    True: dict(window="#202326", text="#fcfcfc", base="#141618", alt="#1d1f22",
               button="#292c30", accent="#3daee9", accent_text="#fcfcfc",
               link="#1d99f3", disabled="#6e7175", tooltip="#292c30", placeholder="#8a8f94"),
}


def builtin_palette(dark: bool) -> QPalette:
    c = {k: QColor(v) for k, v in _BUILTIN[dark].items()}
    # This constructor derives Light/Midlight/Mid/Dark/Shadow from the button
    # colour, which Fusion needs for bevels and check-box outlines.
    pal = QPalette(c["button"], c["window"])
    for group in (G.Active, G.Inactive, G.Disabled):
        text = c["disabled"] if group == G.Disabled else c["text"]
        pal.setColor(group, R.Window, c["window"])
        pal.setColor(group, R.WindowText, text)
        pal.setColor(group, R.Base, c["base"] if group != G.Disabled else c["window"])
        pal.setColor(group, R.AlternateBase, c["alt"])
        pal.setColor(group, R.Text, text)
        pal.setColor(group, R.Button, c["button"])
        pal.setColor(group, R.ButtonText, text)
        pal.setColor(group, R.BrightText, c["accent_text"])
        pal.setColor(group, R.Highlight, c["accent"] if group != G.Disabled else c["disabled"])
        pal.setColor(group, R.HighlightedText, c["accent_text"])
        pal.setColor(group, R.Link, c["link"])
        pal.setColor(group, R.ToolTipBase, c["tooltip"])
        pal.setColor(group, R.ToolTipText, c["text"])
        pal.setColor(group, R.PlaceholderText, c["placeholder"])
    return pal


# ── The xdg portal's colour scheme ──────────────────────────────────────────

class _Portal(QObject):
    """org.freedesktop.appearance color-scheme: 0 none, 1 dark, 2 light."""

    changed = pyqtSignal()
    _SVC = "org.freedesktop.portal.Desktop"
    _PATH = "/org/freedesktop/portal/desktop"
    _IFACE = "org.freedesktop.portal.Settings"
    _NS, _KEY = "org.freedesktop.appearance", "color-scheme"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.value = 0
        if QDBusConnection is None:
            return
        self._bus = QDBusConnection.sessionBus()
        if not self._bus.isConnected():
            return
        self._bus.connect(self._SVC, self._PATH, self._IFACE, "SettingChanged", self._on_setting)
        self._ask("ReadOne")

    def _ask(self, method: str) -> None:
        msg = QDBusMessage.createMethodCall(self._SVC, self._PATH, self._IFACE, method)
        msg.setArguments([self._NS, self._KEY])
        watcher = QDBusPendingCallWatcher(self._bus.asyncCall(msg, 2000), self)
        watcher.finished.connect(lambda w, m=method: self._on_reply(w, m))

    def _on_reply(self, watcher, method: str) -> None:
        reply = QDBusPendingReply(watcher)
        watcher.deleteLater()
        if not reply.isError():
            self._set(reply.argumentAt(0))
        elif method == "ReadOne" and reply.error().name() == "org.freedesktop.DBus.Error.UnknownMethod":
            self._ask("Read")   # portals before 1.15 only have Read

    def _on_setting(self, message) -> None:
        namespace, key, value = (message.arguments() + [None, None, None])[:3]
        if namespace == self._NS and key == self._KEY:
            self._set(value)

    if QDBusConnection is not None:
        # Typed (str, str, QDBusVariant) slots fail to connect on PyQt6 6.4;
        # taking the whole message works on every version (measured).
        _on_setting = pyqtSlot(QDBusMessage)(_on_setting)

    def _set(self, value) -> None:
        while QDBusConnection is not None and isinstance(value, QDBusVariant):
            value = value.variant()   # Read() nests the value one level deeper than ReadOne()
        try:
            value = int(value)
        except (TypeError, ValueError):
            value = 0
        if value != self.value:
            self.value = value
            self.changed.emit()


# ── The watcher ──────────────────────────────────────────────────────────────

class ThemeWatcher(QObject):
    """Decides which palette the app uses and says when it changed.

    `changed` is emitted synchronously, in the same pass as the palette change,
    so scoped stylesheets never paint a frame against the other scheme.
    """

    changed = pyqtSignal()

    def __init__(self, app) -> None:
        super().__init__(app)
        self._app = app
        self._mode = ""
        self._forced: bool | None = None     # the built-in palette in use, if any
        self._busy = False
        self._key = None
        # On KDE (and with qt5ct/qt6ct) the palette already is the user's
        # choice and follows the colour scheme live; portal-kde even announces
        # the new scheme before the palette arrives, so steering there would
        # replace a custom scheme with ours.
        desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
        platform_theme = os.environ.get("QT_QPA_PLATFORMTHEME", "").lower()
        self._palette_follows = "kde" in desktop or platform_theme in ("kde", "qt5ct", "qt6ct")
        self._portal = _Portal(self)
        self._portal.changed.connect(self._evaluate)
        hints = app.styleHints()
        if hasattr(hints, "colorSchemeChanged"):          # Qt >= 6.5
            hints.colorSchemeChanged.connect(self._evaluate)
        app.installEventFilter(self)
        self._evaluate()

    def set_mode(self, mode: str) -> None:
        self._mode = mode if mode in APPEARANCES else ""
        self._evaluate()

    def eventFilter(self, obj, event) -> bool:
        if obj is self._app and event.type() in (
                QEvent.Type.ApplicationPaletteChange, QEvent.Type.ApplicationFontChange):
            self._evaluate(force=event.type() == QEvent.Type.ApplicationFontChange)
        return False

    def wanted_dark(self) -> bool | None:
        """What the user or the desktop asks for; None to keep the palette."""
        if self._mode:
            return self._mode == "dark"
        if self._palette_follows:
            return None
        # The portal first: Qt's gtk3 theme reports the GTK theme's scheme at
        # startup even when the portal says otherwise.
        if self._portal.value in (1, 2):
            return self._portal.value == 1
        hints = self._app.styleHints()
        if hasattr(hints, "colorScheme"):                  # Qt >= 6.5; 6.4 has no enum either
            scheme = getattr(hints.colorScheme(), "value", 0)
            if scheme in (1, 2):                           # Light, Dark
                return scheme == 2
        return None

    def _evaluate(self, *_args, force: bool = False) -> None:
        if self._busy:
            return
        self._busy = True
        try:
            want = self.wanted_dark()
            if self._forced is not None and want != self._forced:
                # Back to the system palette first: it may have caught up.
                self._app.setPalette(QPalette())
                self._forced = None
            if want is not None and self._forced is None and is_dark(self._app.palette()) != want:
                logger.debug("Palette does not match the %s scheme – using the built-in one",
                             "dark" if want else "light")
                self._app.setPalette(builtin_palette(want))
                self._forced = want
            pal = self._app.palette()
            key = tuple(pal.color(r).rgba() for r in
                        (R.Window, R.WindowText, R.Base, R.Text, R.Highlight, R.Button))
            if key != self._key or force:
                # Qt sends a burst of palette events per switch; restyle once.
                self._key = key
                self.changed.emit()
        finally:
            self._busy = False


_watcher: ThemeWatcher | None = None


def watcher() -> ThemeWatcher:
    """The app-wide watcher, created on first use."""
    global _watcher
    app = QGuiApplication.instance()
    if _watcher is None or _watcher.parent() is not app:
        _watcher = ThemeWatcher(app)
    return _watcher


def set_appearance(mode: str) -> None:
    watcher().set_mode(mode)


if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication
    _app = QApplication(sys.argv[:1] + ["-platform", "offscreen"])
    assert round(contrast(QColor("#000"), QColor("#fff")), 1) == 21.0
    assert round(contrast(QColor("#777"), QColor("#fff")), 2) == 4.48
    for dark in (False, True):
        t = Tokens(builtin_palette(dark))
        assert t.dark is dark
        for tone in ("success", "warning", "danger"):
            for surface in (t.card, t.window, t.tint[tone], t.badge[tone]):
                assert contrast(t.tone_text[tone], surface) >= 4.5, (dark, tone)
        assert contrast(t.secondary, t.card) >= 4.5 and contrast(t.secondary, t.sidebar) >= 4.5
        assert contrast(t.accent, t.card) >= 3.0 and contrast(t.switch_off, t.card) >= 3.0
    w = watcher()
    w.set_mode("dark")
    assert is_dark(_app.palette())
    w.set_mode("light")
    assert not is_dark(_app.palette())
    w.set_mode("")
    print("theme ok")
