"""Network – how traffic reaches AdGuard's proxy (proxy.yaml), and AdGuard VPN next to it."""

import logging
from pathlib import Path

from PyQt6.QtCore import QThread, QUrl, pyqtSignal
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QComboBox, QPushButton

from . import installer, vpn
from .i18n import _t
from .proxy_settings import PROXY_YAML, add_combo, add_spin, add_switch, add_text, gate, guard
from .ui import Banner, Page, Row, one_line

logger = logging.getLogger(__name__)

OUTBOUND = "outbound_proxy"
_PROXY_TYPES = ("HTTP", "HTTPS", "SOCKS4", "SOCKS5")    # adguard-cli's spelling in proxy.yaml


def _label(key: str) -> str:
    """A former form label ("Filtered ports:") as a row title."""
    return _t(key).rstrip(":：")


class _VpnWorker(QThread):
    done = pyqtSignal(str, object, str)     # path ("" = not installed), VpnConfig or None, error

    def __init__(self, switch: bool) -> None:
        super().__init__()
        self.switch = switch

    def run(self) -> None:
        path, config, error = "", None, ""
        try:
            path = vpn.find()
            if path:
                config, error = (vpn.set_socks_mode if self.switch else vpn.read_config)(path)
        except Exception as exc:
            logger.exception("adguardvpn-cli call failed")
            error = str(exc)
        self.done.emit(path, config, error)


def open_folder(page: Page, folder: Path) -> None:
    if not QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder))):
        page.banner.show_message(_t("Could not open {}", str(folder)), "warning")


class NetworkTab(Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(parent=parent)
        self.ctx = ctx
        s = ctx.settings
        self._workers: list[QThread] = []
        self._busy = False
        self._switch_pending = False
        self._vpn_path, self._vpn = "", None

        mode_card = self.section(_t("Proxy mode"))
        mode = add_combo(mode_card, s, ("proxy_mode",), "auto", _label("Mode:"),
                         _t("Automatic: AdGuard redirects all app traffic to itself via iptables. "
                            "Manual: AdGuard only listens on the SOCKS5 and HTTP ports below."),
                         [("auto", _t("Automatic – filter all apps")),
                          ("manual", _t("Manual – only apps set to use the proxy"))])
        ports = add_text(mode_card, s, ("filtered_ports",), "80:5221,5300:49151", _label("Filtered ports:"),
                         _t("Used in automatic mode only. Ranges (80:5221,5300:49151) "
                            "or single ports (80,443,8080)."))

        vpn_card = self.section(
            _t("AdGuard VPN"),
            _t("AdGuard's VPN for Linux (adguardvpn-cli) runs next to AdGuard CLI. AdGuard Tray checks "
               "that their settings fit together; it does not connect the VPN or log in."))
        self.vpn_conflict = Banner()
        vpn_card.add(self.vpn_conflict)
        self.btn_vpn_install = QPushButton(_t("Install…"))
        self.btn_vpn_install.clicked.connect(lambda: installer.start_install(self, vpn.BINARY))
        self.btn_vpn_install.hide()
        self.vpn_row = vpn_card.add_row(Row(_t("AdGuard VPN CLI"), _t("Checking…"), self.btn_vpn_install))

        outbound = self.section(_t("Outbound proxy"),
                                _t("AdGuard sends its own connections through this proxy, for example "
                                   "through AdGuard VPN in SOCKS5 mode."))
        use = add_switch(outbound, s, (OUTBOUND, "enabled"), False, _t("Use an outbound proxy"))
        kind = add_combo(outbound, s, (OUTBOUND, "mode"), "HTTP", _t("Type"), "",
                         [(name, name) for name in _PROXY_TYPES])
        host = add_text(outbound, s, (OUTBOUND, "host"), "localhost", _t("Host"), "")
        port = add_spin(outbound, s, (OUTBOUND, "port"), 3128, _t("Port"), "", 1)
        gate(use.switch, kind, host, port)

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

        guard(self, s, mode_card, outbound, manual, perf)
        s.reloaded.connect(follow)      # after guard, which re-enables the manual card
        follow()
        s.changed.connect(lambda key: self._show_conflict() if key == ("proxy_mode",) else None)
        s.reloaded.connect(self._show_conflict)
        self.finish()

    # ── AdGuard VPN ────────────────────────────────────────────────────────

    def on_shown(self) -> None:
        self._check_vpn()

    def refresh(self) -> None:
        self._check_vpn()

    def _check_vpn(self, switch: bool = False) -> None:
        if self._busy:
            # The warning's button hides it on click; run the switch right after this check.
            self._switch_pending = self._switch_pending or switch
            return
        self._busy = True
        worker = _VpnWorker(switch)
        worker.done.connect(self._vpn_switched if switch else self._vpn_checked)
        worker.finished.connect(lambda: self._workers.remove(worker) if worker in self._workers else None)
        worker.finished.connect(worker.deleteLater)
        self._workers.append(worker)
        worker.start()

    def _vpn_checked(self, path: str, config, error: str) -> None:
        self._busy = False
        self._vpn_path, self._vpn = path, config
        self.btn_vpn_install.setVisible(not path)
        if not path:
            text = _t("Not installed.")
        elif config is None:
            text = _t("Installed, but its settings could not be read: {}", one_line(error)[:200] or "?")
        elif config.mode == "socks":
            text = _t("Installed · SOCKS5 mode on {}:{}", config.socks_host, config.socks_port)
        elif config.mode == "tun":
            text = _t("Installed · TUN mode")
        else:
            text = _t("Installed · {} mode", config.mode)
        self.vpn_row.subtitle.setText(text)
        self._show_conflict()
        if self._switch_pending:
            self._switch_pending = False
            if not self.vpn_conflict.isHidden():     # still needed after the fresh check
                self._check_vpn(True)

    def _show_conflict(self) -> None:
        s = self.ctx.settings
        loop = (self._vpn is not None and self._vpn.mode == "tun" and s.available
                and s.value(("proxy_mode",), "auto") == "auto")
        if not loop:
            self.vpn_conflict.hide()
            return
        self.vpn_conflict.show_message(
            _t("AdGuard VPN is set to TUN mode while AdGuard filters in automatic mode. Connected like "
               "this, traffic loops between the two – AdGuard does not support this combination."),
            "warning", action=_t("Route AdGuard through the VPN"), callback=lambda: self._check_vpn(True))

    def _vpn_switched(self, path: str, config, error: str) -> None:
        """The VPN is in SOCKS5 mode now; point adguard-cli's outbound proxy at it."""
        self._busy = False
        if config is None:
            self.banner.show_message(_t("Could not switch AdGuard VPN to SOCKS5 mode."), "danger",
                                     details=error)
            self._check_vpn()
            return
        s = self.ctx.settings
        s.set((OUTBOUND, "enabled"), True, False)
        s.set((OUTBOUND, "mode"), "SOCKS5", "HTTP")
        s.set((OUTBOUND, "host"), config.socks_host, "localhost")
        s.set((OUTBOUND, "port"), config.socks_port, 3128)
        # Without this rule the VPN's own traffic would go into the proxy it is.
        apps = s.value(("apps",), [])
        if not vpn.skips_outbound_proxy(apps, (vpn.BINARY, path)):
            s.set(("apps",), [dict(vpn.VPN_RULE), *apps], [])
        self._vpn_checked(path, config, "")
        self.banner.show_message(
            _t("AdGuard VPN now uses SOCKS5 mode. Press Apply to send AdGuard's traffic through it, "
               "and reconnect AdGuard VPN if it is connected."), "success")
