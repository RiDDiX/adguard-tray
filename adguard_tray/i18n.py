"""
Lightweight internationalisation.

Detects the system locale and provides a ``_t()`` translation function.
English is the default language; additional translations are stored as
simple dictionaries.  Falls back to the English key when no translation
exists for the active locale.
"""

import locale
import os

# ── Locale detection ──────────────────────────────────────────────────────

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
                return lang
    except Exception:
        pass

    # Fall back to system locale
    for var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        val = os.environ.get(var, "")
        if val:
            lang = val.split("_")[0].split(".")[0].split(":")[0].lower()
            if lang and lang not in ("c", "posix"):
                return lang
    try:
        lang, _ = locale.getlocale()
        if lang:
            return lang.split("_")[0].lower()
    except (ValueError, AttributeError):
        pass
    return "en"


_LANG = _detect_language()

# ── German translations ───────────────────────────────────────────────────

_DE: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "Sprache",
    "Auto (system locale)":              "Automatisch (Systemsprache)",
    "English":                           "Englisch",
    "Simplified Chinese":                "Chinesisch (Vereinfacht)",
    "German":                            "Deutsch",
    "Requires application restart to take effect.":
        "Erfordert einen Neustart der Anwendung.",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "Aktiv – Schutz läuft",
    "Inactive – Protection stopped":        "Inaktiv – Schutz gestoppt",
    "Error retrieving status":              "Fehler beim Statusabruf",
    "adguard-cli not found":                "adguard-cli nicht gefunden",
    "Unknown status":                       "Status unbekannt",
    "Checking status…":                     "Status wird abgefragt…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Toggle":                               "Umschalten",
    "Enable":                               "Aktivieren",
    "Disable":                              "Deaktivieren",
    "Restart":                              "Neu starten",
    "Filters":                              "Filter",
    "Loading…":                             "Wird geladen…",
    "Manage filters…":                      "Filter verwalten…",
    "No userscripts installed":             "Keine Userscripts installiert",
    "Manage userscripts…":                  "Userscripts verwalten…",
    "Refresh status":                       "Status aktualisieren",
    "Settings…":                            "Einstellungen…",
    "Autostart on login":                   "Autostart beim Login",
    "Quit":                                 "Beenden",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "aktiv",
    "inactive":                             "inaktiv",
    "System-wide filtering: {}":            "Systemweites Filtern: {}",
    "Error: {}":                            "Fehler: {}",
    "AdGuard Tray – Error":                 "AdGuard Tray – Fehler",
    "AdGuard is now active – protection running.":
        "AdGuard ist jetzt aktiv – Schutz läuft.",
    "AdGuard has been stopped.":
        "AdGuard wurde gestoppt.",
    "Could not retrieve status.":
        "Status konnte nicht abgerufen werden.",
    "Command failed":                       "Befehl fehlgeschlagen",

    # ── settings_dialog.py ────────────────────────────────────────────────
    "AdGuard Tray – Settings":              "AdGuard Tray – Einstellungen",
    "Status Refresh":                       "Status-Aktualisierung",
    " seconds":                             " Sekunden",
    "How often adguard-cli status is checked automatically.":
        "Wie häufig der Status von adguard-cli automatisch abgefragt wird.",
    "Interval:":                            "Intervall:",
    "Log level:":                           "Log-Level:",
    "adguard-cli path:":                    "adguard-cli-Pfad:",
    "auto-detect via PATH":                 "automatisch via PATH",
    "Browse…":                              "Durchsuchen…",
    "Select adguard-cli binary":            "adguard-cli-Binary auswählen",
    "Notifications":                        "Benachrichtigungen",
    "Desktop notification on status change":
        "Desktop-Benachrichtigung bei Statusänderung",
    "<small>Requires <i>libnotify</i> / <i>notify-send</i> or an "
    "active notification service (dunst, mako, KDE).</small>":
        "<small>Benötigt <i>libnotify</i> / <i>notify-send</i> oder einen "
        "aktiven Benachrichtigungsdienst (dunst, mako, KDE).</small>",
    "Autostart":                            "Autostart",
    "Start automatically on desktop login (XDG Autostart)":
        "Beim Desktop-Login automatisch starten (XDG Autostart)",
    "<small>Creates <i>~/.config/autostart/adguard-tray.desktop</i>.<br>"
    "Works on KDE Plasma, GNOME, Hyprland (with xdg-autostart-impl) "
    "and other XDG-compliant environments.</small>":
        "<small>Erstellt <i>~/.config/autostart/adguard-tray.desktop</i>.<br>"
        "Funktioniert auf KDE Plasma, GNOME, Hyprland (mit xdg-autostart-impl) "
        "und anderen XDG-konformen Umgebungen.</small>",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "Filter aktualisieren",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "Aktualisiert alle Filter, DNS-Filter, Userscripts,\n"
        "SafebrowsingV2, CRLite und prüft auf App-Updates.",
    "Add custom filter…":                   "Eigenen Filter hinzufügen…",
    "Install custom filter by URL":         "Custom-Filter per URL installieren",
    "↺ Reload":                             "↺ Neu laden",
    "Loading filters…":                     "Filter werden geladen…",
    "No filters found.":                    "Keine Filter gefunden.",
    "{} of {} filters active":              "{} von {} Filtern aktiv",
    "Filter":                               "Filter",
    "ID":                                   "ID",
    "Last updated":                         "Zuletzt aktualisiert",
    "Enabling filter {}…":                  "Filter {} wird aktiviert…",
    "Disabling filter {}…":                 "Filter {} wird deaktiviert…",
    "Updating filters…":                    "Filter werden aktualisiert…",
    "Updating filters… (can take up to 2 minutes)":
        "Filter werden aktualisiert… (kann bis zu 2 Minuten dauern)",
    "Update completed.":                    "Aktualisierung abgeschlossen.",
    "Update failed.":                       "Aktualisierung fehlgeschlagen.",
    "Add Custom Filter":                    "Eigenen Filter hinzufügen",
    "Installing: {}":                       "Installiere: {}",
    "Filter installed.":                    "Filter installiert.",
    "Remove":                               "Entfernen",
    "Remove filter":                        "Filter entfernen",
    'Really remove filter "{}"?':           'Filter «{}» wirklich entfernen?',
    "Removing filter {}…":                  "Filter {} wird entfernt…",
    "Filter {} removed.":                   "Filter {} entfernt.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install (URL)…":                       "Installieren (URL)…",
    "Install userscript from a direct .js URL":
        "Userscript von einer direkten .js-URL installieren",
    "Userscript":                           "Userscript",
    "ID / Name":                            "ID / Name",
    "<small>Right-click a userscript to remove it.<br>"
    "Userscripts are automatically updated when running "
    "<i>Update filters</i>.</small>":
        "<small>Rechtsklick auf ein Userscript zum Entfernen.<br>"
        "Userscripts werden bei <i>Filter aktualisieren</i> "
        "automatisch mit aktualisiert.</small>",
    "Loading userscripts…":                 "Userscripts werden geladen…",
    "No userscripts installed.":            "Keine Userscripts installiert.",
    "{} of {} userscripts active":          "{} von {} Userscripts aktiv",
    "Userscript '{}' enabled.":             "Userscript '{}' aktiviert.",
    "Userscript '{}' disabled.":            "Userscript '{}' deaktiviert.",
    "Install Userscript":                   "Userscript installieren",
    "Userscript URL (direct .js URL):":     "Userscript-URL (direkte .js-URL):",
    "Userscript installed.":                "Userscript installiert.",
    'Remove "{}"':                          '«{}» entfernen',
    "Remove userscript":                    "Userscript entfernen",
    'Really remove userscript "{}"?':       'Userscript «{}» wirklich entfernen?',
    "'{}' removed.":                        "'{}' entfernt.",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "adguard-cli wurde nicht gefunden.\n"
        "Installation über offizielles Skript oder AUR:\n"
        "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
        "  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "Unbekannter Fehler beim Statusabruf",
    "AdGuard {} ok":                        "AdGuard {} ok",
    "AdGuard via systemctl {} ok":          "AdGuard via systemctl {} ok",
    "'{}' failed – insufficient privileges?":
        "'{}' fehlgeschlagen – Rechte unzureichend?",
    "Could not retrieve filter list":
        "Filter-Liste konnte nicht abgerufen werden",
    "Filter {} enabled":                    "Filter {} aktiviert",
    "Could not enable filter {}":           "Filter {} konnte nicht aktiviert werden",
    "Filter {} disabled":                   "Filter {} deaktiviert",
    "Could not disable filter {}":
        "Filter {} konnte nicht deaktiviert werden",
    "Filter installed":                     "Filter installiert",
    "Installation failed":                  "Installation fehlgeschlagen",
    "Filter {} removed":                    "Filter {} entfernt",
    "Could not remove filter {}":
        "Filter {} konnte nicht entfernt werden",
    "Filters updated":                      "Filter aktualisiert",
    "Update failed":                        "Update fehlgeschlagen",
    "Could not retrieve userscript list":
        "Userscript-Liste konnte nicht abgerufen werden",
    "Userscript '{}' enabled":              "Userscript '{}' aktiviert",
    "Could not enable userscript '{}'":
        "Userscript '{}' konnte nicht aktiviert werden",
    "Userscript '{}' disabled":             "Userscript '{}' deaktiviert",
    "Could not disable userscript '{}'":
        "Userscript '{}' konnte nicht deaktiviert werden",
    "Userscript '{}' removed":              "Userscript '{}' entfernt",
    "Could not remove userscript '{}'":
        "Userscript '{}' konnte nicht entfernt werden",
    "Userscript installed":                 "Userscript installiert",
    "Other":                                "Sonstige",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "Filter durchsuchen…",
    "Search userscripts…":              "Userscripts durchsuchen…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "AdGuard CLI – Configuration":      "AdGuard CLI – Konfiguration",
    "Could not load proxy.yaml.\nPath: {}":
        "proxy.yaml konnte nicht geladen werden.\nPfad: {}",
    "Proxy":                            "Proxy",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Stealth Mode":                     "Tarnmodus",
    "Apps":                             "Apps",
    "Security":                         "Sicherheit",
    "<small><b>Note:</b> Changes require an AdGuard CLI restart to take effect.</small>":
        "<small><b>Hinweis:</b> Änderungen erfordern einen Neustart von AdGuard CLI.</small>",
    "Proxy Mode":                       "Proxy-Modus",
    "Mode:":                            "Modus:",
    "auto: AdGuard redirects app traffic into itself via iptables\n"
    "manual: Only listens on the configured proxy ports (SOCKS5/HTTP)":
        "auto: AdGuard leitet App-Traffic via iptables um\n"
        "manual: Lauscht nur auf den konfigurierten Proxy-Ports (SOCKS5/HTTP)",
    "Filtered ports:":                  "Gefilterte Ports:",
    "Port ranges intercepted in auto mode.\n"
    "Format: 80:5221,5300:49151 (range) or 80,443,8080 (individual)\n"
    "Only applies when proxy mode is 'auto'.":
        "Port-Bereiche die im Auto-Modus abgefangen werden.\n"
        "Format: 80:5221,5300:49151 (Bereich) oder 80,443,8080 (einzeln)\n"
        "Gilt nur im Proxy-Modus 'auto'.",
    "Manual Proxy Ports":               "Manuelle Proxy-Ports",
    "SOCKS5 port:":                     "SOCKS5-Port:",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "SOCKS5-Proxy-Port für den manuellen Modus.\n-1 zum Deaktivieren.",
    "HTTP port:":                       "HTTP-Port:",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "HTTP-Proxy-Port für den manuellen Modus.\n-1 zum Deaktivieren.",
    "Listen address:":                  "Lausch-Adresse:",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "Adresse auf der der Proxy lauscht.\n"
        "127.0.0.1 = nur lokal. 0.0.0.0 = alle Interfaces (erfordert Authentifizierung).",
    "Worker threads:":                  "Worker-Threads:",
    "Number of proxy worker threads.":  "Anzahl der Proxy-Worker-Threads.",
    "HTTPS Filtering":                  "HTTPS-Filterung",
    "Enable HTTPS filtering":           "HTTPS-Filterung aktivieren",
    "Decrypt and filter HTTPS traffic.\n"
    "Needed to block ads on https sites.\n"
    "Requires a trusted root certificate installed on the system.":
        "HTTPS-Traffic entschlüsseln und filtern.\n"
        "Nötig, um Werbung auf https-Seiten zu blockieren.\n"
        "Benötigt ein installiertes Root-Zertifikat auf dem System.",
    "Enable TLS 1.3":                   "TLS 1.3 aktivieren",
    "Enable TLS 1.3 support for filtered connections.":
        "TLS 1.3 für gefilterte Verbindungen aktivieren.",
    "Filter HTTP/3 (QUIC) – experimental":
        "HTTP/3 (QUIC) filtern – experimentell",
    "Filter HTTP/3 (QUIC) traffic.\nExperimental – may cause issues with some sites.":
        "HTTP/3 (QUIC)-Traffic filtern.\nExperimentell – kann bei manchen Seiten Probleme verursachen.",
    "OCSP certificate checks":          "OCSP-Zertifikatsprüfung",
    "Check certificate revocation status via OCSP.\n"
    "Slower but more secure.":
        "Zertifikatswiderruf per OCSP prüfen.\n"
        "Langsamer, aber sicherer.",
    "Enforce Certificate Transparency": "Certificate Transparency erzwingen",
    "Enforce Certificate Transparency timestamp checks.\n"
    "Similar to Chrome's built-in CT policy.":
        "Certificate-Transparency-Prüfungen erzwingen.\n"
        "Ähnlich der CT-Richtlinie von Chrome.",
    "Filter EV certificate sites":      "EV-Zertifikat-Seiten filtern",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "Standardmäßig werden Seiten mit EV-Zertifikaten nicht gefiltert.\n"
        "Aktivieren um auch diese zu filtern (z.B. Banking-Seiten).",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "ECH für besseren Datenschutz aktivieren.\nErfordert aktivierte DNS-Filterung.",
    "Secure DNS Filtering":             "Sichere DNS-Filterung",
    "off: No secure DNS filtering\n"
    "transparent: Filter DoH/DoT inline without changing destination\n"
    "redirect: Redirect all secure DNS to the local DNS proxy":
        "off: Keine sichere DNS-Filterung\n"
        "transparent: DoH/DoT inline filtern ohne Ziel zu ändern\n"
        "redirect: Alle sichere DNS-Anfragen zum lokalen DNS-Proxy umleiten",
    "DNS Filtering":                    "DNS-Filterung",
    "Enable DNS filtering":             "DNS-Filterung aktivieren",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "DNS-Anfragen filtern um Werbung und Tracker auf DNS-Ebene zu blockieren.\n"
        "Nutzt einen lokalen DNS-Proxy mit konfigurierbaren Upstreams.",
    "Upstream:":                        "Upstream:",
    "DNS upstream server.\n'default' = system DNS\n"
    "Examples: 1.1.1.1, https://dns.google/dns-query,\n"
    "tls://dns.adguard.com, quic://dns.adguard.com":
        "DNS-Upstream-Server.\n'default' = System-DNS\n"
        "Beispiele: 1.1.1.1, https://dns.google/dns-query,\n"
        "tls://dns.adguard.com, quic://dns.adguard.com",
    "Fallbacks:":                       "Fallbacks:",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "Fallback-DNS-Server (wenn primärer Upstream ausfällt).\n"
        "'default' = System-DNS. Leerzeichen-getrennte Liste.\n"
        "Beispiel: default 1.1.1.1",
    "Bootstraps:":                      "Bootstraps:",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "Bootstrap-DNS zum Auflösen von Upstream-Hostnamen.\n"
        "'default' = System-DNS-IPs. Nur IP-Adressen erlaubt.\n"
        "Beispiel: default 8.8.8.8 tls://1.1.1.1",
    "Block ECH in DNS":                 "ECH in DNS blockieren",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "ECH-Parameter aus SVCB/HTTPS-DNS-Einträgen entfernen.\n"
        "Nur aktivieren für Browser, die HTTPS-Filterung nicht automatisch erkennen.",
    "Stealth Mode (Tracking Protection)":
        "Tarnmodus (Tracking-Schutz)",
    "Enable Stealth Mode":              "Tarnmodus aktivieren",
    "Master switch for all tracking protection features below.":
        "Hauptschalter für alle folgenden Tracking-Schutz-Funktionen.",
    "Cookies":                          "Cookies",
    "Block third-party cookies":        "Drittanbieter-Cookies blockieren",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "Drittanbieter-Cookies nach einer bestimmten Zeit löschen.\nVerhindert Cross-Site-Tracking.",
    "Lifetime (minutes):":              "Lebensdauer (Minuten):",
    "0 = block immediately. Default: 180 minutes.":
        "0 = sofort blockieren. Standard: 180 Minuten.",
    "Block first-party cookies":        "Erstanbieter-Cookies blockieren",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "Alle Cookies (inkl. Erstanbieter) nach einer bestimmten Zeit löschen.\n"
        "Warnung: du wirst überall ausgeloggt.",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = sofort blockieren. Standard: 4320 Minuten (3 Tage).",
    "Privacy":                          "Privatsphäre",
    "Hide / reduce User-Agent":         "User-Agent verstecken / reduzieren",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "Kürzt den User-Agent.\n"
        "Hilft gegen Fingerprinting.",
    "Hide search queries in referrer":  "Suchanfragen im Referrer verstecken",
    "Hides your search terms when clicking from a search engine to a website.":
        "Versteckt deine Suchbegriffe beim Klick von einer Suchmaschine auf eine Webseite.",
    "Remove referrer from third-party requests":
        "Referrer aus Drittanbieter-Anfragen entfernen",
    "Prevents third-party sites from knowing which page you came from.":
        "Verhindert, dass Drittanbieter-Seiten sehen, von welcher Seite du kommst.",
    "Send Do-Not-Track signal":         "Do-Not-Track-Signal senden",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "Sendet DNT-Header mit Anfragen.\nHinweis: Die meisten Seiten ignorieren dies.",
    "Disable third-party ETag cache":   "Drittanbieter-ETag-Cache deaktivieren",
    "Prevents tracking via ETag caching in third-party content.":
        "Verhindert Tracking über ETag-Caching bei Drittanbieter-Inhalten.",
    "Block third-party Authorization header":
        "Drittanbieter-Authorization-Header blockieren",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "Blockiert den Authorization-Header bei Drittanbieter-Anfragen.",
    "Remove X-Client-Data header":      "X-Client-Data-Header entfernen",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "Entfernt den X-Client-Data-Header den Chrome an Google-Dienste sendet.",
    "Browser API Blocking":             "Browser-API-Blockierung",
    "Block WebRTC":                     "WebRTC blockieren",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "Verhindert IP-Leaks über WebRTC.\nKann Videoanrufe und Web-Apps stören.",
    "Block Push API":                   "Push-API blockieren",
    "Blocks browser push notifications from websites.":
        "Blockiert Browser-Push-Benachrichtigungen von Webseiten.",
    "Block Location API":               "Standort-API blockieren",
    "Prevents websites from accessing your GPS location.":
        "Verhindert den Zugriff von Webseiten auf deinen GPS-Standort.",
    "Block Flash":                      "Flash blockieren",
    "Blocks the Flash plugin.":
        "Blockiert das Flash-Plugin.",
    "Block Java":                       "Java blockieren",
    "Disables Java plugins. JavaScript remains enabled.":
        "Deaktiviert Java-Plugins. JavaScript bleibt aktiviert.",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "Anti-DPI aktivieren",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\n"
    "Useful in countries with internet censorship.":
        "Verändert ausgehende Paketdaten um Deep Packet Inspection zu umgehen.\n"
        "Nützlich in Ländern mit Internet-Zensur.",
    "App pattern":                      "App-Muster",
    "Action":                           "Aktion",
    "Skip outbound proxy":              "Ausgehenden Proxy umgehen",
    "default: Filter fully\n"
    "bypass_https: Skip HTTPS filtering\n"
    "bypass: Skip all filtering (games, anti-cheat)":
        "default: Vollständig filtern\n"
        "bypass_https: HTTPS-Filterung überspringen\n"
        "bypass: Gesamte Filterung überspringen (Spiele, Anti-Cheat)",
    "Don't route this app's traffic through outbound proxy":
        "Traffic dieser App nicht über den ausgehenden Proxy leiten",
    "Browser list included from {}":    "Browser-Liste eingebunden aus {}",
    "+ Add rule":                        "+ Regel hinzufügen",
    "Add a new app filter rule":        "Neue App-Filterregel hinzufügen",
    "− Remove selected":                "− Ausgewählte entfernen",
    "Remove the selected rule":         "Ausgewählte Regel entfernen",
    "↑ Move up":                        "↑ Nach oben",
    "↓ Move down":                      "↓ Nach unten",
    "Cannot remove":                    "Kann nicht entfernt werden",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "Die Browser-Include-Liste und die Wildcard-Regel (*) können nicht entfernt werden.",
    "Browsing Security":                "Browser-Sicherheit",
    "Enable Safe Browsing":             "Safe Browsing aktivieren",
    "Warns about malicious and phishing websites.\n"
    "Uses AdGuard's Safe Browsing database.":
        "Warnt vor bösartigen und Phishing-Webseiten.\n"
        "Nutzt die Safe-Browsing-Datenbank von AdGuard.",
    "Send anonymous statistics":        "Anonyme Statistiken senden",
    "Send anonymous lookups to AdGuard.":
        "Anonyme Abfragen an AdGuard schicken.",
    "CRLite":                           "CRLite",
    "Enable CRLite":                    "CRLite aktivieren",
    "Certificate revocation checking using Mozilla's CRLite.\n"
    "Faster and more reliable than traditional CRL/OCSP checks.":
        "Zertifikatswiderrufsprüfung mit Mozillas CRLite.\n"
        "Schneller und zuverlässiger als herkömmliche CRL/OCSP-Prüfungen.",
    "Content Filtering":                "Inhaltsfilterung",
    "Enable ad blocking":               "Werbeblocker aktivieren",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "Werbeblockierungsregeln auf HTTP/HTTPS-Anfragen anwenden.",
    "Save failed":                      "Speichern fehlgeschlagen",
    "Could not save proxy.yaml:\n{}":   "proxy.yaml konnte nicht gespeichert werden:\n{}",
    "Configuration saved. Restart AdGuard to apply changes.":
        "Konfiguration gespeichert. AdGuard neu starten um Änderungen anzuwenden.",
    "Restarting AdGuard…":              "AdGuard wird neu gestartet…",
    "AdGuard restarted.":               "AdGuard neu gestartet.",
    "Restart failed: {}":               "Neustart fehlgeschlagen: {}",
    "Unknown error":                    "Unbekannter Fehler",
    "AdGuard Configuration…":           "AdGuard-Konfiguration…",
    "<b>App filter rules</b> (auto mode only)<br>"
    "<small>"
    "<b>default</b> – filter this app fully<br>"
    "<b>bypass_https</b> – no HTTPS filtering for this app<br>"
    "<b>bypass</b> – no filtering at all (use for games with anti-cheat)<br><br>"
    "Wildcard patterns supported (e.g. <code>*steam*</code>, <code>*EasyAntiCheat*</code>).<br>"
    "Rules are evaluated top to bottom – first match wins.<br>"
    "The wildcard <code>*</code> rule should always be last."
    "</small>":
        "<b>App-Filterregeln</b> (nur im Auto-Modus)<br>"
        "<small>"
        "<b>default</b> – App vollständig filtern<br>"
        "<b>bypass_https</b> – keine HTTPS-Filterung für diese App<br>"
        "<b>bypass</b> – keine Filterung (für Spiele mit Anti-Cheat)<br><br>"
        "Wildcard-Muster möglich (z.B. <code>*steam*</code>, <code>*EasyAntiCheat*</code>).<br>"
        "Regeln werden von oben nach unten ausgewertet – erster Treffer gewinnt.<br>"
        "Die Wildcard-Regel <code>*</code> sollte immer am Ende stehen."
        "</small>",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Website Exceptions…":              "Website-Ausnahmen…",
    "AdGuard Tray – Website Exceptions":
        "AdGuard Tray – Website-Ausnahmen",
    "<small>Websites listed here will not have ads or trackers blocked.<br>"
    "Enter a domain (e.g. <code>example.com</code>) without <code>https://</code>.</small>":
        "<small>Für hier gelistete Websites werden keine Werbung oder Tracker blockiert.<br>"
        "Domain eingeben (z.B. <code>example.com</code>) ohne <code>https://</code>.</small>",
    "example.com":                      "beispiel.de",
    "Add":                              "Hinzufügen",
    "Search exceptions…":               "Ausnahmen durchsuchen…",
    "Remove selected":                  "Ausgewählte entfernen",
    "1 exception":                      "1 Ausnahme",
    "{} exceptions":                    "{} Ausnahmen",
    "Invalid domain":                   "Ungültige Domain",
    "Invalid URL":                      "Ungültige URL",
    "'{}' is not a valid domain or IP address.":
        "'{}' ist keine gültige Domain oder IP-Adresse.",
    "'{}' is already in the list.":     "'{}' ist bereits in der Liste.",
    "Could not save exceptions:\n{}":
        "Ausnahmen konnten nicht gespeichert werden:\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "AdGuard Tray – Manager":           "AdGuard Tray – Manager",
    "Overview":                         "Übersicht",
    "DNS Filters":                      "DNS-Filter",
    "Userscripts":                      "Userscripts",
    "Exceptions":                       "Ausnahmen",
    "Configuration":                    "Konfiguration",
    "Diagnostics":                      "Diagnose",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Status":                           "Status",
    "↺ Refresh":                        "↺ Aktualisieren",
    "Version & License":                "Version & Lizenz",
    "Check for CLI update":             "Auf CLI-Update prüfen",
    "Reset license":                    "Lizenz zurücksetzen",
    "HTTPS Certificate":                "HTTPS-Zertifikat",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "Root-CA-Zertifikat für HTTPS-Filterung generieren. "
        "Das Zertifikat muss auf dem System installiert und als vertrauenswürdig eingestuft werden.",
    "Generate certificate":             "Zertifikat generieren",
    "Checking for updates…":            "Suche nach Updates…",
    "Are you sure you want to reset the AdGuard license?":
        "Möchtest du die AdGuard-Lizenz wirklich zurücksetzen?",
    "Generating certificate…":          "Zertifikat wird generiert…",
    "Firefox profile:":                 "Firefox-Profil:",
    "(optional) e.g. abcd1234.MyProfile":
        "(optional) z.B. abcd1234.MeinProfil",
    "License: {}":                      "Lizenz: {}",
    "Could not retrieve":               "Konnte nicht abgerufen werden",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Add by ID…":                       "Nach ID hinzufügen…",
    "Add internal filter by ID or name":
        "Internen Filter nach ID oder Name hinzufügen",
    "Show all available":               "Alle verfügbaren anzeigen",
    "Show all available filters, not just installed ones":
        "Alle verfügbaren Filter anzeigen, nicht nur installierte",
    "Add Filter by ID":                 "Filter nach ID hinzufügen",
    "Enter filter ID or name:":         "Filter-ID oder Name eingeben:",
    "Adding filter: {}":                "Filter wird hinzugefügt: {}",
    "Filter added.":                    "Filter hinzugefügt.",
    "Rename…":                          "Umbenennen…",
    "Set trusted":                      "Als vertrauenswürdig markieren",
    "Set untrusted":                    "Als nicht vertrauenswürdig markieren",
    "Rename filter":                    "Filter umbenennen",
    "New title:":                       "Neuer Titel:",
    "Renaming filter {}…":              "Filter {} wird umbenannt…",
    "Filter renamed.":                  "Filter umbenannt.",
    "trusted":                          "vertrauenswürdig",
    "untrusted":                        "nicht vertrauenswürdig",
    "Setting filter {} as {}…":         "Filter {} wird als {} gesetzt…",
    "Filter trust updated.":            "Filtervertrauen aktualisiert.",
    "Filter URL:":                      "Filter-URL:",
    "Title:":                           "Titel:",
    "(optional)":                       "(optional)",
    "Trusted filter":                   "Vertrauenswürdiger Filter",
    "Trusted filters can use advanced rules (JS scriptlets, etc.)":
        "Vertrauenswürdige Filter können erweiterte Regeln verwenden (JS-Scriptlets, etc.)",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Add custom DNS filter…":           "Eigenen DNS-Filter hinzufügen…",
    "Search DNS filters…":              "DNS-Filter durchsuchen…",
    "DNS filters block domains at the DNS level. "
    "Requires DNS filtering to be enabled in Configuration → DNS.":
        "DNS-Filter blockieren Domains auf DNS-Ebene. "
        "Erfordert aktivierte DNS-Filterung in Konfiguration → DNS.",
    "Loading DNS filters…":             "DNS-Filter werden geladen…",
    "No DNS filters found.":            "Keine DNS-Filter gefunden.",
    "{} of {} DNS filters active":      "{} von {} DNS-Filtern aktiv",
    "DNS filter installed.":            "DNS-Filter installiert.",
    "Add DNS Filter by ID":             "DNS-Filter nach ID hinzufügen",
    "Adding DNS filter: {}":            "DNS-Filter wird hinzugefügt: {}",
    "DNS filter added.":                "DNS-Filter hinzugefügt.",
    "Remove DNS filter":                "DNS-Filter entfernen",
    'Really remove DNS filter "{}"?':   'DNS-Filter «{}» wirklich entfernen?',
    "DNS filter {} removed.":           "DNS-Filter {} entfernt.",
    "Rename DNS filter":                "DNS-Filter umbenennen",
    "DNS filter renamed.":              "DNS-Filter umbenannt.",
    "Add Custom DNS Filter":            "Eigenen DNS-Filter hinzufügen",

    # ── config_tab.py ────────────────────────────────────────────────────
    "Could not load proxy.yaml.":       "proxy.yaml konnte nicht geladen werden.",
    "Edit the full AdGuard CLI configuration (proxy.yaml).":
        "Die vollständige AdGuard-CLI-Konfiguration (proxy.yaml) bearbeiten.",
    "Open Configuration Editor…":       "Konfigurations-Editor öffnen…",

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export & Import":                  "Export & Import",
    "Export logs…":                     "Logs exportieren…",
    "Export AdGuard CLI logs to a zip file":
        "AdGuard-CLI-Logs in eine ZIP-Datei exportieren",
    "Export settings…":                 "Einstellungen exportieren…",
    "Export all AdGuard CLI settings to a zip file":
        "Alle AdGuard-CLI-Einstellungen in eine ZIP-Datei exportieren",
    "Import settings…":                 "Einstellungen importieren…",
    "Import settings from a previously exported zip file":
        "Einstellungen aus einer zuvor exportierten ZIP-Datei importieren",
    "Performance Benchmark":            "Leistungs-Benchmark",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "Einen kryptografischen und HTTPS-Filterungs-Benchmark ausführen.",
    "Run benchmark":                    "Benchmark starten",
    "Running benchmark…":               "Benchmark wird ausgeführt…",
    "Done.":                            "Fertig.",
    "Failed.":                          "Fehlgeschlagen.",
    "Export logs to…":                  "Logs exportieren nach…",
    "Exporting logs…":                  "Logs werden exportiert…",
    "Export settings to…":              "Einstellungen exportieren nach…",
    "Exporting settings…":              "Einstellungen werden exportiert…",
    "Import settings from…":            "Einstellungen importieren aus…",
    "Zip files (*.zip);;All files (*)":
        "ZIP-Dateien (*.zip);;Alle Dateien (*)",
    "Importing settings…":              "Einstellungen werden importiert…",
    "Application Log":                  "Anwendungs-Log",
    "View recent log entries":          "Letzte Log-Einträge anzeigen",
    "Log file not found.":              "Log-Datei nicht gefunden.",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "DNS-Filter-Liste konnte nicht abgerufen werden",
    "DNS filter {} enabled":            "DNS-Filter {} aktiviert",
    "Could not enable DNS filter {}":   "DNS-Filter {} konnte nicht aktiviert werden",
    "DNS filter {} disabled":           "DNS-Filter {} deaktiviert",
    "Could not disable DNS filter {}":  "DNS-Filter {} konnte nicht deaktiviert werden",
    "DNS filter installed":             "DNS-Filter installiert",
    "DNS filter {} removed":            "DNS-Filter {} entfernt",
    "Could not remove DNS filter {}":   "DNS-Filter {} konnte nicht entfernt werden",
    "DNS filter added":                 "DNS-Filter hinzugefügt",
    "Could not add DNS filter":         "DNS-Filter konnte nicht hinzugefügt werden",
    "DNS filter title updated":         "DNS-Filter-Titel aktualisiert",
    "Could not set DNS filter title":   "DNS-Filter-Titel konnte nicht gesetzt werden",
    "Filter added":                     "Filter hinzugefügt",
    "Could not add filter":             "Filter konnte nicht hinzugefügt werden",
    "Filter trust updated":             "Filtervertrauen aktualisiert",
    "Could not update filter trust":    "Filtervertrauen konnte nicht aktualisiert werden",
    "Filter title updated":             "Filtertitel aktualisiert",
    "Could not set filter title":       "Filtertitel konnte nicht gesetzt werden",
    "License reset":                    "Lizenz zurückgesetzt",
    "Could not reset license":          "Lizenz konnte nicht zurückgesetzt werden",
    "Could not retrieve license info":  "Lizenzinformationen konnten nicht abgerufen werden",
    "Certificate generated":            "Zertifikat generiert",
    "Certificate generation failed":    "Zertifikatgenerierung fehlgeschlagen",
    "Logs exported":                    "Logs exportiert",
    "Log export failed":                "Log-Export fehlgeschlagen",
    "Settings exported":                "Einstellungen exportiert",
    "Settings export failed":           "Einstellungs-Export fehlgeschlagen",
    "Settings imported":                "Einstellungen importiert",
    "Settings import failed":           "Einstellungs-Import fehlgeschlagen",
    "Update check completed":           "Update-Prüfung abgeschlossen",
    "Update check failed":              "Update-Prüfung fehlgeschlagen",
    "Benchmark failed":                 "Benchmark fehlgeschlagen",
    "Open Manager…":                    "Manager öffnen…",
    "AdGuard stopped (forced)":         "AdGuard gestoppt (erzwungen)",
    "Could not stop AdGuard – process may still be running":
        "AdGuard konnte nicht gestoppt werden – Prozess läuft möglicherweise noch.",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "adguard-cli wurde auf diesem System nicht gefunden.\n\n"
        "Empfohlene Installation (offiziell):\n"
        "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
        "Alternative (Arch Linux AUR):\n"
        "  paru -S adguard-cli-bin\n\n"
        "Das Tray läuft, aber Start/Stop geht erst nach der Installation von adguard-cli.",
    "Copy install command":             "Installationsbefehl kopieren",
    "Continue":                         "Weiter",
    "AdGuard Tray is already running":  "AdGuard Tray läuft bereits",
    "Only one instance can run at a time. Check your system tray.":
        "Es kann nur eine Instanz gleichzeitig laufen. Schau in den System-Tray.",
    "Authentication cancelled":         "Authentifizierung abgebrochen",
    "Authorization failed":             "Autorisierung fehlgeschlagen",
    "URL must start with http:// or https://":
        "URL muss mit http:// oder https:// beginnen",
    "Log level and CLI path changes apply after a restart.":
        "Log-Level und CLI-Pfad werden nach einem Neustart wirksam.",
    "adguard-cli path does not exist or is not executable.":
        "adguard-cli-Pfad existiert nicht oder ist nicht ausführbar.",
    "That binary does not identify as adguard-cli. Save anyway?":
        "Diese Datei meldet sich nicht als adguard-cli. Trotzdem speichern?",
    "Update channel":                   "Update-Channel",
    "Channel:":                         "Channel:",
    "<small>Controls which AdGuard CLI build <i>Check for CLI update</i> "
    "will pull. Changes take effect on the next update run.</small>":
        "<small>Legt fest, welchen AdGuard-CLI-Build <i>Check for CLI update</i> "
        "holt. Änderungen greifen beim nächsten Update-Lauf.</small>",
    "Switching update channel to {}…":  "Wechsle Update-Channel auf {}…",
    "Update channel set to {}":         "Update-Channel auf {} gesetzt",
    "Could not set update channel":     "Update-Channel konnte nicht gesetzt werden",
    "Invalid channel: {}":              "Ungültiger Channel: {}",
}

