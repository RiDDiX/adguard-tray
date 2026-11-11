"""VPN – AdGuard VPN CLI: log in through the browser, connect, pick the mode."""

import logging
import shlex
import time
from dataclasses import dataclass, field

from PyQt6 import sip
from PyQt6.QtCore import QProcess, Qt, QThread, QTimer, QUrl, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QApplication, QComboBox, QLabel, QPushButton, QVBoxLayout, QWidget

from . import installer, ui, vpn
from .i18n import _t
from .proxy_settings import unavailable_message

logger = logging.getLogger(__name__)

POLL_MS = 3000          # status while the user types the password for a TUN connect
POLL_FOR = 60           # seconds


def _stopped() -> str:
    return _t("AdGuard VPN was disconnected to change its mode. Connect again.")


@dataclass
class _Result:
    path: str = ""                  # "" = not installed
    status: vpn.VpnStatus | None = None
    ok: bool = False                # the action's outcome
    message: str = ""               # the action's output or error
    stopped: bool = False           # the mode change had to disconnect
    full: bool = False              # licence and locations were read
    licence: str = ""
    configured: bool = False        # config is the VPN's current one (None: unreadable)
    config: vpn.VpnConfig | None = None
    locations: list = field(default_factory=list)
    errors: list = field(default_factory=list)


class _Worker(QThread):
    done = pyqtSignal(object)       # _Result

    def __init__(self, action, mode: str, config: bool, full: bool, locations: bool) -> None:
        super().__init__()
        self.action, self.mode, self.config, self.full, self.locations = action, mode, config, full, locations

    def run(self) -> None:
        r = _Result()
        try:
            r.path = vpn.find()
            if r.path:
                if self.mode:
                    r.config, r.message, r.stopped = vpn.change_mode(r.path, self.mode)
                    r.ok = r.configured = r.config is not None
                elif self.action:
                    r.ok, r.message = self.action(r.path)
                r.status = vpn.status(r.path)
                if self.config and r.status.logged_in and not r.status.error:
                    if self.full:
                        r.full = True
                        r.licence, licence_error = vpn.license_info(r.path)
                        r.errors.append(licence_error)
                        if self.locations:
                            r.locations = vpn.locations(r.path)[0]
                    if not r.configured:
                        r.configured = True
                        r.config, config_error = vpn.read_config(r.path)
                        r.errors.append(config_error)
        except Exception as exc:
            logger.exception("adguardvpn-cli call failed")
            r.errors.append(str(exc))
        self.done.emit(r)


class _Login(QProcess):
    """`login`, a child of the page whose destroyed signal reaches end() as a real
    slot: Qt drops that connection when the process goes, and no Python closure
    is left for interpreter teardown (see proxy_settings._Follower)."""

    @pyqtSlot()
    def end(self) -> None:
        """Stop a running login the way its own "x - Cancel" does, then make sure."""
        self.blockSignals(True)     # the page is half destroyed
        if self.state() == QProcess.ProcessState.NotRunning:
            return
        self.write(b"x")
        if not self.waitForFinished(1000):
            self.kill()
            self.waitForFinished(1000)


