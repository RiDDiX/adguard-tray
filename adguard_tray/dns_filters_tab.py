"""
DNS page – DNS filtering (proxy.yaml `dns_filtering`), its servers, secure
DNS and ECH, and the DNS filter lists (`adguard-cli dns filters`).
"""

from . import ui
from .filters_tab import FilterList
from .i18n import _t
from .proxy_settings import add_combo, add_switch, add_text, gate, guard

DNS = "dns_filtering"
HTTPS = "https_filtering"


class DnsFiltersTab(ui.Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(parent=parent)
        s = ctx.settings

        top = self.section()
        master = add_switch(top, s, (DNS, "enabled"), False, _t("DNS filtering"),
                            ui.one_line(_t("Filter DNS queries to block ads and trackers at the DNS level.\n"
                                           "Uses a local DNS proxy with configurable upstreams.")))

        servers = self.section(_t("DNS servers"))
        for key, title, tip in (
            ("upstream", "Upstream:",
             "DNS upstream server.\n'default' = system DNS.\n"
             "Examples: 1.1.1.1, https://dns.google/dns-query,\n"
             "tls://dns.adguard.com, quic://dns.adguard.com"),
            ("fallbacks", "Fallbacks:",
             "Fallback DNS servers (used when primary upstream fails).\n"
             "'default' = system DNS. Space-separated list.\nExample: default 1.1.1.1"),
            ("bootstraps", "Bootstraps:",
             "Bootstrap DNS for resolving upstream hostnames.\n"
             "'default' = system DNS IPs. Only IP addresses allowed.\n"
             "Example: default 8.8.8.8 tls://1.1.1.1"),
        ):
            add_text(servers, s, (DNS, key), "default", _t(title).rstrip(":："), ui.one_line(_t(tip)))

        secure = self.section(_t("Secure DNS and ECH"))
        add_combo(secure, s, (HTTPS, "filter_secure_dns_mode"), "transparent",
                  _t("Secure DNS filtering"),
                  _t("Only affects browsers that use DoH or DoT. Off lets them bypass "
                     "AdGuard's DNS filtering."),
                  [("off", _t("Off")), ("transparent", _t("Filter in place")),
                   ("redirect", _t("Redirect to AdGuard's DNS"))])
        add_switch(secure, s, (DNS, "block_ech"), False, _t("Block ECH in DNS records"),
                   ui.one_line(_t("Remove ECH parameter from SVCB/HTTPS DNS records.\n"
                                  "Enable only for browsers that don't auto-detect HTTPS filtering.")))
        add_switch(secure, s, (HTTPS, "encrypted_client_hello"), False,
                   _t("Encrypted Client Hello (ECH)"),
                   ui.one_line(_t("Enable ECH for better privacy.\nRequires DNS filtering to be enabled.")))

        gate(master.switch, servers, secure)
        guard(self, s, top)     # the lists below work without proxy.yaml

        self.body.addSpacing(16)
        self.add(ui.heading(_t("DNS filter lists")))
        self.add(ui.Caption(_t("Block domains before a connection is made.")))
        off = ui.Caption(_t("DNS filtering is off, so these lists have no effect."), tone="warning")
        self.add(off)

        def sync_off(*_):
            off.setVisible(s.available and not master.switch.isChecked())
        master.switch.toggled.connect(sync_off)
        s.reloaded.connect(sync_off)
        sync_off()
        self.body.addSpacing(4)
        self.lists = FilterList(self, ctx, dns=True, fit=True)
        self.add(self.lists)
        self._workers = self.lists._workers
        self.finish()
        self.lists.load()

    def refresh(self) -> None:
        self.lists.load()

    def on_shown(self) -> None:
        self.lists.load()

    def focus_search(self) -> None:
        self.lists.focus_search()
        self.ensureWidgetVisible(self.lists.search)
