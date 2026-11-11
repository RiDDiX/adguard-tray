import json
import logging
import os
import shlex
import time
from types import SimpleNamespace

import pytest
from PyQt6 import sip
from PyQt6.QtTest import QTest

from adguard_tray import installer, proxy_settings, vpn, vpn_tab
from adguard_tray.proxy_settings import ProxySettings

# adguardvpn-cli 1.8.2 as measured. State in files next to it: "logged-in", "broken",
# "connected" (the city), "mode" (socks/tun), "readonly" (set-mode fails), "unavailable"
# (status exit 10), "licence-fails" (exit 12), "login-fails" (exit 1), "login-silent"
# (no link); "calls" logs argv.
FAKE = r"""#!/usr/bin/env python3
import json, os, select, sys
here = os.path.dirname(os.path.abspath(__file__))
def path(name):
    return os.path.join(here, name)
def read(name, default=""):
    return open(path(name)).read() if os.path.exists(path(name)) else default
with open(path("calls"), "a") as f:
    f.write(json.dumps(sys.argv[1:]) + "\n")
UPSELL = "You are using a FREE version. Upgrade at https://agrd.io/vpn_cli to get more locations and higher speeds"
marker = path("logged-in")
mode = read("mode", "socks")
cmd = sys.argv[1:2]
args = sys.argv[1:]
if cmd == ["login"]:
    with open(path("login.pid"), "w") as f:
        f.write(str(os.getpid()))
    if os.path.exists(path("login-fails")):
        print("Failed to log in: the server did not answer")
        sys.exit(1)
    if not os.path.exists(path("login-silent")):
        print("You need to authorize in your browser. The following link will be available for 1799 seconds: "
              "\x1b[1mhttps://auth.adguard.io/device_code?user_code=ABCD-EFGH\x1b[0m")
        print("b - Open link in browser")
        print("x - Cancel")
    sys.stdout.flush()
    while not os.path.exists(marker):
        if select.select([sys.stdin], [], [], 0.05)[0]:
            key = sys.stdin.read(1)
            if key in ("x", ""):
                with open(path("login.end"), "w") as f:
                    f.write(key or "eof")
                sys.exit(0)
    print("Successfully logged in")
    sys.exit(0)
if cmd == ["status"] and os.path.exists(path("broken")):
    sys.exit(3)
if not os.path.exists(marker) and cmd != ["config"]:
    print("You are not logged in")
    print(f"You can log in by running `{sys.argv[0]} login`")
    sys.exit(11)
if cmd == ["connect"] and os.path.exists(path("connected")):
    print("Disconnecting from current location to connect elsewhere...")
print("Log is being written to: /home/u/.local/share/adguardvpn-cli/app.log")
if cmd == ["logout"]:
    os.remove(marker)
    print("Logged out")
    sys.exit(0)
if cmd == ["status"] and os.path.exists(path("unavailable")):
    print("VPN active, but status unavailable")
    sys.exit(10)
if cmd == ["status"]:
    city = read("connected")
    if not city:
        print("VPN is disconnected")
        print(f"You can connect by running `{sys.argv[0]} connect`")
    elif mode == "tun":
        print(f"Connected to {city} in TUN mode, running on tun0")
    else:
        print(f"Connected to {city} in SOCKS mode, listening on 127.0.0.1:1080")
    print(UPSELL)
    sys.exit(0)
if cmd == ["license"] and os.path.exists(path("licence-fails")):
    print("Logged in as user@example.com\nFailed to get license information")
    sys.exit(12)
if cmd == ["license"]:
    print("Logged in as user@example.com\nYou are using the FREE version\nUp to 2 devices simultaneously")
    print("You have 3.00 GB left for this month")
    print(UPSELL)
    sys.exit(0)
if cmd == ["list-locations"]:
    print("ISO   COUNTRY              CITY                           PING ESTIMATE")
    print("DE    Germany              Frankfurt                      25")
    print("GB    United Kingdom       London                         70")
    print("US    United States        New York                       139")
    print("US    United States        Miami                          150")
    print()
    print(f"You can connect to a location by running `{sys.argv[0]} connect -l <city>`")
    sys.exit(0)
if cmd == ["connect"]:
    cities = {"frankfurt": "FRANKFURT", "de": "FRANKFURT", "london": "LONDON", "new york": "NEW YORK"}
    city = "FRANKFURT" if args[1:] == ["-f"] else cities.get(args[2].lower()) if args[1:2] == ["-l"] else None
    if city is None:
        if os.path.exists(path("connected")):
            os.remove(path("connected"))
        print("Failed to start the VPN service in the background: There is no location with the specified "
              "city name, country name, or ISO code. To see the available options, please run `list-locations`")
        sys.exit(13)
    with open(path("connected"), "w") as f:
        f.write(city)
    print(f"Successfully Connected to {city}")
    print(UPSELL)
    sys.exit(0)
if cmd == ["disconnect"]:
    if not os.path.exists(path("connected")):
        print("Failed to disconnect. Process is not running")
        sys.exit(14)
    os.remove(path("connected"))
    print("VPN stopped")
    print(f"You can connect by running `{sys.argv[0]} connect`")
    sys.exit(0)
if args[:2] == ["config", "set-mode"]:
    if os.path.exists(path("readonly")):
        print("Permission denied", file=sys.stderr)
        sys.exit(1)
    mode = args[2]
    with open(path("mode"), "w") as f:
        f.write(mode)
    print("Config has been updated")
    if os.path.exists(path("connected")):
        # Restarts the VPN in the new mode itself; TUN fails without a terminal.
        os.remove(path("connected"))
        print("Failed to start the VPN service in the background: sudo: a terminal is required")
        sys.exit(13)
if args[:2] in (["config", "show"], ["config", "set-mode"]):
    print(f"\tMode: {mode}\n\tSOCKS port: 1080\n\tSOCKS host: 127.0.0.1")
    sys.exit(0)
sys.exit(1)
"""

