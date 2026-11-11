import os
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest  # noqa: E402

from adguard_tray import tray  # noqa: E402
from adguard_tray.cli import AdGuardStatus  # noqa: E402


@pytest.mark.parametrize(("msg", "expected"), [
    ("first line\nsecond line\n", "first line"),
    ("x" * 400 + "\nsecond line", "x" * 300),
])
def test_report_error_notifies_one_short_line(monkeypatch, msg, expected):
    sent = []
    monkeypatch.setattr(tray, "notify", lambda title, body, **kw: sent.append(body))
    fake = SimpleNamespace(
        config=SimpleNamespace(notifications_enabled=True),
        _act_status=SimpleNamespace(setText=lambda text: None),
        setToolTip=lambda text: None,
        _last_status=AdGuardStatus.ERROR,
    )

    tray.AdGuardTray._report_error(fake, msg)

    assert sent == [expected]
