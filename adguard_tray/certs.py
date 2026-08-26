"""Install AdGuard's HTTPS filtering root CA into browser certificate stores.

`adguard-cli cert` adds the CA to the system trust store and, with
--firefox-profile, to one Firefox profile. Chromium-family browsers don't use
the system store: they read an NSS database, and AdGuard's own installer only
looks at ~/.pki/nssdb (plus the Chromium snap) and skips any database that
doesn't exist yet. Chromium ≥ M146 additionally prefers
~/.local/share/pki/nssdb, so a fresh Brave/Chrome/ungoogled-chromium install
ends up without the CA.

This module finds the installed CA and imports it into every NSS database it
can find – Chromium-family and Firefox-family alike, since both are plain NSS
sql databases.
"""

import configparser
import glob
import hashlib
import logging
import os
import shutil
import ssl
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from .i18n import _t

logger = logging.getLogger(__name__)

HOME = Path.home()

# Where `install_cert.sh` puts the CA (first existing dir wins, same order).
_SYSTEM_CERT_DIRS = (
    "/usr/local/share/ca-certificates",     # Debian/Ubuntu
    "/usr/share/pki/trust/anchors",         # openSUSE
    "/etc/pki/ca-trust/source/anchors",     # Fedora/RHEL
    "/etc/ca-certificates/trust-source/anchors",  # Arch
)
_EXTRA_CERT_DIRS = (
    str(HOME / ".local" / "share" / "adguard-cli"),
    "/opt/adguard-cli",
)

# certutil ships with adguard-cli, so the `nss` package is only a fallback.
_BUNDLED_CERTUTIL = "/opt/adguard-cli/certutil"

# Chromium-family databases. The first two are created when missing – that is
# what makes a browser that never had a client certificate work.
_CHROMIUM_DBS = (
    (HOME / ".pki" / "nssdb", True),
    (HOME / ".local" / "share" / "pki" / "nssdb", True),  # Chromium ≥ M146
)
_CHROMIUM_GLOBS = (
    str(HOME / "snap" / "*" / "current" / ".pki" / "nssdb"),
    str(HOME / ".var" / "app" / "*" / ".pki" / "nssdb"),        # Flatpak
    str(HOME / ".var" / "app" / "*" / "data" / "pki" / "nssdb"),
)

# Firefox-family profiles.ini locations (Gecko browsers share the format).
_FIREFOX_INIS = (
    str(HOME / ".mozilla" / "firefox" / "profiles.ini"),
    str(HOME / ".librewolf" / "profiles.ini"),
    str(HOME / ".waterfox" / "profiles.ini"),
    str(HOME / ".zen" / "profiles.ini"),
    str(HOME / "snap" / "firefox*" / "common" / ".mozilla" / "firefox" / "profiles.ini"),
    str(HOME / ".var" / "app" / "*" / ".mozilla" / "firefox" / "profiles.ini"),
    str(HOME / ".var" / "app" / "*" / ".librewolf" / "profiles.ini"),
)


@dataclass
class CertTarget:
    """One certificate store plus the result of importing into it."""
    name: str
    path: Path
    create: bool = False   # create the directory when it doesn't exist
    ok: bool = False
    error: str = ""


def certutil_path() -> str:
    """certutil from PATH, else the one shipped with adguard-cli."""
    found = shutil.which("certutil")
    if found:
        return found
    if os.access(_BUNDLED_CERTUTIL, os.X_OK):
        return _BUNDLED_CERTUTIL
    return ""


def _cert_info(path: Path) -> tuple[str, float] | None:
    """(common name, notAfter) of a PEM certificate, or None if unusable.

    Expired certificates are skipped: after regenerating the CA the old file
    often stays behind, and importing that one would trust nothing useful.
    """
    try:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.load_verify_locations(cafile=str(path))
        certs = ctx.get_ca_certs()
    except (ssl.SSLError, OSError, ValueError) as exc:
        logger.debug("Not a readable PEM certificate: %s (%s)", path, exc)
        return None
    for cert in certs:
        cn = ""
        for rdn in cert.get("subject", ()):
            for key, value in rdn:
                if key == "commonName":
                    cn = value
        not_after = cert.get("notAfter", "")
        try:
            expires = ssl.cert_time_to_seconds(not_after) if not_after else 0.0
        except ValueError:
            expires = 0.0
        if expires and expires < time.time():
            logger.debug("Certificate expired, skipping: %s", path)
            continue
        if cn:
            return cn, expires
    return None


