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


def _unit_disabled(run):
    """Fake _run that answers `systemctl is-enabled` with "disabled" itself and passes other calls to run."""
    def wrapped(args, timeout=15, stdin_data=None):
        if args[:2] == ["systemctl", "is-enabled"]:
            return 1, "disabled", ""
        return run(args, timeout, stdin_data)
    return wrapped


@pytest.mark.parametrize("out, expected", [
    ("AdGuard CLI v1.3.45", "1.3.45"),
    ("AdGuard CLI v1.5.1\nfilter-list-manager v2.7.0", "1.5.1"),
    ("AdGuard CLI v1.5.1 (filter-list-manager v2.7.0)", "1.5.1"),
    ("filter-list-manager v2.7.0\nAdGuard CLI v1.5.1", "1.5.1"),
    ("AdGuard CLI version 1.5.1", "1.5.1"),
    ("AdGuard CLI 1.5.1-beta.2", "1.5.1-beta.2"),
    ("AdGuard CLI v1.5.1-nightly+abc.1", "1.5.1-nightly+abc.1"),
    ("AdGuard CLI v1.5.1.", "1.5.1"),
    ("AdGuard CLI\nfilter-list-manager v2.7.0", ""),
    ("unexpected output", ""),
])
def test_get_version_takes_cli_version(fake_run, out, expected):
    _, result = fake_run
    result[0] = (0, out, "")
    assert cli.AdGuardCLI().get_version() == expected


def test_get_version_empty_on_failure(fake_run):
    _, result = fake_run
    result[0] = (1, "AdGuard CLI v1.5.1", "")
    assert cli.AdGuardCLI().get_version() == ""
    result[0] = (0, "", "")
    assert cli.AdGuardCLI().get_version() == ""


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
    monkeypatch.setattr(cli, "_run", _unit_disabled(lambda args, timeout=15, stdin_data=None: next(results)))
    with caplog.at_level(logging.INFO, logger="adguard_tray.cli"):
        cli.AdGuardCLI()._privileged_command("start")
    assert "https://h.example/p: 403" in caplog.text
    assert "token" not in caplog.text


def test_privileged_command_error_drops_cli_error_prefix(monkeypatch):
    results = iter([(1, "", "Error: socket busy"), (1, "", "Error: still busy"), (1, "Error: unit failed", "")])
    monkeypatch.setattr(cli, "_run", _unit_disabled(lambda args, timeout=15, stdin_data=None: next(results)))
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

    monkeypatch.setattr(cli, "_run", _unit_disabled(run))
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
    monkeypatch.setattr(cli, "_run", _unit_disabled(lambda args, timeout=15, stdin_data=None: next(results)))
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


@pytest.mark.parametrize("result, expected", [
    ((0, "enabled", ""), True),
    ((1, "disabled", ""), False),
    ((1, "masked", ""), False),
    ((0, "static", ""), False),
    ((1, "", ""), False),               # no unit installed
    ((-1, "", "Binary not found: systemctl"), False),
])
def test_service_enabled(fake_run, result, expected):
    calls, results = fake_run
    results[0] = result
    assert cli.AdGuardCLI().service_enabled() is expected
    assert calls == [["systemctl", "is-enabled", "adguard-cli.service"]]


def test_service_command_uses_the_configured_binary():
    adguard = cli.AdGuardCLI("/opt/adguard-cli/adguard-cli")
    assert adguard.service_command(True) == ["/opt/adguard-cli/adguard-cli", "install-service"]
    assert adguard.service_command(False) == ["/opt/adguard-cli/adguard-cli", "install-service", "--uninstall"]


IS_ENABLED = ["systemctl", "is-enabled", "adguard-cli.service"]
IS_ACTIVE = ["systemctl", "is-active", "adguard-cli"]
UNIT_RESTART = ["pkexec", "systemctl", "restart", "adguard-cli"]
UNIT_STOP = ["pkexec", "systemctl", "stop", "adguard-cli"]
RUNNING = (0, "AdGuard CLI is running on 127.0.0.1:3129", "")
STOPPED = (0, "AdGuard CLI is not running", "")
FAILED = (1, "", "Error: cannot read proxy.yaml")
TIMED_OUT = (-2, "", "Command timed out after 15s")


