"""Check for a newer adguard-tray release and, where we own the files, install it.

adguard-tray is installed in three ways: as the AUR package, through
install.sh into ~/.local/lib/adguard-tray, or run straight from a checkout.
Only the second one is ours to replace. Files that belong to pacman have to be
updated by pacman, otherwise the package database and the next system upgrade
disagree with what is on disk, and a checkout belongs to git.
"""

import json
import logging
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from . import __version__
from .i18n import _t

logger = logging.getLogger(__name__)

REPO = "RiDDiX/adguard-tray"
LATEST_URL = f"https://api.github.com/repos/{REPO}/releases/latest"
RELEASES_PAGE = f"https://github.com/{REPO}/releases"
USER_AGENT = f"adguard-tray/{__version__}"

LOCAL_LIB = Path.home() / ".local" / "lib" / "adguard-tray"
_AUR_HELPERS = ("paru", "yay", "pikaur", "trizen")

# A release is ~200 KB. The caps are what an update may cost at worst; /tmp is
# tmpfs on Arch, so an unpacked archive costs RAM.
DOWNLOAD_TIMEOUT = 30           # per socket read
DOWNLOAD_DEADLINE = 120         # for the whole download
MAX_TARBALL_BYTES = 32 * 1024 * 1024
MAX_EXTRACTED_BYTES = 64 * 1024 * 1024

# A tag we are willing to build a download URL from.
_TAG_RE = re.compile(r"^\d{1,6}(\.\d{1,6}){0,3}$")


@dataclass
class Release:
    version: str = ""
    url: str = RELEASES_PAGE


@dataclass
class Install:
    """How this copy of adguard-tray got onto the machine."""
    kind: str = "unknown"      # pacman | local | source | unknown
    root: Path | None = None   # directory holding the adguard_tray package
    package: str = ""          # pacman package name, when it owns us

    @property
    def can_self_update(self) -> bool:
        return self.kind == "local"


def parse_version(text: str) -> tuple[int, ...]:
    """(1, 8, 1) for "v1.8.1". Trailing non-numeric parts are ignored."""
    parts: list[int] = []
    for chunk in re.split(r"[._-]", text.strip().lstrip("vV")):
        match = re.match(r"^(\d+)", chunk)
        if not match:
            break
        parts.append(int(match.group(1)))
    return tuple(parts)


def is_newer(candidate: str, current: str) -> bool:
    left, right = parse_version(candidate), parse_version(current)
    if not left or not right:
        return False
    return left > right


def package_dir() -> Path:
    return Path(__file__).resolve().parent


def aur_helper() -> str:
    for helper in _AUR_HELPERS:
        if shutil.which(helper):
            return helper
    return ""


def detect_install() -> Install:
    """Work out who owns the files we are running from."""
    root = package_dir().parent
    marker = package_dir() / "main.py"

    pacman = shutil.which("pacman")
    if pacman:
        try:
            result = subprocess.run([pacman, "-Qoq", str(marker)],
                                    capture_output=True, text=True, timeout=10)
        except (OSError, subprocess.SubprocessError) as exc:
            logger.debug("pacman -Qoq failed: %s", exc)
        else:
            name = result.stdout.strip().splitlines()
            if result.returncode == 0 and name:
                return Install(kind="pacman", root=root, package=name[-1].strip())

    try:
        same = root.samefile(LOCAL_LIB)
    except OSError:
        same = False
    if same:
        return Install(kind="local", root=root)

    if (root / ".git").is_dir():
        return Install(kind="source", root=root)
    return Install(kind="unknown", root=root)


def update_command(install: Install) -> str:
    """The command a user would run to update this installation."""
    if install.kind == "pacman":
        helper = aur_helper()
        package = install.package or "adguard-tray"
        return f"{helper} -Syu {package}" if helper else f"makepkg -si  # {package}"
    if install.kind == "source":
        return "git pull && bash install.sh"
    if install.kind == "local":
        return "bash install.sh"
    return ""


