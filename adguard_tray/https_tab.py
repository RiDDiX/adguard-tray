"""HTTPS – filtering switch, AdGuard's certificate, certificate checks and HTTP/3.

The certificate tools don't touch proxy.yaml, so they stay usable when the
file is missing; only the cards bound to it are disabled then.
"""

import logging

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget

from . import ui
from .i18n import _t
from .proxy_settings import add_switch, gate, guard
from .ui import Caption, Page, Row, Spinner, ToneLabel

logger = logging.getLogger(__name__)

HF = "https_filtering"
HTTP3 = (HF, "http3_filtering_enabled")
# (key, default, value when turned off) for "Turn off all strict checks".
STRICT = (
    (HTTP3, True, False),
    ((HF, "ocsp_check_enabled"), True, False),
    ((HF, "enforce_certificate_transparency"), True, False),
    ((HF, "filter_secure_dns_mode"), "transparent", "off"),
)


def _plain(text: str, tone: str = "secondary") -> Caption:
    # Profile names, paths and CLI output are data, never markup.
    label = Caption(text, tone=tone)
    label.setTextFormat(Qt.TextFormat.PlainText)
    return label


def _clear(layout) -> None:
    while layout.count():
        widget = layout.takeAt(0).widget()
        if widget is not None:
            widget.setParent(None)      # gone now, not at the next event loop pass
            widget.deleteLater()


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


class _CertWorker(QThread):
    """Imports the AdGuard CA into the browsers' certificate stores."""
    done = pyqtSignal(bool, str, object)

    def run(self):
        from .certs import install_into_browsers
        try:
            ok, msg, targets = install_into_browsers()
        except Exception as exc:  # never abort the app from a worker
            logger.exception("Certificate install failed")
            ok, msg, targets = False, str(exc), []
        self.done.emit(ok, msg, targets)


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