def find_ca() -> tuple[Path | None, str]:
    """Locate the AdGuard root CA to install. Returns (path, common name).

    Several anchors can carry an AdGuard CN – a regenerated CA, a leftover from
    another AdGuard product – so the newest valid one wins instead of whichever
    directory happens to be searched first.
    """
    best: tuple[float, Path, str] | None = None
    for directory in (*_SYSTEM_CERT_DIRS, *_EXTRA_CERT_DIRS):
        base = Path(directory)
        if not base.is_dir():
            continue
        for candidate in sorted([*base.glob("*.crt"), *base.glob("*.pem")]):
            info = _cert_info(candidate)
            if not info:
                continue
            cn, expires = info
            if "adguard" not in cn.lower():
                continue
            try:
                mtime = candidate.stat().st_mtime
            except OSError:
                mtime = 0.0
            rank = max(expires, mtime)
            if best is None or rank > best[0]:
                best = (rank, candidate, cn)
    if best:
        logger.info("Using AdGuard CA %s (%s)", best[1], best[2])
        return best[1], best[2]
    return None, ""


def _firefox_profiles() -> list[tuple[str, Path]]:
    """(label, profile dir) for every Gecko profile found."""
    profiles: list[tuple[str, Path]] = []
    for pattern in _FIREFOX_INIS:
        for ini_path in sorted(glob.glob(pattern)):
            ini = Path(ini_path)
            # interpolation=None: a '%' in a profile path is data, not a format
            parser = configparser.ConfigParser(interpolation=None)
            try:
                parser.read(ini, encoding="utf-8")
            except (OSError, configparser.Error, UnicodeDecodeError) as exc:
                logger.warning("Could not read %s: %s", ini, exc)
                continue
            for section in parser.sections():
                if not section.lower().startswith("profile"):
                    continue
                rel = parser.get(section, "Path", fallback="")
                if not rel:
                    continue
                is_relative = parser.get(section, "IsRelative", fallback="1") == "1"
                path = (ini.parent / rel) if is_relative else Path(rel)
                if path.is_dir():
                    profiles.append((f"{_browser_label(ini)}: {path.name}", path))
    return profiles


def _browser_label(ini: Path) -> str:
    parts = {p.lower() for p in ini.parts}
    for marker, label in (
        ("librewolf", "LibreWolf"), (".waterfox", "Waterfox"), (".zen", "Zen"),
    ):
        if marker in parts or any(marker in p.lower() for p in ini.parts):
            return label
    return "Firefox"


def nss_targets() -> list[CertTarget]:
    """Every NSS database we can import into, browser-family agnostic."""
    targets = [
        CertTarget(_t("Chromium-based browsers"), path, create=True)
        for path, _ in _CHROMIUM_DBS
    ]
    for pattern in _CHROMIUM_GLOBS:
        for found in sorted(glob.glob(pattern)):
            path = Path(found)
            parts = path.parts
            # ~/.var/app/com.brave.Browser/… and ~/snap/chromium/current/…
            if "app" in parts:
                owner = parts[parts.index("app") + 1]
            elif "snap" in parts:
                owner = parts[parts.index("snap") + 1]
            else:
                owner = path.name
            targets.append(CertTarget(str(owner), path))
    targets += [CertTarget(label, path) for label, path in _firefox_profiles()]
    return targets


def _nickname_count(certutil: str, db: Path, nickname: str) -> int:
    """How often *nickname* is in the database (-L -n exits 0 even if absent)."""
    proc = subprocess.run(
        [certutil, "-d", f"sql:{db}", "-L"],
        capture_output=True, timeout=30, check=False,
    )
    out = proc.stdout.decode("utf-8", errors="replace")
    return sum(1 for line in out.splitlines() if line.startswith(nickname))


def _has_fingerprint(certutil: str, db: Path, fingerprint: str) -> bool:
    """True when a certificate with this SHA-256 fingerprint is in the store.

    NSS keys on the certificate, not the nickname: re-adding the same DER under
    a new nickname keeps the old one, so checking the nickname alone would call
    a perfectly good import a failure.
    """
    if not fingerprint:
        return False
    proc = subprocess.run(
        [certutil, "-d", f"sql:{db}", "-L", "-a"],
        capture_output=True, timeout=30, check=False,
    )
    return fingerprint in _fingerprints(proc.stdout)


def _fingerprints(pem_bundle: bytes) -> set[str]:
    """SHA-256 fingerprints of every certificate in a PEM bundle."""
    found = set()
    marker = b"-----BEGIN CERTIFICATE-----"
    end = b"-----END CERTIFICATE-----"
    blob = pem_bundle
    while marker in blob and end in blob:
        start = blob.index(marker)
        stop = blob.index(end) + len(end)
        try:
            der = ssl.PEM_cert_to_DER_cert(blob[start:stop].decode("ascii"))
            found.add(hashlib.sha256(der).hexdigest())
        except (ValueError, UnicodeDecodeError):
            pass
        blob = blob[stop:]
    return found