def _unit_run(monkeypatch, enabled=(0, "enabled", ""), active=(3, "inactive", ""), restart=(0, "", ""),
              status=STOPPED, direct=(1, "", "Error: no privileges")):
    """Fake _run for the boot unit; every other call fails like a CLI without privileges."""
    calls = []

    def run(args, timeout=15, stdin_data=None):
        calls.append((args, timeout))
        if args == IS_ENABLED:
            return enabled
        if args == IS_ACTIVE:
            return active
        if args == UNIT_RESTART:
            return restart
        if args == ["adguard-cli", "status"]:
            return status
        if args in (["adguard-cli", "start"], ["adguard-cli", "restart"]):
            return direct
        return 1, "", "Error: no privileges"

    monkeypatch.setattr(cli, "_run", run)
    return calls


@pytest.mark.parametrize("cmd", ["start", "restart"])
@pytest.mark.parametrize("active", [(3, "inactive", ""), (3, "failed", ""), (3, "activating", "")])
def test_enabled_unit_down_starts_through_the_unit(monkeypatch, cmd, active):
    calls = _unit_run(monkeypatch, active=active)
    assert cli.AdGuardCLI()._privileged_command(cmd) == (True, cli._t("AdGuard via systemctl {} ok", cmd), "")
    assert calls == [(IS_ENABLED, 5), (IS_ACTIVE, 5), (["adguard-cli", "status"], 15), (UNIT_RESTART, 60)]


@pytest.mark.parametrize("cmd", ["start", "restart"])
@pytest.mark.parametrize("status", [STOPPED, RUNNING])
@pytest.mark.parametrize("active", [
    (0, "active", ""),
    (3, "deactivating", ""),
    (4, "unknown", ""),
    (1, "", "Failed to connect to bus: No such file or directory"),
])
def test_enabled_unit_not_down_goes_direct(monkeypatch, cmd, status, active):
    calls = _unit_run(monkeypatch, active=active, status=status, direct=(0, "started", ""))
    assert cli.AdGuardCLI()._privileged_command(cmd) == (True, "started", "started")
    assert [args for args, _ in calls] == [IS_ENABLED, IS_ACTIVE, ["adguard-cli", cmd]]


@pytest.mark.parametrize("cmd", ["start", "restart"])
@pytest.mark.parametrize("status", [
    RUNNING,
    (0, "adguard-cli has been stopped\nAdGuard CLI is running on 127.0.0.1:3129", ""),
    TIMED_OUT,
    FAILED,
    (0, "AdGuard CLI status unavailable", ""),
])
def test_enabled_unit_down_goes_direct_unless_the_proxy_is_stopped(monkeypatch, cmd, status):
    calls = _unit_run(monkeypatch, status=status, direct=(0, "started", ""))
    assert cli.AdGuardCLI()._privileged_command(cmd) == (True, "started", "started")
    assert [args for args, _ in calls] == [IS_ENABLED, IS_ACTIVE, ["adguard-cli", "status"], ["adguard-cli", cmd]]


@pytest.mark.parametrize("cmd", ["start", "restart"])
@pytest.mark.parametrize("enabled", [(1, "disabled", ""), (-1, "", "Binary not found: systemctl")])
def test_start_without_enabled_unit_keeps_attempt_order(monkeypatch, cmd, enabled):
    calls = _unit_run(monkeypatch, enabled=enabled, restart=(1, "", "Error: no privileges"))
    assert cli.AdGuardCLI()._privileged_command(cmd) == (False, "no privileges", "no privileges")
    assert [args for args, _ in calls] == [
        IS_ENABLED, ["adguard-cli", cmd], ["pkexec", "adguard-cli", cmd],
        ["pkexec", "systemctl", cmd, "adguard-cli"],
    ]


