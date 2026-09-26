"""adguard-cli's proxy.yaml as one shared, editable model.

Every Manager page that shows a proxy.yaml setting binds its widget to a key
here. Edits collect until the window's Apply bar writes them, so switching a
few options costs one restart, not one per click. Two widgets bound to the
same key (the Overview's module switches and the pages' own) stay in sync.

Applying re-reads the file and writes back only the keys that were edited:
adguard-cli keeps writing proxy.yaml while the window is open, and nothing
else should be replaced with the value the window loaded.
"""

import logging
from pathlib import Path

import yaml
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QComboBox, QLineEdit, QSpinBox

from ._allowlist import write_atomic

logger = logging.getLogger(__name__)

PROXY_YAML = Path.home() / ".local" / "share" / "adguard-cli" / "proxy.yaml"


# ── YAML helpers ─────────────────────────────────────────────────────────────

def load_yaml() -> dict:
    """proxy.yaml as a dict; {} when it is missing or unreadable."""
    try:
        data = yaml.safe_load(PROXY_YAML.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        logger.error("Failed to load proxy.yaml: %s", exc)
        return {}
    return data if isinstance(data, dict) else {}


def save_yaml(data: dict) -> tuple[bool, str]:
    try:
        class _Dumper(yaml.SafeDumper):
            pass

        def _str(dumper, value):
            style = "|" if "\n" in value else "'"
            return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)

        _Dumper.add_representer(str, _str)
        text = yaml.dump(data, Dumper=_Dumper, default_flow_style=False,
                         allow_unicode=True, sort_keys=False, width=120)
        write_atomic(PROXY_YAML, text)
        return True, ""
    except Exception as exc:
        logger.error("Failed to save proxy.yaml: %s", exc)
        return False, str(exc)


def get(data: dict, *keys, default=None):
    """A nested value, or *default* when it is missing or of an unexpected type.

    proxy.yaml is written by adguard-cli, and a reshaped key must not take the
    window (and with it the tray) down.
    """
    node = data
    for k in keys:
        if isinstance(node, dict):
            node = node.get(k, default)
        else:
            return default
    if node is None:
        return default
    if isinstance(default, bool):
        # YAML 1.1 has on/off/yes/no, and safe_load gives ints for 0/1.
        return bool(node) if isinstance(node, (bool, int)) else default
    if isinstance(default, int) and isinstance(node, bool):
        return default  # a bool is not a port or a thread count
    if default is not None and not isinstance(node, type(default)):
        return default
    return node


def put(data: dict, keys: tuple, value) -> None:
    node = data
    for k in keys[:-1]:
        if not isinstance(node.get(k), dict):
            node[k] = {}
        node = node[k]
    node[keys[-1]] = value


# ── The model ────────────────────────────────────────────────────────────────

class ProxySettings(QObject):
    changed = pyqtSignal(tuple)         # a key's shown value changed
    dirty_changed = pyqtSignal(int)     # number of pending edits
    reloaded = pyqtSignal()             # after load / discard / apply

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._data: dict = {}
        self._edits: dict[tuple, object] = {}
        self.error = ""
        self.load()

    @property
    def available(self) -> bool:
        return not self.error

    def load(self) -> None:
        self.error = ""
        if not PROXY_YAML.exists():
            self.error = "missing"
            self._data = {}
        else:
            self._data = load_yaml()
            if not self._data:
                self.error = "unreadable"
        self._edits.clear()
        self.dirty_changed.emit(0)
        self.reloaded.emit()

    def original(self, key: tuple, default=None):
        return get(self._data, *key, default=default)

    def value(self, key: tuple, default=None):
        if key in self._edits:
            return self._edits[key]
        return self.original(key, default)

    def set(self, key: tuple, value, default=None) -> None:
        if self.value(key, default) == value and type(self.value(key, default)) is type(value):
            return
        original = self.original(key, default)
        if value == original and type(value) is type(original):
            self._edits.pop(key, None)
        else:
            self._edits[key] = value
        self.changed.emit(key)
        self.dirty_changed.emit(len(self._edits))

    def dirty(self) -> int:
        return len(self._edits)

    def discard(self) -> None:
        # Re-read as well: adguard-cli may have changed the file meanwhile.
        self.load()

    def apply(self) -> tuple[bool, str]:
        """Write the pending edits into a fresh read of proxy.yaml."""
        if not self._edits:
            return True, ""
        fresh = load_yaml() if not self.error else {}
        if not fresh:
            # Never create or replace a file adguard-cli owns from a partial view.
            return False, unavailable_message(PROXY_YAML.exists())
        for key, value in self._edits.items():
            put(fresh, key, value)
        ok, err = save_yaml(fresh)
        if ok:
            self._data = fresh
            self._edits.clear()
            self.dirty_changed.emit(0)
            self.reloaded.emit()
        return ok, err


