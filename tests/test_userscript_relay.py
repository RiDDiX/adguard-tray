import contextlib
import http.client
import http.server
import io
import logging
import os
import socket
import struct
import threading
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit

import pytest

import adguard_tray
from adguard_tray import cli, userscript_relay

HEADER = b"// ==UserScript==\n// @name Relayed\n// @downloadURL https://example.org/x.user.js\n// ==/UserScript==\n"
BODY = HEADER + bytes(range(256))
FAIL = (0, "Failed to install userscript", "")


class _Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.seen.append(self.path)
        self.server.agents.append(self.headers["User-Agent"])
        status, location, body, *stall = self.server.routes.get(self.path, (404, None, b""))
        if stall:
            time.sleep(stall[0])
        self.send_response(status)
        if location:
            self.send_header("Location", location)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


@contextlib.contextmanager
def _serve(host):
    srv = http.server.ThreadingHTTPServer((host, 0), _Handler)
    srv.daemon_threads = True
    srv.routes, srv.seen, srv.agents = {}, [], []
    srv.base = f"http://{host}:{srv.server_address[1]}"
    thread = threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
    thread.start()
    try:
        yield srv
    finally:
        srv.shutdown()
        srv.server_close()
        thread.join()


@pytest.fixture
def server(monkeypatch):
    monkeypatch.setenv("no_proxy", "*")
    monkeypatch.setenv("NO_PROXY", "*")
    with _serve("127.0.0.1") as srv:
        yield srv


@contextlib.contextmanager
def _raw_server(head, drip=b"", interval=0.0):
    """One connection: send `head`, then `drip` byte by byte, then close."""
    lsock = socket.create_server(("127.0.0.1", 0))
    lsock.settimeout(5)
    stop = threading.Event()

    def serve():
        with contextlib.suppress(OSError):
            conn, _ = lsock.accept()
            with conn:
                conn.recv(65536)
                conn.sendall(head)
                for b in drip:
                    if stop.wait(interval):
                        break
                    conn.sendall(bytes([b]))

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{lsock.getsockname()[1]}"
    finally:
        stop.set()
        thread.join(10)
        lsock.close()


@pytest.fixture
def fake_run(monkeypatch):
    calls, fetched = [], []
    behaviour = {"first": FAIL, "fetch": False, "raise": False}

    def run(args, timeout=15, stdin_data=None):
        calls.append(args)
        if len(calls) == 1 and behaviour["first"]:
            return behaviour["first"]
        if behaviour["fetch"]:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            with opener.open(args[-1], timeout=5) as resp:
                fetched.append(resp.read())
        if behaviour["raise"]:
            raise RuntimeError("cli crashed")
        return 0, "Userscript installed", ""

    monkeypatch.setattr(cli, "_run", run)
    return calls, fetched, behaviour


def _refused(url):
    host, port = url.split("//")[1].split("/")[0].split(":")
    with pytest.raises(ConnectionRefusedError), socket.create_connection((host, int(port)), timeout=2):
        pass


def _first_failure():
    return False, "Failed to install userscript"


def test_cli_success_makes_no_request(server, fake_run):
    calls, _, behaviour = fake_run
    behaviour["first"] = None
    server.routes["/x.user.js"] = (302, "/asset/1", b"")
    url = server.base + "/x.user.js"
    assert cli.AdGuardCLI().install_userscript(url) == (True, "Userscript installed")
    assert [c[-3:] for c in calls] == [["userscripts", "install", url]]
    assert server.seen == []


def test_not_redirected_returns_first_failure_after_one_probe(server, fake_run, monkeypatch):
    calls, _, _ = fake_run
    reads = []
    for name in ("read", "read1"):
        real = getattr(http.client.HTTPResponse, name)
        monkeypatch.setattr(http.client.HTTPResponse, name,
                            lambda self, *a, _real=real: reads.append(a) or _real(self, *a))
    seen_by_cli, run = [], cli._run
    monkeypatch.setattr(cli, "_run", lambda *a, **kw: seen_by_cli.append(list(server.seen)) or run(*a, **kw))
    server.routes["/x.user.js"] = (200, None, BODY)
    url = server.base + "/x.user.js"
    assert cli.AdGuardCLI().install_userscript(url) == _first_failure()
    assert [c[-3:] for c in calls] == [["userscripts", "install", url]]
    assert seen_by_cli == [[]]
    assert server.seen == ["/x.user.js"]
    assert reads == []


