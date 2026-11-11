import contextlib
import logging
import os
import subprocess
import time

import pytest

from adguard_tray import cli

URL = "https://github.com/redphx/better-xcloud/releases/latest/download/better-xcloud.user.js"


@pytest.fixture
def fake_run(monkeypatch):
    calls = []
    result = [(0, "", "")]

    def run(args, timeout=15, stdin_data=None):
        calls.append(args)
        return result[0]

    monkeypatch.setattr(cli, "_run", run)
    # No redirect probe: these tests never reach the network.
    monkeypatch.setattr(cli, "_userscript_source", contextlib.nullcontext)
    return calls, result


def test_install_failure_keeps_cli_error_and_url(fake_run):
    calls, result = fake_run
    result[0] = (1, "", "Error: Failed to install userscript")
    ok, msg = cli.AdGuardCLI().install_userscript(URL)
    assert not ok
    assert msg == "Failed to install userscript"
    assert calls[0][-3:] == ["userscripts", "install", URL]


def test_install_failure_text_with_exit_zero(fake_run):
    _, result = fake_run
    result[0] = (0, "Error: Failed to install userscript", "")
    ok, _ = cli.AdGuardCLI().install_userscript(URL)
    assert not ok


def test_install_failure_shows_stderr_and_stdout(fake_run):
    _, result = fake_run
    result[0] = (1, "Download returned HTTP 404", "Error: Failed to install userscript")
    ok, msg = cli.AdGuardCLI().install_userscript(URL)
    assert not ok
    assert msg.splitlines() == ["Failed to install userscript", "Download returned HTTP 404"]


def test_install_failure_lists_each_line_once(fake_run):
    _, result = fake_run
    result[0] = (1, "Error: Failed to install userscript\nDownload returned HTTP 404",
                 "Error: Failed to install userscript")
    ok, msg = cli.AdGuardCLI().install_userscript(URL)
    assert not ok
    assert msg.splitlines() == ["Failed to install userscript", "Download returned HTTP 404"]


def test_simple_strips_cli_error_prefix_once(fake_run):
    _, result = fake_run
    result[0] = (1, "  \nError: Error: nested\n  Error  \nreason on stdout", "Error:   Failed\n   \nERROR:")
    ok, msg = cli.AdGuardCLI()._simple(["x"], "ok", "fallback")
    assert not ok
    assert msg.splitlines() == ["Failed", "Error: nested", "reason on stdout"]


def test_simple_falls_back_when_only_error_noise(fake_run):
    _, result = fake_run
    result[0] = (1, "  \nError", "Error:\n\t")
    assert cli.AdGuardCLI()._simple(["x"], "ok", "fallback") == (False, "fallback")


@pytest.mark.parametrize("method", ["install_userscript", "install_dns_filter", "install_filter_ext"])
def test_install_failure_keeps_credentials_out_of_log(fake_run, caplog, method):
    calls, result = fake_run
    url = "https://user:pw@host.example:8443/x.js?token=abc#frag"
    echoed = "https://user:SECRET@host.example/a.user.js?token=abc"
    result[0] = (0, f"failed to download {echoed}: 403", "Error: Failed to install userscript")
    with caplog.at_level(logging.ERROR, logger="adguard_tray.cli"):
        ok, msg = getattr(cli.AdGuardCLI(), method)(url)
    assert not ok
    assert f"failed to download {echoed}: 403" in msg
    assert url in calls[0]
    assert f"{method}(https://host.example:8443/x.js)" in caplog.text
    assert "failed to download https://host.example/a.user.js: 403" in caplog.text
    for secret in ("user:", "pw@", "SECRET", "token", "abc", "frag"):
        assert secret not in caplog.text


def test_log_text_punctuation_run_is_linear():
    text = "http://a" + ".," * 99995 + "x/"
    start = time.monotonic()
    assert cli._log_text(text) == text
    assert time.monotonic() - start < 0.5


def test_unparsable_url_is_logged_as_placeholder(fake_run, caplog):
    _, result = fake_run
    result[0] = (1, "", "Error: bad URL")
    assert cli._log_url("http://u:p@[x") == "<unparsable URL>"
    with caplog.at_level(logging.ERROR, logger="adguard_tray.cli"):
        assert cli.AdGuardCLI().install_userscript("http://[x") == (False, "bad URL")
    assert "install_userscript(<unparsable URL>)" in caplog.text


def test_remove_userscript_ambiguous_name_is_failure(fake_run):
    _, result = fake_run
    result[0] = (0, "Multiple userscripts match 'a'. Please specify more precisely:\n  adguard-extra\n  abc", "")
    ok, msg = cli.AdGuardCLI().remove_userscript("a")
    assert not ok
    assert msg.startswith("Multiple userscripts match 'a'.")


def test_simple_signal_exit_names_crash(fake_run):
    _, result = fake_run
    result[0] = (-11, "Checking filters updates...", "")
    assert cli.AdGuardCLI().update_filters() == (
        False, cli._t("Update failed") + "\nadguard-cli crashed (SIGSEGV)\nChecking filters updates...")


