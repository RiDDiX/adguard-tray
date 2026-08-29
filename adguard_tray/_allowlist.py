"""
Shared allowlist logic for website exceptions.

Manages @@||domain^$important,document rules in AdGuard CLI's user.txt file.
Used by both the standalone ExceptionsDialog and the ExceptionsTab in the Manager window.
"""

import logging
import os
import re
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

USER_RULES_FILE = Path.home() / ".local" / "share" / "adguard-cli" / "user.txt"

ALLOWLIST_RE = re.compile(r"^@@\|\|(.+?)\^\$important,document\s*$")
_DOMAIN_RE = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$"
)
_IP_RE = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")


def write_atomic(path: Path, text: str) -> None:
    """Write via a temp file + rename so a failed write can't truncate the original.

    Symlinks are resolved first – os.replace would otherwise replace the link
    itself (dotfile setups symlink these files).
    """
    target = Path(os.path.realpath(path))
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        mode = target.stat().st_mode & 0o777
    except OSError:
        mode = 0o600  # these files can hold browsing-related rules
    fd, tmp_name = tempfile.mkstemp(dir=target.parent, prefix=target.name + ".", suffix=".tmp")
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, mode)
        os.replace(tmp, target)
    except OSError:
        tmp.unlink(missing_ok=True)
        raise


def is_valid_domain(text: str) -> bool:
    if _IP_RE.match(text):
        return all(int(o) <= 255 for o in text.split("."))
    return len(text) <= 253 and bool(_DOMAIN_RE.match(text))


def domain_to_rule(domain: str) -> str:
    return f"@@||{domain}^$important,document"


def add_rule_line(rule: str) -> tuple[bool, str]:
    """Append a raw filter rule to user.txt, keeping every existing line.

    save_user_rules() rewrites the file from the allowlist it manages, so a
    plain blocking rule has to be appended separately.
    """
    try:
        existing = USER_RULES_FILE.read_text(encoding="utf-8") if USER_RULES_FILE.exists() else ""
    except (OSError, ValueError) as exc:
        logger.warning("Could not read user rules: %s", exc)
        return False, str(exc)
    lines = existing.splitlines()
    if any(line.strip() == rule for line in lines):
        return True, ""
    lines.append(rule)
    try:
        write_atomic(USER_RULES_FILE, "\n".join(lines) + "\n")
    except OSError as exc:
        logger.error("Failed to add rule: %s", exc)
        return False, str(exc)
    return True, ""


def load_user_rules() -> tuple[list[str], list[str]]:
    """Load user.txt and split into (allowlist_domains, other_lines).

    Returns the domain part of each allowlist rule and preserves
    all non-allowlist lines (comments, other rules) unchanged.
    Raises OSError (or UnicodeDecodeError) if the file exists but can't be
    read – callers must not save (and thereby overwrite) in that case.
    """
    domains: list[str] = []
    other_lines: list[str] = []
    if not USER_RULES_FILE.exists():
        return domains, other_lines
    for line in USER_RULES_FILE.read_text(encoding="utf-8").splitlines():
        m = ALLOWLIST_RE.match(line)
        if m:
            domains.append(m.group(1))
        else:
            other_lines.append(line)
    return domains, other_lines


def save_user_rules(
    domains: list[str], other_lines: list[str], loaded: list[str] | None = None
) -> tuple[bool, str]:
    """Write user.txt back: other lines first, then the allowlist rules.

    The file is re-read right before writing and merged with the caller's list:
    *domains* is what the UI shows, *loaded* what it showed when it was loaded.
    Entries that appeared on disk since then (a second window, adguard-cli, an
    editor) are kept, entries the user removed stay removed. It narrows the
    race, it does not close it: an append between the re-read and the rename is
    still lost.
    """
    try:
        if USER_RULES_FILE.exists():
            try:
                disk_domains, other_lines = load_user_rules()
            except (OSError, ValueError) as exc:
                logger.warning("Could not re-read user rules before saving: %s", exc)
                return False, str(exc)
            removed = set(loaded or []) - set(domains)
            merged = (set(domains) | set(disk_domains)) - removed
        else:
            merged = set(domains)
        lines = list(other_lines)
        for d in sorted(merged):
            lines.append(domain_to_rule(d))
        text = "\n".join(lines)
        if text and not text.endswith("\n"):
            text += "\n"
        write_atomic(USER_RULES_FILE, text)
        return True, ""
    except OSError as exc:
        logger.error("Failed to save user rules: %s", exc)
        return False, str(exc)
