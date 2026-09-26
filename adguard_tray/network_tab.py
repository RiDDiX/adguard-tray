"""Network – how traffic reaches AdGuard's proxy (proxy.yaml)."""

from pathlib import Path

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QComboBox, QPushButton

from .i18n import _t
from .proxy_settings import PROXY_YAML, add_combo, add_spin, add_text, guard
from .ui import Page, Row, one_line


def _label(key: str) -> str:
    """A former form label ("Filtered ports:") as a row title."""
    return _t(key).rstrip(":：")


def open_folder(page: Page, folder: Path) -> None:
    if not QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder))):
        page.banner.show_message(_t("Could not open {}", str(folder)), "warning")


class NetworkTab(Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(parent=parent)
        s = ctx.settings

        mode_card = self.section(_t("Proxy mode"))
        mode = add_combo(mode_card, s, ("proxy_mode",), "auto", _label("Mode:"),
                         _t("Automatic: AdGuard redirects all app traffic to itself via iptables. "
                            "Manual: AdGuard only listens on the SOCKS5 and HTTP ports below."),
                         [("auto", _t("Automatic – filter all apps")),
                          ("manual", _t("Manual – only apps set to use the proxy"))])
        ports = add_text(mode_card, s, ("filtered_ports",), "80:5221,5300:49151", _label("Filtered ports:"),
                         _t("Used in automatic mode only. Ranges (80:5221,5300:49151) "
                            "or single ports (80,443,8080)."))

        manual = self.section(_t("Manual proxy"), _t("Used in manual mode only."))
        add_spin(manual, s, ("listen_ports", "socks5_proxy"), 1081, _label("SOCKS5 port:"),
                 one_line(_t("SOCKS5 proxy port for manual mode.\nSet to -1 to disable.")),
                 minimum=-1, special=_t("Off"))
        add_spin(manual, s, ("listen_ports", "http_proxy"), 3129, _label("HTTP port:"),
                 one_line(_t("HTTP proxy port for manual mode.\nSet to -1 to disable.")),
                 minimum=-1, special=_t("Off"))
        add_text(manual, s, ("listen_address",), "127.0.0.1", _label("Listen address:"),
                 one_line(_t("Address the proxy listens on.\n"
                             "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).")))

        perf = self.section(_t("Performance"))
        add_spin(perf, s, ("worker_threads",), 4, _label("Worker threads:"),
                 _t("Number of proxy worker threads."), 1, 64)

        # Outside the guard: the folder is worth opening most when the file is missing.
        files = self.section(_t("Settings file"))
        btn_open = QPushButton(_t("Open folder"))
        btn_open.clicked.connect(lambda: open_folder(self, PROXY_YAML.parent))
        files.add_row(Row("proxy.yaml", str(PROXY_YAML), btn_open))

        combo = mode.findChild(QComboBox)

        def follow(_index=None) -> None:
            is_manual = combo.currentData() == "manual"
            ports.setEnabled(not is_manual)
            manual.setEnabled(is_manual and s.available)
        combo.currentIndexChanged.connect(follow)

        guard(self, s, mode_card, manual, perf)
        s.reloaded.connect(follow)      # after guard, which re-enables the manual card
        follow()
        self.finish()