@pytest.mark.parametrize("code, err", [
    (-1, "Binary not found: adguard-cli"), (-2, "Command timed out after 120s"), (-3, "Permission denied"),
])
def test_simple_run_sentinels_keep_their_message(fake_run, code, err):
    _, result = fake_run
    result[0] = (code, "", err)
    assert cli.AdGuardCLI().update_filters() == (False, err)


@pytest.mark.parametrize("result", [(-6, "", "Error: aborted\n"), (1, "", "Error: cannot read proxy.yaml")])
def test_get_status_error_drops_cli_error_prefix(fake_run, result):
    _, results = fake_run
    results[0] = result
    status = cli.AdGuardCLI().get_status()
    assert status.status == cli.AdGuardStatus.ERROR
    assert status.message == result[2].removeprefix("Error: ").strip()


@pytest.mark.parametrize("method, result_type", [
    ("get_filters", "groups"), ("get_dns_filters", "groups"), ("get_userscripts", "scripts"),
])
def test_list_error_drops_cli_error_prefix(fake_run, method, result_type):
    _, result = fake_run
    result[0] = (1, "Error: not running\nhint", "Error: not running")
    res = getattr(cli.AdGuardCLI(), method)()
    assert res.error.splitlines() == ["not running", "hint"]
    assert not getattr(res, result_type)


def test_privileged_command_keeps_credentials_out_of_log(monkeypatch, caplog):
    results = iter([(1, "", "Error: https://h.example/p?token=abc: 403")] * 3)
    monkeypatch.setattr(cli, "_run", lambda args, timeout=15, stdin_data=None: next(results))
    with caplog.at_level(logging.INFO, logger="adguard_tray.cli"):
        cli.AdGuardCLI()._privileged_command("start")
    assert "https://h.example/p: 403" in caplog.text
    assert "token" not in caplog.text


def test_privileged_command_error_drops_cli_error_prefix(monkeypatch):
    results = iter([(1, "", "Error: socket busy"), (1, "", "Error: still busy"), (1, "Error: unit failed", "")])
    monkeypatch.setattr(cli, "_run", lambda args, timeout=15, stdin_data=None: next(results))
    assert cli.AdGuardCLI()._privileged_command("start") == (False, "unit failed", "socket busy")


def test_install_rejects_non_http_url(fake_run):
    calls, _ = fake_run
    ok, _ = cli.AdGuardCLI().install_userscript("file:///etc/passwd")
    assert not ok
    assert calls == []


def test_get_userscripts_survives_bad_meta(fake_run, monkeypatch, tmp_path):
    _, result = fake_run
    monkeypatch.setattr(cli, "_USERSCRIPTS_DIR", tmp_path)
    (tmp_path / "good.meta.json").write_text('{"name": "Good Script"}', encoding="utf-8")
    (tmp_path / "latin1.meta.json").write_bytes(b'{"name": "\xe4\xf6\xfc"}')
    (tmp_path / "listed.meta.json").write_text('["x"]', encoding="utf-8")
    (tmp_path / "nested.meta.json").write_text('{"name": {"en": "X"}}', encoding="utf-8")
    result[0] = (0, "\n".join(
        f"[x] | Title: {title}                 2026-03-10 20:10:25\n    |    ID: {sid}"
        for sid, title in (("good", "Good Script"), ("latin1", "Latin"),
                           ("listed", "Listed"), ("nested", "Nested"))
    ), "")

    scripts = cli.AdGuardCLI().get_userscripts().scripts

    titles = {s.name: s.title for s in scripts}
    assert titles == {"good": "Good Script", "latin1": "latin1", "listed": "listed", "nested": "nested"}


def test_get_userscripts_blank_meta_name_falls_back_to_id(fake_run, monkeypatch, tmp_path):
    _, result = fake_run
    monkeypatch.setattr(cli, "_USERSCRIPTS_DIR", tmp_path)
    (tmp_path / "blank.meta.json").write_text('{"name": "   "}', encoding="utf-8")
    (tmp_path / "padded.meta.json").write_text('{"name": "  Padded  "}', encoding="utf-8")
    result[0] = (0, "", "")

    titles = {s.name: s.title for s in cli.AdGuardCLI().get_userscripts().scripts}

    assert titles == {"blank": "blank", "padded": "Padded"}


@pytest.mark.parametrize("code, expected", [
    (126, "Authentication cancelled"),
    (127, "Authorization failed"),
    (-2, "Command timed out after 60s"),
])
def test_privileged_command_pkexec_exit_stops_fallbacks(monkeypatch, code, expected):
    calls = []
    results = iter([(1, "", "socket busy"), (code, "", "Command timed out after 60s")])

    def run(args, timeout=15, stdin_data=None):
        calls.append(args)
        return next(results)

    monkeypatch.setattr(cli, "_run", run)
    ok, msg, first_error = cli.AdGuardCLI()._privileged_command("start")
    assert (ok, msg, first_error) == (False, cli._t(expected), "")
    assert [c[0] for c in calls] == ["adguard-cli", "pkexec"]


