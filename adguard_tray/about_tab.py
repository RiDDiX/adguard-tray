"""About – AdGuard Tray and AdGuard CLI (version, updates, filters) and the licence."""

import logging
import re
import shutil

from PyQt6.QtCore import QProcess, Qt, QThread, QUrl, pyqtSignal
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QApplication, QComboBox, QMessageBox, QPushButton, QWidget

from . import __version__
from .cli import AdGuardStatus, mask_license
from .i18n import _t
from .ui import Caption, LinkButton, Page, Row, Spinner, ToneLabel, confirm, ignore_idle_wheel, one_line
from .updates import REPO, Install, update_command
from .worker import safe_call

logger = logging.getLogger(__name__)

PROJECT_URL = f"https://github.com/{REPO}"


def _channel_label(channel: str) -> str:
    return {
        "release": _t("Release (stable)"),
        "beta": _t("Beta"),
        "nightly": _t("Nightly"),
        "default": _t("Default"),
    }.get(channel, channel)


def _license_word(text: str) -> str:
    """adguard-cli's English licence words in the UI language; anything else as it is."""
    if m := re.fullmatch(r"(\d+) of (\d+)", text):
        return _t("{} of {}", *m.groups())
    return {
        "license type": _t("License type"),
        "status": _t("Status"),
        "license key": _t("License key"),
        "owner": _t("Owner"),
        "expires": _t("Expires"),
        "expiration date": _t("Expiration date"),
        "computers": _t("Computers"),
        "active": _t("Active"),
        "personal": _t("Personal"),
        "trial": _t("Trial"),
    }.get(text.lower(), text)


def _reset_text() -> str:
    return _t("AdGuard CLI forgets the license on this computer. You will have to activate it again.")


def _button(text: str, slot) -> QPushButton:
    button = QPushButton(text)
    # Row names unnamed controls after its title, which would hide the verb.
    button.setAccessibleName(text.rstrip("…"))
    button.clicked.connect(slot)
    return button


def _value(text: str) -> ToneLabel:
    """A value on the right of a row, selectable for bug reports."""
    label = ToneLabel(text)
    label.setAccessibleName(text)
    label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    return label


class _Worker(QThread):
    done = pyqtSignal(bool, str)

    def __init__(self, fn):
        super().__init__()
        self._fn = fn

    def run(self):
        self.done.emit(*safe_call(self._fn))


class _AppUpdateWorker(QThread):
    """Asks GitHub for the newest adguard-tray release."""
    done = pyqtSignal(object, bool, str)   # release, newer, error

    def run(self):
        from .updates import check
        try:
            release, newer, error = check()
        except Exception as exc:
            logger.exception("Update check failed")
            release, newer, error = None, False, str(exc)
        self.done.emit(release, newer, error)


class _InstallKindWorker(QThread):
    """detect_install() shells out to pacman – not on the GUI thread."""
    done = pyqtSignal(object)

    def run(self):
        from .updates import detect_install
        try:
            self.done.emit(detect_install())
        except Exception:
            logger.exception("Install detection failed")
            self.done.emit(None)


class _SelfUpdateWorker(QThread):
    """Downloads and installs a release into a ~/.local installation."""
    done = pyqtSignal(bool, str)

    def __init__(self, release):
        super().__init__()
        self._release = release

    def run(self):
        from .updates import self_update
        try:
            ok, msg = self_update(self._release)
        except Exception as exc:
            logger.exception("Self-update failed")
            ok, msg = False, str(exc)
        self.done.emit(ok, msg)


class _RefreshWorker(QThread):
    done = pyqtSignal(object)  # dict with version, channel, license

    def __init__(self, cli):
        super().__init__()
        self.cli = cli

    def run(self):
        try:
            data = {"version": self.cli.get_version(), "channel": self.cli.get_update_channel()}
            ok, lic = self.cli.get_license()
        except Exception as exc:  # would otherwise abort the process (qFatal)
            logger.exception("About refresh failed")
            data = {"version": "", "channel": ""}
            ok, lic = False, str(exc)
        data["license_ok"] = ok
        data["license"] = lic
        self.done.emit(data)