def test_redirect_to_userscript_url_hands_final_url(server, fake_run):
    calls, _, _ = fake_run
    server.routes["/latest/x.user.js"] = (302, "/v2/x.user.js", b"")
    server.routes["/v2/x.user.js"] = (200, None, BODY)
    ok, _ = cli.AdGuardCLI().install_userscript(server.base + "/latest/x.user.js")
    assert ok
    assert [c[-1] for c in calls] == [server.base + "/latest/x.user.js", server.base + "/v2/x.user.js"]


def test_redirect_to_asset_url_is_relayed(server, fake_run):
    calls, fetched, behaviour = fake_run
    behaviour["fetch"] = True
    server.routes["/latest/better-xcloud.user.js"] = (302, "/asset/123?sig=abc", b"")
    server.routes["/asset/123?sig=abc"] = (200, None, BODY)
    ok, _ = cli.AdGuardCLI().install_userscript(server.base + "/latest/better-xcloud.user.js")
    assert ok
    assert len(calls) == 2
    relay = calls[1][-1]
    assert relay.startswith("http://127.0.0.1:")
    assert relay.rpartition("/")[2] == "better-xcloud.user.js"
    assert relay.split(":")[2].split("/")[0] != str(server.server_address[1])
    assert fetched == [BODY]
    _refused(relay)


def test_relay_answers_only_its_path(server, monkeypatch):
    monkeypatch.setattr(userscript_relay, "_redirect_plan", lambda url, hops: None)
    server.routes["/x.user.js"] = (200, None, BODY)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with userscript_relay._userscript_source(server.base + "/x.user.js") as relay:
        with pytest.raises(urllib.error.HTTPError) as exc:
            opener.open(relay.rsplit("/", 1)[0] + "/other.user.js", timeout=5)
        assert exc.value.code == 404
        exc.value.close()
        with opener.open(relay, timeout=5) as resp:
            assert resp.headers["Content-Length"] == str(len(BODY))
            assert resp.read() == BODY


def test_relay_path_carries_a_token(server, monkeypatch):
    monkeypatch.setattr(userscript_relay, "_redirect_plan", lambda url, hops: None)
    server.routes["/x.user.js"] = (200, None, BODY)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with (userscript_relay._userscript_source(server.base + "/x.user.js") as first,
          userscript_relay._userscript_source(server.base + "/x.user.js") as second):
        base, token, name = first.rsplit("/", 2)
        assert name == "x.user.js" and len(token) >= 16
        assert token != second.rsplit("/", 2)[1]
        with pytest.raises(urllib.error.HTTPError) as exc:
            opener.open(f"{base}/{name}", timeout=5)
        assert exc.value.code == 404
        exc.value.close()
        with opener.open(first, timeout=5) as resp:
            assert resp.read() == BODY


def test_probe_failure_returns_first_failure(fake_run, monkeypatch):
    calls, _, _ = fake_run
    monkeypatch.setenv("no_proxy", "*")
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        url = f"http://127.0.0.1:{s.getsockname()[1]}/x.user.js"
    assert cli.AdGuardCLI().install_userscript(url) == _first_failure()
    assert [c[-1] for c in calls] == [url]


def test_body_over_cap_returns_first_failure(server, fake_run, monkeypatch):
    calls, _, _ = fake_run
    monkeypatch.setattr(userscript_relay, "_RELAY_MAX", 10)
    server.routes["/x.user.js"] = (302, "/asset/1", b"")
    server.routes["/asset/1"] = (200, None, BODY)
    url = server.base + "/x.user.js"
    assert cli.AdGuardCLI().install_userscript(url) == _first_failure()
    assert [c[-1] for c in calls] == [url]