@pytest.mark.parametrize("restart, expected", [
    ((126, "", ""), ("Authentication cancelled",)),
    ((-2, "", "Command timed out after 60s"), ("Command timed out after 60s",)),
    ((-2, "", ""), ("'{}' failed – insufficient privileges?", "start")),
])
def test_enabled_unit_failure_is_final(monkeypatch, restart, expected):
    calls = _unit_run(monkeypatch, restart=restart)
    assert cli.AdGuardCLI()._privileged_command("start") == (False, cli._t(*expected), "")
    assert [args for args, _ in calls] == [IS_ENABLED, IS_ACTIVE, ["adguard-cli", "status"], UNIT_RESTART]


@pytest.mark.parametrize("cmd", ["start", "restart"])
@pytest.mark.parametrize("restart, level", [
    ((1, "hint", "Error: unit failed"), logging.WARNING),
    ((1, "", ""), logging.WARNING),
    ((127, "", "Error: not authorized"), logging.INFO),
    ((-1, "", "Binary not found: pkexec"), logging.INFO),
    ((-3, "", "[Errno 13] Permission denied: 'pkexec'"), logging.INFO),
])
def test_enabled_unit_failure_falls_back_to_the_direct_attempt(monkeypatch, caplog, cmd, restart, level):
    calls = _unit_run(monkeypatch, restart=restart, direct=(0, "started", ""))
    with caplog.at_level(logging.INFO, logger="adguard_tray.cli"):
        assert cli.AdGuardCLI()._privileged_command(cmd) == (True, "started", "started")
    assert [args for args, _ in calls] == [
        IS_ENABLED, IS_ACTIVE, ["adguard-cli", "status"], UNIT_RESTART, ["adguard-cli", cmd],
    ]
    assert [r.levelno for r in caplog.records if "systemctl restart adguard-cli" in r.getMessage()] == [level]


def test_start_socket_busy_retry_does_not_ask_for_the_unit_again(monkeypatch):
    calls = _unit_run(monkeypatch, restart=(1, "", "Error: unit failed"))
    inner = cli._run
    direct = iter([(1, "", "Error: socket busy"), (0, "started", "")])

    def run(args, timeout=15, stdin_data=None):
        if args == ["adguard-cli", "start"]:
            calls.append((args, timeout))
            return next(direct)
        return inner(args, timeout, stdin_data)

    monkeypatch.setattr(cli, "_run", run)
    monkeypatch.setattr(cli.time, "sleep", lambda s: None)
    adguard = cli.AdGuardCLI()
    kills = []
    monkeypatch.setattr(adguard, "_force_kill", lambda: kills.append(len(calls)))
    assert adguard.start() == (True, "started")
    assert [args for args, _ in calls] == [
        IS_ENABLED, IS_ACTIVE, ["adguard-cli", "status"], UNIT_RESTART,
        ["adguard-cli", "start"], ["pkexec", "adguard-cli", "start"], ["adguard-cli", "start"],
    ]
    assert kills == [6]


def test_failed_unit_restart_skips_the_systemctl_fallback(monkeypatch):
    calls = _unit_run(monkeypatch, restart=(1, "", "Error: unit failed"), direct=(1, "", "Error: direct failed"))
    assert cli.AdGuardCLI()._privileged_command("restart") == (False, "no privileges", "direct failed")
    assert [args for args, _ in calls] == [
        IS_ENABLED, IS_ACTIVE, ["adguard-cli", "status"], UNIT_RESTART,
        ["adguard-cli", "restart"], ["pkexec", "adguard-cli", "restart"],
    ]


def test_each_action_tries_the_unit_once(monkeypatch):
    calls = _unit_run(monkeypatch, restart=(1, "", "Error: unit failed"), direct=(0, "started", ""))
    adguard = cli.AdGuardCLI()
    assert adguard.start() == (True, "started")
    assert adguard.start() == (True, "started")
    assert [args for args, _ in calls] == 2 * [
        IS_ENABLED, IS_ACTIVE, ["adguard-cli", "status"], UNIT_RESTART, ["adguard-cli", "start"],
    ]


