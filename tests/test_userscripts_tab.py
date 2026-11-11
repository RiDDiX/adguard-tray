import threading
import time
from types import SimpleNamespace

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QDialog

from adguard_tray import userscripts_tab
from adguard_tray.cli import UserscriptEntry, UserscriptListResult


class FakeCli:
    def __init__(self):
        self.loads = 0
        self.running = 0
        self.max_running = 0
        self.gate = None
        self.list_error = ""
        self.toggles = 0
        self.ok = False

    def get_userscripts(self):
        self.loads += 1
        self.running += 1
        self.max_running = max(self.max_running, self.running)
        if self.gate:
            self.gate.wait(5)
        self.running -= 1
        if self.list_error:
            return UserscriptListResult(error=self.list_error)
        return UserscriptListResult(scripts=[UserscriptEntry("s1", "Script One", True, "")])

    def disable_userscript(self, name):
        self.toggles += 1
        return self.ok, "toggle boom"

    def install_userscript(self, url):
        return self.ok, "install boom"

    def remove_userscript(self, name):
        return self.ok, "remove boom"


@pytest.fixture
def tab(app):
    cli = FakeCli()
    tab = userscripts_tab.UserscriptsTab(SimpleNamespace(cli=cli, navigate=None, restart_adguard=lambda: ""))
    tab.refresh()
    wait_idle(tab)
    assert cli.loads == 1
    yield tab
    tab.deleteLater()


def wait_idle(tab, timeout=5.0):
    deadline = time.monotonic() + timeout
    while tab._busy or tab._workers:
        assert time.monotonic() < deadline, "tab still busy"
        QTest.qWait(10)


class Dialog:
    on_exec = None
    def __init__(self, parent=None): pass
    def exec(self):
        if Dialog.on_exec:
            Dialog.on_exec()
        return QDialog.DialogCode.Accepted
    def url(self): return "https://example.com/a.user.js"
    def deleteLater(self): pass


@pytest.fixture
def dialog(monkeypatch):
    monkeypatch.setattr(userscripts_tab, "_UrlDialog", Dialog)
    yield Dialog
    Dialog.on_exec = None


def test_failed_install_reloads_once_and_keeps_error(tab, dialog):
    tab._install()
    wait_idle(tab)
    assert tab.cli.loads == 2
    assert "install boom" in tab.banner.text.text()
    assert tab.btn_add.isEnabled()


def test_failed_remove_reloads(tab, monkeypatch):
    monkeypatch.setattr(userscripts_tab.ui, "confirm", lambda *args: True)
    tab._remove("s1")
    wait_idle(tab)
    assert tab.cli.loads == 2
    assert "remove boom" in tab.banner.text.text()


def test_install_failing_during_load_never_overlaps_loads(tab, dialog):
    tab.cli.gate = threading.Event()
    dialog.on_exec = tab.refresh        # the tray asks for a reload while the dialog is open
    tab._install()
    deadline = time.monotonic() + 5
    while tab._acting:
        assert time.monotonic() < deadline
        QTest.qWait(10)
    tab.cli.gate.set()
    wait_idle(tab)
    assert tab.cli.max_running == 1
    assert tab.cli.loads == 3
    assert "install boom" in tab.banner.text.text()


def test_failing_reload_keeps_install_error(tab, dialog):
    tab.cli.list_error = "list boom"
    tab._install()
    wait_idle(tab)
    assert tab.cli.loads == 2
    assert "install boom" in tab.banner.text.text()
    details = tab.banner.details.toPlainText()
    assert "install boom" in details and "list boom" in details
    tab.cli.list_error = "later boom"
    tab.refresh()
    wait_idle(tab)
    assert tab.banner.text.text() == userscripts_tab._t("Could not retrieve userscript list")


def test_failed_toggle_reverts_and_reloads_once(tab):
    tab.tree.topLevelItem(0).setCheckState(0, Qt.CheckState.Unchecked)
    wait_idle(tab)
    assert tab.tree.topLevelItem(0).checkState(0) == Qt.CheckState.Checked
    assert tab.cli.loads == 2
    assert "toggle boom" in tab.banner.text.text()
    tab.tree.topLevelItem(0).setCheckState(0, Qt.CheckState.Unchecked)
    wait_idle(tab)
    assert tab.cli.toggles == 2


def wait_acted(tab, timeout=5.0):
    deadline = time.monotonic() + timeout
    while tab._acting:
        assert time.monotonic() < deadline, "change still running"
        QTest.qWait(10)


def count_refresh(tab, monkeypatch):
    calls = []
    real = tab.refresh
    monkeypatch.setattr(tab, "refresh", lambda: (calls.append(1), real())[1])
    return calls


def test_toggle_reloads_once_through_refresh(tab, monkeypatch):
    tab.cli.ok = True
    calls = count_refresh(tab, monkeypatch)
    tab.tree.topLevelItem(0).setCheckState(0, Qt.CheckState.Unchecked)
    wait_idle(tab)
    assert calls == [1]
    assert tab.cli.loads == 2
    assert tab.cli.max_running == 1


def test_install_during_load_reloads_once_without_overlap(tab, dialog):
    tab.cli.ok = True
    tab.cli.gate = threading.Event()
    dialog.on_exec = tab.refresh        # the tray asks for a reload while the dialog is open
    tab._install()
    wait_acted(tab)
    tab.cli.gate.set()
    wait_idle(tab)
    assert tab.cli.max_running == 1
    assert tab.cli.loads == 3
    assert "Userscript installed." in tab.banner.text.text()


def test_reload_queued_during_load_waits_for_install(tab, dialog, monkeypatch):
    tab.cli.ok = True
    tab.cli.gate = threading.Event()
    installed = threading.Event()
    monkeypatch.setattr(tab.cli, "install_userscript", lambda url: (installed.wait(5), (True, ""))[1])
    dialog.on_exec = lambda: (tab.refresh(), tab.refresh())     # the tray asks twice while the dialog is open
    tab._install()
    tab.cli.gate.set()
    deadline = time.monotonic() + 5
    while len(tab._workers) > 1:        # until only the install still runs
        assert time.monotonic() < deadline
        QTest.qWait(10)
    QTest.qWait(50)
    assert tab.cli.loads == 2
    installed.set()
    wait_idle(tab)
    assert tab.cli.loads == 3
    assert tab.cli.max_running == 1


def test_remove_during_load_reloads_once_without_overlap(tab, monkeypatch):
    tab.cli.ok = True
    tab.cli.gate = threading.Event()
    monkeypatch.setattr(userscripts_tab.ui, "confirm", lambda *args: (tab.refresh(), True)[1])
    tab._remove("s1")
    wait_acted(tab)
    tab.cli.gate.set()
    wait_idle(tab)
    assert tab.cli.max_running == 1
    assert tab.cli.loads == 3
    assert "removed." in tab.banner.text.text()