class VpnTab(ui.Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(parent=parent)
        self.ctx = ctx
        self._workers: list[QThread] = []
        self._busy = False
        self._again = False
        self._path = ""
        self._config: vpn.VpnConfig | None = None
        self._poll = QTimer(self)
        self._poll.timeout.connect(self._poll_tick)
        self._poll_end = 0.0
        self._poll_from = ""
        self._login: QProcess | None = None
        self._login_out = b""
        self._link = ""

        self.install_box, card = self._section("")
        btn_install = QPushButton(_t("Install…"))
        btn_install.clicked.connect(lambda: installer.start_install(self, vpn.BINARY))
        card.add_row(ui.Row(_t("AdGuard VPN CLI"),
                            _t("Not installed. Install adguardvpn-cli to log in to AdGuard VPN here."),
                            btn_install))
        self.install_box.hide()

        self.account_box, card = self._section(_t("Account"))
        self.btn_login = QPushButton(_t("Log in"))
        self.btn_login.clicked.connect(self._start_login)
        self.btn_login.hide()
        self.btn_logout = QPushButton(_t("Log out"))
        self.btn_logout.clicked.connect(self._logout)
        self.btn_logout.hide()
        self.account_row = card.add_row(ui.Row(_t("Checking…")))
        self.account_row.add_control(self.btn_login)
        self.account_row.add_control(self.btn_logout)
        self.licence = card.add_row(self._text_label())
        self.licence.hide()
        self.btn_open = QPushButton(_t("Open in browser"))
        self.btn_open.clicked.connect(self._open_link)
        self.btn_cancel = QPushButton(_t("Cancel"))
        self.btn_cancel.clicked.connect(self._cancel_login)
        self.link_row = card.add_row(ui.Row(_t("Authorize in your browser"), "", self.btn_open))
        self.link_row.add_control(self.btn_cancel)
        self.link_row.subtitle.setTextFormat(Qt.TextFormat.PlainText)
        self.link_row.hide()

        self.connection_box, card = self._section(_t("Connection"))
        self.status_text = card.add_row(self._text_label())
        self.location = ui.ignore_idle_wheel(QComboBox())
        self.location.setEditable(True)
        self.location.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        # Qt's completer silently extends typed text to the first item with that prefix.
        self.location.setCompleter(None)
        self.location.setMinimumWidth(260)
        self.location.addItem(_t("Fastest location"), None)
        self.btn_connect = QPushButton(_t("Connect"))
        self.btn_connect.clicked.connect(self._connect)
        self.btn_disconnect = QPushButton(_t("Disconnect"))
        self.btn_disconnect.clicked.connect(
            lambda: self._run(vpn.disconnect, lambda r: self._show_result(r, success=False)))
        row = card.add_row(ui.Row(_t("Location"), "", self.location))
        row.add_control(self.btn_connect)
        row.add_control(self.btn_disconnect)
        self.connection_box.hide()

        self.mode_box, card = self._section(_t("Network"))
        self.conflict = ui.Banner()
        card.add(self.conflict)
        self.mode = ui.ignore_idle_wheel(QComboBox())
        self.mode.addItem("TUN", "tun")
        self.mode.addItem("SOCKS5", "socks")
        self.mode.activated.connect(self._mode_chosen)
        card.add_row(ui.Row(_t("Mode:").rstrip(":："), "", self.mode))
        self.route = ui.Switch()
        self.route.toggled.connect(self._route_toggled)
        self.route_row = card.add_row(ui.Row(_t("Route AdGuard through the VPN"), "", self.route))
        self.mode_box.hide()
        self.finish()

        settings = ctx.settings
        settings.changed.connect(self._sync_route)
        settings.reloaded.connect(self._sync_route)
        self._sync_route()

    @staticmethod
    def _text_label() -> QLabel:
        label = QLabel("")
        label.setTextFormat(Qt.TextFormat.PlainText)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        label.setWordWrap(True)
        label.setContentsMargins(14, 10, 14, 10)
        return label

    def _section(self, title: str) -> tuple[QWidget, ui.Card]:
        """Heading and card in one widget, so a state can hide both."""
        box = QWidget()
        lay = QVBoxLayout(box)
        lay.setContentsMargins(0, 0, 0, 10)
        lay.setSpacing(8)
        if title:
            lay.addWidget(ui.heading(title))
        card = ui.Card()
        lay.addWidget(card)
        self.add(box)
        return box, card

    # ── Shell hooks ───────────────────────────────────────────────────────

    def on_shown(self) -> None:
        self.refresh()

    def refresh(self) -> None:
        if self._busy or self._login is not None:
            self._again = True      # one CLI call at a time; checked once this one ends
            return
        self._run()

    # ── Calls: an action, then status and config (and the account on a refresh) ──

    def _run(self, action=None, then=None, mode: str = "", poll: bool = False) -> None:
        if self._busy or self._login is not None:
            return
        self._again = False
        if action or mode:
            self.banner.hide()      # not next to this action's result
        if poll:
            self._busy = True       # buttons stay as they are: no focus jumping every few seconds
        else:
            self._set_busy(True)
        plain = not (action or mode or poll)
        worker = _Worker(action, mode, not poll, plain, plain and self.location.count() < 2)
        worker.done.connect(lambda r: self._checked(r, then))
        worker.finished.connect(lambda: self._workers.remove(worker) if worker in self._workers else None)
        worker.finished.connect(worker.deleteLater)
        self._workers.append(worker)
        worker.start()

    def _logout(self) -> None:
        self._run(vpn.logout, lambda r: self._show_result(r, success=False))

    def _checked(self, r: _Result, then=None) -> None:
        if sip.isdeleted(self):
            return
        self._set_busy(False)
        self._path = path = r.path
        status = r.status
        known = status is not None and not status.error     # a failed call says nothing about the account
        logged_in = known and status.logged_in
        connected = logged_in and not vpn.is_disconnected(status.text)
        self.install_box.setVisible(not path)
        self.account_box.setVisible(bool(path))
        self.connection_box.setVisible(bool(path) and logged_in)
        self.mode_box.setVisible(bool(path) and logged_in)
        self.account_row.title.setText(
            _t("AdGuard VPN CLI") if not known else _t("Logged in") if logged_in else _t("Not logged in"))
        self.btn_login.setVisible(known and not logged_in and self._login is None)
        self.btn_logout.setVisible(bool(path) and logged_in)
        self.status_text.setText(status.text if logged_in else "")
        self.btn_disconnect.setVisible(connected)
        if r.full:
            self.licence.setText(r.licence)
        if r.configured:
            self._config = r.config
        self.licence.setVisible(logged_in and bool(self.licence.text()))
        if known and not logged_in:
            while self.location.count() > 1:
                self.location.removeItem(1)
        for loc in r.locations:
            ping = f" ({loc.ping} ms)" if loc.ping.isdigit() else ""
            self.location.addItem(f"{loc.country} – {loc.city}{ping}", loc.city)
        index = self.mode.findData(self._config.mode if self._config else None)
        self.mode.setCurrentIndex(index)
        self._sync_route()
        if then:
            then(r)
        error = "\n".join(e for e in (*r.errors, status.error if status else "") if e)
        if error:
            lines = error.splitlines()
            self.banner.show_message(_t("Error: {}", lines[0]), "danger",
                                     details=error if len(lines) > 1 else "")
        if self._again:
            self.refresh()

    def _show_result(self, r: _Result, success: bool = True) -> None:
        """The action's first line in the banner; *success* False shows failures only."""
        lines = r.message.splitlines()
        if not r.ok and lines:
            self.banner.show_message(_t("Error: {}", lines[0]), "danger",
                                     details=r.message if len(lines) > 1 else "")
        elif r.ok and success and lines:
            self.banner.show_message(lines[0], "success", details=r.message if len(lines) > 1 else "")

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        for widget in (self.btn_login, self.btn_logout, self.btn_connect, self.btn_disconnect, self.mode):
            widget.setEnabled(not busy)
        self.route.setEnabled(not busy and self.ctx.settings.available)

    # ── Connection ────────────────────────────────────────────────────────

    def _chosen_location(self) -> str | None:
        """The picked city, or the typed text as it is; None for the fastest."""
        text = self.location.currentText().strip()
        index = self.location.findText(text)
        if index >= 0:
            return self.location.itemData(index)
        return text or None

    def _connect(self) -> None:
        if self._busy or not self._path:
            return
        location = self._chosen_location()
        if self._config is None or self._config.mode != "tun":
            self._run(lambda path: vpn.connect(path, location), self._show_result)
            return
        self.banner.hide()
        # TUN needs root: the CLI asks for the password through sudo, which needs a terminal.
        command = shlex.join(vpn.connect_command(self._path, location))
        if not installer.open_in_terminal(command):
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText(command)
            self.banner.show_message(
                _t("No terminal app was found. The command is on the clipboard: paste it into a terminal."),
                "warning", details=command)
            return
        self.banner.show_message(_t("AdGuard VPN asks for your password in the terminal window."), "info",
                                 details=command)
        self._poll_from = self.status_text.text()
        self._poll_end = time.monotonic() + POLL_FOR
        self._poll.start(POLL_MS)

    def _poll_tick(self) -> None:
        if time.monotonic() > self._poll_end:
            self._end_poll()
        elif not self._busy and self._login is None:
            self._run(then=self._polled, poll=True)

    def _polled(self, r: _Result) -> None:
        status = r.status
        if status and not status.error and vpn.is_connected(status.text) and status.text != self._poll_from:
            self._end_poll()

    def _end_poll(self) -> None:
        self._poll.stop()
        self.banner.hide()      # the password hint: connected, or nobody typed one in time
        self.refresh()

    # ── Mode and AdGuard CLI ──────────────────────────────────────────────

    def _mode_chosen(self, _index: int) -> None:
        mode = self.mode.currentData()
        if self._busy or self._config is None or mode == self._config.mode:
            self.mode.setCurrentIndex(self.mode.findData(self._config.mode if self._config else None))
            return
        routed = vpn.routed(self.ctx.settings, self._config)
        self._run(then=lambda r: self._mode_set(r, routed), mode=mode)

    def _mode_set(self, r: _Result, routed: bool) -> None:
        if not r.ok:
            self._show_result(r)
            return
        messages = [_stopped()] if r.stopped else []
        if routed and r.config.mode != "socks":
            # In TUN mode nothing listens on the SOCKS5 port AdGuard would send its traffic to.
            vpn.stop_routing(self.ctx.settings)
            messages.append(_t("AdGuard no longer sends its traffic through AdGuard VPN. Press Apply to save this."))
        if messages:
            self.banner.show_message(" ".join(messages), "info")

    def _route_toggled(self, on: bool) -> None:
        if on:
            self._route_on()
        else:
            self.banner.hide()
            vpn.stop_routing(self.ctx.settings)
            self._sync_route()

    def _route_on(self) -> None:
        if self._busy or self._config is None or not self.ctx.settings.available:
            self._sync_route()
        elif self._config.mode == "socks":
            self._routed(None)
        else:
            self._run(then=self._routed, mode="socks")

    def _routed(self, r: _Result | None) -> None:
        if self._config is None or self._config.mode != "socks":
            self.banner.show_message(_t("Could not switch AdGuard VPN to SOCKS5 mode."), "danger",
                                     details=r.message if r else "")
            return
        vpn.route_through(self.ctx.settings, self._config, self._path)
        text = _t("AdGuard VPN now uses SOCKS5 mode. Press Apply to send AdGuard's traffic through it, "
                  "and reconnect AdGuard VPN if it is connected.")
        if r and r.stopped:
            self.banner.show_message(f"{_stopped()} {text}", "info")
        else:
            self.banner.show_message(text, "success")

    def _sync_route(self, *_args) -> None:
        s = self.ctx.settings
        self.route.blockSignals(True)
        self.route.setChecked(vpn.routed(s, self._config))
        self.route.blockSignals(False)
        self.route.setEnabled(s.available and not self._busy)
        self.route_row.set_subtitle("" if s.available else unavailable_message(s.error != "missing"))
        if vpn.loops(s, self._config):
            self.conflict.show_message(
                _t("AdGuard VPN is set to TUN mode while AdGuard filters in automatic mode. Connected like "
                   "this, traffic loops between the two – AdGuard does not support this combination."),
                "warning", action=_t("Route AdGuard through the VPN"), callback=self._route_on)
        else:
            self.conflict.hide()

    # ── Login ─────────────────────────────────────────────────────────────

    def _start_login(self) -> None:
        if self._busy or self._login is not None or not self._path:
            return
        self.banner.hide()
        proc = _Login(self)
        proc.setStandardErrorFile(QProcess.nullDevice())
        proc.readyReadStandardOutput.connect(self._login_output)
        proc.finished.connect(self._login_finished)
        proc.errorOccurred.connect(self._login_error)
        self._login, self._login_out, self._link = proc, b"", ""
        self.destroyed.connect(proc.end)
        self.btn_login.hide()
        self.btn_open.hide()
        self.link_row.set_subtitle("")
        self.link_row.show()
        # stdin stays QProcess's open pipe: closed or /dev/null, adguardvpn-cli 1.8.2 spins and floods its log.
        proc.start(self._path, ["login"])

    def _login_output(self) -> None:
        data = bytes(self._login.readAllStandardOutput())
        if self._link:
            return
        self._login_out += data
        # The link holds a short-lived device code: shown here, never logged.
        link = vpn.login_link(self._login_out.decode("utf-8", errors="replace"))
        if link:
            self._link, self._login_out = link, b""
            self.link_row.set_subtitle(link)
            self.btn_open.show()

    def _open_link(self) -> None:
        if self._link and not QDesktopServices.openUrl(QUrl(self._link)):
            self.banner.show_message(_t("Could not open the browser. Copy the link instead."), "warning")

    def _cancel_login(self) -> None:
        proc = self._login
        if proc is None:
            return
        proc.write(b"x")
        timer = QTimer(proc)        # goes with the process when it ends in time
        timer.setSingleShot(True)
        timer.timeout.connect(proc.kill)
        timer.start(3000)

    def _login_error(self, error) -> None:
        if error == QProcess.ProcessError.FailedToStart:     # no finished() follows
            self.banner.show_message(_t("Could not start adguardvpn-cli."), "danger",
                                     details=self._login.errorString())
            self._login_finished()

    def _login_finished(self, code: int = 0, exit_status=None) -> None:
        if self._login is None:
            return
        self._login_output()        # what came with the exit
        proc, self._login = self._login, None
        proc.deleteLater()
        if code and exit_status == QProcess.ExitStatus.NormalExit:
            self._show_result(_Result(message=vpn.login_error(code, self._login_out.decode("utf-8", "replace"))))
        self._link = ""
        self._login_out = b""
        self.link_row.hide()
        self.refresh()      # exit code 0 also means cancelled: only status knows
