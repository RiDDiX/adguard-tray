"""French."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "Langue",
    "English":                           "Anglais",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "Actif – Protection en cours",
    "Inactive – Protection stopped":        "Inactif – Protection arrêtée",
    "Error retrieving status":              "Erreur lors de la récupération de l’état",
    "adguard-cli not found":                "adguard-cli introuvable",
    "Unknown status":                       "État inconnu",
    "Checking status…":                     "Vérification de l’état…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "Redémarrer",
    "Filters":                              "Filtres",
    "Loading…":                             "Chargement…",
    "Manage filters…":                      "Gérer les filtres…",
    "No userscripts installed":             "Aucun script utilisateur installé",
    "Manage userscripts…":                  "Gérer les scripts utilisateur…",
    "Quit":                                 "Quitter",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "actif",
    "inactive":                             "inactif",
    "System-wide filtering: {}":            "Filtrage à l’échelle du système : {}",
    "Error: {}":                            "Erreur : {}",
    "AdGuard Tray – Error":                 "AdGuard Tray – Erreur",
    "AdGuard is now active – protection running.":
        "AdGuard est maintenant actif – protection en cours.",
    "AdGuard has been stopped.":
        "AdGuard a été arrêté.",
    "Could not retrieve status.":
        "Impossible de récupérer l’état.",
    "Command failed":                       "Échec de la commande",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " secondes",
    "How often adguard-cli status is checked automatically.":
        "Fréquence de vérification automatique de l’état d’adguard-cli.",
    "Log level:":                           "Niveau de journalisation :",
    "adguard-cli path:":                    "Chemin d’adguard-cli :",
    "auto-detect via PATH":                 "détection automatique via PATH",
    "Browse…":                              "Parcourir…",
    "Select adguard-cli binary":            "Sélectionner l’exécutable adguard-cli",
    "Notifications":                        "Notifications",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "Mettre à jour les filtres",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "Met à jour tous les filtres, les filtres DNS, les scripts utilisateur,\nSafebrowsingV2 et CRLite, puis recherche les mises à jour de l’application.",
    "No filters found.":                    "Aucun filtre trouvé.",
    "Updating filters… (can take up to 2 minutes)":
        "Mise à jour des filtres… (cela peut prendre jusqu’à 2 minutes)",
    "Update completed.":                    "Mise à jour terminée.",
    "Update failed.":                       "Échec de la mise à jour.",
    "Installing: {}":                       "Installation : {}",
    "Filter installed.":                    "Filtre installé.",
    "Remove":                               "Supprimer",
    "Remove filter":                        "Supprimer le filtre",
    "Filter {} removed.":                   "Filtre {} supprimé.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        "Installer un script utilisateur depuis une URL .js directe",
    "No userscripts installed.":            "Aucun script utilisateur installé.",
    "Userscript URL (direct .js URL):":     "URL du script utilisateur (URL .js directe) :",
    "Userscript installed.":                "Script utilisateur installé.",
    'Remove "{}"':                          "Supprimer « {} »",
    "Remove userscript":                    "Supprimer le script utilisateur",
    "'{}' removed.":                        "« {} » supprimé.",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "adguard-cli est introuvable.\nInstallez-le avec le script officiel ou depuis AUR :\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "Erreur inconnue lors de la récupération de l’état",
    "AdGuard {} ok":                        "AdGuard {} : OK",
    "AdGuard via systemctl {} ok":          "AdGuard via systemctl {} : OK",
    "'{}' failed – insufficient privileges?":
        "Échec de « {} » – privilèges insuffisants ?",
    "Could not retrieve filter list":
        "Impossible de récupérer la liste des filtres",
    "Filter {} enabled":                    "Filtre {} activé",
    "Could not enable filter {}":           "Impossible d’activer le filtre {}",
    "Filter {} disabled":                   "Filtre {} désactivé",
    "Could not disable filter {}":
        "Impossible de désactiver le filtre {}",
    "Filter installed":                     "Filtre installé",
    "Installation failed":                  "Échec de l’installation",
    "Filter {} removed":                    "Filtre {} supprimé",
    "Could not remove filter {}":
        "Impossible de supprimer le filtre {}",
    "Filters updated":                      "Filtres mis à jour",
    "Update failed":                        "Échec de la mise à jour",
    "Could not retrieve userscript list":
        "Impossible de récupérer la liste des scripts utilisateur",
    "Userscript '{}' enabled":              "Script utilisateur « {} » activé",
    "Could not enable userscript '{}'":
        "Impossible d’activer le script utilisateur « {} »",
    "Userscript '{}' disabled":             "Script utilisateur « {} » désactivé",
    "Could not disable userscript '{}'":
        "Impossible de désactiver le script utilisateur « {} »",
    "Userscript '{}' removed":              "Script utilisateur « {} » supprimé",
    "Could not remove userscript '{}'":
        "Impossible de supprimer le script utilisateur « {} »",
    "Userscript installed":                 "Script utilisateur installé",
    "Other":                                "Autres",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "Rechercher des filtres…",
    "Search userscripts…":              "Rechercher des scripts utilisateur…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "Impossible de charger proxy.yaml.\nChemin : {}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "Applications",
    "Mode:":                            "Mode :",
    "Filtered ports:":                  "Ports filtrés :",
    "SOCKS5 port:":                     "Port SOCKS5 :",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "Port du proxy SOCKS5 pour le mode manuel.\nIndiquez -1 pour le désactiver.",
    "HTTP port:":                       "Port HTTP :",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "Port du proxy HTTP pour le mode manuel.\nIndiquez -1 pour le désactiver.",
    "Listen address:":                  "Adresse d’écoute :",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "Adresse sur laquelle le proxy écoute.\n127.0.0.1 = local uniquement. 0.0.0.0 = toutes les interfaces (authentification requise).",
    "Worker threads:":                  "Threads de travail :",
    "Number of proxy worker threads.":  "Nombre de threads de travail du proxy.",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "Déchiffre et filtre le trafic HTTPS.\nNécessaire pour bloquer les publicités sur les sites https.\nNécessite un certificat racine de confiance installé sur le système.",
    "Enable TLS 1.3":                   "Activer TLS 1.3",
    "Enable TLS 1.3 support for filtered connections.":
        "Active la prise en charge de TLS 1.3 pour les connexions filtrées.",
    "Filter HTTP/3 (QUIC) – experimental":
        "Filtrer HTTP/3 (QUIC) – expérimental",
    "OCSP certificate checks":          "Vérifications OCSP des certificats",
    "Enforce Certificate Transparency": "Imposer Certificate Transparency",
    "Filter EV certificate sites":      "Filtrer les sites à certificat EV",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "Par défaut, les sites dotés d’un certificat EV (Extended Validation) ne sont pas filtrés.\nActivez cette option pour les filtrer aussi (p. ex. les sites bancaires).",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "Active ECH pour une meilleure confidentialité.\nNécessite l’activation du filtrage DNS.",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "Filtre les requêtes DNS pour bloquer les publicités et les traqueurs au niveau DNS.\nUtilise un proxy DNS local avec des serveurs amont configurables.",
    "Upstream:":                        "Serveur amont :",
    "Fallbacks:":                       "Serveurs de secours :",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "Serveurs DNS de secours (utilisés en cas de défaillance du serveur amont principal).\n'default' = DNS du système. Liste séparée par des espaces.\nExemple : default 1.1.1.1",
    "Bootstraps:":                      "Serveurs d’amorçage :",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "DNS d’amorçage pour résoudre les noms d’hôte des serveurs amont.\n'default' = IP des DNS du système. Adresses IP uniquement.\nExemple : default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "Supprime le paramètre ECH des enregistrements DNS SVCB/HTTPS.\nN’activez cette option que pour les navigateurs qui ne détectent pas automatiquement le filtrage HTTPS.",
    "Master switch for all tracking protection features below.":
        "Interrupteur principal de toutes les fonctions de protection contre le suivi ci-dessous.",
    "Cookies":                          "Cookies",
    "Block third-party cookies":        "Bloquer les cookies tiers",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "Supprime les cookies tiers après un délai défini.\nEmpêche le suivi intersite.",
    "Lifetime (minutes):":              "Durée de vie (minutes) :",
    "0 = block immediately. Default: 180 minutes.":
        "0 = bloquer immédiatement. Par défaut : 180 minutes.",
    "Block first-party cookies":        "Bloquer les cookies propriétaires",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "Supprime tous les cookies (y compris propriétaires) après un délai défini.\nAttention : vous serez déconnecté de tous les sites.",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = bloquer immédiatement. Par défaut : 4320 minutes (3 jours).",
    "Privacy":                          "Confidentialité",
    "Hide / reduce User-Agent":         "Masquer / réduire le User-Agent",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "Retire les éléments identifiants du User-Agent.\nLimite la prise d’empreinte numérique.",
    "Hide search queries in referrer":  "Masquer les requêtes de recherche dans le référent",
    "Hides your search terms when clicking from a search engine to a website.":
        "Masque vos termes de recherche lorsque vous passez d’un moteur de recherche à un site web.",
    "Remove referrer from third-party requests":
        "Supprimer le référent des requêtes tierces",
    "Prevents third-party sites from knowing which page you came from.":
        "Empêche les sites tiers de savoir de quelle page vous venez.",
    "Send Do-Not-Track signal":         "Envoyer le signal Do-Not-Track",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "Envoie l’en-tête DNT avec les requêtes.\nRemarque : la plupart des sites l’ignorent, mais certains le respectent.",
    "Disable third-party ETag cache":   "Désactiver le cache ETag tiers",
    "Prevents tracking via ETag caching in third-party content.":
        "Empêche le suivi via le cache ETag dans les contenus tiers.",
    "Block third-party Authorization header":
        "Bloquer l’en-tête Authorization tiers",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "Bloque l’en-tête Authorization dans les requêtes tierces pour empêcher le suivi.",
    "Remove X-Client-Data header":      "Retirer l’en-tête X-Client-Data",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "Retire l’en-tête X-Client-Data envoyé par Chrome aux services Google.",
    "Block WebRTC":                     "Bloquer WebRTC",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "Empêche les fuites d’adresse IP via WebRTC.\nPeut perturber les appels vidéo et certaines applications web.",
    "Block Push API":                   "Bloquer l’API Push",
    "Blocks browser push notifications from websites.":
        "Bloque les notifications push des sites web dans le navigateur.",
    "Block Location API":               "Bloquer l’API de position",
    "Prevents websites from accessing your GPS location.":
        "Empêche les sites web d’accéder à votre position GPS.",
    "Block Flash":                      "Bloquer Flash",
    "Blocks the Flash plugin.":
        "Bloque le plugin Flash.",
    "Block Java":                       "Bloquer Java",
    "Disables Java plugins. JavaScript remains enabled.":
        "Désactive les plugins Java. JavaScript reste activé.",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "Activer Anti-DPI",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "Modifie les données des paquets sortants pour contourner l’inspection approfondie des paquets (DPI).\nUtile dans les pays qui censurent Internet.",
    "App pattern":
        "Motif d’application",
    "Skip outbound proxy":              "Ignorer le proxy sortant",
    "Don't route this app's traffic through outbound proxy":
        "Ne pas faire passer le trafic de cette application par le proxy sortant",
    "Browser list included from {}":    "Liste de navigateurs incluse depuis {}",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "La liste de navigateurs incluse et la règle générique (*) ne peuvent pas être supprimées.",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "Vous avertit des sites web malveillants et d’hameçonnage.\nUtilise la base de données de Navigation sécurisée d’AdGuard.",
    "Send anonymous statistics":        "Envoyer des statistiques anonymes",
    "Send anonymous lookups to AdGuard.":
        "Envoie des requêtes anonymes à AdGuard.",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "Vérification de la révocation des certificats avec CRLite de Mozilla.\nPlus rapide et plus fiable que les vérifications CRL/OCSP classiques.",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "Applique les règles de filtrage publicitaire aux requêtes HTTP/HTTPS.",
    "Save failed":                      "Échec de l’enregistrement",
    "Could not save proxy.yaml:\n{}":   "Impossible d’enregistrer proxy.yaml :\n{}",
    "Restarting AdGuard…":              "Redémarrage d’AdGuard…",
    "AdGuard restarted.":               "AdGuard redémarré.",
    "Restart failed: {}":               "Échec du redémarrage : {}",
    "Unknown error":                    "Erreur inconnue",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "Ajouter",
    "Search exceptions…":               "Rechercher des exceptions…",
    "1 exception":                      "1 exception",
    "{} exceptions":                    "Exceptions : {}",
    "'{}' is not a valid domain or IP address.":
        "« {} » n’est pas un domaine ou une adresse IP valide.",
    "'{}' is already in the list.":     "« {} » figure déjà dans la liste.",
    "Could not save exceptions:\n{}":
        "Impossible d’enregistrer les exceptions :\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "Aperçu",
    "Userscripts":                      "Scripts utilisateur",
    "Exceptions":                       "Exceptions",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "Réinitialiser la licence",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "Générer un certificat racine (CA) pour le filtrage HTTPS. Le certificat doit être installé et approuvé sur votre système.",
    "Checking for updates…":            "Recherche de mises à jour…",
    "Firefox profile:":                 "Profil Firefox :",
    "(optional) e.g. abcd1234.MyProfile":
        "(facultatif) p. ex. abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "Saisissez l’ID ou le nom du filtre :",
    "Filter added.":                    "Filtre ajouté.",
    "Rename…":                          "Renommer…",
    "Rename filter":                    "Renommer le filtre",
    "New title:":                       "Nouveau titre :",
    "Filter renamed.":                  "Filtre renommé.",
    "Filter trust updated.":            "Confiance du filtre mise à jour.",
    "Filter URL:":                      "URL du filtre :",
    "Title:":                           "Titre :",
    "(optional)":                       "(facultatif)",
    "Trusted filter":                   "Filtre de confiance",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "Rechercher des filtres DNS…",
    "No DNS filters found.":            "Aucun filtre DNS trouvé.",
    "DNS filter installed.":            "Filtre DNS installé.",
    "DNS filter added.":                "Filtre DNS ajouté.",
    "Remove DNS filter":                "Supprimer le filtre DNS",
    "DNS filter {} removed.":           "Filtre DNS {} supprimé.",
    "Rename DNS filter":                "Renommer le filtre DNS",
    "DNS filter renamed.":              "Filtre DNS renommé.",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "Exporter les journaux…",
    "Export AdGuard CLI logs to a zip file":
        "Exporter les journaux d’AdGuard CLI dans un fichier zip",
    "Export settings…":                 "Exporter les paramètres…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "Lancer un test de performances de la cryptographie et du filtrage HTTPS.",
    "Run benchmark":                    "Lancer le test de performances",
    "Done.":                            "Terminé.",
    "Export logs to…":                  "Exporter les journaux vers…",
    "Export settings to…":              "Exporter les paramètres vers…",
    "Zip files (*.zip);;All files (*)":
        "Fichiers zip (*.zip);;Tous les fichiers (*)",
    "Log file not found.":              "Fichier journal introuvable.",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "Impossible de récupérer la liste des filtres DNS",
    "DNS filter {} enabled":            "Filtre DNS {} activé",
    "Could not enable DNS filter {}":   "Impossible d’activer le filtre DNS {}",
    "DNS filter {} disabled":           "Filtre DNS {} désactivé",
    "Could not disable DNS filter {}":  "Impossible de désactiver le filtre DNS {}",
    "DNS filter installed":             "Filtre DNS installé",
    "DNS filter {} removed":            "Filtre DNS {} supprimé",
    "Could not remove DNS filter {}":   "Impossible de supprimer le filtre DNS {}",
    "DNS filter added":                 "Filtre DNS ajouté",
    "Could not add DNS filter":         "Impossible d’ajouter le filtre DNS",
    "DNS filter title updated":         "Titre du filtre DNS mis à jour",
    "Could not set DNS filter title":   "Impossible de définir le titre du filtre DNS",
    "Filter added":                     "Filtre ajouté",
    "Could not add filter":             "Impossible d’ajouter le filtre",
    "Filter trust updated":             "Confiance du filtre mise à jour",
    "Could not update filter trust":    "Impossible de mettre à jour la confiance du filtre",
    "Filter title updated":             "Titre du filtre mis à jour",
    "Could not set filter title":       "Impossible de définir le titre du filtre",
    "License reset":                    "Licence réinitialisée",
    "Could not reset license":          "Impossible de réinitialiser la licence",
    "Could not retrieve license info":  "Impossible de récupérer les informations de licence",
    "Certificate generated":            "Certificat généré",
    "Certificate generation failed":    "Échec de la génération du certificat",
    "Logs exported":                    "Journaux exportés",
    "Log export failed":                "Échec de l’export des journaux",
    "Settings exported":                "Paramètres exportés",
    "Settings export failed":           "Échec de l’export des paramètres",
    "Settings imported":                "Paramètres importés",
    "Settings import failed":           "Échec de l’import des paramètres",
    "Update check completed":           "Vérification des mises à jour terminée",
    "Update check failed":              "Échec de la vérification des mises à jour",
    "Benchmark failed":                 "Échec du test de performances",
    "AdGuard stopped (forced)":         "AdGuard arrêté de force",
    "Could not stop AdGuard – process may still be running":
        "Impossible d’arrêter AdGuard – le processus est peut-être encore en cours d’exécution",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "adguard-cli est introuvable sur ce système.\n\nMéthode d’installation recommandée (officielle) :\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\nAutre possibilité (AUR d’Arch Linux) :\n  paru -S adguard-cli-bin\n\nAdGuard Tray se lance, mais le démarrage et l’arrêt ne fonctionneront pas tant qu’adguard-cli ne sera pas installé.",
    "Copy install command":             "Copier la commande d’installation",
    "Continue":                         "Continuer",
    "AdGuard Tray is already running":  "AdGuard Tray est déjà en cours d’exécution",
    "Only one instance can run at a time. Check your system tray.":
        "Une seule instance peut s’exécuter à la fois. Regardez dans votre zone de notification.",
    "Authentication cancelled":         "Authentification annulée",
    "Authorization failed":             "Échec de l’autorisation",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "Vérifie si le certificat d’un site a été révoqué (OCSP).\nAdGuard vérifie de manière asynchrone et laisse passer la connexion si\nla vérification est lente ; elle perturbe donc rarement un site – laissez-la\nactivée, sauf si vous avez établi qu’un problème vient bien d’elle.",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "Impose les vérifications Certificate Transparency (politique CT de Chrome).\nLes sites dont le certificat n’est pas conforme à CT ne sont plus filtrés\net le navigateur peut les refuser. Les grands sites sont conformes ; ne désactivez donc\ncette option que si un site signale une erreur de certificat.",
    "Sites that don't load":
        "Sites qui ne se chargent pas",
    "Turn off HTTP/3 filtering":
        "Désactiver le filtrage HTTP/3",
    "No filters installed":
        "Aucun filtre installé",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "HTTP/3 est bloqué par une règle de pare-feu ; les navigateurs utilisent HTTP/2.",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "Applications exclues du filtrage (leur trafic HTTP/3 n’est pas filtré non plus) : {}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuard n’est pas en cours d’exécution – rien n’est filtré.",
    "could not remove the previous certificate":
        "impossible de supprimer le certificat précédent",
    "HTTP/3 state unknown":
        "État HTTP/3 inconnu",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "Une règle de pare-feu rejette le trafic UDP 443 sortant ; QUIC ne peut donc pas être utilisé.",
    "Browser policy disables QUIC: {}":
        "Une stratégie du navigateur désactive QUIC : {}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "Les navigateurs peuvent contourner AdGuard via HTTP/3 (UDP 443).",
    "Checking…":
        "Vérification…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "Impossible de lire proxy.yaml – état HTTP/3 inconnu.",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "Profils de la famille Firefox avec HTTP/3 désactivé : {} sur {}",
    "HTTP/3 (QUIC)":
        "HTTP/3 (QUIC)",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "HTTP/3 est bloqué par AdGuard ; les navigateurs se rabattent sur HTTP/2, qui est filtré.",
    "HTTP/3 is filtered by AdGuard.":
        "HTTP/3 est filtré par AdGuard.",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "HTTP/3 désactivé dans les profils Firefox – redémarrez le navigateur.",
    "HTTPS filtering is off – nothing is filtered.":
        "Le filtrage HTTPS est désactivé – rien n’est filtré.",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "Mode proxy : {} – seul le trafic qui passe par le proxy est filtré, et les navigateurs n’y font pas passer QUIC.",
    "unknown":
        "inconnu",
    "AdGuard's certificate was not found. Generate it first.":
        "Certificat d’AdGuard introuvable. Générez-le d’abord.",
    "Certificate could not be installed in any browser.":
        "Le certificat n’a pu être installé dans aucun navigateur.",
    "Certificate installed for {} of {} stores.":
        "Certificat installé dans les magasins de certificats : {} sur {}.",
    "Chromium-based browsers":
        "Navigateurs basés sur Chromium",
    "No browser certificate stores found.":
        "Aucun magasin de certificats de navigateur trouvé.",
    "Restart your browsers for the certificate to take effect.":
        "Redémarrez vos navigateurs pour que le certificat soit pris en compte.",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "N’utilisez pas sudo/pkexec – l’installation se fait dans vos propres profils de navigateur",
    "certificate not found after import":
        "certificat introuvable après l’import",
    "certutil not found – install the 'nss' package":
        "certutil introuvable – installez le paquet « nss »",
    "not found":
        "introuvable",
    "Could not read the filter list (unexpected CLI output).":
        "Impossible de lire la liste des filtres (sortie CLI inattendue).",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "Aucune zone de notification trouvée. AdGuard Tray s’exécute sans icône — activez une zone de notification/AppIndicator dans votre panneau.",
    "URL must start with http:// or https://":
        "L’URL doit commencer par http:// ou https://",
    "adguard-cli path does not exist or is not executable.":
        "Le chemin d’adguard-cli n’existe pas ou n’est pas exécutable.",
    "That binary does not identify as adguard-cli. Save anyway?":
        "Ce binaire ne s’identifie pas comme adguard-cli. Enregistrer quand même ?",
    "Update channel":                   "Canal de mise à jour",
    "Switching update channel to {}…":  "Passage au canal de mise à jour {}…",
    "Update channel set to {}":         "Canal de mise à jour défini sur {}",
    "Could not set update channel":     "Impossible de définir le canal de mise à jour",
    "Invalid channel: {}":              "Canal non valide : {}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        "Pas encore de journal d’accès ({}). AdGuard le crée dès qu’il a filtré du trafic ; lorsqu’il s’exécute en tant que service système, le journal appartient à root et n’est pas lisible ici.",
    'Cannot read the access log ({}): {}':
        "Impossible de lire le journal d’accès ({}) : {}",
    'Blocked':
        "Bloqué",
    'Blocked only':
        "Bloqués uniquement",
    "Refresh":
        "Actualiser",
    'Allow selected domain':
        "Autoriser le domaine sélectionné",
    'Block selected domain':
        "Bloquer le domaine sélectionné",
    'Activity':
        "Activité",
    'Time':
        "Heure",
    'Domain':
        "Domaine",
    'Result':
        "Résultat",
    'Rule':
        "Règle",
    'Size':
        "Taille",
    'Count':
        "Nombre",
    'Could not read the access log.':
        "Impossible de lire le journal d’accès.",
    '{} lines not understood':
        "Lignes non comprises : {}",
    'Not a valid domain: {}':
        "Domaine non valide : {}",
    'Source: {}':
        "Source : {}",
    'Allowed':
        "Autorisé",
    'Added rule: {}':
        "Règle ajoutée : {}",
    'Requests per hour, {} to {} · busiest hour: {}':
        "Requêtes par heure, de {} à {} · heure la plus chargée : {}",
    'Last 24 hours':
        "24 dernières heures",
    'Last 7 days':
        "7 derniers jours",
    'Requests':
        "Requêtes",
    'Traffic':
        "Trafic",

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        "La version {} est disponible (version installée : {}).",
    'Application update':
        "Mise à jour de l’application",
    'Check for update':
        "Rechercher une mise à jour",
    'Install update':
        "Installer la mise à jour",
    'Installing update…':
        "Installation de la mise à jour…",
    'Restart now':
        "Redémarrer maintenant",
    'Later':
        "Plus tard",
    'You are running the latest version ({}).':
        "Vous utilisez la dernière version ({}).",
    'Installation not recognised':
        "Type d’installation non reconnu",
    'Could not check for updates.':
        "Impossible de rechercher les mises à jour.",
    'Update with: {}':
        "Mettre à jour avec : {}",
    'Installed with the AUR package {}':
        "Installé via le paquet AUR {}",
    'Installed in {}':
        "Installé dans : {}",
    'Running from a source checkout':
        "Exécuté depuis une copie des sources",
    'Version {} installed. Restart adguard-tray to use it.':
        "Version {} installée. Redémarrez adguard-tray pour l’utiliser.",
    'Unexpected answer from GitHub: {}':
        "Réponse inattendue de GitHub : {}",
    'Download failed: {}':
        "Échec du téléchargement : {}",
    'Could not unpack the download: {}':
        "Impossible de décompresser le téléchargement : {}",
    'This installation is managed elsewhere: {}':
        "Cette installation est gérée ailleurs : {}",
    'No permission to write to {}':
        "Pas de droit d’écriture dans : {}",
    'GitHub returned {}.':
        "GitHub a renvoyé {}.",
    'No connection to GitHub: {}':
        "Pas de connexion à GitHub : {}",
    'The download does not contain adguard-tray.':
        "Le téléchargement ne contient pas adguard-tray.",
    'The download says version {} instead of {} – aborted.':
        "Le téléchargement indique la version {} au lieu de {} – opération annulée.",
    'GitHub is rate limiting this address. Try again later.':
        "GitHub limite le nombre de requêtes depuis cette adresse. Réessayez plus tard.",
    'The download is larger than expected – aborted.':
        "Le téléchargement est plus volumineux que prévu – opération annulée.",
    'Update failed: {}':
        "Échec de la mise à jour : {}",
    'The archive contains unexpected paths – aborted.':
        "L’archive contient des chemins inattendus – opération annulée.",
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        "Échec de la mise à jour et impossible de restaurer l’ancienne version. Restaurez-la depuis {} ou réinstallez avec : {}",
    'Last 30 days':
        "30 derniers jours",
    'All time':
        "Toute la période",
    'Modified':
        "Modifié",
    'Rules':
        "Règles",
    'Showing {} – show all':
        "Affichage : {} – tout afficher",
    'history {}':
        "historique {}",
    'Filter list ID: {}':
        "ID de la liste de filtres : {}",
    'App':
        "Application",
    'Protocol':
        "Protocole",
    'Type':
        "Type",
    'Reset history':
        "Réinitialiser l’historique",
    'Delete the stored history and read the log again.':
        "Supprime l’historique enregistré et relit le journal.",
    'Delete the stored history? Only what the log still holds can be read back.':
        "Supprimer l’historique enregistré ? Seul ce que le journal contient encore pourra être relu.",
    'History is not being updated: {}':
        "L’historique n’est pas mis à jour : {}",

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "1 modification non enregistrée des paramètres d’AdGuard",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "Un filtre de confiance peut exécuter des scripts dans les pages que vous visitez. Ne faites confiance qu’aux listes provenant de sources que vous connaissez.",
    "About":
        "À propos",
    "Actions for the selected filter":
        "Actions pour le filtre sélectionné",
    "Ad blocking":
        "Blocage des publicités",
    "Ad blocking is off, so the filter lists below have no effect.":
        "Le blocage des publicités est désactivé, les listes de filtres ci-dessous sont donc sans effet.",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLI télécharge et installe sa dernière version.",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "AdGuard CLI oublie la licence sur cet ordinateur. Vous devrez la réactiver.",
    "AdGuard CLI logs":
        "Journaux d’AdGuard CLI",
    "AdGuard CLI update finished.":
        "Mise à jour d’AdGuard CLI terminée.",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "Journal d’AdGuard Tray",
    "AdGuard doesn't filter these websites.":
        "AdGuard ne filtre pas ces sites web.",
    "AdGuard is filtering this computer's traffic.":
        "AdGuard filtre le trafic de cet ordinateur.",
    "AdGuard restarts to load the new lists.":
        "AdGuard redémarre pour charger les nouvelles listes.",
    "AdGuard's reply did not say whether it is running.":
        "La réponse d’AdGuard n’indique pas s’il est en cours d’exécution.",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "Fichier de paramètres d’AdGuard introuvable ({}). Lancez adguard-cli une fois pour le créer.",
    "Add DNS filter by ID":
        "Ajouter un filtre DNS par ID",
    "Add DNS filter from URL":
        "Ajouter un filtre DNS depuis une URL",
    "Add filter":
        "Ajouter un filtre",
    "Add filter by ID":
        "Ajouter un filtre par ID",
    "Add filter from URL":
        "Ajouter un filtre depuis une URL",
    "Add rule":
        "Ajouter une règle",
    "Add to browsers":
        "Ajouter aux navigateurs",
    "Add userscript":
        "Ajouter un script utilisateur",
    "Add userscript…":
        "Ajouter un script utilisateur…",
    "Add website":
        "Ajouter un site web",
    "Add…":
        "Ajouter…",
    "Advanced":
        "Avancé",
    "All available":
        "Tous les filtres",
    "Allow {}":
        "Autoriser {}",
    "Also adds the certificate to this Firefox profile.":
        "Ajoute également le certificat à ce profil Firefox.",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "Également lors des redémarrages et en cas d’erreur. Nécessite notify-send (libnotify) ou un service de notification actif, comme dunst, mako ou celui de KDE.",
    "Appearance":
        "Apparence",
    "Applies after AdGuard Tray restarts.":
        "Prend effet au prochain redémarrage d’AdGuard Tray.",
    "Apply":
        "Appliquer",
    "Apply your changes to AdGuard's settings before closing?":
        "Appliquer vos modifications des paramètres d’AdGuard avant de fermer ?",
    "Applying them restarts AdGuard if protection is on.":
        "Leur application redémarre AdGuard si la protection est activée.",
    "Asks GitHub for the newest release.":
        "Demande à GitHub la version la plus récente.",
    "At a glance":
        "En un coup d’œil",
    "Automatic":
        "Automatique",
    "Automatic – filter all apps":
        "Automatique – filtrer toutes les applications",
    "Benchmark":
        "Test de performances",
    "Beta":
        "Bêta",
    "Block ECH in DNS records":
        "Bloquer ECH dans les enregistrements DNS",
    "Block domains before a connection is made.":
        "Bloque les domaines avant l’établissement de la connexion.",
    "Block {}":
        "Bloquer {}",
    "Blocked (24 h)":
        "Bloqué (24 h)",
    "Browser list ({})":
        "Liste de navigateurs ({})",
    "By ID or name…":
        "Par ID ou nom…",
    "Certificate":
        "Certificat",
    "Certificate checks":
        "Vérifications des certificats",
    "Changes are collected in the bar at the bottom and applied together.":
        "Les modifications sont regroupées dans la barre du bas et appliquées ensemble.",
    "Check again":
        "Vérifier à nouveau",
    "Check every":
        "Vérifier toutes les",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "Les navigateurs basés sur Chromium et sur Firefox ont leur propre magasin de certificats.",
    "Close":
        "Fermer",
    "Controls which AdGuard CLI build “{}” installs.":
        "Détermine la version d’AdGuard CLI installée par « {} ».",
    "Could not add the rule.":
        "Impossible d’ajouter la règle.",
    "Could not open {}":
        "Impossible d’ouvrir {}",
    "Could not read {}":
        "Impossible de lire {}",
    "Could not refresh. Showing data from {}.":
        "Impossible d’actualiser. Affichage des données de {}.",
    "Could not reset the history.":
        "Impossible de réinitialiser l’historique.",
    "Could not restart AdGuard.":
        "Impossible de redémarrer AdGuard.",
    "Could not start protection.":
        "Impossible d’activer la protection.",
    "Could not stop protection.":
        "Impossible de désactiver la protection.",
    "Create":
        "Créer",
    "Create certificate":
        "Créer le certificat",
    "Custom":
        "Personnalisé",
    "DNS filter lists":
        "Listes de filtres DNS",
    "DNS filtering":
        "Filtrage DNS",
    "DNS filtering is off, so these lists have no effect.":
        "Le filtrage DNS est désactivé, ces listes sont donc sans effet.",
    "DNS servers":
        "Serveurs DNS",
    "Dark":
        "Sombre",
    "Default":
        "Par défaut",
    "Details":
        "Détails",
    "Discard":
        "Abandonner",
    "Don't filter":
        "Ne pas filtrer",
    "Don't trust":
        "Retirer la confiance",
    "Downloads and installs the newest AdGuard CLI build.":
        "Télécharge et installe la dernière version d’AdGuard CLI.",
    "Duration":
        "Durée",
    "Export…":
        "Exporter…",
    "Filter everything":
        "Tout filtrer",
    "Filter in place":
        "Filtrer sur place",
    "Filtering":
        "Filtrage",
    "Follow system":
        "Suivre le système",
    "From URL…":
        "Depuis une URL…",
    "Go to updates":
        "Aller aux mises à jour",
    "HTTP proxy: {}":
        "Proxy HTTP : {}",
    "HTTPS filtering":
        "Filtrage HTTPS",
    "How much detail AdGuard Tray writes to its own log.":
        "Quantité de détails consignés par AdGuard Tray dans son propre journal.",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "Si un site ne se charge pas, désactivez d’abord le filtrage HTTP/3. Les autres vérifications protègent tous les sites – ne les désactivez que si cela n’a pas suffi.",
    "Included":
        "Inclus",
    "Installed":
        "Installés",
    "License":
        "Licence",
    "Light":
        "Clair",
    "Logs":
        "Journaux",
    "MIT license":
        "Licence MIT",
    "Maintenance":
        "Maintenance",
    "Manual proxy":
        "Proxy manuel",
    "Manual – only apps set to use the proxy":
        "Manuel – seules les applications configurées pour le proxy",
    "More":
        "Plus",
    "Move down":
        "Descendre",
    "Move up":
        "Monter",
    "Network":
        "Réseau",
    "Nightly":
        "Nightly",
    "No requests yet – AdGuard logs requests while protection is on.":
        "Aucune requête pour l’instant – AdGuard enregistre les requêtes tant que la protection est activée.",
    "Not added":
        "Non ajouté",
    "Nothing matches your search.":
        "Aucun résultat pour votre recherche.",
    "Notify me when protection turns on or off":
        "M’avertir quand la protection est activée ou désactivée",
    "Off":
        "Désactivé",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "Ne concerne que les navigateurs qui utilisent DoH ou DoT. « Désactivé » leur permet de contourner le filtrage DNS d’AdGuard.",
    "Open AdGuard Tray":
        "Ouvrir AdGuard Tray",
    "Open exceptions":
        "Ouvrir les exceptions",
    "Open folder":
        "Ouvrir le dossier",
    "Open release page":
        "Ouvrir la page de la version",
    "Pages":
        "Pages",
    "Performance":
        "Performances",
    "Protection":
        "Protection",
    "Protection started.":
        "Protection activée.",
    "Protection stopped.":
        "Protection désactivée.",
    "Proxy mode":
        "Mode proxy",
    "Redirect to AdGuard's DNS":
        "Rediriger vers le DNS d’AdGuard",
    "Refresh this page (F5)":
        "Actualiser cette page (F5)",
    "Release (stable)":
        "Release (stable)",
    "Remove rule":
        "Supprimer la règle",
    "Remove “{}”?":
        "Supprimer « {} » ?",
    "Remove…":
        "Supprimer…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "Remplacer les paramètres actuels d’AdGuard par ceux du fichier {} ?\n\nAdGuard redémarre pour les appliquer.",
    "Reset history…":
        "Réinitialiser l’historique…",
    "Reset…":
        "Réinitialiser…",
    "Restart AdGuard":
        "Redémarrer AdGuard",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "Les règles ne s’appliquent qu’en mode proxy automatique. La première règle correspondante l’emporte : gardez donc « * » en dernier.",
    "Safe Browsing":
        "Navigation sécurisée",
    "Save anyway":
        "Enregistrer quand même",
    "Saved. AdGuard restarts to apply the change.":
        "Enregistré. AdGuard redémarre pour appliquer la modification.",
    "Saved. Applies after AdGuard Tray restarts.":
        "Enregistré. La modification prendra effet au prochain redémarrage d’AdGuard Tray.",
    "Saved. The change applies when protection is turned on.":
        "Enregistré. La modification s’appliquera à l’activation de la protection.",
    "Secure DNS and ECH":
        "DNS sécurisé et ECH",
    "Secure DNS filtering":
        "Filtrage du DNS sécurisé",
    "Set the path in Settings":
        "Définir le chemin dans « Paramètres »",
    "Settings":
        "Paramètres",
    "Show":
        "Afficher",
    "Show recent entries":
        "Afficher les entrées récentes",
    "Skip HTTPS filtering":
        "Ignorer le filtrage HTTPS",
    "Some counts could not be loaded.":
        "Impossible de charger certains compteurs.",
    "Source code":
        "Code source",
    "Start AdGuard Tray when I log in":
        "Lancer AdGuard Tray à l’ouverture de session",
    "Startup":
        "Démarrage",
    "Status checks":
        "Vérifications de l’état",
    "Stealth mode":
        "Mode furtif",
    "System":
        "Système",
    "The new lists load when protection is turned on.":
        "Les nouvelles listes seront chargées à l’activation de la protection.",
    "Theme":
        "Thème",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "Cette action désactive le filtrage HTTP/3, les vérifications OCSP, Certificate Transparency et le filtrage du DNS sécurisé. Les certificats révoqués ou émis à tort passent alors inaperçus, et les navigateurs peuvent résoudre les noms sans passer par le filtre DNS d’AdGuard.",
    "Time range":
        "Période",
    "To keep it but stop using it, switch it off instead.":
        "Pour le conserver sans l’utiliser, désactivez-le plutôt.",
    "Top lists":
        "Classements",
    "Trust":
        "Faire confiance",
    "Trust “{}”?":
        "Faire confiance à « {} » ?",
    "Trust…":
        "Faire confiance…",
    "Turn off all strict checks…":
        "Désactiver toutes les vérifications strictes…",
    "Undo":
        "Annuler",
    "Unknown":
        "Inconnu",
    "Unsaved changes":
        "Modifications non enregistrées",
    "Update AdGuard CLI…":
        "Mettre à jour AdGuard CLI…",
    "Update channel: {}":
        "Canal de mise à jour : {}",
    "Updated {}":
        "Mis à jour : {}",
    "Updates":
        "Mises à jour",
    "Used in manual mode only.":
        "Utilisé uniquement en mode manuel.",
    "Userscripts update together with filters.":
        "Les scripts utilisateur sont mis à jour en même temps que les filtres.",
    "Uses XDG autostart (~/.config/autostart).":
        "Utilise le démarrage automatique XDG (~/.config/autostart).",
    "Waiting for authorization…":
        "En attente d’autorisation…",
    "Website exceptions":
        "Exceptions de sites web",
    "Websites":
        "Sites web",
    "example.com or a link":
        "example.com ou un lien",
    "expires {}":
        "expiration : {}",
    "of {} requests in the last 24 hours":
        "Total des requêtes (24 h) : {}",
    "{} of {} DNS filters on":
        "Filtres DNS actifs : {} sur {}",
    "{} of {} filters on":
        "Filtres actifs : {} sur {}",
    "{} of {} on":
        "Actifs : {} sur {}",
    "{} unsaved changes to AdGuard's settings":
        "Modifications non enregistrées des paramètres d’AdGuard : {}",
    "“Follow system” uses your desktop's light or dark setting.":
        "« Suivre le système » utilise le réglage clair ou sombre de votre bureau.",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "Active",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "Le certificat d’AdGuard sera ajouté à chaque profil de navigateur trouvé sur ce système.\n\nAdGuard pourra ainsi inspecter le trafic HTTPS de ces navigateurs. Fermez d’abord vos navigateurs – ils lisent le magasin de certificats au démarrage.",
    "Allow":
        "Autoriser",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "Appliquez ou abandonnez d’abord vos modifications des paramètres d’AdGuard, puis redémarrez.",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "Automatique : AdGuard redirige vers lui-même tout le trafic des applications via iptables. Manuel : AdGuard écoute uniquement sur les ports SOCKS5 et HTTP ci-dessous.",
    "Block":
        "Bloquer",
    "Browser API blocking":
        "Blocage des API du navigateur",
    "CRLite":
        "CRLite",
    "Cancel":
        "Annuler",
    "Computers":
        "Ordinateurs",
    "Could not change the autostart entry.":
        "Impossible de modifier l’entrée de démarrage automatique.",
    "Could not export the logs.":
        "Impossible d’exporter les journaux.",
    "Could not export the settings.":
        "Impossible d’exporter les paramètres.",
    "Could not reset the license.":
        "Impossible de réinitialiser la licence.",
    "Could not retrieve license info.":
        "Impossible de récupérer les informations de licence.",
    "Could not run the benchmark.":
        "Impossible de lancer le test de performances.",
    "Could not save the settings.":
        "Impossible d’enregistrer les paramètres.",
    "Could not set the update channel.":
        "Impossible de définir le canal de mise à jour.",
    "Could not update AdGuard CLI.":
        "Impossible de mettre à jour AdGuard CLI.",
    "Could not update the filters.":
        "Impossible de mettre à jour les filtres.",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "Serveur DNS amont.\n'default' = DNS du système.\nExemples : 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com",
    "Expiration date":
        "Date d’expiration",
    "Expires":
        "Expire",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "HTTP/3 réactivé dans les profils Firefox – redémarrez le navigateur.",
    "License key":
        "Clé de licence",
    "License type":
        "Type de licence",
    "Manual":
        "Manuel",
    "No exceptions.":
        "Aucune exception.",
    "OK":
        "OK",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "Activé : AdGuard filtre lui-même HTTP/3 (QUIC) – expérimental, et certains\nnavigateurs refusent de toute façon HTTP/3 via un certificat installé par l’utilisateur.\nDésactivé : AdGuard bloque plutôt QUIC, et les navigateurs se rabattent sur HTTP/2,\nqui est filtré de manière fiable.\nDans les deux cas, cela ne s’applique qu’en mode automatique – en mode manuel,\nle trafic HTTP/3 n’atteint jamais AdGuard.",
    "Owner":
        "Titulaire",
    "Personal":
        "Personnelle",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "Mode proxy : {} – le port UDP 443 est redirigé vers AdGuard.",
    "Save adguard-cli path":
        "Enregistrer le chemin d’adguard-cli",
    "Search domains or rules…":
        "Rechercher des domaines ou des règles…",
    "Settings file":
        "Fichier de paramètres",
    "Status":
        "État",
    "Trial":
        "Essai",
    "Turn HTTP/3 back on in Firefox profiles":
        "Réactiver HTTP/3 dans les profils Firefox",
    "Turn off":
        "Désactiver",
    "Turn off HTTP/3 in Firefox profiles":
        "Désactiver HTTP/3 dans les profils Firefox",
    "Turn off HTTP/3 in Firefox profiles…":
        "Désactiver HTTP/3 dans les profils Firefox…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "Désactiver HTTP/3 dans les profils de la famille Firefox (nombre : {}) ?\n\nLeur trafic passera alors par HTTP/2, qu’AdGuard peut filtrer. Redémarrez ensuite le navigateur.",
    "Turn off all strict checks":
        "Désactiver toutes les vérifications strictes",
    "Unavailable until AdGuard CLI reports its current channel.":
        "Indisponible tant qu’AdGuard CLI n’a pas indiqué son canal actuel.",
    "Update AdGuard CLI":
        "Mettre à jour AdGuard CLI",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "Utilisé uniquement en mode automatique. Plages (80:5221,5300:49151) ou ports individuels (80,443,8080).",
    "{} of {}":
        "{} sur {}",
    "{} of {} userscripts on":
        "Scripts utilisateur actifs : {} sur {}",
    "{}% blocked":
        "{} % bloqué",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "Nuisances",
    "General":
        "Général",
    "Language-specific":
        "Spécifique à une langue",
    "Security":
        "Sécurité",
    "Social widgets":
        "Widgets sociaux",
    "Expired":
        "Expirée",
    "Autostart on login":
        "Démarrage automatique à la connexion",
    "Add app rule":
        "Ajouter une règle d’application",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "Les caractères génériques sont acceptés, p. ex. *steam* ou *EasyAntiCheat*.",
    "There is already a rule for '{}'.":
        "Une règle existe déjà pour « {} ».",
    "AdGuard settings":
        "Paramètres d’AdGuard",
    "Ads and trackers are not blocked until you enable protection.":
        "Les publicités et les traqueurs ne sont pas bloqués tant que vous n’activez pas la protection.",
    "Could not import the settings.":
        "Impossible d’importer les paramètres.",
    "Disable protection":
        "Désactiver la protection",
    "Enable protection":
        "Activer la protection",
    "Export and import":
        "Export et import",
    "Features":
        "Fonctionnalités",
    "Import settings":
        "Importer les paramètres",
    "Import settings from…":
        "Importer les paramètres depuis…",
    "Import settings…":
        "Importer les paramètres…",
    "Import…":
        "Importer…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "Enregistrer les filtres, les règles et la configuration dans un fichier zip, ou les charger depuis un tel fichier.",
    "Update":
        "Mettre à jour",
    "Version":
        "Version",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "{} n’est pas un export de paramètres. Choisissez un fichier enregistré avec « Exporter » sous « Paramètres d’AdGuard ».",
}
