import os
import sys
import traceback

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest  # noqa: E402
from PyQt6.QtWidgets import QApplication  # noqa: E402


@pytest.fixture(scope="session")
def app():
    return QApplication.instance() or QApplication([])


def _fail_on_slot_errors(errors):
    if errors:
        tb = "".join("".join(traceback.format_exception(*exc)) for exc in errors)
        errors.clear()
        pytest.fail(f"unhandled exception in a Qt slot:\n{tb}", pytrace=False)


@pytest.fixture(autouse=True)
def slot_errors(request, monkeypatch):
    # PyQt aborts the interpreter on an exception in a slot unless sys.excepthook is replaced.
    errors = request.node.slot_errors = []
    monkeypatch.setattr(sys, "excepthook", lambda *exc: errors.append(exc))
    yield
    _fail_on_slot_errors(errors)


@pytest.hookimpl(wrapper=True)
def pytest_runtest_call(item):
    result = yield
    _fail_on_slot_errors(getattr(item, "slot_errors", []))
    return result
