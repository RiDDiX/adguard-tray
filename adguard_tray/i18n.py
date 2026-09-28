"""
Lightweight internationalisation.

Detects the language (config file first, then the system locale) and provides
a ``_t()`` translation function.  English is the default language; the other
languages live in ``locales/<code>.py`` as a ``STRINGS`` dict, and only the
active one is imported.  Falls back to the English key when no translation
exists.
"""

import importlib
import locale
import os

# Endonyms, never translated: someone stuck in the wrong language still finds their own.
LANGUAGES = {
    "en": "English",
    "de": "Deutsch",
    "es": "Español",
    "fr": "Français",
    "it": "Italiano",
    "ja": "日本語",
    "ko": "한국어",
    "nl": "Nederlands",
    "pl": "Polski",
    "pt": "Português (Brasil)",
    "ru": "Русский",
    "tr": "Türkçe",
    "uk": "Українська",
    "zh": "简体中文",
    "zh_TW": "繁體中文",
}

# ── Locale detection ──────────────────────────────────────────────────────

def _normalize(tag: str) -> str:
    """'de_DE.UTF-8' → 'de', 'pt_BR' → 'pt', 'zh_TW' / 'zh_HK' / 'zh-Hant' → 'zh_TW'."""
    tag = tag.strip().split(".")[0].split("@")[0].replace("-", "_")
    lang, _, region = tag.partition("_")
    lang = lang.lower()
    if lang == "zh" and {"tw", "hk", "mo", "hant"} & set(region.lower().split("_")):
        return "zh_TW"
    return lang


def _detect_language() -> str:
    """
    Return a language code based on config file, then system locale.
    Config file overrides system locale.
    Empty string in config means auto-detect.
    """
    # First, check config file
    try:
        import json
        from pathlib import Path
        config_file = Path.home() / ".config" / "adguard-tray" / "config.json"
        if config_file.exists():
            data = json.loads(config_file.read_text(encoding="utf-8"))
            lang = data.get("language", "")
            if isinstance(lang, str) and lang:  # "" = auto-detect
                return _normalize(lang)
    except Exception:
        pass

    # Fall back to system locale. LANGUAGE may list several ("de_DE:en"):
    # the first one we have wins.
    for var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        tags = [_normalize(t) for t in os.environ.get(var, "").split(":")]
        tags = [t for t in tags if t and t not in ("c", "posix")]
        if tags:
            return next((t for t in tags if t in LANGUAGES), "en")
    try:
        lang, _ = locale.getlocale()
        if lang:
            return _normalize(lang)
    except (ValueError, AttributeError):
        pass
    return "en"


def _load(code: str) -> dict[str, str]:
    if code == "en" or code not in LANGUAGES:
        return {}
    try:
        return importlib.import_module(f".locales.{code}", __package__).STRINGS
    except (ImportError, SyntaxError):     # a broken install still starts, in English
        return {}


_LANG = _detect_language()
_CURRENT: dict[str, str] = _load(_LANG)


def _t(key: str, *args: object) -> str:
    """Return the translated string, optionally formatted with *args*."""
    text = _CURRENT.get(key, key)
    if args:
        return text.format(*args)
    return text