def test_redirect_body_is_not_read(server, fake_run):
    calls, fetched, behaviour = fake_run
    behaviour["fetch"] = True
    server.routes["/asset/1"] = (200, None, BODY)
    limit, sent = 32 * 1024 * 1024, []
    chunk = b"%x\r\n%s\r\n" % (65536, b"x" * 65536)
    lsock = socket.create_server(("127.0.0.1", 0))
    lsock.settimeout(5)

    def serve():
        # Bounded stand-in for an endless chunked redirect body.
        with contextlib.suppress(OSError):
            conn, _ = lsock.accept()
            with conn:
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
                conn.recv(65536)
                conn.sendall(b"HTTP/1.1 302 Found\r\nLocation: %s/asset/1\r\n"
                             b"Transfer-Encoding: chunked\r\n\r\n" % server.base.encode())
                while sum(sent) < limit:
                    conn.sendall(chunk)
                    sent.append(len(chunk))
                conn.sendall(b"0\r\n\r\n")

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{lsock.getsockname()[1]}/x.user.js"
        assert cli.AdGuardCLI().install_userscript(url)[0]
        thread.join(10)
    finally:
        lsock.close()
    assert calls[1][-1].startswith("http://127.0.0.1:") and fetched == [BODY]
    assert sum(sent) < limit // 2


def test_dripping_body_hits_deadline(server, fake_run, monkeypatch):
    calls, _, _ = fake_run
    monkeypatch.setattr(userscript_relay, "_RELAY_DEADLINE", 0.5)
    with _raw_server(b"HTTP/1.0 200 OK\r\n\r\n" + HEADER, drip=b"x" * 100, interval=0.1) as raw:
        server.routes["/x.user.js"] = (302, raw + "/asset/1", b"")
        url = server.base + "/x.user.js"
        start = time.monotonic()
        assert cli.AdGuardCLI().install_userscript(url) == _first_failure()
        assert time.monotonic() - start < 3
    assert [c[-1] for c in calls] == [url]


@pytest.mark.parametrize("head", [
    b"HTTP/1.1 200 OK\r\nContent-Length: 5000\r\n\r\n" + BODY,
    b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n",
    b"HTTP/1.0 200 OK\r\n\r\n",
], ids=["short", "empty-length", "empty-close"])
def test_truncated_or_empty_body_is_not_relayed(server, fake_run, head):
    calls, _, _ = fake_run
    with _raw_server(head) as raw:
        server.routes["/x.user.js"] = (302, raw + "/asset/1", b"")
        url = server.base + "/x.user.js"
        assert cli.AdGuardCLI().install_userscript(url) == _first_failure()
    assert [c[-1] for c in calls] == [url]


@pytest.mark.parametrize("body", [
    b"// ==UserScript==\n// @name X\n// @updateURL https://example.org/x.meta.js\n// ==/UserScript==\n",
    b"// ==UserScript==\n// @name X\n// @downloadURL\n// ==/UserScript==\n",
    b"// ==UserScript==\n// @name X\n// ==/UserScript==\n// @downloadURL https://example.org/x.user.js\n",
    b"// @downloadURL https://example.org/x.user.js\n// ==UserScript==\n// @name X\n// ==/UserScript==\n",
], ids=["missing", "empty", "after-header", "before-header"])
def test_body_without_download_url_is_not_relayed(server, fake_run, body):
    calls, _, _ = fake_run
    server.routes["/x.user.js"] = (302, "/asset/1", b"")
    server.routes["/asset/1"] = (200, None, body)
    url = server.base + "/x.user.js"
    assert cli.AdGuardCLI().install_userscript(url) == _first_failure()
    assert [c[-1] for c in calls] == [url]


def test_redirect_to_ftp_is_not_followed(server, fake_run, monkeypatch):
    calls, _, _ = fake_run
    monkeypatch.setattr(userscript_relay, "_PROBE_TIMEOUT", 1)
    with socket.create_server(("127.0.0.1", 0)) as hop:
        hop.setblocking(False)
        server.routes["/x.user.js"] = (302, f"ftp://127.0.0.1:{hop.getsockname()[1]}/x.user.js", b"")
        url = server.base + "/x.user.js"
        assert cli.AdGuardCLI().install_userscript(url) == _first_failure()
        with pytest.raises(BlockingIOError):
            hop.accept()
    assert [c[-1] for c in calls] == [url]