def test_run_timeout_kills_child(monkeypatch):
    procs = []

    class Popen(subprocess.Popen):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            procs.append(self)

    monkeypatch.setattr(cli.subprocess, "Popen", Popen)
    start = time.monotonic()
    assert cli._run(["sleep", "5"], timeout=0.2) == (-2, "", "Command timed out after 0.2s")
    assert time.monotonic() - start < 2
    assert procs[0].wait(timeout=2) is not None


def test_run_does_not_inherit_stdin():
    # An open pipe on fd 0 stands in for the launching terminal.
    saved = os.dup(0)
    r, w = os.pipe()
    try:
        os.dup2(r, 0)
        code, out, _ = cli._run(["sh", "-c", "read x || echo EOF"], timeout=3)
    finally:
        os.dup2(saved, 0)
        for fd in (saved, r, w):
            os.close(fd)
    assert (code, out) == (0, "EOF")


def test_privileged_command_127_log_keeps_credentials_out(monkeypatch, caplog):
    results = iter([(1, "", "x"), (127, "", "Error: https://u:pw@h.example/p?token=abc denied")])
    monkeypatch.setattr(cli, "_run", lambda args, timeout=15, stdin_data=None: next(results))
    with caplog.at_level(logging.INFO, logger="adguard_tray.cli"):
        assert cli.AdGuardCLI()._privileged_command("start")[1] == cli._t("Authorization failed")
    assert "https://h.example/p denied" in caplog.text
    for secret in ("u:", "pw@", "token", "abc"):
        assert secret not in caplog.text


def test_get_status_exit_zero_stderr_only_drops_prefix(fake_run):
    _, results = fake_run
    results[0] = (0, "", "Error: x")
    assert cli.AdGuardCLI().get_status().message == "x"


@pytest.mark.parametrize("result, expected", [
    ((1, "hint", "Error: unit busy"), "unit busy\nhint"),
    ((126, "", ""), "Authentication cancelled"),
    ((127, "", "Error: not authorized"), "Authorization failed"),
    ((1, "", ""), "Could not stop AdGuard – process may still be running"),
])
def test_stop_systemctl_failure_message(monkeypatch, result, expected):
    def run(args, timeout=15, stdin_data=None):
        if args[:2] == ["pkexec", "systemctl"]:
            return result
        if args[:2] == ["systemctl", "is-active"]:
            return 0, "active", ""
        return 0, "adguard-cli has been stopped", ""

    monkeypatch.setattr(cli, "_run", run)
    monkeypatch.setattr(cli.time, "sleep", lambda s: None)
    assert cli.AdGuardCLI().stop() == (False, cli._t(expected))


@pytest.mark.parametrize("err, expected", [
    ("Download error: 403", "Download error: 403"), ("Error: x", "x"), ("ERROR", ""),
])
def test_cli_error_strips_prefix_only_at_line_start(err, expected):
    assert cli._cli_error(err, "") == expected


def test_cli_error_is_clipped():
    assert cli._cli_error("x" * 30_000, "") == "x" * cli._MAX_OUTPUT + "\n…"


def test_log_text_redacts_uppercase_scheme():
    logged = cli._log_text("HTTPS://u:pw@h.example/p?token=x")
    assert "pw" not in logged
    assert "token" not in logged


@pytest.mark.parametrize("text, expected", [
    ("(https://h.example/p?x=1).", "(https://h.example/p)."),
    ("https://h.example/p.", "https://h.example/p."),
    ('"https://h.example/p?x=1"', '"https://h.example/p"'),
    ("'https://h.example/p?x=1'", "'https://h.example/p'"),
    *((f"https://h.example/p?x=1{c}", f"https://h.example/p{c}") for c in ".,;:!?)]}'\""),
])
def test_log_text_keeps_trailing_punctuation(text, expected):
    assert cli._log_text(text) == expected


def test_simple_unnamed_signal_crash(fake_run):
    _, result = fake_run
    result[0] = (-40, "", "")
    assert cli.AdGuardCLI()._simple(["x"], "ok", "fallback") == (False, "fallback\nadguard-cli crashed (signal 40)")


def test_simple_signal_crash_is_logged(fake_run, caplog):
    _, result = fake_run
    result[0] = (-11, "", "")
    with caplog.at_level(logging.ERROR, logger="adguard_tray.cli"):
        cli.AdGuardCLI()._simple(["x"], "ok", "fallback", "do_thing(1)")
    errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
    assert len(errors) == 1
    assert "do_thing(1)" in errors[0]
    assert "crashed" in errors[0]


def test_install_userscript_uses_30s_timeout_for_both_attempts(monkeypatch):
    timeouts = []

    def run(args, timeout=15, stdin_data=None):
        timeouts.append(timeout)
        return 1, "", "Error: Failed to install userscript"

    monkeypatch.setattr(cli, "_run", run)
    monkeypatch.setattr(cli, "_userscript_source",
                        lambda url: contextlib.nullcontext("http://127.0.0.1:1/x.user.js"))
    assert not cli.AdGuardCLI().install_userscript(URL)[0]
    assert timeouts == [30, 30]