PROXY_YAML = """proxy_mode: auto
outbound_proxy:
  enabled: false
  mode: HTTP
  host: localhost
  port: 3128
apps: []
"""


@pytest.fixture
def fake(tmp_path, monkeypatch):
    path = tmp_path / "adguardvpn-cli"
    path.write_text(FAKE)
    path.chmod(0o755)
    monkeypatch.setattr(vpn, "find", lambda: str(path))
    return path


@pytest.fixture
def settings(app, tmp_path, monkeypatch):
    yaml = tmp_path / "proxy.yaml"
    yaml.write_text(PROXY_YAML)
    monkeypatch.setattr(proxy_settings, "PROXY_YAML", yaml)
    return ProxySettings()


def make_tab(settings):
    tab = vpn_tab.VpnTab(SimpleNamespace(settings=settings))
    tab.refresh()
    wait_idle(tab)
    return tab


@pytest.fixture
def tab(app, fake, settings):
    tab = make_tab(settings)
    yield tab
    if not sip.isdeleted(tab):
        sip.delete(tab)


@pytest.fixture
def logged_in(fake):
    (fake.parent / "logged-in").touch()
    return fake


def calls(fake) -> list[list[str]]:
    return [json.loads(line) for line in (fake.parent / "calls").read_text().splitlines()]


def wait_for(cond, timeout=5.0):
    deadline = time.monotonic() + timeout
    while not cond():
        assert time.monotonic() < deadline, "timed out"
        QTest.qWait(10)


def wait_idle(tab):
    wait_for(lambda: not tab._busy and not tab._workers and tab._login is None)


def alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


def start_login(tab, fake):
    tab.btn_login.click()
    wait_for(lambda: tab._link)
    pidfile = fake.parent / "login.pid"
    wait_for(pidfile.exists)
    return int(pidfile.read_text())


def test_missing_binary_offers_install(app, settings, monkeypatch):
    monkeypatch.setattr(vpn, "find", lambda: "")
    tab = make_tab(settings)
    assert not tab.install_box.isHidden()
    assert tab.account_box.isHidden() and tab.connection_box.isHidden() and tab.mode_box.isHidden()
    sip.delete(tab)


def test_logged_out(tab):
    assert tab.install_box.isHidden()
    assert tab.account_row.title.text() == "Not logged in"
    assert not tab.btn_login.isHidden()
    assert tab.btn_logout.isHidden()
    assert tab.connection_box.isHidden() and tab.mode_box.isHidden() and tab.licence.isHidden()


