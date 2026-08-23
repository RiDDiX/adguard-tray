"""
Shared allowlist logic for website exceptions.

Manages @@||domain^$important,document rules in AdGuard CLI's user.txt file.
Used by both the standalone ExceptionsDialog and the ExceptionsTab in the Manager window.
"""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

USER_RULES_FILE = Path.home() / ".local" / "share" / "adguard-cli" / "user.txt"

ALLOWLIST_RE = re.compile(r"^@@\|\|(.+?)\^\$important,document\s*$")
_DOMAIN_RE = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$"
)
_IP_RE = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")


def is_valid_domain(text: str) -> bool:
    if _IP_RE.match(text):
        return all(int(o) <= 255 for o in text.split("."))
    return len(text) <= 253 and bool(_DOMAIN_RE.match(text))


def domain_to_rule(domain: str) -> str:
    return f"@@||{domain}^$important,document"


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


def save_user_rules(domains: list[str], other_lines: list[str]) -> tuple[bool, str]:
    """Write user.txt back: other_lines first, then allowlist rules."""
    try:
        lines = list(other_lines)
        for d in sorted(domains):
            lines.append(domain_to_rule(d))
        text = "\n".join(lines)
        if text and not text.endswith("\n"):
            text += "\n"
        USER_RULES_FILE.write_text(text, encoding="utf-8")
        return True, ""
    except OSError as exc:
        logger.error("Failed to save user rules: %s", exc)
        return False, str(exc)
