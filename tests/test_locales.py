import importlib
import importlib.util

import pytest

from adguard_tray.i18n import LANGUAGES

CODES = [c for c in LANGUAGES if importlib.util.find_spec(f"adguard_tray.locales.{c}")]

# Korean puts the numbers in the other order with indexed fields: "{1}개 중 {0}개".
INDEXED_FIELDS = {("ko", "Certificate installed for {} of {} stores.")}


def _strings(code):
    return importlib.import_module(f"adguard_tray.locales.{code}").STRINGS


def test_every_language_but_english_has_a_module():
    assert set(LANGUAGES) - set(CODES) == {"en"}


@pytest.mark.parametrize("code", CODES)
def test_same_keys_as_german(code):
    keys, de = set(_strings(code)), set(_strings("de"))
    assert (sorted(de - keys), sorted(keys - de)) == ([], [])


@pytest.mark.parametrize("code", CODES)
def test_placeholders_match(code):
    wrong = [k for k, v in _strings(code).items()
             if v.count("{}") != k.count("{}") and (code, k) not in INDEXED_FIELDS]
    assert wrong == []


@pytest.mark.parametrize("code", CODES)
def test_no_empty_translation(code):
    assert [k for k, v in _strings(code).items() if not v.strip()] == []