def latest_release(timeout: int = 10) -> tuple[Release | None, str]:
    """Ask GitHub for the newest release. Returns (release, error message)."""
    request = urllib.request.Request(LATEST_URL, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
    })
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read(1024 * 1024).decode("utf-8"))
    except urllib.error.HTTPError as exc:
        remaining = ""
        try:
            remaining = exc.headers.get("X-RateLimit-Remaining", "")
        except AttributeError:
            pass
        if exc.code == 429 or (exc.code == 403 and remaining == "0"):
            return None, _t("GitHub is rate limiting this address. Try again later.")
        return None, _t("GitHub returned {}.", f"HTTP {exc.code}")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return None, _t("No connection to GitHub: {}", getattr(exc, "reason", exc))
    except (ValueError, UnicodeDecodeError) as exc:
        return None, _t("Unexpected answer from GitHub: {}", exc)

    if not isinstance(data, dict):
        return None, _t("Unexpected answer from GitHub: {}", type(data).__name__)
    tag = str(data.get("tag_name") or "").strip().lstrip("vV")
    # The tag ends up in a download URL, so only a plain version is accepted.
    if not _TAG_RE.match(tag):
        return None, _t("Unexpected answer from GitHub: {}", f"tag_name={tag!r}")
    page = str(data.get("html_url") or "")
    if not page.startswith(f"https://github.com/{REPO}/"):
        page = RELEASES_PAGE            # the answer does not get to pick the link
    return Release(version=tag, url=page), ""


def _archive_url(version: str) -> str:
    """Where a release tarball lives. Built here, never taken from an answer."""
    return f"https://github.com/{REPO}/archive/refs/tags/v{version}.tar.gz"


def _download(url: str, target: Path) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    deadline = time.monotonic() + DOWNLOAD_DEADLINE
    try:
        with urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT) as response, \
                target.open("wb") as handle:
            written = 0
            while True:
                chunk = response.read(64 * 1024)
                if not chunk:
                    break
                written += len(chunk)
                if written > MAX_TARBALL_BYTES:
                    return _t("The download is larger than expected – aborted.")
                # The socket timeout is per read; a server trickling bytes would
                # otherwise keep this worker alive forever.
                if time.monotonic() > deadline:
                    return _t("Download failed: {}", "timeout")
                handle.write(chunk)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return _t("Download failed: {}", getattr(exc, "reason", exc))
    return ""


def _check_members(tar: tarfile.TarFile, into: Path) -> str:
    """Refuse anything but plain files and directories that stay inside `into`.

    A symlink member is enough to defeat a name-only check: extract the link
    first, then a file "through" it, and the write lands wherever the link
    points. Sizes are summed here as well – `filter="data"` does not cap them,
    and /tmp is RAM on Arch.
    """
    base = into.resolve()
    total = 0
    for member in tar.getmembers():
        if not (member.isfile() or member.isdir()):
            return _t("The archive contains unexpected paths – aborted.")
        destination = (base / member.name).resolve()
        if destination != base and not destination.is_relative_to(base):
            return _t("The archive contains unexpected paths – aborted.")
        total += max(0, member.size)
        if total > MAX_EXTRACTED_BYTES:
            return _t("The download is larger than expected – aborted.")
    return ""


def _extract(archive: Path, into: Path) -> str:
    into.mkdir(parents=True, exist_ok=True)
    try:
        with tarfile.open(archive, "r:gz") as tar:
            error = _check_members(tar, into)
            if error:
                return error
            try:
                tar.extractall(into, filter="data")
            except TypeError:                          # Python < 3.11.4
                tar.extractall(into)                   # noqa: S202 – checked above
    except (tarfile.TarError, OSError, ValueError) as exc:
        return _t("Could not unpack the download: {}", exc)
    return ""


def _extracted_package(root: Path) -> Path | None:
    """The adguard_tray package inside an extracted release tarball."""
    for candidate in sorted(root.glob("*/adguard_tray/__init__.py")):
        return candidate.parent
    return None