def test_failed_status_does_not_claim_logged_out(tab, fake):
    (fake.parent / "broken").touch()
    tab.refresh()
    wait_idle(tab)
    assert tab.account_row.title.text() != "Not logged in"
    assert tab.btn_login.isHidden() and tab.btn_logout.isHidden()
    assert not tab.banner.isHidden()


def test_cancel_ends_login(tab, fake):
    pid = start_login(tab, fake)
    assert tab.link_row.subtitle.text() == "https://auth.adguard.io/device_code?user_code=ABCD-EFGH"
    assert tab.btn_login.isHidden()
    tab._cancel_login()
    wait_idle(tab)
    assert not alive(pid)
    assert (fake.parent / "login.end").read_text() == "x"
    assert tab.link_row.isHidden()
    assert not tab.btn_login.isHidden()


def test_login_then_logged_in(tab, fake):
    start_login(tab, fake)
    (fake.parent / "logged-in").touch()
    wait_idle(tab)
    assert tab.link_row.isHidden()
    assert tab.account_row.title.text() == "Logged in"
    assert tab.btn_login.isHidden() and not tab.btn_logout.isHidden()
    assert not tab.connection_box.isHidden() and not tab.mode_box.isHidden()
    assert tab.status_text.text() == "VPN is disconnected"


def test_destroying_page_ends_login(tab, fake):
    pid = start_login(tab, fake)
    sip.delete(tab)
    assert not alive(pid)
    assert (fake.parent / "login.end").read_text() == "x"


def connect(tab, location=None):
    if location is not None:
        tab.location.setEditText(location)
    tab.btn_connect.click()
    wait_idle(tab)


def test_logged_in_shows_licence_and_locations(tab, logged_in):
    tab.refresh()
    wait_idle(tab)
    assert tab.licence.text() == ("Logged in as u***@example.com\nYou are using the FREE version\n"
                                  "Up to 2 devices simultaneously\nYou have 3.00 GB left for this month")
    assert not tab.licence.isHidden()
    assert tab.status_text.text() == "VPN is disconnected"
    assert [tab.location.itemText(i) for i in range(tab.location.count())] == [
        "Fastest location", "Germany – Frankfurt (25 ms)", "United Kingdom – London (70 ms)",
        "United States – New York (139 ms)", "United States – Miami (150 ms)"]
    assert tab.location.itemData(3) == "New York"
    assert tab.btn_disconnect.isHidden() and not tab.btn_connect.isHidden()
    assert tab.mode.currentData() == "socks"
    assert tab.banner.isHidden()


def test_connect_and_disconnect_in_socks_mode(tab, logged_in):
    tab.refresh()
    wait_idle(tab)
    connect(tab)
    assert calls(logged_in)[-3:] == [["connect", "-f"], ["status"], ["config", "show"]]
    assert tab.banner.text.text() == "Successfully Connected to FRANKFURT"
    assert tab.status_text.text() == "Connected to FRANKFURT in SOCKS mode, listening on 127.0.0.1:1080"
    assert not tab.btn_disconnect.isHidden()
    tab.location.setCurrentIndex(3)
    connect(tab)
    assert ["connect", "-l", "New York"] in calls(logged_in)
    assert tab.banner.text.text() == "Successfully Connected to NEW YORK"
    assert tab.status_text.text().startswith("Connected to NEW YORK")
    tab.btn_disconnect.click()
    wait_idle(tab)
    assert calls(logged_in)[-3:] == [["disconnect"], ["status"], ["config", "show"]]
    assert tab.status_text.text() == "VPN is disconnected"
    assert tab.btn_disconnect.isHidden()


def test_typed_location_is_passed_as_it_is(tab, logged_in):
    tab.refresh()
    wait_idle(tab)
    connect(tab, "  london ")
    assert ["connect", "-l", "london"] in calls(logged_in)
    assert tab.status_text.text().startswith("Connected to LONDON")


def test_unknown_location_ends_disconnected(tab, logged_in):
    tab.refresh()
    wait_idle(tab)
    connect(tab)
    connect(tab, "Atlantis")
    assert ["connect", "-l", "Atlantis"] in calls(logged_in)
    assert tab.banner.text.text().startswith("Error: Failed to start the VPN service")
    assert "Log is being" not in tab.banner.details.toPlainText()
    assert "Disconnecting" not in tab.banner.details.toPlainText()
    assert tab.status_text.text() == "VPN is disconnected"
    assert tab.btn_disconnect.isHidden()


