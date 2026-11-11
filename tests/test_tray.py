import os
import shlex
import time
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest  # noqa: E402
from PyQt6.QtCore import QThreadPool  # noqa: E402
from PyQt6.QtTest import QTest  # noqa: E402

from adguard_tray import installer, tray, vpn  # noqa: E402
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
