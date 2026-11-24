import os
import shlex
import threading
import time
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest  # noqa: E402
from PyQt6.QtCore import QThreadPool  # noqa: E402
from PyQt6.QtTest import QTest  # noqa: E402

from adguard_tray import installer, tray, vpn, worker  # noqa: E402
from adguard_tray.cli import AdGuardStatus, FilterListResult, StatusResult, UserscriptListResult  # noqa: E402
from adguard_tray.config import Config  # noqa: E402


@pytest.mark.parametrize(("msg", "expected"), [
    ("first line\nsecond line\n", "first line"),
    ("x" * 400 + "\nsecond line", "x" * 300),
])
def test_report_error_notifies_one_short_line(monkeypatch, msg, expected):
    sent = []
    monkeypatch.setattr(tray, "notify", lambda title, body, **kw: sent.append(body))
    fake = SimpleNamespace(
        config=SimpleNamespace(notifications_enabled=True),
        _act_status=SimpleNamespace(setText=lambda text: None),
        setToolTip=lambda text: None,
        _last_status=AdGuardStatus.ERROR,
    )

    tray.AdGuardTray._report_error(fake, msg)

    assert sent == [expected]


PATH = "/usr/bin/adguardvpn-cli"


def wait_for(cond, timeout=5.0):
    end = time.monotonic() + timeout
    while not cond():
        assert time.monotonic() < end, "timed out"
        QTest.qWait(10)


@pytest.fixture
def fake_vpn(monkeypatch):
    calls = SimpleNamespace(status=[], connect=[], disconnect=[], terminal=[])
    state = SimpleNamespace(status=vpn.VpnStatus(True, "VPN is disconnected"), mode="socks",
                            connect=(True, ""), disconnect=(True, ""), path=PATH)
    monkeypatch.setattr(vpn, "find", lambda: state.path)
    monkeypatch.setattr(vpn, "status", lambda path: calls.status.append(path) or state.status)
    monkeypatch.setattr(vpn, "read_config", lambda path: (vpn.VpnConfig(mode=state.mode), ""))
    monkeypatch.setattr(vpn, "connect", lambda path, loc: calls.connect.append((path, loc)) or state.connect)
    monkeypatch.setattr(vpn, "disconnect", lambda path: calls.disconnect.append(path) or state.disconnect)
    monkeypatch.setattr(installer, "open_in_terminal", lambda command: calls.terminal.append(command) or True)
    state.calls = calls
    return state


@pytest.fixture
def make_tray(app):
    made = []

    def make():
        cli = SimpleNamespace(
            get_status=lambda: StatusResult(AdGuardStatus.INACTIVE),
            get_filters=FilterListResult, get_userscripts=UserscriptListResult, get_version=lambda: "1.0",
        )
        t = tray.AdGuardTray(app, cli, Config(notifications_enabled=False), "adguard-tray")
        made.append(t)
        return t

    yield make
    for t in made:
        # Let the startup loaders run out first: a queued slot on a deleted tray crashes Qt.
        QTest.qWait(20)
        wait_for(lambda t=t: not t._bg_threads)
        t.shutdown()
        QTest.qWait(20)


def vpn_entries(t):
    t._vpn_menu.aboutToShow.emit()
    wait_for(lambda: not t._loading_vpn)
    return {a.text(): a for a in t._vpn_menu.actions() if not a.isSeparator()}


def wait_action_done():
    QThreadPool.globalInstance().waitForDone(5000)
    QTest.qWait(20)


def test_no_vpn_binary_no_submenu(make_tray, fake_vpn):
    fake_vpn.path = ""
    t = make_tray()
    t._refresh_dynamic_menu_state()
    assert not t._vpn_menu.menuAction().isVisible()
    assert fake_vpn.calls.status == []


def test_vpn_logged_out_shows_only_page_entry(make_tray, fake_vpn, monkeypatch):
    fake_vpn.status = vpn.VpnStatus(False, "You are not logged in")
    t = make_tray()
    assert t._vpn_menu.menuAction().isVisible()
    entries = vpn_entries(t)
    assert list(entries) == ["Not logged in", "VPN"]
    assert not entries["Not logged in"].isEnabled()
    shown = []
    monkeypatch.setattr(t, "_show_manager", shown.append)
    entries["VPN"].trigger()
    assert shown == [tray.PAGE_VPN]