def choose_mode(tab, mode):
    index = tab.mode.findData(mode)
    tab.mode.setCurrentIndex(index)
    tab.mode.activated.emit(index)
    wait_idle(tab)


def test_mode_change_disconnects_first(tab, logged_in):
    tab.refresh()
    wait_idle(tab)
    connect(tab)
    choose_mode(tab, "tun")
    assert calls(logged_in)[-5:] == [["status"], ["disconnect"], ["config", "set-mode", "tun"],
                                     ["config", "show"], ["status"]]
    assert (logged_in.parent / "mode").read_text() == "tun"
    assert tab.mode.currentData() == "tun"
    assert tab.status_text.text() == "VPN is disconnected"
    assert tab.banner.text.text() == "AdGuard VPN was disconnected to change its mode. Connect again."
    assert tab.banner._tone == "info"


def test_mode_change_while_disconnected_says_nothing(tab, logged_in):
    tab.refresh()
    wait_idle(tab)
    choose_mode(tab, "tun")
    assert ["disconnect"] not in calls(logged_in)
    assert tab.mode.currentData() == "tun" and tab.banner.isHidden()


def test_mode_combo_follows_the_change_when_status_fails(tab, logged_in):
    tab.refresh()
    wait_idle(tab)
    (logged_in.parent / "broken").touch()
    choose_mode(tab, "tun")
    assert tab.mode.currentData() == "tun"


def test_tun_while_routed_stops_routing(tab, logged_in, settings):
    tab.refresh()
    wait_idle(tab)
    tab.route.click()
    assert settings.value(("outbound_proxy", "enabled")) is True
    choose_mode(tab, "tun")
    assert settings.value(("outbound_proxy", "enabled")) is False
    assert not tab.route.isChecked()
    assert "Press Apply" in tab.banner.text.text()


def test_mode_change_failure_goes_back(tab, logged_in):
    (logged_in.parent / "readonly").touch()
    tab.refresh()
    wait_idle(tab)
    index = tab.mode.findData("tun")
    tab.mode.setCurrentIndex(index)
    tab.mode.activated.emit(index)
    wait_idle(tab)
    assert tab.mode.currentData() == "socks"
    assert tab.banner.text.text() == "Error: Permission denied"


def test_route_switch(tab, logged_in, settings):
    (logged_in.parent / "mode").write_text("tun")
    tab.refresh()
    wait_idle(tab)
    assert not tab.route.isChecked() and tab.route.isEnabled()
    assert not tab.conflict.isHidden()
    assert tab.conflict.action.text() == "Route AdGuard through the VPN"
    tab.route.click()
    wait_idle(tab)
    assert (logged_in.parent / "mode").read_text() == "socks"
    assert settings.value(("outbound_proxy", "enabled")) is True
    assert settings.value(("outbound_proxy", "mode")) == "SOCKS5"
    assert settings.value(("outbound_proxy", "host")) == "127.0.0.1"
    assert settings.value(("outbound_proxy", "port")) == 1080
    assert settings.value(("apps",)) == [vpn.VPN_RULE]
    assert tab.route.isChecked() and tab.conflict.isHidden()
    assert tab.banner.text.text().startswith("AdGuard VPN now uses SOCKS5 mode.")
    tab.route.click()
    assert settings.value(("outbound_proxy", "enabled")) is False
    assert settings.value(("outbound_proxy", "port")) == 1080
    assert not tab.route.isChecked()
    settings.discard()
    assert not tab.route.isChecked()


def test_route_switch_follows_settings(tab, logged_in, settings):
    tab.refresh()
    wait_idle(tab)
    vpn.route_through(settings, vpn.VpnConfig("socks", "127.0.0.1", 1080), str(logged_in))
    assert tab.route.isChecked()
    settings.discard()
    assert not tab.route.isChecked()


def test_route_switch_disabled_without_settings(app, logged_in, tmp_path, monkeypatch):
    monkeypatch.setattr(proxy_settings, "PROXY_YAML", tmp_path / "missing.yaml")
    tab = make_tab(ProxySettings())
    assert not tab.route.isEnabled()
    assert not tab.route_row.subtitle.isHidden()
    assert tab.mode.isEnabled() and tab.mode.currentData() == "socks"
    sip.delete(tab)


