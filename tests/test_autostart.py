import pytest

from adguard_tray import autostart

ENTRY = "[Desktop Entry]\nType=Application\nExec=adguard-tray\n"


@pytest.fixture
def entry(tmp_path, monkeypatch):
    monkeypatch.setattr(autostart, "AUTOSTART_DIR", tmp_path / "autostart")
    monkeypatch.setattr(autostart, "AUTOSTART_FILE", tmp_path / "autostart" / "adguard-tray.desktop")
    return autostart.AUTOSTART_FILE


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_set_autostart_round_trip(entry):
    assert autostart.set_autostart(True, ["/usr/bin/adguard-tray"]) == (True, "")
    assert autostart.autostart_enabled()
    assert autostart.set_autostart(False, ["/usr/bin/adguard-tray"]) == (True, "")
    assert not entry.exists()
    assert not autostart.autostart_enabled()


@pytest.mark.parametrize("text, expected", [
    ("", False),
    ("[Desktop Entry]\nType=Applic", False),        # truncated
    (ENTRY, True),
    (ENTRY + "Hidden=true\n", False),
    (ENTRY + "Hidden = true\n", False),
    (ENTRY + "hidden=True\n", False),
    ("# Hidden=true\n" + ENTRY, True),
    (ENTRY + "Hidden=false\n", True),
    (ENTRY + "X-GNOME-Autostart-enabled=false\n", False),
    (ENTRY + "X-GNOME-Autostart-enabled=true\n", True),
    ("[Desktop Entry]\nType=Application\n[Desktop Action quit]\nExec=adguard-tray --quit\n", False),
    ("[Desktop Entry]\nType=Application\nExec=\n", False),
    (ENTRY + "[Desktop Action quit]\nExec=adguard-tray --quit\nHidden=true\n", True),
    ("\ufeff" + ENTRY.replace("\n", "\r\n"), True),
])
def test_autostart_enabled_reads_the_entry(entry, text, expected):
    write(entry, text)
    assert autostart.autostart_enabled() is expected


def test_autostart_enabled_without_a_file(entry):
    assert not autostart.autostart_enabled()


def tryexec(text):
    return next(line for line in text.splitlines() if line.startswith("TryExec="))


@pytest.mark.parametrize("interpreter", ["/usr/bin/python3.12", "/usr/bin/python3", "python"])
def test_tryexec_points_at_the_script(interpreter):
    assert tryexec(autostart.desktop_entry([interpreter, "/opt/x/adguard-tray.py"])) == \
        "TryExec=/opt/x/adguard-tray.py"


def test_tryexec_keeps_a_plain_binary():
    text = autostart.desktop_entry(["/usr/bin/adguard-tray", "--hidden"])
    assert tryexec(text) == "TryExec=/usr/bin/adguard-tray"


def test_exec_quotes_a_path_with_a_space():
    text = autostart.desktop_entry(["/usr/bin/python3", "/opt/my apps/adguard-tray.py"])
    assert 'Exec=/usr/bin/python3 "/opt/my apps/adguard-tray.py"' in text.splitlines()
    assert tryexec(text) == "TryExec=/opt/my apps/adguard-tray.py"