def test_vpn_connect_socks_runs_off_thread_and_reports_failure(make_tray, fake_vpn):
    fake_vpn.connect = (False, "boom\nmore")
    t = make_tray()
    entries = vpn_entries(t)
    assert list(entries) == ["VPN is disconnected", "Connect", "VPN"]
    entries["Connect"].trigger()
    wait_action_done()
    assert fake_vpn.calls.connect == [(PATH, None)]
    assert fake_vpn.calls.terminal == []
    assert t._act_status.text() == "Error: boom"


def test_vpn_connected_offers_disconnect(make_tray, fake_vpn):
    fake_vpn.status = vpn.VpnStatus(True, "Connected to FRANKFURT in SOCKS mode, listening on 127.0.0.1:1080\nmore")
    t = make_tray()
    entries = vpn_entries(t)
    assert list(entries) == ["Connected to FRANKFURT in SOCKS mode, listening on 127.0.0.1:1080", "Disconnect", "VPN"]
    entries["Disconnect"].trigger()
    wait_action_done()
    assert fake_vpn.calls.disconnect == [PATH]


def test_vpn_connect_tun_opens_terminal(make_tray, fake_vpn):
    fake_vpn.mode = "tun"
    t = make_tray()
    vpn_entries(t)["Connect"].trigger()
    wait_action_done()
    assert fake_vpn.calls.terminal == [shlex.join(vpn.connect_command(PATH, None))]
    assert fake_vpn.calls.connect == []


def test_vpn_submenu_is_not_rebuilt_while_unchanged(make_tray, fake_vpn):
    t = make_tray()
    first = list(vpn_entries(t).values())
    assert list(vpn_entries(t).values()) == first, "same actions: a rebuild closes the open submenu on GNOME"
    fake_vpn.status = vpn.VpnStatus(True, "Connected to PARIS in SOCKS mode, listening on 127.0.0.1:1080")
    assert list(vpn_entries(t))[:2] == ["Connected to PARIS in SOCKS mode, listening on 127.0.0.1:1080", "Disconnect"]


def test_vpn_status_error_shows_first_line(make_tray, fake_vpn):
    fake_vpn.status = vpn.VpnStatus(False, "", "adguardvpn-cli failed with exit code 3\ndetails")
    t = make_tray()
    assert list(vpn_entries(t)) == ["Error: adguardvpn-cli failed with exit code 3", "VPN"]


class SlowStatus:
    """get_status that reads the state when called, then blocks until released."""

    def __init__(self, status):
        self.status = status
        self.release = threading.Event()
        self.started = 0

    def get_status(self):
        self.started += 1
        status = self.status
        self.release.wait(5)
        return StatusResult(status)


def settle():
    QThreadPool.globalInstance().waitForDone()
    QTest.qWait(20)


def started_worker(fake):
    w = worker.StatusWorker(fake)
    seen = []
    w.status_updated.connect(lambda r: seen.append(r.status))
    w.start()
    wait_for(lambda: fake.started == 1)
    return w, seen


def poll_once(status, act):
    fake = SlowStatus(AdGuardStatus.ACTIVE)
    w, seen = started_worker(fake)
    act(w)
    fake.status = status
    fake.release.set()
    wait_for(lambda: seen)
    settle()
    w.stop()
    return fake, seen


def test_refresh_during_a_poll_drops_the_older_result():
    # The poll started before a stop; the tray's refresh after it must not report "active".
    fake, seen = poll_once(AdGuardStatus.INACTIVE, lambda w: w.refresh())
    assert seen == [AdGuardStatus.INACTIVE]
    assert fake.started == 2


def test_timer_tick_during_a_poll_keeps_its_result():
    fake, seen = poll_once(AdGuardStatus.INACTIVE, lambda w: w._timer.timeout.emit())
    assert seen == [AdGuardStatus.ACTIVE]
    assert fake.started == 1