@pytest.mark.parametrize("origin, location", [
    ("https://a.example/x.user.js", "http://127.0.0.1:{}/x.user.js"),
    ("https://a.example/x.user.js", "HTTP://127.0.0.1:{}/x.user.js"),
])
def test_refused_hop_is_not_contacted(origin, location):
    with socket.create_server(("127.0.0.1", 0)) as hop:
        hop.setblocking(False)
        log = userscript_relay._RedirectLog(origin)
        req = urllib.request.Request(origin)
        req.timeout = 1
        headers = {"location": location.format(hop.getsockname()[1])}
        with pytest.raises(urllib.error.HTTPError):
            log.http_error_302(req, io.BytesIO(b""), 302, "Found", headers)
        with pytest.raises(BlockingIOError):
            hop.accept()
    assert log.hops == []


def test_relay_shut_down_when_cli_raises(server, fake_run):
    calls, _, behaviour = fake_run
    behaviour["raise"] = True
    server.routes["/x.user.js"] = (302, "/asset/1", b"")
    server.routes["/asset/1"] = (200, None, BODY)
    with pytest.raises(RuntimeError):
        cli.AdGuardCLI().install_userscript(server.base + "/x.user.js")
    assert len(calls) == 2
    relay = calls[1][-1]
    assert relay.startswith("http://127.0.0.1:") and relay.endswith("/x.user.js")
    assert not relay.startswith(server.base)
    _refused(relay)


@pytest.mark.parametrize("url, hops, expected", [
    ("https://a/x.user.js", [], "https://a/x.user.js"),
    ("https://a/x.user.js", ["https://b/y.user.js"], "https://b/y.user.js"),
    ("https://a/x.user.js", ["https://b/asset?sig=1"], None),
    ("http://a/x.user.js", ["https://b/asset"], None),
    ("https://a/download", ["https://b/asset"], "https://a/download"),
    ("https://a/x.user.js#f", ["https://b/asset"], "https://a/x.user.js#f"),
    ("https://a/x.user.js", ["https://b/y.user.js#f"], None),
    ("https://a/x.user.js", ["https://b/y.meta.js"], "https://b/y.meta.js"),
    ("https://a/x.user.js", ["https://b/y.user.css"], "https://b/y.user.css"),
    ("https://a/x.meta.js", ["https://b/asset"], None),
    ("https://a/x.user.css", ["https://b/asset"], None),
])
def test_redirect_plan(url, hops, expected):
    assert userscript_relay._redirect_plan(url, hops) == expected


def test_https_origin_refuses_public_http_hop():
    log = userscript_relay._RedirectLog("https://a.example/x.user.js")
    req = urllib.request.Request("https://a.example/x.user.js")
    with pytest.raises(urllib.error.HTTPError):
        log.redirect_request(req, io.BytesIO(b""), 302, "Found", {}, "http://b.example/x.user.js")
    assert log.hops == []


@pytest.mark.parametrize("host, is_global", [
    ("100.64.0.1", False), ("127.0.0.1", False), ("10.1.2.3", False), ("169.254.169.254", False),
    ("0.0.0.0", False), ("::1", False), ("fe80::1%lo", False), ("fd00::1", False),
    ("8.8.8.8", True), ("2001:4860::8888", True),
])
def test_global_address(host, is_global):
    assert userscript_relay._global_address(host) is is_global


