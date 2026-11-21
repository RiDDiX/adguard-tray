import shlex
import threading
import time
from types import SimpleNamespace

import pytest
from PyQt6 import sip
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from adguard_tray import cli, installer, preferences_tab
from adguard_tray.config import Config


class FakeCLI(cli.AdGuardCLI):
    def __init__(self) -> None:
        super().__init__("/opt/adguard-cli/adguard-cli")
        self.enabled = False
        self.reads = 0
        self.gate = threading.Event()
        self.gate.set()

    def service_enabled(self) -> bool:
        self.reads += 1
        self.gate.wait(5)
        return self.enabled


def wait_for(cond, timeout=5.0):
    deadline = time.monotonic() + timeout
    while not cond():
        assert time.monotonic() < deadline, "timed out"
        QTest.qWait(10)


def wait_idle(tab):
    wait_for(lambda: not tab._workers)


@pytest.fixture
def fake_cli():
    return FakeCLI()


@pytest.fixture
def make_tab(app, fake_cli, monkeypatch):
    monkeypatch.setattr(preferences_tab, "autostart_enabled", lambda: False)
    monkeypatch.setattr(preferences_tab, "set_autostart", lambda on, path: (True, ""))
    monkeypatch.setattr(preferences_tab.shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(preferences_tab, "POLL_MS", 20)
    tabs = []

    def make(idle=True):
        ctx = SimpleNamespace(cli=fake_cli, config=Config(), exec_path=["/usr/bin/adguard-tray"],
                              on_config_change=None)
        tab = preferences_tab.PreferencesTab(ctx)
        tabs.append(tab)
        if idle:
            wait_idle(tab)
        return tab

    yield make
    for tab in tabs:
        tab._boot_poll.stop()
        wait_idle(tab)
        sip.delete(tab)


@pytest.fixture
def opened(monkeypatch):
    commands = []
    monkeypatch.setattr(installer, "open_in_terminal", lambda command: commands.append(command) or True)
    return commands


@pytest.mark.parametrize("enabled", [True, False])
def test_switch_shows_the_service_state(make_tab, fake_cli, enabled):
    fake_cli.enabled = enabled
    tab = make_tab()
    assert tab.sw_boot.isChecked() is enabled
    assert not tab.boot_row.isHidden()


def test_turning_on_installs_in_a_terminal_and_polls(make_tab, fake_cli, opened):
    tab = make_tab()
    tab.sw_boot.setChecked(True)
    assert opened == [shlex.join(fake_cli.service_command(True))]
    assert opened == ["/opt/adguard-cli/adguard-cli install-service"]
    assert tab.banner.text.text() == "AdGuard CLI asks for your password in the terminal window."
    assert tab._boot_poll.isActive()
    assert not tab.sw_boot.isEnabled()
    reads = fake_cli.reads
    wait_for(lambda: fake_cli.reads >= reads + 3)
    assert tab._boot_poll.isActive() and tab.sw_boot.isChecked()
    fake_cli.enabled = True
    wait_for(lambda: not tab._boot_poll.isActive())
    wait_idle(tab)
    assert tab.sw_boot.isChecked() and tab.sw_boot.isEnabled()
    assert tab.banner.isHidden()


def test_a_poll_without_change_ends_at_the_deadline(make_tab, fake_cli, opened, monkeypatch):
    monkeypatch.setattr(preferences_tab, "POLL_FOR", 0.2)
    tab = make_tab()
    tab.sw_boot.setChecked(True)
    assert tab._boot_poll.isActive() and not tab.sw_boot.isEnabled()
    wait_for(lambda: not tab._boot_poll.isActive(), timeout=2)
    wait_idle(tab)
    assert not tab.sw_boot.isChecked() and tab.sw_boot.isEnabled()
    assert tab.banner.isHidden()


def test_poll_end_keeps_an_unrelated_banner(make_tab, fake_cli, opened):
    tab = make_tab()
    tab.sw_boot.setChecked(True)
    tab.banner.show_message("Could not change the autostart entry.", "danger")
    fake_cli.enabled = True
    wait_for(lambda: not tab._boot_poll.isActive(), timeout=2)
    wait_idle(tab)
    assert not tab.banner.isHidden()
    assert tab.banner.text.text() == "Could not change the autostart entry."


def test_switch_disabled_while_on_shown_reads(make_tab, fake_cli, opened):
    tab = make_tab()
    assert tab.sw_boot.isEnabled() and not tab.sw_boot.isChecked()
    fake_cli.enabled = True         # changed outside the app
    fake_cli.gate.clear()
    tab.on_shown()
    assert not tab.sw_boot.isEnabled()
    # A click before the read returns would race it with a terminal for the stale state.
    QTest.mouseClick(tab.boot_row, Qt.MouseButton.LeftButton)
    QTest.mouseClick(tab.sw_boot, Qt.MouseButton.LeftButton)
    QTest.keyClick(tab.sw_boot, Qt.Key.Key_Space)
    assert opened == []
    fake_cli.gate.set()
    wait_idle(tab)
    assert tab.sw_boot.isEnabled() and tab.sw_boot.isChecked()
    assert opened == [] and not tab._boot_poll.isActive()


def test_switch_disabled_until_the_first_read(make_tab, fake_cli):
    fake_cli.gate.clear()
    fake_cli.enabled = True
    tab = make_tab(idle=False)
    assert not tab.sw_boot.isEnabled() and not tab.sw_boot.isChecked()
    fake_cli.gate.set()
    wait_idle(tab)
    assert tab.sw_boot.isEnabled() and tab.sw_boot.isChecked()


def test_on_shown_does_not_flip_the_switch_mid_install(make_tab, fake_cli, opened):
    tab = make_tab()
    tab.sw_boot.setChecked(True)
    tab._boot_poll.stop()           # freeze the poll as running
    tab._boot_poll.start(60_000)
    reads = fake_cli.reads
    tab.on_shown()
    wait_idle(tab)
    assert fake_cli.reads == reads
    assert tab.sw_boot.isChecked()


def test_turning_off_uninstalls(make_tab, fake_cli, opened):
    fake_cli.enabled = True
    tab = make_tab()
    tab.sw_boot.setChecked(False)
    assert opened == [shlex.join(fake_cli.service_command(False))]
    assert opened[0].endswith("install-service --uninstall")
    fake_cli.enabled = False
    wait_for(lambda: not tab._boot_poll.isActive())
    wait_idle(tab)
    assert not tab.sw_boot.isChecked()


def test_no_terminal_puts_the_command_on_the_clipboard(make_tab, fake_cli, monkeypatch):
    monkeypatch.setattr(installer, "open_in_terminal", lambda command: False)
    tab = make_tab()
    tab.sw_boot.setChecked(True)
    command = shlex.join(fake_cli.service_command(True))
    assert QApplication.clipboard().text() == command
    assert tab.banner.text.text() == \
        "No terminal app was found. The command is on the clipboard: paste it into a terminal."
    assert not tab.sw_boot.isChecked() and tab.sw_boot.isEnabled()
    assert not tab._boot_poll.isActive()


def test_row_hidden_without_systemctl(make_tab, fake_cli, monkeypatch):
    monkeypatch.setattr(preferences_tab.shutil, "which", lambda name: None)
    tab = make_tab()
    assert tab.boot_row.isHidden()
    tab.on_shown()
    wait_idle(tab)
    assert fake_cli.reads == 0