# ── Simplified Chinese translations ──────────────────────────────────────

_ZH_CN: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "语言",
    "Auto (system locale)":              "自动（系统语言）",
    "English":                           "英语",
    "Simplified Chinese":                "简体中文",
    "German":                            "德语",
    "Requires application restart to take effect.":
        "需要重启应用程序才能生效。",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "已激活 – 保护运行中",
    "Inactive – Protection stopped":        "未激活 – 保护已停止",
    "Error retrieving status":              "获取状态出错",
    "adguard-cli not found":                "未找到 adguard-cli",
    "Unknown status":                       "未知状态",
    "Checking status…":                     "正在检查状态…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Toggle":                               "切换",
    "Enable":                               "启用",
    "Disable":                              "禁用",
    "Restart":                              "重启",
    "Filters":                              "过滤器",
    "Loading…":                             "加载中…",
    "Manage filters…":                      "管理过滤器…",
    "No userscripts installed":             "未安装用户脚本",
    "Manage userscripts…":                  "管理用户脚本…",
    "Refresh status":                       "刷新状态",
    "Settings…":                            "设置…",
    "Autostart on login":                   "登录时自动启动",
    "Quit":                                 "退出",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "已激活",
    "inactive":                             "未激活",
    "System-wide filtering: {}":            "系统范围过滤：{}",
    "Error: {}":                            "错误：{}",
    "AdGuard Tray – Error":                 "AdGuard Tray – 错误",
    "AdGuard is now active – protection running.":
        "AdGuard 现已激活 – 保护运行中。",
    "AdGuard has been stopped.":
        "AdGuard 已停止。",
    "Could not retrieve status.":
        "无法获取状态。",
    "Command failed":                       "命令失败",

    # ── settings_dialog.py ────────────────────────────────────────────────
    "AdGuard Tray – Settings":              "AdGuard Tray – 设置",
    "Status Refresh":                       "状态刷新",
    " seconds":                             " 秒",
    "How often adguard-cli status is checked automatically.":
        "自动检查 adguard-cli 状态的频率。",
    "Interval:":                            "间隔：",
    "Log level:":                           "日志级别：",
    "adguard-cli path:":                    "adguard-cli 路径：",
    "auto-detect via PATH":                 "通过 PATH 自动检测",
    "Browse…":                              "浏览…",
    "Select adguard-cli binary":            "选择 adguard-cli 二进制文件",
    "Notifications":                        "通知",
    "Desktop notification on status change":
        "状态变更时显示桌面通知",
    "<small>Requires <i>libnotify</i> / <i>notify-send</i> or an "
    "active notification service (dunst, mako, KDE).</small>":
        "<small>需要 <i>libnotify</i> / <i>notify-send</i> 或活动的 "
        "通知服务（dunst、mako、KDE）。</small>",
    "Autostart":                            "自动启动",
    "Start automatically on desktop login (XDG Autostart)":
        "桌面登录时自动启动（XDG 自动启动）",
    "<small>Creates <i>~/.config/autostart/adguard-tray.desktop</i>.<br>"
    "Works on KDE Plasma, GNOME, Hyprland (with xdg-autostart-impl) "
    "and other XDG-compliant environments.</small>":
        "<small>创建 <i>~/.config/autostart/adguard-tray.desktop</i>。<br>"
        "适用于 KDE Plasma、GNOME、Hyprland（使用 xdg-autostart-impl）"
        "和其他兼容 XDG 的环境。</small>",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "更新过滤器",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "更新所有过滤器、DNS 过滤器、用户脚本，\n"
        "SafebrowsingV2、CRLite 并检查应用更新。",
    "Add custom filter…":                   "添加自定义过滤器…",
    "Install custom filter by URL":         "通过 URL 安装自定义过滤器",
    "↺ Reload":                             "↺ 重新加载",
    "Loading filters…":                     "正在加载过滤器…",
    "No filters found.":                    "未找到过滤器。",
    "{} of {} filters active":              "{} / {} 个过滤器已激活",
    "Filter":                               "过滤器",
    "ID":                                   "ID",
    "Last updated":                         "上次更新",
    "Enabling filter {}…":                  "正在启用过滤器 {}…",
    "Disabling filter {}…":                 "正在禁用过滤器 {}…",
    "Updating filters…":                    "正在更新过滤器…",
    "Updating filters… (can take up to 2 minutes)":
        "正在更新过滤器…（可能需要最多 2 分钟）",
    "Update completed.":                    "更新完成。",
    "Update failed.":                       "更新失败。",
    "Add Custom Filter":                    "添加自定义过滤器",
    "Installing: {}":                       "正在安装：{}",
    "Filter installed.":                    "过滤器已安装。",
    "Remove":                               "移除",
    "Remove filter":                        "移除过滤器",
    'Really remove filter "{}"?':           "确定要移除过滤器 “{}” 吗？",
    "Removing filter {}…":                  "正在移除过滤器 {}…",
    "Filter {} removed.":                   "过滤器 {} 已移除。",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install (URL)…":                       "安装（URL）…",
    "Install userscript from a direct .js URL":
        "从直接的 .js URL 安装用户脚本",
    "Userscript":                           "用户脚本",
    "ID / Name":                            "ID / 名称",
    "<small>Right-click a userscript to remove it.<br>"
    "Userscripts are automatically updated when running "
    "<i>Update filters</i>.</small>":
        "<small>右键单击用户脚本以移除它。<br>"
        "运行 <i>更新过滤器</i> 时，用户脚本会自动更新。</small>",
    "Loading userscripts…":                 "正在加载用户脚本…",
    "No userscripts installed.":            "未安装用户脚本。",
    "{} of {} userscripts active":          "{} / {} 个用户脚本已激活",
    "Userscript '{}' enabled.":             "用户脚本 '{}' 已启用。",
    "Userscript '{}' disabled.":            "用户脚本 '{}' 已禁用。",
    "Install Userscript":                   "安装用户脚本",
    "Userscript URL (direct .js URL):":     "用户脚本 URL（直接 .js URL）：",
    "Userscript installed.":                "用户脚本已安装。",
    'Remove "{}"':                          "移除 “{}”",
    "Remove userscript":                    "移除用户脚本",
    'Really remove userscript "{}"?':       "确定要移除用户脚本 “{}” 吗？",
    "'{}' removed.":                        "'{}' 已移除。",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "未找到 adguard-cli。\n"
        "通过官方脚本或 AUR 安装：\n"
        "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
        "  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "获取状态时发生未知错误",
    "AdGuard {} ok":                        "AdGuard {} 正常",
    "AdGuard via systemctl {} ok":          "通过 systemctl 的 AdGuard {} 正常",
    "'{}' failed – insufficient privileges?":
        "'{}' 失败 – 权限不足？",
    "Could not retrieve filter list":
        "无法获取过滤器列表",
    "Filter {} enabled":                    "过滤器 {} 已启用",
    "Could not enable filter {}":           "无法启用过滤器 {}",
    "Filter {} disabled":                   "过滤器 {} 已禁用",
    "Could not disable filter {}":          "无法禁用过滤器 {}",
    "Filter installed":                     "过滤器已安装",
    "Installation failed":                  "安装失败",
    "Filter {} removed":                    "过滤器 {} 已移除",
    "Could not remove filter {}":          "无法移除过滤器 {}",
    "Filters updated":                      "过滤器已更新",
    "Update failed":                        "更新失败",
    "Could not retrieve userscript list":
        "无法获取用户脚本列表",
    "Userscript '{}' enabled":              "用户脚本 '{}' 已启用",
    "Could not enable userscript '{}'":
        "无法启用用户脚本 '{}'",
    "Userscript '{}' disabled":             "用户脚本 '{}' 已禁用",
    "Could not disable userscript '{}'":
        "无法禁用用户脚本 '{}'",
    "Userscript '{}' removed":              "用户脚本 '{}' 已移除",
    "Could not remove userscript '{}'":
        "无法移除用户脚本 '{}'",
    "Userscript installed":                 "用户脚本已安装",
    "Other":                                "其他",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "搜索过滤器…",
    "Search userscripts…":              "搜索用户脚本…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "AdGuard CLI – Configuration":      "AdGuard CLI – 配置",
    "Could not load proxy.yaml.\nPath: {}":
        "无法加载 proxy.yaml。\n路径：{}",
    "Proxy":                            "代理",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Stealth Mode":                     "隐身模式",
    "Apps":                             "应用",
    "Security":                         "安全",
    "<small><b>Note:</b> Changes require an AdGuard CLI restart to take effect.</small>":
        "<small><b>注意：</b>更改需要重启 AdGuard CLI 才能生效。</small>",
    "Proxy Mode":                       "代理模式",
    "Mode:":                            "模式：",
    "auto: AdGuard redirects app traffic into itself via iptables\n"
    "manual: Only listens on the configured proxy ports (SOCKS5/HTTP)":
        "auto：AdGuard 通过 iptables 将应用流量重定向到自身\n"
        "manual：仅监听配置的代理端口（SOCKS5/HTTP）",
    "Filtered ports:":                  "过滤的端口：",
    "Port ranges intercepted in auto mode.\n"
    "Format: 80:5221,5300:49151 (range) or 80,443,8080 (individual)\n"
    "Only applies when proxy mode is 'auto'.":
        "自动模式下拦截的端口范围。\n"
        "格式：80:5221,5300:49151（范围）或 80,443,8080（单个）\n"
        "仅适用于代理模式为 “auto” 时。",
    "Manual Proxy Ports":               "手动代理端口",
    "SOCKS5 port:":                     "SOCKS5 端口：",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "手动模式的 SOCKS5 代理端口。\n设置为 -1 以禁用。",
    "HTTP port:":                       "HTTP 端口：",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "手动模式的 HTTP 代理端口。\n设置为 -1 以禁用。",
    "Listen address:":                  "监听地址：",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "代理监听的地址。\n"
        "127.0.0.1 = 仅本地。0.0.0.0 = 所有接口（需要身份验证）。",
    "Worker threads:":                  "工作线程：",
    "Number of proxy worker threads.":  "代理工作线程数量。",
    "HTTPS Filtering":                  "HTTPS 过滤",
    "Enable HTTPS filtering":           "启用 HTTPS 过滤",
    "Decrypt and filter HTTPS traffic.\n"
    "Needed to block ads on https sites.\n"
    "Requires a trusted root certificate installed on the system.":
        "解密并过滤 HTTPS 流量。\n"
        "需要阻止 https 网站上的广告。\n"
        "需要在系统上安装受信任的根证书。",
    "Enable TLS 1.3":                   "启用 TLS 1.3",
    "Enable TLS 1.3 support for filtered connections.":
        "为过滤的连接启用 TLS 1.3 支持。",
    "Filter HTTP/3 (QUIC) – experimental":
        "过滤 HTTP/3 (QUIC) – 实验性",
    "Filter HTTP/3 (QUIC) traffic.\nExperimental – may cause issues with some sites.":
        "过滤 HTTP/3 (QUIC) 流量。\n实验性 – 可能会导致某些网站出现问题。",
    "OCSP certificate checks":          "OCSP 证书检查",
    "Check certificate revocation status via OCSP.\n"
    "Slower but more secure.":
        "通过 OCSP 检查证书撤销状态。\n"
        "较慢但更安全。",
    "Enforce Certificate Transparency": "强制证书透明度",
    "Enforce Certificate Transparency timestamp checks.\n"
    "Similar to Chrome's built-in CT policy.":
        "强制证书透明度时间戳检查。\n"
        "类似于 Chrome 的内置 CT 策略。",
    "Filter EV certificate sites":      "过滤 EV 证书网站",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "默认情况下，具有扩展验证证书的网站不会被过滤。\n"
        "启用此选项以过滤它们（例如银行网站）。",
    "Encrypted Client Hello (ECH)":     "加密客户端 Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "启用 ECH 以获得更好的隐私。\n需要启用 DNS 过滤。",
    "Secure DNS Filtering":             "安全 DNS 过滤",
    "off: No secure DNS filtering\n"
    "transparent: Filter DoH/DoT inline without changing destination\n"
    "redirect: Redirect all secure DNS to the local DNS proxy":
        "off：无安全 DNS 过滤\n"
        "transparent：内联过滤 DoH/DoT，无需更改目标\n"
        "redirect：将所有安全 DNS 重定向到本地 DNS 代理",
    "DNS Filtering":                    "DNS 过滤",
    "Enable DNS filtering":             "启用 DNS 过滤",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "过滤 DNS 查询以在 DNS 级别阻止广告和跟踪器。\n"
        "使用具有可配置上游的本地 DNS 代理。",
    "Upstream:":                        "上游：",
    "DNS upstream server.\n'default' = system DNS\n"
    "Examples: 1.1.1.1, https://dns.google/dns-query,\n"
    "tls://dns.adguard.com, quic://dns.adguard.com":
        "DNS 上游服务器。\n'default' = 系统 DNS\n"
        "示例：1.1.1.1、https://dns.google/dns-query、\n"
        "tls://dns.adguard.com、quic://dns.adguard.com",
    "Fallbacks:":                       "后备：",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "后备 DNS 服务器（当主上游失败时使用的）。\n"
        "'default' = 系统 DNS。空格分隔的列表。\n"
        "示例：default 1.1.1.1",
    "Bootstraps:":                      "引导：",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "用于解析上游主机名的引导 DNS。\n"
        "'default' = 系统 DNS IP。仅允许 IP 地址。\n"
        "示例：default 8.8.8.8 tls://1.1.1.1",
    "Block ECH in DNS":                 "在 DNS 中阻止 ECH",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "从 SVCB/HTTPS DNS 记录中移除 ECH 参数。\n"
        "仅对无法自动检测 HTTPS 过滤的浏览器启用。",
    "Stealth Mode (Tracking Protection)":
        "隐身模式（跟踪保护）",
    "Enable Stealth Mode":              "启用隐身模式",
    "Master switch for all tracking protection features below.":
        "以下所有跟踪保护功能的主开关。",
    "Cookies":                          "Cookie",
    "Block third-party cookies":        "阻止第三方 Cookie",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "在设定的时间后删除第三方 Cookie。\n防止跨站点跟踪。",
    "Lifetime (minutes):":              "生命周期（分钟）：",
    "0 = block immediately. Default: 180 minutes.":
        "0 = 立即阻止。默认：180 分钟。",
    "Block first-party cookies":        "阻止第一方 Cookie",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "在设定的时间后删除所有 Cookie（包括第一方）。\n"
        "警告：这将使你从所有网站退出登录。",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = 立即阻止。默认：4320 分钟（3 天）。",
    "Privacy":                          "隐私",
    "Hide / reduce User-Agent":         "隐藏 / 减少 User-Agent",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "从 User-Agent 中移除标识位。\n"
        "减少指纹识别。",
    "Hide search queries in referrer":  "在引用页中隐藏搜索查询",
    "Hides your search terms when clicking from a search engine to a website.":
        "从搜索引擎点击到网站时隐藏你的搜索词。",
    "Remove referrer from third-party requests":
        "从第三方请求中移除引用页",
    "Prevents third-party sites from knowing which page you came from.":
        "防止第三方网站知道你来自哪个页面。",
    "Send Do-Not-Track signal":         "发送 Do-Not-Track 信号",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "发送带有请求的 DNT 标头。\n注意：大多数网站会忽略此信号，但有些会尊重它。",
    "Disable third-party ETag cache":   "禁用第三方 ETag 缓存",
    "Prevents tracking via ETag caching in third-party content.":
        "防止通过第三方内容中的 ETag 缓存进行跟踪。",
    "Block third-party Authorization header":
        "阻止第三方 Authorization 标头",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "阻止第三方请求中的 Authorization 标头以防止跟踪。",
    "Remove X-Client-Data header":      "移除 X-Client-Data 标头",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "移除 Chrome 发送到 Google 服务的 X-Client-Data 标头。",
    "Browser API Blocking":             "浏览器 API 阻止",
    "Block WebRTC":                     "阻止 WebRTC",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "防止通过 WebRTC 泄露 IP。\n可能会破坏视频通话和一些 Web 应用。",
    "Block Push API":                   "阻止 Push API",
    "Blocks browser push notifications from websites.":
        "阻止来自网站的浏览器推送通知。",
    "Block Location API":               "阻止位置 API",
    "Prevents websites from accessing your GPS location.":
        "防止网站访问你的 GPS 位置。",
    "Block Flash":                      "阻止 Flash",
    "Blocks the Flash plugin.":
        "阻止 Flash 插件。",
    "Block Java":                       "阻止 Java",
    "Disables Java plugins. JavaScript remains enabled.":
        "禁用 Java 插件。JavaScript 保持启用。",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "启用 Anti-DPI",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\n"
    "Useful in countries with internet censorship.":
        "更改传出数据包以绕过深度数据包检测。\n"
        "在存在互联网审查的国家/地区很有用。",
    "App pattern":                      "应用模式",
    "Action":                           "操作",
    "Skip outbound proxy":              "跳过出站代理",
    "default: Filter fully\n"
    "bypass_https: Skip HTTPS filtering\n"
    "bypass: Skip all filtering (games, anti-cheat)":
        "default：完全过滤\n"
        "bypass_https：跳过 HTTPS 过滤\n"
        "bypass：跳过所有过滤（游戏、反作弊）",
    "Don't route this app's traffic through outbound proxy":
        "不要将此应用的流量通过出站代理路由",
    "Browser list included from {}":    "浏览器列表从 {} 包含",
    "+ Add rule":                        "+ 添加规则",
    "Add a new app filter rule":        "添加新的应用过滤规则",
    "− Remove selected":                "− 移除选中项",
    "Remove the selected rule":         "移除选中的规则",
    "↑ Move up":                        "↑ 上移",
    "↓ Move down":                      "↓ 下移",
    "Cannot remove":                    "无法移除",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "浏览器包含列表和通配符 (*) 规则无法移除。",
    "Browsing Security":                "浏览安全",
    "Enable Safe Browsing":             "启用安全浏览",
    "Warns about malicious and phishing websites.\n"
    "Uses AdGuard's Safe Browsing database.":
        "警告恶意和钓鱼网站。\n"
        "使用 AdGuard 的安全浏览数据库。",
    "Send anonymous statistics":        "发送匿名统计信息",
    "Send anonymous lookups to AdGuard.":
        "向 AdGuard 发送匿名查询。",
    "CRLite":                           "CRLite",
    "Enable CRLite":                    "启用 CRLite",
    "Certificate revocation checking using Mozilla's CRLite.\n"
    "Faster and more reliable than traditional CRL/OCSP checks.":
        "使用 Mozilla 的 CRLite 进行证书撤销检查。\n"
        "比传统的 CRL/OCSP 检查更快、更可靠。",
    "Content Filtering":                "内容过滤",
    "Enable ad blocking":               "启用广告拦截",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "将广告拦截过滤规则应用于 HTTP/HTTPS 请求。",
    "Save failed":                      "保存失败",
    "Could not save proxy.yaml:\n{}":   "无法保存 proxy.yaml：\n{}",
    "Configuration saved. Restart AdGuard to apply changes.":
        "配置已保存。重启 AdGuard 以应用更改。",
    "Restarting AdGuard…":              "正在重启 AdGuard…",
    "AdGuard restarted.":               "AdGuard 已重启。",
    "Restart failed: {}":               "重启失败：{}",
    "Unknown error":                    "未知错误",
    "AdGuard Configuration…":           "AdGuard 配置…",
    "<b>App filter rules</b> (auto mode only)<br>"
    "<small>"
    "<b>default</b> – filter this app fully<br>"
    "<b>bypass_https</b> – no HTTPS filtering for this app<br>"
    "<b>bypass</b> – no filtering at all (use for games with anti-cheat)<br><br>"
    "Wildcard patterns supported (e.g. <code>*steam*</code>, <code>*EasyAntiCheat*</code>).<br>"
    "Rules are evaluated top to bottom – first match wins.<br>"
    "The wildcard <code>*</code> rule should always be last."
    "</small>":
        "<b>应用过滤规则</b>（仅自动模式）<br>"
        "<small>"
        "<b>default</b> – 完全过滤此应用<br>"
        "<b>bypass_https</b> – 此应用不进行 HTTPS 过滤<br>"
        "<b>bypass</b> – 完全不过滤（用于带有反作弊的游戏）<br><br>"
        "支持通配符模式（例如 <code>*steam*</code>、<code>*EasyAntiCheat*</code>）。<br>"
        "规则从上到下评估 – 第一个匹配项生效。<br>"
        "通配符 <code>*</code> 规则应始终在最后。"
        "</small>",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Website Exceptions…":              "网站例外…",
    "AdGuard Tray – Website Exceptions":
        "AdGuard Tray – 网站例外",
    "<small>Websites listed here will not have ads or trackers blocked.<br>"
    "Enter a domain (e.g. <code>example.com</code>) without <code>https://</code>.</small>":
        "<small>此处列出的网站将不会阻止广告或跟踪器。<br>"
        "输入域名（例如 <code>example.com</code>）不带 <code>https://</code>。</small>",
    "example.com":                      "example.com",
    "Add":                              "添加",
    "Search exceptions…":               "搜索例外…",
    "Remove selected":                  "移除选中项",
    "1 exception":                      "1 个例外",
    "{} exceptions":                    "{} 个例外",
    "Invalid domain":                   "无效域名",
    "Invalid URL":                      "无效 URL",
    "'{}' is not a valid domain or IP address.":
        "'{}' 不是有效的域名或 IP 地址。",
    "'{}' is already in the list.":     "'{}' 已在列表中。",
    "Could not save exceptions:\n{}":
        "无法保存例外：\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "AdGuard Tray – Manager":           "AdGuard Tray – 管理器",
    "Overview":                         "概览",
    "DNS Filters":                      "DNS 过滤器",
    "Userscripts":                      "用户脚本",
    "Exceptions":                       "例外",
    "Configuration":                    "配置",
    "Diagnostics":                      "诊断",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Status":                           "状态",
    "↺ Refresh":                        "↺ 刷新",
    "Version & License":                "版本和许可证",
    "Check for CLI update":             "检查 CLI 更新",
    "Reset license":                    "重置许可证",
    "HTTPS Certificate":                "HTTPS 证书",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "生成用于 HTTPS 过滤的根 CA 证书。"
        "证书必须在你的系统上安装并受信任。",
    "Generate certificate":             "生成证书",
    "Checking for updates…":            "正在检查更新…",
    "Are you sure you want to reset the AdGuard license?":
        "你确定要重置 AdGuard 许可证吗？",
    "Generating certificate…":          "正在生成证书…",
    "Firefox profile:":                 "Firefox 配置文件：",
    "(optional) e.g. abcd1234.MyProfile":
        "（可选）例如 abcd1234.MyProfile",
    "License: {}":                      "许可证：{}",
    "Could not retrieve":               "无法获取",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Add by ID…":                       "按 ID 添加…",
    "Add internal filter by ID or name":
        "按 ID 或名称添加内部过滤器",
    "Show all available":               "显示所有可用项",
    "Show all available filters, not just installed ones":
        "显示所有可用的过滤器，不仅仅是已安装的",
    "Add Filter by ID":                 "按 ID 添加过滤器",
    "Enter filter ID or name:":         "输入过滤器 ID 或名称：",
    "Adding filter: {}":                "正在添加过滤器：{}",
    "Filter added.":                    "过滤器已添加。",
    "Rename…":                          "重命名…",
    "Set trusted":                      "设为受信任",
    "Set untrusted":                    "设为不受信任",
    "Rename filter":                    "重命名过滤器",
    "New title:":                       "新标题：",
    "Renaming filter {}…":              "正在重命名过滤器 {}…",
    "Filter renamed.":                  "过滤器已重命名。",
    "trusted":                          "受信任",
    "untrusted":                        "不受信任",
    "Setting filter {} as {}…":         "正在将过滤器 {} 设为 {}…",
    "Filter trust updated.":            "过滤器信任已更新。",
    "Filter URL:":                      "过滤器 URL：",
    "Title:":                           "标题：",
    "(optional)":                       "（可选）",
    "Trusted filter":                   "受信任的过滤器",
    "Trusted filters can use advanced rules (JS scriptlets, etc.)":
        "受信任的过滤器可以使用高级规则（JS scriptlets 等）",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Add custom DNS filter…":           "添加自定义 DNS 过滤器…",
    "Search DNS filters…":              "搜索 DNS 过滤器…",
    "DNS filters block domains at the DNS level. "
    "Requires DNS filtering to be enabled in Configuration → DNS.":
        "DNS 过滤器在 DNS 级别阻止域名。"
        "需要在配置 → DNS 中启用 DNS 过滤。",
    "Loading DNS filters…":             "正在加载 DNS 过滤器…",
    "No DNS filters found.":            "未找到 DNS 过滤器。",
    "{} of {} DNS filters active":      "{} / {} 个 DNS 过滤器已激活",
    "DNS filter installed.":            "DNS 过滤器已安装。",
    "Add DNS Filter by ID":             "按 ID 添加 DNS 过滤器",
    "Adding DNS filter: {}":            "正在添加 DNS 过滤器：{}",
    "DNS filter added.":                "DNS 过滤器已添加。",
    "Remove DNS filter":                "移除 DNS 过滤器",
    'Really remove DNS filter "{}"?':   "确定要移除 DNS 过滤器 “{}” 吗？",
    "DNS filter {} removed.":           "DNS 过滤器 {} 已移除。",
    "Rename DNS filter":                "重命名 DNS 过滤器",
    "DNS filter renamed.":              "DNS 过滤器已重命名。",
    "Add Custom DNS Filter":            "添加自定义 DNS 过滤器",

    # ── config_tab.py ────────────────────────────────────────────────────
    "Could not load proxy.yaml.":       "无法加载 proxy.yaml。",
    "Edit the full AdGuard CLI configuration (proxy.yaml).":
        "编辑完整的 AdGuard CLI 配置 (proxy.yaml)。",
    "Open Configuration Editor…":       "打开配置编辑器…",

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export & Import":                  "导出和导入",
    "Export logs…":                     "导出日志…",
    "Export AdGuard CLI logs to a zip file":
        "将 AdGuard CLI 日志导出到 zip 文件",
    "Export settings…":                 "导出设置…",
    "Export all AdGuard CLI settings to a zip file":
        "将所有 AdGuard CLI 设置导出到 zip 文件",
    "Import settings…":                 "导入设置…",
    "Import settings from a previously exported zip file":
        "从先前导出的 zip 文件导入设置",
    "Performance Benchmark":            "性能基准测试",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "运行加密和 HTTPS 过滤基准测试。",
    "Run benchmark":                    "运行基准测试",
    "Running benchmark…":               "正在运行基准测试…",
    "Done.":                            "完成。",
    "Failed.":                          "失败。",
    "Export logs to…":                  "导出日志到…",
    "Exporting logs…":                  "正在导出日志…",
    "Export settings to…":              "导出设置到…",
    "Exporting settings…":              "正在导出设置…",
    "Import settings from…":            "从…导入设置",
    "Zip files (*.zip);;All files (*)":
        "Zip 文件 (*.zip);;所有文件 (*)",
    "Importing settings…":              "正在导入设置…",
    "Application Log":                  "应用程序日志",
    "View recent log entries":          "查看最近的日志条目",
    "Log file not found.":              "未找到日志文件。",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "无法获取 DNS 过滤器列表",
    "DNS filter {} enabled":            "DNS 过滤器 {} 已启用",
    "Could not enable DNS filter {}":   "无法启用 DNS 过滤器 {}",
    "DNS filter {} disabled":           "DNS 过滤器 {} 已禁用",
    "Could not disable DNS filter {}":  "无法禁用 DNS 过滤器 {}",
    "DNS filter installed":             "DNS 过滤器已安装",
    "DNS filter {} removed":            "DNS 过滤器 {} 已移除",
    "Could not remove DNS filter {}":   "无法移除 DNS 过滤器 {}",
    "DNS filter added":                 "DNS 过滤器已添加",
    "Could not add DNS filter":         "无法添加 DNS 过滤器",
    "DNS filter title updated":         "DNS 过滤器标题已更新",
    "Could not set DNS filter title":   "无法设置 DNS 过滤器标题",
    "Filter added":                     "过滤器已添加",
    "Could not add filter":             "无法添加过滤器",
    "Filter trust updated":             "过滤器信任已更新",
    "Could not update filter trust":    "无法更新过滤器信任",
    "Filter title updated":             "过滤器标题已更新",
    "Could not set filter title":       "无法设置过滤器标题",
    "License reset":                    "许可证已重置",
    "Could not reset license":          "无法重置许可证",
    "Could not retrieve license info":  "无法获取许可证信息",
    "Certificate generated":            "证书已生成",
    "Certificate generation failed":    "证书生成失败",
    "Logs exported":                    "日志已导出",
    "Log export failed":                "日志导出失败",
    "Settings exported":                "设置已导出",
    "Settings export failed":           "设置导出失败",
    "Settings imported":                "设置已导入",
    "Settings import failed":           "设置导入失败",
    "Update check completed":           "更新检查完成",
    "Update check failed":              "更新检查失败",
    "Benchmark failed":                 "基准测试失败",
    "Open Manager…":                    "打开管理器…",
    "AdGuard stopped (forced)":         "AdGuard 已停止（强制）",
    "Could not stop AdGuard – process may still be running":
        "无法停止 AdGuard – 进程可能仍在运行",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "在此系统上未找到 adguard-cli。\n\n"
        "推荐的安装方法（官方）：\n"
        "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
        "替代方法（Arch Linux AUR）：\n"
        "  paru -S adguard-cli-bin\n\n"
        "托盘会加载，但在安装 adguard-cli 之前，启动/停止将不起作用。",
    "Copy install command":             "复制安装命令",
    "Continue":                         "继续",
    "AdGuard Tray is already running":  "AdGuard Tray 已在运行",
    "Only one instance can run at a time. Check your system tray.":
        "一次只能运行一个实例。请检查你的系统托盘。",
    "Authentication cancelled":         "身份验证已取消",
    "Authorization failed":             "授权失败",
    "URL must start with http:// or https://":
        "URL 必须以 http:// 或 https:// 开头",
    "Log level and CLI path changes apply after a restart.":
        "日志级别和 CLI 路径更改在重启后生效。",
    "adguard-cli path does not exist or is not executable.":
        "adguard-cli 路径不存在或不可执行。",
    "That binary does not identify as adguard-cli. Save anyway?":
        "该二进制文件未标识为 adguard-cli。仍然保存吗？",
    "Update channel":                   "更新通道",
    "Channel:":                         "通道：",
    "<small>Controls which AdGuard CLI build <i>Check for CLI update</i> "
    "will pull. Changes take effect on the next update run.</small>":
        "<small>控制 <i>检查 CLI 更新</i> 将拉取哪个 AdGuard CLI 构建。"
        "更改在下次更新运行时生效。</small>",
    "Switching update channel to {}…":  "正在将更新通道切换到 {}…",
    "Update channel set to {}":         "更新通道已设置为 {}",
    "Could not set update channel":     "无法设置更新通道",
    "Invalid channel: {}":              "无效通道：{}",
}

# ── Translation registry ──────────────────────────────────────────────────

_TRANSLATIONS: dict[str, dict[str, str]] = {
    "de": _DE,
    "zh": _ZH_CN,  # Simplified Chinese (zh_CN, zh_SG, etc.)
}

_CURRENT: dict[str, str] = _TRANSLATIONS.get(_LANG, {})


def _t(key: str, *args: object) -> str:
    """Return the translated string, optionally formatted with *args*."""
    text = _CURRENT.get(key, key)
    if args:
        return text.format(*args)
    return text