@pytest.mark.parametrize("location", [
    "http://127.0.0.1:{}/x.user.js",
    "http://%31%32%37.0.0.1:{}/x.user.js",
    "http://%6c%6f%63%61%6c%68%6f%73%74:{}/x.user.js",
    "http://127.0.0.1%2e:{}/x.user.js",
    "http://internal.example:{}/x.user.js",
], ids=["plain", "encoded-ip", "encoded-localhost", "encoded-dot", "private-name"])
def test_public_origin_refuses_local_hop(fake_run, monkeypatch, location):
    calls, _, _ = fake_run
    monkeypatch.setenv("no_proxy", "*")
    # 127.0.0.2 stands in for a public origin; the hop listens on 127.0.0.1.
    monkeypatch.setattr(userscript_relay, "_global_address", lambda host: host == "127.0.0.2")
    resolve = socket.getaddrinfo
    names = {"127.0.0.1.": "127.0.0.1", "internal.example": "127.0.0.1"}
    monkeypatch.setattr(socket, "getaddrinfo", lambda host, *a, **kw: resolve(names.get(host, host), *a, **kw))
    with _serve("127.0.0.2") as origin, _serve("127.0.0.1") as hop:
        hop.routes["/x.user.js"] = (200, None, BODY)
        origin.routes["/x.user.js"] = (302, location.format(hop.server_address[1]), b"")
        url = origin.base + "/x.user.js"
        assert cli.AdGuardCLI().install_userscript(url) == _first_failure()
        assert hop.seen == []
    assert [c[-1] for c in calls] == [url]


def test_public_origin_follows_public_hop(fake_run, monkeypatch):
    calls, _, _ = fake_run
    monkeypatch.setenv("no_proxy", "*")
    monkeypatch.setattr(userscript_relay, "_global_address", lambda host: host == "127.0.0.2")
    with _serve("127.0.0.2") as origin:
        origin.routes["/x.user.js"] = (302, "/v2/x.user.js", b"")
        origin.routes["/v2/x.user.js"] = (200, None, BODY)
        assert cli.AdGuardCLI().install_userscript(origin.base + "/x.user.js")[0]
        assert [c[-1] for c in calls] == [origin.base + "/x.user.js", origin.base + "/v2/x.user.js"]


def test_connect_timeout_capped_by_deadline(monkeypatch):
    timeouts = []

    def connect(address, timeout, source_address=None):
        timeouts.append(timeout)
        raise ConnectionRefusedError

    monkeypatch.setattr(socket, "create_connection", connect)
    probe = userscript_relay._ProbeHandler(0.2)
    with pytest.raises(ConnectionRefusedError):
        probe._connect(("127.0.0.1", 9), 15)
    with pytest.raises(ConnectionRefusedError):
        userscript_relay._ProbeHandler(60)._connect(("127.0.0.1", 9), 0.2)
    assert 0 < timeouts[0] <= 0.2 and timeouts[1] == 0.2


def test_relay_log_keeps_secrets_out(server, fake_run, caplog):
    calls, _, _ = fake_run
    server.routes["/x.user.js?token=abc"] = (302, "/asset/1", b"")
    server.routes["/asset/1"] = (200, None, BODY)
    with caplog.at_level(logging.INFO, logger="adguard_tray.userscript_relay"):
        assert cli.AdGuardCLI().install_userscript(server.base + "/x.user.js?token=abc")[0]
    assert calls[1][-1].startswith("http://127.0.0.1:")
    assert f"Userscript {server.base}/x.user.js is redirected, relaying it from 127.0.0.1" in caplog.text
    for secret in ("token", "abc"):
        assert secret not in caplog.text


@pytest.mark.parametrize("body, named", [
    (HEADER, True),
    (b"\xef\xbb\xbf" + HEADER, True),
    (b" \t// \t==UserScript==\n\t// @downloadURL https://e.org/x.user.js\n  // ==/UserScript==\n", True),
    (b"// ==UserScript==\n// @downloadURL https://e.org/x.user.js\n", False),
    (b"// ==UserScript==\n" + b"// @name X\n" * 7000 + b"// @downloadURL https://e.org/x.user.js\n"
     b"// ==/UserScript==\n", False),
    (b"'use strict';\n// note\n" + HEADER, True),
    (b"x = '// ==UserScript=='\n// @downloadURL https://e.org/x.user.js\n// ==/UserScript==\n", False),
    (b"// ==UserScript==\n// @downloadURL https://e.org/x.user.js\nx = '// ==/UserScript=='\n", False),
    (b"// ==UserScript==\n// @name X // @downloadURL https://e.org/x.user.js\n// ==/UserScript==\n", False),
    (b"// ==/UserScript==\n" + HEADER, True),
], ids=["header", "bom", "indented", "unclosed", "beyond-scan", "after-lines", "open-mid-line",
        "close-mid-line", "key-mid-line", "stray-close"])