def _version_of(package: Path) -> str:
    try:
        text = (package / "__init__.py").read_text(encoding="utf-8")
    except OSError:
        return ""
    match = re.search(r"__version__\s*=\s*[\"']([^\"']+)[\"']", text)
    return match.group(1) if match else ""


def _sweep(root: Path) -> None:
    """Remove staging and backup directories a killed run left behind."""
    for pattern in (".adguard_tray.new-*", ".adguard_tray.old-*", ".adguard-tray.py.new-*"):
        for leftover in root.glob(pattern):
            if leftover.is_dir():
                shutil.rmtree(leftover, ignore_errors=True)
            else:
                leftover.unlink(missing_ok=True)


def self_update(release: Release, install: Install | None = None) -> tuple[bool, str]:
    """Replace a ~/.local install with *release*. Returns (ok, message).

    The extracted tree has to carry the version we asked for; otherwise a
    redirected or stale download would be installed without anyone noticing.
    """
    install = install or detect_install()
    if not install.can_self_update or install.root is None:
        return False, _t("This installation is managed elsewhere: {}",
                         update_command(install) or install.kind)
    if not os.access(install.root, os.W_OK):
        return False, _t("No permission to write to {}", str(install.root))

    if not _TAG_RE.match(release.version):
        return False, _t("Unexpected answer from GitHub: {}", release.version)
    _sweep(install.root)
    url = _archive_url(release.version)
    with tempfile.TemporaryDirectory(prefix="adguard-tray-update-") as tmp:
        work = Path(tmp)
        archive = work / "release.tar.gz"
        error = _download(url, archive)
        if error:
            return False, error
        error = _extract(archive, work / "src")
        if error:
            return False, error

        new_package = _extracted_package(work / "src")
        if new_package is None:
            return False, _t("The download does not contain adguard-tray.")
        found = _version_of(new_package)
        if found != release.version:
            return False, _t("The download says version {} instead of {} – aborted.",
                             found or "?", release.version)

        target = install.root / "adguard_tray"
        staged = install.root / f".adguard_tray.new-{os.getpid()}"
        backup = install.root / f".adguard_tray.old-{int(time.time())}"
        try:
            shutil.rmtree(staged, ignore_errors=True)
            shutil.copytree(new_package, staged)
            if target.exists():
                os.replace(target, backup)
            os.replace(staged, target)
        except BaseException as exc:   # including Ctrl-C from `--update`
            shutil.rmtree(staged, ignore_errors=True)
            if backup.exists() and not target.exists():
                try:
                    os.replace(backup, target)          # put the old one back
                except OSError:
                    logger.exception("Could not restore the previous version")
                    # The backup stays on disk: it is the only copy left.
                    return False, _t("Update failed and the old version could not be "
                                     "restored. Restore it from {} or reinstall with: {}",
                                     str(backup), "bash install.sh")
            shutil.rmtree(backup, ignore_errors=True)
            if not isinstance(exc, OSError):
                raise
            return False, _t("Update failed: {}", exc)
        # Only now is the old copy expendable.
        shutil.rmtree(backup, ignore_errors=True)

        launcher = new_package.parent / "adguard-tray.py"
        if launcher.is_file():
            try:
                # In-place copy would leave a truncated entry point on a crash.
                spare = install.root / f".adguard-tray.py.new-{os.getpid()}"
                shutil.copy2(launcher, spare)
                os.replace(spare, install.root / "adguard-tray.py")
            except OSError as exc:      # the package alone is enough to run
                logger.warning("Could not update the launcher: %s", exc)

    return True, _t("Version {} installed. Restart adguard-tray to use it.", release.version)


def check(timeout: int = 10) -> tuple[Release | None, bool, str]:
    """(release, newer, error) – one call for the UI and the command line."""
    release, error = latest_release(timeout=timeout)
    if release is None:
        return None, False, error
    return release, is_newer(release.version, __version__), ""
