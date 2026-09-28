"""Polish."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "Język",
    "English":                           "Angielski",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "Aktywny – ochrona działa",
    "Inactive – Protection stopped":        "Nieaktywny – ochrona zatrzymana",
    "Error retrieving status":              "Błąd pobierania stanu",
    "adguard-cli not found":                "Nie znaleziono adguard-cli",
    "Unknown status":                       "Nieznany stan",
    "Checking status…":                     "Sprawdzanie stanu…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "Uruchom ponownie",
    "Filters":                              "Filtry",
    "Loading…":                             "Wczytywanie…",
    "Manage filters…":                      "Zarządzaj filtrami…",
    "No userscripts installed":             "Brak zainstalowanych skryptów użytkownika",
    "Manage userscripts…":                  "Zarządzaj skryptami użytkownika…",
    "Quit":                                 "Zakończ",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "aktywne",
    "inactive":                             "nieaktywne",
    "System-wide filtering: {}":            "Filtrowanie w całym systemie: {}",
    "Error: {}":                            "Błąd: {}",
    "AdGuard Tray – Error":                 "AdGuard Tray – błąd",
    "AdGuard is now active – protection running.":
        "AdGuard jest teraz aktywny – ochrona działa.",
    "AdGuard has been stopped.":
        "Zatrzymano AdGuard.",
    "Could not retrieve status.":
        "Nie udało się pobrać stanu.",
    "Command failed":                       "Polecenie nie powiodło się",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " s",
    "How often adguard-cli status is checked automatically.":
        "Jak często stan adguard-cli jest automatycznie sprawdzany.",
    "Log level:":                           "Poziom dziennika:",
    "adguard-cli path:":                    "Ścieżka do adguard-cli:",
    "auto-detect via PATH":                 "automatyczne wykrywanie w PATH",
    "Browse…":                              "Przeglądaj…",
    "Select adguard-cli binary":            "Wybierz plik wykonywalny adguard-cli",
    "Notifications":                        "Powiadomienia",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "Aktualizuj filtry",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "Aktualizuje wszystkie filtry, filtry DNS, skrypty użytkownika,\nSafebrowsingV2, CRLite i sprawdza aktualizacje aplikacji.",
    "No filters found.":                    "Nie znaleziono filtrów.",
    "Updating filters… (can take up to 2 minutes)":
        "Aktualizowanie filtrów… (może potrwać do 2 minut)",
    "Update completed.":                    "Aktualizacja zakończona.",
    "Update failed.":                       "Aktualizacja nie powiodła się.",
    "Installing: {}":                       "Instalowanie: {}",
    "Filter installed.":                    "Zainstalowano filtr.",
    "Remove":                               "Usuń",
    "Remove filter":                        "Usuń filtr",
    "Filter {} removed.":                   "Usunięto filtr {}.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        "Zainstaluj skrypt użytkownika z bezpośredniego adresu URL pliku .js",
    "No userscripts installed.":            "Brak zainstalowanych skryptów użytkownika.",
    "Userscript URL (direct .js URL):":     "Adres URL skryptu użytkownika (bezpośredni adres pliku .js):",
    "Userscript installed.":                "Zainstalowano skrypt użytkownika.",
    'Remove "{}"':                          "Usuń „{}”",
    "Remove userscript":                    "Usuń skrypt użytkownika",
    "'{}' removed.":                        "Usunięto „{}”.",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "Nie znaleziono adguard-cli.\nZainstaluj za pomocą oficjalnego skryptu lub z AUR:\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "Nieznany błąd podczas pobierania stanu",
    "AdGuard {} ok":                        "AdGuard {}: OK",
    "AdGuard via systemctl {} ok":          "AdGuard przez systemctl {}: OK",
    "'{}' failed – insufficient privileges?":
        "Niepowodzenie: „{}” – brak uprawnień?",
    "Could not retrieve filter list":
        "Nie udało się pobrać listy filtrów",
    "Filter {} enabled":                    "Włączono filtr {}",
    "Could not enable filter {}":           "Nie udało się włączyć filtru {}",
    "Filter {} disabled":                   "Wyłączono filtr {}",
    "Could not disable filter {}":
        "Nie udało się wyłączyć filtru {}",
    "Filter installed":                     "Zainstalowano filtr",
    "Installation failed":                  "Instalacja nie powiodła się",
    "Filter {} removed":                    "Usunięto filtr {}",
    "Could not remove filter {}":
        "Nie udało się usunąć filtru {}",
    "Filters updated":                      "Zaktualizowano filtry",
    "Update failed":                        "Aktualizacja nie powiodła się",
    "Could not retrieve userscript list":
        "Nie udało się pobrać listy skryptów użytkownika",
    "Userscript '{}' enabled":              "Włączono skrypt użytkownika „{}”",
    "Could not enable userscript '{}'":
        "Nie udało się włączyć skryptu użytkownika „{}”",
    "Userscript '{}' disabled":             "Wyłączono skrypt użytkownika „{}”",
    "Could not disable userscript '{}'":
        "Nie udało się wyłączyć skryptu użytkownika „{}”",
    "Userscript '{}' removed":              "Usunięto skrypt użytkownika „{}”",
    "Could not remove userscript '{}'":
        "Nie udało się usunąć skryptu użytkownika „{}”",
    "Userscript installed":                 "Zainstalowano skrypt użytkownika",
    "Other":                                "Inne",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "Szukaj filtrów…",
    "Search userscripts…":              "Szukaj skryptów użytkownika…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "Nie udało się wczytać pliku proxy.yaml.\nŚcieżka: {}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "Aplikacje",
    "Mode:":                            "Tryb:",
    "Filtered ports:":                  "Filtrowane porty:",
    "SOCKS5 port:":                     "Port SOCKS5:",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "Port proxy SOCKS5 w trybie ręcznym.\nUstaw -1, aby wyłączyć.",
    "HTTP port:":                       "Port HTTP:",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "Port proxy HTTP w trybie ręcznym.\nUstaw -1, aby wyłączyć.",
    "Listen address:":                  "Adres nasłuchiwania:",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "Adres, na którym nasłuchuje proxy.\n127.0.0.1 = tylko lokalnie. 0.0.0.0 = wszystkie interfejsy (wymaga uwierzytelniania).",
    "Worker threads:":                  "Wątki robocze:",
    "Number of proxy worker threads.":  "Liczba wątków roboczych proxy.",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "Odszyfrowuje i filtruje ruch HTTPS.\nNiezbędne do blokowania reklam w witrynach https.\nWymaga zaufanego certyfikatu głównego zainstalowanego w systemie.",
    "Enable TLS 1.3":                   "Włącz TLS 1.3",
    "Enable TLS 1.3 support for filtered connections.":
        "Włącza obsługę TLS 1.3 dla filtrowanych połączeń.",
    "Filter HTTP/3 (QUIC) – experimental":
        "Filtruj HTTP/3 (QUIC) – eksperymentalne",
    "OCSP certificate checks":          "Sprawdzanie certyfikatów OCSP",
    "Enforce Certificate Transparency": "Wymuszaj Certificate Transparency",
    "Filter EV certificate sites":      "Filtruj witryny z certyfikatem EV",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "Domyślnie witryny z certyfikatami Extended Validation nie są filtrowane.\nWłącz tę opcję, aby filtrować także je (np. witryny banków).",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "Włącza ECH, aby zwiększyć prywatność.\nWymaga włączonego filtrowania DNS.",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "Filtruje zapytania DNS, aby blokować reklamy i moduły śledzące na poziomie DNS.\nUżywa lokalnego proxy DNS z konfigurowalnymi serwerami nadrzędnymi.",
    "Upstream:":                        "Serwer nadrzędny:",
    "Fallbacks:":                       "Zapasowe:",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "Zapasowe serwery DNS (używane, gdy główny serwer nadrzędny nie działa).\n'default' = systemowy DNS. Lista rozdzielana spacjami.\nPrzykład: default 1.1.1.1",
    "Bootstraps:":                      "Serwery bootstrap:",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "Bootstrap DNS do rozwiązywania nazw hostów serwerów nadrzędnych.\n'default' = adresy IP systemowego DNS. Dozwolone są tylko adresy IP.\nPrzykład: default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "Usuwa parametr ECH z rekordów DNS SVCB/HTTPS.\nWłącz tylko dla przeglądarek, które nie wykrywają automatycznie filtrowania HTTPS.",
    "Master switch for all tracking protection features below.":
        "Główny przełącznik wszystkich poniższych funkcji ochrony przed śledzeniem.",
    "Cookies":                          "Pliki cookie",
    "Block third-party cookies":        "Blokuj pliki cookie innych firm",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "Usuwa pliki cookie innych firm po określonym czasie.\nZapobiega śledzeniu między witrynami.",
    "Lifetime (minutes):":              "Czas życia (minuty):",
    "0 = block immediately. Default: 180 minutes.":
        "0 = blokuj natychmiast. Domyślnie: 180 minut.",
    "Block first-party cookies":        "Blokuj własne pliki cookie",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "Usuwa wszystkie pliki cookie (także własne) po określonym czasie.\nUwaga: powoduje wylogowanie ze wszystkich witryn.",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = blokuj natychmiast. Domyślnie: 4320 minut (3 dni).",
    "Privacy":                          "Prywatność",
    "Hide / reduce User-Agent":         "Ukrywaj / ograniczaj User-Agent",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "Usuwa z nagłówka User-Agent informacje identyfikujące.\nUtrudnia fingerprinting.",
    "Hide search queries in referrer":  "Ukrywaj zapytania wyszukiwania w nagłówku Referer",
    "Hides your search terms when clicking from a search engine to a website.":
        "Ukrywa wyszukiwane hasła po przejściu z wyszukiwarki do witryny.",
    "Remove referrer from third-party requests":
        "Usuwaj nagłówek Referer z żądań do innych firm",
    "Prevents third-party sites from knowing which page you came from.":
        "Ukrywa przed witrynami innych firm, z jakiej strony przychodzisz.",
    "Send Do-Not-Track signal":         "Wysyłaj sygnał Do-Not-Track",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "Wysyła nagłówek DNT wraz z żądaniami.\nUwaga: większość witryn go ignoruje, ale niektóre go respektują.",
    "Disable third-party ETag cache":   "Wyłącz pamięć podręczną ETag innych firm",
    "Prevents tracking via ETag caching in third-party content.":
        "Zapobiega śledzeniu przez buforowanie ETag w treściach innych firm.",
    "Block third-party Authorization header":
        "Blokuj nagłówek Authorization innych firm",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "Blokuje nagłówek Authorization w żądaniach do innych firm, aby zapobiec śledzeniu.",
    "Remove X-Client-Data header":      "Usuwaj nagłówek X-Client-Data",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "Usuwa nagłówek X-Client-Data wysyłany przez Chrome do usług Google.",
    "Block WebRTC":                     "Blokuj WebRTC",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "Zapobiega wyciekom adresu IP przez WebRTC.\nMoże zakłócić rozmowy wideo i niektóre aplikacje internetowe.",
    "Block Push API":                   "Blokuj Push API",
    "Blocks browser push notifications from websites.":
        "Blokuje powiadomienia push przeglądarki wysyłane przez witryny.",
    "Block Location API":               "Blokuj API lokalizacji",
    "Prevents websites from accessing your GPS location.":
        "Uniemożliwia witrynom dostęp do twojej lokalizacji GPS.",
    "Block Flash":                      "Blokuj Flash",
    "Blocks the Flash plugin.":
        "Blokuje wtyczkę Flash.",
    "Block Java":                       "Blokuj wtyczki Java",
    "Disables Java plugins. JavaScript remains enabled.":
        "Wyłącza wtyczki Java. JavaScript pozostaje włączony.",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "Włącz Anti-DPI",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "Modyfikuje dane wychodzących pakietów, aby obejść głęboką inspekcję pakietów (DPI).\nPrzydatne w krajach z cenzurą internetu.",
    "App pattern":
        "Wzorzec aplikacji",
    "Skip outbound proxy":              "Pomiń proxy wychodzące",
    "Don't route this app's traffic through outbound proxy":
        "Nie kieruj ruchu tej aplikacji przez proxy wychodzące",
    "Browser list included from {}":    "Lista przeglądarek dołączona z: {}",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "Nie można usunąć dołączonej listy przeglądarek ani reguły z symbolem wieloznacznym (*).",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "Ostrzega przed złośliwymi witrynami i phishingiem.\nKorzysta z bazy danych Safe Browsing firmy AdGuard.",
    "Send anonymous statistics":        "Wysyłaj anonimowe statystyki",
    "Send anonymous lookups to AdGuard.":
        "Wysyła anonimowe zapytania do AdGuard.",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "Sprawdzanie unieważnienia certyfikatów za pomocą CRLite firmy Mozilla.\nSzybsze i bardziej niezawodne niż tradycyjne sprawdzanie CRL/OCSP.",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "Stosuje reguły filtrów blokujących reklamy do żądań HTTP/HTTPS.",
    "Save failed":                      "Zapisywanie nie powiodło się",
    "Could not save proxy.yaml:\n{}":   "Nie udało się zapisać pliku proxy.yaml:\n{}",
    "Restarting AdGuard…":              "Ponowne uruchamianie AdGuard…",
    "AdGuard restarted.":               "Uruchomiono ponownie AdGuard.",
    "Restart failed: {}":               "Ponowne uruchomienie nie powiodło się: {}",
    "Unknown error":                    "Nieznany błąd",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "Dodaj",
    "Search exceptions…":               "Szukaj wyjątków…",
    "1 exception":                      "Wyjątki: 1",
    "{} exceptions":                    "Wyjątki: {}",
    "'{}' is not a valid domain or IP address.":
        "„{}” nie jest prawidłową domeną ani adresem IP.",
    "'{}' is already in the list.":     "„{}” jest już na liście.",
    "Could not save exceptions:\n{}":
        "Nie udało się zapisać wyjątków:\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "Przegląd",
    "Userscripts":                      "Skrypty użytkownika",
    "Exceptions":                       "Wyjątki",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "Zresetuj licencję",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "Generuje certyfikat główny CA na potrzeby filtrowania HTTPS. Certyfikat musi zostać zainstalowany w systemie i oznaczony jako zaufany.",
    "Checking for updates…":            "Sprawdzanie aktualizacji…",
    "Firefox profile:":                 "Profil przeglądarki Firefox:",
    "(optional) e.g. abcd1234.MyProfile":
        "(opcjonalnie) np. abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "Podaj ID lub nazwę filtru:",
    "Filter added.":                    "Dodano filtr.",
    "Rename…":                          "Zmień nazwę…",
    "Rename filter":                    "Zmień nazwę filtru",
    "New title:":                       "Nowy tytuł:",
    "Filter renamed.":                  "Zmieniono nazwę filtru.",
    "Filter trust updated.":            "Zaktualizowano zaufanie do filtru.",
    "Filter URL:":                      "Adres URL filtru:",
    "Title:":                           "Tytuł:",
    "(optional)":                       "(opcjonalnie)",
    "Trusted filter":                   "Zaufany filtr",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "Szukaj filtrów DNS…",
    "No DNS filters found.":            "Nie znaleziono filtrów DNS.",
    "DNS filter installed.":            "Zainstalowano filtr DNS.",
    "DNS filter added.":                "Dodano filtr DNS.",
    "Remove DNS filter":                "Usuń filtr DNS",
    "DNS filter {} removed.":           "Usunięto filtr DNS {}.",
    "Rename DNS filter":                "Zmień nazwę filtru DNS",
    "DNS filter renamed.":              "Zmieniono nazwę filtru DNS.",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "Eksportuj dzienniki…",
    "Export AdGuard CLI logs to a zip file":
        "Eksportuje dzienniki AdGuard CLI do pliku zip",
    "Export settings…":                 "Eksportuj ustawienia…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "Uruchamia test wydajności kryptografii i filtrowania HTTPS.",
    "Run benchmark":                    "Uruchom test wydajności",
    "Done.":                            "Gotowe.",
    "Export logs to…":                  "Eksportuj dzienniki do…",
    "Export settings to…":              "Eksportuj ustawienia do…",
    "Zip files (*.zip);;All files (*)":
        "Pliki zip (*.zip);;Wszystkie pliki (*)",
    "Log file not found.":              "Nie znaleziono pliku dziennika.",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "Nie udało się pobrać listy filtrów DNS",
    "DNS filter {} enabled":            "Włączono filtr DNS {}",
    "Could not enable DNS filter {}":   "Nie udało się włączyć filtru DNS {}",
    "DNS filter {} disabled":           "Wyłączono filtr DNS {}",
    "Could not disable DNS filter {}":  "Nie udało się wyłączyć filtru DNS {}",
    "DNS filter installed":             "Zainstalowano filtr DNS",
    "DNS filter {} removed":            "Usunięto filtr DNS {}",
    "Could not remove DNS filter {}":   "Nie udało się usunąć filtru DNS {}",
    "DNS filter added":                 "Dodano filtr DNS",
    "Could not add DNS filter":         "Nie udało się dodać filtru DNS",
    "DNS filter title updated":         "Zaktualizowano tytuł filtru DNS",
    "Could not set DNS filter title":   "Nie udało się ustawić tytułu filtru DNS",
    "Filter added":                     "Dodano filtr",
    "Could not add filter":             "Nie udało się dodać filtru",
    "Filter trust updated":             "Zaktualizowano zaufanie do filtru",
    "Could not update filter trust":    "Nie udało się zaktualizować zaufania do filtru",
    "Filter title updated":             "Zaktualizowano tytuł filtru",
    "Could not set filter title":       "Nie udało się ustawić tytułu filtru",
    "License reset":                    "Zresetowano licencję",
    "Could not reset license":          "Nie udało się zresetować licencji",
    "Could not retrieve license info":  "Nie udało się pobrać informacji o licencji",
    "Certificate generated":            "Wygenerowano certyfikat",
    "Certificate generation failed":    "Generowanie certyfikatu nie powiodło się",
    "Logs exported":                    "Wyeksportowano dzienniki",
    "Log export failed":                "Eksport dzienników nie powiódł się",
    "Settings exported":                "Wyeksportowano ustawienia",
    "Settings export failed":           "Eksport ustawień nie powiódł się",
    "Settings imported":                "Zaimportowano ustawienia",
    "Settings import failed":           "Import ustawień nie powiódł się",
    "Update check completed":           "Zakończono sprawdzanie aktualizacji",
    "Update check failed":              "Sprawdzanie aktualizacji nie powiodło się",
    "Benchmark failed":                 "Test wydajności nie powiódł się",
    "AdGuard stopped (forced)":         "Wymuszono zatrzymanie AdGuard",
    "Could not stop AdGuard – process may still be running":
        "Nie udało się zatrzymać AdGuard – proces może nadal działać",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "Nie znaleziono adguard-cli w tym systemie.\n\nZalecana metoda instalacji (oficjalna):\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\nAlternatywa (Arch Linux AUR):\n  paru -S adguard-cli-bin\n\nAdGuard Tray uruchomi się, ale włączanie i wyłączanie AdGuard nie zadziała do czasu zainstalowania adguard-cli.",
    "Copy install command":             "Kopiuj polecenie instalacji",
    "Continue":                         "Kontynuuj",
    "AdGuard Tray is already running":  "AdGuard Tray już działa",
    "Only one instance can run at a time. Check your system tray.":
        "Jednocześnie może działać tylko jedna instancja. Sprawdź tackę systemową.",
    "Authentication cancelled":         "Anulowano uwierzytelnianie",
    "Authorization failed":             "Autoryzacja nie powiodła się",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "Sprawdza, czy certyfikat witryny został unieważniony (OCSP).\nAdGuard sprawdza to asynchronicznie i przepuszcza połączenie,\njeśli sprawdzanie trwa długo, więc rzadko psuje to witryny – pozostaw\nwłączone, chyba że problem udało się zawęzić właśnie do tego.",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "Wymusza sprawdzanie Certificate Transparency (zasady CT przeglądarki Chrome).\nWitryny, których własny certyfikat nie jest zgodny z CT, przestają być filtrowane,\na przeglądarka może je odrzucić. Duże witryny są zgodne, więc zmieniaj to\ntylko w przypadku witryny, która zgłasza błąd certyfikatu.",
    "Sites that don't load":
        "Witryny, które się nie wczytują",
    "Turn off HTTP/3 filtering":
        "Wyłącz filtrowanie HTTP/3",
    "No filters installed":
        "Brak zainstalowanych filtrów",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "Reguła zapory blokuje HTTP/3; przeglądarki używają HTTP/2.",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "Aplikacje wyłączone z filtrowania (ich ruch HTTP/3 również nie jest filtrowany): {}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuard nie działa – nic nie jest filtrowane.",
    "could not remove the previous certificate":
        "nie udało się usunąć poprzedniego certyfikatu",
    "HTTP/3 state unknown":
        "Nieznany stan HTTP/3",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "Reguła zapory odrzuca wychodzący ruch UDP 443, więc nie można używać QUIC.",
    "Browser policy disables QUIC: {}":
        "Zasady przeglądarki wyłączają QUIC: {}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "Przeglądarki mogą omijać AdGuard przez HTTP/3 (UDP 443).",
    "Checking…":
        "Sprawdzanie…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "Nie udało się odczytać pliku proxy.yaml – stan HTTP/3 nieznany.",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "Profile z rodziny Firefox z wyłączonym HTTP/3: {} z {}",
    "HTTP/3 (QUIC)":
        "HTTP/3 (QUIC)",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "AdGuard blokuje HTTP/3; przeglądarki przełączają się na filtrowany HTTP/2.",
    "HTTP/3 is filtered by AdGuard.":
        "AdGuard filtruje HTTP/3.",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "Wyłączono HTTP/3 w profilach przeglądarki Firefox – uruchom ponownie przeglądarkę.",
    "HTTPS filtering is off – nothing is filtered.":
        "Filtrowanie HTTPS jest wyłączone – nic nie jest filtrowane.",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "Tryb proxy: {} – filtrowany jest tylko ruch przesyłany przez proxy, a przeglądarki nie wysyłają QUIC przez proxy.",
    "unknown":
        "nieznane",
    "AdGuard's certificate was not found. Generate it first.":
        "Nie znaleziono certyfikatu AdGuard. Najpierw go wygeneruj.",
    "Certificate could not be installed in any browser.":
        "Nie udało się zainstalować certyfikatu w żadnej przeglądarce.",
    "Certificate installed for {} of {} stores.":
        "Zainstalowano certyfikat w magazynach: {} z {}.",
    "Chromium-based browsers":
        "Przeglądarki oparte na Chromium",
    "No browser certificate stores found.":
        "Nie znaleziono magazynów certyfikatów przeglądarek.",
    "Restart your browsers for the certificate to take effect.":
        "Uruchom ponownie przeglądarki, aby certyfikat zaczął działać.",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "Uruchom bez sudo/pkexec – instalacja następuje w twoich profilach przeglądarek",
    "certificate not found after import":
        "nie znaleziono certyfikatu po imporcie",
    "certutil not found – install the 'nss' package":
        "nie znaleziono certutil – zainstaluj pakiet „nss”",
    "not found":
        "nie znaleziono",
    "Could not read the filter list (unexpected CLI output).":
        "Nie udało się odczytać listy filtrów (nieoczekiwane dane wyjściowe CLI).",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "Nie znaleziono tacki systemowej. AdGuard Tray działa bez ikony — włącz tackę systemową/AppIndicator w panelu.",
    "URL must start with http:// or https://":
        "Adres URL musi zaczynać się od http:// lub https://",
    "adguard-cli path does not exist or is not executable.":
        "Ścieżka do adguard-cli nie istnieje lub nie wskazuje pliku wykonywalnego.",
    "That binary does not identify as adguard-cli. Save anyway?":
        "Ten plik wykonywalny nie przedstawia się jako adguard-cli. Zapisać mimo to?",
    "Update channel":                   "Kanał aktualizacji",
    "Switching update channel to {}…":  "Przełączanie kanału aktualizacji: {}…",
    "Update channel set to {}":         "Ustawiono kanał aktualizacji: {}",
    "Could not set update channel":     "Nie udało się ustawić kanału aktualizacji",
    "Invalid channel: {}":              "Nieprawidłowy kanał: {}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        "Brak dziennika dostępu ({}). AdGuard zapisuje go, gdy tylko przefiltruje jakiś ruch; gdy działa jako usługa systemowa, dziennik należy do użytkownika root i nie można go tu odczytać.",
    'Cannot read the access log ({}): {}':
        "Nie można odczytać dziennika dostępu ({}): {}",
    'Blocked':
        "Zablokowane",
    'Blocked only':
        "Tylko zablokowane",
    "Refresh":
        "Odśwież",
    'Allow selected domain':
        "Zezwól na wybraną domenę",
    'Block selected domain':
        "Zablokuj wybraną domenę",
    'Activity':
        "Aktywność",
    'Time':
        "Czas",
    'Domain':
        "Domena",
    'Result':
        "Wynik",
    'Rule':
        "Reguła",
    'Size':
        "Rozmiar",
    'Count':
        "Liczba",
    'Could not read the access log.':
        "Nie udało się odczytać dziennika dostępu.",
    '{} lines not understood':
        "Nierozpoznane wiersze: {}",
    'Not a valid domain: {}':
        "Nieprawidłowa domena: {}",
    'Source: {}':
        "Źródło: {}",
    'Allowed':
        "Dozwolone",
    'Added rule: {}':
        "Dodano regułę: {}",
    'Requests per hour, {} to {} · busiest hour: {}':
        "Żądania na godzinę, od {} do {} · godzina szczytu: {}",
    'Last 24 hours':
        "Ostatnie 24 godziny",
    'Last 7 days':
        "Ostatnie 7 dni",
    'Requests':
        "Żądania",
    'Traffic':
        "Ruch",

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        "Dostępna jest wersja {} (zainstalowana: {}).",
    'Application update':
        "Aktualizacja aplikacji",
    'Check for update':
        "Sprawdź aktualizacje",
    'Install update':
        "Zainstaluj aktualizację",
    'Installing update…':
        "Instalowanie aktualizacji…",
    'Restart now':
        "Uruchom ponownie teraz",
    'Later':
        "Później",
    'You are running the latest version ({}).':
        "Zainstalowana jest najnowsza wersja ({}).",
    'Installation not recognised':
        "Nie rozpoznano sposobu instalacji",
    'Could not check for updates.':
        "Nie udało się sprawdzić aktualizacji.",
    'Update with: {}':
        "Polecenie aktualizacji: {}",
    'Installed with the AUR package {}':
        "Zainstalowano z pakietu AUR {}",
    'Installed in {}':
        "Zainstalowano w: {}",
    'Running from a source checkout':
        "Uruchomiono z kopii roboczej kodu źródłowego",
    'Version {} installed. Restart adguard-tray to use it.':
        "Zainstalowano wersję {}. Uruchom ponownie adguard-tray, aby jej używać.",
    'Unexpected answer from GitHub: {}':
        "Nieoczekiwana odpowiedź serwisu GitHub: {}",
    'Download failed: {}':
        "Pobieranie nie powiodło się: {}",
    'Could not unpack the download: {}':
        "Nie udało się rozpakować pobranego pliku: {}",
    'This installation is managed elsewhere: {}':
        "Ta instalacja jest zarządzana gdzie indziej: {}",
    'No permission to write to {}':
        "Brak uprawnień do zapisu w: {}",
    'GitHub returned {}.':
        "Odpowiedź serwisu GitHub: {}.",
    'No connection to GitHub: {}':
        "Brak połączenia z serwisem GitHub: {}",
    'The download does not contain adguard-tray.':
        "Pobrany plik nie zawiera adguard-tray.",
    'The download says version {} instead of {} – aborted.':
        "Pobrany plik ma wersję {} zamiast {} – przerwano.",
    'GitHub is rate limiting this address. Try again later.':
        "Serwis GitHub ogranicza liczbę żądań z tego adresu. Spróbuj ponownie później.",
    'The download is larger than expected – aborted.':
        "Pobrany plik jest większy, niż oczekiwano – przerwano.",
    'Update failed: {}':
        "Aktualizacja nie powiodła się: {}",
    'The archive contains unexpected paths – aborted.':
        "Archiwum zawiera nieoczekiwane ścieżki – przerwano.",
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        "Aktualizacja nie powiodła się, a poprzedniej wersji nie udało się przywrócić. Przywróć ją z katalogu {} lub zainstaluj ponownie poleceniem: {}",
    'Last 30 days':
        "Ostatnie 30 dni",
    'All time':
        "Cały okres",
    'Modified':
        "Zmodyfikowane",
    'Rules':
        "Reguły",
    'Showing {} – show all':
        "Wyświetlanie: {} – pokaż wszystko",
    'history {}':
        "historia: {}",
    'Filter list ID: {}':
        "ID listy filtrów: {}",
    'App':
        "Aplikacja",
    'Protocol':
        "Protokół",
    'Type':
        "Typ",
    'Reset history':
        "Wyczyść historię",
    'Delete the stored history and read the log again.':
        "Usuwa zapisaną historię i ponownie wczytuje dziennik.",
    'Delete the stored history? Only what the log still holds can be read back.':
        "Usunąć zapisaną historię? Odtworzyć można tylko to, co nadal znajduje się w dzienniku.",
    'History is not being updated: {}':
        "Historia nie jest aktualizowana: {}",

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "Niezapisane zmiany w ustawieniach AdGuard: 1",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "Zaufany filtr może uruchamiać skrypty na odwiedzanych stronach. Ufaj tylko listom ze znanych ci źródeł.",
    "About":
        "O programie",
    "Actions for the selected filter":
        "Działania dla wybranego filtru",
    "Ad blocking":
        "Blokowanie reklam",
    "Ad blocking is off, so the filter lists below have no effect.":
        "Blokowanie reklam jest wyłączone, więc poniższe listy filtrów nie działają.",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLI pobierze i zainstaluje najnowszą wersję.",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "AdGuard CLI usunie licencję z tego komputera. Konieczna będzie ponowna aktywacja.",
    "AdGuard CLI logs":
        "Dzienniki AdGuard CLI",
    "AdGuard CLI update finished.":
        "Zakończono aktualizację AdGuard CLI.",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "Dziennik AdGuard Tray",
    "AdGuard doesn't filter these websites.":
        "AdGuard nie filtruje tych witryn.",
    "AdGuard is filtering this computer's traffic.":
        "AdGuard filtruje ruch tego komputera.",
    "AdGuard restarts to load the new lists.":
        "AdGuard uruchomi się ponownie, aby wczytać nowe listy.",
    "AdGuard's reply did not say whether it is running.":
        "Z odpowiedzi AdGuard nie wynika, czy program działa.",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "Nie znaleziono pliku ustawień AdGuard ({}). Uruchom raz adguard-cli, aby go utworzyć.",
    "Add DNS filter by ID":
        "Dodaj filtr DNS według ID",
    "Add DNS filter from URL":
        "Dodaj filtr DNS z adresu URL",
    "Add filter":
        "Dodaj filtr",
    "Add filter by ID":
        "Dodaj filtr według ID",
    "Add filter from URL":
        "Dodaj filtr z adresu URL",
    "Add rule":
        "Dodaj regułę",
    "Add to browsers":
        "Dodaj do przeglądarek",
    "Add userscript":
        "Dodaj skrypt użytkownika",
    "Add userscript…":
        "Dodaj skrypt użytkownika…",
    "Add website":
        "Dodaj witrynę",
    "Add…":
        "Dodaj…",
    "Advanced":
        "Zaawansowane",
    "All available":
        "Wszystkie dostępne",
    "Allow {}":
        "Zezwól: {}",
    "Also adds the certificate to this Firefox profile.":
        "Dodaje certyfikat również do tego profilu przeglądarki Firefox.",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "Również przy ponownych uruchomieniach i błędach. Wymaga notify-send (libnotify) lub działającej usługi powiadomień, np. dunst, mako albo usługi KDE.",
    "Appearance":
        "Wygląd",
    "Applies after AdGuard Tray restarts.":
        "Zmiana zadziała po ponownym uruchomieniu AdGuard Tray.",
    "Apply":
        "Zastosuj",
    "Apply your changes to AdGuard's settings before closing?":
        "Zastosować zmiany w ustawieniach AdGuard przed zamknięciem?",
    "Applying them restarts AdGuard if protection is on.":
        "Zastosowanie zmian uruchomi ponownie AdGuard, jeśli ochrona jest włączona.",
    "Asks GitHub for the newest release.":
        "Pobiera z serwisu GitHub informacje o najnowszym wydaniu.",
    "At a glance":
        "W skrócie",
    "Automatic":
        "Automatycznie",
    "Automatic – filter all apps":
        "Automatyczny – filtruj wszystkie aplikacje",
    "Benchmark":
        "Test wydajności",
    "Beta":
        "Beta",
    "Block ECH in DNS records":
        "Blokuj ECH w rekordach DNS",
    "Block domains before a connection is made.":
        "Blokują domeny jeszcze przed nawiązaniem połączenia.",
    "Block {}":
        "Zablokuj: {}",
    "Blocked (24 h)":
        "Zablokowane (24 h)",
    "Browser list ({})":
        "Lista przeglądarek ({})",
    "By ID or name…":
        "Według ID lub nazwy…",
    "Certificate":
        "Certyfikat",
    "Certificate checks":
        "Sprawdzanie certyfikatów",
    "Changes are collected in the bar at the bottom and applied together.":
        "Zmiany są zbierane na pasku u dołu i stosowane razem.",
    "Check again":
        "Sprawdź ponownie",
    "Check every":
        "Sprawdzaj co",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "Przeglądarki z rodziny Chromium i Firefox mają własne magazyny certyfikatów.",
    "Close":
        "Zamknij",
    "Controls which AdGuard CLI build “{}” installs.":
        "Określa, którą wersję AdGuard CLI instaluje przycisk „{}”.",
    "Could not add the rule.":
        "Nie udało się dodać reguły.",
    "Could not open {}":
        "Nie udało się otworzyć: {}",
    "Could not read {}":
        "Nie udało się odczytać: {}",
    "Could not refresh. Showing data from {}.":
        "Nie udało się odświeżyć. Wyświetlane są dane z godziny {}.",
    "Could not reset the history.":
        "Nie udało się wyczyścić historii.",
    "Could not restart AdGuard.":
        "Nie udało się ponownie uruchomić AdGuard.",
    "Could not start protection.":
        "Nie udało się włączyć ochrony.",
    "Could not stop protection.":
        "Nie udało się wyłączyć ochrony.",
    "Create":
        "Utwórz",
    "Create certificate":
        "Utwórz certyfikat",
    "Custom":
        "Własne",
    "DNS filter lists":
        "Listy filtrów DNS",
    "DNS filtering":
        "Filtrowanie DNS",
    "DNS filtering is off, so these lists have no effect.":
        "Filtrowanie DNS jest wyłączone, więc te listy nie działają.",
    "DNS servers":
        "Serwery DNS",
    "Dark":
        "Ciemny",
    "Default":
        "Domyślny",
    "Details":
        "Szczegóły",
    "Discard":
        "Odrzuć",
    "Don't filter":
        "Nie filtruj",
    "Don't trust":
        "Nie ufaj",
    "Downloads and installs the newest AdGuard CLI build.":
        "Pobiera i instaluje najnowszą wersję AdGuard CLI.",
    "Duration":
        "Czas trwania",
    "Export…":
        "Eksportuj…",
    "Filter everything":
        "Filtruj wszystko",
    "Filter in place":
        "Filtruj bezpośrednio",
    "Filtering":
        "Filtrowanie",
    "Follow system":
        "Zgodnie z systemem",
    "From URL…":
        "Z adresu URL…",
    "Go to updates":
        "Przejdź do aktualizacji",
    "HTTP proxy: {}":
        "Proxy HTTP: {}",
    "HTTPS filtering":
        "Filtrowanie HTTPS",
    "How much detail AdGuard Tray writes to its own log.":
        "Określa, jak szczegółowe wpisy AdGuard Tray zapisuje we własnym dzienniku.",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "Jeśli witryna się nie wczytuje, najpierw wyłącz filtrowanie HTTP/3. Pozostałe kontrole chronią każdą witrynę – wyłącz je tylko wtedy, gdy to nie pomogło.",
    "Included":
        "Dołączona",
    "Installed":
        "Zainstalowane",
    "License":
        "Licencja",
    "Light":
        "Jasny",
    "Logs":
        "Dzienniki",
    "MIT license":
        "Licencja MIT",
    "Maintenance":
        "Konserwacja",
    "Manual proxy":
        "Ręczne proxy",
    "Manual – only apps set to use the proxy":
        "Ręczny – tylko aplikacje używające proxy",
    "More":
        "Więcej",
    "Move down":
        "Przenieś niżej",
    "Move up":
        "Przenieś wyżej",
    "Network":
        "Sieć",
    "Nightly":
        "Nightly",
    "No requests yet – AdGuard logs requests while protection is on.":
        "Brak jeszcze żądań – AdGuard rejestruje żądania, gdy ochrona jest włączona.",
    "Not added":
        "Nie dodano",
    "Nothing matches your search.":
        "Brak wyników wyszukiwania.",
    "Notify me when protection turns on or off":
        "Powiadamiaj o włączeniu lub wyłączeniu ochrony",
    "Off":
        "Wyłączone",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "Dotyczy tylko przeglądarek, które używają DoH lub DoT. Ustawienie „Wyłączone” pozwala im omijać filtrowanie DNS AdGuard.",
    "Open AdGuard Tray":
        "Otwórz AdGuard Tray",
    "Open exceptions":
        "Otwórz wyjątki",
    "Open folder":
        "Otwórz katalog",
    "Open release page":
        "Otwórz stronę wydania",
    "Pages":
        "Strony",
    "Performance":
        "Wydajność",
    "Protection":
        "Ochrona",
    "Protection started.":
        "Ochrona została włączona.",
    "Protection stopped.":
        "Ochrona została wyłączona.",
    "Proxy mode":
        "Tryb proxy",
    "Redirect to AdGuard's DNS":
        "Przekieruj do DNS AdGuard",
    "Refresh this page (F5)":
        "Odśwież tę stronę (F5)",
    "Release (stable)":
        "Wydanie (stabilne)",
    "Remove rule":
        "Usuń regułę",
    "Remove “{}”?":
        "Usunąć „{}”?",
    "Remove…":
        "Usuń…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "Zastąpić bieżące ustawienia AdGuard ustawieniami z pliku {}?\n\nAdGuard uruchomi się ponownie, aby je zastosować.",
    "Reset history…":
        "Wyczyść historię…",
    "Reset…":
        "Zresetuj…",
    "Restart AdGuard":
        "Uruchom ponownie AdGuard",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "Reguły działają tylko w automatycznym trybie proxy. Obowiązuje pierwsza pasująca reguła, więc regułę \"*\" umieść na końcu.",
    "Safe Browsing":
        "Bezpieczna sieć",
    "Save anyway":
        "Zapisz mimo to",
    "Saved. AdGuard restarts to apply the change.":
        "Zapisano. AdGuard uruchomi się ponownie, aby zastosować zmianę.",
    "Saved. Applies after AdGuard Tray restarts.":
        "Zapisano. Zmiana zadziała po ponownym uruchomieniu AdGuard Tray.",
    "Saved. The change applies when protection is turned on.":
        "Zapisano. Zmiana zadziała po włączeniu ochrony.",
    "Secure DNS and ECH":
        "Bezpieczny DNS i ECH",
    "Secure DNS filtering":
        "Filtrowanie bezpiecznego DNS",
    "Set the path in Settings":
        "Ustaw ścieżkę w Ustawieniach",
    "Settings":
        "Ustawienia",
    "Show":
        "Pokaż:",
    "Show recent entries":
        "Pokaż ostatnie wpisy",
    "Skip HTTPS filtering":
        "Pomiń filtrowanie HTTPS",
    "Some counts could not be loaded.":
        "Nie udało się wczytać niektórych wartości.",
    "Source code":
        "Kod źródłowy",
    "Start AdGuard Tray when I log in":
        "Uruchamiaj AdGuard Tray po zalogowaniu",
    "Startup":
        "Uruchamianie",
    "Status checks":
        "Sprawdzanie stanu",
    "Stealth mode":
        "Tryb ukrycia",
    "System":
        "System",
    "The new lists load when protection is turned on.":
        "Nowe listy zostaną wczytane po włączeniu ochrony.",
    "Theme":
        "Motyw",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "Wyłącza to filtrowanie HTTP/3, sprawdzanie OCSP, Certificate Transparency i filtrowanie bezpiecznego DNS. Unieważnione lub nieprawidłowo wystawione certyfikaty nie zostaną wtedy wykryte, a przeglądarki mogą rozwiązywać nazwy z pominięciem filtru DNS AdGuard.",
    "Time range":
        "Zakres czasu",
    "To keep it but stop using it, switch it off instead.":
        "Aby go zachować, ale nie używać, wyłącz go, zamiast usuwać.",
    "Top lists":
        "Najczęstsze",
    "Trust":
        "Zaufaj",
    "Trust “{}”?":
        "Zaufać „{}”?",
    "Trust…":
        "Zaufaj…",
    "Turn off all strict checks…":
        "Wyłącz wszystkie rygorystyczne kontrole…",
    "Undo":
        "Cofnij",
    "Unknown":
        "Nieznane",
    "Unsaved changes":
        "Niezapisane zmiany",
    "Update AdGuard CLI…":
        "Aktualizuj AdGuard CLI…",
    "Update channel: {}":
        "Kanał aktualizacji: {}",
    "Updated {}":
        "Zaktualizowano: {}",
    "Updates":
        "Aktualizacje",
    "Used in manual mode only.":
        "Używane tylko w trybie ręcznym.",
    "Userscripts update together with filters.":
        "Skrypty użytkownika są aktualizowane razem z filtrami.",
    "Uses XDG autostart (~/.config/autostart).":
        "Używa mechanizmu autostartu XDG (~/.config/autostart).",
    "Waiting for authorization…":
        "Oczekiwanie na autoryzację…",
    "Website exceptions":
        "Wyjątki witryn",
    "Websites":
        "Witryny",
    "example.com or a link":
        "example.com lub odnośnik",
    "expires {}":
        "wygasa: {}",
    "of {} requests in the last 24 hours":
        "z {} (żądania z ostatnich 24 godzin)",
    "{} of {} DNS filters on":
        "Włączone filtry DNS: {} z {}",
    "{} of {} filters on":
        "Włączone filtry: {} z {}",
    "{} of {} on":
        "Włączone: {} z {}",
    "{} unsaved changes to AdGuard's settings":
        "Niezapisane zmiany w ustawieniach AdGuard: {}",
    "“Follow system” uses your desktop's light or dark setting.":
        "Opcja „Zgodnie z systemem” stosuje jasny lub ciemny motyw ustawiony w środowisku pulpitu.",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "Aktywna",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "Certyfikat AdGuard zostanie dodany do każdego profilu przeglądarki znalezionego w tym systemie.\n\nDzięki temu AdGuard może analizować ruch HTTPS w tych przeglądarkach. Najpierw zamknij przeglądarki – odczytują one magazyn certyfikatów podczas uruchamiania.",
    "Allow":
        "Zezwól",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "Najpierw zastosuj lub odrzuć zmiany w ustawieniach AdGuard, a potem uruchom ponownie.",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "Automatyczny: AdGuard przekierowuje do siebie ruch wszystkich aplikacji za pomocą iptables. Ręczny: AdGuard nasłuchuje tylko na poniższych portach SOCKS5 i HTTP.",
    "Block":
        "Zablokuj",
    "Browser API blocking":
        "Blokowanie API przeglądarki",
    "CRLite":
        "CRLite",
    "Cancel":
        "Anuluj",
    "Computers":
        "Komputery",
    "Could not change the autostart entry.":
        "Nie udało się zmienić wpisu autostartu.",
    "Could not export the logs.":
        "Nie udało się wyeksportować dzienników.",
    "Could not export the settings.":
        "Nie udało się wyeksportować ustawień.",
    "Could not reset the license.":
        "Nie udało się zresetować licencji.",
    "Could not retrieve license info.":
        "Nie udało się pobrać informacji o licencji.",
    "Could not run the benchmark.":
        "Nie udało się uruchomić testu wydajności.",
    "Could not save the settings.":
        "Nie udało się zapisać ustawień.",
    "Could not set the update channel.":
        "Nie udało się ustawić kanału aktualizacji.",
    "Could not update AdGuard CLI.":
        "Nie udało się zaktualizować AdGuard CLI.",
    "Could not update the filters.":
        "Nie udało się zaktualizować filtrów.",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "Nadrzędny serwer DNS.\n'default' = systemowy DNS.\nPrzykłady: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com",
    "Expiration date":
        "Data wygaśnięcia",
    "Expires":
        "Wygasa",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "Ponownie włączono HTTP/3 w profilach przeglądarki Firefox – uruchom ponownie przeglądarkę.",
    "License key":
        "Klucz licencyjny",
    "License type":
        "Typ licencji",
    "Manual":
        "Ręczny",
    "No exceptions.":
        "Brak wyjątków.",
    "OK":
        "OK",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "Włączone: AdGuard sam filtruje HTTP/3 (QUIC) – to funkcja eksperymentalna, a niektóre\nprzeglądarki i tak odrzucają HTTP/3 z certyfikatem zainstalowanym przez użytkownika.\nWyłączone: AdGuard zamiast tego blokuje QUIC, więc przeglądarki wracają do HTTP/2,\nktóry jest niezawodnie filtrowany.\nW obu przypadkach dotyczy to tylko trybu automatycznego – w trybie ręcznym\nruch HTTP/3 w ogóle nie trafia do AdGuard.",
    "Owner":
        "Właściciel",
    "Personal":
        "Osobista",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "Tryb proxy: {} – port UDP 443 jest przekierowywany do AdGuard.",
    "Save adguard-cli path":
        "Zapisz ścieżkę do adguard-cli",
    "Search domains or rules…":
        "Szukaj domen lub reguł…",
    "Settings file":
        "Plik ustawień",
    "Status":
        "Stan",
    "Trial":
        "Okres próbny",
    "Turn HTTP/3 back on in Firefox profiles":
        "Włącz ponownie HTTP/3 w profilach przeglądarki Firefox",
    "Turn off":
        "Wyłącz",
    "Turn off HTTP/3 in Firefox profiles":
        "Wyłącz HTTP/3 w profilach przeglądarki Firefox",
    "Turn off HTTP/3 in Firefox profiles…":
        "Wyłącz HTTP/3 w profilach przeglądarki Firefox…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "Wyłączyć HTTP/3 w profilach z rodziny Firefox (liczba profili: {})?\n\nIch ruch będzie wtedy korzystał z HTTP/2, który AdGuard potrafi filtrować. Następnie uruchom ponownie przeglądarkę.",
    "Turn off all strict checks":
        "Wyłącz wszystkie rygorystyczne kontrole",
    "Unavailable until AdGuard CLI reports its current channel.":
        "Niedostępne, dopóki AdGuard CLI nie poda bieżącego kanału.",
    "Update AdGuard CLI":
        "Aktualizuj AdGuard CLI",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "Używane tylko w trybie automatycznym. Zakresy (80:5221,5300:49151) lub pojedyncze porty (80,443,8080).",
    "{} of {}":
        "{} z {}",
    "{} of {} userscripts on":
        "Włączone skrypty użytkownika: {} z {}",
    "{}% blocked":
        "{}% zablokowanych",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "Elementy irytujące",
    "General":
        "Ogólne",
    "Language-specific":
        "Językowe",
    "Security":
        "Bezpieczeństwo",
    "Social widgets":
        "Widżety społecznościowe",
    "Expired":
        "Wygasła",
    "Autostart on login":
        "Autostart po zalogowaniu",
    "Add app rule":
        "Dodaj regułę aplikacji",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "Można używać symboli wieloznacznych, np. *steam* lub *EasyAntiCheat*.",
    "There is already a rule for '{}'.":
        "Reguła dla „{}” już istnieje.",
    "AdGuard settings":
        "Ustawienia AdGuard",
    "Ads and trackers are not blocked until you enable protection.":
        "Reklamy i moduły śledzące będą blokowane dopiero po włączeniu ochrony.",
    "Could not import the settings.":
        "Nie udało się zaimportować ustawień.",
    "Disable protection":
        "Wyłącz ochronę",
    "Enable protection":
        "Włącz ochronę",
    "Export and import":
        "Eksport i import",
    "Features":
        "Funkcje",
    "Import settings":
        "Importuj ustawienia",
    "Import settings from…":
        "Importuj ustawienia z…",
    "Import settings…":
        "Importuj ustawienia…",
    "Import…":
        "Importuj…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "Zapisuje filtry, reguły i konfigurację w pliku zip lub wczytuje je z takiego pliku.",
    "Update":
        "Aktualizuj",
    "Version":
        "Wersja",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "Plik {} nie zawiera eksportu ustawień. Wybierz plik zapisany przyciskiem „Eksportuj” w sekcji „Ustawienia AdGuard”.",
}