def test_names_download_url(body, named):
    assert userscript_relay._names_download_url(body) is named


def test_repeated_unclosed_header_is_cheap():
    start = time.monotonic()
    assert not userscript_relay._names_download_url(b"// ==UserScript==\n" * 200000)
    assert time.monotonic() - start < 1


def test_local_origin_follows_local_hop(server, fake_run):
    calls, _, _ = fake_run
    final = f"http://localhost:{server.server_address[1]}/v2/x.user.js"
    server.routes["/x.user.js"] = (302, final, b"")
    server.routes["/v2/x.user.js"] = (200, None, BODY)
    assert cli.AdGuardCLI().install_userscript(server.base + "/x.user.js")[0]
    assert [c[-1] for c in calls] == [server.base + "/x.user.js", final]


def test_relay_listens_on_loopback_only():
    srv = userscript_relay._RelayServer("/x.user.js", b"")
    try:
        assert srv.server_address[0] == "127.0.0.1"
    finally:
        srv.server_close()


def test_relay_matches_unquoted_path(server, monkeypatch):
    monkeypatch.setattr(userscript_relay, "_redirect_plan", lambda url, hops: None)
    server.routes["/x%7E1.user.js"] = (200, None, BODY)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with (userscript_relay._userscript_source(server.base + "/x%7E1.user.js") as relay,
          opener.open(relay.rsplit("/", 1)[0] + "/x~1.user.js", timeout=5) as resp):
        assert resp.read() == BODY


def test_bom_before_header_is_relayed(server, fake_run):
    calls, fetched, behaviour = fake_run
    behaviour["fetch"] = True
    server.routes["/x.user.js"] = (302, "/asset/1", b"")
    server.routes["/asset/1"] = (200, None, b"\xef\xbb\xbf" + BODY)
    assert cli.AdGuardCLI().install_userscript(server.base + "/x.user.js")[0]
    assert calls[1][-1].startswith("http://127.0.0.1:")
    assert fetched == [b"\xef\xbb\xbf" + BODY]


def test_relay_bind_failure_returns_first_failure(server, fake_run, monkeypatch):
    calls, _, _ = fake_run

    def no_bind(path, body):
        raise OSError("address in use")

    monkeypatch.setattr(userscript_relay, "_RelayServer", no_bind)
    server.routes["/x.user.js"] = (302, "/asset/1", b"")
    server.routes["/asset/1"] = (200, None, BODY)
    url = server.base + "/x.user.js"
    assert cli.AdGuardCLI().install_userscript(url) == _first_failure()
    assert [c[-1] for c in calls] == [url]


def test_probe_sends_user_agent(server, fake_run):
    server.routes["/x.user.js"] = (200, None, BODY)
    cli.AdGuardCLI().install_userscript(server.base + "/x.user.js")
    assert server.agents == [f"adguard-tray/{adguard_tray.__version__}"]


def test_probe_failure_log_keeps_secrets_out(fake_run, monkeypatch, caplog):
    def fail(self, req, *args, **kwargs):
        raise ValueError(f"cannot open {req.full_url}")

    monkeypatch.setattr(urllib.request.OpenerDirector, "open", fail)
    with caplog.at_level(logging.INFO, logger="adguard_tray.userscript_relay"):
        assert cli.AdGuardCLI().install_userscript(
            "https://user:pw@host.example/x.user.js?token=abc") == _first_failure()
    assert "Redirect probe for https://host.example/x.user.js failed: ValueError" in caplog.text
    for secret in ("user:", "pw@", "token", "abc", "cannot open"):
        assert secret not in caplog.text