def test_tun_connect_runs_in_a_terminal_and_polls(tab, logged_in, monkeypatch):
    (logged_in.parent / "mode").write_text("tun")
    opened = []
    monkeypatch.setattr(installer, "open_in_terminal", lambda command: opened.append(command) or True)
    monkeypatch.setattr(vpn_tab, "POLL_MS", 20)
    tab.refresh()
    wait_idle(tab)
    tab.location.setCurrentIndex(3)
    tab.btn_connect.click()
    assert opened == [shlex.join(vpn.connect_command(str(logged_in), "New York"))]
    assert tab.banner.text.text() == "AdGuard VPN asks for your password in the terminal window."
    assert tab._poll.isActive()
    wait_for(lambda: calls(logged_in).count(["status"]) >= 4)
    (logged_in.parent / "connected").write_text("NEW YORK")
    wait_for(lambda: not tab._poll.isActive())
    wait_idle(tab)
    assert tab.status_text.text() == "Connected to NEW YORK in TUN mode, running on tun0"
    assert not tab.btn_disconnect.isHidden()
    assert not any(call[0] == "connect" for call in calls(logged_in))


def test_typed_location_is_not_completed(tab, logged_in):
    tab.refresh()
    wait_idle(tab)
    tab.show()      # Qt only completes in a shown widget with focus
    assert QTest.qWaitForWindowExposed(tab)
    tab.location.lineEdit().setFocus()
    tab.location.clearEditText()
    QTest.keyClicks(tab.location.lineEdit(), "United")
    assert tab.location.currentText() == "United"
    connect(tab)
    assert calls(logged_in)[-3][-3:] == ["connect", "-l", "United"]


def test_cancel_before_the_link(tab, fake):
    (fake.parent / "login-silent").touch()
    tab.btn_login.click()
    wait_for((fake.parent / "login.pid").exists)
    assert not tab.link_row.isHidden() and not tab.btn_cancel.isHidden()
    assert tab.btn_open.isHidden()
    tab.btn_cancel.click()
    wait_idle(tab)
    assert (fake.parent / "login.end").read_text() == "x"
    assert tab.link_row.isHidden() and not tab.btn_login.isHidden()


def test_failed_login_shows_why(tab, fake):
    (fake.parent / "login-fails").touch()
    tab.btn_login.click()
    wait_idle(tab)
    assert tab.banner.text.text() == "Error: Failed to log in: the server did not answer"
    assert tab.link_row.isHidden() and not tab.btn_login.isHidden()


def test_login_that_cannot_start(tab, fake):
    tab._path = str(fake.parent / "missing")
    tab.btn_login.click()
    wait_idle(tab)
    assert tab.banner.text.text() == "Could not start adguardvpn-cli."
    assert not tab.btn_login.isHidden() and tab.btn_login.isEnabled()
    start_login(tab, fake)
    tab._cancel_login()
    wait_idle(tab)


def test_route_on_while_connected_says_it_disconnected(tab, logged_in, settings):
    (logged_in.parent / "mode").write_text("tun")
    (logged_in.parent / "connected").write_text("FRANKFURT")
    tab.refresh()
    wait_idle(tab)
    tab.route.click()
    wait_idle(tab)
    assert calls(logged_in)[-5:-2] == [["status"], ["disconnect"], ["config", "set-mode", "socks"]]
    assert settings.value(("outbound_proxy", "enabled")) is True
    assert tab.banner.text.text().startswith("AdGuard VPN was disconnected to change its mode.")


def tun_poll(tab, logged_in, monkeypatch, opened=None):
    opened = [] if opened is None else opened
    (logged_in.parent / "mode").write_text("tun")
    monkeypatch.setattr(installer, "open_in_terminal", lambda command: opened.append(command) or True)
    monkeypatch.setattr(vpn_tab, "POLL_MS", 20)
    tab.refresh()
    wait_idle(tab)