class HttpsTab(Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(parent=parent)
        self.ctx = ctx
        self._workers: list[QThread] = []
        self._cert_busy = False
        self._quic_state = None
        self._quic_busy = False
        self._quic_again = False
        s = ctx.settings

        master_card = self.section()
        master = add_switch(master_card, s, (HF, "enabled"), True, _t("HTTPS filtering"),
                            ui.one_line(_t("Decrypt and filter HTTPS traffic.\n"
                                           "Needed to block ads on https sites.\n"
                                           "Requires a trusted root certificate installed on the system.")))

        self._build_certificate()

        checks = self.section(_t("Certificate checks"))
        for key, default, title, tip in (
            ("enable_tls13", True, "Enable TLS 1.3", "Enable TLS 1.3 support for filtered connections."),
            ("ocsp_check_enabled", True, "OCSP certificate checks",
             "Check whether a site's certificate was revoked (OCSP).\n"
             "AdGuard checks asynchronously and lets the connection through if\n"
             "the check is slow, so this rarely breaks a site – leave it on\n"
             "unless you have narrowed a problem down to it."),
            ("enforce_certificate_transparency", True, "Enforce Certificate Transparency",
             "Enforce Certificate Transparency checks (Chrome's CT policy).\n"
             "Sites whose own certificate is not CT-compliant stop being filtered\n"
             "and the browser may refuse them. Large sites are compliant, so try\n"
             "this only for a site that reports a certificate error."),
            ("filter_ev_certificates", False, "Filter EV certificate sites",
             "By default, sites with Extended Validation certificates are not filtered.\n"
             "Enable this to filter them as well (e.g. banking sites)."),
        ):
            add_switch(checks, s, (HF, key), default, _t(title), ui.one_line(_t(tip)))
        add_switch(checks, s, ("crlite", "enabled"), True, _t("CRLite"),
                   ui.one_line(_t("Certificate revocation checking using Mozilla's CRLite.\n"
                                  "Faster and more reliable than traditional CRL/OCSP checks.")))

        quic = self.section(_t("HTTP/3 (QUIC)"))
        http3 = add_switch(quic, s, HTTP3, True, _t("Filter HTTP/3 (QUIC) – experimental"),
                           ui.one_line(_t(
                               "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\n"
                               "browsers refuse HTTP/3 through a user-installed certificate anyway.\n"
                               "Off: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\n"
                               "which is filtered reliably.\n"
                               "Either way this only applies in automatic mode – in manual mode\n"
                               "HTTP/3 traffic never reaches AdGuard.")))
        quic.add_row(self._build_quic_status())

        safe = self.section(_t("Safe Browsing"))
        sb = add_switch(safe, s, ("safebrowsing", "enabled"), True, _t("Safe Browsing"),
                        ui.one_line(_t("Warns about malicious and phishing websites.\n"
                                       "Uses AdGuard's Safe Browsing database.")))
        stats = add_switch(safe, s, ("safebrowsing", "send_anonymous_statistics"), False,
                           _t("Send anonymous statistics"), _t("Send anonymous lookups to AdGuard."))
        gate(sb.switch, stats)

        compat = self.section(_t("Sites that don't load"), _t(
            "If a site doesn't load, turn off HTTP/3 filtering first. The other checks "
            "protect every site – turn them off only if that didn't help."))
        buttons = QWidget()
        bl = QHBoxLayout(buttons)
        bl.setContentsMargins(12, 10, 12, 10)
        self.btn_http3_off = QPushButton(_t("Turn off HTTP/3 filtering"))
        self.btn_http3_off.clicked.connect(lambda: s.set(HTTP3, False, True))
        bl.addWidget(self.btn_http3_off)
        self.btn_strict = QPushButton(_t("Turn off all strict checks…"))
        self.btn_strict.clicked.connect(self._turn_off_strict)
        bl.addWidget(self.btn_strict)
        bl.addStretch(1)
        compat.add_row(buttons)

        self._master = master.switch
        self._bound = (master_card, safe)
        self._gated = (checks, http3, compat)
        gate(master.switch, *self._gated)
        guard(self, s, *self._bound)
        s.changed.connect(self._sync_compat)
        s.reloaded.connect(self._on_reloaded)
        self._on_reloaded()
        self.finish()

    # ── Certificate ────────────────────────────────────────────────────────

    def _build_certificate(self) -> None:
        card = self.section(_t("Certificate"))
        self.edit_profile = QLineEdit()
        self.edit_profile.setPlaceholderText(_t("(optional) e.g. abcd1234.MyProfile"))
        self.edit_profile.setMinimumWidth(240)
        card.add_row(Row(_t("Firefox profile:").rstrip(":："),
                         _t("Also adds the certificate to this Firefox profile."), self.edit_profile))

        self.spin_cert = Spinner()
        self.btn_cert = QPushButton(_t("Create"))
        self.btn_cert.clicked.connect(self._create_cert)
        row = card.add_row(Row(_t("Create certificate"), _t(
            "Generate a root CA certificate for HTTPS filtering. "
            "The certificate must be installed and trusted on your system.")))
        row.add_control(self.spin_cert)
        row.add_control(self.btn_cert)

        self.spin_browsers = Spinner()
        self.btn_browsers = QPushButton(_t("Add…"))
        self.btn_browsers.clicked.connect(self._add_to_browsers)
        row = card.add_row(Row(_t("Add to browsers"), _t(
            "Chromium- and Firefox-based browsers keep their own certificate store.")))
        row.add_control(self.spin_browsers)
        row.add_control(self.btn_browsers)

        # One line per certificate store after "Add to browsers".
        self.cert_results = QWidget()
        self._cert_lines = QVBoxLayout(self.cert_results)
        self._cert_lines.setContentsMargins(14, 0, 12, 10)
        self._cert_lines.setSpacing(2)
        self.cert_results.hide()
        card.add(self.cert_results)

    def _set_cert_busy(self, busy: bool, spinner: Spinner) -> None:
        self._cert_busy = busy
        for widget in (self.btn_cert, self.btn_browsers, self.edit_profile):
            widget.setEnabled(not busy)
        spinner.set_busy(busy)

    def _start(self, w: QThread) -> None:
        w.finished.connect(lambda: self._workers.remove(w) if w in self._workers else None)
        self._workers.append(w)
        w.start()

    def _create_cert(self) -> None:
        if self._cert_busy:
            return
        profile = self.edit_profile.text().strip()
        self._set_cert_busy(True, self.spin_cert)
        w = _Worker(lambda: self.ctx.cli.generate_cert(firefox_profile=profile))
        w.done.connect(self._on_cert_created)
        self._start(w)

    def _on_cert_created(self, ok: bool, msg: str) -> None:
        self._set_cert_busy(False, self.spin_cert)
        if ok:
            done = _t("Certificate generated")
            details = "" if msg == done else msg
            # CLI output may carry warnings; don't hide it while it is being read.
            self.banner.show_message(done, "success", details=details,
                                     timeout_ms=0 if details else 5000)
        else:
            self.banner.show_message(_t("Certificate generation failed"), "danger", details=msg)

    def _add_to_browsers(self) -> None:
        if self._cert_busy:
            return
        if not ui.confirm(
            self, _t("Add to browsers"),
            _t("AdGuard's certificate will be added to every browser profile found "
               "on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in "
               "those browsers. Close your browsers first – they read the "
               "certificate store at startup."),
            _t("Add to browsers"), destructive=False,
        ):
            return
        self.cert_results.hide()
        self._set_cert_busy(True, self.spin_browsers)
        w = _CertWorker()
        w.done.connect(self._on_added_to_browsers)
        self._start(w)

    def _on_added_to_browsers(self, ok: bool, msg: str, targets: object) -> None:
        self._set_cert_busy(False, self.spin_browsers)
        targets = list(targets or [])
        failed = any(not t.ok for t in targets)
        if ok:
            self.banner.show_message(msg, "warning" if failed else "success",
                                     timeout_ms=0 if failed else 5000)
        else:
            self.banner.show_message(msg, "danger")
        _clear(self._cert_lines)
        for t in targets:
            text = f"{t.name} – {t.path}" + ("" if t.ok else f" – {t.error}")
            self._cert_lines.addWidget(_plain(text, "success" if t.ok else "danger"))
        if targets and ok:
            self._cert_lines.addWidget(_plain(_t("Restart your browsers for the certificate to take effect.")))
        self.cert_results.setVisible(bool(targets))

    # ── HTTP/3 (QUIC) ──────────────────────────────────────────────────────

    def _build_quic_status(self) -> QWidget:
        box = QWidget()
        lay = QVBoxLayout(box)
        lay.setContentsMargins(14, 10, 12, 10)
        lay.setSpacing(2)
        self.lbl_quic = ToneLabel(_t("Checking…"))
        self.lbl_quic.setFont(ui.scaled_font(self.lbl_quic, bold=True))
        self.lbl_quic.setTextFormat(Qt.TextFormat.PlainText)
        self.lbl_quic.setWordWrap(True)
        lay.addWidget(self.lbl_quic)
        self._quic_lines = QVBoxLayout()
        self._quic_lines.setSpacing(2)
        lay.addLayout(self._quic_lines)
        lay.addSpacing(6)
        row = QHBoxLayout()
        row.setSpacing(6)
        self.btn_quic_check = QPushButton(_t("Check again"))
        self.btn_quic_check.clicked.connect(self._check_quic)
        row.addWidget(self.btn_quic_check)
        self.btn_firefox = QPushButton(_t("Turn off HTTP/3 in Firefox profiles…"))
        self.btn_firefox.clicked.connect(self._toggle_firefox_http3)
        self.btn_firefox.hide()
        row.addWidget(self.btn_firefox)
        self.spin_quic = Spinner()
        row.addWidget(self.spin_quic)
        row.addStretch(1)
        lay.addLayout(row)
        return box

    def _check_quic(self) -> None:
        if self._quic_busy:
            self._quic_again = True
            return
        self._quic_busy = True
        self.btn_quic_check.setEnabled(False)
        self.btn_firefox.setEnabled(False)
        # The last verdict stays up while the spinner runs, so revisits don't flicker.
        self.spin_quic.set_busy(True)
        w = _QuicWorker(self.ctx.cli)
        w.done.connect(self._on_quic_checked)
        self._start(w)

    def _show_quic(self, headline: str, tone: str, details: list[str]) -> None:
        self.lbl_quic.setText(headline)
        self.lbl_quic.set_tone(tone)
        _clear(self._quic_lines)
        for line in details:
            self._quic_lines.addWidget(_plain(line))

    def _on_quic_checked(self, state: object) -> None:
        self._quic_busy = False
        self.spin_quic.set_busy(False)
        self.btn_quic_check.setEnabled(True)
        self.btn_firefox.setEnabled(True)
        if self._quic_again:
            # Something changed while this check ran; its answer may be stale.
            self._quic_again = False
            self._check_quic()
            return
        if state is None:
            self._show_quic(_t("Error: {}", _t("HTTP/3 state unknown")), "danger", [])
            self.btn_firefox.hide()
            return
        self._quic_state = state
        self._show_quic(state.headline, "success" if state.filtered else "warning", state.details)
        if state.firefox_profiles:
            all_off = state.firefox_disabled == len(state.firefox_profiles)
            self.btn_firefox.setText(
                _t("Turn HTTP/3 back on in Firefox profiles") if all_off
                else _t("Turn off HTTP/3 in Firefox profiles…"))
            self.btn_firefox.show()
        else:
            self.btn_firefox.hide()

    def _toggle_firefox_http3(self) -> None:
        from .quic import set_firefox_http3
        state = self._quic_state
        if self._quic_busy or not state or not state.firefox_profiles:
            return
        enable = state.firefox_disabled == len(state.firefox_profiles)
        if not enable and not ui.confirm(
            self, _t("Turn off HTTP/3 in Firefox profiles"),
            _t("Turn off HTTP/3 in {} Firefox-family profile(s)?\n\n"
               "Their traffic then uses HTTP/2, which AdGuard can filter. "
               "Restart the browser afterwards.", len(state.firefox_profiles)),
            _t("Turn off"), destructive=False,
        ):
            return
        failed = []
        for profile in state.firefox_profiles:
            ok, err = set_firefox_http3(profile, enable)
            if not ok:
                failed.append(f"{profile.name}: {err}")
        if failed:
            self.banner.show_message(_t("Error: {}", "; ".join(failed)[:200]), "danger",
                                     details="\n".join(failed))
        else:
            self.banner.show_message(
                _t("HTTP/3 turned back on in Firefox profiles – restart the browser.") if enable
                else _t("HTTP/3 switched off in Firefox profiles – restart the browser."),
                "success", timeout_ms=5000)
        self._check_quic()

    # ── proxy.yaml ─────────────────────────────────────────────────────────

    def _sync_compat(self, *_) -> None:
        # A button that would change nothing stays disabled.
        s = self.ctx.settings
        self.btn_http3_off.setEnabled(bool(s.value(HTTP3, True)))
        self.btn_strict.setEnabled(any(s.value(key, default) != off for key, default, off in STRICT))

    def _turn_off_strict(self) -> None:
        if not ui.confirm(
            self, _t("Turn off all strict checks"),
            _t("This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and "
               "secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, "
               "and browsers can resolve past AdGuard's DNS filter."),
            _t("Turn off"),
        ):
            return
        for key, default, off in STRICT:
            self.ctx.settings.set(key, off, default)

    def _on_reloaded(self) -> None:
        s = self.ctx.settings
        # Runs after the bindings, gate() and guard(), so an unusable file wins.
        for widget in self._gated:
            widget.setEnabled(s.available and self._master.isChecked())
        self._sync_compat()
        # proxy.yaml decides what happens to HTTP/3 (proxy mode, HTTPS, HTTP/3 filtering).
        # Hidden pages check in on_shown.
        if self.isVisible():
            self._check_quic()

    # ── Shell hooks ────────────────────────────────────────────────────────

    def on_shown(self) -> None:
        # AdGuard may have been started or stopped from the tray or Overview.
        self._check_quic()

    def refresh(self) -> None:
        self._check_quic()