def _leftover(before):
    """Threads started since `before`, except the test server's request handlers."""
    return [t for t in threading.enumerate() if t not in before and "process_request" not in t.name]


def test_header_drip_hits_deadline(fake_run, monkeypatch):
    calls, _, _ = fake_run
    monkeypatch.setenv("no_proxy", "*")
    monkeypatch.setattr(userscript_relay, "_RELAY_DEADLINE", 0.5)
    fds = len(os.listdir("/proc/self/fd"))
    with _raw_server(b"HTTP/1.1 302 Found\r\n", drip=b"X-Pad: " + b"a" * 200, interval=0.05) as raw:
        before = set(threading.enumerate())
        start = time.monotonic()
        assert cli.AdGuardCLI().install_userscript(raw + "/x.user.js") == _first_failure()
        assert time.monotonic() - start < 2
        assert _leftover(before) == []
    assert [c[-1] for c in calls] == [raw + "/x.user.js"]
    assert len(os.listdir("/proc/self/fd")) == fds


def test_silent_server_hits_deadline(fake_run, monkeypatch):
    calls, _, _ = fake_run
    monkeypatch.setenv("no_proxy", "*")
    monkeypatch.setattr(userscript_relay, "_RELAY_DEADLINE", 0.5)
    with socket.create_server(("127.0.0.1", 0)) as silent:
        url = f"http://127.0.0.1:{silent.getsockname()[1]}/x.user.js"
        start = time.monotonic()
        assert cli.AdGuardCLI().install_userscript(url) == _first_failure()
        assert time.monotonic() - start < 2
    assert [c[-1] for c in calls] == [url]


def test_stalling_redirect_chain_hits_deadline(server, fake_run, monkeypatch):
    calls, _, _ = fake_run
    monkeypatch.setattr(userscript_relay, "_RELAY_DEADLINE", 1.0)
    server.routes["/x.user.js"] = (302, "/h1", b"", 0.4)
    for i in range(1, 12):
        server.routes[f"/h{i}"] = (302, f"/h{i + 1}", b"", 0.4)
    url = server.base + "/x.user.js"
    before = set(threading.enumerate())
    start = time.monotonic()
    assert cli.AdGuardCLI().install_userscript(url) == _first_failure()
    assert time.monotonic() - start < 2.5
    assert len(server.seen) <= 4
    assert _leftover(before) == []
    assert [c[-1] for c in calls] == [url]


def test_stalling_local_client_does_not_delay_install(server, monkeypatch):
    clients, calls = [], []

    def stall_relay(args, timeout=15, stdin_data=None):
        calls.append(args)
        if len(calls) == 1:
            return FAIL
        host, port = args[-1].split("//")[1].split("/")[0].split(":")
        client = socket.create_connection((host, int(port)), timeout=5)
        clients.append(client)
        client.sendall(b"GET /")
        time.sleep(0.3)    # let the relay accept it
        return 0, "Userscript installed", ""

    monkeypatch.setattr(cli, "_run", stall_relay)
    server.routes["/x.user.js"] = (302, "/asset/1", b"")
    server.routes["/asset/1"] = (200, None, BODY)
    start = time.monotonic()
    try:
        assert cli.AdGuardCLI().install_userscript(server.base + "/x.user.js")[0]
        assert time.monotonic() - start < 3
    finally:
        for client in clients:
            client.close()
    assert len(calls) == 2


def _raw_get(url):
    p = urlsplit(url)
    with socket.create_connection((p.hostname, p.port), timeout=5) as sock:
        sock.sendall(f"GET {p.path} HTTP/1.0\r\n\r\n".encode())
        reply = b""
        while chunk := sock.recv(65536):
            reply += chunk
    return reply


def test_relay_wrong_path_sends_no_body(server, monkeypatch):
    monkeypatch.setattr(userscript_relay, "_redirect_plan", lambda url, hops: None)
    server.routes["/x.user.js"] = (200, None, BODY)
    with userscript_relay._userscript_source(server.base + "/x.user.js") as relay:
        for wrong in (relay.rsplit("/", 1)[0] + "/other.user.js", relay + ".bak"):
            reply = _raw_get(wrong)
            assert reply.startswith(b"HTTP/1.0 404") and HEADER not in reply


