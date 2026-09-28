"""German."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "Sprache",
    "English":                           "Englisch",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "Aktiv – Schutz läuft",
    "Inactive – Protection stopped":        "Inaktiv – Schutz gestoppt",
    "Error retrieving status":              "Fehler beim Statusabruf",
    "adguard-cli not found":                "adguard-cli nicht gefunden",
    "Unknown status":                       "Status unbekannt",
    "Checking status…":                     "Status wird abgefragt…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "Neu starten",
    "Filters":                              "Filter",
    "Loading…":                             "Wird geladen…",
    "Manage filters…":                      "Filter verwalten…",
    "No userscripts installed":             "Keine Userscripts installiert",
    "Manage userscripts…":                  "Userscripts verwalten…",
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
    " seconds":                             " Sekunden",
    "How often adguard-cli status is checked automatically.":
        "Wie häufig der Status von adguard-cli automatisch abgefragt wird.",
    "Log level:":                           "Log-Level:",
    "adguard-cli path:":                    "adguard-cli-Pfad:",
    "auto-detect via PATH":                 "automatisch via PATH",
    "Browse…":                              "Durchsuchen…",
    "Select adguard-cli binary":            "adguard-cli-Binary auswählen",
    "Notifications":                        "Benachrichtigungen",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "Filter aktualisieren",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "Aktualisiert alle Filter, DNS-Filter, Userscripts,\n"
        "SafebrowsingV2, CRLite und prüft auf App-Updates.",
    "No filters found.":                    "Keine Filter gefunden.",
    "Updating filters… (can take up to 2 minutes)":
        "Filter werden aktualisiert… (kann bis zu 2 Minuten dauern)",
    "Update completed.":                    "Aktualisierung abgeschlossen.",
    "Update failed.":                       "Aktualisierung fehlgeschlagen.",
    "Installing: {}":                       "Installiere: {}",
    "Filter installed.":                    "Filter installiert.",
    "Remove":                               "Entfernen",
    "Remove filter":                        "Filter entfernen",
    "Filter {} removed.":                   "Filter {} entfernt.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        "Userscript von einer direkten .js-URL installieren",
    "No userscripts installed.":            "Keine Userscripts installiert.",
    "Userscript URL (direct .js URL):":     "Userscript-URL (direkte .js-URL):",
    "Userscript installed.":                "Userscript installiert.",
    'Remove "{}"':                          '«{}» entfernen',
    "Remove userscript":                    "Userscript entfernen",
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
    "Could not load proxy.yaml.\nPath: {}":
        "proxy.yaml konnte nicht geladen werden.\nPfad: {}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "Apps",
    "Mode:":                            "Modus:",
    "Filtered ports:":                  "Gefilterte Ports:",
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
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "HTTPS-Datenverkehr entschlüsseln und filtern.\nNötig, um Werbung auf https-Seiten zu blockieren.\nBenötigt ein installiertes Root-Zertifikat auf dem System.",
    "Enable TLS 1.3":                   "TLS 1.3 aktivieren",
    "Enable TLS 1.3 support for filtered connections.":
        "TLS 1.3 für gefilterte Verbindungen aktivieren.",
    "Filter HTTP/3 (QUIC) – experimental":
        "HTTP/3 (QUIC) filtern – experimentell",
    "OCSP certificate checks":          "OCSP-Zertifikatsprüfung",
    "Enforce Certificate Transparency": "Certificate Transparency erzwingen",
    "Filter EV certificate sites":      "EV-Zertifikat-Seiten filtern",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "Standardmäßig werden Seiten mit EV-Zertifikaten nicht gefiltert.\n"
        "Aktivieren um auch diese zu filtern (z.B. Banking-Seiten).",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "ECH für besseren Datenschutz aktivieren.\nErfordert aktivierte DNS-Filterung.",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "DNS-Anfragen filtern um Werbung und Tracker auf DNS-Ebene zu blockieren.\n"
        "Nutzt einen lokalen DNS-Proxy mit konfigurierbaren Upstreams.",
    "Upstream:":                        "Upstream:",
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
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "ECH-Parameter aus SVCB/HTTPS-DNS-Einträgen entfernen.\n"
        "Nur aktivieren für Browser, die HTTPS-Filterung nicht automatisch erkennen.",
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
        "Versteckt deine Suchbegriffe beim Klick von einer Suchmaschine auf eine Website.",
    "Remove referrer from third-party requests":
        "Referrer aus Drittanbieter-Anfragen entfernen",
    "Prevents third-party sites from knowing which page you came from.":
        "Verhindert, dass Drittanbieter-Websites sehen, von welcher Seite du kommst.",
    "Send Do-Not-Track signal":         "Do-Not-Track-Signal senden",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "Sendet DNT-Header mit Anfragen.\nHinweis: Die meisten Websites ignorieren das, manche beachten es.",
    "Disable third-party ETag cache":   "Drittanbieter-ETag-Cache deaktivieren",
    "Prevents tracking via ETag caching in third-party content.":
        "Verhindert Tracking über ETag-Caching bei Drittanbieter-Inhalten.",
    "Block third-party Authorization header":
        "Drittanbieter-Authorization-Header blockieren",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "Blockiert den Authorization-Header bei Drittanbieter-Anfragen.",
    "Remove X-Client-Data header":      "X-Client-Data-Header entfernen",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "Entfernt den X-Client-Data-Header, den Chrome an Google-Dienste sendet.",
    "Block WebRTC":                     "WebRTC blockieren",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "Verhindert IP-Leaks über WebRTC.\nKann Videoanrufe und Web-Apps stören.",
    "Block Push API":                   "Push-API blockieren",
    "Blocks browser push notifications from websites.":
        "Blockiert Browser-Push-Benachrichtigungen von Websites.",
    "Block Location API":               "Standort-API blockieren",
    "Prevents websites from accessing your GPS location.":
        "Verhindert den Zugriff von Websites auf deinen GPS-Standort.",
    "Block Flash":                      "Flash blockieren",
    "Blocks the Flash plugin.":
        "Blockiert das Flash-Plugin.",
    "Block Java":                       "Java blockieren",
    "Disables Java plugins. JavaScript remains enabled.":
        "Deaktiviert Java-Plugins. JavaScript bleibt aktiviert.",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "Anti-DPI aktivieren",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "Verändert ausgehende Paketdaten, um Deep Packet Inspection zu umgehen.\nNützlich in Ländern mit Internet-Zensur.",
    "App pattern":
        "App-Muster",
    "Skip outbound proxy":              "Ausgehenden Proxy umgehen",
    "Don't route this app's traffic through outbound proxy":
        "Traffic dieser App nicht über den ausgehenden Proxy leiten",
    "Browser list included from {}":    "Browser-Liste eingebunden aus {}",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "Die Browser-Include-Liste und die Wildcard-Regel (*) können nicht entfernt werden.",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "Warnt vor bösartigen und Phishing-Websites.\nNutzt die Safe-Browsing-Datenbank von AdGuard.",
    "Send anonymous statistics":        "Anonyme Statistiken senden",
    "Send anonymous lookups to AdGuard.":
        "Anonyme Abfragen an AdGuard schicken.",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "Prüfung auf widerrufene Zertifikate mit Mozillas CRLite.\nSchneller und zuverlässiger als herkömmliche CRL/OCSP-Prüfungen.",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "Werbeblockierungsregeln auf HTTP/HTTPS-Anfragen anwenden.",
    "Save failed":                      "Speichern fehlgeschlagen",
    "Could not save proxy.yaml:\n{}":   "proxy.yaml konnte nicht gespeichert werden:\n{}",
    "Restarting AdGuard…":              "AdGuard wird neu gestartet…",
    "AdGuard restarted.":               "AdGuard neu gestartet.",
    "Restart failed: {}":               "Neustart fehlgeschlagen: {}",
    "Unknown error":                    "Unbekannter Fehler",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "Hinzufügen",
    "Search exceptions…":               "Ausnahmen durchsuchen…",
    "1 exception":                      "1 Ausnahme",
    "{} exceptions":                    "{} Ausnahmen",
    "'{}' is not a valid domain or IP address.":
        "'{}' ist keine gültige Domain oder IP-Adresse.",
    "'{}' is already in the list.":     "'{}' ist bereits in der Liste.",
    "Could not save exceptions:\n{}":
        "Ausnahmen konnten nicht gespeichert werden:\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "Übersicht",
    "Userscripts":                      "Userscripts",
    "Exceptions":                       "Ausnahmen",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "Lizenz zurücksetzen",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "Root-CA-Zertifikat für HTTPS-Filterung generieren. "
        "Das Zertifikat muss auf dem System installiert und als vertrauenswürdig eingestuft werden.",
    "Checking for updates…":            "Suche nach Updates…",
    "Firefox profile:":                 "Firefox-Profil:",
    "(optional) e.g. abcd1234.MyProfile":
        "(optional) z.B. abcd1234.MeinProfil",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "Filter-ID oder Name eingeben:",
    "Filter added.":                    "Filter hinzugefügt.",
    "Rename…":                          "Umbenennen…",
    "Rename filter":                    "Filter umbenennen",
    "New title:":                       "Neuer Titel:",
    "Filter renamed.":                  "Filter umbenannt.",
    "Filter trust updated.":            "Filtervertrauen aktualisiert.",
    "Filter URL:":                      "Filter-URL:",
    "Title:":                           "Titel:",
    "(optional)":                       "(optional)",
    "Trusted filter":                   "Vertrauenswürdiger Filter",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "DNS-Filter durchsuchen…",
    "No DNS filters found.":            "Keine DNS-Filter gefunden.",
    "DNS filter installed.":            "DNS-Filter installiert.",
    "DNS filter added.":                "DNS-Filter hinzugefügt.",
    "Remove DNS filter":                "DNS-Filter entfernen",
    "DNS filter {} removed.":           "DNS-Filter {} entfernt.",
    "Rename DNS filter":                "DNS-Filter umbenennen",
    "DNS filter renamed.":              "DNS-Filter umbenannt.",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "Logs exportieren…",
    "Export AdGuard CLI logs to a zip file":
        "AdGuard-CLI-Logs in eine ZIP-Datei exportieren",
    "Export settings…":                 "Einstellungen exportieren…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "Einen kryptografischen und HTTPS-Filterungs-Benchmark ausführen.",
    "Run benchmark":                    "Benchmark starten",
    "Done.":                            "Fertig.",
    "Export logs to…":                  "Logs exportieren nach…",
    "Export settings to…":              "Einstellungen exportieren nach…",
    "Zip files (*.zip);;All files (*)":
        "ZIP-Dateien (*.zip);;Alle Dateien (*)",
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
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "Prüft, ob das Zertifikat einer Seite widerrufen wurde (OCSP).\nAdGuard prüft asynchron und lässt die Verbindung durch, wenn die\nPrüfung langsam ist – bricht also selten eine Seite. Nur ausschalten,\nwenn ein Problem konkret darauf eingegrenzt wurde.",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "Certificate-Transparency-Prüfung erzwingen (Chromes CT-Richtlinie).\nSeiten, deren eigenes Zertifikat nicht CT-konform ist, werden nicht\nmehr gefiltert und vom Browser evtl. abgelehnt. Große Seiten sind\nkonform – nur bei gemeldetem Zertifikatsfehler probieren.",
    "Sites that don't load":
        "Seiten, die nicht laden",
    "Turn off HTTP/3 filtering":
        "HTTP/3-Filterung ausschalten",
    "No filters installed":
        "Keine Filter installiert",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "Eine Firewall-Regel blockiert HTTP/3; Browser nutzen HTTP/2.",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "Von der Filterung ausgenommene Apps (auch deren HTTP/3-Verkehr wird nicht gefiltert): {}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuard läuft nicht – es wird nichts gefiltert.",
    "could not remove the previous certificate":
        "Vorheriges Zertifikat konnte nicht entfernt werden",
    "HTTP/3 state unknown":
        "HTTP/3-Status unbekannt",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "Eine Firewall-Regel weist ausgehendes UDP 443 ab, QUIC ist damit nicht nutzbar.",
    "Browser policy disables QUIC: {}":
        "Browser-Richtlinie deaktiviert QUIC: {}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "Browser können AdGuard über HTTP/3 (UDP 443) umgehen.",
    "Checking…":
        "Wird geprüft…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "proxy.yaml konnte nicht gelesen werden – HTTP/3-Status unbekannt.",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "Firefox-Profile mit ausgeschaltetem HTTP/3: {} von {}",
    "HTTP/3 (QUIC)":
        "HTTP/3 (QUIC)",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "AdGuard blockiert HTTP/3; Browser weichen auf gefiltertes HTTP/2 aus.",
    "HTTP/3 is filtered by AdGuard.":
        "HTTP/3 wird von AdGuard gefiltert.",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "HTTP/3 in den Firefox-Profilen ausgeschaltet – Browser neu starten.",
    "HTTPS filtering is off – nothing is filtered.":
        "HTTPS-Filterung ist aus – es wird nichts gefiltert.",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "Proxy-Modus: {} – gefiltert wird nur, was über den Proxy läuft, und QUIC schicken Browser nicht darüber.",
    "unknown":
        "unbekannt",
    "AdGuard's certificate was not found. Generate it first.":
        "AdGuards Zertifikat wurde nicht gefunden. Erzeuge es zuerst.",
    "Certificate could not be installed in any browser.":
        "Zertifikat konnte in keinem Browser installiert werden.",
    "Certificate installed for {} of {} stores.":
        "Zertifikat in {} von {} Speichern installiert.",
    "Chromium-based browsers":
        "Chromium-basierte Browser",
    "No browser certificate stores found.":
        "Keine Browser-Zertifikatsspeicher gefunden.",
    "Restart your browsers for the certificate to take effect.":
        "Starte die Browser neu, damit das Zertifikat wirkt.",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "Ohne sudo/pkexec ausführen – die Installation erfolgt in deine eigenen Browser-Profile",
    "certificate not found after import":
        "Zertifikat nach dem Import nicht gefunden",
    "certutil not found – install the 'nss' package":
        "certutil nicht gefunden – Paket „nss“ installieren",
    "not found":
        "nicht vorhanden",
    "Could not read the filter list (unexpected CLI output).":
        "Filterliste konnte nicht gelesen werden (unerwartete CLI-Ausgabe).",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "Kein System-Tray gefunden. AdGuard Tray läuft ohne Symbol – aktiviere ein Tray/AppIndicator in deiner Leiste.",
    "URL must start with http:// or https://":
        "URL muss mit http:// oder https:// beginnen",
    "adguard-cli path does not exist or is not executable.":
        "adguard-cli-Pfad existiert nicht oder ist nicht ausführbar.",
    "That binary does not identify as adguard-cli. Save anyway?":
        "Diese Datei meldet sich nicht als adguard-cli. Trotzdem speichern?",
    "Update channel":                   "Update-Channel",
    "Switching update channel to {}…":  "Wechsle Update-Channel auf {}…",
    "Update channel set to {}":         "Update-Channel auf {} gesetzt",
    "Could not set update channel":     "Update-Channel konnte nicht gesetzt werden",
    "Invalid channel: {}":              "Ungültiger Channel: {}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        'Noch kein Zugriffsprotokoll ({}). AdGuard schreibt es, sobald es Datenverkehr gefiltert hat; läuft es als Systemdienst, gehört das Protokoll root und ist hier nicht lesbar.',
    'Cannot read the access log ({}): {}':
        'Zugriffsprotokoll ({}) nicht lesbar: {}',
    'Blocked':
        'Blockiert',
    'Blocked only':
        'Nur blockierte',
    "Refresh":
        "Neu laden",
    'Allow selected domain':
        'Ausgewählte Domain erlauben',
    'Block selected domain':
        'Ausgewählte Domain blockieren',
    'Activity':
        'Aktivität',
    'Time':
        'Zeit',
    'Domain':
        'Domain',
    'Result':
        'Ergebnis',
    'Rule':
        'Regel',
    'Size':
        'Größe',
    'Count':
        'Anzahl',
    'Could not read the access log.':
        'Zugriffsprotokoll konnte nicht gelesen werden.',
    '{} lines not understood':
        '{} Zeilen nicht verstanden',
    'Not a valid domain: {}':
        'Keine gültige Domain: {}',
    'Source: {}':
        'Quelle: {}',
    'Allowed':
        'Erlaubt',
    'Added rule: {}':
        'Regel hinzugefügt: {}',
    'Requests per hour, {} to {} · busiest hour: {}':
        'Anfragen pro Stunde, {} bis {} · stärkste Stunde: {}',
    'Last 24 hours':
        'Letzte 24 Stunden',
    'Last 7 days':
        'Letzte 7 Tage',
    'Requests':
        'Anfragen',
    'Traffic':
        'Datenmenge',

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        'Version {} ist verfügbar (installiert ist {}).',
    'Application update':
        'Anwendungs-Update',
    'Check for update':
        'Nach Update suchen',
    'Install update':
        'Update installieren',
    'Installing update…':
        'Update wird installiert…',
    'Restart now':
        'Jetzt neu starten',
    'Later':
        'Später',
    'You are running the latest version ({}).':
        'Die neueste Version ist installiert ({}).',
    'Installation not recognised':
        'Installationsart unbekannt',
    'Could not check for updates.':
        'Update-Prüfung fehlgeschlagen.',
    'Update with: {}':
        'Aktualisieren mit: {}',
    'Installed with the AUR package {}':
        'Installiert über das AUR-Paket {}',
    'Installed in {}':
        'Installiert in {}',
    'Running from a source checkout':
        'Läuft aus einem Quellcode-Checkout',
    'Version {} installed. Restart adguard-tray to use it.':
        'Version {} installiert. adguard-tray neu starten, um sie zu nutzen.',
    'Unexpected answer from GitHub: {}':
        'Unerwartete Antwort von GitHub: {}',
    'Download failed: {}':
        'Download fehlgeschlagen: {}',
    'Could not unpack the download: {}':
        'Download konnte nicht entpackt werden: {}',
    'This installation is managed elsewhere: {}':
        'Diese Installation wird anderweitig verwaltet: {}',
    'No permission to write to {}':
        'Keine Schreibrechte für {}',
    'GitHub returned {}.':
        'GitHub antwortete mit {}.',
    'No connection to GitHub: {}':
        'Keine Verbindung zu GitHub: {}',
    'The download does not contain adguard-tray.':
        'Der Download enthält kein adguard-tray.',
    'The download says version {} instead of {} – aborted.':
        'Der Download meldet Version {} statt {} – abgebrochen.',
    'GitHub is rate limiting this address. Try again later.':
        'GitHub drosselt diese Adresse. Später erneut versuchen.',
    'The download is larger than expected – aborted.':
        'Der Download ist größer als erwartet – abgebrochen.',
    'Update failed: {}':
        'Update fehlgeschlagen: {}',
    'The archive contains unexpected paths – aborted.':
        'Das Archiv enthält unerwartete Pfade – abgebrochen.',
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        'Update fehlgeschlagen, die alte Version konnte nicht wiederhergestellt werden. Aus {} wiederherstellen oder neu installieren mit: {}',
    'Last 30 days':
        'Letzte 30 Tage',
    'All time':
        'Gesamter Zeitraum',
    'Modified':
        'Verändert',
    'Rules':
        'Regeln',
    'Showing {} – show all':
        'Zeigt {} – alle anzeigen',
    'history {}':
        'Verlauf {}',
    'Filter list ID: {}':
        'Filterlisten-ID: {}',
    'App':
        'App',
    'Protocol':
        'Protokoll',
    'Type':
        'Typ',
    'Reset history':
        'Verlauf zurücksetzen',
    'Delete the stored history and read the log again.':
        'Gespeicherten Verlauf löschen und das Protokoll neu einlesen.',
    'Delete the stored history? Only what the log still holds can be read back.':
        'Gespeicherten Verlauf löschen? Zurückgelesen werden kann nur, was noch im Protokoll steht.',
    'History is not being updated: {}':
        'Verlauf wird nicht aktualisiert: {}',

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "1 nicht gespeicherte Änderung an den AdGuard-Einstellungen",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "Ein vertrauenswürdiger Filter kann Skripte in den Seiten ausführen, die du besuchst. Vertraue nur Listen aus Quellen, die du kennst.",
    "About":
        "Über",
    "Actions for the selected filter":
        "Aktionen für den ausgewählten Filter",
    "Ad blocking":
        "Werbeblocker",
    "Ad blocking is off, so the filter lists below have no effect.":
        "Der Werbeblocker ist aus, die Filterlisten unten wirken daher nicht.",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLI lädt den neuesten Build herunter und installiert ihn.",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "AdGuard CLI vergisst die Lizenz auf diesem Computer. Du musst sie danach erneut aktivieren.",
    "AdGuard CLI logs":
        "AdGuard-CLI-Logs",
    "AdGuard CLI update finished.":
        "AdGuard-CLI-Update abgeschlossen.",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "AdGuard-Tray-Log",
    "AdGuard doesn't filter these websites.":
        "AdGuard filtert diese Websites nicht.",
    "AdGuard is filtering this computer's traffic.":
        "AdGuard filtert den Datenverkehr dieses Computers.",
    "AdGuard restarts to load the new lists.":
        "AdGuard startet neu, um die neuen Listen zu laden.",
    "AdGuard's reply did not say whether it is running.":
        "Aus der Antwort von AdGuard geht nicht hervor, ob es läuft.",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "AdGuards Einstellungsdatei wurde nicht gefunden ({}). Starte adguard-cli einmal, um sie anzulegen.",
    "Add DNS filter by ID":
        "DNS-Filter nach ID hinzufügen",
    "Add DNS filter from URL":
        "DNS-Filter von URL hinzufügen",
    "Add filter":
        "Filter hinzufügen",
    "Add filter by ID":
        "Filter nach ID hinzufügen",
    "Add filter from URL":
        "Filter von URL hinzufügen",
    "Add rule":
        "Regel hinzufügen",
    "Add to browsers":
        "Zu Browsern hinzufügen",
    "Add userscript":
        "Userscript hinzufügen",
    "Add userscript…":
        "Userscript hinzufügen…",
    "Add website":
        "Website hinzufügen",
    "Add…":
        "Hinzufügen…",
    "Advanced":
        "Erweitert",
    "All available":
        "Alle verfügbaren",
    "Allow {}":
        "{} erlauben",
    "Also adds the certificate to this Firefox profile.":
        "Trägt das Zertifikat zusätzlich in dieses Firefox-Profil ein.",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "Auch bei Neustarts und Fehlern. Benötigt notify-send (libnotify) oder einen laufenden Benachrichtigungsdienst wie dunst, mako oder den von KDE.",
    "Appearance":
        "Darstellung",
    "Applies after AdGuard Tray restarts.":
        "Wird nach einem Neustart von AdGuard Tray wirksam.",
    "Apply":
        "Übernehmen",
    "Apply your changes to AdGuard's settings before closing?":
        "Änderungen an den AdGuard-Einstellungen vor dem Schließen übernehmen?",
    "Applying them restarts AdGuard if protection is on.":
        "Beim Übernehmen startet AdGuard neu, wenn der Schutz aktiv ist.",
    "Asks GitHub for the newest release.":
        "Fragt GitHub nach der neuesten Version.",
    "At a glance":
        "Auf einen Blick",
    "Automatic":
        "Automatisch",
    "Automatic – filter all apps":
        "Automatisch – alle Apps filtern",
    "Benchmark":
        "Benchmark",
    "Beta":
        "Beta",
    "Block ECH in DNS records":
        "ECH in DNS-Einträgen blockieren",
    "Block domains before a connection is made.":
        "Blockiert Domains, bevor eine Verbindung aufgebaut wird.",
    "Block {}":
        "{} blockieren",
    "Blocked (24 h)":
        "Blockiert (24 h)",
    "Browser list ({})":
        "Browser-Liste ({})",
    "By ID or name…":
        "Nach ID oder Name…",
    "Certificate":
        "Zertifikat",
    "Certificate checks":
        "Zertifikatsprüfungen",
    "Changes are collected in the bar at the bottom and applied together.":
        "Änderungen werden in der Leiste unten gesammelt und gemeinsam übernommen.",
    "Check again":
        "Erneut prüfen",
    "Check every":
        "Prüfen alle",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "Chromium- und Firefox-basierte Browser haben einen eigenen Zertifikatsspeicher.",
    "Close":
        "Schließen",
    "Controls which AdGuard CLI build “{}” installs.":
        "Legt fest, welchen AdGuard-CLI-Build „{}“ installiert.",
    "Could not add the rule.":
        "Regel konnte nicht hinzugefügt werden.",
    "Could not open {}":
        "{} konnte nicht geöffnet werden",
    "Could not read {}":
        "{} konnte nicht gelesen werden",
    "Could not refresh. Showing data from {}.":
        "Aktualisierung fehlgeschlagen. Angezeigt werden Daten von {}.",
    "Could not reset the history.":
        "Verlauf konnte nicht zurückgesetzt werden.",
    "Could not restart AdGuard.":
        "AdGuard konnte nicht neu gestartet werden.",
    "Could not start protection.":
        "Schutz konnte nicht gestartet werden.",
    "Could not stop protection.":
        "Schutz konnte nicht gestoppt werden.",
    "Create":
        "Erstellen",
    "Create certificate":
        "Zertifikat erstellen",
    "Custom":
        "Eigene",
    "DNS filter lists":
        "DNS-Filterlisten",
    "DNS filtering":
        "DNS-Filterung",
    "DNS filtering is off, so these lists have no effect.":
        "Die DNS-Filterung ist aus, diese Listen wirken daher nicht.",
    "DNS servers":
        "DNS-Server",
    "Dark":
        "Dunkel",
    "Default":
        "Standard",
    "Details":
        "Details",
    "Discard":
        "Verwerfen",
    "Don't filter":
        "Nicht filtern",
    "Don't trust":
        "Nicht vertrauen",
    "Downloads and installs the newest AdGuard CLI build.":
        "Lädt den neuesten AdGuard-CLI-Build herunter und installiert ihn.",
    "Duration":
        "Dauer",
    "Export…":
        "Exportieren…",
    "Filter everything":
        "Alles filtern",
    "Filter in place":
        "Direkt filtern",
    "Filtering":
        "Filterung",
    "Follow system":
        "Systemeinstellung",
    "From URL…":
        "Von URL…",
    "Go to updates":
        "Zu den Updates",
    "HTTP proxy: {}":
        "HTTP-Proxy: {}",
    "HTTPS filtering":
        "HTTPS-Filterung",
    "How much detail AdGuard Tray writes to its own log.":
        "Wie ausführlich AdGuard Tray in sein eigenes Log schreibt.",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "Lädt eine Seite nicht, schalte zuerst die HTTP/3-Filterung aus. Die anderen Prüfungen schützen alle Seiten – schalte sie nur aus, wenn das nicht geholfen hat.",
    "Included":
        "Eingebunden",
    "Installed":
        "Installiert",
    "License":
        "Lizenz",
    "Light":
        "Hell",
    "Logs":
        "Logs",
    "MIT license":
        "MIT-Lizenz",
    "Maintenance":
        "Wartung",
    "Manual proxy":
        "Manueller Proxy",
    "Manual – only apps set to use the proxy":
        "Manuell – nur Apps, die den Proxy verwenden",
    "More":
        "Mehr",
    "Move down":
        "Nach unten",
    "Move up":
        "Nach oben",
    "Network":
        "Netzwerk",
    "Nightly":
        "Nightly",
    "No requests yet – AdGuard logs requests while protection is on.":
        "Noch keine Anfragen – AdGuard protokolliert Anfragen, solange der Schutz aktiv ist.",
    "Not added":
        "Nicht hinzugefügt",
    "Nothing matches your search.":
        "Keine Treffer für deine Suche.",
    "Notify me when protection turns on or off":
        "Benachrichtigen, wenn der Schutz ein- oder ausgeschaltet wird",
    "Off":
        "Aus",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "Betrifft nur Browser, die DoH oder DoT nutzen. Mit „Aus“ umgehen sie AdGuards DNS-Filterung.",
    "Open AdGuard Tray":
        "AdGuard Tray öffnen",
    "Open exceptions":
        "Ausnahmen öffnen",
    "Open folder":
        "Ordner öffnen",
    "Open release page":
        "Release-Seite öffnen",
    "Pages":
        "Seiten",
    "Performance":
        "Leistung",
    "Protection":
        "Schutz",
    "Protection started.":
        "Schutz gestartet.",
    "Protection stopped.":
        "Schutz gestoppt.",
    "Proxy mode":
        "Proxy-Modus",
    "Redirect to AdGuard's DNS":
        "Zu AdGuards DNS umleiten",
    "Refresh this page (F5)":
        "Diese Seite aktualisieren (F5)",
    "Release (stable)":
        "Release (stabil)",
    "Remove rule":
        "Regel entfernen",
    "Remove “{}”?":
        "«{}» entfernen?",
    "Remove…":
        "Entfernen…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "Die aktuellen AdGuard-Einstellungen durch die aus {} ersetzen?\n\nAdGuard startet neu, um sie zu übernehmen.",
    "Reset history…":
        "Verlauf zurücksetzen…",
    "Reset…":
        "Zurücksetzen…",
    "Restart AdGuard":
        "AdGuard neu starten",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "Regeln gelten nur im automatischen Proxy-Modus. Die erste passende Regel gewinnt, daher \"*\" immer als letzte Regel.",
    "Safe Browsing":
        "Safe Browsing",
    "Save anyway":
        "Trotzdem speichern",
    "Saved. AdGuard restarts to apply the change.":
        "Gespeichert. AdGuard startet neu, um die Änderung zu übernehmen.",
    "Saved. Applies after AdGuard Tray restarts.":
        "Gespeichert. Wird nach einem Neustart von AdGuard Tray wirksam.",
    "Saved. The change applies when protection is turned on.":
        "Gespeichert. Die Änderung gilt, sobald der Schutz eingeschaltet wird.",
    "Secure DNS and ECH":
        "Sicheres DNS und ECH",
    "Secure DNS filtering":
        "Sichere DNS-Filterung",
    "Set the path in Settings":
        "Pfad in den Einstellungen festlegen",
    "Settings":
        "Einstellungen",
    "Show":
        "Anzeigen",
    "Show recent entries":
        "Letzte Einträge anzeigen",
    "Skip HTTPS filtering":
        "HTTPS-Filterung überspringen",
    "Some counts could not be loaded.":
        "Einige Zahlen konnten nicht geladen werden.",
    "Source code":
        "Quellcode",
    "Start AdGuard Tray when I log in":
        "AdGuard Tray beim Anmelden starten",
    "Startup":
        "Start",
    "Status checks":
        "Statusabfrage",
    "Stealth mode":
        "Tarnmodus",
    "System":
        "System",
    "The new lists load when protection is turned on.":
        "Die neuen Listen werden geladen, sobald der Schutz eingeschaltet ist.",
    "Theme":
        "Design",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "Damit werden HTTP/3-Filterung, OCSP-Prüfung, Certificate Transparency und Secure-DNS-Filterung ausgeschaltet. Widerrufene oder falsch ausgestellte Zertifikate fallen dann nicht mehr auf, und Browser können an AdGuards DNS-Filter vorbei auflösen.",
    "Time range":
        "Zeitraum",
    "To keep it but stop using it, switch it off instead.":
        "Zum Behalten ohne Nutzung stattdessen ausschalten.",
    "Top lists":
        "Toplisten",
    "Trust":
        "Vertrauen",
    "Trust “{}”?":
        "«{}» vertrauen?",
    "Trust…":
        "Vertrauen…",
    "Turn off all strict checks…":
        "Alle strengen Prüfungen ausschalten…",
    "Undo":
        "Rückgängig",
    "Unknown":
        "Unbekannt",
    "Unsaved changes":
        "Nicht gespeicherte Änderungen",
    "Update AdGuard CLI…":
        "AdGuard CLI aktualisieren…",
    "Update channel: {}":
        "Update-Channel: {}",
    "Updated {}":
        "Aktualisiert {}",
    "Updates":
        "Updates",
    "Used in manual mode only.":
        "Wird nur im manuellen Modus verwendet.",
    "Userscripts update together with filters.":
        "Userscripts werden zusammen mit den Filtern aktualisiert.",
    "Uses XDG autostart (~/.config/autostart).":
        "Nutzt XDG-Autostart (~/.config/autostart).",
    "Waiting for authorization…":
        "Warte auf Autorisierung…",
    "Website exceptions":
        "Website-Ausnahmen",
    "Websites":
        "Websites",
    "example.com or a link":
        "beispiel.de oder ein Link",
    "expires {}":
        "läuft ab am {}",
    "of {} requests in the last 24 hours":
        "von {} Anfragen in den letzten 24 Stunden",
    "{} of {} DNS filters on":
        "{} von {} DNS-Filtern an",
    "{} of {} filters on":
        "{} von {} Filtern an",
    "{} of {} on":
        "{} von {} an",
    "{} unsaved changes to AdGuard's settings":
        "{} nicht gespeicherte Änderungen an den AdGuard-Einstellungen",
    "“Follow system” uses your desktop's light or dark setting.":
        "„Systemeinstellung“ übernimmt die helle oder dunkle Darstellung deines Desktops.",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "Aktiv",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "AdGuards Zertifikat wird in jedes gefundene Browser-Profil auf diesem System eingetragen.\n\nDamit kann AdGuard den HTTPS-Verkehr dieser Browser mitlesen. Schließe die Browser vorher – sie lesen den Zertifikatsspeicher beim Start.",
    "Allow":
        "Erlauben",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "Übernimm oder verwirf zuerst deine Änderungen an den AdGuard-Einstellungen und starte dann neu.",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "Automatisch: AdGuard leitet den Datenverkehr aller Apps per iptables zu sich um. Manuell: AdGuard lauscht nur auf den SOCKS5- und HTTP-Ports unten.",
    "Block":
        "Blockieren",
    "Browser API blocking":
        "Browser-API-Blockierung",
    "CRLite":
        "CRLite",
    "Cancel":
        "Abbrechen",
    "Computers":
        "Computer",
    "Could not change the autostart entry.":
        "Autostart-Eintrag konnte nicht geändert werden.",
    "Could not export the logs.":
        "Logs konnten nicht exportiert werden.",
    "Could not export the settings.":
        "Einstellungen konnten nicht exportiert werden.",
    "Could not reset the license.":
        "Lizenz konnte nicht zurückgesetzt werden.",
    "Could not retrieve license info.":
        "Lizenzinformationen konnten nicht abgerufen werden.",
    "Could not run the benchmark.":
        "Benchmark konnte nicht ausgeführt werden.",
    "Could not save the settings.":
        "Einstellungen konnten nicht gespeichert werden.",
    "Could not set the update channel.":
        "Update-Channel konnte nicht gesetzt werden.",
    "Could not update AdGuard CLI.":
        "AdGuard CLI konnte nicht aktualisiert werden.",
    "Could not update the filters.":
        "Filter konnten nicht aktualisiert werden.",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "DNS-Upstream-Server.\n'default' = System-DNS.\nBeispiele: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com",
    "Expiration date":
        "Ablaufdatum",
    "Expires":
        "Läuft ab",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "HTTP/3 in den Firefox-Profilen wieder eingeschaltet – Browser neu starten.",
    "License key":
        "Lizenzschlüssel",
    "License type":
        "Lizenztyp",
    "Manual":
        "Manuell",
    "No exceptions.":
        "Keine Ausnahmen.",
    "OK":
        "OK",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "An: AdGuard filtert HTTP/3 (QUIC) selbst – experimentell, und manche\nBrowser lehnen HTTP/3 über ein selbst installiertes Zertifikat ohnehin ab.\nAus: AdGuard blockiert QUIC stattdessen, Browser weichen auf HTTP/2 aus,\ndas zuverlässig gefiltert wird.\nBeides gilt nur im automatischen Modus – im manuellen Modus erreicht\nHTTP/3-Verkehr AdGuard gar nicht.",
    "Owner":
        "Inhaber",
    "Personal":
        "Persönlich",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "Proxy-Modus: {} – UDP-Port 443 wird zu AdGuard umgeleitet.",
    "Save adguard-cli path":
        "adguard-cli-Pfad speichern",
    "Search domains or rules…":
        "Domains oder Regeln durchsuchen…",
    "Settings file":
        "Einstellungsdatei",
    "Status":
        "Status",
    "Trial":
        "Testversion",
    "Turn HTTP/3 back on in Firefox profiles":
        "HTTP/3 in Firefox-Profilen wieder einschalten",
    "Turn off":
        "Ausschalten",
    "Turn off HTTP/3 in Firefox profiles":
        "HTTP/3 in Firefox-Profilen ausschalten",
    "Turn off HTTP/3 in Firefox profiles…":
        "HTTP/3 in Firefox-Profilen ausschalten…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "HTTP/3 in {} Firefox-Profil(en) ausschalten?\n\nDeren Datenverkehr läuft dann über HTTP/2, das AdGuard filtern kann. Browser danach neu starten.",
    "Turn off all strict checks":
        "Alle strengen Prüfungen ausschalten",
    "Unavailable until AdGuard CLI reports its current channel.":
        "Nicht verfügbar, bis AdGuard CLI den aktuellen Channel meldet.",
    "Update AdGuard CLI":
        "AdGuard CLI aktualisieren",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "Wird nur im automatischen Modus verwendet. Bereiche (80:5221,5300:49151) oder einzelne Ports (80,443,8080).",
    "{} of {}":
        "{} von {}",
    "{} of {} userscripts on":
        "{} von {} Userscripts an",
    "{}% blocked":
        "{} % blockiert",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "Belästigungen",
    "General":
        "Allgemein",
    "Language-specific":
        "Sprachspezifisch",
    "Security":
        "Sicherheit",
    "Social widgets":
        "Social-Media-Widgets",
    "Expired":
        "Abgelaufen",
    "Autostart on login":
        "Autostart beim Login",
    "Add app rule":
        "App-Regel hinzufügen",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "Platzhalter sind erlaubt, z. B. *steam* oder *EasyAntiCheat*.",
    "There is already a rule for '{}'.":
        "Für „{}“ gibt es schon eine Regel.",
    "AdGuard settings":
        "AdGuard-Einstellungen",
    "Ads and trackers are not blocked until you enable protection.":
        "Werbung und Tracker werden erst blockiert, wenn du den Schutz aktivierst.",
    "Could not import the settings.":
        "Einstellungen konnten nicht importiert werden.",
    "Disable protection":
        "Schutz deaktivieren",
    "Enable protection":
        "Schutz aktivieren",
    "Export and import":
        "Export und Import",
    "Features":
        "Funktionen",
    "Import settings":
        "Einstellungen importieren",
    "Import settings from…":
        "Einstellungen importieren aus…",
    "Import settings…":
        "Einstellungen importieren…",
    "Import…":
        "Importieren…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "Filter, Regeln und Konfiguration in einer ZIP-Datei speichern oder daraus laden.",
    "Update":
        "Aktualisieren",
    "Version":
        "Version",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "{} ist keine Einstellungssicherung. Wähle eine Datei, die unter „AdGuard-Einstellungen“ mit „Exportieren“ gespeichert wurde.",
}