def test_stop_never_asks_for_the_unit(monkeypatch):
    calls = _unit_run(monkeypatch)
    cli.AdGuardCLI()._privileged_command("stop")
    assert [args for args, _ in calls] == [
        ["adguard-cli", "stop"], ["pkexec", "adguard-cli", "stop"], ["pkexec", "systemctl", "stop", "adguard-cli"],
    ]


@pytest.mark.parametrize("retry, expected", [
    ([(0, "started", "")], (True, "started")),
    ([(1, "", "Error: socket busy"), (1, "", "still busy"), (1, "", "unit failed")], (False, "unit failed")),
])
def test_start_socket_busy_force_kills_and_retries_once(monkeypatch, retry, expected):
    results = iter([(1, "", "Error: socket busy"), (1, "", "still busy"), (1, "", "unit failed"), *retry])
    calls = []

    def run(args, timeout=15, stdin_data=None):
        calls.append(args)
        return next(results)

    monkeypatch.setattr(cli, "_run", _unit_disabled(run))
    monkeypatch.setattr(cli.time, "sleep", lambda s: None)
    adguard = cli.AdGuardCLI()
    kills = []
    monkeypatch.setattr(adguard, "_force_kill", lambda: kills.append(len(calls)))
    assert adguard.start() == expected
    assert kills == [3]
    assert len(calls) == 3 + len(retry)


@pytest.mark.parametrize("status, started", [
    (cli.AdGuardStatus.INACTIVE, True),
    (cli.AdGuardStatus.ERROR, True),
    (cli.AdGuardStatus.UNKNOWN, True),
    (cli.AdGuardStatus.ACTIVE, False),
])
def test_restart_falls_back_to_start_unless_active(monkeypatch, status, started):
    monkeypatch.setattr(cli.time, "sleep", lambda s: None)
    adguard = cli.AdGuardCLI()
    starts = []
    monkeypatch.setattr(adguard, "_privileged_command", lambda cmd: (True, f"{cmd} ok", ""))
    monkeypatch.setattr(adguard, "get_status", lambda: cli.StatusResult(status))
    monkeypatch.setattr(adguard, "_start", lambda: starts.append(1) or (True, "start ok"))
    assert adguard.restart() == ((True, "start ok") if started else (True, "restart ok"))
    assert len(starts) == started


def _status_run(monkeypatch, unit="inactive"):
    status = [RUNNING]

    def run(args, timeout=15, stdin_data=None):
        if args == IS_ACTIVE:
            return (0 if unit == "active" else 3), unit, ""
        return status[0]

    monkeypatch.setattr(cli, "_run", run)
    return status


@pytest.mark.parametrize("before", [RUNNING, STOPPED])
@pytest.mark.parametrize("failure, fallback", [(FAILED, cli.AdGuardStatus.INACTIVE), (TIMED_OUT, cli.AdGuardStatus.ERROR)])
def test_get_status_keeps_answer_over_one_failed_call(monkeypatch, before, failure, fallback):
    status = _status_run(monkeypatch)
    status[0] = before
    adguard = cli.AdGuardCLI()
    answer = adguard.get_status()
    status[0] = failure
    assert adguard.get_status() == answer
    assert adguard.get_status().status == fallback


@pytest.mark.parametrize("unit, failure, expected", [
    ("inactive", FAILED, cli.AdGuardStatus.INACTIVE),
    ("inactive", TIMED_OUT, cli.AdGuardStatus.ERROR),
    ("active", FAILED, cli.AdGuardStatus.ACTIVE),
])
def test_get_status_failure_without_answer_falls_back_at_once(monkeypatch, unit, failure, expected):
    status = _status_run(monkeypatch, unit)
    status[0] = failure
    assert cli.AdGuardCLI().get_status().status == expected