@pytest.mark.parametrize("head", [
    b"HTTP/1.0 200 OK\r\n\r\n" + BODY,
    b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n%x\r\n%s\r\n0\r\n\r\n" % (len(BODY), BODY),
], ids=["close", "chunked"])
def test_body_without_length_is_relayed(server, fake_run, head):
    calls, fetched, behaviour = fake_run
    behaviour["fetch"] = True
    with _raw_server(head) as raw:
        server.routes["/x.user.js"] = (302, raw + "/asset/1", b"")
        assert cli.AdGuardCLI().install_userscript(server.base + "/x.user.js")[0]
    assert calls[1][-1].startswith("http://127.0.0.1:") and fetched == [BODY]


def test_relay_name_ignores_query(server, fake_run):
    calls, _, _ = fake_run
    server.routes["/a.user.js?v=1/2"] = (302, "/asset/1", b"")
    server.routes["/asset/1"] = (200, None, BODY)
    assert cli.AdGuardCLI().install_userscript(server.base + "/a.user.js?v=1/2")[0]
    assert calls[1][-1].rpartition("/")[2] == "a.user.js"


@pytest.mark.parametrize("origin", ["http://a.example/x.user.js", "https://a.example/x.user.js"])
def test_https_hop_is_followed(origin):
    log = userscript_relay._RedirectLog(origin)
    req = urllib.request.Request(origin)
    new = log.redirect_request(req, io.BytesIO(b""), 302, "Found", {}, "https://b.example/y.user.js")
    assert new.full_url == "https://b.example/y.user.js"
    assert log.hops == ["https://b.example/y.user.js"]


def test_deadline_is_shared_across_hops(server, fake_run, monkeypatch):
    calls, _, _ = fake_run
    monkeypatch.setattr(userscript_relay, "_RELAY_DEADLINE", 1.0)
    # Hop 2 drips its header faster than the socket timeout, so only the shared deadline ends it.
    with _raw_server(b"HTTP/1.1 200 OK\r\n", drip=b"X-Pad: " + b"a" * 200, interval=0.1) as drip:
        server.routes["/x.user.js"] = (302, drip + "/asset/1", b"", 0.5)
        url = server.base + "/x.user.js"
        start = time.monotonic()
        assert cli.AdGuardCLI().install_userscript(url) == _first_failure()
        assert time.monotonic() - start < 1.3
    assert [c[-1] for c in calls] == [url]


def test_relay_install_is_quiet(server, fake_run, caplog, capfd):
    calls, fetched, behaviour = fake_run
    behaviour["fetch"] = True
    server.routes["/x.user.js"] = (302, "/asset/1", b"")
    server.routes["/asset/1"] = (200, None, BODY)
    with caplog.at_level(logging.DEBUG):
        assert cli.AdGuardCLI().install_userscript(server.base + "/x.user.js")[0]
    token = calls[1][-1].split("/")[3]
    assert fetched == [BODY] and token not in caplog.text
    assert capfd.readouterr().err == ""


def test_relay_client_disconnect_is_quiet(capfd):
    srv = userscript_relay._RelayServer("/x.user.js", b"x" * (32 * 1024 * 1024))
    before = set(threading.enumerate())
    threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True).start()
    try:
        with socket.create_connection(srv.server_address, timeout=5) as client:
            client.sendall(b"GET /x.user.js HTTP/1.0\r\n\r\n")
            assert client.recv(1)
            # Linger 0: close resets the connection while the relay is still writing.
            client.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
    finally:
        srv.shutdown()
        srv.server_close()
    for thread in set(threading.enumerate()) - before:
        thread.join(5)
    assert capfd.readouterr().err == ""


def test_expire_on_closed_socket():
    probe = userscript_relay._ProbeHandler(1)
    sock = socket.socket()
    sock.close()
    probe._expire(sock)
    assert probe.expired.is_set()
