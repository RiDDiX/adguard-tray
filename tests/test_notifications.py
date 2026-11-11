from adguard_tray import notifications


class FakeProc:
    returncode = 0

    def communicate(self, timeout=None):
        return b"", b""


def test_body_starting_with_dash_is_not_an_option(monkeypatch):
    calls = []

    def popen(argv, **kwargs):
        calls.append((argv, kwargs))
        return FakeProc()

    monkeypatch.setattr(notifications.subprocess, "Popen", popen)

    notifications.notify("Title", "--help is not an option", replace_tag="t")

    argv, kwargs = calls[0]
    assert argv[-3:] == ["--", "Title", "--help is not an option"]
    assert kwargs["stdin"] is notifications.subprocess.DEVNULL
