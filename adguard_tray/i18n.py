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
    """Return a 2-letter language code based on the system locale."""
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
    "AdGuard Tray – Manage Filters":        "AdGuard Tray – Filter verwalten",
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
    "Filter {} enabled.":                   "Filter {} aktiviert.",
    "Filter {} disabled.":                  "Filter {} deaktiviert.",
    "Updating filters…":                    "Filter werden aktualisiert…",
    "Update completed.":                    "Aktualisierung abgeschlossen.",
    "Update failed.":                       "Aktualisierung fehlgeschlagen.",
    "Add Custom Filter":                    "Eigenen Filter hinzufügen",
    "Filter URL (direct .txt URL of the filter list):":
        "Filter-URL (direkte .txt-URL der Filterliste):",
    "Installing: {}":                       "Installiere: {}",
    "Filter installed.":                    "Filter installiert.",
    "Remove":                               "Entfernen",
    "Remove filter":                        "Filter entfernen",
    'Really remove filter "{}"?':           'Filter «{}» wirklich entfernen?',
    "Removing filter {}…":                  "Filter {} wird entfernt…",
    "Filter {} removed.":                   "Filter {} entfernt.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "AdGuard Tray – Userscripts":           "AdGuard Tray – Userscripts",
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
    "Enabling userscript '{}'…":            "Userscript '{}' wird aktiviert…",
    "Disabling userscript '{}'…":           "Userscript '{}' wird deaktiviert…",
    "Userscript '{}' enabled.":             "Userscript '{}' aktiviert.",
    "Userscript '{}' disabled.":            "Userscript '{}' deaktiviert.",
    "Install Userscript":                   "Userscript installieren",
    "Userscript URL (direct .js URL):":     "Userscript-URL (direkte .js-URL):",
    "Userscript installed.":                "Userscript installiert.",
    'Remove "{}"':                          '«{}» entfernen',
    "Remove userscript":                    "Userscript entfernen",
    'Really remove userscript "{}"?':       'Userscript «{}» wirklich entfernen?',
    "Removing '{}'…":                       "Entferne '{}'…",
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
    "AdGuard {} successful":                "AdGuard {} erfolgreich",
    "AdGuard via systemctl {} successful":  "AdGuard via systemctl {} erfolgreich",
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
    "Required for high-quality ad blocking on encrypted sites.\n"
    "Requires a trusted root certificate installed on the system.":
        "HTTPS-Traffic entschlüsseln und filtern.\n"
        "Erforderlich für effektive Werbeblockierung auf verschlüsselten Seiten.\n"
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
    "Improves security but may slightly increase connection latency.":
        "Zertifikatswiderruf per OCSP prüfen.\n"
        "Verbessert die Sicherheit, kann aber die Verbindungslatenz leicht erhöhen.",
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
        "Nur aktivieren für Browser die HTTPS-Filterung nicht automatisch erkennen.",
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
    "Warning: This will log you out of all sites!":
        "Alle Cookies (inkl. Erstanbieter) nach einer bestimmten Zeit löschen.\n"
        "Warnung: Du wirst auf allen Seiten ausgeloggt!",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = sofort blockieren. Standard: 4320 Minuten (3 Tage).",
    "Privacy":                          "Privatsphäre",
    "Hide / reduce User-Agent":         "User-Agent verstecken / reduzieren",
    "Reduces the User-Agent header to remove identifying information.\n"
    "Helps prevent browser fingerprinting.":
        "Reduziert den User-Agent-Header um identifizierende Informationen zu entfernen.\n"
        "Hilft gegen Browser-Fingerprinting.",
    "Hide search queries in referrer":  "Suchanfragen im Referrer verstecken",
    "Hides your search terms when clicking from a search engine to a website.":
        "Versteckt deine Suchbegriffe beim Klick von einer Suchmaschine auf eine Webseite.",
    "Remove referrer from third-party requests":
        "Referrer aus Drittanbieter-Anfragen entfernen",
    "Prevents third-party sites from knowing which page you came from.":
        "Verhindert dass Drittanbieter-Seiten wissen von welcher Seite du kommst.",
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
    "Prevents IP leaks via WebRTC.\nWarning: May break video calls and some web apps!":
        "Verhindert IP-Leaks über WebRTC.\nWarnung: Kann Videoanrufe und Web-Apps beeinträchtigen!",
    "Block Push API":                   "Push-API blockieren",
    "Blocks browser push notifications from websites.":
        "Blockiert Browser-Push-Benachrichtigungen von Webseiten.",
    "Block Location API":               "Standort-API blockieren",
    "Prevents websites from accessing your GPS location.":
        "Verhindert den Zugriff von Webseiten auf deinen GPS-Standort.",
    "Block Flash":                      "Flash blockieren",
    "Blocks Flash plugin to reduce security vulnerabilities.":
        "Blockiert das Flash-Plugin zur Reduzierung von Sicherheitslücken.",
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
    "Help improve Safe Browsing by sending anonymous lookup statistics.":
        "Safe Browsing verbessern durch Senden anonymer Abfragestatistiken.",
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
    "AdGuard restarted successfully.":  "AdGuard erfolgreich neu gestartet.",
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
    "{} exception(s)":                  "{} Ausnahme(n)",
    "Invalid domain":                   "Ungültige Domain",
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
    "DNS filter {} enabled.":           "DNS-Filter {} aktiviert.",
    "DNS filter {} disabled.":          "DNS-Filter {} deaktiviert.",
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
    "License reset successful":         "Lizenz erfolgreich zurückgesetzt",
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

    # ── main.py ───────────────────────────────────────────────────────────
    "System tray not available":
        "Kein System-Tray verfügbar",
    "The system tray is not available in this desktop environment.\n\n"
    "On Hyprland: waybar with the [tray] module enabled or sfwbar is required.\n"
    "On KDE Plasma it should work out of the box.":
        "Das System-Tray ist in dieser Desktop-Umgebung nicht verfügbar.\n\n"
        "Unter Hyprland: waybar mit aktiviertem [tray]-Modul oder sfwbar benötigt.\n"
        "Unter KDE Plasma sollte es sofort funktionieren.",
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "The application will start but protection controls will not work until adguard-cli is installed.":
        "adguard-cli konnte auf diesem System nicht gefunden werden.\n\n"
        "Empfohlene Installation (offiziell):\n"
        "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
        "Alternative (Arch Linux AUR):\n"
        "  paru -S adguard-cli-bin\n\n"
        "Die Anwendung startet, aber Schutzfunktionen sind erst nach der Installation von adguard-cli verfügbar.",
    "Copy install command":             "Installationsbefehl kopieren",
    "Continue":                         "Weiter",
}

# ── Translation registry ──────────────────────────────────────────────────

_TRANSLATIONS: dict[str, dict[str, str]] = {
    "de": _DE,
}

_CURRENT: dict[str, str] = _TRANSLATIONS.get(_LANG, {})


def _t(key: str, *args: object) -> str:
    """Return the translated string, optionally formatted with *args*."""
    text = _CURRENT.get(key, key)
    if args:
        return text.format(*args)
    return text
