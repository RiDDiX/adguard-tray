import time
from types import SimpleNamespace

import pytest
from PyQt6 import sip
from PyQt6.QtTest import QTest

from adguard_tray import cli, overview_tab, proxy_settings
from adguard_tray.proxy_settings import ProxySettings


class FakeCLI(cli.AdGuardCLI):
    def __init__(self, result) -> None:
        super().__init__("/opt/adguard-cli/adguard-cli")
        self.result = result

    def get_status(self):
        return cli.StatusResult(cli.AdGuardStatus.ACTIVE)

    def get_filters(self, all_available=False):
        return cli.FilterListResult()

    get_dns_filters = get_filters

    def get_userscripts(self):
        return cli.UserscriptListResult()

    def get_license(self):
        return False, ""

    def restart(self):
        return self.result


def wait_idle(tab):
    deadline = time.monotonic() + 5
    while tab._workers:
        assert time.monotonic() < deadline, "timed out"
        QTest.qWait(10)


@pytest.mark.parametrize("result, kind", [
    ((True, "x"), "success"),
    ((False, "Authentication cancelled"), "info"),
    ((False, "Another action is still running"), "info"),
    ((False, "socket busy"), "danger"),
])
def test_action_result_picks_the_banner_kind(app, tmp_path, monkeypatch, result, kind):
    yaml = tmp_path / "proxy.yaml"
    yaml.write_text("proxy_mode: auto\napps: []\n")
    monkeypatch.setattr(proxy_settings, "PROXY_YAML", yaml)
    monkeypatch.setattr(overview_tab, "_exception_count", lambda: 0)
    monkeypatch.setattr(overview_tab, "_blocked_24h", lambda: (0, 0, ""))
    ctx = SimpleNamespace(cli=FakeCLI(result), settings=ProxySettings(), on_status_change=None,
                          navigate=lambda page: None)
    tab = overview_tab.OverviewTab(ctx)
    tab.on_shown()
    wait_idle(tab)
    shown = []
    monkeypatch.setattr(tab.banner, "show_message",
                        lambda text, tone="info", **kw: shown.append((text, tone)))
    tab.btn_restart.click()
    wait_idle(tab)
    assert [tone for _, tone in shown] == [kind]
    sip.delete(tab)