def test_poll_waits_for_a_new_connection_then_refreshes(tab, logged_in, monkeypatch):
    (logged_in.parent / "connected").write_text("FRANKFURT")
    tun_poll(tab, logged_in, monkeypatch)
    enabled = []
    tab._poll.timeout.connect(lambda: enabled.append(tab.btn_connect.isEnabled() and tab.mode.isEnabled())
                              if tab._busy else None)
    connect(tab, "London")
    assert tab._poll.isActive()
    (logged_in.parent / "unavailable").touch()
    start = calls(logged_in).count(["status"])
    wait_for(lambda: calls(logged_in).count(["status"]) >= start + 3)
    assert tab._poll.isActive()
    (logged_in.parent / "unavailable").unlink()
    start = calls(logged_in).count(["status"])
    wait_for(lambda: calls(logged_in).count(["status"]) >= start + 3)
    assert tab._poll.isActive(), "still the connection it started from"
    (logged_in.parent / "connected").write_text("LONDON")
    wait_for(lambda: not tab._poll.isActive())
    wait_idle(tab)
    assert calls(logged_in)[-3:] == [["status"], ["license"], ["config", "show"]]
    assert tab.status_text.text() == "Connected to LONDON in TUN mode, running on tun0"
    assert tab.banner.isHidden(), "the password hint goes once connected"
    assert enabled and all(enabled)


def test_poll_expiry_refreshes(tab, logged_in, monkeypatch):
    tun_poll(tab, logged_in, monkeypatch)
    monkeypatch.setattr(vpn_tab, "POLL_FOR", 0.2)
    connect(tab)
    wait_for(lambda: not tab._poll.isActive())
    wait_idle(tab)
    assert calls(logged_in)[-3:] == [["status"], ["license"], ["config", "show"]]
    assert tab.status_text.text() == "VPN is disconnected"
    assert tab.banner.isHidden(), "the password hint does not outlive the wait"


def test_refresh_while_busy_runs_once_afterwards(tab, logged_in):
    tab._run(lambda path: (time.sleep(0.2), (True, ""))[1])
    tab.refresh()
    tab.refresh()
    wait_idle(tab)
    assert calls(logged_in).count(["license"]) == 1


def test_failed_licence_keeps_its_text(tab, logged_in):
    (logged_in.parent / "licence-fails").touch()
    tab.refresh()
    wait_idle(tab)
    assert tab.licence.text() == "Logged in as u***@example.com\nFailed to get license information"
    assert tab.banner.isHidden()


def test_stale_error_goes_with_the_next_action(tab, logged_in):
    tab.refresh()
    wait_idle(tab)
    connect(tab, "Atlantis")
    assert tab.banner.text.text().startswith("Error:")
    tab.btn_logout.click()
    wait_idle(tab)
    assert tab.banner.isHidden()
    assert tab.location.count() == 1, "the locations go with the account"


def test_no_terminal_puts_the_command_on_the_clipboard(tab, logged_in, monkeypatch, app):
    (logged_in.parent / "mode").write_text("tun")
    monkeypatch.setattr(installer, "open_in_terminal", lambda command: False)
    tab.refresh()
    wait_idle(tab)
    tab.btn_connect.click()
    assert app.clipboard().text() == shlex.join([str(logged_in), "connect", "-f"])
    assert tab.banner.text.text().startswith("No terminal app was found.")
    assert not tab._poll.isActive()


def test_typed_location_reaches_the_terminal_quoted(tab, logged_in, monkeypatch):
    opened = []
    tun_poll(tab, logged_in, monkeypatch, opened)
    tab.location.setEditText("x'; touch pwned; '")
    tab.btn_connect.click()
    assert shlex.split(opened[0]) == [str(logged_in), "connect", "-l", "x'; touch pwned; '"]
    tab._poll.stop()


def test_worker_after_the_page_is_gone(tab, logged_in):
    tab._run(lambda path: (time.sleep(0.2), (True, "done"))[1])
    worker = tab._workers[0]
    sip.delete(tab)
    worker.wait()
    QTest.qWait(50)


def test_no_link_or_e_mail_in_the_log(tab, fake, caplog):
    caplog.set_level(logging.DEBUG)
    start_login(tab, fake)
    (fake.parent / "logged-in").touch()
    wait_idle(tab)
    tab.refresh()
    wait_idle(tab)
    assert tab.licence.text().startswith("Logged in as u***@example.com")
    assert "ABCD-EFGH" not in caplog.text and "user@example.com" not in caplog.text
