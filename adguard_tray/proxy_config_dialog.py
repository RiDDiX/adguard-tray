"""
AdGuard CLI proxy.yaml configuration editor.

Tabs:
  1. Proxy       – mode, filtered ports, listen ports
  2. HTTPS       – HTTPS filtering, TLS 1.3, HTTP/3, OCSP, CT, ECH
  3. DNS         – DNS filtering, upstream, fallbacks, bootstraps
  4. Stealth     – tracking protection / anti-fingerprint options
  5. Apps        – per-app filter rules (bypass for games, etc.)
  6. Security    – SafeBrowsing, CRLite
"""

import logging
from pathlib import Path

import yaml
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ._allowlist import write_atomic
from .i18n import _t

logger = logging.getLogger(__name__)

_PROXY_YAML = Path.home() / ".local" / "share" / "adguard-cli" / "proxy.yaml"


# ── YAML helpers ──────────────────────────────────────────────────────────────

def _load_yaml() -> dict:
    """Load proxy.yaml preserving all keys."""
    try:
        return yaml.safe_load(_PROXY_YAML.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        logger.error("Failed to load proxy.yaml: %s", exc)
        return {}


def _save_yaml(data: dict) -> tuple[bool, str]:
    """Write proxy.yaml back. Returns (ok, message)."""
    try:
        # Custom representer to keep strings quoted for readability
        class _Dumper(yaml.SafeDumper):
            pass

        def _str_representer(dumper, data):
            if "\n" in data:
                return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="'")

        _Dumper.add_representer(str, _str_representer)

        text = yaml.dump(data, Dumper=_Dumper, default_flow_style=False,
                         allow_unicode=True, sort_keys=False, width=120)
        write_atomic(_PROXY_YAML, text)
        return True, ""
    except Exception as exc:
        logger.error("Failed to save proxy.yaml: %s", exc)
        return False, str(exc)


def _get(data: dict, *keys, default=None):
    """Safely traverse nested dict.

    Values of an unexpected type fall back to *default*: proxy.yaml is written
    by adguard-cli, and a reshaped key must not take the dialog (and with it
    the tray) down.
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


def _raw_edit(raw, default: str) -> QLineEdit:
    """QLineEdit that remembers the raw YAML value.

    adguard-cli writes lists (and sometimes numbers) where the UI shows one
    line of text. Those are displayed space-joined and written back untouched
    unless the user actually edits the field.
    """
    if raw is None:
        shown = default
    elif isinstance(raw, list):
        shown = " ".join(str(x) for x in raw)
    else:
        shown = str(raw)
    edit = QLineEdit(shown)
    edit.setProperty("_raw", default if raw is None else raw)
    edit.setProperty("_shown", shown)
    return edit


def _raw_value(edit: QLineEdit):
    """Edited text, or the untouched original when the field wasn't changed."""
    text = edit.text().strip()
    raw = edit.property("_raw")
    if text == str(edit.property("_shown") or "").strip():
        return raw
    if isinstance(raw, list):
        # Keep the shape adguard-cli wrote; the field shows it space-joined.
        return text.split()
    return text


def _set(data: dict, *keys_and_value):
    """Set a value in a nested dict, creating intermediate dicts as needed."""
    *keys, value = keys_and_value
    node = data
    for k in keys[:-1]:
        if k not in node or not isinstance(node[k], dict):
            node[k] = {}
        node = node[k]
    node[keys[-1]] = value


# ── Scrollable tab helper ─────────────────────────────────────────────────────

def _scrollable(widget: QWidget) -> QScrollArea:
    scroll = QScrollArea()
    scroll.setWidget(widget)
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QScrollArea.Shape.NoFrame)
    return scroll


# ── Main dialog ───────────────────────────────────────────────────────────────

class ProxyConfigDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(_t("AdGuard CLI – Configuration"))
        self.setMinimumSize(720, 600)
        self.resize(780, 660)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        self._data = _load_yaml()
        if not self._data:
            QMessageBox.warning(
                self,
                _t("AdGuard CLI – Configuration"),
                _t("Could not load proxy.yaml.\nPath: {}",
                    str(_PROXY_YAML)),
            )
            # Nothing to edit – close as soon as the caller's exec() starts.
            QTimer.singleShot(0, self.reject)
            return

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        # Path info
        path_label = QLabel(f"<small><code>{_PROXY_YAML}</code></small>")
        path_label.setTextFormat(Qt.TextFormat.RichText)
        path_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(path_label)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_proxy_tab(), _t("Proxy"))
        self.tabs.addTab(self._build_https_tab(), _t("HTTPS"))
        self.tabs.addTab(self._build_dns_tab(), _t("DNS"))
        self.tabs.addTab(self._build_stealth_tab(), _t("Stealth Mode"))
        self.tabs.addTab(self._build_apps_tab(), _t("Apps"))
        self.tabs.addTab(self._build_security_tab(), _t("Security"))
        layout.addWidget(self.tabs)

        # Restart hint
        hint = QLabel(_t(
            "<small><b>Note:</b> Changes require an AdGuard CLI restart to take effect.</small>"
        ))
        hint.setTextFormat(Qt.TextFormat.RichText)
        hint.setWordWrap(True)
        layout.addWidget(hint)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # ── Tab 1: Proxy ──────────────────────────────────────────────────────

    def _build_proxy_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)

        # Proxy mode
        grp = QGroupBox(_t("Proxy Mode"))
        form = QFormLayout(grp)

        self.combo_proxy_mode = QComboBox()
        self.combo_proxy_mode.addItems(["auto", "manual"])
        self.combo_proxy_mode.setCurrentText(
            _get(self._data, "proxy_mode", default="auto")
        )
        self.combo_proxy_mode.setToolTip(_t(
            "auto: AdGuard redirects app traffic into itself via iptables\n"
            "manual: Only listens on the configured proxy ports (SOCKS5/HTTP)"
        ))
        form.addRow(_t("Mode:"), self.combo_proxy_mode)

        self.edit_filtered_ports = _raw_edit(
            _get(self._data, "filtered_ports"), "80:5221,5300:49151"
        )
        self.edit_filtered_ports.setToolTip(_t(
            "Port ranges intercepted in auto mode.\n"
            "Format: 80:5221,5300:49151 (range) or 80,443,8080 (individual)\n"
            "Only applies when proxy mode is 'auto'."
        ))
        form.addRow(_t("Filtered ports:"), self.edit_filtered_ports)

        layout.addWidget(grp)

        # Listen ports (manual mode)
        grp2 = QGroupBox(_t("Manual Proxy Ports"))
        form2 = QFormLayout(grp2)

        self.spin_socks5 = QSpinBox()
        self.spin_socks5.setRange(-1, 65535)
        self.spin_socks5.setValue(
            _get(self._data, "listen_ports", "socks5_proxy", default=1081)
        )
        self.spin_socks5.setToolTip(_t(
            "SOCKS5 proxy port for manual mode.\n"
            "Set to -1 to disable."
        ))
        form2.addRow(_t("SOCKS5 port:"), self.spin_socks5)

        self.spin_http = QSpinBox()
        self.spin_http.setRange(-1, 65535)
        self.spin_http.setValue(
            _get(self._data, "listen_ports", "http_proxy", default=3129)
        )
        self.spin_http.setToolTip(_t(
            "HTTP proxy port for manual mode.\n"
            "Set to -1 to disable."
        ))
        form2.addRow(_t("HTTP port:"), self.spin_http)

        self.edit_listen_addr = _raw_edit(
            _get(self._data, "listen_address"), "127.0.0.1"
        )
        self.edit_listen_addr.setToolTip(_t(
            "Address the proxy listens on.\n"
            "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth)."
        ))
        form2.addRow(_t("Listen address:"), self.edit_listen_addr)

        self.spin_workers = QSpinBox()
        self.spin_workers.setRange(1, 64)
        self.spin_workers.setValue(
            _get(self._data, "worker_threads", default=4)
        )
        self.spin_workers.setToolTip(_t("Number of proxy worker threads."))
        form2.addRow(_t("Worker threads:"), self.spin_workers)

        layout.addWidget(grp2)
        layout.addStretch()
        return _scrollable(w)

    # ── Tab 2: HTTPS ──────────────────────────────────────────────────────

    def _build_https_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        https = _get(self._data, "https_filtering", default={})

        grp = QGroupBox(_t("HTTPS Filtering"))
        form = QVBoxLayout(grp)

        self.cb_https = QCheckBox(_t("Enable HTTPS filtering"))
        self.cb_https.setChecked(_get(https, "enabled", default=True))
        self.cb_https.setToolTip(_t(
            "Decrypt and filter HTTPS traffic.\n"
            "Needed to block ads on https sites.\n"
            "Requires a trusted root certificate installed on the system."
        ))
        form.addWidget(self.cb_https)

        self.cb_tls13 = QCheckBox(_t("Enable TLS 1.3"))
        self.cb_tls13.setChecked(_get(https, "enable_tls13", default=True))
        self.cb_tls13.setToolTip(_t("Enable TLS 1.3 support for filtered connections."))
        form.addWidget(self.cb_tls13)

        self.cb_http3 = QCheckBox(_t("Filter HTTP/3 (QUIC) – experimental"))
        self.cb_http3.setChecked(_get(https, "http3_filtering_enabled", default=True))
        self.cb_http3.setToolTip(_t(
            "Filter HTTP/3 (QUIC) traffic.\n"
            "Experimental – may cause issues with some sites."
        ))
        form.addWidget(self.cb_http3)

        self.cb_ocsp = QCheckBox(_t("OCSP certificate checks"))
        self.cb_ocsp.setChecked(_get(https, "ocsp_check_enabled", default=True))
        self.cb_ocsp.setToolTip(_t(
            "Check certificate revocation status via OCSP.\n"
            "Slower but more secure."
        ))
        form.addWidget(self.cb_ocsp)

        self.cb_ct = QCheckBox(_t("Enforce Certificate Transparency"))
        self.cb_ct.setChecked(_get(https, "enforce_certificate_transparency", default=True))
        self.cb_ct.setToolTip(_t(
            "Enforce Certificate Transparency timestamp checks.\n"
            "Similar to Chrome's built-in CT policy."
        ))
        form.addWidget(self.cb_ct)

        self.cb_ev = QCheckBox(_t("Filter EV certificate sites"))
        self.cb_ev.setChecked(_get(https, "filter_ev_certificates", default=False))
        self.cb_ev.setToolTip(_t(
            "By default, sites with Extended Validation certificates are not filtered.\n"
            "Enable this to filter them as well (e.g. banking sites)."
        ))
        form.addWidget(self.cb_ev)

        self.cb_ech = QCheckBox(_t("Encrypted Client Hello (ECH)"))
        self.cb_ech.setChecked(_get(https, "encrypted_client_hello", default=False))
        self.cb_ech.setToolTip(_t(
            "Enable ECH for better privacy.\n"
            "Requires DNS filtering to be enabled."
        ))
        form.addWidget(self.cb_ech)

        layout.addWidget(grp)

        # Secure DNS filtering mode
        grp2 = QGroupBox(_t("Secure DNS Filtering"))
        form2 = QFormLayout(grp2)

        self.combo_sdns = QComboBox()
        self.combo_sdns.addItems(["off", "transparent", "redirect"])
        self.combo_sdns.setCurrentText(
            _get(https, "filter_secure_dns_mode", default="transparent")
        )
        self.combo_sdns.setToolTip(_t(
            "off: No secure DNS filtering\n"
            "transparent: Filter DoH/DoT inline without changing destination\n"
            "redirect: Redirect all secure DNS to the local DNS proxy"
        ))
        form2.addRow(_t("Mode:"), self.combo_sdns)

        layout.addWidget(grp2)
        layout.addStretch()
        return _scrollable(w)

    # ── Tab 3: DNS ────────────────────────────────────────────────────────

    def _build_dns_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        dns = _get(self._data, "dns_filtering", default={})

        grp = QGroupBox(_t("DNS Filtering"))
        form = QVBoxLayout(grp)

        self.cb_dns = QCheckBox(_t("Enable DNS filtering"))
        self.cb_dns.setChecked(_get(dns, "enabled", default=False))
        self.cb_dns.setToolTip(_t(
            "Filter DNS queries to block ads and trackers at the DNS level.\n"
            "Uses a local DNS proxy with configurable upstreams."
        ))
        form.addWidget(self.cb_dns)

        form_fields = QFormLayout()

        self.edit_dns_upstream = _raw_edit(_get(dns, "upstream"), "default")
        self.edit_dns_upstream.setToolTip(_t(
            "DNS upstream server.\n"
            "'default' = system DNS\n"
            "Examples: 1.1.1.1, https://dns.google/dns-query,\n"
            "tls://dns.adguard.com, quic://dns.adguard.com"
        ))
        form_fields.addRow(_t("Upstream:"), self.edit_dns_upstream)

        self.edit_dns_fallback = _raw_edit(_get(dns, "fallbacks"), "default")
        self.edit_dns_fallback.setToolTip(_t(
            "Fallback DNS servers (used when primary upstream fails).\n"
            "'default' = system DNS. Space-separated list.\n"
            "Example: default 1.1.1.1"
        ))
        form_fields.addRow(_t("Fallbacks:"), self.edit_dns_fallback)

        self.edit_dns_bootstrap = _raw_edit(_get(dns, "bootstraps"), "default")
        self.edit_dns_bootstrap.setToolTip(_t(
            "Bootstrap DNS for resolving upstream hostnames.\n"
            "'default' = system DNS IPs. Only IP addresses allowed.\n"
            "Example: default 8.8.8.8 tls://1.1.1.1"
        ))
        form_fields.addRow(_t("Bootstraps:"), self.edit_dns_bootstrap)

        self.cb_block_ech = QCheckBox(_t("Block ECH in DNS"))
        self.cb_block_ech.setChecked(_get(dns, "block_ech", default=False))
        self.cb_block_ech.setToolTip(_t(
            "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
            "Enable only for browsers that don't auto-detect HTTPS filtering."
        ))

        form.addLayout(form_fields)
        form.addWidget(self.cb_block_ech)
        layout.addWidget(grp)
        layout.addStretch()
        return _scrollable(w)

    # ── Tab 4: Stealth Mode ───────────────────────────────────────────────

    def _build_stealth_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        sm = _get(self._data, "stealthmode", default={})

        grp = QGroupBox(_t("Stealth Mode (Tracking Protection)"))
        form = QVBoxLayout(grp)

        self.cb_stealth = QCheckBox(_t("Enable Stealth Mode"))
        self.cb_stealth.setChecked(_get(sm, "enabled", default=False))
        self.cb_stealth.setToolTip(_t(
            "Master switch for all tracking protection features below."
        ))
        form.addWidget(self.cb_stealth)

        layout.addWidget(grp)

        # Cookies
        grp_cookies = QGroupBox(_t("Cookies"))
        fc = QVBoxLayout(grp_cookies)

        self.cb_block_3p_cookies = QCheckBox(_t("Block third-party cookies"))
        self.cb_block_3p_cookies.setChecked(_get(sm, "block_third_party_cookies", default=True))
        self.cb_block_3p_cookies.setToolTip(_t(
            "Delete third-party cookies after a set time.\n"
            "Prevents cross-site tracking."
        ))
        fc.addWidget(self.cb_block_3p_cookies)

        h_3p = QHBoxLayout()
        h_3p.addWidget(QLabel(_t("Lifetime (minutes):")))
        self.spin_3p_min = QSpinBox()
        self.spin_3p_min.setRange(0, 43200)
        self.spin_3p_min.setValue(_get(sm, "block_third_party_cookies_min", default=180))
        self.spin_3p_min.setToolTip(_t("0 = block immediately. Default: 180 minutes."))
        h_3p.addWidget(self.spin_3p_min)
        h_3p.addStretch()
        fc.addLayout(h_3p)

        self.cb_block_1p_cookies = QCheckBox(_t("Block first-party cookies"))
        self.cb_block_1p_cookies.setChecked(_get(sm, "block_first_party_cookies", default=False))
        self.cb_block_1p_cookies.setToolTip(_t(
            "Delete all cookies (including first-party) after a set time.\n"
            "Warning: this logs you out of every site."
        ))
        fc.addWidget(self.cb_block_1p_cookies)

        h_1p = QHBoxLayout()
        h_1p.addWidget(QLabel(_t("Lifetime (minutes):")))
        self.spin_1p_min = QSpinBox()
        self.spin_1p_min.setRange(0, 43200)
        self.spin_1p_min.setValue(_get(sm, "block_first_party_cookies_min", default=4320))
        self.spin_1p_min.setToolTip(_t("0 = block immediately. Default: 4320 minutes (3 days)."))
        h_1p.addWidget(self.spin_1p_min)
        h_1p.addStretch()
        fc.addLayout(h_1p)

        layout.addWidget(grp_cookies)

        # Privacy
        grp_priv = QGroupBox(_t("Privacy"))
        fp = QVBoxLayout(grp_priv)

        self.cb_hide_ua = QCheckBox(_t("Hide / reduce User-Agent"))
        self.cb_hide_ua.setChecked(_get(sm, "hide_user_agent", default=True))
        self.cb_hide_ua.setToolTip(_t(
            "Strips identifying bits from the User-Agent.\n"
            "Reduces fingerprinting."
        ))
        fp.addWidget(self.cb_hide_ua)

        self.cb_hide_search = QCheckBox(_t("Hide search queries in referrer"))
        self.cb_hide_search.setChecked(_get(sm, "hide_search_queries", default=True))
        self.cb_hide_search.setToolTip(_t(
            "Hides your search terms when clicking from a search engine to a website."
        ))
        fp.addWidget(self.cb_hide_search)

        self.cb_remove_referrer = QCheckBox(_t("Remove referrer from third-party requests"))
        self.cb_remove_referrer.setChecked(
            _get(sm, "remove_referrer_from_third_party_requests", default=True)
        )
        self.cb_remove_referrer.setToolTip(_t(
            "Prevents third-party sites from knowing which page you came from."
        ))
        fp.addWidget(self.cb_remove_referrer)

        self.cb_dnt = QCheckBox(_t("Send Do-Not-Track signal"))
        self.cb_dnt.setChecked(_get(sm, "send_do_not_track_signals", default=True))
        self.cb_dnt.setToolTip(_t(
            "Sends DNT header with requests.\n"
            "Note: Most sites ignore this, but some respect it."
        ))
        fp.addWidget(self.cb_dnt)

        self.cb_3p_cache = QCheckBox(_t("Disable third-party ETag cache"))
        self.cb_3p_cache.setChecked(_get(sm, "disable_third_party_cache", default=True))
        self.cb_3p_cache.setToolTip(_t(
            "Prevents tracking via ETag caching in third-party content."
        ))
        fp.addWidget(self.cb_3p_cache)

        self.cb_3p_auth = QCheckBox(_t("Block third-party Authorization header"))
        self.cb_3p_auth.setChecked(_get(sm, "block_third_party_authorization", default=True))
        self.cb_3p_auth.setToolTip(_t(
            "Blocks the Authorization header in third-party requests to prevent tracking."
        ))
        fp.addWidget(self.cb_3p_auth)

        self.cb_x_client = QCheckBox(_t("Remove X-Client-Data header"))
        self.cb_x_client.setChecked(_get(sm, "remove_x_client_data_header", default=True))
        self.cb_x_client.setToolTip(_t(
            "Removes the X-Client-Data header sent by Chrome to Google services."
        ))
        fp.addWidget(self.cb_x_client)

        layout.addWidget(grp_priv)

        # Browser APIs
        grp_api = QGroupBox(_t("Browser API Blocking"))
        fa = QVBoxLayout(grp_api)

        self.cb_webrtc = QCheckBox(_t("Block WebRTC"))
        self.cb_webrtc.setChecked(_get(sm, "block_web_rtc", default=False))
        self.cb_webrtc.setToolTip(_t(
            "Prevents IP leaks via WebRTC.\n"
            "May break video calls and some web apps."
        ))
        fa.addWidget(self.cb_webrtc)

        self.cb_push = QCheckBox(_t("Block Push API"))
        self.cb_push.setChecked(_get(sm, "block_browser_push_api", default=True))
        self.cb_push.setToolTip(_t("Blocks browser push notifications from websites."))
        fa.addWidget(self.cb_push)

        self.cb_location = QCheckBox(_t("Block Location API"))
        self.cb_location.setChecked(_get(sm, "block_browser_location_api", default=True))
        self.cb_location.setToolTip(_t("Prevents websites from accessing your GPS location."))
        fa.addWidget(self.cb_location)

        self.cb_flash = QCheckBox(_t("Block Flash"))
        self.cb_flash.setChecked(_get(sm, "block_browser_flash", default=True))
        self.cb_flash.setToolTip(_t("Blocks the Flash plugin."))
        fa.addWidget(self.cb_flash)

        self.cb_java = QCheckBox(_t("Block Java"))
        self.cb_java.setChecked(_get(sm, "block_browser_java", default=True))
        self.cb_java.setToolTip(_t("Disables Java plugins. JavaScript remains enabled."))
        fa.addWidget(self.cb_java)

        layout.addWidget(grp_api)

        # Anti-DPI
        grp_dpi = QGroupBox(_t("Anti-DPI"))
        fd = QVBoxLayout(grp_dpi)

        anti_dpi = _get(sm, "anti_dpi", default={})
        self.cb_anti_dpi = QCheckBox(_t("Enable Anti-DPI"))
        self.cb_anti_dpi.setChecked(_get(anti_dpi, "enabled", default=False))
        self.cb_anti_dpi.setToolTip(_t(
            "Alters outgoing packet data to bypass Deep Packet Inspection.\n"
            "Useful in countries with internet censorship."
        ))
        fd.addWidget(self.cb_anti_dpi)

        layout.addWidget(grp_dpi)
        layout.addStretch()
        return _scrollable(w)

    # ── Tab 5: Apps ───────────────────────────────────────────────────────

    def _build_apps_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)

        info = QLabel(_t(
            "<b>App filter rules</b> (auto mode only)<br>"
            "<small>"
            "<b>default</b> – filter this app fully<br>"
            "<b>bypass_https</b> – no HTTPS filtering for this app<br>"
            "<b>bypass</b> – no filtering at all (use for games with anti-cheat)<br><br>"
            "Wildcard patterns supported (e.g. <code>*steam*</code>, <code>*EasyAntiCheat*</code>).<br>"
            "Rules are evaluated top to bottom – first match wins.<br>"
            "The wildcard <code>*</code> rule should always be last."
            "</small>"
        ))
        info.setTextFormat(Qt.TextFormat.RichText)
        info.setWordWrap(True)
        layout.addWidget(info)

        # App rules table
        self.app_table = QTableWidget()
        self.app_table.setColumnCount(3)
        self.app_table.setHorizontalHeaderLabels(
            [_t("App pattern"), _t("Action"), _t("Skip outbound proxy")]
        )
        self.app_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.app_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self.app_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        self.app_table.setAlternatingRowColors(True)

        # Load existing app rules
        self._app_rules = []
        raw_apps = _get(self._data, "apps", default=[])
        for entry in raw_apps:
            if isinstance(entry, dict):
                if "include-list" in entry:
                    # Keep include-list entries as-is (not editable in table)
                    self._app_rules.append(entry)
                    continue
                self._app_rules.append(entry)

        self._populate_app_table()
        layout.addWidget(self.app_table)

        # Buttons
        btn_row = QHBoxLayout()
        btn_add = QPushButton(_t("+ Add rule"))
        btn_add.setToolTip(_t("Add a new app filter rule"))
        btn_add.clicked.connect(self._add_app_rule)
        btn_row.addWidget(btn_add)

        btn_remove = QPushButton(_t("− Remove selected"))
        btn_remove.setToolTip(_t("Remove the selected rule"))
        btn_remove.clicked.connect(self._remove_app_rule)
        btn_row.addWidget(btn_remove)

        btn_up = QPushButton(_t("↑ Move up"))
        btn_up.clicked.connect(self._move_app_rule_up)
        btn_row.addWidget(btn_up)

        btn_down = QPushButton(_t("↓ Move down"))
        btn_down.clicked.connect(self._move_app_rule_down)
        btn_row.addWidget(btn_down)

        btn_row.addStretch()
        layout.addLayout(btn_row)

        return w

    def _populate_app_table(self) -> None:
        self.app_table.setRowCount(0)
        for entry in self._app_rules:
            if "include-list" in entry:
                row = self.app_table.rowCount()
                self.app_table.insertRow(row)
                item = QTableWidgetItem(f"[include: {entry['include-list']}]")
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setToolTip(_t("Browser list included from {}",
                                   entry["include-list"]))
                self.app_table.setItem(row, 0, item)
                item2 = QTableWidgetItem("(included)")
                item2.setFlags(item2.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.app_table.setItem(row, 1, item2)
                item3 = QTableWidgetItem("")
                item3.setFlags(item3.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.app_table.setItem(row, 2, item3)
                continue

            name = entry.get("name", "")
            action = entry.get("action", "")
            skip = entry.get("skip_outbound_proxy", False)

            row = self.app_table.rowCount()
            self.app_table.insertRow(row)

            self.app_table.setItem(row, 0, QTableWidgetItem(name))

            combo = QComboBox()
            combo.addItems(["default", "bypass_https", "bypass"])
            combo.setCurrentText(action)
            combo.setToolTip(_t(
                "default: Filter fully\n"
                "bypass_https: Skip HTTPS filtering\n"
                "bypass: Skip all filtering (games, anti-cheat)"
            ))
            self.app_table.setCellWidget(row, 1, combo)

            cb = QCheckBox()
            cb.setChecked(skip)
            cb.setToolTip(_t("Don't route this app's traffic through outbound proxy"))
            # Center the checkbox
            container = QWidget()
            hl = QHBoxLayout(container)
            hl.addWidget(cb)
            hl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            hl.setContentsMargins(0, 0, 0, 0)
            self.app_table.setCellWidget(row, 2, container)

    def _add_app_rule(self) -> None:
        # Insert before the last wildcard rule
        insert_idx = len(self._app_rules)
        # Find the wildcard '*' entry and insert before it
        for i, entry in enumerate(self._app_rules):
            if isinstance(entry, dict) and entry.get("name") == "*":
                insert_idx = i
                break
        new_rule = {"name": "*new_app*", "action": "bypass", "skip_outbound_proxy": True}
        self._app_rules.insert(insert_idx, new_rule)
        self._populate_app_table()

    def _remove_app_rule(self) -> None:
        row = self.app_table.currentRow()
        if row < 0:
            return
        entry = self._app_rules[row]
        # Don't allow removing include-list or wildcard
        if isinstance(entry, dict) and ("include-list" in entry or entry.get("name") == "*"):
            QMessageBox.information(
                self, _t("Cannot remove"),
                _t("The browser include-list and wildcard (*) rule cannot be removed.")
            )
            return
        self._app_rules.pop(row)
        self._populate_app_table()

    def _move_app_rule_up(self) -> None:
        row = self.app_table.currentRow()
        if row <= 0:
            return
        self._app_rules[row - 1], self._app_rules[row] = \
            self._app_rules[row], self._app_rules[row - 1]
        self._populate_app_table()
        self.app_table.setCurrentCell(row - 1, 0)

    def _move_app_rule_down(self) -> None:
        row = self.app_table.currentRow()
        if row < 0 or row >= len(self._app_rules) - 1:
            return
        self._app_rules[row], self._app_rules[row + 1] = \
            self._app_rules[row + 1], self._app_rules[row]
        self._populate_app_table()
        self.app_table.setCurrentCell(row + 1, 0)

    # ── Tab 6: Security ───────────────────────────────────────────────────

    def _build_security_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)

        grp = QGroupBox(_t("Browsing Security"))
        form = QVBoxLayout(grp)

        sb = _get(self._data, "safebrowsing", default={})
        self.cb_safebrowsing = QCheckBox(_t("Enable Safe Browsing"))
        self.cb_safebrowsing.setChecked(_get(sb, "enabled", default=True))
        self.cb_safebrowsing.setToolTip(_t(
            "Warns about malicious and phishing websites.\n"
            "Uses AdGuard's Safe Browsing database."
        ))
        form.addWidget(self.cb_safebrowsing)

        self.cb_sb_stats = QCheckBox(_t("Send anonymous statistics"))
        self.cb_sb_stats.setChecked(_get(sb, "send_anonymous_statistics", default=False))
        self.cb_sb_stats.setToolTip(_t(
            "Send anonymous lookups to AdGuard."
        ))
        form.addWidget(self.cb_sb_stats)

        layout.addWidget(grp)

        grp2 = QGroupBox(_t("CRLite"))
        form2 = QVBoxLayout(grp2)

        cr = _get(self._data, "crlite", default={})
        self.cb_crlite = QCheckBox(_t("Enable CRLite"))
        self.cb_crlite.setChecked(_get(cr, "enabled", default=True))
        self.cb_crlite.setToolTip(_t(
            "Certificate revocation checking using Mozilla's CRLite.\n"
            "Faster and more reliable than traditional CRL/OCSP checks."
        ))
        form2.addWidget(self.cb_crlite)

        layout.addWidget(grp2)

        # Ad blocking
        grp3 = QGroupBox(_t("Content Filtering"))
        form3 = QVBoxLayout(grp3)

        self.cb_adblocking = QCheckBox(_t("Enable ad blocking"))
        self.cb_adblocking.setChecked(
            _get(self._data, "ad_blocking_enabled", default=True)
        )
        self.cb_adblocking.setToolTip(_t(
            "Apply ad-blocking filter rules to HTTP/HTTPS requests."
        ))
        form3.addWidget(self.cb_adblocking)

        layout.addWidget(grp3)
        layout.addStretch()
        return _scrollable(w)

    # ── Collect values from UI → dict ─────────────────────────────────────

    def _collect(self) -> dict:
        d = self._data

        # Proxy
        d["proxy_mode"] = self.combo_proxy_mode.currentText()
        d["filtered_ports"] = _raw_value(self.edit_filtered_ports)
        _set(d, "listen_ports", "socks5_proxy", self.spin_socks5.value())
        _set(d, "listen_ports", "http_proxy", self.spin_http.value())
        d["listen_address"] = _raw_value(self.edit_listen_addr)
        d["worker_threads"] = self.spin_workers.value()

        # HTTPS
        _set(d, "https_filtering", "enabled", self.cb_https.isChecked())
        _set(d, "https_filtering", "enable_tls13", self.cb_tls13.isChecked())
        _set(d, "https_filtering", "http3_filtering_enabled", self.cb_http3.isChecked())
        _set(d, "https_filtering", "ocsp_check_enabled", self.cb_ocsp.isChecked())
        _set(d, "https_filtering", "enforce_certificate_transparency", self.cb_ct.isChecked())
        _set(d, "https_filtering", "filter_ev_certificates", self.cb_ev.isChecked())
        _set(d, "https_filtering", "encrypted_client_hello", self.cb_ech.isChecked())
        _set(d, "https_filtering", "filter_secure_dns_mode", self.combo_sdns.currentText())

        # DNS
        _set(d, "dns_filtering", "enabled", self.cb_dns.isChecked())
        _set(d, "dns_filtering", "upstream", _raw_value(self.edit_dns_upstream))
        _set(d, "dns_filtering", "fallbacks", _raw_value(self.edit_dns_fallback))
        _set(d, "dns_filtering", "bootstraps", _raw_value(self.edit_dns_bootstrap))
        _set(d, "dns_filtering", "block_ech", self.cb_block_ech.isChecked())

        # Stealth
        _set(d, "stealthmode", "enabled", self.cb_stealth.isChecked())
        _set(d, "stealthmode", "block_third_party_cookies", self.cb_block_3p_cookies.isChecked())
        _set(d, "stealthmode", "block_third_party_cookies_min", self.spin_3p_min.value())
        _set(d, "stealthmode", "block_first_party_cookies", self.cb_block_1p_cookies.isChecked())
        _set(d, "stealthmode", "block_first_party_cookies_min", self.spin_1p_min.value())
        _set(d, "stealthmode", "hide_user_agent", self.cb_hide_ua.isChecked())
        _set(d, "stealthmode", "hide_search_queries", self.cb_hide_search.isChecked())
        _set(d, "stealthmode", "remove_referrer_from_third_party_requests",
             self.cb_remove_referrer.isChecked())
        _set(d, "stealthmode", "send_do_not_track_signals", self.cb_dnt.isChecked())
        _set(d, "stealthmode", "disable_third_party_cache", self.cb_3p_cache.isChecked())
        _set(d, "stealthmode", "block_third_party_authorization", self.cb_3p_auth.isChecked())
        _set(d, "stealthmode", "remove_x_client_data_header", self.cb_x_client.isChecked())
        _set(d, "stealthmode", "block_web_rtc", self.cb_webrtc.isChecked())
        _set(d, "stealthmode", "block_browser_push_api", self.cb_push.isChecked())
        _set(d, "stealthmode", "block_browser_location_api", self.cb_location.isChecked())
        _set(d, "stealthmode", "block_browser_flash", self.cb_flash.isChecked())
        _set(d, "stealthmode", "block_browser_java", self.cb_java.isChecked())
        _set(d, "stealthmode", "anti_dpi", "enabled", self.cb_anti_dpi.isChecked())

        # Apps – read back from table
        apps = []
        for row in range(self.app_table.rowCount()):
            # Check if it's an include-list row
            item0 = self.app_table.item(row, 0)
            if item0 and item0.text().startswith("[include:"):
                # Table rows mirror self._app_rules 1:1 (see _populate_app_table)
                apps.append(self._app_rules[row])
                continue

            name = item0.text().strip() if item0 else ""
            if not name:
                continue

            combo = self.app_table.cellWidget(row, 1)
            action = combo.currentText() if isinstance(combo, QComboBox) else ""

            container = self.app_table.cellWidget(row, 2)
            skip = False
            if container:
                cb = container.findChild(QCheckBox)
                if cb:
                    skip = cb.isChecked()

            entry = {"name": name, "action": action}
            if skip:
                entry["skip_outbound_proxy"] = True
            apps.append(entry)
        d["apps"] = apps

        # Security
        _set(d, "safebrowsing", "enabled", self.cb_safebrowsing.isChecked())
        _set(d, "safebrowsing", "send_anonymous_statistics", self.cb_sb_stats.isChecked())
        _set(d, "crlite", "enabled", self.cb_crlite.isChecked())
        d["ad_blocking_enabled"] = self.cb_adblocking.isChecked()

        return d

    # ── Save ──────────────────────────────────────────────────────────────

    def _save(self) -> None:
        data = self._collect()
        ok, err = _save_yaml(data)
        if ok:
            self.accept()
        else:
            QMessageBox.critical(
                self,
                _t("Save failed"),
                _t("Could not save proxy.yaml:\n{}", err),
            )