class AboutTab(Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(parent=parent)
        self.ctx = ctx
        self._workers: list[QThread] = []
        self._refreshing = False
        self._acting = False        # a CLI action (update, channel, reset) is running
        self._app_busy = False      # the app's own update check or install is running
        self._channel_loaded = False
        self._release = None
        self._install = Install()

        tray = self.section(_t("AdGuard Tray"))
        self.row_app = tray.add_row(Row(_t("Version"), _t("Checking…"), _value(__version__)))
        self.btn_release = LinkButton(_t("Open release page"), self._open_release)
        self.btn_release.setAccessibleName(_t("Open release page"))
        self.btn_release.hide()
        self.btn_app_install = _button(_t("Install update"), self._do_app_install)
        self.btn_app_install.setDefault(True)
        self.btn_app_install.hide()
        self.btn_app_restart = _button(_t("Restart now"), self._restart_app)
        self.btn_app_restart.hide()
        self.btn_app_check = _button(_t("Check for update"), self._do_app_update_check)
        self.row_app_update = self._row(tray, _t("Updates"), _t("Asks GitHub for the newest release."),
                                        self.btn_release, self.btn_app_install, self.btn_app_restart,
                                        self.btn_app_check)
        link = LinkButton(PROJECT_URL.removeprefix("https://"),
                          lambda: QDesktopServices.openUrl(QUrl(PROJECT_URL)))
        link.setToolTip(PROJECT_URL)
        link.setAccessibleName(PROJECT_URL)
        tray.add_row(Row(_t("Source code"), _t("MIT license"), link))

        cli = self.section(_t("AdGuard CLI"))
        self.lbl_cli_version = _value(_t("Loading…"))
        self.row_cli = cli.add_row(Row(_t("Version"), "", self.lbl_cli_version))

        self.btn_cli_update = _button(_t("Update AdGuard CLI…"), self._do_cli_update)
        self.row_cli_update = self._row(cli, _t("Updates"),
                                        _t("Downloads and installs the newest AdGuard CLI build."),
                                        self.btn_cli_update)

        # A new channel is set at once, so scrolling past it must not change it.
        self.combo_channel = ignore_idle_wheel(QComboBox())
        for channel in ctx.cli.UPDATE_CHANNELS:
            self.combo_channel.addItem(_channel_label(channel), channel)
        self.combo_channel.setEnabled(False)   # until the current channel is known
        self.combo_channel.currentIndexChanged.connect(self._on_channel_changed)
        self._channel_hint = _t("Controls which AdGuard CLI build “{}” installs.", _t("Update AdGuard CLI"))
        self.row_channel = self._row(cli, _t("Update channel"), self._channel_hint, self.combo_channel)

        self.btn_filters = _button(_t("Update"), self._do_update_filters)
        self.btn_filters.setAccessibleName(_t("Update filters"))
        self.row_filters = self._row(
            cli, _t("Update filters"),
            # The same words as the Filters page: both rows run adguard-cli check-update.
            one_line(_t("Updates all filters, DNS filters, userscripts,\n"
                        "SafebrowsingV2, CRLite and checks for app updates.")), self.btn_filters)

        self.license_card = self.section(_t("License"))
        self._show_license(True, _t("Loading…"))

        self.finish()
        self._describe_install()
        self.refresh()

    def _row(self, card, title: str, subtitle: str, *controls) -> Row:
        """A row whose spinner turns while its action runs."""
        row = card.add_row(Row(title, subtitle))
        for widget in (Spinner(), *controls):
            row.add_control(widget)
        return row

    def _start(self, worker: QThread, slot) -> None:
        worker.done.connect(slot)
        worker.finished.connect(lambda: self._workers.remove(worker) if worker in self._workers else None)
        self._workers.append(worker)
        worker.start()

    def _sync(self) -> None:
        cli_busy = self._acting or self._refreshing
        for button in (self.btn_cli_update, self.btn_filters, self.btn_reset):
            button.setEnabled(not cli_busy)
        # The app's update check or install runs on its own; a finishing CLI
        # action must not hand those buttons back mid-flight.
        for button in (self.btn_app_check, self.btn_app_install, self.btn_app_restart):
            button.setEnabled(not cli_busy and not self._app_busy)
        self.combo_channel.setEnabled(not cli_busy and self._channel_loaded)

    # ── CLI version, channel, licence ────────────────────────────────────────

    def refresh(self) -> None:
        if self._refreshing or self._acting:
            return
        self._refreshing = True
        self._sync()
        self.row_cli.set_subtitle(shutil.which(self.ctx.cli.BINARY) or _t("adguard-cli not found"))
        self._start(_RefreshWorker(self.ctx.cli), self._on_refreshed)

    def _on_refreshed(self, data: dict) -> None:
        self._refreshing = False
        version = data["version"] or "–"
        self.lbl_cli_version.setText(version)
        self.lbl_cli_version.setAccessibleName(version)

        channel = data["channel"]
        index = self.combo_channel.findData(channel) if channel else -1
        # An unknown or unreadable channel keeps the combo disabled.
        self._channel_loaded = index >= 0
        if self._channel_loaded:
            self.combo_channel.blockSignals(True)
            self.combo_channel.setCurrentIndex(index)
            self.combo_channel.blockSignals(False)
        self.row_channel.set_subtitle(
            self._channel_hint if self._channel_loaded
            else _t("Unavailable until AdGuard CLI reports its current channel."))

        self._show_license(data["license_ok"], data["license"])
        self._sync()

    def _show_license(self, ok: bool, text: str) -> None:
        card = self.license_card
        card.clear_rows()
        text = mask_license(text or "")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if ok and any(": " in line for line in lines):
            facts = [line.partition(": ")[::2] for line in lines]
        elif ok and text:           # e.g. "You are using the free version"
            facts = []
            caption = Caption(text)
            caption.setContentsMargins(14, 12, 12, 12)
            card.add_row(caption)
        else:                       # the error itself goes to the banner
            facts = [(_t("Status"), _t("Unknown"))]
        for key, value in facts:
            value = value.strip()
            # mask_license only knows the exact "License key: " spelling.
            if value and "key" in key.lower():
                value = value[:4] + "****"
            row = card.add_row(Row(_license_word(key.strip()), "", _value(_license_word(value))))
            row.setMinimumHeight(38)     # one-line facts, denser than settings
        self.btn_reset = _button(_t("Reset…"), self._do_reset_license)
        self.row_reset = self._row(card, _t("Reset license"), _reset_text(), self.btn_reset)
        # A rebuilt button joins the end of the window's focus chain; keep it after the page above.
        QWidget.setTabOrder(self.btn_filters, self.btn_reset)

        failed = _t("Could not retrieve license info.")
        ours = not self.banner.isHidden() and self.banner.text.text() == failed
        if not ok and (self.banner.isHidden() or ours):
            # Not over the result of an action that just finished.
            self.banner.show_message(failed, "danger", details=text)
        elif ok and ours:
            self.banner.hide()

    # ── CLI actions ────────────────────────────────────────────────────────

    def _run_cli(self, row: Row, busy_text: str, fn, done) -> None:
        self._acting = True
        idle_text = row.subtitle.text()
        if busy_text:
            row.set_subtitle(busy_text)
        spinner = row.findChild(Spinner)
        spinner.set_busy(True)
        self._sync()

        def finished(ok: bool, msg: str) -> None:
            self._acting = False
            spinner.set_busy(False)
            row.set_subtitle(idle_text)
            self._sync()
            done(ok, msg)
            if ok and self.ctx.on_status_change:
                self.ctx.on_status_change()
            self.refresh()

        self._start(_Worker(fn), finished)

    def _report(self, ok: bool, success: str, failure: str, output: str = "") -> None:
        if ok:
            self.banner.show_message(success, "success", details=output, timeout_ms=5000)
        else:
            self.banner.show_message(failure, "danger", details=output)

    def _do_cli_update(self) -> None:
        # `adguard-cli update` installs whatever it finds, it does not only check.
        body = _t("AdGuard CLI downloads and installs its newest build.")
        if self._channel_loaded:
            body += "\n\n" + _t("Update channel: {}", self.combo_channel.currentText())
        if not confirm(self, _t("Update AdGuard CLI"), body, _t("Install update"), destructive=False):
            return
        self._run_cli(self.row_cli_update, _t("Checking for updates…"), self.ctx.cli.check_cli_update,
                      lambda ok, msg: self._report(ok, _t("AdGuard CLI update finished."),
                                                   _t("Could not update AdGuard CLI."), msg))

    def _on_channel_changed(self, index: int) -> None:
        if not self._channel_loaded or index < 0:
            return
        channel = self.combo_channel.itemData(index)
        label = self.combo_channel.itemText(index)
        self._run_cli(self.row_channel, _t("Switching update channel to {}…", label),
                      lambda: self.ctx.cli.set_update_channel(channel),
                      lambda ok, msg: self._report(ok, _t("Update channel set to {}", label),
                                                   _t("Could not set the update channel."), "" if ok else msg))

    def _do_update_filters(self) -> None:
        def done(ok: bool, msg: str) -> None:
            if not ok:
                self._report(False, "", _t("Could not update the filters."), msg)
                return
            # The running proxy only picks up the new lists after a restart.
            if self.ctx.on_restart:
                self.ctx.on_restart()
            status = self.ctx.status() if self.ctx.status else None
            if status in (AdGuardStatus.INACTIVE, AdGuardStatus.NOT_INSTALLED):
                after = _t("The new lists load when protection is turned on.")
            else:
                after = _t("AdGuard restarts to load the new lists.")
            self._report(True, f"{_t('Update completed.')} {after}", "", msg)

        self._run_cli(self.row_filters, _t("Updating filters… (can take up to 2 minutes)"),
                      self.ctx.cli.update_filters, done)

    def _do_reset_license(self) -> None:
        if not confirm(self, _t("Reset license"), _reset_text(), _t("Reset license")):
            return
        self._run_cli(self.row_reset, "", self.ctx.cli.reset_license,
                      lambda ok, msg: self._report(ok, _t("License reset"), _t("Could not reset the license."), msg))

    # ── adguard-tray's own version ─────────────────────────────────────────

    def _describe_install(self) -> None:
        self._start(_InstallKindWorker(), self._on_install_detected)

    def _on_install_detected(self, install) -> None:
        self._install = install or Install()
        where = {
            "pacman": lambda: _t("Installed with the AUR package {}",
                                 self._install.package or "adguard-tray"),
            "local": lambda: _t("Installed in {}", str(self._install.root or "")),
            "source": lambda: _t("Running from a source checkout"),
        }.get(self._install.kind, lambda: _t("Installation not recognised"))()
        self.row_app.set_subtitle(where)

    def _set_app_result(self, text: str, tone: str = "secondary") -> None:
        self.row_app_update.set_subtitle(text)
        self.row_app_update.subtitle.set_tone(tone)

    def _set_app_busy(self, busy: bool) -> None:
        self._app_busy = busy
        self.row_app_update.findChild(Spinner).set_busy(busy)
        self._sync()

    def _do_app_update_check(self) -> None:
        self.btn_app_install.hide()
        self.btn_release.hide()
        self._set_app_result(_t("Checking for updates…"))
        self._set_app_busy(True)
        self._start(_AppUpdateWorker(), self._on_app_update_checked)

    def _on_app_update_checked(self, release, newer: bool, error: str) -> None:
        self._set_app_busy(False)
        self._release = release
        if error or release is None:
            self._set_app_result(error or _t("Could not check for updates."), "danger")
            return
        if not newer:
            self._set_app_result(_t("You are running the latest version ({}).", __version__))
            return
        message = _t("Version {} is available (you have {}).", release.version, __version__)
        command = update_command(self._install)
        if self._install.can_self_update:
            self.btn_app_install.show()
        elif command:
            message += "\n" + _t("Update with: {}", command)
        else:
            self.btn_release.show()
        self._set_app_result(message)

    def _open_release(self) -> None:
        if self._release is not None:
            QDesktopServices.openUrl(QUrl(self._release.url))

    def _do_app_install(self) -> None:
        if self._release is None:
            return
        self._set_app_result(_t("Installing update…"))
        self._set_app_busy(True)
        self._start(_SelfUpdateWorker(self._release), self._on_app_installed)

    def _on_app_installed(self, ok: bool, msg: str) -> None:
        self._set_app_busy(False)
        self._set_app_result(msg, "secondary" if ok else "danger")
        if not ok:
            return
        self.btn_app_install.hide()
        self.btn_app_restart.show()     # for "Later", or when the restart has to wait
        # The running process still holds the old modules; anything imported
        # lazily from here on would mix versions.
        box = QMessageBox(self)
        box.setWindowTitle(_t("Application update"))
        box.setText(msg)
        restart = box.addButton(_t("Restart now"), QMessageBox.ButtonRole.AcceptRole)
        box.addButton(_t("Later"), QMessageBox.ButtonRole.RejectRole)
        box.exec()
        if box.clickedButton() is restart:
            self._restart_app()

    def _restart_app(self) -> None:
        if self.ctx.settings.dirty():
            # A quit would drop them, and applying them queues an AdGuard
            # restart that the quit would cut off.
            self.banner.show_message(
                _t("Apply or discard your changes to AdGuard's settings first, then restart."), "warning")
            return

        from .main import _resolve_exec

        argv = _resolve_exec()
        if argv:
            QProcess.startDetached(argv[0], argv[1:])
        QApplication.quit()