def _export_cert(certutil: str, db: Path, nickname: str) -> bytes:
    """The stored certificate as PEM, so a failed replacement can be undone."""
    proc = subprocess.run(
        [certutil, "-d", f"sql:{db}", "-L", "-n", nickname, "-a"],
        capture_output=True, timeout=30, check=False,
    )
    return proc.stdout if proc.returncode == 0 and b"BEGIN CERTIFICATE" in proc.stdout else b""


def _add_cert(certutil: str, db: Path, nickname: str, pem_file: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        [certutil, "-d", f"sql:{db}", "-A", "-n", nickname, "-t", "C,,", "-i", str(pem_file)],
        capture_output=True, timeout=30, check=False,
    )
    if proc.returncode == 0:
        return True, ""
    return False, proc.stderr.decode("utf-8", errors="replace").strip()[:200]


def install_ca(ca_path: Path, nickname: str, targets: list[CertTarget]) -> list[CertTarget]:
    """Import *ca_path* into every target. Never raises; results are per target.

    Importing the same nickname twice leaves two entries behind, so existing
    ones are removed first – otherwise a regenerated CA leaves a stale copy
    the browser may keep using.
    """
    try:
        fingerprint = next(iter(_fingerprints(ca_path.read_bytes())), "")
    except OSError:
        fingerprint = ""
    certutil = certutil_path()
    if not certutil:
        for target in targets:
            target.ok = False
            target.error = _t("certutil not found – install the 'nss' package")
        return targets

    try:
        home_owner = HOME.stat().st_uid
    except OSError:
        home_owner = os.geteuid()
    if os.geteuid() != home_owner or (
        os.geteuid() == 0 and (os.environ.get("SUDO_USER") or os.environ.get("PKEXEC_UID"))
    ):
        # Started via sudo/pkexec/su: the stores we would write belong to
        # somebody else, and the user's browsers would still not trust the CA.
        for target in targets:
            target.ok = False
            target.error = _t("Run this without sudo/pkexec – it installs into your own browser profiles")
        return targets

    for target in targets:
        try:
            if not target.path.is_dir():
                if not target.create:
                    target.error = _t("not found")
                    continue
                target.path.mkdir(parents=True, exist_ok=True)

            # Keep the entry we are about to replace, so a failed import
            # doesn't leave the browser with no certificate at all.
            backup = _export_cert(certutil, target.path, nickname)

            # certutil -D removes one entry per call and fails once none is left.
            for _ in range(20):
                purge = subprocess.run(
                    [certutil, "-d", f"sql:{target.path}", "-D", "-n", nickname],
                    capture_output=True, timeout=30, check=False,
                )
                if purge.returncode != 0:
                    break
            if _nickname_count(certutil, target.path, nickname):
                target.error = _t("could not remove the previous certificate")
                continue

            ok, err = _add_cert(certutil, target.path, nickname, ca_path)
            if ok and (_nickname_count(certutil, target.path, nickname) == 1
                       or _has_fingerprint(certutil, target.path, fingerprint)):
                target.ok = True
                continue

            target.error = err or _t("certificate not found after import")
            if backup:
                restored = target.path / "adguard-tray-restore.pem"
                try:
                    restored.write_bytes(backup)
                    _add_cert(certutil, target.path, nickname, restored)
                finally:
                    restored.unlink(missing_ok=True)
                logger.warning("Import failed for %s, restored the previous certificate",
                               target.path)
        except (OSError, subprocess.SubprocessError) as exc:
            target.error = str(exc)[:200]
            logger.warning("Certificate import failed for %s: %s", target.path, exc)
    return targets


def install_into_browsers() -> tuple[bool, str, list[CertTarget]]:
    """Find the CA and import it everywhere. Returns (ok, message, targets)."""
    ca_path, cn = find_ca()
    if not ca_path:
        return False, _t(
            "AdGuard's certificate was not found. Generate it first."
        ), []
    targets = nss_targets()
    if not targets:
        return False, _t("No browser certificate stores found."), []
    install_ca(ca_path, cn, targets)
    done = sum(1 for t in targets if t.ok)
    if not done:
        return False, _t("Certificate could not be installed in any browser."), targets
    return True, _t("Certificate installed for {} of {} stores.", done, len(targets)), targets
