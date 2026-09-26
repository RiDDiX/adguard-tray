"""
Overview page – is protection running, and which parts of it are on.

Enable/Disable/Restart, the features as switches (applied through the
window's Apply bar), a few counts that lead to their pages, and the licence.
Versions, updates and the licence details live on About; the certificate
tools on HTTPS.
"""

import logging

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from . import icons, ui
from .cli import AdGuardStatus, StatusResult, mask_license
from .i18n import _t
from .manager_window import (
    PAGE_ABOUT,
    PAGE_ACTIVITY,
    PAGE_DNS,
    PAGE_EXCEPTIONS,
    PAGE_FILTERS,
    PAGE_HTTPS,
    PAGE_SETTINGS,
    PAGE_STEALTH,
    PAGE_USERSCRIPTS,
)
from .proxy_settings import add_switch, gate, guard
from .ui import Page

logger = logging.getLogger(__name__)

def _number(value: int) -> str:
    """Thin spaces between thousands, as on the Activity page."""
    return f"{value:,}".replace(",", " ")


def _blocked_24h() -> tuple[int, int, str]:
    """(blocked, total, problem) for the last 24 hours, read like the Activity page does."""
    from . import store
    from .stats import read_activity
    try:
        result = store.ingest()
        summary = store.summary(24)
    except Exception:
        # An unusable database is not a blank tile: the log itself still counts.
        logger.exception("Reading the activity store failed")
        activity = read_activity().window(24)
        return activity.blocked, activity.total, activity.problem
    problem = ""
    if result.error:
        # Typical when adguard-cli runs as a root service: the log is not readable,
        # and a plain 0 would read as "nothing was blocked".
        problem = (read_activity(max_lines=1).problem
                   or _t("History is not being updated: {}", result.error))
    return summary["blocked"], summary["total"], problem


def _exception_count() -> int:
    from ._allowlist import load_user_rules
    return len(load_user_rules()[0])


def _license_summary(masked: str) -> str:
    """E.g. "Personal · Active · expires 2027-09-25"; else the first line as it is."""
    fields = {}
    for line in masked.splitlines():
        key, sep, value = line.partition(":")
        if sep and value.strip():
            fields[key.strip().lower()] = value.strip()
    kind = next((v for k, v in fields.items() if "type" in k), "")
    state = fields.get("status", "")
    expires = next((v for k, v in fields.items() if "expir" in k or "valid until" in k), "")
    # Known values ("Personal", "Active") are translated, others stay as the CLI wrote them.
    parts = [_t(p) for p in (kind, state) if p]
    if expires:
        parts.append(_t("expires {}", expires))
    if parts:
        return " · ".join(parts)
    return next((line.strip() for line in masked.splitlines() if line.strip()), "")


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


class _LoadWorker(QThread):
    """Everything the page shows. The status goes out first so the hero does
    not wait for the lists."""
    status = pyqtSignal(object)    # StatusResult
    done = pyqtSignal(object)      # {key: value, or the exception it raised}

    def __init__(self, cli):
        super().__init__()
        self.cli = cli

    def run(self):
        try:
            result = self.cli.get_status()
        except Exception as exc:  # would otherwise abort the process (qFatal)
            logger.exception("Status check failed")
            result = StatusResult(AdGuardStatus.ERROR, str(exc))
        self.status.emit(result)
        data = {}
        for key, fn in (
            ("filters", self.cli.get_filters),
            ("dns", self.cli.get_dns_filters),
            ("userscripts", self.cli.get_userscripts),
            ("exceptions", _exception_count),
            ("blocked", _blocked_24h),
            ("license", self.cli.get_license),
        ):
            try:
                data[key] = fn()
            except Exception as exc:
                logger.exception("Overview: loading %s failed", key)
                data[key] = exc
        self.done.emit(data)