def test_refresh_during_a_poll_then_stop_starts_nothing():
    fake = SlowStatus(AdGuardStatus.ACTIVE)
    w, seen = started_worker(fake)
    w.refresh()
    w.stop()        # tray shutdown
    fake.release.set()
    settle()
    assert fake.started == 1
    assert seen == []


def test_refresh_without_a_pending_poll_emits_its_result():
    fake = SlowStatus(AdGuardStatus.ACTIVE)
    fake.release.set()
    w, seen = started_worker(fake)
    wait_for(lambda: seen)
    settle()
    fake.status = AdGuardStatus.INACTIVE
    w.refresh()
    wait_for(lambda: len(seen) == 2)
    settle()
    w.stop()
    assert seen == [AdGuardStatus.ACTIVE, AdGuardStatus.INACTIVE]
    assert fake.started == 2


STOPPED = "AdGuard has been stopped."
STARTED = "AdGuard is now active – protection running."


@pytest.fixture
def status_tray(make_tray, monkeypatch):
    t = make_tray()
    wait_for(lambda: t._last_status is not None)  # the startup poll
    t._last_status = None
    t.config.notifications_enabled = True
    t.sent = []
    monkeypatch.setattr(tray, "notify", lambda title, body, **kw: t.sent.append(body))
    return t


def push(t, status, message=""):
    t._on_status_result(StatusResult(status, message))


def test_first_status_is_not_notified(status_tray):
    push(status_tray, AdGuardStatus.ACTIVE)
    assert status_tray.sent == []


def test_status_change_notifies_once(status_tray):
    push(status_tray, AdGuardStatus.ACTIVE)
    push(status_tray, AdGuardStatus.INACTIVE)
    assert status_tray.sent == [STOPPED]
    push(status_tray, AdGuardStatus.INACTIVE)
    assert status_tray.sent == [STOPPED]


def test_flapping_status_notifies_every_change_so_the_last_popup_is_current(status_tray):
    for status in (AdGuardStatus.ACTIVE, AdGuardStatus.INACTIVE, AdGuardStatus.ACTIVE, AdGuardStatus.INACTIVE):
        push(status_tray, status)
    assert status_tray.sent == [STOPPED, STARTED, STOPPED]


def test_error_status_message_goes_into_tooltip(status_tray):
    push(status_tray, AdGuardStatus.ERROR, "adguard-cli timed out")
    assert "Error: adguard-cli timed out" in status_tray.toolTip().splitlines()


@pytest.fixture
def restart_tray(make_tray):
    t = make_tray()
    wait_for(lambda: t._last_status is not None)
    t.calls = []
    t.cli.get_status = lambda: t.calls.append("status") or StatusResult(AdGuardStatus.ACTIVE)
    t.cli.restart = lambda: t.calls.append("restart") or (True, "restarted")
    t._refresh_status_soon = lambda: None  # no 2 s re-poll timer left behind
    t._restart_pending = True
    return t


@pytest.mark.parametrize("status", [AdGuardStatus.INACTIVE, AdGuardStatus.NOT_INSTALLED])
def test_queued_restart_is_dropped_while_adguard_is_off(restart_tray, status):
    restart_tray._last_status = status
    restart_tray._fire_pending_restart()
    wait_action_done()
    assert not restart_tray._restart_pending
    assert restart_tray.calls == []


def test_queued_restart_runs_while_adguard_is_active(restart_tray):
    restart_tray._last_status = AdGuardStatus.ACTIVE
    restart_tray._fire_pending_restart()
    wait_action_done()
    assert restart_tray.calls == ["status", "restart"]
    assert not restart_tray._restart_pending
    assert not restart_tray._busy


@pytest.mark.parametrize(("status", "expected", "restarts"), [
    (AdGuardStatus.INACTIVE, (True, ""), 0),
    (AdGuardStatus.ACTIVE, (False, "boom"), 1),
    (AdGuardStatus.ERROR, (False, "boom"), 1),
])
def test_restart_if_running_asks_the_cli_first(status, expected, restarts):
    restarted = []
    cli = SimpleNamespace(get_status=lambda: StatusResult(status),
                          restart=lambda: restarted.append(1) or (False, "boom"))
    assert tray.AdGuardTray._restart_if_running(SimpleNamespace(cli=cli)) == expected
    assert len(restarted) == restarts
