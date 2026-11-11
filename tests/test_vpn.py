import pytest

from adguard_tray import vpn

LOGGED_OUT = "You are not logged in\nYou can log in by running `adguardvpn-cli login`"


@pytest.fixture
def run(monkeypatch):
    calls = []

    def fake(result):
        monkeypatch.setattr(vpn, "_run", lambda args, timeout=15: (calls.append(args), result)[1])
        return calls
    return fake


def test_status_logged_out(run):
    calls = run((11, LOGGED_OUT, ""))
    assert vpn.status("/x/adguardvpn-cli") == vpn.VpnStatus(False, "You are not logged in", "")
    assert calls == [["/x/adguardvpn-cli", "status"]]


def test_status_logged_in_drops_hint_lines(run):
    run((0, "Connected to FRANKFURT in TUN mode\n  Line two  \n"
            "You can disconnect by running `adguardvpn-cli disconnect`", ""))
    status = vpn.status("adguardvpn-cli")
    assert status.logged_in and not status.error
    assert status.text == "Connected to FRANKFURT in TUN mode\n  Line two"


def test_status_drops_hint_with_the_path_the_cli_was_started_as(run):
    run((11, "You are not logged in\nYou can log in by running `/usr/local/sbin/adguardvpn-cli login`", ""))
    assert vpn.status("/usr/local/sbin/adguardvpn-cli").text == "You are not logged in"


def test_status_binary_missing():
    status = vpn.status("/nonexistent/adguardvpn-cli")
    assert not status.logged_in
    assert "/nonexistent/adguardvpn-cli" in status.error


def test_status_failure_without_output_has_a_message(run):
    run((3, "", ""))
    status = vpn.status("adguardvpn-cli")
    assert not status.logged_in and status.error


@pytest.mark.parametrize("code, out", [(0, "Logged out"), (11, "You are not logged in")])
def test_logout_success(run, code, out):
    calls = run((code, out, ""))
    assert vpn.logout("adguardvpn-cli") == (True, "")
    assert calls == [["adguardvpn-cli", "logout"]]


def test_logout_failure(run):
    run((1, "Something broke\nYou can retry by running `adguardvpn-cli logout`", ""))
    assert vpn.logout("adguardvpn-cli") == (False, "Something broke")


def test_login_link():
    out = ("You need to authorize in your browser. The following link will be available for 1799 seconds: "
           "\x1b[1mhttps://auth.adguard.io/device_code?user_code=ABCD-EFGH\x1b[0m\nb - Open link in browser\n")
    assert vpn.login_link(out) == "https://auth.adguard.io/device_code?user_code=ABCD-EFGH"
    assert vpn.login_link("b - Open link in browser\nx - Cancel") is None
    assert vpn.login_link("link: http://auth.adguard.io/device_code?user_code=ABCD-EFGH") is None
    assert vpn.login_link("link: https://auth.adguard.io/device_code?user_co") is None, "not complete yet"
    assert vpn.login_link("link: https://auth.adguard.io/x\n") == "https://auth.adguard.io/x"


UPSELL = ("You are using a FREE version. Upgrade at https://agrd.io/vpn_cli "
          "to get more locations and higher speeds")
LOG_LINE = "Log is being written to: /home/u/.local/share/adguardvpn-cli/app.log"
LOCATIONS = """ISO   COUNTRY              CITY                           PING ESTIMATE
DE    Germany              Frankfurt                      25
GB    United Kingdom       London                         70
US    United States        New York                       139
US    United States        Miami
\nYou can connect to a location by running `adguardvpn-cli connect -l <city>`
"""


def test_status_drops_log_and_upsell_lines(run):
    run((0, f"{LOG_LINE}\nConnected to FRANKFURT in SOCKS mode, listening on 127.0.0.1:1080\n{UPSELL}", ""))
    assert vpn.status("adguardvpn-cli").text == "Connected to FRANKFURT in SOCKS mode, listening on 127.0.0.1:1080"


def test_locations(run):
    calls = run((0, LOCATIONS, ""))
    assert vpn.locations("cli") == ([
        vpn.Location("DE", "Germany", "Frankfurt", "25"),
        vpn.Location("GB", "United Kingdom", "London", "70"),
        vpn.Location("US", "United States", "New York", "139"),
        vpn.Location("US", "United States", "Miami", ""),
    ], "")
    assert calls == [["cli", "list-locations"]]


