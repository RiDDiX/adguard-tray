"""Dutch."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "Taal",
    "English":                           "Engels",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "Actief – Bescherming ingeschakeld",
    "Inactive – Protection stopped":        "Inactief – Bescherming gestopt",
    "Error retrieving status":              "Fout bij ophalen van status",
    "adguard-cli not found":                "adguard-cli niet gevonden",
    "Unknown status":                       "Onbekende status",
    "Checking status…":                     "Status controleren…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "Opnieuw starten",
    "Filters":                              "Filters",
    "Loading…":                             "Laden…",
    "Manage filters…":                      "Filters beheren…",
    "No userscripts installed":             "Geen userscripts geïnstalleerd",
    "Manage userscripts…":                  "Userscripts beheren…",
    "Quit":                                 "Afsluiten",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "actief",
    "inactive":                             "inactief",
    "System-wide filtering: {}":            "Systeembrede filtering: {}",
    "Error: {}":                            "Fout: {}",
    "AdGuard Tray – Error":                 "AdGuard Tray – Fout",
    "AdGuard is now active – protection running.":
        "AdGuard is nu actief – bescherming ingeschakeld.",
    "AdGuard has been stopped.":
        "AdGuard is gestopt.",
    "Could not retrieve status.":
        "Kon status niet ophalen.",
    "Command failed":                       "Opdracht mislukt",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " seconden",
    "How often adguard-cli status is checked automatically.":
        "Hoe vaak de status van adguard-cli automatisch wordt gecontroleerd.",
    "Log level:":                           "Logniveau:",
    "adguard-cli path:":                    "adguard-cli-pad:",
    "auto-detect via PATH":                 "automatisch detecteren via PATH",
    "Browse…":                              "Bladeren…",
    "Select adguard-cli binary":            "Uitvoerbaar bestand van adguard-cli kiezen",
    "Notifications":                        "Meldingen",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "Filters bijwerken",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "Werkt alle filters, DNS-filters, userscripts,\nSafebrowsingV2 en CRLite bij en controleert op app-updates.",
    "No filters found.":                    "Geen filters gevonden.",
    "Updating filters… (can take up to 2 minutes)":
        "Filters bijwerken… (kan tot 2 minuten duren)",
    "Update completed.":                    "Update voltooid.",
    "Update failed.":                       "Update mislukt.",
    "Installing: {}":                       "Installeren: {}",
    "Filter installed.":                    "Filter geïnstalleerd.",
    "Remove":                               "Verwijderen",
    "Remove filter":                        "Filter verwijderen",
    "Filter {} removed.":                   "Filter {} verwijderd.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        "Userscript installeren via een directe .js-URL",
    "No userscripts installed.":            "Geen userscripts geïnstalleerd.",
    "Userscript URL (direct .js URL):":     "Userscript-URL (directe .js-URL):",
    "Userscript installed.":                "Userscript geïnstalleerd.",
    'Remove "{}"':                          "“{}” verwijderen",
    "Remove userscript":                    "Userscript verwijderen",
    "'{}' removed.":                        "‘{}’ verwijderd.",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "adguard-cli is niet gevonden.\nInstalleer het via het officiële script of de AUR:\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "Onbekende fout bij ophalen van status",
    "AdGuard {} ok":                        "AdGuard {}: gelukt",
    "AdGuard via systemctl {} ok":          "AdGuard via systemctl {}: gelukt",
    "'{}' failed – insufficient privileges?":
        "‘{}’ mislukt – onvoldoende rechten?",
    "Could not retrieve filter list":
        "Kon filterlijst niet ophalen",
    "Filter {} enabled":                    "Filter {} ingeschakeld",
    "Could not enable filter {}":           "Kon filter {} niet inschakelen",
    "Filter {} disabled":                   "Filter {} uitgeschakeld",
    "Could not disable filter {}":
        "Kon filter {} niet uitschakelen",
    "Filter installed":                     "Filter geïnstalleerd",
    "Installation failed":                  "Installatie mislukt",
    "Filter {} removed":                    "Filter {} verwijderd",
    "Could not remove filter {}":
        "Kon filter {} niet verwijderen",
    "Filters updated":                      "Filters bijgewerkt",
    "Update failed":                        "Update mislukt",
    "Could not retrieve userscript list":
        "Kon lijst met userscripts niet ophalen",
    "Userscript '{}' enabled":              "Userscript ‘{}’ ingeschakeld",
    "Could not enable userscript '{}'":
        "Kon userscript ‘{}’ niet inschakelen",
    "Userscript '{}' disabled":             "Userscript ‘{}’ uitgeschakeld",
    "Could not disable userscript '{}'":
        "Kon userscript ‘{}’ niet uitschakelen",
    "Userscript '{}' removed":              "Userscript ‘{}’ verwijderd",
    "Could not remove userscript '{}'":
        "Kon userscript ‘{}’ niet verwijderen",
    "Userscript installed":                 "Userscript geïnstalleerd",
    "Other":                                "Overige",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "Filters zoeken…",
    "Search userscripts…":              "Userscripts zoeken…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "Kon proxy.yaml niet laden.\nPad: {}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "Apps",
    "Mode:":                            "Modus:",
    "Filtered ports:":                  "Gefilterde poorten:",
    "SOCKS5 port:":                     "SOCKS5-poort:",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "SOCKS5-proxypoort voor de handmatige modus.\nStel in op -1 om uit te schakelen.",
    "HTTP port:":                       "HTTP-poort:",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "HTTP-proxypoort voor de handmatige modus.\nStel in op -1 om uit te schakelen.",
    "Listen address:":                  "Luisteradres:",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "Adres waarop de proxy luistert.\n127.0.0.1 = alleen lokaal. 0.0.0.0 = alle interfaces (vereist authenticatie).",
    "Worker threads:":                  "Worker-threads:",
    "Number of proxy worker threads.":  "Aantal worker-threads van de proxy.",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "Ontsleutelt en filtert HTTPS-verkeer.\nNodig om advertenties op https-websites te blokkeren.\nVereist een vertrouwd rootcertificaat dat op het systeem is geïnstalleerd.",
    "Enable TLS 1.3":                   "TLS 1.3 inschakelen",
    "Enable TLS 1.3 support for filtered connections.":
        "Ondersteuning voor TLS 1.3 inschakelen voor gefilterde verbindingen.",
    "Filter HTTP/3 (QUIC) – experimental":
        "HTTP/3 (QUIC) filteren – experimenteel",
    "OCSP certificate checks":          "OCSP-certificaatcontroles",
    "Enforce Certificate Transparency": "Certificate Transparency afdwingen",
    "Filter EV certificate sites":      "Websites met EV-certificaat filteren",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "Standaard worden websites met Extended Validation-certificaten niet gefilterd.\nSchakel dit in om ook die te filteren (bijv. websites van banken).",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "ECH inschakelen voor betere privacy.\nVereist dat DNS-filtering is ingeschakeld.",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "Filtert DNS-verzoeken om advertenties en volgers op DNS-niveau te blokkeren.\nGebruikt een lokale DNS-proxy met instelbare upstreamservers.",
    "Upstream:":                        "Upstream:",
    "Fallbacks:":                       "Fallbacks:",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "Fallback-DNS-servers (gebruikt als de primaire upstream uitvalt).\n'default' = systeem-DNS. Lijst gescheiden door spaties.\nVoorbeeld: default 1.1.1.1",
    "Bootstraps:":                      "Bootstraps:",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "Bootstrap-DNS voor het omzetten van upstream-hostnamen.\n'default' = IP-adressen van de systeem-DNS. Alleen IP-adressen toegestaan.\nVoorbeeld: default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "Verwijdert de ECH-parameter uit SVCB/HTTPS-DNS-records.\nSchakel dit alleen in voor browsers die HTTPS-filtering niet automatisch herkennen.",
    "Master switch for all tracking protection features below.":
        "Hoofdschakelaar voor alle onderstaande functies voor bescherming tegen volgen.",
    "Cookies":                          "Cookies",
    "Block third-party cookies":        "Cookies van derden blokkeren",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "Verwijdert cookies van derden na een ingestelde tijd.\nVoorkomt dat je van website naar website wordt gevolgd.",
    "Lifetime (minutes):":              "Levensduur (minuten):",
    "0 = block immediately. Default: 180 minutes.":
        "0 = direct blokkeren. Standaard: 180 minuten.",
    "Block first-party cookies":        "Directe cookies blokkeren",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "Verwijdert alle cookies (ook directe cookies) na een ingestelde tijd.\nWaarschuwing: hierdoor word je op elke website afgemeld.",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = direct blokkeren. Standaard: 4320 minuten (3 dagen).",
    "Privacy":                          "Privacy",
    "Hide / reduce User-Agent":         "User-Agent verbergen / inkorten",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "Verwijdert identificerende delen uit de User-Agent.\nVermindert fingerprinting.",
    "Hide search queries in referrer":  "Zoekopdrachten in referrer verbergen",
    "Hides your search terms when clicking from a search engine to a website.":
        "Verbergt je zoektermen wanneer je vanuit een zoekmachine naar een website klikt.",
    "Remove referrer from third-party requests":
        "Referrer uit verzoeken van derden verwijderen",
    "Prevents third-party sites from knowing which page you came from.":
        "Voorkomt dat websites van derden weten van welke pagina je komt.",
    "Send Do-Not-Track signal":         "Do-Not-Track-signaal verzenden",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "Verzendt de DNT-header met verzoeken.\nLet op: de meeste websites negeren dit, maar sommige respecteren het.",
    "Disable third-party ETag cache":   "ETag-cache van derden uitschakelen",
    "Prevents tracking via ETag caching in third-party content.":
        "Voorkomt volgen via ETag-caching in inhoud van derden.",
    "Block third-party Authorization header":
        "Authorization-header van derden blokkeren",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "Blokkeert de Authorization-header in verzoeken van derden om volgen te voorkomen.",
    "Remove X-Client-Data header":      "X-Client-Data-header verwijderen",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "Verwijdert de X-Client-Data-header die Chrome naar Google-diensten stuurt.",
    "Block WebRTC":                     "WebRTC blokkeren",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "Voorkomt IP-lekken via WebRTC.\nKan videogesprekken en sommige webapps verstoren.",
    "Block Push API":                   "Push-API blokkeren",
    "Blocks browser push notifications from websites.":
        "Blokkeert pushmeldingen van websites in de browser.",
    "Block Location API":               "Locatie-API blokkeren",
    "Prevents websites from accessing your GPS location.":
        "Voorkomt dat websites toegang krijgen tot je GPS-locatie.",
    "Block Flash":                      "Flash blokkeren",
    "Blocks the Flash plugin.":
        "Blokkeert de Flash-plug-in.",
    "Block Java":                       "Java blokkeren",
    "Disables Java plugins. JavaScript remains enabled.":
        "Schakelt Java-plug-ins uit. JavaScript blijft ingeschakeld.",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "Anti-DPI inschakelen",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "Wijzigt uitgaande pakketgegevens om Deep Packet Inspection te omzeilen.\nNuttig in landen met internetcensuur.",
    "App pattern":
        "App-patroon",
    "Skip outbound proxy":              "Uitgaande proxy overslaan",
    "Don't route this app's traffic through outbound proxy":
        "Verkeer van deze app niet via de uitgaande proxy leiden",
    "Browser list included from {}":    "Browserlijst opgenomen uit {}",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "De opgenomen browserlijst en de jokertekenregel (*) kunnen niet worden verwijderd.",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "Waarschuwt voor schadelijke websites en phishingwebsites.\nGebruikt de Safe Browsing-database van AdGuard.",
    "Send anonymous statistics":        "Anonieme statistieken verzenden",
    "Send anonymous lookups to AdGuard.":
        "Anonieme opvragingen naar AdGuard verzenden.",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "Controle op intrekking van certificaten met CRLite van Mozilla.\nSneller en betrouwbaarder dan traditionele CRL/OCSP-controles.",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "Filterregels voor advertentieblokkering toepassen op HTTP/HTTPS-verzoeken.",
    "Save failed":                      "Opslaan mislukt",
    "Could not save proxy.yaml:\n{}":   "Kon proxy.yaml niet opslaan:\n{}",
    "Restarting AdGuard…":              "AdGuard wordt opnieuw gestart…",
    "AdGuard restarted.":               "AdGuard opnieuw gestart.",
    "Restart failed: {}":               "Opnieuw starten mislukt: {}",
    "Unknown error":                    "Onbekende fout",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "Toevoegen",
    "Search exceptions…":               "Uitzonderingen zoeken…",
    "1 exception":                      "1 uitzondering",
    "{} exceptions":                    "{} uitzonderingen",
    "'{}' is not a valid domain or IP address.":
        "‘{}’ is geen geldig domein of IP-adres.",
    "'{}' is already in the list.":     "‘{}’ staat al in de lijst.",
    "Could not save exceptions:\n{}":
        "Kon uitzonderingen niet opslaan:\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "Overzicht",
    "Userscripts":                      "Userscripts",
    "Exceptions":                       "Uitzonderingen",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "Licentie resetten",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "Genereert een root-CA-certificaat voor HTTPS-filtering. Het certificaat moet op je systeem worden geïnstalleerd en vertrouwd.",
    "Checking for updates…":            "Controleren op updates…",
    "Firefox profile:":                 "Firefox-profiel:",
    "(optional) e.g. abcd1234.MyProfile":
        "(optioneel) bijv. abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "Voer een filter-ID of naam in:",
    "Filter added.":                    "Filter toegevoegd.",
    "Rename…":                          "Naam wijzigen…",
    "Rename filter":                    "Naam van filter wijzigen",
    "New title:":                       "Nieuwe titel:",
    "Filter renamed.":                  "Naam van filter gewijzigd.",
    "Filter trust updated.":            "Vertrouwensstatus van filter bijgewerkt.",
    "Filter URL:":                      "Filter-URL:",
    "Title:":                           "Titel:",
    "(optional)":                       "(optioneel)",
    "Trusted filter":                   "Vertrouwd filter",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "DNS-filters zoeken…",
    "No DNS filters found.":            "Geen DNS-filters gevonden.",
    "DNS filter installed.":            "DNS-filter geïnstalleerd.",
    "DNS filter added.":                "DNS-filter toegevoegd.",
    "Remove DNS filter":                "DNS-filter verwijderen",
    "DNS filter {} removed.":           "DNS-filter {} verwijderd.",
    "Rename DNS filter":                "Naam van DNS-filter wijzigen",
    "DNS filter renamed.":              "Naam van DNS-filter gewijzigd.",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "Logboeken exporteren…",
    "Export AdGuard CLI logs to a zip file":
        "Exporteert de logboeken van AdGuard CLI naar een zip-bestand",
    "Export settings…":                 "Instellingen exporteren…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "Voert een benchmark uit voor cryptografie en HTTPS-filtering.",
    "Run benchmark":                    "Benchmark uitvoeren",
    "Done.":                            "Klaar.",
    "Export logs to…":                  "Logboeken exporteren naar…",
    "Export settings to…":              "Instellingen exporteren naar…",
    "Zip files (*.zip);;All files (*)":
        "Zip-bestanden (*.zip);;Alle bestanden (*)",
    "Log file not found.":              "Logbestand niet gevonden.",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "Kon DNS-filterlijst niet ophalen",
    "DNS filter {} enabled":            "DNS-filter {} ingeschakeld",
    "Could not enable DNS filter {}":   "Kon DNS-filter {} niet inschakelen",
    "DNS filter {} disabled":           "DNS-filter {} uitgeschakeld",
    "Could not disable DNS filter {}":  "Kon DNS-filter {} niet uitschakelen",
    "DNS filter installed":             "DNS-filter geïnstalleerd",
    "DNS filter {} removed":            "DNS-filter {} verwijderd",
    "Could not remove DNS filter {}":   "Kon DNS-filter {} niet verwijderen",
    "DNS filter added":                 "DNS-filter toegevoegd",
    "Could not add DNS filter":         "Kon DNS-filter niet toevoegen",
    "DNS filter title updated":         "DNS-filtertitel bijgewerkt",
    "Could not set DNS filter title":   "Kon DNS-filtertitel niet instellen",
    "Filter added":                     "Filter toegevoegd",
    "Could not add filter":             "Kon filter niet toevoegen",
    "Filter trust updated":             "Vertrouwensstatus van filter bijgewerkt",
    "Could not update filter trust":    "Kon vertrouwensstatus van filter niet bijwerken",
    "Filter title updated":             "Filtertitel bijgewerkt",
    "Could not set filter title":       "Kon filtertitel niet instellen",
    "License reset":                    "Licentie gereset",
    "Could not reset license":          "Kon licentie niet resetten",
    "Could not retrieve license info":  "Kon licentiegegevens niet ophalen",
    "Certificate generated":            "Certificaat gegenereerd",
    "Certificate generation failed":    "Genereren van certificaat mislukt",
    "Logs exported":                    "Logboeken geëxporteerd",
    "Log export failed":                "Exporteren van logboeken mislukt",
    "Settings exported":                "Instellingen geëxporteerd",
    "Settings export failed":           "Exporteren van instellingen mislukt",
    "Settings imported":                "Instellingen geïmporteerd",
    "Settings import failed":           "Importeren van instellingen mislukt",
    "Update check completed":           "Controle op updates voltooid",
    "Update check failed":              "Controle op updates mislukt",
    "Benchmark failed":                 "Benchmark mislukt",
    "AdGuard stopped (forced)":         "AdGuard gestopt (geforceerd)",
    "Could not stop AdGuard – process may still be running":
        "Kon AdGuard niet stoppen – het proces draait mogelijk nog",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "adguard-cli is niet gevonden op dit systeem.\n\nAanbevolen installatiemethode (officieel):\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\nAlternatief (Arch Linux AUR):\n  paru -S adguard-cli-bin\n\nAdGuard Tray start wel, maar starten/stoppen werkt pas nadat adguard-cli is geïnstalleerd.",
    "Copy install command":             "Installatieopdracht kopiëren",
    "Continue":                         "Doorgaan",
    "AdGuard Tray is already running":  "AdGuard Tray draait al",
    "Only one instance can run at a time. Check your system tray.":
        "Er kan maar één exemplaar tegelijk draaien. Kijk in je systeemvak.",
    "Authentication cancelled":         "Authenticatie geannuleerd",
    "Authorization failed":             "Autorisatie mislukt",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "Controleert of het certificaat van een website is ingetrokken (OCSP).\nAdGuard controleert asynchroon en laat de verbinding door als\nde controle traag is; dit geeft dus zelden problemen – laat het ingeschakeld,\ntenzij je een probleem tot deze controle hebt herleid.",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "Dwingt controles op Certificate Transparency af (het CT-beleid van Chrome).\nWebsites waarvan het eigen certificaat niet CT-conform is, worden niet meer gefilterd\nen de browser kan ze weigeren. Grote websites zijn conform, dus probeer\ndit alleen bij een website die een certificaatfout meldt.",
    "Sites that don't load":
        "Websites die niet laden",
    "Turn off HTTP/3 filtering":
        "HTTP/3-filtering uitschakelen",
    "No filters installed":
        "Geen filters geïnstalleerd",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "HTTP/3 wordt geblokkeerd door een firewallregel; browsers gebruiken HTTP/2.",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "Van filtering uitgesloten apps (hun HTTP/3-verkeer wordt ook niet gefilterd): {}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuard draait niet – er wordt niets gefilterd.",
    "could not remove the previous certificate":
        "kon het vorige certificaat niet verwijderen",
    "HTTP/3 state unknown":
        "HTTP/3-status onbekend",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "Een firewallregel weigert uitgaand UDP 443, waardoor QUIC niet kan worden gebruikt.",
    "Browser policy disables QUIC: {}":
        "Browserbeleid schakelt QUIC uit: {}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "Browsers kunnen AdGuard via HTTP/3 (UDP 443) omzeilen.",
    "Checking…":
        "Controleren…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "Kon proxy.yaml niet lezen – HTTP/3-status onbekend.",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "Profielen van Firefox-achtige browsers met HTTP/3 uitgeschakeld: {} van {}",
    "HTTP/3 (QUIC)":
        "HTTP/3 (QUIC)",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "HTTP/3 wordt geblokkeerd door AdGuard; browsers vallen terug op gefilterd HTTP/2.",
    "HTTP/3 is filtered by AdGuard.":
        "HTTP/3 wordt gefilterd door AdGuard.",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "HTTP/3 uitgeschakeld in Firefox-profielen – start de browser opnieuw.",
    "HTTPS filtering is off – nothing is filtered.":
        "HTTPS-filtering is uit – er wordt niets gefilterd.",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "Proxymodus: {} – alleen verkeer dat via de proxy loopt, wordt gefilterd, en browsers sturen QUIC er niet doorheen.",
    "unknown":
        "onbekend",
    "AdGuard's certificate was not found. Generate it first.":
        "Het certificaat van AdGuard is niet gevonden. Genereer het eerst.",
    "Certificate could not be installed in any browser.":
        "Het certificaat kon in geen enkele browser worden geïnstalleerd.",
    "Certificate installed for {} of {} stores.":
        "Certificaat geïnstalleerd in {} van {} certificaatopslagen.",
    "Chromium-based browsers":
        "Op Chromium gebaseerde browsers",
    "No browser certificate stores found.":
        "Geen certificaatopslagen van browsers gevonden.",
    "Restart your browsers for the certificate to take effect.":
        "Start je browsers opnieuw zodat het certificaat actief wordt.",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "Voer dit uit zonder sudo/pkexec – de installatie gebeurt in je eigen browserprofielen",
    "certificate not found after import":
        "certificaat niet gevonden na import",
    "certutil not found – install the 'nss' package":
        "certutil niet gevonden – installeer het pakket 'nss'",
    "not found":
        "niet gevonden",
    "Could not read the filter list (unexpected CLI output).":
        "Kon de filterlijst niet lezen (onverwachte CLI-uitvoer).",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "Geen systeemvak gevonden. AdGuard Tray draait zonder pictogram — schakel een systeemvak/AppIndicator in je paneel in.",
    "URL must start with http:// or https://":
        "URL moet beginnen met http:// of https://",
    "adguard-cli path does not exist or is not executable.":
        "Het adguard-cli-pad bestaat niet of is niet uitvoerbaar.",
    "That binary does not identify as adguard-cli. Save anyway?":
        "Dat uitvoerbare bestand identificeert zich niet als adguard-cli. Toch opslaan?",
    "Update channel":                   "Updatekanaal",
    "Switching update channel to {}…":  "Updatekanaal wijzigen in {}…",
    "Update channel set to {}":         "Updatekanaal ingesteld op {}",
    "Could not set update channel":     "Kon updatekanaal niet instellen",
    "Invalid channel: {}":              "Ongeldig kanaal: {}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        "Nog geen toegangslogboek ({}). AdGuard schrijft het zodra er verkeer is gefilterd; als AdGuard als systeemdienst draait, is het logboek van root en hier niet leesbaar.",
    'Cannot read the access log ({}): {}':
        "Kan het toegangslogboek ({}) niet lezen: {}",
    'Blocked':
        "Geblokkeerd",
    'Blocked only':
        "Alleen geblokkeerd",
    "Refresh":
        "Vernieuwen",
    'Allow selected domain':
        "Geselecteerd domein toestaan",
    'Block selected domain':
        "Geselecteerd domein blokkeren",
    'Activity':
        "Activiteit",
    'Time':
        "Tijd",
    'Domain':
        "Domein",
    'Result':
        "Resultaat",
    'Rule':
        "Regel",
    'Size':
        "Grootte",
    'Count':
        "Aantal",
    'Could not read the access log.':
        "Kon het toegangslogboek niet lezen.",
    '{} lines not understood':
        "Niet-begrepen logregels: {}",
    'Not a valid domain: {}':
        "Geen geldig domein: {}",
    'Source: {}':
        "Bron: {}",
    'Allowed':
        "Toegestaan",
    'Added rule: {}':
        "Regel toegevoegd: {}",
    'Requests per hour, {} to {} · busiest hour: {}':
        "Verzoeken per uur, {} tot {} · drukste uur: {}",
    'Last 24 hours':
        "Afgelopen 24 uur",
    'Last 7 days':
        "Afgelopen 7 dagen",
    'Requests':
        "Verzoeken",
    'Traffic':
        "Dataverkeer",

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        "Versie {} is beschikbaar (je hebt {}).",
    'Application update':
        "Programma-update",
    'Check for update':
        "Controleren op update",
    'Install update':
        "Update installeren",
    'Installing update…':
        "Update wordt geïnstalleerd…",
    'Restart now':
        "Nu opnieuw starten",
    'Later':
        "Later",
    'You are running the latest version ({}).':
        "Je gebruikt de nieuwste versie ({}).",
    'Installation not recognised':
        "Installatie niet herkend",
    'Could not check for updates.':
        "Kon niet controleren op updates.",
    'Update with: {}':
        "Bijwerken met: {}",
    'Installed with the AUR package {}':
        "Geïnstalleerd met het AUR-pakket {}",
    'Installed in {}':
        "Geïnstalleerd in {}",
    'Running from a source checkout':
        "Draait vanuit een lokale kopie van de broncode",
    'Version {} installed. Restart adguard-tray to use it.':
        "Versie {} geïnstalleerd. Start adguard-tray opnieuw om deze te gebruiken.",
    'Unexpected answer from GitHub: {}':
        "Onverwacht antwoord van GitHub: {}",
    'Download failed: {}':
        "Downloaden mislukt: {}",
    'Could not unpack the download: {}':
        "Kon de download niet uitpakken: {}",
    'This installation is managed elsewhere: {}':
        "Deze installatie wordt elders beheerd: {}",
    'No permission to write to {}':
        "Geen schrijfrechten voor {}",
    'GitHub returned {}.':
        "GitHub antwoordde met {}.",
    'No connection to GitHub: {}':
        "Geen verbinding met GitHub: {}",
    'The download does not contain adguard-tray.':
        "De download bevat geen adguard-tray.",
    'The download says version {} instead of {} – aborted.':
        "De download vermeldt versie {} in plaats van {} – afgebroken.",
    'GitHub is rate limiting this address. Try again later.':
        "GitHub beperkt het aantal verzoeken van dit adres. Probeer het later opnieuw.",
    'The download is larger than expected – aborted.':
        "De download is groter dan verwacht – afgebroken.",
    'Update failed: {}':
        "Update mislukt: {}",
    'The archive contains unexpected paths – aborted.':
        "Het archief bevat onverwachte paden – afgebroken.",
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        "Update mislukt en de oude versie kon niet worden hersteld. Herstel deze vanuit {} of installeer opnieuw met: {}",
    'Last 30 days':
        "Afgelopen 30 dagen",
    'All time':
        "Alles",
    'Modified':
        "Gewijzigd",
    'Rules':
        "Regels",
    'Showing {} – show all':
        "{} getoond – alles tonen",
    'history {}':
        "geschiedenis: {}",
    'Filter list ID: {}':
        "Filterlijst-ID: {}",
    'App':
        "App",
    'Protocol':
        "Protocol",
    'Type':
        "Type",
    'Reset history':
        "Geschiedenis wissen",
    'Delete the stored history and read the log again.':
        "Verwijdert de opgeslagen geschiedenis en leest het logboek opnieuw in.",
    'Delete the stored history? Only what the log still holds can be read back.':
        "Opgeslagen geschiedenis verwijderen? Alleen wat nog in het logboek staat, kan opnieuw worden ingelezen.",
    'History is not being updated: {}':
        "Geschiedenis wordt niet bijgewerkt: {}",

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "1 niet-opgeslagen wijziging in de AdGuard-instellingen",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "Een vertrouwd filter kan scripts uitvoeren op de pagina's die je bezoekt. Vertrouw alleen lijsten uit bronnen die je kent.",
    "About":
        "Over",
    "Actions for the selected filter":
        "Acties voor het geselecteerde filter",
    "Ad blocking":
        "Advertentieblokkering",
    "Ad blocking is off, so the filter lists below have no effect.":
        "Advertentieblokkering staat uit, dus de filterlijsten hieronder hebben geen effect.",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLI downloadt en installeert de nieuwste build.",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "AdGuard CLI vergeet de licentie op deze computer. Je moet deze daarna opnieuw activeren.",
    "AdGuard CLI logs":
        "Logboeken van AdGuard CLI",
    "AdGuard CLI update finished.":
        "Bijwerken van AdGuard CLI voltooid.",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "Logboek van AdGuard Tray",
    "AdGuard doesn't filter these websites.":
        "AdGuard filtert deze websites niet.",
    "AdGuard is filtering this computer's traffic.":
        "AdGuard filtert het verkeer van deze computer.",
    "AdGuard restarts to load the new lists.":
        "AdGuard wordt opnieuw gestart om de nieuwe lijsten te laden.",
    "AdGuard's reply did not say whether it is running.":
        "Uit het antwoord van AdGuard blijkt niet of het actief is.",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "Het instellingenbestand van AdGuard is niet gevonden ({}). Voer adguard-cli één keer uit om het aan te maken.",
    "Add DNS filter by ID":
        "DNS-filter toevoegen op ID",
    "Add DNS filter from URL":
        "DNS-filter toevoegen via URL",
    "Add filter":
        "Filter toevoegen",
    "Add filter by ID":
        "Filter toevoegen op ID",
    "Add filter from URL":
        "Filter toevoegen via URL",
    "Add rule":
        "Regel toevoegen",
    "Add to browsers":
        "Aan browsers toevoegen",
    "Add userscript":
        "Userscript toevoegen",
    "Add userscript…":
        "Userscript toevoegen…",
    "Add website":
        "Website toevoegen",
    "Add…":
        "Toevoegen…",
    "Advanced":
        "Geavanceerd",
    "All available":
        "Alle beschikbare",
    "Allow {}":
        "{} toestaan",
    "Also adds the certificate to this Firefox profile.":
        "Voegt het certificaat ook aan dit Firefox-profiel toe.",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "Ook bij herstarts en fouten. Vereist notify-send (libnotify) of een actieve meldingsdienst zoals dunst, mako of die van KDE.",
    "Appearance":
        "Uiterlijk",
    "Applies after AdGuard Tray restarts.":
        "Wordt van kracht nadat AdGuard Tray opnieuw is gestart.",
    "Apply":
        "Toepassen",
    "Apply your changes to AdGuard's settings before closing?":
        "Wijzigingen in de AdGuard-instellingen toepassen voor het sluiten?",
    "Applying them restarts AdGuard if protection is on.":
        "Bij het toepassen wordt AdGuard opnieuw gestart als de bescherming is ingeschakeld.",
    "Asks GitHub for the newest release.":
        "Vraagt de nieuwste release op bij GitHub.",
    "At a glance":
        "In één oogopslag",
    "Automatic":
        "Automatisch",
    "Automatic – filter all apps":
        "Automatisch – alle apps filteren",
    "Benchmark":
        "Benchmark",
    "Beta":
        "Bèta",
    "Block ECH in DNS records":
        "ECH in DNS-records blokkeren",
    "Block domains before a connection is made.":
        "Blokkeert domeinen voordat er een verbinding wordt gemaakt.",
    "Block {}":
        "{} blokkeren",
    "Blocked (24 h)":
        "Geblokkeerd (24 uur)",
    "Browser list ({})":
        "Browserlijst ({})",
    "By ID or name…":
        "Op ID of naam…",
    "Certificate":
        "Certificaat",
    "Certificate checks":
        "Certificaatcontroles",
    "Changes are collected in the bar at the bottom and applied together.":
        "Wijzigingen worden in de balk onderaan verzameld en samen toegepast.",
    "Check again":
        "Opnieuw controleren",
    "Check every":
        "Controleren elke",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "Op Chromium en Firefox gebaseerde browsers hebben een eigen certificaatopslag.",
    "Close":
        "Sluiten",
    "Controls which AdGuard CLI build “{}” installs.":
        "Bepaalt welke build van AdGuard CLI “{}” installeert.",
    "Could not add the rule.":
        "Kon de regel niet toevoegen.",
    "Could not open {}":
        "Kon {} niet openen",
    "Could not read {}":
        "Kon {} niet lezen",
    "Could not refresh. Showing data from {}.":
        "Kon niet vernieuwen. Gegevens van {} worden getoond.",
    "Could not reset the history.":
        "Kon de geschiedenis niet wissen.",
    "Could not restart AdGuard.":
        "Kon AdGuard niet opnieuw starten.",
    "Could not start protection.":
        "Kon de bescherming niet starten.",
    "Could not stop protection.":
        "Kon de bescherming niet stoppen.",
    "Create":
        "Aanmaken",
    "Create certificate":
        "Certificaat aanmaken",
    "Custom":
        "Aangepast",
    "DNS filter lists":
        "DNS-filterlijsten",
    "DNS filtering":
        "DNS-filtering",
    "DNS filtering is off, so these lists have no effect.":
        "DNS-filtering staat uit, dus deze lijsten hebben geen effect.",
    "DNS servers":
        "DNS-servers",
    "Dark":
        "Donker",
    "Default":
        "Standaard",
    "Details":
        "Details",
    "Discard":
        "Verwerpen",
    "Don't filter":
        "Niet filteren",
    "Don't trust":
        "Niet vertrouwen",
    "Downloads and installs the newest AdGuard CLI build.":
        "Downloadt en installeert de nieuwste build van AdGuard CLI.",
    "Duration":
        "Duur",
    "Export…":
        "Exporteren…",
    "Filter everything":
        "Alles filteren",
    "Filter in place":
        "Ter plekke filteren",
    "Filtering":
        "Filtering",
    "Follow system":
        "Systeem volgen",
    "From URL…":
        "Via URL…",
    "Go to updates":
        "Naar updates",
    "HTTP proxy: {}":
        "HTTP-proxy: {}",
    "HTTPS filtering":
        "HTTPS-filtering",
    "How much detail AdGuard Tray writes to its own log.":
        "Hoeveel details AdGuard Tray in zijn eigen logboek schrijft.",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "Als een website niet laadt, schakel dan eerst HTTP/3-filtering uit. De andere controles beschermen elke website – schakel ze alleen uit als dat niet heeft geholpen.",
    "Included":
        "Inbegrepen",
    "Installed":
        "Geïnstalleerd",
    "License":
        "Licentie",
    "Light":
        "Licht",
    "Logs":
        "Logboeken",
    "MIT license":
        "MIT-licentie",
    "Maintenance":
        "Onderhoud",
    "Manual proxy":
        "Handmatige proxy",
    "Manual – only apps set to use the proxy":
        "Handmatig – alleen apps die zijn ingesteld om de proxy te gebruiken",
    "More":
        "Meer",
    "Move down":
        "Omlaag",
    "Move up":
        "Omhoog",
    "Network":
        "Netwerk",
    "Nightly":
        "Nightly",
    "No requests yet – AdGuard logs requests while protection is on.":
        "Nog geen verzoeken – AdGuard legt verzoeken vast zolang de bescherming is ingeschakeld.",
    "Not added":
        "Niet toegevoegd",
    "Nothing matches your search.":
        "Niets gevonden voor je zoekopdracht.",
    "Notify me when protection turns on or off":
        "Melding geven wanneer de bescherming wordt in- of uitgeschakeld",
    "Off":
        "Uit",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "Geldt alleen voor browsers die DoH of DoT gebruiken. Met “Uit” omzeilen ze de DNS-filtering van AdGuard.",
    "Open AdGuard Tray":
        "AdGuard Tray openen",
    "Open exceptions":
        "Uitzonderingen openen",
    "Open folder":
        "Map openen",
    "Open release page":
        "Releasepagina openen",
    "Pages":
        "Pagina's",
    "Performance":
        "Prestaties",
    "Protection":
        "Bescherming",
    "Protection started.":
        "Bescherming gestart.",
    "Protection stopped.":
        "Bescherming gestopt.",
    "Proxy mode":
        "Proxymodus",
    "Redirect to AdGuard's DNS":
        "Naar de DNS van AdGuard omleiden",
    "Refresh this page (F5)":
        "Deze pagina vernieuwen (F5)",
    "Release (stable)":
        "Release (stabiel)",
    "Remove rule":
        "Regel verwijderen",
    "Remove “{}”?":
        "“{}” verwijderen?",
    "Remove…":
        "Verwijderen…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "De huidige AdGuard-instellingen vervangen door die uit {}?\n\nAdGuard wordt opnieuw gestart om ze toe te passen.",
    "Reset history…":
        "Geschiedenis wissen…",
    "Reset…":
        "Resetten…",
    "Restart AdGuard":
        "AdGuard opnieuw starten",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "Regels gelden alleen in de automatische proxymodus. De eerste regel die overeenkomt, wint, dus zet \"*\" als laatste.",
    "Safe Browsing":
        "Safe Browsing",
    "Save anyway":
        "Toch opslaan",
    "Saved. AdGuard restarts to apply the change.":
        "Opgeslagen. AdGuard wordt opnieuw gestart om de wijziging toe te passen.",
    "Saved. Applies after AdGuard Tray restarts.":
        "Opgeslagen. Wordt van kracht nadat AdGuard Tray opnieuw is gestart.",
    "Saved. The change applies when protection is turned on.":
        "Opgeslagen. De wijziging wordt van kracht zodra de bescherming wordt ingeschakeld.",
    "Secure DNS and ECH":
        "Beveiligde DNS en ECH",
    "Secure DNS filtering":
        "Beveiligde DNS-filtering",
    "Set the path in Settings":
        "Pad instellen in Instellingen",
    "Settings":
        "Instellingen",
    "Show":
        "Tonen",
    "Show recent entries":
        "Recente items tonen",
    "Skip HTTPS filtering":
        "HTTPS-filtering overslaan",
    "Some counts could not be loaded.":
        "Sommige aantallen konden niet worden geladen.",
    "Source code":
        "Broncode",
    "Start AdGuard Tray when I log in":
        "AdGuard Tray starten bij aanmelden",
    "Startup":
        "Opstarten",
    "Status checks":
        "Statuscontrole",
    "Stealth mode":
        "Incognitomodus",
    "System":
        "Systeem",
    "The new lists load when protection is turned on.":
        "De nieuwe lijsten worden geladen zodra de bescherming wordt ingeschakeld.",
    "Theme":
        "Thema",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "Hiermee worden HTTP/3-filtering, OCSP-controles, Certificate Transparency en beveiligde DNS-filtering uitgeschakeld. Ingetrokken of onterecht uitgegeven certificaten vallen dan niet meer op, en browsers kunnen namen omzetten buiten het DNS-filter van AdGuard om.",
    "Time range":
        "Periode",
    "To keep it but stop using it, switch it off instead.":
        "Wil je het behouden maar niet meer gebruiken, schakel het dan uit.",
    "Top lists":
        "Toplijsten",
    "Trust":
        "Vertrouwen",
    "Trust “{}”?":
        "“{}” vertrouwen?",
    "Trust…":
        "Vertrouwen…",
    "Turn off all strict checks…":
        "Alle strikte controles uitschakelen…",
    "Undo":
        "Ongedaan maken",
    "Unknown":
        "Onbekend",
    "Unsaved changes":
        "Niet-opgeslagen wijzigingen",
    "Update AdGuard CLI…":
        "AdGuard CLI bijwerken…",
    "Update channel: {}":
        "Updatekanaal: {}",
    "Updated {}":
        "Bijgewerkt: {}",
    "Updates":
        "Updates",
    "Used in manual mode only.":
        "Wordt alleen in de handmatige modus gebruikt.",
    "Userscripts update together with filters.":
        "Userscripts worden samen met de filters bijgewerkt.",
    "Uses XDG autostart (~/.config/autostart).":
        "Gebruikt XDG-autostart (~/.config/autostart).",
    "Waiting for authorization…":
        "Wachten op autorisatie…",
    "Website exceptions":
        "Website-uitzonderingen",
    "Websites":
        "Websites",
    "example.com or a link":
        "voorbeeld.nl of een link",
    "expires {}":
        "verloopt: {}",
    "of {} requests in the last 24 hours":
        "van {} verzoeken in de afgelopen 24 uur",
    "{} of {} DNS filters on":
        "{} van {} DNS-filters aan",
    "{} of {} filters on":
        "{} van {} filters aan",
    "{} of {} on":
        "{} van {} aan",
    "{} unsaved changes to AdGuard's settings":
        "{} niet-opgeslagen wijzigingen in de AdGuard-instellingen",
    "“Follow system” uses your desktop's light or dark setting.":
        "“Systeem volgen” neemt de lichte of donkere modus van je bureaublad over.",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "Actief",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "Het AdGuard-certificaat wordt toegevoegd aan elk browserprofiel dat op dit systeem is gevonden.\n\nHierdoor kan AdGuard het HTTPS-verkeer in die browsers inspecteren. Sluit eerst je browsers – ze lezen de certificaatopslag bij het opstarten.",
    "Allow":
        "Toestaan",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "Pas eerst je wijzigingen in de AdGuard-instellingen toe of verwerp ze, en start daarna opnieuw.",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "Automatisch: AdGuard leidt het verkeer van alle apps via iptables naar zichzelf om. Handmatig: AdGuard luistert alleen op de SOCKS5- en HTTP-poorten hieronder.",
    "Block":
        "Blokkeren",
    "Browser API blocking":
        "Blokkering van browser-API's",
    "CRLite":
        "CRLite",
    "Cancel":
        "Annuleren",
    "Computers":
        "Computers",
    "Could not change the autostart entry.":
        "Kon de autostartvermelding niet wijzigen.",
    "Could not export the logs.":
        "Kon de logboeken niet exporteren.",
    "Could not export the settings.":
        "Kon de instellingen niet exporteren.",
    "Could not reset the license.":
        "Kon de licentie niet resetten.",
    "Could not retrieve license info.":
        "Kon licentiegegevens niet ophalen.",
    "Could not run the benchmark.":
        "Kon de benchmark niet uitvoeren.",
    "Could not save the settings.":
        "Kon de instellingen niet opslaan.",
    "Could not set the update channel.":
        "Kon het updatekanaal niet instellen.",
    "Could not update AdGuard CLI.":
        "Kon AdGuard CLI niet bijwerken.",
    "Could not update the filters.":
        "Kon de filters niet bijwerken.",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "Upstream-DNS-server.\n'default' = systeem-DNS.\nVoorbeelden: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com",
    "Expiration date":
        "Vervaldatum",
    "Expires":
        "Verloopt",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "HTTP/3 weer ingeschakeld in Firefox-profielen – start de browser opnieuw.",
    "License key":
        "Licentiesleutel",
    "License type":
        "Licentietype",
    "Manual":
        "Handmatig",
    "No exceptions.":
        "Geen uitzonderingen.",
    "OK":
        "OK",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "Aan: AdGuard filtert HTTP/3 (QUIC) zelf – experimenteel, en sommige\nbrowsers weigeren HTTP/3 via een zelf geïnstalleerd certificaat toch al.\nUit: AdGuard blokkeert in plaats daarvan QUIC, zodat browsers terugvallen op HTTP/2,\ndat betrouwbaar wordt gefilterd.\nIn beide gevallen geldt dit alleen in de automatische modus – in de handmatige modus\nbereikt HTTP/3-verkeer AdGuard nooit.",
    "Owner":
        "Eigenaar",
    "Personal":
        "Persoonlijk",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "Proxymodus: {} – UDP-poort 443 wordt omgeleid naar AdGuard.",
    "Save adguard-cli path":
        "adguard-cli-pad opslaan",
    "Search domains or rules…":
        "Domeinen of regels zoeken…",
    "Settings file":
        "Instellingenbestand",
    "Status":
        "Status",
    "Trial":
        "Proefversie",
    "Turn HTTP/3 back on in Firefox profiles":
        "HTTP/3 in Firefox-profielen weer inschakelen",
    "Turn off":
        "Uitschakelen",
    "Turn off HTTP/3 in Firefox profiles":
        "HTTP/3 in Firefox-profielen uitschakelen",
    "Turn off HTTP/3 in Firefox profiles…":
        "HTTP/3 in Firefox-profielen uitschakelen…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "HTTP/3 uitschakelen in de profielen van Firefox-achtige browsers (aantal: {})?\n\nHun verkeer loopt dan via HTTP/2, dat AdGuard kan filteren. Start de browser daarna opnieuw.",
    "Turn off all strict checks":
        "Alle strikte controles uitschakelen",
    "Unavailable until AdGuard CLI reports its current channel.":
        "Niet beschikbaar totdat AdGuard CLI het huidige kanaal doorgeeft.",
    "Update AdGuard CLI":
        "AdGuard CLI bijwerken",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "Wordt alleen in de automatische modus gebruikt. Bereiken (80:5221,5300:49151) of losse poorten (80,443,8080).",
    "{} of {}":
        "{} van {}",
    "{} of {} userscripts on":
        "{} van {} userscripts aan",
    "{}% blocked":
        "{}% geblokkeerd",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "Ergernissen",
    "General":
        "Algemeen",
    "Language-specific":
        "Taalspecifiek",
    "Security":
        "Beveiliging",
    "Social widgets":
        "Sociale widgets",
    "Expired":
        "Verlopen",
    "Autostart on login":
        "Automatisch starten bij aanmelden",
    "Add app rule":
        "App-regel toevoegen",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "Jokertekens werken, bijv. *steam* of *EasyAntiCheat*.",
    "There is already a rule for '{}'.":
        "Er is al een regel voor ‘{}’.",
    "AdGuard settings":
        "AdGuard-instellingen",
    "Ads and trackers are not blocked until you enable protection.":
        "Advertenties en volgers worden pas geblokkeerd als je de bescherming inschakelt.",
    "Could not import the settings.":
        "Kon de instellingen niet importeren.",
    "Disable protection":
        "Bescherming uitschakelen",
    "Enable protection":
        "Bescherming inschakelen",
    "Export and import":
        "Exporteren en importeren",
    "Features":
        "Functies",
    "Import settings":
        "Instellingen importeren",
    "Import settings from…":
        "Instellingen importeren uit…",
    "Import settings…":
        "Instellingen importeren…",
    "Import…":
        "Importeren…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "Filters, regels en configuratie in een zip-bestand opslaan of daaruit laden.",
    "Update":
        "Bijwerken",
    "Version":
        "Versie",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "{} is geen instellingenexport. Kies een bestand dat is opgeslagen met “Exporteren” onder “AdGuard-instellingen”.",
}
