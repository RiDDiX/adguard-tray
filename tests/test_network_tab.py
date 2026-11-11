import time
from types import SimpleNamespace

from PyQt6 import sip
from PyQt6.QtTest import QTest

from adguard_tray import network_tab, proxy_settings, vpn
from adguard_tray.proxy_settings import ProxySettings


def test_vpn_switch_points_the_outbound_proxy_at_the_vpn(app, tmp_path, monkeypatch):
    yaml = tmp_path / "proxy.yaml"
    yaml.write_text("proxy_mode: auto\napps: []\n")
    monkeypatch.setattr(proxy_settings, "PROXY_YAML", yaml)
    settings = ProxySettings()
    tab = network_tab.NetworkTab(SimpleNamespace(settings=settings))
    tab._vpn_checked("/x/adguardvpn-cli", vpn.VpnConfig("tun"), "")
    assert not tab.vpn_conflict.isHidden()
    tab._vpn_switched("/x/adguardvpn-cli", vpn.VpnConfig("socks", "127.0.0.1", 1080), "")
    assert vpn.routed(settings, vpn.VpnConfig("socks", "127.0.0.1", 1080))
    assert settings.value(("apps",)) == [vpn.VPN_RULE]
    assert tab.vpn_conflict.isHidden()
    assert tab.banner.text.text().startswith("AdGuard VPN now uses SOCKS5 mode.")
    sip.delete(tab)


def test_vpn_switch_disconnects_a_connected_vpn_first(app, tmp_path, monkeypatch):
    yaml = tmp_path / "proxy.yaml"
    yaml.write_text("proxy_mode: auto\napps: []\n")
    monkeypatch.setattr(proxy_settings, "PROXY_YAML", yaml)
    calls = []
    answers = {
        ("status",): (0, "Connected to PARIS in TUN mode, running on tun0", ""),
        ("disconnect",): (0, "VPN stopped", ""),
        ("config", "set-mode", "socks"): (0, "Config has been updated", ""),
        ("config", "show"): (0, "\tMode: socks\n\tSOCKS port: 1080\n\tSOCKS host: 127.0.0.1", ""),
    }

    def fake(args, timeout=15):
        calls.append(args[1:])
        return answers[tuple(args[1:])]
    monkeypatch.setattr(vpn, "_run", fake)
    monkeypatch.setattr(vpn, "find", lambda: "/x/adguardvpn-cli")
    settings = ProxySettings()
    tab = network_tab.NetworkTab(SimpleNamespace(settings=settings))
    tab._check_vpn(True)
    deadline = time.monotonic() + 5
    while tab._busy or tab._workers:
        assert time.monotonic() < deadline, "timed out"
        QTest.qWait(10)
    assert calls == [["status"], ["disconnect"], ["config", "set-mode", "socks"], ["config", "show"]]
    assert vpn.routed(settings, vpn.VpnConfig("socks", "127.0.0.1", 1080))
    sip.delete(tab)