def test_get_status_failed_call_with_the_unit_active_is_an_answer(monkeypatch):
    status = _status_run(monkeypatch)
    status[0] = STOPPED
    adguard = cli.AdGuardCLI()
    assert adguard.get_status().status == cli.AdGuardStatus.INACTIVE
    status = _status_run(monkeypatch, "active")
    status[0] = FAILED
    answer = adguard.get_status()
    assert answer == cli.StatusResult(cli.AdGuardStatus.ACTIVE, "cannot read proxy.yaml")
    status[0] = TIMED_OUT
    assert adguard.get_status() == answer
    assert adguard.get_status().status == cli.AdGuardStatus.ERROR


@pytest.mark.parametrize("action", ["start", "stop", "restart"])
def test_get_status_does_not_replay_answer_across_an_action(monkeypatch, action):
    status = _status_run(monkeypatch)
    adguard = cli.AdGuardCLI()
    adguard.get_status()
    status[0] = FAILED
    during = []

    def act():
        during.append(adguard.get_status().status)
        status[0] = RUNNING
        adguard.get_status()
        status[0] = FAILED
        return True, ""

    monkeypatch.setattr(adguard, f"_{action}", act)
    assert getattr(adguard, action)() == (True, "")
    assert during == [cli.AdGuardStatus.INACTIVE]
    assert adguard.get_status().status == cli.AdGuardStatus.INACTIVE


def test_stop_force_kill_does_not_escalate_on_one_failed_status_call(monkeypatch):
    calls = []

    def run(args, timeout=15, stdin_data=None):
        calls.append(args)
        if args == IS_ACTIVE:
            return 3, "inactive", ""
        if args == ["adguard-cli", "status"]:
            return TIMED_OUT if ["pkill", "-x", "adguard_root_he"] in calls else RUNNING
        return 0, "", ""

    monkeypatch.setattr(cli, "_run", run)
    monkeypatch.setattr(cli.time, "sleep", lambda s: None)
    adguard = cli.AdGuardCLI()
    assert adguard.get_status().status == cli.AdGuardStatus.ACTIVE
    assert adguard.stop() == (True, cli._t("AdGuard stopped (forced)"))
    assert ["pkill", "-x", "adguard_root_he"] in calls
    assert not [c for c in calls if c[:2] == ["pkexec", "pkill"]]


def test_get_status_neither_replays_nor_remembers_while_the_lock_is_held(monkeypatch):
    status = _status_run(monkeypatch)
    adguard = cli.AdGuardCLI()
    adguard._action_lock.acquire()
    assert adguard.get_status().status == cli.AdGuardStatus.ACTIVE
    adguard._action_lock.release()
    status[0] = FAILED
    assert adguard.get_status().status == cli.AdGuardStatus.INACTIVE

    status[0] = RUNNING
    adguard.get_status()
    adguard._action_lock.acquire()
    status[0] = FAILED
    assert adguard.get_status().status == cli.AdGuardStatus.INACTIVE
    adguard._action_lock.release()


def test_get_status_overlapping_the_end_of_an_action_is_not_remembered(monkeypatch):
    status = _status_run(monkeypatch)
    adguard = cli.AdGuardCLI()
    inner = cli._run

    def run(args, timeout=15, stdin_data=None):
        if args == ["adguard-cli", "status"] and status[0] == RUNNING:
            assert adguard._exclusive(lambda: (True, "")) == (True, "")
        return inner(args, timeout, stdin_data)

    monkeypatch.setattr(cli, "_run", run)
    assert adguard.get_status().status == cli.AdGuardStatus.ACTIVE
    status[0] = FAILED
    assert adguard.get_status().status == cli.AdGuardStatus.INACTIVE


def test_get_status_remembers_the_latest_answer(monkeypatch):
    status = _status_run(monkeypatch)
    adguard = cli.AdGuardCLI()
    assert adguard.get_status().status == cli.AdGuardStatus.ACTIVE
    status[0] = (0, "AdGuard CLI status unavailable", "")
    answer = adguard.get_status()
    assert answer.status == cli.AdGuardStatus.INACTIVE
    status[0] = TIMED_OUT
    assert adguard.get_status() == answer


