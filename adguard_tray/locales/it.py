"""Italian."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "Lingua",
    "English":                           "Inglese",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "Attiva – Protezione in esecuzione",
    "Inactive – Protection stopped":        "Inattiva – Protezione arrestata",
    "Error retrieving status":              "Errore durante il recupero dello stato",
    "adguard-cli not found":                "adguard-cli non trovato",
    "Unknown status":                       "Stato sconosciuto",
    "Checking status…":                     "Verifica dello stato…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "Riavvia",
    "Filters":                              "Filtri",
    "Loading…":                             "Caricamento…",
    "Manage filters…":                      "Gestisci filtri…",
    "No userscripts installed":             "Nessuno userscript installato",
    "Manage userscripts…":                  "Gestisci userscript…",
    "Quit":                                 "Esci",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "attivo",
    "inactive":                             "inattivo",
    "System-wide filtering: {}":            "Filtraggio di sistema: {}",
    "Error: {}":                            "Errore: {}",
    "AdGuard Tray – Error":                 "AdGuard Tray – Errore",
    "AdGuard is now active – protection running.":
        "AdGuard è ora attivo – protezione in esecuzione.",
    "AdGuard has been stopped.":
        "AdGuard è stato arrestato.",
    "Could not retrieve status.":
        "Impossibile recuperare lo stato.",
    "Command failed":                       "Comando non riuscito",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " secondi",
    "How often adguard-cli status is checked automatically.":
        "Ogni quanto controllare automaticamente lo stato di adguard-cli.",
    "Log level:":                           "Livello di log:",
    "adguard-cli path:":                    "Percorso di adguard-cli:",
    "auto-detect via PATH":                 "rilevamento automatico tramite PATH",
    "Browse…":                              "Sfoglia…",
    "Select adguard-cli binary":            "Seleziona l'eseguibile di adguard-cli",
    "Notifications":                        "Notifiche",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "Aggiorna filtri",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "Aggiorna tutti i filtri, i filtri DNS, gli userscript,\nSafebrowsingV2, CRLite e controlla gli aggiornamenti dell'app.",
    "No filters found.":                    "Nessun filtro trovato.",
    "Updating filters… (can take up to 2 minutes)":
        "Aggiornamento dei filtri… (può richiedere fino a 2 minuti)",
    "Update completed.":                    "Aggiornamento completato.",
    "Update failed.":                       "Aggiornamento non riuscito.",
    "Installing: {}":                       "Installazione: {}",
    "Filter installed.":                    "Filtro installato.",
    "Remove":                               "Rimuovi",
    "Remove filter":                        "Rimuovi filtro",
    "Filter {} removed.":                   "Filtro {} rimosso.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        "Installa uno userscript da un URL .js diretto",
    "No userscripts installed.":            "Nessuno userscript installato.",
    "Userscript URL (direct .js URL):":     "URL dello userscript (URL .js diretto):",
    "Userscript installed.":                "Userscript installato.",
    'Remove "{}"':                          "Rimuovi “{}”",
    "Remove userscript":                    "Rimuovi userscript",
    "'{}' removed.":                        "“{}” rimosso.",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "adguard-cli non è stato trovato.\nInstallalo con lo script ufficiale o da AUR:\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "Errore sconosciuto durante il recupero dello stato",
    "AdGuard {} ok":                        "AdGuard {}: ok",
    "AdGuard via systemctl {} ok":          "AdGuard tramite systemctl {}: ok",
    "'{}' failed – insufficient privileges?":
        "Comando “{}” non riuscito – privilegi insufficienti?",
    "Could not retrieve filter list":
        "Impossibile recuperare l'elenco dei filtri",
    "Filter {} enabled":                    "Filtro {} attivato",
    "Could not enable filter {}":           "Impossibile attivare il filtro {}",
    "Filter {} disabled":                   "Filtro {} disattivato",
    "Could not disable filter {}":
        "Impossibile disattivare il filtro {}",
    "Filter installed":                     "Filtro installato",
    "Installation failed":                  "Installazione non riuscita",
    "Filter {} removed":                    "Filtro {} rimosso",
    "Could not remove filter {}":
        "Impossibile rimuovere il filtro {}",
    "Filters updated":                      "Filtri aggiornati",
    "Update failed":                        "Aggiornamento non riuscito",
    "Could not retrieve userscript list":
        "Impossibile recuperare l'elenco degli userscript",
    "Userscript '{}' enabled":              "Userscript “{}” attivato",
    "Could not enable userscript '{}'":
        "Impossibile attivare lo userscript “{}”",
    "Userscript '{}' disabled":             "Userscript “{}” disattivato",
    "Could not disable userscript '{}'":
        "Impossibile disattivare lo userscript “{}”",
    "Userscript '{}' removed":              "Userscript “{}” rimosso",
    "Could not remove userscript '{}'":
        "Impossibile rimuovere lo userscript “{}”",
    "Userscript installed":                 "Userscript installato",
    "Other":                                "Altro",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "Cerca filtri…",
    "Search userscripts…":              "Cerca userscript…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "Impossibile caricare proxy.yaml.\nPercorso: {}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "App",
    "Mode:":                            "Modalità:",
    "Filtered ports:":                  "Porte filtrate:",
    "SOCKS5 port:":                     "Porta SOCKS5:",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "Porta del proxy SOCKS5 per la modalità manuale.\nImposta -1 per disattivarla.",
    "HTTP port:":                       "Porta HTTP:",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "Porta del proxy HTTP per la modalità manuale.\nImposta -1 per disattivarla.",
    "Listen address:":                  "Indirizzo di ascolto:",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "Indirizzo su cui il proxy è in ascolto.\n127.0.0.1 = solo locale. 0.0.0.0 = tutte le interfacce (richiede autenticazione).",
    "Worker threads:":                  "Thread di lavoro:",
    "Number of proxy worker threads.":  "Numero di thread di lavoro del proxy.",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "Decifra e filtra il traffico HTTPS.\nNecessario per bloccare gli annunci sui siti https.\nRichiede un certificato root attendibile installato nel sistema.",
    "Enable TLS 1.3":                   "Attiva TLS 1.3",
    "Enable TLS 1.3 support for filtered connections.":
        "Attiva il supporto a TLS 1.3 per le connessioni filtrate.",
    "Filter HTTP/3 (QUIC) – experimental":
        "Filtra HTTP/3 (QUIC) – sperimentale",
    "OCSP certificate checks":          "Controlli OCSP dei certificati",
    "Enforce Certificate Transparency": "Imponi Certificate Transparency",
    "Filter EV certificate sites":      "Filtra siti con certificato EV",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "Per impostazione predefinita, i siti con certificati a convalida estesa non vengono filtrati.\nAttiva questa opzione per filtrare anche quelli (es. siti bancari).",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "Attiva ECH per una maggiore privacy.\nRichiede che il filtraggio DNS sia attivo.",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "Filtra le query DNS per bloccare annunci e tracciatori a livello DNS.\nUsa un proxy DNS locale con server upstream configurabili.",
    "Upstream:":                        "Upstream:",
    "Fallbacks:":                       "Fallback:",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "Server DNS di riserva (usati quando l'upstream principale non risponde).\n'default' = DNS di sistema. Elenco separato da spazi.\nEsempio: default 1.1.1.1",
    "Bootstraps:":                      "Bootstrap:",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "DNS di bootstrap per risolvere i nomi host degli upstream.\n'default' = IP dei DNS di sistema. Sono ammessi solo indirizzi IP.\nEsempio: default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "Rimuove il parametro ECH dai record DNS SVCB/HTTPS.\nAttivalo solo per i browser che non rilevano automaticamente il filtraggio HTTPS.",
    "Master switch for all tracking protection features below.":
        "Interruttore generale per tutte le funzioni di protezione dal tracciamento qui sotto.",
    "Cookies":                          "Cookie",
    "Block third-party cookies":        "Blocca cookie di terze parti",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "Elimina i cookie di terze parti dopo un tempo prestabilito.\nImpedisce il tracciamento tra siti.",
    "Lifetime (minutes):":              "Durata (minuti):",
    "0 = block immediately. Default: 180 minutes.":
        "0 = blocca subito. Predefinito: 180 minuti.",
    "Block first-party cookies":        "Blocca cookie proprietari",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "Elimina tutti i cookie (inclusi quelli proprietari) dopo un tempo prestabilito.\nAttenzione: questo ti disconnette da tutti i siti.",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = blocca subito. Predefinito: 4320 minuti (3 giorni).",
    "Privacy":                          "Privacy",
    "Hide / reduce User-Agent":         "Nascondi / riduci User-Agent",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "Rimuove dallo User-Agent le parti identificative.\nRiduce il fingerprinting.",
    "Hide search queries in referrer":  "Nascondi le query di ricerca nel referrer",
    "Hides your search terms when clicking from a search engine to a website.":
        "Nasconde i termini di ricerca quando passi da un motore di ricerca a un sito web.",
    "Remove referrer from third-party requests":
        "Rimuovi il referrer dalle richieste di terze parti",
    "Prevents third-party sites from knowing which page you came from.":
        "Impedisce ai siti di terze parti di sapere da quale pagina provieni.",
    "Send Do-Not-Track signal":         "Invia segnale Do-Not-Track",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "Invia l'intestazione DNT con le richieste.\nNota: la maggior parte dei siti la ignora, ma alcuni la rispettano.",
    "Disable third-party ETag cache":   "Disattiva cache ETag di terze parti",
    "Prevents tracking via ETag caching in third-party content.":
        "Impedisce il tracciamento tramite la cache ETag nei contenuti di terze parti.",
    "Block third-party Authorization header":
        "Blocca intestazione Authorization di terze parti",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "Blocca l'intestazione Authorization nelle richieste di terze parti per impedire il tracciamento.",
    "Remove X-Client-Data header":      "Rimuovi intestazione X-Client-Data",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "Rimuove l'intestazione X-Client-Data inviata da Chrome ai servizi Google.",
    "Block WebRTC":                     "Blocca WebRTC",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "Impedisce la fuga dell'indirizzo IP tramite WebRTC.\nPuò interferire con le videochiamate e alcune app web.",
    "Block Push API":                   "Blocca API Push",
    "Blocks browser push notifications from websites.":
        "Blocca le notifiche push del browser provenienti dai siti web.",
    "Block Location API":               "Blocca API di posizione",
    "Prevents websites from accessing your GPS location.":
        "Impedisce ai siti web di accedere alla tua posizione GPS.",
    "Block Flash":                      "Blocca Flash",
    "Blocks the Flash plugin.":
        "Blocca il plugin Flash.",
    "Block Java":                       "Blocca Java",
    "Disables Java plugins. JavaScript remains enabled.":
        "Disattiva i plugin Java. JavaScript resta attivo.",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "Attiva Anti-DPI",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "Modifica i dati dei pacchetti in uscita per aggirare la Deep Packet Inspection.\nUtile nei paesi con censura di internet.",
    "App pattern":
        "Modello app",
    "Skip outbound proxy":              "Salta proxy in uscita",
    "Don't route this app's traffic through outbound proxy":
        "Non instradare il traffico di questa app attraverso il proxy in uscita",
    "Browser list included from {}":    "Elenco browser incluso da: {}",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "L'elenco di inclusione dei browser e la regola con carattere jolly (*) non possono essere rimossi.",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "Avvisa in caso di siti web dannosi e di phishing.\nUsa il database di Sicurezza di navigazione di AdGuard.",
    "Send anonymous statistics":        "Invia statistiche anonime",
    "Send anonymous lookups to AdGuard.":
        "Invia ad AdGuard le verifiche in forma anonima.",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "Verifica della revoca dei certificati tramite CRLite di Mozilla.\nPiù veloce e affidabile dei tradizionali controlli CRL/OCSP.",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "Applica le regole di blocco degli annunci alle richieste HTTP/HTTPS.",
    "Save failed":                      "Salvataggio non riuscito",
    "Could not save proxy.yaml:\n{}":   "Impossibile salvare proxy.yaml:\n{}",
    "Restarting AdGuard…":              "Riavvio di AdGuard…",
    "AdGuard restarted.":               "AdGuard riavviato.",
    "Restart failed: {}":               "Riavvio non riuscito: {}",
    "Unknown error":                    "Errore sconosciuto",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "Aggiungi",
    "Search exceptions…":               "Cerca eccezioni…",
    "1 exception":                      "1 eccezione",
    "{} exceptions":                    "{} eccezioni",
    "'{}' is not a valid domain or IP address.":
        "“{}” non è un dominio o un indirizzo IP valido.",
    "'{}' is already in the list.":     "“{}” è già nell'elenco.",
    "Could not save exceptions:\n{}":
        "Impossibile salvare le eccezioni:\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "Panoramica",
    "Userscripts":                      "Userscript",
    "Exceptions":                       "Eccezioni",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "Reimposta licenza",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "Genera un certificato CA root per il filtraggio HTTPS. Il certificato deve essere installato e considerato attendibile nel sistema.",
    "Checking for updates…":            "Ricerca aggiornamenti…",
    "Firefox profile:":                 "Profilo Firefox:",
    "(optional) e.g. abcd1234.MyProfile":
        "(facoltativo) es. abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "Inserisci l'ID o il nome del filtro:",
    "Filter added.":                    "Filtro aggiunto.",
    "Rename…":                          "Rinomina…",
    "Rename filter":                    "Rinomina filtro",
    "New title:":                       "Nuovo titolo:",
    "Filter renamed.":                  "Filtro rinominato.",
    "Filter trust updated.":            "Attendibilità del filtro aggiornata.",
    "Filter URL:":                      "URL del filtro:",
    "Title:":                           "Titolo:",
    "(optional)":                       "(facoltativo)",
    "Trusted filter":                   "Filtro attendibile",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "Cerca filtri DNS…",
    "No DNS filters found.":            "Nessun filtro DNS trovato.",
    "DNS filter installed.":            "Filtro DNS installato.",
    "DNS filter added.":                "Filtro DNS aggiunto.",
    "Remove DNS filter":                "Rimuovi filtro DNS",
    "DNS filter {} removed.":           "Filtro DNS {} rimosso.",
    "Rename DNS filter":                "Rinomina filtro DNS",
    "DNS filter renamed.":              "Filtro DNS rinominato.",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "Esporta log…",
    "Export AdGuard CLI logs to a zip file":
        "Esporta i log di AdGuard CLI in un file zip",
    "Export settings…":                 "Esporta impostazioni…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "Esegui un benchmark crittografico e del filtraggio HTTPS.",
    "Run benchmark":                    "Esegui benchmark",
    "Done.":                            "Fatto.",
    "Export logs to…":                  "Esporta log in…",
    "Export settings to…":              "Esporta impostazioni in…",
    "Zip files (*.zip);;All files (*)":
        "File zip (*.zip);;Tutti i file (*)",
    "Log file not found.":              "File di log non trovato.",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "Impossibile recuperare l'elenco dei filtri DNS",
    "DNS filter {} enabled":            "Filtro DNS {} attivato",
    "Could not enable DNS filter {}":   "Impossibile attivare il filtro DNS {}",
    "DNS filter {} disabled":           "Filtro DNS {} disattivato",
    "Could not disable DNS filter {}":  "Impossibile disattivare il filtro DNS {}",
    "DNS filter installed":             "Filtro DNS installato",
    "DNS filter {} removed":            "Filtro DNS {} rimosso",
    "Could not remove DNS filter {}":   "Impossibile rimuovere il filtro DNS {}",
    "DNS filter added":                 "Filtro DNS aggiunto",
    "Could not add DNS filter":         "Impossibile aggiungere il filtro DNS",
    "DNS filter title updated":         "Titolo del filtro DNS aggiornato",
    "Could not set DNS filter title":   "Impossibile impostare il titolo del filtro DNS",
    "Filter added":                     "Filtro aggiunto",
    "Could not add filter":             "Impossibile aggiungere il filtro",
    "Filter trust updated":             "Attendibilità del filtro aggiornata",
    "Could not update filter trust":    "Impossibile aggiornare l'attendibilità del filtro",
    "Filter title updated":             "Titolo del filtro aggiornato",
    "Could not set filter title":       "Impossibile impostare il titolo del filtro",
    "License reset":                    "Licenza reimpostata",
    "Could not reset license":          "Impossibile reimpostare la licenza",
    "Could not retrieve license info":  "Impossibile recuperare le informazioni sulla licenza",
    "Certificate generated":            "Certificato generato",
    "Certificate generation failed":    "Generazione del certificato non riuscita",
    "Logs exported":                    "Log esportati",
    "Log export failed":                "Esportazione dei log non riuscita",
    "Settings exported":                "Impostazioni esportate",
    "Settings export failed":           "Esportazione delle impostazioni non riuscita",
    "Settings imported":                "Impostazioni importate",
    "Settings import failed":           "Importazione delle impostazioni non riuscita",
    "Update check completed":           "Controllo aggiornamenti completato",
    "Update check failed":              "Controllo aggiornamenti non riuscito",
    "Benchmark failed":                 "Benchmark non riuscito",
    "AdGuard stopped (forced)":         "AdGuard arrestato forzatamente",
    "Could not stop AdGuard – process may still be running":
        "Impossibile arrestare AdGuard – il processo potrebbe essere ancora in esecuzione",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "Impossibile trovare adguard-cli su questo sistema.\n\nMetodo di installazione consigliato (ufficiale):\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\nAlternativa (Arch Linux AUR):\n  paru -S adguard-cli-bin\n\nAdGuard Tray si avvia, ma avvio/arresto non funzioneranno finché adguard-cli non sarà installato.",
    "Copy install command":             "Copia comando di installazione",
    "Continue":                         "Continua",
    "AdGuard Tray is already running":  "AdGuard Tray è già in esecuzione",
    "Only one instance can run at a time. Check your system tray.":
        "Può essere in esecuzione una sola istanza alla volta. Controlla il vassoio di sistema.",
    "Authentication cancelled":         "Autenticazione annullata",
    "Authorization failed":             "Autorizzazione non riuscita",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "Verifica se il certificato di un sito è stato revocato (OCSP).\nAdGuard esegue il controllo in modo asincrono e lascia passare la connessione\nse il controllo è lento, quindi raramente causa problemi con un sito – lascialo attivo\na meno che tu non abbia ricondotto un problema proprio a questo.",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "Impone i controlli Certificate Transparency (criterio CT di Chrome).\nI siti il cui certificato non è conforme a CT non vengono più filtrati\ne il browser potrebbe rifiutarli. I grandi siti sono conformi, quindi prova\nquesta opzione solo per un sito che segnala un errore di certificato.",
    "Sites that don't load":
        "Siti che non si caricano",
    "Turn off HTTP/3 filtering":
        "Disattiva filtraggio HTTP/3",
    "No filters installed":
        "Nessun filtro installato",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "HTTP/3 è bloccato da una regola del firewall; i browser usano HTTP/2.",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "App escluse dal filtraggio (neanche il loro traffico HTTP/3 viene filtrato): {}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuard non è in esecuzione – non viene filtrato nulla.",
    "could not remove the previous certificate":
        "impossibile rimuovere il certificato precedente",
    "HTTP/3 state unknown":
        "Stato HTTP/3 sconosciuto",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "Una regola del firewall rifiuta il traffico UDP 443 in uscita, quindi QUIC non può essere usato.",
    "Browser policy disables QUIC: {}":
        "Criteri del browser che disattivano QUIC: {}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "I browser possono aggirare AdGuard tramite HTTP/3 (UDP 443).",
    "Checking…":
        "Verifica in corso…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "Impossibile leggere proxy.yaml – stato HTTP/3 sconosciuto.",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "Profili della famiglia Firefox con HTTP/3 disattivato: {} di {}",
    "HTTP/3 (QUIC)":
        "HTTP/3 (QUIC)",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "HTTP/3 è bloccato da AdGuard; i browser ripiegano su HTTP/2 filtrato.",
    "HTTP/3 is filtered by AdGuard.":
        "HTTP/3 è filtrato da AdGuard.",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "HTTP/3 disattivato nei profili Firefox – riavvia il browser.",
    "HTTPS filtering is off – nothing is filtered.":
        "Il filtraggio HTTPS è disattivato – non viene filtrato nulla.",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "Modalità proxy: {} – viene filtrato solo il traffico che passa dal proxy e i browser non vi fanno passare QUIC.",
    "unknown":
        "sconosciuta",
    "AdGuard's certificate was not found. Generate it first.":
        "Certificato di AdGuard non trovato. Generalo prima.",
    "Certificate could not be installed in any browser.":
        "Impossibile installare il certificato in alcun browser.",
    "Certificate installed for {} of {} stores.":
        "Certificato installato negli archivi: {} di {}.",
    "Chromium-based browsers":
        "Browser basati su Chromium",
    "No browser certificate stores found.":
        "Nessun archivio dei certificati del browser trovato.",
    "Restart your browsers for the certificate to take effect.":
        "Riavvia i browser per rendere effettivo il certificato.",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "Esegui senza sudo/pkexec – l'installazione avviene nei tuoi profili del browser",
    "certificate not found after import":
        "certificato non trovato dopo l'importazione",
    "certutil not found – install the 'nss' package":
        "certutil non trovato – installa il pacchetto 'nss'",
    "not found":
        "non trovato",
    "Could not read the filter list (unexpected CLI output).":
        "Impossibile leggere l'elenco dei filtri (output della CLI imprevisto).",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "Nessun vassoio di sistema trovato. AdGuard Tray è in esecuzione senza icona — attiva un vassoio/AppIndicator nel pannello.",
    "URL must start with http:// or https://":
        "L'URL deve iniziare con http:// o https://",
    "adguard-cli path does not exist or is not executable.":
        "Il percorso di adguard-cli non esiste o non è eseguibile.",
    "That binary does not identify as adguard-cli. Save anyway?":
        "Questo eseguibile non si identifica come adguard-cli. Salvare comunque?",
    "Update channel":                   "Canale di aggiornamento",
    "Switching update channel to {}…":  "Passaggio al canale di aggiornamento {}…",
    "Update channel set to {}":         "Canale di aggiornamento impostato su {}",
    "Could not set update channel":     "Impossibile impostare il canale di aggiornamento",
    "Invalid channel: {}":              "Canale non valido: {}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        "Ancora nessun log degli accessi ({}). AdGuard lo scrive dopo aver filtrato del traffico; quando è in esecuzione come servizio di sistema, il log appartiene a root e qui non è leggibile.",
    'Cannot read the access log ({}): {}':
        "Impossibile leggere il log degli accessi ({}): {}",
    'Blocked':
        "Bloccate",
    'Blocked only':
        "Solo bloccate",
    "Refresh":
        "Ricarica",
    'Allow selected domain':
        "Consenti dominio selezionato",
    'Block selected domain':
        "Blocca dominio selezionato",
    'Activity':
        "Attività",
    'Time':
        "Ora",
    'Domain':
        "Dominio",
    'Result':
        "Esito",
    'Rule':
        "Regola",
    'Size':
        "Dimensione",
    'Count':
        "Conteggio",
    'Could not read the access log.':
        "Impossibile leggere il log degli accessi.",
    '{} lines not understood':
        "Righe non interpretate: {}",
    'Not a valid domain: {}':
        "Dominio non valido: {}",
    'Source: {}':
        "Origine: {}",
    'Allowed':
        "Consentite",
    'Added rule: {}':
        "Regola aggiunta: {}",
    'Requests per hour, {} to {} · busiest hour: {}':
        "Richieste all'ora, da {} a {} · ora di picco: {}",
    'Last 24 hours':
        "Ultime 24 ore",
    'Last 7 days':
        "Ultimi 7 giorni",
    'Requests':
        "Richieste",
    'Traffic':
        "Traffico",

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        "È disponibile la versione {} (hai la {}).",
    'Application update':
        "Aggiornamento dell'applicazione",
    'Check for update':
        "Controlla aggiornamenti",
    'Install update':
        "Installa aggiornamento",
    'Installing update…':
        "Installazione dell'aggiornamento…",
    'Restart now':
        "Riavvia ora",
    'Later':
        "Più tardi",
    'You are running the latest version ({}).':
        "Stai usando la versione più recente ({}).",
    'Installation not recognised':
        "Tipo di installazione non riconosciuto",
    'Could not check for updates.':
        "Impossibile controllare gli aggiornamenti.",
    'Update with: {}':
        "Aggiorna con: {}",
    'Installed with the AUR package {}':
        "Installato con il pacchetto AUR {}",
    'Installed in {}':
        "Installato in {}",
    'Running from a source checkout':
        "In esecuzione da un checkout dei sorgenti",
    'Version {} installed. Restart adguard-tray to use it.':
        "Versione {} installata. Riavvia adguard-tray per usarla.",
    'Unexpected answer from GitHub: {}':
        "Risposta inattesa da GitHub: {}",
    'Download failed: {}':
        "Download non riuscito: {}",
    'Could not unpack the download: {}':
        "Impossibile estrarre il file scaricato: {}",
    'This installation is managed elsewhere: {}':
        "Questa installazione è gestita altrove: {}",
    'No permission to write to {}':
        "Nessun permesso di scrittura su {}",
    'GitHub returned {}.':
        "GitHub ha risposto con {}.",
    'No connection to GitHub: {}':
        "Nessuna connessione a GitHub: {}",
    'The download does not contain adguard-tray.':
        "Il file scaricato non contiene adguard-tray.",
    'The download says version {} instead of {} – aborted.':
        "Il file scaricato indica la versione {} invece della {} – operazione annullata.",
    'GitHub is rate limiting this address. Try again later.':
        "GitHub sta limitando le richieste da questo indirizzo. Riprova più tardi.",
    'The download is larger than expected – aborted.':
        "Il file scaricato è più grande del previsto – operazione annullata.",
    'Update failed: {}':
        "Aggiornamento non riuscito: {}",
    'The archive contains unexpected paths – aborted.':
        "L'archivio contiene percorsi inattesi – operazione annullata.",
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        "Aggiornamento non riuscito e impossibile ripristinare la versione precedente. Ripristinala da {} o reinstalla con: {}",
    'Last 30 days':
        "Ultimi 30 giorni",
    'All time':
        "Sempre",
    'Modified':
        "Modificata",
    'Rules':
        "Regole",
    'Showing {} – show all':
        "Solo {} – mostra tutto",
    'history {}':
        "cronologia: {}",
    'Filter list ID: {}':
        "ID elenco di filtri: {}",
    'App':
        "App",
    'Protocol':
        "Protocollo",
    'Type':
        "Tipo",
    'Reset history':
        "Azzera cronologia",
    'Delete the stored history and read the log again.':
        "Elimina la cronologia salvata e rilegge il log.",
    'Delete the stored history? Only what the log still holds can be read back.':
        "Eliminare la cronologia salvata? Si potrà recuperare solo ciò che è ancora presente nel log.",
    'History is not being updated: {}':
        "La cronologia non viene aggiornata: {}",

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "1 modifica non salvata alle impostazioni di AdGuard",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "Un filtro attendibile può eseguire script nelle pagine che visiti. Considera attendibili solo elenchi provenienti da fonti che conosci.",
    "About":
        "Informazioni",
    "Actions for the selected filter":
        "Azioni per il filtro selezionato",
    "Ad blocking":
        "Blocco annunci",
    "Ad blocking is off, so the filter lists below have no effect.":
        "Il blocco annunci è disattivato, quindi gli elenchi di filtri qui sotto non hanno effetto.",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLI scarica e installa la sua build più recente.",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "AdGuard CLI dimentica la licenza su questo computer. Dovrai attivarla di nuovo.",
    "AdGuard CLI logs":
        "Log di AdGuard CLI",
    "AdGuard CLI update finished.":
        "Aggiornamento di AdGuard CLI completato.",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "Log di AdGuard Tray",
    "AdGuard doesn't filter these websites.":
        "AdGuard non filtra questi siti web.",
    "AdGuard is filtering this computer's traffic.":
        "AdGuard sta filtrando il traffico di questo computer.",
    "AdGuard restarts to load the new lists.":
        "AdGuard si riavvia per caricare i nuovi elenchi.",
    "AdGuard's reply did not say whether it is running.":
        "Dalla risposta di AdGuard non risulta se è in esecuzione.",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "File delle impostazioni di AdGuard non trovato ({}). Esegui adguard-cli una volta per crearlo.",
    "Add DNS filter by ID":
        "Aggiungi filtro DNS tramite ID",
    "Add DNS filter from URL":
        "Aggiungi filtro DNS da URL",
    "Add filter":
        "Aggiungi filtro",
    "Add filter by ID":
        "Aggiungi filtro tramite ID",
    "Add filter from URL":
        "Aggiungi filtro da URL",
    "Add rule":
        "Aggiungi regola",
    "Add to browsers":
        "Aggiungi ai browser",
    "Add userscript":
        "Aggiungi userscript",
    "Add userscript…":
        "Aggiungi userscript…",
    "Add website":
        "Aggiungi sito web",
    "Add…":
        "Aggiungi…",
    "Advanced":
        "Avanzate",
    "All available":
        "Tutti quelli disponibili",
    "Allow {}":
        "Consenti {}",
    "Also adds the certificate to this Firefox profile.":
        "Aggiunge il certificato anche a questo profilo Firefox.",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "Anche in caso di riavvii ed errori. Richiede notify-send (libnotify) o un servizio di notifiche attivo come dunst, mako o quello di KDE.",
    "Appearance":
        "Aspetto",
    "Applies after AdGuard Tray restarts.":
        "Ha effetto dopo il riavvio di AdGuard Tray.",
    "Apply":
        "Applica",
    "Apply your changes to AdGuard's settings before closing?":
        "Applicare le modifiche alle impostazioni di AdGuard prima di chiudere?",
    "Applying them restarts AdGuard if protection is on.":
        "Se la protezione è attiva, applicarle riavvia AdGuard.",
    "Asks GitHub for the newest release.":
        "Chiede a GitHub la release più recente.",
    "At a glance":
        "In breve",
    "Automatic":
        "Automatica",
    "Automatic – filter all apps":
        "Automatica – filtra tutte le app",
    "Benchmark":
        "Benchmark",
    "Beta":
        "Beta",
    "Block ECH in DNS records":
        "Blocca ECH nei record DNS",
    "Block domains before a connection is made.":
        "Blocca i domini prima che venga stabilita una connessione.",
    "Block {}":
        "Blocca {}",
    "Blocked (24 h)":
        "Bloccate (24 h)",
    "Browser list ({})":
        "Elenco browser ({})",
    "By ID or name…":
        "Tramite ID o nome…",
    "Certificate":
        "Certificato",
    "Certificate checks":
        "Controlli dei certificati",
    "Changes are collected in the bar at the bottom and applied together.":
        "Le modifiche vengono raccolte nella barra in basso e applicate tutte insieme.",
    "Check again":
        "Controlla di nuovo",
    "Check every":
        "Controlla ogni",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "I browser basati su Chromium e Firefox hanno un proprio archivio dei certificati.",
    "Close":
        "Chiudi",
    "Controls which AdGuard CLI build “{}” installs.":
        "Determina quale build di AdGuard CLI viene installata da “{}”.",
    "Could not add the rule.":
        "Impossibile aggiungere la regola.",
    "Could not open {}":
        "Impossibile aprire {}",
    "Could not read {}":
        "Impossibile leggere {}",
    "Could not refresh. Showing data from {}.":
        "Impossibile ricaricare. Vengono mostrati i dati delle ore {}.",
    "Could not reset the history.":
        "Impossibile azzerare la cronologia.",
    "Could not restart AdGuard.":
        "Impossibile riavviare AdGuard.",
    "Could not start protection.":
        "Impossibile avviare la protezione.",
    "Could not stop protection.":
        "Impossibile arrestare la protezione.",
    "Create":
        "Crea",
    "Create certificate":
        "Crea certificato",
    "Custom":
        "Personalizzato",
    "DNS filter lists":
        "Elenchi di filtri DNS",
    "DNS filtering":
        "Filtraggio DNS",
    "DNS filtering is off, so these lists have no effect.":
        "Il filtraggio DNS è disattivato, quindi questi elenchi non hanno effetto.",
    "DNS servers":
        "Server DNS",
    "Dark":
        "Scuro",
    "Default":
        "Predefinito",
    "Details":
        "Dettagli",
    "Discard":
        "Scarta",
    "Don't filter":
        "Non filtrare",
    "Don't trust":
        "Non considerare attendibile",
    "Downloads and installs the newest AdGuard CLI build.":
        "Scarica e installa la build più recente di AdGuard CLI.",
    "Duration":
        "Durata",
    "Export…":
        "Esporta…",
    "Filter everything":
        "Filtra tutto",
    "Filter in place":
        "Filtra direttamente",
    "Filtering":
        "Filtraggio",
    "Follow system":
        "Segui il sistema",
    "From URL…":
        "Da URL…",
    "Go to updates":
        "Vai agli aggiornamenti",
    "HTTP proxy: {}":
        "Proxy HTTP: {}",
    "HTTPS filtering":
        "Filtraggio HTTPS",
    "How much detail AdGuard Tray writes to its own log.":
        "Quanti dettagli AdGuard Tray scrive nel proprio log.",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "Se un sito non si carica, disattiva prima il filtraggio HTTP/3. Gli altri controlli proteggono tutti i siti – disattivali solo se non è servito.",
    "Included":
        "Incluso",
    "Installed":
        "Installati",
    "License":
        "Licenza",
    "Light":
        "Chiaro",
    "Logs":
        "Log",
    "MIT license":
        "Licenza MIT",
    "Maintenance":
        "Manutenzione",
    "Manual proxy":
        "Proxy manuale",
    "Manual – only apps set to use the proxy":
        "Manuale – solo le app configurate per usare il proxy",
    "More":
        "Altro",
    "Move down":
        "Sposta giù",
    "Move up":
        "Sposta su",
    "Network":
        "Rete",
    "Nightly":
        "Nightly",
    "No requests yet – AdGuard logs requests while protection is on.":
        "Ancora nessuna richiesta – AdGuard registra le richieste mentre la protezione è attiva.",
    "Not added":
        "Non aggiunto",
    "Nothing matches your search.":
        "Nessun risultato per la ricerca.",
    "Notify me when protection turns on or off":
        "Avvisami quando la protezione si attiva o disattiva",
    "Off":
        "Disattivato",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "Riguarda solo i browser che usano DoH o DoT. Con “Disattivato” possono aggirare il filtraggio DNS di AdGuard.",
    "Open AdGuard Tray":
        "Apri AdGuard Tray",
    "Open exceptions":
        "Apri eccezioni",
    "Open folder":
        "Apri cartella",
    "Open release page":
        "Apri pagina della release",
    "Pages":
        "Pagine",
    "Performance":
        "Prestazioni",
    "Protection":
        "Protezione",
    "Protection started.":
        "Protezione avviata.",
    "Protection stopped.":
        "Protezione arrestata.",
    "Proxy mode":
        "Modalità proxy",
    "Redirect to AdGuard's DNS":
        "Reindirizza al DNS di AdGuard",
    "Refresh this page (F5)":
        "Ricarica questa pagina (F5)",
    "Release (stable)":
        "Release (stabile)",
    "Remove rule":
        "Rimuovi regola",
    "Remove “{}”?":
        "Rimuovere “{}”?",
    "Remove…":
        "Rimuovi…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "Sostituire le impostazioni attuali di AdGuard con quelle contenute in {}?\n\nAdGuard si riavvia per applicarle.",
    "Reset history…":
        "Azzera cronologia…",
    "Reset…":
        "Reimposta…",
    "Restart AdGuard":
        "Riavvia AdGuard",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "Le regole valgono solo in modalità proxy automatica. Si applica la prima regola corrispondente, quindi metti \"*\" per ultimo.",
    "Safe Browsing":
        "Sicurezza di navigazione",
    "Save anyway":
        "Salva comunque",
    "Saved. AdGuard restarts to apply the change.":
        "Salvato. AdGuard si riavvia per applicare la modifica.",
    "Saved. Applies after AdGuard Tray restarts.":
        "Salvato. Ha effetto dopo il riavvio di AdGuard Tray.",
    "Saved. The change applies when protection is turned on.":
        "Salvato. La modifica avrà effetto quando attivi la protezione.",
    "Secure DNS and ECH":
        "DNS sicuro ed ECH",
    "Secure DNS filtering":
        "Filtraggio DNS sicuro",
    "Set the path in Settings":
        "Imposta il percorso in “Impostazioni”",
    "Settings":
        "Impostazioni",
    "Show":
        "Mostra",
    "Show recent entries":
        "Mostra voci recenti",
    "Skip HTTPS filtering":
        "Escludi dal filtraggio HTTPS",
    "Some counts could not be loaded.":
        "Impossibile caricare alcuni conteggi.",
    "Source code":
        "Codice sorgente",
    "Start AdGuard Tray when I log in":
        "Avvia AdGuard Tray all'accesso",
    "Startup":
        "Avvio",
    "Status checks":
        "Controlli dello stato",
    "Stealth mode":
        "Modalità invisibilità",
    "System":
        "Sistema",
    "The new lists load when protection is turned on.":
        "I nuovi elenchi verranno caricati quando attivi la protezione.",
    "Theme":
        "Tema",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "Vengono disattivati il filtraggio HTTP/3, i controlli OCSP, Certificate Transparency e il filtraggio DNS sicuro. I certificati revocati o emessi in modo errato passeranno quindi inosservati e i browser potranno risolvere i nomi aggirando il filtro DNS di AdGuard.",
    "Time range":
        "Intervallo",
    "To keep it but stop using it, switch it off instead.":
        "Per tenerlo senza usarlo, disattivalo invece di rimuoverlo.",
    "Top lists":
        "Classifiche",
    "Trust":
        "Considera attendibile",
    "Trust “{}”?":
        "Considerare attendibile “{}”?",
    "Trust…":
        "Considera attendibile…",
    "Turn off all strict checks…":
        "Disattiva tutti i controlli rigorosi…",
    "Undo":
        "Annulla",
    "Unknown":
        "Sconosciuto",
    "Unsaved changes":
        "Modifiche non salvate",
    "Update AdGuard CLI…":
        "Aggiorna AdGuard CLI…",
    "Update channel: {}":
        "Canale di aggiornamento: {}",
    "Updated {}":
        "Aggiornato: {}",
    "Updates":
        "Aggiornamenti",
    "Used in manual mode only.":
        "Usato solo in modalità manuale.",
    "Userscripts update together with filters.":
        "Gli userscript si aggiornano insieme ai filtri.",
    "Uses XDG autostart (~/.config/autostart).":
        "Usa l'avvio automatico XDG (~/.config/autostart).",
    "Waiting for authorization…":
        "In attesa di autorizzazione…",
    "Website exceptions":
        "Eccezioni siti web",
    "Websites":
        "Siti web",
    "example.com or a link":
        "example.com o un link",
    "expires {}":
        "scadenza: {}",
    "of {} requests in the last 24 hours":
        "su un totale di {} nelle ultime 24 ore",
    "{} of {} DNS filters on":
        "Filtri DNS attivi: {} di {}",
    "{} of {} filters on":
        "Filtri attivi: {} di {}",
    "{} of {} on":
        "Attivi: {} di {}",
    "{} unsaved changes to AdGuard's settings":
        "Modifiche non salvate alle impostazioni di AdGuard: {}",
    "“Follow system” uses your desktop's light or dark setting.":
        "“Segui il sistema” usa il tema chiaro o scuro del desktop.",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "Attiva",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "Il certificato di AdGuard verrà aggiunto a ogni profilo di browser trovato su questo sistema.\n\nIn questo modo AdGuard può ispezionare il traffico HTTPS in quei browser. Chiudi prima i browser – leggono l'archivio dei certificati all'avvio.",
    "Allow":
        "Consenti",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "Applica o scarta prima le modifiche alle impostazioni di AdGuard, poi riavvia.",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "Automatica: AdGuard reindirizza a sé tutto il traffico delle app tramite iptables. Manuale: AdGuard resta in ascolto solo sulle porte SOCKS5 e HTTP qui sotto.",
    "Block":
        "Blocca",
    "Browser API blocking":
        "Blocco delle API del browser",
    "CRLite":
        "CRLite",
    "Cancel":
        "Annulla",
    "Computers":
        "Computer",
    "Could not change the autostart entry.":
        "Impossibile modificare la voce di avvio automatico.",
    "Could not export the logs.":
        "Impossibile esportare i log.",
    "Could not export the settings.":
        "Impossibile esportare le impostazioni.",
    "Could not reset the license.":
        "Impossibile reimpostare la licenza.",
    "Could not retrieve license info.":
        "Impossibile recuperare le informazioni sulla licenza.",
    "Could not run the benchmark.":
        "Impossibile eseguire il benchmark.",
    "Could not save the settings.":
        "Impossibile salvare le impostazioni.",
    "Could not set the update channel.":
        "Impossibile impostare il canale di aggiornamento.",
    "Could not update AdGuard CLI.":
        "Impossibile aggiornare AdGuard CLI.",
    "Could not update the filters.":
        "Impossibile aggiornare i filtri.",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "Server DNS upstream.\n'default' = DNS di sistema.\nEsempi: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com",
    "Expiration date":
        "Data di scadenza",
    "Expires":
        "Scadenza",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "HTTP/3 riattivato nei profili Firefox – riavvia il browser.",
    "License key":
        "Chiave di licenza",
    "License type":
        "Tipo di licenza",
    "Manual":
        "Manuale",
    "No exceptions.":
        "Nessuna eccezione.",
    "OK":
        "OK",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "Attivo: AdGuard filtra direttamente HTTP/3 (QUIC) – sperimentale, e alcuni\nbrowser rifiutano comunque HTTP/3 con un certificato installato dall'utente.\nDisattivato: AdGuard blocca invece QUIC, così i browser ripiegano su HTTP/2,\nche viene filtrato in modo affidabile.\nIn entrambi i casi vale solo in modalità automatica – in modalità manuale\nil traffico HTTP/3 non raggiunge mai AdGuard.",
    "Owner":
        "Titolare",
    "Personal":
        "Personale",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "Modalità proxy: {} – la porta UDP 443 viene reindirizzata ad AdGuard.",
    "Save adguard-cli path":
        "Salva percorso di adguard-cli",
    "Search domains or rules…":
        "Cerca domini o regole…",
    "Settings file":
        "File delle impostazioni",
    "Status":
        "Stato",
    "Trial":
        "Prova",
    "Turn HTTP/3 back on in Firefox profiles":
        "Riattiva HTTP/3 nei profili Firefox",
    "Turn off":
        "Disattiva",
    "Turn off HTTP/3 in Firefox profiles":
        "Disattiva HTTP/3 nei profili Firefox",
    "Turn off HTTP/3 in Firefox profiles…":
        "Disattiva HTTP/3 nei profili Firefox…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "Disattivare HTTP/3 nei profili della famiglia Firefox (trovati: {})?\n\nIl loro traffico userà quindi HTTP/2, che AdGuard può filtrare. Al termine riavvia il browser.",
    "Turn off all strict checks":
        "Disattiva tutti i controlli rigorosi",
    "Unavailable until AdGuard CLI reports its current channel.":
        "Non disponibile finché AdGuard CLI non comunica il canale attuale.",
    "Update AdGuard CLI":
        "Aggiorna AdGuard CLI",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "Usate solo in modalità automatica. Intervalli (80:5221,5300:49151) o porte singole (80,443,8080).",
    "{} of {}":
        "{} di {}",
    "{} of {} userscripts on":
        "Userscript attivi: {} di {}",
    "{}% blocked":
        "{}% bloccate",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "Fastidi",
    "General":
        "Generali",
    "Language-specific":
        "Specifici per lingua",
    "Security":
        "Sicurezza",
    "Social widgets":
        "Widget social",
    "Expired":
        "Scaduta",
    "Autostart on login":
        "Avvio automatico all'accesso",
    "Add app rule":
        "Aggiungi regola app",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "Puoi usare caratteri jolly, es. *steam* o *EasyAntiCheat*.",
    "There is already a rule for '{}'.":
        "Esiste già una regola per “{}”.",
    "AdGuard settings":
        "Impostazioni di AdGuard",
    "Ads and trackers are not blocked until you enable protection.":
        "Annunci e tracciatori non vengono bloccati finché non attivi la protezione.",
    "Could not import the settings.":
        "Impossibile importare le impostazioni.",
    "Disable protection":
        "Disattiva protezione",
    "Enable protection":
        "Attiva protezione",
    "Export and import":
        "Esportazione e importazione",
    "Features":
        "Funzionalità",
    "Import settings":
        "Importa impostazioni",
    "Import settings from…":
        "Importa impostazioni da…",
    "Import settings…":
        "Importa impostazioni…",
    "Import…":
        "Importa…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "Salva filtri, regole e configurazione in un file zip o caricali da un file.",
    "Update":
        "Aggiorna",
    "Version":
        "Versione",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "{} non è un'esportazione delle impostazioni. Scegli un file salvato con “Esporta…” in “Impostazioni di AdGuard”.",

    # ── AdGuard VPN, outbound proxy, install ──────────────────────────
    "Press Enter to close this window.":
        "Premi Invio per chiudere questa finestra.",
    "No terminal app was found. The install command is on the clipboard: paste it into a terminal.":
        "Nessuna app di terminale trovata. Il comando di installazione è negli appunti: incollalo in un terminale.",
    "Finish the installation in the terminal, then press Refresh.":
        "Completa l'installazione nel terminale, poi premi “Ricarica”.",
    "Open in a terminal":
        "Apri in un terminale",
    "AdGuard VPN":
        "AdGuard VPN",
    "AdGuard's VPN for Linux (adguardvpn-cli) runs next to AdGuard CLI. AdGuard Tray checks that their settings fit together; it does not connect the VPN or log in.":
        "La VPN di AdGuard per Linux (adguardvpn-cli) funziona insieme ad AdGuard CLI. AdGuard Tray verifica che le loro impostazioni siano compatibili; non connette la VPN né effettua l'accesso.",
    "Install…":
        "Installa…",
    "Outbound proxy":
        "Proxy in uscita",
    "AdGuard sends its own connections through this proxy, for example through AdGuard VPN in SOCKS5 mode.":
        "AdGuard instrada le proprie connessioni attraverso questo proxy, ad esempio tramite AdGuard VPN in modalità SOCKS5.",
    "Use an outbound proxy":
        "Usa un proxy in uscita",
    "Host":
        "Host",
    "Port":
        "Porta",
    "Not installed.":
        "Non installato.",
    "AdGuard VPN is set to TUN mode while AdGuard filters in automatic mode. Connected like this, traffic loops between the two – AdGuard does not support this combination.":
        "AdGuard VPN è impostata sulla modalità TUN mentre AdGuard filtra in modalità automatica. Se la VPN è connessa così, il traffico va in loop tra i due – AdGuard non supporta questa combinazione.",
    "AdGuard VPN now uses SOCKS5 mode. Press Apply to send AdGuard's traffic through it, and reconnect AdGuard VPN if it is connected.":
        "AdGuard VPN ora usa la modalità SOCKS5. Premi “Applica” per instradare il traffico di AdGuard attraverso la VPN e riconnetti AdGuard VPN se la connessione è attiva.",
    "AdGuard VPN CLI":
        "AdGuard VPN CLI",
    "Installed, but its settings could not be read: {}":
        "Installato, ma impossibile leggerne le impostazioni: {}",
    "Route AdGuard through the VPN":
        "Instrada AdGuard attraverso la VPN",
    "Could not switch AdGuard VPN to SOCKS5 mode.":
        "Impossibile impostare AdGuard VPN sulla modalità SOCKS5.",
    "Installed · SOCKS5 mode on {}:{}":
        "Installato · modalità SOCKS5 su {}:{}",
    "Installed · TUN mode":
        "Installato · modalità TUN",
    "Installed · {} mode":
        "Installato · modalità {}",
}
