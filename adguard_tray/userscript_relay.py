# adguard-cli (seen in 1.5.1) does not follow redirects; remove the relay once it does.

import contextlib
import http.server
import ipaddress
import logging
import re
import secrets
import socket
import socketserver
import threading
import time
import urllib.error
import urllib.request
from urllib.parse import unquote, urlsplit, urlunsplit

from . import __version__

logger = logging.getLogger(__name__)

_USERSCRIPT_SUFFIXES = (".user.js", ".meta.js", ".user.css")
_RELAY_MAX = 16 * 1024 * 1024
_PROBE_TIMEOUT = 15
_RELAY_DEADLINE = 30
_META_SCAN = 64 * 1024
_META_OPEN_RE = re.compile(rb"^[ \t]*//[ \t]*==UserScript==", re.M)
_META_CLOSE_RE = re.compile(rb"^[ \t]*//[ \t]*==/UserScript==", re.M)
_DOWNLOAD_URL_RE = re.compile(rb"^[ \t]*//[ \t]*@downloadURL[ \t]+\S", re.M)


def _log_url(url: str) -> str:
    """URL without credentials, query or fragment, safe for the log file."""
    try:
        p = urlsplit(url)
    except ValueError:
        return "<unparsable URL>"
    return urlunsplit((p.scheme, p.netloc.rpartition("@")[2], p.path, "", ""))


def _cli_fetchable(url: str) -> bool:
    """URL that `adguard-cli userscripts install` accepts and downloads itself."""
    p = urlsplit(url)
    return p.scheme in ("http", "https") and "#" not in url and p.path.endswith(_USERSCRIPT_SUFFIXES)


def _redirect_plan(url: str, hops: list[str]) -> str | None:
    """URL to hand adguard-cli after probing `url` went through redirect `hops` (final last).

    None: relay the downloaded body from 127.0.0.1.
    """
    if not hops or hops[-1] == url:
        return url
    if _cli_fetchable(hops[-1]):
        return hops[-1]
    return None if _cli_fetchable(url) else url


def _names_download_url(body: bytes) -> bool:
    """Whether the userscript header sets @downloadURL, so the CLI never stores the relay URL as its source."""
    bom = b"\xef\xbb\xbf"
    head = body[:len(bom) + _META_SCAN].removeprefix(bom)[:_META_SCAN]
    start = _META_OPEN_RE.search(head)
    end = start and _META_CLOSE_RE.search(head, start.end())
    return bool(end and _DOWNLOAD_URL_RE.search(head, start.end(), end.start()))


def _global_address(host: str) -> bool:
    return ipaddress.ip_address(host).is_global


class _RedirectLog(urllib.request.HTTPRedirectHandler):
    def __init__(self, url: str) -> None:
        self.url, self.hops = url, []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # urllib reads the whole redirect body after this returns; a closed response reads as b"".
        fp.close()
        # Refused before the hop is contacted; urllib itself would follow ftp: too.
        if not newurl.startswith(("http://", "https://")) or (
                urlsplit(self.url).scheme == "https" and newurl.startswith("http://")):
            raise urllib.error.HTTPError(newurl, code, "Refused redirect", headers, fp)
        self.hops.append(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class _ProbeHandler(urllib.request.HTTPSHandler, urllib.request.HTTPHandler):
    """HTTP(S) handler whose connections are shut down once the probe's wall-clock limit is over."""

    def __init__(self, seconds: float) -> None:
        super().__init__()
        self.deadline = time.monotonic() + seconds
        self.expired = threading.Event()
        self.origin_global = None
        self._watched = []

    def do_open(self, http_class, req, **kwargs):
        def connection(*args, **kw):
            conn = http_class(*args, **kw)
            # Private http.client API; the deadline tests notice if a Python release drops it.
            conn._create_connection = self._connect
            return conn
        return super().do_open(connection, req, **kwargs)

    def _connect(self, address, timeout, source_address=None):
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("redirect probe over time limit")
        # Name resolution inside create_connection is not bounded by the deadline.
        sock = socket.create_connection(address, min(timeout, remaining), source_address)
        try:
            # The peer, not the URL: urllib unquotes the host and names may resolve to local addresses.
            peer_global = _global_address(sock.getpeername()[0])
            if self.origin_global is None:
                self.origin_global = peer_global
            elif self.origin_global and not peer_global:
                raise ConnectionRefusedError("redirect to a local address")
        except BaseException:
            sock.close()
            raise
        watch = sock.dup()    # ssl detaches `sock`; shutting down a duplicate still ends the connection
        timer = threading.Timer(self.deadline - time.monotonic(), self._expire, (watch,))
        self._watched.append((watch, timer))
        timer.start()
        return sock

    def _expire(self, sock) -> None:
        self.expired.set()
        with contextlib.suppress(OSError):
            sock.shutdown(socket.SHUT_RDWR)

    def close(self) -> None:
        for watch, timer in self._watched:
            timer.cancel()
            timer.join()
            watch.close()


class _RelayHandler(http.server.BaseHTTPRequestHandler):
    timeout = 10

    def do_GET(self) -> None:
        if unquote(self.path) != unquote(self.server.relay_path):
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Length", str(len(self.server.relay_body)))
        self.end_headers()
        self.wfile.write(self.server.relay_body)

    def log_message(self, format, *args) -> None:
        pass


class _RelayServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # A client that stalls must not hold up shutdown().
    daemon_threads, block_on_close = True, False

    def __init__(self, path: str, body: bytes) -> None:
        self.relay_path, self.relay_body = path, body
        super().__init__(("127.0.0.1", 0), _RelayHandler)

    def handle_error(self, request, client_address) -> None:
        pass    # a broken download is reported by the CLI itself


@contextlib.contextmanager
def _userscript_source(url: str):
    """Yield the URL `adguard-cli userscripts install` gets for `url`."""
    body = b""
    # The socket timeout bounds each read only, not a server that drips bytes or stalls every hop.
    probe = _ProbeHandler(_RELAY_DEADLINE)
    try:
        log = _RedirectLog(url)
        request = urllib.request.Request(url, headers={"User-Agent": f"adguard-tray/{__version__}"})
        with urllib.request.build_opener(probe, log).open(request, timeout=_PROBE_TIMEOUT) as resp:
            target = _redirect_plan(url, log.hops)
            if target is None:
                body = bytearray()
                while chunk := resp.read1(64 * 1024):
                    body += chunk
                    if len(body) > _RELAY_MAX:
                        raise ValueError("userscript body over size limit")
                if probe.expired.is_set():
                    raise TimeoutError("redirect probe over time limit")
                length = resp.headers.get("Content-Length")
                if (length is not None and int(length) != len(body)) or not _names_download_url(body):
                    target = url
    except Exception as exc:
        # Advisory only: the CLI then reports the problem itself.
        logger.info("Redirect probe for %s failed: %s", _log_url(url), type(exc).__name__)
        target = url
    finally:
        probe.close()
    if target is not None:
        yield target
        return
    # The CLI takes the script id from the last segment; the token keeps other local processes out.
    path = f"/{secrets.token_urlsafe()}/{urlsplit(url).path.rpartition('/')[2]}"
    try:
        server = _RelayServer(path, body)
    except OSError:
        yield url
        return
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.1}, daemon=True)
    thread.start()
    try:
        logger.info("Userscript %s is redirected, relaying it from 127.0.0.1", _log_url(url))
        yield f"http://127.0.0.1:{server.server_address[1]}{path}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