def test_locations_failure(run):
    run((11, "You are not logged in", ""))
    assert vpn.locations("cli") == ([], "You are not logged in")


def test_license_info(run):
    calls = run((0, "Logged in as a@b.c\nYou are using the FREE version\nUp to 2 devices simultaneously\n"
                    f"You have 3.00 GB left for this month\n{UPSELL}\n", ""))
    assert vpn.license_info("cli") == ("Logged in as a***@b.c\nYou are using the FREE version\n"
                                       "Up to 2 devices simultaneously\nYou have 3.00 GB left for this month", "")
    assert calls == [["cli", "license"]]


@pytest.mark.parametrize("location, argv", [(None, ["cli", "connect", "-f"]), ("", ["cli", "connect", "-f"]),
                                            ("New York", ["cli", "connect", "-l", "New York"])])
def test_connect(run, location, argv):
    calls = run((0, f"{LOG_LINE}\nSuccessfully Connected to FRANKFURT\n{UPSELL}", ""))
    assert vpn.connect_command("cli", location) == argv
    assert vpn.connect("cli", location) == (True, "Successfully Connected to FRANKFURT")
    assert calls == [argv]


def test_connect_unknown_location(run):
    run((13, f"{LOG_LINE}\nFailed to start the VPN service in the background: There is no location with the "
             "specified city name, country name, or ISO code. To see the available options, please run "
             "`list-locations`\n", ""))
    ok, message = vpn.connect("cli", "Atlantis")
    assert not ok
    assert message.startswith("Failed to start the VPN service") and "Log is being" not in message


@pytest.mark.parametrize("code, ok", [(0, True), (14, True), (1, False)])
def test_disconnect(run, code, ok):
    calls = run((code, "VPN stopped" if code == 0 else "Failed to disconnect. Process is not running", ""))
    assert vpn.disconnect("cli")[0] is ok
    assert calls == [["cli", "disconnect"]]


def test_set_mode(monkeypatch):
    calls = []
    outputs = iter([(0, "Config has been updated\n\tMode: tun\n", ""), (0, "\tMode: tun\n\tSOCKS port: 1080\n", "")])
    monkeypatch.setattr(vpn, "_run", lambda args, timeout=15: (calls.append(args), next(outputs))[1])
    config, error = vpn.set_mode("cli", "tun")
    assert config.mode == "tun" and not error
    assert calls == [["cli", "config", "set-mode", "tun"], ["cli", "config", "show"]]


def test_set_mode_failure(run):
    run((1, "", "no permission"))
    assert vpn.set_mode("cli", "socks") == (None, "no permission")


class FakeSettings:
    available = True

    def __init__(self, values=None):
        self.values = values or {}

    def value(self, key, default=None):
        return self.values.get(key, default)

    def set(self, key, value, default=None):
        self.values[key] = value


def test_route_through_and_back():
    s = FakeSettings({("apps",): [{"name": "firefox", "action": "filter"}]})
    config = vpn.VpnConfig("socks", "127.0.0.1", 1080)
    assert not vpn.routed(s, config)
    vpn.route_through(s, config, "/x/adguardvpn-cli")
    assert s.values[("outbound_proxy", "enabled")] is True
    assert s.values[("outbound_proxy", "mode")] == "SOCKS5"
    assert (s.values[("outbound_proxy", "host")], s.values[("outbound_proxy", "port")]) == ("127.0.0.1", 1080)
    assert s.values[("apps",)][0] == vpn.VPN_RULE and len(s.values[("apps",)]) == 2
    assert vpn.routed(s, config)
    assert not vpn.routed(s, vpn.VpnConfig("tun"))
    assert not vpn.routed(s, vpn.VpnConfig("socks", "127.0.0.1", 1090))
    vpn.route_through(s, config, "/x/adguardvpn-cli")
    assert len(s.values[("apps",)]) == 2, "the rule is added once"
    vpn.stop_routing(s)
    assert s.values[("outbound_proxy", "enabled")] is False
    assert s.values[("outbound_proxy", "port")] == 1080
    assert not vpn.routed(s, config)


