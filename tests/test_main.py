from types import SimpleNamespace

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from adguard_tray import main


def test_missing_cli_dialog_survives_its_own_button(app, monkeypatch):
    monkeypatch.setattr(main.shutil, "which", lambda name: None)
    main._dependency_doctor(SimpleNamespace(BINARY="adguard-cli"))
    box = main._doctor_box
    assert box.windowModality() == Qt.WindowModality.NonModal, "the manager window must stay usable"
    button = box.escapeButton()
    del box     # as in the app: the module global is the only reference
    button.click()
    QTest.qWait(50)
    assert main._doctor_box is None
