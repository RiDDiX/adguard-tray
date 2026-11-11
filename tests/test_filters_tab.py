import threading
import time
from types import SimpleNamespace

import pytest
from PyQt6.QtTest import QTest

from adguard_tray import filters_tab, ui
from adguard_tray.cli import FilterListResult


class FakeCli:
    def __init__(self):
        noop = lambda *a, **k: (True, "")  # noqa: E731
        self.enable_filter = self.disable_filter = self.add_filter = noop
        self.remove_filter = self.set_filter_title = noop
        self.gate = None
        self.list_error = ""

    def get_filters(self, all_available=False):
        if self.gate:
            self.gate.wait(5)
        return FilterListResult(error=self.list_error)

    def update_filters(self):
        return False, "update boom"


@pytest.fixture
def lst(app):
    page = ui.Page()
    lst = filters_tab.FilterList(page, SimpleNamespace(cli=FakeCli(), restart_adguard=lambda: ""))
    yield lst
    wait_idle(lst)
    page.deleteLater()


def wait_idle(lst, timeout=5.0):
    deadline = time.monotonic() + timeout
    while lst._busy or lst._workers:
        assert time.monotonic() < deadline, "list still busy"
        QTest.qWait(10)


def fail(*args):
    return False, "act boom"


def test_failing_reload_keeps_update_error(lst):
    lst.ctx.cli.list_error = "list boom"
    lst._run_update()
    wait_idle(lst)
    assert lst.banner.text.text() == filters_tab._t("Update failed.")
    details = lst.banner.details.toPlainText()
    assert "update boom" in details and "list boom" in details


def test_action_failing_during_load_keeps_its_error(lst):
    cli = lst.ctx.cli
    cli.gate = threading.Event()
    lst.load()
    lst._act(fail, done="", error="Act failed")
    deadline = time.monotonic() + 5
    while lst._acting:
        assert time.monotonic() < deadline
        QTest.qWait(10)
    cli.list_error = "list boom"
    cli.gate.set()
    wait_idle(lst)
    assert lst.banner.text.text() == "Act failed"
    details = lst.banner.details.toPlainText()
    assert "act boom" in details and "list boom" in details
    assert lst._failed is None


def test_action_error_is_not_kept_without_a_load(lst):
    lst._act(fail, done="", error="Act failed")
    wait_idle(lst)
    assert lst.banner.text.text() == "Act failed"
    lst.ctx.cli.list_error = "list boom"
    lst.load()
    wait_idle(lst)
    assert lst.banner.text.text() == lst.txt["load_error"]