def test_loops():
    s = FakeSettings()
    assert vpn.loops(s, vpn.VpnConfig("tun"))
    assert not vpn.loops(s, vpn.VpnConfig("socks"))
    assert not vpn.loops(s, None)
    assert not vpn.loops(FakeSettings({("proxy_mode",): "manual"}), vpn.VpnConfig("tun"))


def test_status_unavailable_is_logged_in(run):
    run((10, "VPN active, but status unavailable", ""))
    assert vpn.status("cli") == vpn.VpnStatus(True, "VPN active, but status unavailable", "")


def test_connection_predicates():
    assert vpn.is_disconnected("VPN is disconnected")
    assert vpn.is_disconnected("Something first\nVPN is disconnected")
    assert vpn.is_connected("Line\nConnected to PARIS in TUN mode, running on tun0")
    for text in ("VPN active, but status unavailable", "", "Disconnected to PARIS"):
        assert not vpn.is_connected(text) and not vpn.is_disconnected(text)


def test_switching_location_drops_the_disconnecting_line(run):
    run((0, f"Disconnecting from current location to connect elsewhere...\n{LOG_LINE}\n"
            f"Successfully Connected to PARIS\n{UPSELL}", ""))
    assert vpn.connect("cli", "Paris") == (True, "Successfully Connected to PARIS")


def test_failed_switch_starts_with_the_reason(run):
    run((13, f"Disconnecting from current location to connect elsewhere...\n{LOG_LINE}\n"
             "Failed to start the VPN service in the background: There is no location", ""))
    assert vpn.connect("cli", "Atlantis") == (
        False, "Failed to start the VPN service in the background: There is no location")


def test_licence_failure_keeps_the_text_and_masks_the_e_mail(run):
    run((12, f"{LOG_LINE}\nLogged in as max.mustermann@example.com\nFailed to get license information", ""))
    assert vpn.license_info("cli") == (
        "Logged in as m***@example.com\nFailed to get license information", "")


def test_licence_failure_without_text(run):
    run((12, LOG_LINE, ""))
    assert vpn.license_info("cli") == ("", "adguardvpn-cli failed with exit code 12")


def test_set_mode_error_has_no_headline(run):
    run((13, f"{LOG_LINE}\nConfig has been updated\nFailed to start the VPN service in the background: x", ""))
    assert vpn.set_mode("cli", "tun") == (None, "Failed to start the VPN service in the background: x")


def test_read_config_error_has_no_log_line(run):
    run((1, f"{LOG_LINE}\nCannot read the config", ""))
    assert vpn.read_config("cli") == (None, "Cannot read the config")


def cli(monkeypatch, connected: bool, disconnect=(0, "VPN stopped", "")):
    calls = []
    answers = {
        ("status",): (0, "Connected to PARIS in TUN mode" if connected else "VPN is disconnected", ""),
        ("disconnect",): disconnect,
        ("config", "set-mode", "socks"): (0, "Config has been updated", ""),
        ("config", "show"): (0, "\tMode: socks\n\tSOCKS port: 1080\n\tSOCKS host: 127.0.0.1", ""),
    }

    def fake(args, timeout=15):
        calls.append(args[1:])
        return answers[tuple(args[1:])]
    monkeypatch.setattr(vpn, "_run", fake)
    return calls


def test_change_mode_disconnects_first(monkeypatch):
    calls = cli(monkeypatch, connected=True)
    assert vpn.change_mode("cli", "socks") == (vpn.VpnConfig("socks", "127.0.0.1", 1080), "", True)
    assert calls == [["status"], ["disconnect"], ["config", "set-mode", "socks"], ["config", "show"]]


def test_change_mode_while_disconnected(monkeypatch):
    calls = cli(monkeypatch, connected=False)
    assert vpn.change_mode("cli", "socks") == (vpn.VpnConfig("socks", "127.0.0.1", 1080), "", False)
    assert calls == [["status"], ["config", "set-mode", "socks"], ["config", "show"]]


def test_change_mode_keeps_the_mode_when_disconnect_fails(monkeypatch):
    calls = cli(monkeypatch, connected=True, disconnect=(1, "", "no"))
    assert vpn.change_mode("cli", "socks") == (None, "no", False)
    assert calls == [["status"], ["disconnect"]]