class OverviewTab(Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(parent=parent)
        self.ctx = ctx
        self.cli = ctx.cli
        # Start/Stop/Restart change the run state, not the config, so the
        # tray only needs to re-poll – restarting would fight the user.
        self._on_status_change = ctx.on_status_change
        self._workers: list[QThread] = []
        self._refreshing = False
        self._reload_queued = False
        # Start/Stop wait only for the status, not for the counts below it.
        self._status_pending = True
        self._acting = False
        self._load_message = ""
        self._status: StatusResult | None = None
        self._build_hero()
        self._build_modules()
        self._build_glance()
        self._build_license()
        self.finish()
        self._show_status(None)

    # ── Layout ─────────────────────────────────────────────────────────────

    def _build_hero(self) -> None:
        self.hero = ui.Card(tone="info", padding=20)
        row = QHBoxLayout()
        row.setSpacing(18)
        self.shield = QLabel()
        self.shield.setFixedSize(56, 56)
        row.addWidget(self.shield, 0, Qt.AlignmentFlag.AlignTop)
        text = QVBoxLayout()
        text.setSpacing(6)
        self.lbl_title = ui.heading("", 1.35)
        text.addWidget(self.lbl_title)
        self.lbl_caption = ui.Caption()
        self.lbl_caption.setTextFormat(Qt.TextFormat.PlainText)
        text.addWidget(self.lbl_caption)
        actions = QHBoxLayout()
        actions.setContentsMargins(0, 6, 0, 0)
        actions.setSpacing(8)
        self.btn_primary = QPushButton()
        self.btn_primary.setDefault(True)
        self.btn_primary.clicked.connect(self._do_primary)
        actions.addWidget(self.btn_primary)
        self.btn_restart = QPushButton(_t("Restart"))
        self.btn_restart.clicked.connect(self._do_restart)
        actions.addWidget(self.btn_restart)
        self.btn_path = ui.LinkButton(_t("Set the path in Settings"),
                                      lambda: self.ctx.navigate(PAGE_SETTINGS))
        actions.addWidget(self.btn_path)
        self.spinner = ui.Spinner()
        actions.addWidget(self.spinner)
        self.lbl_busy = ui.Caption(_t("Waiting for authorization…"))
        self.lbl_busy.setWordWrap(False)
        self.lbl_busy.hide()
        actions.addWidget(self.lbl_busy)
        actions.addStretch(1)
        text.addLayout(actions)
        row.addLayout(text, 1)
        self.hero.layout_.addLayout(row)
        self.add(self.hero)

    def _build_modules(self) -> None:
        s = self.ctx.settings
        self.modules = self.section(
            _t("Features"),
            _t("Changes are collected in the bar at the bottom and applied together."))
        rows = {}
        for key, default, title, page in (
            (("ad_blocking_enabled",), True, _t("Ad blocking"), PAGE_FILTERS),
            (("dns_filtering", "enabled"), False, _t("DNS filtering"), PAGE_DNS),
            (("https_filtering", "enabled"), True, _t("HTTPS filtering"), PAGE_HTTPS),
            (("stealthmode", "enabled"), False, _t("Stealth mode"), PAGE_STEALTH),
            (("safebrowsing", "enabled"), True, _t("Safe Browsing"), PAGE_HTTPS),
            (("crlite", "enabled"), True, _t("CRLite"), PAGE_HTTPS),
        ):
            row = rows[key] = add_switch(self.modules, s, key, default, title)
            link = ui.LinkButton(_t("Settings"), lambda _=False, p=page: self.ctx.navigate(p))
            link.setAccessibleName(f"{title}: {_t('Settings')}")
            row.controls.insertWidget(0, link, 0, Qt.AlignmentFlag.AlignVCenter)
            QWidget.setTabOrder(link, row.switch)
        # As on the HTTPS page: revocation checks only happen while HTTPS is filtered.
        gate(rows[("https_filtering", "enabled")].switch, rows[("crlite", "enabled")])
        # Only the switches: Start/Stop and the counts do not need proxy.yaml.
        guard(self, s, self.modules)

    def _build_glance(self) -> None:
        card = self.section(_t("At a glance"))
        # Three per row: five in one row cut "127 of 140 on" off at the minimum width.
        grid = QGridLayout()
        grid.setContentsMargins(4, 4, 4, 4)
        grid.setSpacing(0)
        self.tiles = {}
        for i, (key, caption, page, tone) in enumerate((
            ("filters", _t("Filters"), PAGE_FILTERS, None),
            ("dns", _t("DNS"), PAGE_DNS, None),
            ("userscripts", _t("Userscripts"), PAGE_USERSCRIPTS, None),
            ("exceptions", _t("Exceptions"), PAGE_EXCEPTIONS, None),
            ("blocked", _t("Blocked (24 h)"), PAGE_ACTIVITY, "danger"),
        )):
            tile = ui.StatTile(caption, tone=tone)
            tile.caption = caption
            tile.set_link(lambda _=False, p=page: self.ctx.navigate(p))
            grid.addWidget(tile, i // 3, i % 3)
            self.tiles[key] = tile
        for column in range(3):
            grid.setColumnStretch(column, 1)
        card.layout_.addLayout(grid)

    def _build_license(self) -> None:
        self.license_card = self.section()
        self.license_row = self.license_card.add_row(ui.Row(
            _t("License"), "", ui.LinkButton(_t("Details"), lambda: self.ctx.navigate(PAGE_ABOUT))))
        self.license_card.hide()

    # ── Loading ────────────────────────────────────────────────────────────

    def on_shown(self) -> None:
        # Always: the tray, the CLI and the other pages change what this page
        # shows, and the window is reused rather than rebuilt.
        self.refresh()

    def refresh(self) -> None:
        if self._refreshing and not self._status_pending:
            # The running load has already read the status; this call may be
            # about a newer one (e.g. the tray saw it change).
            self._reload_queued = True
        if self._refreshing or self._acting:
            return
        self._refreshing = self._status_pending = True
        self._set_busy()
        w = _LoadWorker(self.cli)
        w.status.connect(self._show_status)
        w.done.connect(self._on_loaded)
        self._start(w)

    def _start(self, w: QThread) -> None:
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _on_loaded(self, data: dict) -> None:
        self._refreshing = False
        failed = []

        def lists(key, items, on):
            value = data.get(key)
            error = value if isinstance(value, Exception) else getattr(value, "error", "")
            if error:
                self.tiles[key].set_value("–", str(error))
                failed.append((key, str(error)))
            else:
                entries = items(value)
                self.tiles[key].set_value(
                    _t("{} of {} on", sum(1 for e in entries if on(e)), len(entries)))

        lists("filters", lambda r: [f for f in r.all_filters if f.is_added], lambda f: f.enabled)
        lists("dns", lambda r: [f for f in r.all_filters if f.is_added], lambda f: f.enabled)
        lists("userscripts", lambda r: r.scripts, lambda s: s.enabled)

        exceptions = data.get("exceptions")
        if isinstance(exceptions, int):
            self.tiles["exceptions"].set_value(_number(exceptions))
        else:
            self.tiles["exceptions"].set_value("–", str(exceptions))
            failed.append(("exceptions", str(exceptions)))

        blocked = data.get("blocked")
        note = ""
        if isinstance(blocked, tuple):
            count, total, note = blocked
            hint = _t("of {} requests in the last 24 hours", _number(total))
            self.tiles["blocked"].set_value("–" if note and not total else _number(count), hint)
        else:
            self.tiles["blocked"].set_value("–", str(blocked))
            failed.append(("blocked", str(blocked)))

        if self._status is not None and self._status.status == AdGuardStatus.NOT_INSTALLED:
            # The hero already says why the CLI's lists are missing.
            failed = [f for f in failed if f[0] in ("exceptions", "blocked")]
        if failed:
            details = "\n".join(f"{self.tiles[k].caption}: {e}" for k, e in failed)
            self._report("\n".join(filter(None, (_t("Some counts could not be loaded."), note))),
                         "danger", details)
        else:
            self._report(note, "warning")

        # About shows the licence and its error; here only a readable one.
        lic = data.get("license")
        summary = ""
        if isinstance(lic, tuple) and lic[0]:
            summary = _license_summary(mask_license(lic[1]))
        self.license_row.set_subtitle(summary)
        self.license_card.setVisible(bool(summary))
        if self._reload_queued:
            self._reload_queued = False
            self.refresh()

    def _report(self, text: str, tone: str, details: str = "") -> None:
        """Say what the last load could not show, without covering the result of
        an action or nagging again about a message the user closed."""
        if text == self._load_message:
            return
        ours = (bool(self._load_message) and not self.banner.isHidden()
                and self.banner.text.text() == self._load_message)
        if not text:
            if ours:
                self.banner.hide()
            self._load_message = ""
        elif ours or self.banner.isHidden():
            self.banner.show_message(text, tone, details)
            self._load_message = text

    # ── Status ─────────────────────────────────────────────────────────────

    def _show_status(self, result: StatusResult | None) -> None:
        self._status = result
        self._status_pending = result is None
        status = result.status if result is not None else None
        message = (result.message if result is not None else "").strip()
        if status == AdGuardStatus.ACTIVE:
            icon, tone, title = icons.icon_active(), "success", _t("Active – Protection running")
            caption = _t("AdGuard is filtering this computer's traffic.")
        elif status == AdGuardStatus.INACTIVE:
            icon, tone, title = icons.icon_inactive(), "warning", _t("Inactive – Protection stopped")
            caption = _t("Ads and trackers are not blocked until you enable protection.")
        elif status == AdGuardStatus.NOT_INSTALLED:
            icon, tone, title = icons.icon_error(), "danger", _t("adguard-cli not found")
            # The CLI's message starts with what the title already says.
            caption = message.split("\n", 1)[-1]
        elif status == AdGuardStatus.ERROR:
            icon, tone, title = icons.icon_error(), "danger", _t("Error retrieving status")
            caption = message.splitlines()[0][:300] if message else ""
        elif status == AdGuardStatus.UNKNOWN:
            icon, tone, title = icons.icon_unknown(), "info", _t("Unknown status")
            caption = _t("AdGuard's reply did not say whether it is running.")
        else:
            icon, tone, title = icons.icon_unknown(), "info", _t("Checking status…")
            caption = ""
        self.hero.set_tone(tone)
        self.shield.setPixmap(icon.pixmap(56))
        self.lbl_title.setText(title)
        self.lbl_caption.setText(caption)
        self.lbl_caption.setVisible(bool(caption))
        active = status == AdGuardStatus.ACTIVE
        self.btn_primary.setText(_t("Disable protection") if active else _t("Enable protection"))
        self.btn_primary.setVisible(status not in (None, AdGuardStatus.NOT_INSTALLED))
        self.btn_restart.setVisible(active)
        self.btn_path.setVisible(status == AdGuardStatus.NOT_INSTALLED)
        self._set_busy()

    def _set_busy(self) -> None:
        busy = self._status_pending or self._acting
        for btn in (self.btn_primary, self.btn_restart):
            btn.setEnabled(not busy)
        self.spinner.set_busy(busy)
        self.lbl_busy.setVisible(self._acting)

    # ── Actions ────────────────────────────────────────────────────────────

    def _do_primary(self) -> None:
        if self._status is not None and self._status.status == AdGuardStatus.ACTIVE:
            self._run_action(self.cli.stop, _t("Protection stopped."), _t("Could not stop protection."))
        else:
            self._run_action(self.cli.start, _t("Protection started."), _t("Could not start protection."))

    def _do_restart(self) -> None:
        self._run_action(self.cli.restart, _t("AdGuard restarted."), _t("Could not restart AdGuard."))

    def _run_action(self, fn, success: str, failure: str) -> None:
        if self._acting or self._status_pending:
            return
        self._acting = True
        self._set_busy()
        w = _Worker(fn)

        def _done(ok, msg):
            self._acting = False
            # The hero shows the state from before the action until the reload.
            self._status_pending = True
            self._set_busy()
            msg = msg.strip()
            if ok:
                self.banner.show_message(success, "success", timeout_ms=5000)
                if self._on_status_change:
                    self._on_status_change()
            elif msg == _t("Authentication cancelled"):
                self.banner.show_message(msg, "info", timeout_ms=5000)
            elif msg and "\n" not in msg and len(msg) <= 160:
                self.banner.show_message(f"{failure}\n{msg}", "danger")
            else:
                self.banner.show_message(failure, "danger", details=msg)
            if self._refreshing:
                self._reload_queued = True
            self.refresh()

        w.done.connect(_done)
        self._start(w)