@pytest.mark.parametrize("unit, started", [("inactive", True), ("active", False)])
def test_restart_checks_a_failed_status_call_without_replay(monkeypatch, unit, started):
    status = _status_run(monkeypatch, unit)
    monkeypatch.setattr(cli.time, "sleep", lambda s: None)
    adguard = cli.AdGuardCLI()
    assert adguard.get_status().status == cli.AdGuardStatus.ACTIVE
    status[0] = FAILED
    starts = []
    monkeypatch.setattr(adguard, "_privileged_command", lambda cmd: (True, f"{cmd} ok", ""))
    monkeypatch.setattr(adguard, "_start", lambda: starts.append(1) or (True, "start ok"))
    assert adguard.restart() == ((True, "start ok") if started else (True, "restart ok"))
    assert len(starts) == started


@pytest.mark.parametrize("code, ok, msg", [
    (0, True, ("AdGuard via systemctl {} ok", "stop")),
    (126, False, ("Authentication cancelled",)),
])
def test_stop_active_unit_stops_the_unit(monkeypatch, code, ok, msg):
    calls = []

    def run(args, timeout=15, stdin_data=None):
        calls.append(args)
        if args == IS_ACTIVE:
            return 0, "active", ""
        if args == UNIT_STOP:
            return code, "", ""
        return 0, "adguard-cli has been stopped", ""

    monkeypatch.setattr(cli, "_run", run)
    monkeypatch.setattr(cli.time, "sleep", lambda s: None)
    assert cli.AdGuardCLI().stop() == (ok, cli._t(*msg))
    assert calls == [["adguard-cli", "stop"], ["adguard-cli", "status"], IS_ACTIVE, UNIT_STOP]


@pytest.mark.parametrize("status_out, expected", [
    ("adguard-cli has been stopped", (True, "stop ok")),
    ("", (True, "stop ok")),
    ("AdGuard CLI is running", (True, "forced")),
])
def test_stop_force_kills_only_a_proxy_still_running(monkeypatch, status_out, expected):
    calls = []

    def run(args, timeout=15, stdin_data=None):
        calls.append(args)
        if args == IS_ACTIVE:
            return 3, "inactive", ""
        if args == ["adguard-cli", "stop"]:
            return 0, "stop ok", ""
        return 0, status_out, ""

    monkeypatch.setattr(cli, "_run", run)
    monkeypatch.setattr(cli.time, "sleep", lambda s: None)
    adguard = cli.AdGuardCLI()
    monkeypatch.setattr(adguard, "_force_kill", lambda: (True, "forced"))
    assert adguard.stop() == expected
    assert UNIT_STOP not in calls


def test_force_kill_escalates_to_pkexec_when_user_pkill_leaves_it_running(monkeypatch):
    calls = []

    def run(args, timeout=15, stdin_data=None):
        calls.append(args)
        if args == ["adguard-cli", "status"]:
            escalated = ["pkexec", "pkill", "-x", "adguard_root_he"] in calls
            return 0, "AdGuard CLI is not running" if escalated else "AdGuard CLI is running", ""
        if args == IS_ACTIVE:
            return 3, "inactive", ""
        return 1, "", ""    # pkill: the root helper can't be signalled from the user session

    monkeypatch.setattr(cli, "_run", run)
    monkeypatch.setattr(cli.time, "sleep", lambda s: None)
    assert cli.AdGuardCLI()._force_kill() == (True, cli._t("AdGuard stopped (forced)"))
    assert [c for c in calls if "pkill" in c] == [
        ["pkill", "-x", "adguard-cli"], ["pkill", "-x", "adguard_root_he"],
        ["pkexec", "pkill", "-x", "adguard-cli"], ["pkexec", "pkill", "-x", "adguard_root_he"],
    ]