# ── Binding widgets ──────────────────────────────────────────────────────────

def bind_switch(model: ProxySettings, widget, key: tuple, default: bool) -> None:
    """A Switch or QCheckBox for a boolean key."""
    # No blockSignals in pull(): dependents (gate()) must see the change, and
    # model.set() ignores a value it already has, so nothing loops.
    def pull(*_):
        widget.setChecked(bool(model.value(key, default)))
    widget.toggled.connect(lambda on: model.set(key, bool(on), default))
    _follow(model, key, pull, widget)


def bind_spin(model: ProxySettings, widget: QSpinBox, key: tuple, default: int) -> None:
    low, high = widget.minimum(), widget.maximum()

    def pull(*_):
        value = int(model.value(key, default))
        # A value outside the offered range is shown as it is: clamping it
        # would record an edit nobody made.
        widget.setRange(min(low, value), max(high, value))
        widget.setValue(value)
    widget.valueChanged.connect(lambda v: model.set(key, int(v), default))
    _follow(model, key, pull, widget)


def bind_combo(model: ProxySettings, widget: QComboBox, key: tuple, default: str,
               choices: list[tuple[str, str]]) -> None:
    """Human labels, YAML values in itemData. A value this version doesn't know
    is kept as its own entry instead of being rewritten."""
    for value, label in choices:
        widget.addItem(label, value)
    known = len(choices)

    def pull(*_):
        value = str(model.value(key, default))
        # Drop an unknown value shown for an earlier file, keep the current one.
        for index in range(widget.count() - 1, known - 1, -1):
            if widget.itemData(index) != value:
                widget.removeItem(index)
        if widget.findData(value) < 0:
            widget.addItem(value, value)
        widget.setCurrentIndex(widget.findData(value))
    widget.currentIndexChanged.connect(lambda _i: model.set(key, widget.currentData(), default))
    _follow(model, key, pull, widget)


def bind_raw_edit(model: ProxySettings, widget: QLineEdit, key: tuple, default: str) -> None:
    """One line of text for a value adguard-cli may store as a list or number.

    It is shown space-joined and written back untouched unless the text is
    actually changed; a list stays a list.
    """
    def raw():
        value = model.original(key)
        return default if value is None else value

    def shown(value) -> str:
        return " ".join(str(x) for x in value) if isinstance(value, list) else str(value)

    pushing = []

    def pull(*_):
        if pushing:
            return      # our own keystroke: setText would move the cursor and eat spaces
        widget.blockSignals(True)
        widget.setText(shown(model.value(key, raw())))
        widget.blockSignals(False)

    def push(text: str):
        text = text.strip()
        original = raw()
        pushing.append(True)
        try:
            if text == shown(original).strip():
                model.set(key, original)
            elif isinstance(original, list):
                model.set(key, text.split())
            else:
                model.set(key, text)
        finally:
            pushing.pop()
    widget.textEdited.connect(push)
    _follow(model, key, pull, widget)


# ── Rows ─────────────────────────────────────────────────────────────────────
# One call per setting: a titled row in *card* with its control bound to *key*.

def add_switch(card, model: ProxySettings, key: tuple, default: bool, title: str,
               subtitle: str = ""):
    from .ui import Row, Switch
    switch = Switch()
    bind_switch(model, switch, key, default)
    return card.add_row(Row(title, subtitle, switch))


def add_spin(card, model: ProxySettings, key: tuple, default: int, title: str,
             subtitle: str = "", minimum: int = 0, maximum: int = 65535,
             special: str = "", suffix: str = ""):
    """*special* labels the minimum (e.g. "Off" for a port of -1)."""
    from .ui import Row, ignore_idle_wheel
    spin = ignore_idle_wheel(QSpinBox())
    spin.setRange(minimum, maximum)
    if special:
        spin.setSpecialValueText(special)
    if suffix:
        spin.setSuffix(suffix)
    bind_spin(model, spin, key, default)
    return card.add_row(Row(title, subtitle, spin))


def add_combo(card, model: ProxySettings, key: tuple, default: str, title: str,
              subtitle: str, choices: list[tuple[str, str]]):
    from .ui import Row, ignore_idle_wheel
    combo = ignore_idle_wheel(QComboBox())
    bind_combo(model, combo, key, default, choices)
    return card.add_row(Row(title, subtitle, combo))


