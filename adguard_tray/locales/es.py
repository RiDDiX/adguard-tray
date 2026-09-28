"""Spanish."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "Idioma",
    "English":                           "Inglés",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "Activo – Protección en ejecución",
    "Inactive – Protection stopped":        "Inactivo – Protección desactivada",
    "Error retrieving status":              "Error al obtener el estado",
    "adguard-cli not found":                "No se encontró adguard-cli",
    "Unknown status":                       "Estado desconocido",
    "Checking status…":                     "Comprobando estado…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "Reiniciar",
    "Filters":                              "Filtros",
    "Loading…":                             "Cargando…",
    "Manage filters…":                      "Gestionar filtros…",
    "No userscripts installed":             "No hay userscripts instalados",
    "Manage userscripts…":                  "Gestionar userscripts…",
    "Quit":                                 "Salir",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "activo",
    "inactive":                             "inactivo",
    "System-wide filtering: {}":            "Filtrado en todo el sistema: {}",
    "Error: {}":                            "Error: {}",
    "AdGuard Tray – Error":                 "AdGuard Tray – Error",
    "AdGuard is now active – protection running.":
        "AdGuard ya está activo – protección en ejecución.",
    "AdGuard has been stopped.":
        "AdGuard se ha detenido.",
    "Could not retrieve status.":
        "No se pudo obtener el estado.",
    "Command failed":                       "Error al ejecutar el comando",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " segundos",
    "How often adguard-cli status is checked automatically.":
        "Frecuencia con la que se comprueba automáticamente el estado de adguard-cli.",
    "Log level:":                           "Nivel de registro:",
    "adguard-cli path:":                    "Ruta de adguard-cli:",
    "auto-detect via PATH":                 "detectar automáticamente mediante PATH",
    "Browse…":                              "Examinar…",
    "Select adguard-cli binary":            "Seleccionar el ejecutable de adguard-cli",
    "Notifications":                        "Notificaciones",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "Actualizar filtros",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "Actualiza todos los filtros, filtros DNS, userscripts,\nSafebrowsingV2, CRLite y busca actualizaciones de la app.",
    "No filters found.":                    "No se encontraron filtros.",
    "Updating filters… (can take up to 2 minutes)":
        "Actualizando filtros… (puede tardar hasta 2 minutos)",
    "Update completed.":                    "Actualización completada.",
    "Update failed.":                       "Error al actualizar.",
    "Installing: {}":                       "Instalando: {}",
    "Filter installed.":                    "Filtro instalado.",
    "Remove":                               "Eliminar",
    "Remove filter":                        "Eliminar filtro",
    "Filter {} removed.":                   "Filtro {} eliminado.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        "Instala un userscript desde una URL .js directa",
    "No userscripts installed.":            "No hay userscripts instalados.",
    "Userscript URL (direct .js URL):":     "URL del userscript (URL .js directa):",
    "Userscript installed.":                "Userscript instalado.",
    'Remove "{}"':                          "Eliminar «{}»",
    "Remove userscript":                    "Eliminar userscript",
    "'{}' removed.":                        "«{}» eliminado.",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "No se encontró adguard-cli.\nInstálalo con el script oficial o desde AUR:\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "Error desconocido al obtener el estado",
    "AdGuard {} ok":                        "AdGuard {}: correcto",
    "AdGuard via systemctl {} ok":          "AdGuard mediante systemctl {}: correcto",
    "'{}' failed – insufficient privileges?":
        "Error al ejecutar «{}» – ¿privilegios insuficientes?",
    "Could not retrieve filter list":
        "No se pudo obtener la lista de filtros",
    "Filter {} enabled":                    "Filtro {} activado",
    "Could not enable filter {}":           "No se pudo activar el filtro {}",
    "Filter {} disabled":                   "Filtro {} desactivado",
    "Could not disable filter {}":
        "No se pudo desactivar el filtro {}",
    "Filter installed":                     "Filtro instalado",
    "Installation failed":                  "Error al instalar",
    "Filter {} removed":                    "Filtro {} eliminado",
    "Could not remove filter {}":
        "No se pudo eliminar el filtro {}",
    "Filters updated":                      "Filtros actualizados",
    "Update failed":                        "Error al actualizar",
    "Could not retrieve userscript list":
        "No se pudo obtener la lista de userscripts",
    "Userscript '{}' enabled":              "Userscript «{}» activado",
    "Could not enable userscript '{}'":
        "No se pudo activar el userscript «{}»",
    "Userscript '{}' disabled":             "Userscript «{}» desactivado",
    "Could not disable userscript '{}'":
        "No se pudo desactivar el userscript «{}»",
    "Userscript '{}' removed":              "Userscript «{}» eliminado",
    "Could not remove userscript '{}'":
        "No se pudo eliminar el userscript «{}»",
    "Userscript installed":                 "Userscript instalado",
    "Other":                                "Otros",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "Buscar filtros…",
    "Search userscripts…":              "Buscar userscripts…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "No se pudo cargar proxy.yaml.\nRuta: {}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "Apps",
    "Mode:":                            "Modo:",
    "Filtered ports:":                  "Puertos filtrados:",
    "SOCKS5 port:":                     "Puerto SOCKS5:",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "Puerto del proxy SOCKS5 para el modo manual.\nEstablécelo en -1 para desactivarlo.",
    "HTTP port:":                       "Puerto HTTP:",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "Puerto del proxy HTTP para el modo manual.\nEstablécelo en -1 para desactivarlo.",
    "Listen address:":                  "Dirección de escucha:",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "Dirección en la que escucha el proxy.\n127.0.0.1 = solo local. 0.0.0.0 = todas las interfaces (requiere autenticación).",
    "Worker threads:":                  "Hilos de trabajo:",
    "Number of proxy worker threads.":  "Número de hilos de trabajo del proxy.",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "Descifra y filtra el tráfico HTTPS.\nNecesario para bloquear anuncios en sitios https.\nRequiere un certificado raíz de confianza instalado en el sistema.",
    "Enable TLS 1.3":                   "Activar TLS 1.3",
    "Enable TLS 1.3 support for filtered connections.":
        "Activa la compatibilidad con TLS 1.3 en las conexiones filtradas.",
    "Filter HTTP/3 (QUIC) – experimental":
        "Filtrar HTTP/3 (QUIC) – experimental",
    "OCSP certificate checks":          "Comprobaciones OCSP de certificados",
    "Enforce Certificate Transparency": "Exigir Transparencia de certificados",
    "Filter EV certificate sites":      "Filtrar sitios con certificado EV",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "De forma predeterminada, los sitios con certificados de Validación Extendida no se filtran.\nActiva esta opción para filtrarlos también (p. ej., sitios de banca).",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "Activa ECH para una mayor privacidad.\nRequiere tener activado el filtrado DNS.",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "Filtra las consultas DNS para bloquear anuncios y rastreadores a nivel DNS.\nUsa un proxy DNS local con servidores upstream configurables.",
    "Upstream:":                        "Upstream:",
    "Fallbacks:":                       "Respaldo:",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "Servidores DNS de respaldo (se usan cuando falla el upstream principal).\n'default' = DNS del sistema. Lista separada por espacios.\nEjemplo: default 1.1.1.1",
    "Bootstraps:":                      "Bootstrap:",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "DNS de arranque (bootstrap) para resolver los nombres de host de los servidores upstream.\n'default' = IP de los servidores DNS del sistema. Solo se permiten direcciones IP.\nEjemplo: default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "Elimina el parámetro ECH de los registros DNS SVCB/HTTPS.\nActiva esta opción solo para navegadores que no detectan automáticamente el filtrado HTTPS.",
    "Master switch for all tracking protection features below.":
        "Interruptor principal de todas las funciones de protección contra el seguimiento que aparecen debajo.",
    "Cookies":                          "Cookies",
    "Block third-party cookies":        "Bloquear cookies de terceros",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "Borra las cookies de terceros tras un tiempo definido.\nEvita el seguimiento entre sitios.",
    "Lifetime (minutes):":              "Duración (minutos):",
    "0 = block immediately. Default: 180 minutes.":
        "0 = bloquear inmediatamente. Predeterminado: 180 minutos.",
    "Block first-party cookies":        "Bloquear cookies propias",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "Borra todas las cookies (incluidas las propias) tras un tiempo definido.\nAdvertencia: esto cierra tu sesión en todos los sitios.",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = bloquear inmediatamente. Predeterminado: 4320 minutos (3 días).",
    "Privacy":                          "Privacidad",
    "Hide / reduce User-Agent":         "Ocultar o reducir User-Agent",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "Quita los datos identificativos del User-Agent.\nReduce la huella digital del navegador.",
    "Hide search queries in referrer":  "Ocultar consultas de búsqueda en el Referer",
    "Hides your search terms when clicking from a search engine to a website.":
        "Oculta tus términos de búsqueda al hacer clic desde un buscador hacia un sitio web.",
    "Remove referrer from third-party requests":
        "Eliminar Referer de solicitudes de terceros",
    "Prevents third-party sites from knowing which page you came from.":
        "Impide que los sitios de terceros sepan de qué página vienes.",
    "Send Do-Not-Track signal":         "Enviar señal No rastrear (DNT)",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "Envía el encabezado DNT con las solicitudes.\nNota: la mayoría de los sitios lo ignoran, pero algunos lo respetan.",
    "Disable third-party ETag cache":   "Desactivar caché ETag de terceros",
    "Prevents tracking via ETag caching in third-party content.":
        "Evita el seguimiento mediante la caché ETag en contenido de terceros.",
    "Block third-party Authorization header":
        "Bloquear encabezado de autorización de terceros",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "Bloquea el encabezado Authorization en las solicitudes de terceros para evitar el seguimiento.",
    "Remove X-Client-Data header":      "Eliminar encabezado X-Client-Data",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "Elimina el encabezado X-Client-Data que Chrome envía a los servicios de Google.",
    "Block WebRTC":                     "Bloquear WebRTC",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "Evita fugas de IP a través de WebRTC.\nPuede causar fallos en videollamadas y en algunas apps web.",
    "Block Push API":                   "Bloquear API Push",
    "Blocks browser push notifications from websites.":
        "Bloquea las notificaciones push de los sitios web en el navegador.",
    "Block Location API":               "Bloquear API de ubicación",
    "Prevents websites from accessing your GPS location.":
        "Impide que los sitios web accedan a tu ubicación GPS.",
    "Block Flash":                      "Bloquear Flash",
    "Blocks the Flash plugin.":
        "Bloquea el complemento Flash.",
    "Block Java":                       "Bloquear Java",
    "Disables Java plugins. JavaScript remains enabled.":
        "Desactiva los complementos de Java. JavaScript sigue activado.",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "Activar Anti-DPI",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "Modifica los datos de los paquetes salientes para eludir la inspección profunda de paquetes (DPI).\nÚtil en países con censura de internet.",
    "App pattern":
        "Patrón de app",
    "Skip outbound proxy":              "Omitir proxy saliente",
    "Don't route this app's traffic through outbound proxy":
        "No envía el tráfico de esta app a través del proxy saliente",
    "Browser list included from {}":    "Lista de navegadores incluida desde {}",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "La lista de navegadores incluida y la regla comodín (*) no se pueden eliminar.",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "Advierte sobre sitios web maliciosos y de phishing.\nUsa la base de datos de Seguridad de navegación de AdGuard.",
    "Send anonymous statistics":        "Enviar estadísticas anónimas",
    "Send anonymous lookups to AdGuard.":
        "Envía consultas anónimas a AdGuard.",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "Comprobación de revocación de certificados mediante CRLite de Mozilla.\nMás rápida y fiable que las comprobaciones CRL/OCSP tradicionales.",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "Aplica las reglas de filtrado de anuncios a las solicitudes HTTP/HTTPS.",
    "Save failed":                      "Error al guardar",
    "Could not save proxy.yaml:\n{}":   "No se pudo guardar proxy.yaml:\n{}",
    "Restarting AdGuard…":              "Reiniciando AdGuard…",
    "AdGuard restarted.":               "AdGuard reiniciado.",
    "Restart failed: {}":               "Error al reiniciar: {}",
    "Unknown error":                    "Error desconocido",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "Añadir",
    "Search exceptions…":               "Buscar excepciones…",
    "1 exception":                      "1 excepción",
    "{} exceptions":                    "Excepciones: {}",
    "'{}' is not a valid domain or IP address.":
        "«{}» no es un dominio ni una dirección IP válidos.",
    "'{}' is already in the list.":     "«{}» ya está en la lista.",
    "Could not save exceptions:\n{}":
        "No se pudieron guardar las excepciones:\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "Resumen",
    "Userscripts":                      "Userscripts",
    "Exceptions":                       "Excepciones",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "Restablecer licencia",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "Genera un certificado raíz de CA para el filtrado HTTPS. El certificado debe estar instalado y ser de confianza en tu sistema.",
    "Checking for updates…":            "Buscando actualizaciones…",
    "Firefox profile:":                 "Perfil de Firefox:",
    "(optional) e.g. abcd1234.MyProfile":
        "(opcional) p. ej., abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "Escribe el ID o el nombre del filtro:",
    "Filter added.":                    "Filtro añadido.",
    "Rename…":                          "Cambiar nombre…",
    "Rename filter":                    "Cambiar nombre del filtro",
    "New title:":                       "Nuevo título:",
    "Filter renamed.":                  "Nombre del filtro cambiado.",
    "Filter trust updated.":            "Confianza del filtro actualizada.",
    "Filter URL:":                      "URL del filtro:",
    "Title:":                           "Título:",
    "(optional)":                       "(opcional)",
    "Trusted filter":                   "Filtro de confianza",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "Buscar filtros DNS…",
    "No DNS filters found.":            "No se encontraron filtros DNS.",
    "DNS filter installed.":            "Filtro DNS instalado.",
    "DNS filter added.":                "Filtro DNS añadido.",
    "Remove DNS filter":                "Eliminar filtro DNS",
    "DNS filter {} removed.":           "Filtro DNS {} eliminado.",
    "Rename DNS filter":                "Cambiar nombre del filtro DNS",
    "DNS filter renamed.":              "Nombre del filtro DNS cambiado.",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "Exportar registros…",
    "Export AdGuard CLI logs to a zip file":
        "Exporta los registros de AdGuard CLI a un archivo zip",
    "Export settings…":                 "Exportar configuración…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "Ejecuta una prueba de rendimiento de la criptografía y del filtrado HTTPS.",
    "Run benchmark":                    "Ejecutar prueba de rendimiento",
    "Done.":                            "Hecho.",
    "Export logs to…":                  "Exportar registros a…",
    "Export settings to…":              "Exportar configuración a…",
    "Zip files (*.zip);;All files (*)":
        "Archivos zip (*.zip);;Todos los archivos (*)",
    "Log file not found.":              "No se encontró el archivo de registro.",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "No se pudo obtener la lista de filtros DNS",
    "DNS filter {} enabled":            "Filtro DNS {} activado",
    "Could not enable DNS filter {}":   "No se pudo activar el filtro DNS {}",
    "DNS filter {} disabled":           "Filtro DNS {} desactivado",
    "Could not disable DNS filter {}":  "No se pudo desactivar el filtro DNS {}",
    "DNS filter installed":             "Filtro DNS instalado",
    "DNS filter {} removed":            "Filtro DNS {} eliminado",
    "Could not remove DNS filter {}":   "No se pudo eliminar el filtro DNS {}",
    "DNS filter added":                 "Filtro DNS añadido",
    "Could not add DNS filter":         "No se pudo añadir el filtro DNS",
    "DNS filter title updated":         "Título del filtro DNS actualizado",
    "Could not set DNS filter title":   "No se pudo establecer el título del filtro DNS",
    "Filter added":                     "Filtro añadido",
    "Could not add filter":             "No se pudo añadir el filtro",
    "Filter trust updated":             "Confianza del filtro actualizada",
    "Could not update filter trust":    "No se pudo actualizar la confianza del filtro",
    "Filter title updated":             "Título del filtro actualizado",
    "Could not set filter title":       "No se pudo establecer el título del filtro",
    "License reset":                    "Licencia restablecida",
    "Could not reset license":          "No se pudo restablecer la licencia",
    "Could not retrieve license info":  "No se pudo obtener la información de la licencia",
    "Certificate generated":            "Certificado generado",
    "Certificate generation failed":    "Error al generar el certificado",
    "Logs exported":                    "Registros exportados",
    "Log export failed":                "Error al exportar los registros",
    "Settings exported":                "Configuración exportada",
    "Settings export failed":           "Error al exportar la configuración",
    "Settings imported":                "Configuración importada",
    "Settings import failed":           "Error al importar la configuración",
    "Update check completed":           "Búsqueda de actualizaciones completada",
    "Update check failed":              "Error al buscar actualizaciones",
    "Benchmark failed":                 "Error al ejecutar la prueba de rendimiento",
    "AdGuard stopped (forced)":         "AdGuard detenido (forzado)",
    "Could not stop AdGuard – process may still be running":
        "No se pudo detener AdGuard – puede que el proceso siga en ejecución",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "No se encontró adguard-cli en este sistema.\n\nMétodo de instalación recomendado (oficial):\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\nAlternativa (Arch Linux AUR):\n  paru -S adguard-cli-bin\n\nAdGuard Tray se abre igualmente, pero no podrás iniciar ni detener AdGuard hasta que instales adguard-cli.",
    "Copy install command":             "Copiar comando de instalación",
    "Continue":                         "Continuar",
    "AdGuard Tray is already running":  "AdGuard Tray ya se está ejecutando",
    "Only one instance can run at a time. Check your system tray.":
        "Solo puede ejecutarse una instancia a la vez. Revisa la bandeja del sistema.",
    "Authentication cancelled":         "Autenticación cancelada",
    "Authorization failed":             "Error de autorización",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "Comprueba si el certificado de un sitio ha sido revocado (OCSP).\nAdGuard lo comprueba de forma asíncrona y deja pasar la conexión si\nla comprobación tarda, así que rara vez impide cargar un sitio – déjalo activado\na menos que hayas acotado el problema a esta opción.",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "Exige comprobaciones de Transparencia de certificados (política CT de Chrome).\nLos sitios cuyo propio certificado no cumple CT dejan de filtrarse\ny el navegador puede rechazarlos. Los sitios grandes cumplen, así que cambia\nesta opción solo si un sitio muestra un error de certificado.",
    "Sites that don't load":
        "Sitios que no cargan",
    "Turn off HTTP/3 filtering":
        "Desactivar filtrado HTTP/3",
    "No filters installed":
        "No hay filtros instalados",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "Una regla del cortafuegos bloquea HTTP/3; los navegadores usan HTTP/2.",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "Apps excluidas del filtrado (su tráfico HTTP/3 tampoco se filtra): {}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuard no se está ejecutando – no se filtra nada.",
    "could not remove the previous certificate":
        "no se pudo eliminar el certificado anterior",
    "HTTP/3 state unknown":
        "Estado de HTTP/3 desconocido",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "Una regla del cortafuegos rechaza el tráfico UDP 443 saliente, así que no se puede usar QUIC.",
    "Browser policy disables QUIC: {}":
        "QUIC desactivado por política del navegador: {}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "Los navegadores pueden eludir AdGuard mediante HTTP/3 (UDP 443).",
    "Checking…":
        "Comprobando…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "No se pudo leer proxy.yaml – estado de HTTP/3 desconocido.",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "Perfiles de la familia Firefox con HTTP/3 desactivado: {} de {}",
    "HTTP/3 (QUIC)":
        "HTTP/3 (QUIC)",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "AdGuard bloquea HTTP/3; los navegadores recurren a HTTP/2 filtrado.",
    "HTTP/3 is filtered by AdGuard.":
        "AdGuard filtra HTTP/3.",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "HTTP/3 desactivado en los perfiles de Firefox – reinicia el navegador.",
    "HTTPS filtering is off – nothing is filtered.":
        "El filtrado HTTPS está desactivado – no se filtra nada.",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "Modo de proxy: {} – solo se filtra el tráfico que pasa por el proxy, y los navegadores no envían QUIC a través de él.",
    "unknown":
        "desconocido",
    "AdGuard's certificate was not found. Generate it first.":
        "No se encontró el certificado de AdGuard. Genéralo primero.",
    "Certificate could not be installed in any browser.":
        "No se pudo instalar el certificado en ningún navegador.",
    "Certificate installed for {} of {} stores.":
        "Certificado instalado en {} de {} almacenes.",
    "Chromium-based browsers":
        "Navegadores basados en Chromium",
    "No browser certificate stores found.":
        "No se encontraron almacenes de certificados de navegadores.",
    "Restart your browsers for the certificate to take effect.":
        "Reinicia los navegadores para que el certificado surta efecto.",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "Ejecuta esto sin sudo/pkexec – se instala en tus propios perfiles de navegador",
    "certificate not found after import":
        "no se encontró el certificado tras la importación",
    "certutil not found – install the 'nss' package":
        "no se encontró certutil – instala el paquete 'nss'",
    "not found":
        "no encontrado",
    "Could not read the filter list (unexpected CLI output).":
        "No se pudo leer la lista de filtros (salida inesperada de la CLI).",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "No se encontró la bandeja del sistema. AdGuard Tray se ejecuta sin icono — activa una bandeja/AppIndicator en tu panel.",
    "URL must start with http:// or https://":
        "La URL debe empezar por http:// o https://",
    "adguard-cli path does not exist or is not executable.":
        "La ruta de adguard-cli no existe o no es ejecutable.",
    "That binary does not identify as adguard-cli. Save anyway?":
        "Ese ejecutable no se identifica como adguard-cli. ¿Guardar de todos modos?",
    "Update channel":                   "Canal de actualización",
    "Switching update channel to {}…":  "Cambiando el canal de actualización a {}…",
    "Update channel set to {}":         "Canal de actualización cambiado a {}",
    "Could not set update channel":     "No se pudo establecer el canal de actualización",
    "Invalid channel: {}":              "Canal no válido: {}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        "Aún no hay registro de acceso ({}). AdGuard lo escribe en cuanto ha filtrado tráfico; si se ejecuta como servicio del sistema, el registro pertenece a root y no se puede leer aquí.",
    'Cannot read the access log ({}): {}':
        "No se puede leer el registro de acceso ({}): {}",
    'Blocked':
        "Bloqueado",
    'Blocked only':
        "Solo bloqueadas",
    "Refresh":
        "Recargar",
    'Allow selected domain':
        "Permitir el dominio seleccionado",
    'Block selected domain':
        "Bloquear el dominio seleccionado",
    'Activity':
        "Actividad",
    'Time':
        "Hora",
    'Domain':
        "Dominio",
    'Result':
        "Resultado",
    'Rule':
        "Regla",
    'Size':
        "Tamaño",
    'Count':
        "Recuento",
    'Could not read the access log.':
        "No se pudo leer el registro de acceso.",
    '{} lines not understood':
        "Líneas no reconocidas: {}",
    'Not a valid domain: {}':
        "Dominio no válido: {}",
    'Source: {}':
        "Fuente: {}",
    'Allowed':
        "Permitido",
    'Added rule: {}':
        "Regla añadida: {}",
    'Requests per hour, {} to {} · busiest hour: {}':
        "Solicitudes por hora, de {} a {} · hora con más actividad: {}",
    'Last 24 hours':
        "Últimas 24 horas",
    'Last 7 days':
        "Últimos 7 días",
    'Requests':
        "Solicitudes",
    'Traffic':
        "Tráfico",

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        "La versión {} está disponible (tienes la {}).",
    'Application update':
        "Actualización de la aplicación",
    'Check for update':
        "Buscar actualizaciones",
    'Install update':
        "Instalar actualización",
    'Installing update…':
        "Instalando actualización…",
    'Restart now':
        "Reiniciar ahora",
    'Later':
        "Más tarde",
    'You are running the latest version ({}).':
        "Ya tienes la última versión ({}).",
    'Installation not recognised':
        "Instalación no reconocida",
    'Could not check for updates.':
        "No se pudo comprobar si hay actualizaciones.",
    'Update with: {}':
        "Actualizar con: {}",
    'Installed with the AUR package {}':
        "Instalado con el paquete de AUR {}",
    'Installed in {}':
        "Instalado en {}",
    'Running from a source checkout':
        "Se ejecuta desde una copia del código fuente",
    'Version {} installed. Restart adguard-tray to use it.':
        "Versión {} instalada. Reinicia adguard-tray para usarla.",
    'Unexpected answer from GitHub: {}':
        "Respuesta inesperada de GitHub: {}",
    'Download failed: {}':
        "Error al descargar: {}",
    'Could not unpack the download: {}':
        "No se pudo descomprimir la descarga: {}",
    'This installation is managed elsewhere: {}':
        "Esta instalación se gestiona externamente: {}",
    'No permission to write to {}':
        "No hay permiso de escritura en {}",
    'GitHub returned {}.':
        "GitHub devolvió {}.",
    'No connection to GitHub: {}':
        "No hay conexión con GitHub: {}",
    'The download does not contain adguard-tray.':
        "La descarga no contiene adguard-tray.",
    'The download says version {} instead of {} – aborted.':
        "La descarga indica la versión {} en lugar de la {} – operación cancelada.",
    'GitHub is rate limiting this address. Try again later.':
        "GitHub está limitando las solicitudes de esta dirección. Vuelve a intentarlo más tarde.",
    'The download is larger than expected – aborted.':
        "La descarga es más grande de lo esperado – operación cancelada.",
    'Update failed: {}':
        "Error al actualizar: {}",
    'The archive contains unexpected paths – aborted.':
        "El archivo comprimido contiene rutas inesperadas – operación cancelada.",
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        "Error al actualizar: no se pudo restaurar la versión anterior. Restáurala desde {} o reinstala con: {}",
    'Last 30 days':
        "Últimos 30 días",
    'All time':
        "Todo el periodo",
    'Modified':
        "Modificado",
    'Rules':
        "Reglas",
    'Showing {} – show all':
        "Mostrando {} – mostrar todo",
    'history {}':
        "historial: {}",
    'Filter list ID: {}':
        "ID de la lista de filtros: {}",
    'App':
        "App",
    'Protocol':
        "Protocolo",
    'Type':
        "Tipo",
    'Reset history':
        "Restablecer historial",
    'Delete the stored history and read the log again.':
        "Borra el historial guardado y vuelve a leer el registro.",
    'Delete the stored history? Only what the log still holds can be read back.':
        "¿Borrar el historial guardado? Solo se podrá recuperar lo que el registro aún contenga.",
    'History is not being updated: {}':
        "El historial no se está actualizando: {}",

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "1 cambio sin guardar en la configuración de AdGuard",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "Un filtro de confianza puede ejecutar scripts en las páginas que visitas. Confía solo en listas de fuentes que conozcas.",
    "About":
        "Acerca de",
    "Actions for the selected filter":
        "Acciones para el filtro seleccionado",
    "Ad blocking":
        "Bloqueo de anuncios",
    "Ad blocking is off, so the filter lists below have no effect.":
        "El bloqueo de anuncios está desactivado, así que las listas de filtros de abajo no tienen efecto.",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLI descarga e instala su versión más reciente.",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "AdGuard CLI olvidará la licencia en este equipo. Tendrás que volver a activarla.",
    "AdGuard CLI logs":
        "Registros de AdGuard CLI",
    "AdGuard CLI update finished.":
        "Actualización de AdGuard CLI completada.",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "Registro de AdGuard Tray",
    "AdGuard doesn't filter these websites.":
        "AdGuard no filtra estos sitios web.",
    "AdGuard is filtering this computer's traffic.":
        "AdGuard está filtrando el tráfico de este equipo.",
    "AdGuard restarts to load the new lists.":
        "AdGuard se reinicia para cargar las nuevas listas.",
    "AdGuard's reply did not say whether it is running.":
        "La respuesta de AdGuard no indica si está en ejecución.",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "No se encontró el archivo de configuración de AdGuard ({}). Ejecuta adguard-cli una vez para crearlo.",
    "Add DNS filter by ID":
        "Añadir filtro DNS por ID",
    "Add DNS filter from URL":
        "Añadir filtro DNS desde URL",
    "Add filter":
        "Añadir filtro",
    "Add filter by ID":
        "Añadir filtro por ID",
    "Add filter from URL":
        "Añadir filtro desde URL",
    "Add rule":
        "Añadir regla",
    "Add to browsers":
        "Añadir a los navegadores",
    "Add userscript":
        "Añadir userscript",
    "Add userscript…":
        "Añadir userscript…",
    "Add website":
        "Añadir sitio web",
    "Add…":
        "Añadir…",
    "Advanced":
        "Avanzado",
    "All available":
        "Todos los disponibles",
    "Allow {}":
        "Permitir {}",
    "Also adds the certificate to this Firefox profile.":
        "También añade el certificado a este perfil de Firefox.",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "También en reinicios y errores. Requiere notify-send (libnotify) o un servicio de notificaciones en ejecución, como dunst, mako o el de KDE.",
    "Appearance":
        "Apariencia",
    "Applies after AdGuard Tray restarts.":
        "Se aplica tras reiniciar AdGuard Tray.",
    "Apply":
        "Aplicar",
    "Apply your changes to AdGuard's settings before closing?":
        "¿Aplicar los cambios en la configuración de AdGuard antes de cerrar?",
    "Applying them restarts AdGuard if protection is on.":
        "Al aplicarlos, AdGuard se reinicia si la protección está activada.",
    "Asks GitHub for the newest release.":
        "Busca la versión más reciente en GitHub.",
    "At a glance":
        "De un vistazo",
    "Automatic":
        "Automático",
    "Automatic – filter all apps":
        "Automático: filtrar todas las apps",
    "Benchmark":
        "Prueba de rendimiento",
    "Beta":
        "Beta",
    "Block ECH in DNS records":
        "Bloquear ECH en los registros DNS",
    "Block domains before a connection is made.":
        "Bloquea dominios antes de que se establezca una conexión.",
    "Block {}":
        "Bloquear {}",
    "Blocked (24 h)":
        "Bloqueado (24 h)",
    "Browser list ({})":
        "Lista de navegadores ({})",
    "By ID or name…":
        "Por ID o nombre…",
    "Certificate":
        "Certificado",
    "Certificate checks":
        "Comprobaciones de certificados",
    "Changes are collected in the bar at the bottom and applied together.":
        "Los cambios se acumulan en la barra inferior y se aplican a la vez.",
    "Check again":
        "Volver a comprobar",
    "Check every":
        "Comprobar cada",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "Los navegadores basados en Chromium y en Firefox tienen su propio almacén de certificados.",
    "Close":
        "Cerrar",
    "Controls which AdGuard CLI build “{}” installs.":
        "Controla qué versión de AdGuard CLI instala «{}».",
    "Could not add the rule.":
        "No se pudo añadir la regla.",
    "Could not open {}":
        "No se pudo abrir {}",
    "Could not read {}":
        "No se pudo leer {}",
    "Could not refresh. Showing data from {}.":
        "No se pudo recargar. Se muestran los datos de las {}.",
    "Could not reset the history.":
        "No se pudo restablecer el historial.",
    "Could not restart AdGuard.":
        "No se pudo reiniciar AdGuard.",
    "Could not start protection.":
        "No se pudo activar la protección.",
    "Could not stop protection.":
        "No se pudo desactivar la protección.",
    "Create":
        "Crear",
    "Create certificate":
        "Crear certificado",
    "Custom":
        "Personalizado",
    "DNS filter lists":
        "Listas de filtros DNS",
    "DNS filtering":
        "Filtrado DNS",
    "DNS filtering is off, so these lists have no effect.":
        "El filtrado DNS está desactivado, así que estas listas no tienen efecto.",
    "DNS servers":
        "Servidores DNS",
    "Dark":
        "Oscuro",
    "Default":
        "Predeterminado",
    "Details":
        "Detalles",
    "Discard":
        "Descartar",
    "Don't filter":
        "No filtrar",
    "Don't trust":
        "No confiar",
    "Downloads and installs the newest AdGuard CLI build.":
        "Descarga e instala la versión más reciente de AdGuard CLI.",
    "Duration":
        "Duración",
    "Export…":
        "Exportar…",
    "Filter everything":
        "Filtrar todo",
    "Filter in place":
        "Filtrar directamente",
    "Filtering":
        "Filtrado",
    "Follow system":
        "Según el sistema",
    "From URL…":
        "Desde URL…",
    "Go to updates":
        "Ir a Actualizaciones",
    "HTTP proxy: {}":
        "Proxy HTTP: {}",
    "HTTPS filtering":
        "Filtrado HTTPS",
    "How much detail AdGuard Tray writes to its own log.":
        "Cuánto detalle incluye AdGuard Tray en su propio registro.",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "Si un sitio no carga, desactiva primero el filtrado HTTP/3. Las demás comprobaciones protegen todos los sitios – desactívalas solo si eso no resuelve el problema.",
    "Included":
        "Incluida",
    "Installed":
        "Instalados",
    "License":
        "Licencia",
    "Light":
        "Claro",
    "Logs":
        "Registros",
    "MIT license":
        "Licencia MIT",
    "Maintenance":
        "Mantenimiento",
    "Manual proxy":
        "Proxy manual",
    "Manual – only apps set to use the proxy":
        "Manual: solo las apps configuradas para usar el proxy",
    "More":
        "Más",
    "Move down":
        "Bajar",
    "Move up":
        "Subir",
    "Network":
        "Red",
    "Nightly":
        "Nightly",
    "No requests yet – AdGuard logs requests while protection is on.":
        "Aún no hay solicitudes – AdGuard registra las solicitudes mientras la protección está activada.",
    "Not added":
        "No añadido",
    "Nothing matches your search.":
        "No hay resultados para tu búsqueda.",
    "Notify me when protection turns on or off":
        "Notificarme cuando la protección se active o desactive",
    "Off":
        "Desactivado",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "Solo afecta a los navegadores que usan DoH o DoT. Con «Desactivado», pueden eludir el filtrado DNS de AdGuard.",
    "Open AdGuard Tray":
        "Abrir AdGuard Tray",
    "Open exceptions":
        "Abrir excepciones",
    "Open folder":
        "Abrir carpeta",
    "Open release page":
        "Abrir página de la versión",
    "Pages":
        "Páginas",
    "Performance":
        "Rendimiento",
    "Protection":
        "Protección",
    "Protection started.":
        "Protección activada.",
    "Protection stopped.":
        "Protección desactivada.",
    "Proxy mode":
        "Modo de proxy",
    "Redirect to AdGuard's DNS":
        "Redirigir al DNS de AdGuard",
    "Refresh this page (F5)":
        "Recargar esta página (F5)",
    "Release (stable)":
        "Release (estable)",
    "Remove rule":
        "Eliminar regla",
    "Remove “{}”?":
        "¿Eliminar «{}»?",
    "Remove…":
        "Eliminar…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "¿Reemplazar la configuración actual de AdGuard por la guardada en {}?\n\nAdGuard se reinicia para aplicarla.",
    "Reset history…":
        "Restablecer historial…",
    "Reset…":
        "Restablecer…",
    "Restart AdGuard":
        "Reiniciar AdGuard",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "Las reglas solo se aplican en el modo de proxy automático. Prevalece la primera regla que coincida, así que deja \"*\" en último lugar.",
    "Safe Browsing":
        "Seguridad de navegación",
    "Save anyway":
        "Guardar de todos modos",
    "Saved. AdGuard restarts to apply the change.":
        "Guardado. AdGuard se reinicia para aplicar el cambio.",
    "Saved. Applies after AdGuard Tray restarts.":
        "Guardado. Se aplica tras reiniciar AdGuard Tray.",
    "Saved. The change applies when protection is turned on.":
        "Guardado. El cambio se aplicará al activar la protección.",
    "Secure DNS and ECH":
        "DNS seguro y ECH",
    "Secure DNS filtering":
        "Filtrado de DNS seguro",
    "Set the path in Settings":
        "Definir la ruta en «Configuración»",
    "Settings":
        "Configuración",
    "Show":
        "Mostrar",
    "Show recent entries":
        "Mostrar entradas recientes",
    "Skip HTTPS filtering":
        "Omitir filtrado HTTPS",
    "Some counts could not be loaded.":
        "No se pudieron cargar algunos recuentos.",
    "Source code":
        "Código fuente",
    "Start AdGuard Tray when I log in":
        "Iniciar AdGuard Tray al iniciar sesión",
    "Startup":
        "Inicio",
    "Status checks":
        "Comprobaciones de estado",
    "Stealth mode":
        "Modo sigiloso",
    "System":
        "Sistema",
    "The new lists load when protection is turned on.":
        "Las nuevas listas se cargarán al activar la protección.",
    "Theme":
        "Tema",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "Esto desactiva el filtrado HTTP/3, las comprobaciones OCSP, la Transparencia de certificados y el filtrado de DNS seguro. Los certificados revocados o emitidos incorrectamente pasarán desapercibidos, y los navegadores podrán resolver nombres sin pasar por el filtro DNS de AdGuard.",
    "Time range":
        "Periodo",
    "To keep it but stop using it, switch it off instead.":
        "Para conservarlo sin usarlo, desactívalo en lugar de eliminarlo.",
    "Top lists":
        "Clasificaciones",
    "Trust":
        "Confiar",
    "Trust “{}”?":
        "¿Confiar en «{}»?",
    "Trust…":
        "Confiar…",
    "Turn off all strict checks…":
        "Desactivar todas las comprobaciones estrictas…",
    "Undo":
        "Deshacer",
    "Unknown":
        "Desconocido",
    "Unsaved changes":
        "Cambios sin guardar",
    "Update AdGuard CLI…":
        "Actualizar AdGuard CLI…",
    "Update channel: {}":
        "Canal de actualización: {}",
    "Updated {}":
        "Actualizado: {}",
    "Updates":
        "Actualizaciones",
    "Used in manual mode only.":
        "Solo se usa en el modo manual.",
    "Userscripts update together with filters.":
        "Los userscripts se actualizan junto con los filtros.",
    "Uses XDG autostart (~/.config/autostart).":
        "Usa el inicio automático de XDG (~/.config/autostart).",
    "Waiting for authorization…":
        "Esperando autorización…",
    "Website exceptions":
        "Excepciones de sitios web",
    "Websites":
        "Sitios web",
    "example.com or a link":
        "example.com o un enlace",
    "expires {}":
        "caduca: {}",
    "of {} requests in the last 24 hours":
        "de un total de {} en las últimas 24 horas",
    "{} of {} DNS filters on":
        "Filtros DNS activos: {} de {}",
    "{} of {} filters on":
        "Filtros activos: {} de {}",
    "{} of {} on":
        "Activos: {} de {}",
    "{} unsaved changes to AdGuard's settings":
        "Cambios sin guardar en la configuración de AdGuard: {}",
    "“Follow system” uses your desktop's light or dark setting.":
        "«Según el sistema» usa la configuración clara u oscura de tu escritorio.",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "Activa",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "El certificado de AdGuard se añadirá a todos los perfiles de navegador que se encuentren en este sistema.\n\nAsí AdGuard puede inspeccionar el tráfico HTTPS de esos navegadores. Cierra primero los navegadores – leen el almacén de certificados al iniciarse.",
    "Allow":
        "Permitir",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "Primero aplica o descarta tus cambios en la configuración de AdGuard y después reinicia.",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "Automático: AdGuard redirige hacia sí mismo el tráfico de todas las apps mediante iptables. Manual: AdGuard solo escucha en los puertos SOCKS5 y HTTP de abajo.",
    "Block":
        "Bloquear",
    "Browser API blocking":
        "Bloqueo de API del navegador",
    "CRLite":
        "CRLite",
    "Cancel":
        "Cancelar",
    "Computers":
        "Equipos",
    "Could not change the autostart entry.":
        "No se pudo cambiar la entrada de inicio automático.",
    "Could not export the logs.":
        "No se pudieron exportar los registros.",
    "Could not export the settings.":
        "No se pudo exportar la configuración.",
    "Could not reset the license.":
        "No se pudo restablecer la licencia.",
    "Could not retrieve license info.":
        "No se pudo obtener la información de la licencia.",
    "Could not run the benchmark.":
        "No se pudo ejecutar la prueba de rendimiento.",
    "Could not save the settings.":
        "No se pudo guardar la configuración.",
    "Could not set the update channel.":
        "No se pudo establecer el canal de actualización.",
    "Could not update AdGuard CLI.":
        "No se pudo actualizar AdGuard CLI.",
    "Could not update the filters.":
        "No se pudieron actualizar los filtros.",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "Servidor DNS upstream.\n'default' = DNS del sistema.\nEjemplos: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com",
    "Expiration date":
        "Fecha de caducidad",
    "Expires":
        "Caduca",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "HTTP/3 activado de nuevo en los perfiles de Firefox – reinicia el navegador.",
    "License key":
        "Clave de licencia",
    "License type":
        "Tipo de licencia",
    "Manual":
        "Manual",
    "No exceptions.":
        "No hay excepciones.",
    "OK":
        "Aceptar",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "Activado: AdGuard filtra HTTP/3 (QUIC) por sí mismo – experimental, y algunos\nnavegadores rechazan de todos modos HTTP/3 con un certificado instalado por el usuario.\nDesactivado: AdGuard bloquea QUIC en su lugar, y los navegadores recurren a HTTP/2,\nque se filtra de forma fiable.\nEn ambos casos, esto solo se aplica en el modo automático – en el modo manual,\nel tráfico HTTP/3 nunca llega a AdGuard.",
    "Owner":
        "Titular",
    "Personal":
        "Personal",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "Modo de proxy: {} – el puerto UDP 443 se redirige a AdGuard.",
    "Save adguard-cli path":
        "Guardar ruta de adguard-cli",
    "Search domains or rules…":
        "Buscar dominios o reglas…",
    "Settings file":
        "Archivo de configuración",
    "Status":
        "Estado",
    "Trial":
        "Prueba",
    "Turn HTTP/3 back on in Firefox profiles":
        "Volver a activar HTTP/3 en perfiles de Firefox",
    "Turn off":
        "Desactivar",
    "Turn off HTTP/3 in Firefox profiles":
        "Desactivar HTTP/3 en perfiles de Firefox",
    "Turn off HTTP/3 in Firefox profiles…":
        "Desactivar HTTP/3 en perfiles de Firefox…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "¿Desactivar HTTP/3 en los perfiles de la familia Firefox ({})?\n\nEntonces el tráfico de esos perfiles usará HTTP/2, que AdGuard puede filtrar. Después, reinicia el navegador.",
    "Turn off all strict checks":
        "Desactivar todas las comprobaciones estrictas",
    "Unavailable until AdGuard CLI reports its current channel.":
        "No disponible hasta que AdGuard CLI indique su canal actual.",
    "Update AdGuard CLI":
        "Actualizar AdGuard CLI",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "Solo se usa en el modo automático. Rangos (80:5221,5300:49151) o puertos individuales (80,443,8080).",
    "{} of {}":
        "{} de {}",
    "{} of {} userscripts on":
        "Userscripts activos: {} de {}",
    "{}% blocked":
        "{} % bloqueado",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "Elementos molestos",
    "General":
        "General",
    "Language-specific":
        "Específicos de idioma",
    "Security":
        "Seguridad",
    "Social widgets":
        "Widgets sociales",
    "Expired":
        "Caducada",
    "Autostart on login":
        "Inicio automático al iniciar sesión",
    "Add app rule":
        "Añadir regla de app",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "Se admiten comodines, p. ej., *steam* o *EasyAntiCheat*.",
    "There is already a rule for '{}'.":
        "Ya existe una regla para «{}».",
    "AdGuard settings":
        "Configuración de AdGuard",
    "Ads and trackers are not blocked until you enable protection.":
        "Los anuncios y rastreadores no se bloquean hasta que actives la protección.",
    "Could not import the settings.":
        "No se pudo importar la configuración.",
    "Disable protection":
        "Desactivar protección",
    "Enable protection":
        "Activar protección",
    "Export and import":
        "Exportar e importar",
    "Features":
        "Funciones",
    "Import settings":
        "Importar configuración",
    "Import settings from…":
        "Importar configuración desde…",
    "Import settings…":
        "Importar configuración…",
    "Import…":
        "Importar…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "Guarda los filtros, las reglas y la configuración en un archivo zip, o los carga desde uno.",
    "Update":
        "Actualizar",
    "Version":
        "Versión",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "{} no es una exportación de la configuración. Elige un archivo guardado con «Exportar» en «Configuración de AdGuard».",
}
