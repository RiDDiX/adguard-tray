"""
Tray icons drawn via QPainter (no QtSvg dependency).

Icon set:
  icon_active()   – green shield with checkmark
  icon_inactive() – grey shield with X
  icon_error()    – red shield with !
  icon_unknown()  – amber shield with ?
"""

from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPixmap, QPen

_CACHE: dict[str, QIcon] = {}


def _make_icon(
    fill_hex: str,
    border_hex: str,
    symbol: str,  # "check" | "x" | "exclaim" | "question"
    size: int = 64,
) -> QIcon:
    key = f"{fill_hex}:{symbol}:{size}"
    if key in _CACHE:
        return _CACHE[key]

    px = QPixmap(size, size)
    px.fill(Qt.GlobalColor.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    s = float(size)
    m = s * 0.06  # margin

    # ── Shield path ───────────────────────────────────────────────────────
    # Top flat with two upper corners, sides, bottom point
    path = QPainterPath()
    path.moveTo(s * 0.5, m)                          # top-centre
    path.lineTo(s - m, m + s * 0.18)                 # top-right
    path.lineTo(s - m, s * 0.56)                     # right mid
    path.quadTo(s - m, s * 0.84, s * 0.5, s - m)    # bottom-right → tip
    path.quadTo(m,     s * 0.84, m,       s * 0.56) # bottom-left ← tip
    path.lineTo(m, m + s * 0.18)                     # left mid
    path.closeSubpath()

    # Drop shadow (subtle)
    p.save()
    p.translate(s * 0.03, s * 0.04)
    p.fillPath(path, QColor(0, 0, 0, 45))
    p.restore()

    # Fill
    p.fillPath(path, QColor(fill_hex))

    # Border
    border_pen = QPen(QColor(border_hex), s * 0.055)
    border_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    p.strokePath(path, border_pen)

    # ── Symbol ────────────────────────────────────────────────────────────
    sym_pen = QPen(
        QColor("#ffffff"),
        s * 0.10,
        Qt.PenStyle.SolidLine,
        Qt.PenCapStyle.RoundCap,
        Qt.PenJoinStyle.RoundJoin,
    )
    p.setPen(sym_pen)

    cx, cy = s * 0.5, s * 0.54  # centre of symbol area

    if symbol == "check":
        # Checkmark: short left stroke + long right stroke
        p.drawLine(
            QPoint(int(cx - s * 0.18), int(cy + s * 0.01)),
            QPoint(int(cx - s * 0.04), int(cy + s * 0.15)),
        )
        p.drawLine(
            QPoint(int(cx - s * 0.04), int(cy + s * 0.15)),
            QPoint(int(cx + s * 0.19), int(cy - s * 0.13)),
        )

    elif symbol == "x":
        r = s * 0.16
        p.drawLine(
            QPoint(int(cx - r), int(cy - r)),
            QPoint(int(cx + r), int(cy + r)),
        )
        p.drawLine(
            QPoint(int(cx + r), int(cy - r)),
            QPoint(int(cx - r), int(cy + r)),
        )

    elif symbol == "exclaim":
        p.drawLine(
            QPoint(int(cx), int(cy - s * 0.20)),
            QPoint(int(cx), int(cy + s * 0.06)),
        )
        dot_pen = QPen(
            QColor("#ffffff"),
            s * 0.12,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
        )
        p.setPen(dot_pen)
        p.drawPoint(QPoint(int(cx), int(cy + s * 0.19)))

    elif symbol == "question":
        # Use text for "?" – cleaner at small sizes
        p.setPen(QColor("#ffffff"))
        font = p.font()
        font.setPixelSize(int(s * 0.40))
        font.setBold(True)
        p.setFont(font)
        p.drawText(
            QRect(0, int(s * 0.08), int(s), int(s)),
            Qt.AlignmentFlag.AlignHCenter,
            "?",
        )

    p.end()
    icon = QIcon(px)
    _CACHE[key] = icon
    return icon


def icon_active() -> QIcon:
    return _make_icon("#16a34a", "#15803d", "check")


def icon_inactive() -> QIcon:
    return _make_icon("#4b5563", "#374151", "x")


def icon_error() -> QIcon:
    return _make_icon("#dc2626", "#b91c1c", "exclaim")


def icon_unknown() -> QIcon:
    return _make_icon("#d97706", "#b45309", "question")