def add_text(card, model: ProxySettings, key: tuple, default: str, title: str,
             subtitle: str = "", width: int = 260):
    from .ui import Row
    edit = QLineEdit()
    edit.setMinimumWidth(width)
    bind_raw_edit(model, edit, key, default)
    return card.add_row(Row(title, subtitle, edit))


def gate(switch, *widgets) -> None:
    """Enable *widgets* only while *switch* is on (a master switch)."""
    def follow(on: bool) -> None:
        for widget in widgets:
            widget.setEnabled(bool(on))
    switch.toggled.connect(follow)
    follow(switch.isChecked())


def unavailable_message(exists: bool) -> str:
    from .i18n import _t
    if not exists:
        return _t("AdGuard's settings file was not found ({}). Run adguard-cli once "
                  "to create it.", str(PROXY_YAML))
    return _t("Could not load proxy.yaml.\nPath: {}", str(PROXY_YAML))


def guard(page, model: ProxySettings, *widgets) -> None:
    """Disable *widgets* (default: the page's content) and say why while
    proxy.yaml can't be edited; clear the message again once it can."""
    targets = widgets or (page.content,)

    def check() -> None:
        for widget in targets:
            widget.setEnabled(model.available)
        if model.available:
            if getattr(page, "_guard_shown", False):
                page.banner.hide()
                page._guard_shown = False
            return
        page._guard_shown = True
        page.banner.show_message(unavailable_message(model.error != "missing"),
                                 "warning" if model.error == "missing" else "danger")
    model.reloaded.connect(check)
    check()


class _Follower(QObject):
    """Keeps one widget in step with one key.

    A child of the widget, connected through real slots, so Qt drops the
    connections by itself when the widget goes. A Python closure on the
    widget's destroyed signal ran during interpreter teardown instead and
    crashed PyQt6 6.4 at exit.
    """

    def __init__(self, model: ProxySettings, key: tuple, pull, widget) -> None:
        super().__init__(widget)
        self._key, self._pull = key, pull
        model.changed.connect(self._on_changed)
        model.reloaded.connect(self._on_reloaded)

    @pyqtSlot(tuple)
    def _on_changed(self, key: tuple) -> None:
        if key == self._key:
            self._pull()

    @pyqtSlot()
    def _on_reloaded(self) -> None:
        self._pull()


def _follow(model: ProxySettings, key: tuple, pull, widget) -> None:
    pull()
    _Follower(model, key, pull, widget)


if __name__ == "__main__":
    import os
    import sys
    import tempfile

    from PyQt6.QtWidgets import QApplication, QCheckBox

    app = QApplication(sys.argv[:1] + ["-platform", "offscreen"])
    tmp = Path(tempfile.mkdtemp())
    PROXY_YAML = tmp / "proxy.yaml"
    PROXY_YAML.write_text("https_filtering:\n  enabled: true\nfiltered_ports: 80:5221\n"
                          "dns_filtering:\n  upstream: [a, b]\nkeep_me: 1\n")
    m = ProxySettings()
    a, b = QCheckBox(), QCheckBox()
    bind_switch(m, a, ("https_filtering", "enabled"), True)
    bind_switch(m, b, ("https_filtering", "enabled"), True)
    assert a.isChecked() and b.isChecked()
    a.setChecked(False)
    assert not b.isChecked() and m.dirty() == 1, "second widget follows"
    a.setChecked(True)
    assert m.dirty() == 0, "back to the original is not an edit"
    edit = QLineEdit()
    bind_raw_edit(m, edit, ("dns_filtering", "upstream"), "default")
    assert edit.text() == "a b"
    edit.textEdited.emit("a b c")
    b.setChecked(False)
    # adguard-cli writes something else meanwhile – it must survive
    PROXY_YAML.write_text(PROXY_YAML.read_text().replace("keep_me: 1", "keep_me: 2"))
    ok, err = m.apply()
    assert ok, err
    data = yaml.safe_load(PROXY_YAML.read_text())
    assert data["keep_me"] == 2 and data["dns_filtering"]["upstream"] == ["a", "b", "c"]
    assert data["https_filtering"]["enabled"] is False and data["filtered_ports"] == "80:5221"
    assert m.dirty() == 0 and not a.isChecked()
    a.setChecked(True)
    dependent = QLineEdit()
    gate(a, dependent)
    assert dependent.isEnabled()
    m.discard()
    assert not a.isChecked() and not b.isChecked() and not dependent.isEnabled()
    assert m.dirty() == 0
    del a
    os.remove(PROXY_YAML)
    m.load()
    assert m.error == "missing"
    print("proxy_settings ok")
