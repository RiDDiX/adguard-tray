"""Brazilian Portuguese (also used for pt_PT)."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "Idioma",
    "English":                           "Inglês",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "Ativo – Proteção em execução",
    "Inactive – Protection stopped":        "Inativo – Proteção parada",
    "Error retrieving status":              "Erro ao obter o status",
    "adguard-cli not found":                "adguard-cli não encontrado",
    "Unknown status":                       "Status desconhecido",
    "Checking status…":                     "Verificando status…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "Reiniciar",
    "Filters":                              "Filtros",
    "Loading…":                             "Carregando…",
    "Manage filters…":                      "Gerenciar filtros…",
    "No userscripts installed":             "Nenhum userscript instalado",
    "Manage userscripts…":                  "Gerenciar userscripts…",
    "Quit":                                 "Sair",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "ativa",
    "inactive":                             "inativa",
    "System-wide filtering: {}":            "Filtragem em todo o sistema: {}",
    "Error: {}":                            "Erro: {}",
    "AdGuard Tray – Error":                 "AdGuard Tray – Erro",
    "AdGuard is now active – protection running.":
        "O AdGuard agora está ativo – proteção em execução.",
    "AdGuard has been stopped.":
        "O AdGuard foi parado.",
    "Could not retrieve status.":
        "Não foi possível obter o status.",
    "Command failed":                       "Falha no comando",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " segundos",
    "How often adguard-cli status is checked automatically.":
        "Com que frequência o status do adguard-cli é verificado automaticamente.",
    "Log level:":                           "Nível de log:",
    "adguard-cli path:":                    "Caminho do adguard-cli:",
    "auto-detect via PATH":                 "detectar automaticamente via PATH",
    "Browse…":                              "Procurar…",
    "Select adguard-cli binary":            "Selecionar o binário do adguard-cli",
    "Notifications":                        "Notificações",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "Atualizar filtros",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "Atualiza todos os filtros, filtros DNS, userscripts,\nSafebrowsingV2, CRLite e verifica atualizações do aplicativo.",
    "No filters found.":                    "Nenhum filtro encontrado.",
    "Updating filters… (can take up to 2 minutes)":
        "Atualizando filtros… (pode levar até 2 minutos)",
    "Update completed.":                    "Atualização concluída.",
    "Update failed.":                       "Falha na atualização.",
    "Installing: {}":                       "Instalando: {}",
    "Filter installed.":                    "Filtro instalado.",
    "Remove":                               "Remover",
    "Remove filter":                        "Remover filtro",
    "Filter {} removed.":                   "Filtro {} removido.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        "Instalar userscript a partir de uma URL .js direta",
    "No userscripts installed.":            "Nenhum userscript instalado.",
    "Userscript URL (direct .js URL):":     "URL do userscript (URL .js direta):",
    "Userscript installed.":                "Userscript instalado.",
    'Remove "{}"':                          "Remover “{}”",
    "Remove userscript":                    "Remover userscript",
    "'{}' removed.":                        "“{}” removido.",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "O adguard-cli não foi encontrado.\nInstale pelo script oficial ou pelo AUR:\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "Erro desconhecido ao obter o status",
    "AdGuard {} ok":                        "AdGuard {} ok",
    "AdGuard via systemctl {} ok":          "AdGuard via systemctl {} ok",
    "'{}' failed – insufficient privileges?":
        "“{}” falhou – privilégios insuficientes?",
    "Could not retrieve filter list":
        "Não foi possível obter a lista de filtros",
    "Filter {} enabled":                    "Filtro {} ativado",
    "Could not enable filter {}":           "Não foi possível ativar o filtro {}",
    "Filter {} disabled":                   "Filtro {} desativado",
    "Could not disable filter {}":
        "Não foi possível desativar o filtro {}",
    "Filter installed":                     "Filtro instalado",
    "Installation failed":                  "Falha na instalação",
    "Filter {} removed":                    "Filtro {} removido",
    "Could not remove filter {}":
        "Não foi possível remover o filtro {}",
    "Filters updated":                      "Filtros atualizados",
    "Update failed":                        "Falha na atualização",
    "Could not retrieve userscript list":
        "Não foi possível obter a lista de userscripts",
    "Userscript '{}' enabled":              "Userscript “{}” ativado",
    "Could not enable userscript '{}'":
        "Não foi possível ativar o userscript “{}”",
    "Userscript '{}' disabled":             "Userscript “{}” desativado",
    "Could not disable userscript '{}'":
        "Não foi possível desativar o userscript “{}”",
    "Userscript '{}' removed":              "Userscript “{}” removido",
    "Could not remove userscript '{}'":
        "Não foi possível remover o userscript “{}”",
    "Userscript installed":                 "Userscript instalado",
    "Other":                                "Outros",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "Pesquisar filtros…",
    "Search userscripts…":              "Pesquisar userscripts…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "Não foi possível carregar o proxy.yaml.\nCaminho: {}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "Aplicativos",
    "Mode:":                            "Modo:",
    "Filtered ports:":                  "Portas filtradas:",
    "SOCKS5 port:":                     "Porta SOCKS5:",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "Porta do proxy SOCKS5 para o modo manual.\nDefina -1 para desativar.",
    "HTTP port:":                       "Porta HTTP:",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "Porta do proxy HTTP para o modo manual.\nDefina -1 para desativar.",
    "Listen address:":                  "Endereço de escuta:",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "Endereço em que o proxy escuta.\n127.0.0.1 = apenas local. 0.0.0.0 = todas as interfaces (requer autenticação).",
    "Worker threads:":                  "Threads de trabalho:",
    "Number of proxy worker threads.":  "Número de threads de trabalho do proxy.",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "Descriptografar e filtrar o tráfego HTTPS.\nNecessário para bloquear anúncios em sites https.\nRequer um certificado raiz confiável instalado no sistema.",
    "Enable TLS 1.3":                   "Ativar TLS 1.3",
    "Enable TLS 1.3 support for filtered connections.":
        "Ativar o suporte a TLS 1.3 nas conexões filtradas.",
    "Filter HTTP/3 (QUIC) – experimental":
        "Filtrar HTTP/3 (QUIC) – experimental",
    "OCSP certificate checks":          "Verificações de certificado OCSP",
    "Enforce Certificate Transparency": "Exigir Certificate Transparency",
    "Filter EV certificate sites":      "Filtrar sites com certificados EV",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "Por padrão, sites com certificados de Validação Estendida não são filtrados.\nAtive para filtrá-los também (ex.: sites de bancos).",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "Ativar ECH para mais privacidade.\nRequer a filtragem DNS ativada.",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "Filtrar consultas DNS para bloquear anúncios e rastreadores no nível do DNS.\nUsa um proxy DNS local com upstreams configuráveis.",
    "Upstream:":                        "Upstream:",
    "Fallbacks:":                       "Fallback:",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "Servidores DNS de fallback (usados quando o upstream principal falha).\n'default' = DNS do sistema. Lista separada por espaços.\nExemplo: default 1.1.1.1",
    "Bootstraps:":                      "Bootstrap:",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "DNS de bootstrap para resolver os hostnames dos upstreams.\n'default' = IPs do DNS do sistema. Apenas endereços IP são permitidos.\nExemplo: default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "Remove o parâmetro ECH dos registros DNS SVCB/HTTPS.\nAtive apenas para navegadores que não detectam a filtragem HTTPS automaticamente.",
    "Master switch for all tracking protection features below.":
        "Chave geral de todos os recursos de proteção contra rastreamento abaixo.",
    "Cookies":                          "Cookies",
    "Block third-party cookies":        "Bloquear cookies de terceiros",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "Exclui cookies de terceiros após um tempo definido.\nImpede o rastreamento entre sites.",
    "Lifetime (minutes):":              "Tempo de vida (minutos):",
    "0 = block immediately. Default: 180 minutes.":
        "0 = bloquear imediatamente. Padrão: 180 minutos.",
    "Block first-party cookies":        "Bloquear cookies primários",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "Exclui todos os cookies (inclusive os primários) após um tempo definido.\nAviso: isso encerra a sessão em todos os sites.",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = bloquear imediatamente. Padrão: 4320 minutos (3 dias).",
    "Privacy":                          "Privacidade",
    "Hide / reduce User-Agent":         "Ocultar / reduzir User-Agent",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "Remove partes identificadoras do User-Agent.\nReduz o fingerprinting.",
    "Hide search queries in referrer":  "Ocultar consultas de pesquisa no referrer",
    "Hides your search terms when clicking from a search engine to a website.":
        "Oculta os termos de pesquisa ao acessar um site a partir de um mecanismo de pesquisa.",
    "Remove referrer from third-party requests":
        "Remover referrer de requisições de terceiros",
    "Prevents third-party sites from knowing which page you came from.":
        "Impede que sites de terceiros saibam a página de origem.",
    "Send Do-Not-Track signal":         "Enviar sinal Do-Not-Track",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "Envia o cabeçalho DNT com as requisições.\nObservação: a maioria dos sites ignora isso, mas alguns respeitam.",
    "Disable third-party ETag cache":   "Desativar cache ETag de terceiros",
    "Prevents tracking via ETag caching in third-party content.":
        "Impede o rastreamento via cache ETag em conteúdo de terceiros.",
    "Block third-party Authorization header":
        "Bloquear cabeçalho Authorization de terceiros",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "Bloqueia o cabeçalho Authorization em requisições de terceiros para impedir o rastreamento.",
    "Remove X-Client-Data header":      "Remover cabeçalho X-Client-Data",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "Remove o cabeçalho X-Client-Data enviado pelo Chrome aos serviços do Google.",
    "Block WebRTC":                     "Bloquear WebRTC",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "Impede vazamentos de IP via WebRTC.\nPode quebrar chamadas de vídeo e alguns aplicativos web.",
    "Block Push API":                   "Bloquear API Push",
    "Blocks browser push notifications from websites.":
        "Bloqueia notificações push do navegador enviadas por sites.",
    "Block Location API":               "Bloquear API de localização",
    "Prevents websites from accessing your GPS location.":
        "Impede que sites acessem a localização por GPS.",
    "Block Flash":                      "Bloquear Flash",
    "Blocks the Flash plugin.":
        "Bloqueia o plugin Flash.",
    "Block Java":                       "Bloquear Java",
    "Disables Java plugins. JavaScript remains enabled.":
        "Desativa plugins Java. O JavaScript continua ativado.",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "Ativar Anti-DPI",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "Altera os dados dos pacotes de saída para contornar a inspeção profunda de pacotes (DPI).\nÚtil em países com censura na internet.",
    "App pattern":
        "Padrão de aplicativo",
    "Skip outbound proxy":              "Ignorar proxy de saída",
    "Don't route this app's traffic through outbound proxy":
        "Não encaminhar o tráfego deste aplicativo pelo proxy de saída",
    "Browser list included from {}":    "Lista de navegadores incluída a partir de {}",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "A lista incluída de navegadores e a regra curinga (*) não podem ser removidas.",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "Alerta sobre sites maliciosos e de phishing.\nUsa o banco de dados Safe Browsing do AdGuard.",
    "Send anonymous statistics":        "Enviar estatísticas anônimas",
    "Send anonymous lookups to AdGuard.":
        "Enviar consultas anônimas ao AdGuard.",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "Verificação de revogação de certificados com o CRLite da Mozilla.\nMais rápida e confiável que as verificações CRL/OCSP tradicionais.",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "Aplicar as regras dos filtros de bloqueio de anúncios às requisições HTTP/HTTPS.",
    "Save failed":                      "Falha ao salvar",
    "Could not save proxy.yaml:\n{}":   "Não foi possível salvar o proxy.yaml:\n{}",
    "Restarting AdGuard…":              "Reiniciando o AdGuard…",
    "AdGuard restarted.":               "AdGuard reiniciado.",
    "Restart failed: {}":               "Falha ao reiniciar: {}",
    "Unknown error":                    "Erro desconhecido",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "Adicionar",
    "Search exceptions…":               "Pesquisar exceções…",
    "1 exception":                      "1 exceção",
    "{} exceptions":                    "{} exceções",
    "'{}' is not a valid domain or IP address.":
        "“{}” não é um domínio ou endereço IP válido.",
    "'{}' is already in the list.":     "“{}” já está na lista.",
    "Could not save exceptions:\n{}":
        "Não foi possível salvar as exceções:\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "Visão geral",
    "Userscripts":                      "Userscripts",
    "Exceptions":                       "Exceções",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "Redefinir licença",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "Gerar um certificado de CA raiz para a filtragem HTTPS. O certificado precisa ser instalado e marcado como confiável no sistema.",
    "Checking for updates…":            "Verificando atualizações…",
    "Firefox profile:":                 "Perfil do Firefox:",
    "(optional) e.g. abcd1234.MyProfile":
        "(opcional) ex.: abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "Digite o ID ou o nome do filtro:",
    "Filter added.":                    "Filtro adicionado.",
    "Rename…":                          "Renomear…",
    "Rename filter":                    "Renomear filtro",
    "New title:":                       "Novo título:",
    "Filter renamed.":                  "Filtro renomeado.",
    "Filter trust updated.":            "Confiança do filtro atualizada.",
    "Filter URL:":                      "URL do filtro:",
    "Title:":                           "Título:",
    "(optional)":                       "(opcional)",
    "Trusted filter":                   "Filtro confiável",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "Pesquisar filtros DNS…",
    "No DNS filters found.":            "Nenhum filtro DNS encontrado.",
    "DNS filter installed.":            "Filtro DNS instalado.",
    "DNS filter added.":                "Filtro DNS adicionado.",
    "Remove DNS filter":                "Remover filtro DNS",
    "DNS filter {} removed.":           "Filtro DNS {} removido.",
    "Rename DNS filter":                "Renomear filtro DNS",
    "DNS filter renamed.":              "Filtro DNS renomeado.",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "Exportar logs…",
    "Export AdGuard CLI logs to a zip file":
        "Exportar os logs do AdGuard CLI para um arquivo zip",
    "Export settings…":                 "Exportar configurações…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "Executar um benchmark criptográfico e de filtragem HTTPS.",
    "Run benchmark":                    "Executar benchmark",
    "Done.":                            "Concluído.",
    "Export logs to…":                  "Exportar logs para…",
    "Export settings to…":              "Exportar configurações para…",
    "Zip files (*.zip);;All files (*)":
        "Arquivos zip (*.zip);;Todos os arquivos (*)",
    "Log file not found.":              "Arquivo de log não encontrado.",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "Não foi possível obter a lista de filtros DNS",
    "DNS filter {} enabled":            "Filtro DNS {} ativado",
    "Could not enable DNS filter {}":   "Não foi possível ativar o filtro DNS {}",
    "DNS filter {} disabled":           "Filtro DNS {} desativado",
    "Could not disable DNS filter {}":  "Não foi possível desativar o filtro DNS {}",
    "DNS filter installed":             "Filtro DNS instalado",
    "DNS filter {} removed":            "Filtro DNS {} removido",
    "Could not remove DNS filter {}":   "Não foi possível remover o filtro DNS {}",
    "DNS filter added":                 "Filtro DNS adicionado",
    "Could not add DNS filter":         "Não foi possível adicionar o filtro DNS",
    "DNS filter title updated":         "Título do filtro DNS atualizado",
    "Could not set DNS filter title":   "Não foi possível definir o título do filtro DNS",
    "Filter added":                     "Filtro adicionado",
    "Could not add filter":             "Não foi possível adicionar o filtro",
    "Filter trust updated":             "Confiança do filtro atualizada",
    "Could not update filter trust":    "Não foi possível atualizar a confiança do filtro",
    "Filter title updated":             "Título do filtro atualizado",
    "Could not set filter title":       "Não foi possível definir o título do filtro",
    "License reset":                    "Licença redefinida",
    "Could not reset license":          "Não foi possível redefinir a licença",
    "Could not retrieve license info":  "Não foi possível obter as informações da licença",
    "Certificate generated":            "Certificado gerado",
    "Certificate generation failed":    "Falha ao gerar o certificado",
    "Logs exported":                    "Logs exportados",
    "Log export failed":                "Falha na exportação dos logs",
    "Settings exported":                "Configurações exportadas",
    "Settings export failed":           "Falha na exportação das configurações",
    "Settings imported":                "Configurações importadas",
    "Settings import failed":           "Falha na importação das configurações",
    "Update check completed":           "Verificação de atualizações concluída",
    "Update check failed":              "Falha na verificação de atualizações",
    "Benchmark failed":                 "Falha no benchmark",
    "AdGuard stopped (forced)":         "AdGuard parado (forçado)",
    "Could not stop AdGuard – process may still be running":
        "Não foi possível parar o AdGuard – o processo ainda pode estar em execução",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "O adguard-cli não foi encontrado neste sistema.\n\nMétodo de instalação recomendado (oficial):\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\nAlternativa (AUR do Arch Linux):\n  paru -S adguard-cli-bin\n\nO AdGuard Tray será carregado, mas iniciar/parar só funcionará após a instalação do adguard-cli.",
    "Copy install command":             "Copiar comando de instalação",
    "Continue":                         "Continuar",
    "AdGuard Tray is already running":  "O AdGuard Tray já está em execução",
    "Only one instance can run at a time. Check your system tray.":
        "Apenas uma instância pode ser executada por vez. Verifique a bandeja do sistema.",
    "Authentication cancelled":         "Autenticação cancelada",
    "Authorization failed":             "Falha na autorização",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "Verifica se o certificado de um site foi revogado (OCSP).\nO AdGuard verifica de forma assíncrona e deixa a conexão passar\nse a verificação for lenta, então isso raramente causa problemas em sites –\nmantenha ativado, a menos que um problema tenha sido atribuído a essa verificação.",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "Exige as verificações de Certificate Transparency (a política de CT do Chrome).\nSites cujo próprio certificado não é compatível com CT deixam de ser filtrados\ne o navegador pode recusá-los. Sites grandes são compatíveis; por isso, só\nexperimente esta opção em um site que apresente erro de certificado.",
    "Sites that don't load":
        "Sites que não carregam",
    "Turn off HTTP/3 filtering":
        "Desativar a filtragem de HTTP/3",
    "No filters installed":
        "Nenhum filtro instalado",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "O HTTP/3 está bloqueado por uma regra de firewall; os navegadores usam HTTP/2.",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "Aplicativos excluídos da filtragem (o tráfego HTTP/3 deles também não é filtrado): {}",
    "AdGuard is not running – nothing is filtered.":
        "O AdGuard não está em execução – nada é filtrado.",
    "could not remove the previous certificate":
        "não foi possível remover o certificado anterior",
    "HTTP/3 state unknown":
        "Estado do HTTP/3 desconhecido",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "Uma regra de firewall rejeita o tráfego UDP 443 de saída, então o QUIC não pode ser usado.",
    "Browser policy disables QUIC: {}":
        "A política do navegador desativa o QUIC: {}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "Os navegadores podem contornar o AdGuard via HTTP/3 (UDP 443).",
    "Checking…":
        "Verificando…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "Não foi possível ler o proxy.yaml – estado do HTTP/3 desconhecido.",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "Perfis da família Firefox com HTTP/3 desativado: {} de {}",
    "HTTP/3 (QUIC)":
        "HTTP/3 (QUIC)",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "O HTTP/3 é bloqueado pelo AdGuard; os navegadores voltam a usar o HTTP/2 filtrado.",
    "HTTP/3 is filtered by AdGuard.":
        "O HTTP/3 é filtrado pelo AdGuard.",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "HTTP/3 desativado nos perfis do Firefox – reinicie o navegador.",
    "HTTPS filtering is off – nothing is filtered.":
        "A filtragem HTTPS está desativada – nada é filtrado.",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "Modo de proxy: {} – só o tráfego que passa pelo proxy é filtrado, e os navegadores não enviam QUIC por ele.",
    "unknown":
        "desconhecido",
    "AdGuard's certificate was not found. Generate it first.":
        "O certificado do AdGuard não foi encontrado. Gere-o primeiro.",
    "Certificate could not be installed in any browser.":
        "Não foi possível instalar o certificado em nenhum navegador.",
    "Certificate installed for {} of {} stores.":
        "Certificado instalado em {} de {} repositórios.",
    "Chromium-based browsers":
        "Navegadores baseados em Chromium",
    "No browser certificate stores found.":
        "Nenhum repositório de certificados de navegador encontrado.",
    "Restart your browsers for the certificate to take effect.":
        "Reinicie os navegadores para que o certificado tenha efeito.",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "Execute sem sudo/pkexec – a instalação é feita nos perfis de navegador do usuário atual",
    "certificate not found after import":
        "certificado não encontrado após a importação",
    "certutil not found – install the 'nss' package":
        "certutil não encontrado – instale o pacote 'nss'",
    "not found":
        "não encontrado",
    "Could not read the filter list (unexpected CLI output).":
        "Não foi possível ler a lista de filtros (saída inesperada do CLI).",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "Nenhuma bandeja do sistema encontrada. O AdGuard Tray está em execução sem ícone — ative uma bandeja/AppIndicator no painel.",
    "URL must start with http:// or https://":
        "A URL deve começar com http:// ou https://",
    "adguard-cli path does not exist or is not executable.":
        "O caminho do adguard-cli não existe ou não é executável.",
    "That binary does not identify as adguard-cli. Save anyway?":
        "Esse binário não se identifica como adguard-cli. Salvar mesmo assim?",
    "Update channel":                   "Canal de atualização",
    "Switching update channel to {}…":  "Mudando o canal de atualização para {}…",
    "Update channel set to {}":         "Canal de atualização definido como {}",
    "Could not set update channel":     "Não foi possível definir o canal de atualização",
    "Invalid channel: {}":              "Canal inválido: {}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        "Ainda não há log de acesso ({}). O AdGuard o cria depois de filtrar tráfego; quando é executado como serviço do sistema, o log pertence ao root e não pode ser lido aqui.",
    'Cannot read the access log ({}): {}':
        "Não foi possível ler o log de acesso ({}): {}",
    'Blocked':
        "Bloqueado",
    'Blocked only':
        "Só bloqueados",
    "Refresh":
        "Recarregar",
    'Allow selected domain':
        "Permitir domínio selecionado",
    'Block selected domain':
        "Bloquear domínio selecionado",
    'Activity':
        "Atividade",
    'Time':
        "Hora",
    'Domain':
        "Domínio",
    'Result':
        "Resultado",
    'Rule':
        "Regra",
    'Size':
        "Tamanho",
    'Count':
        "Contagem",
    'Could not read the access log.':
        "Não foi possível ler o log de acesso.",
    '{} lines not understood':
        "{} linhas não reconhecidas",
    'Not a valid domain: {}':
        "Domínio inválido: {}",
    'Source: {}':
        "Fonte: {}",
    'Allowed':
        "Permitido",
    'Added rule: {}':
        "Regra adicionada: {}",
    'Requests per hour, {} to {} · busiest hour: {}':
        "Requisições por hora, {} a {} · hora de pico: {}",
    'Last 24 hours':
        "Últimas 24 horas",
    'Last 7 days':
        "Últimos 7 dias",
    'Requests':
        "Requisições",
    'Traffic':
        "Tráfego",

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        "A versão {} está disponível (a atual é {}).",
    'Application update':
        "Atualização do aplicativo",
    'Check for update':
        "Verificar atualizações",
    'Install update':
        "Instalar atualização",
    'Installing update…':
        "Instalando atualização…",
    'Restart now':
        "Reiniciar agora",
    'Later':
        "Mais tarde",
    'You are running the latest version ({}).':
        "A versão mais recente já está instalada ({}).",
    'Installation not recognised':
        "Instalação não reconhecida",
    'Could not check for updates.':
        "Não foi possível verificar atualizações.",
    'Update with: {}':
        "Atualizar com: {}",
    'Installed with the AUR package {}':
        "Instalado com o pacote do AUR {}",
    'Installed in {}':
        "Instalado em {}",
    'Running from a source checkout':
        "Executando a partir do código-fonte (checkout)",
    'Version {} installed. Restart adguard-tray to use it.':
        "Versão {} instalada. Reinicie o adguard-tray para usá-la.",
    'Unexpected answer from GitHub: {}':
        "Resposta inesperada do GitHub: {}",
    'Download failed: {}':
        "Falha no download: {}",
    'Could not unpack the download: {}':
        "Não foi possível descompactar o download: {}",
    'This installation is managed elsewhere: {}':
        "Esta instalação é gerenciada por outro meio: {}",
    'No permission to write to {}':
        "Sem permissão para gravar em {}",
    'GitHub returned {}.':
        "O GitHub retornou {}.",
    'No connection to GitHub: {}':
        "Sem conexão com o GitHub: {}",
    'The download does not contain adguard-tray.':
        "O download não contém o adguard-tray.",
    'The download says version {} instead of {} – aborted.':
        "O download indica a versão {} em vez de {} – operação cancelada.",
    'GitHub is rate limiting this address. Try again later.':
        "O GitHub está limitando a taxa de requisições deste endereço. Tente novamente mais tarde.",
    'The download is larger than expected – aborted.':
        "O download é maior que o esperado – operação cancelada.",
    'Update failed: {}':
        "Falha na atualização: {}",
    'The archive contains unexpected paths – aborted.':
        "O arquivo compactado contém caminhos inesperados – operação cancelada.",
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        "Falha na atualização e não foi possível restaurar a versão antiga. Restaure-a a partir de {} ou reinstale com: {}",
    'Last 30 days':
        "Últimos 30 dias",
    'All time':
        "Todo o período",
    'Modified':
        "Modificado",
    'Rules':
        "Regras",
    'Showing {} – show all':
        "Mostrando {} – mostrar todos",
    'history {}':
        "histórico {}",
    'Filter list ID: {}':
        "ID da lista de filtros: {}",
    'App':
        "Aplicativo",
    'Protocol':
        "Protocolo",
    'Type':
        "Tipo",
    'Reset history':
        "Redefinir histórico",
    'Delete the stored history and read the log again.':
        "Excluir o histórico armazenado e ler o log novamente.",
    'Delete the stored history? Only what the log still holds can be read back.':
        "Excluir o histórico armazenado? Só é possível recuperar o que ainda estiver no log.",
    'History is not being updated: {}':
        "O histórico não está sendo atualizado: {}",

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "1 alteração não salva nas configurações do AdGuard",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "Um filtro confiável pode executar scripts nas páginas visitadas. Confie apenas em listas de fontes conhecidas.",
    "About":
        "Sobre",
    "Actions for the selected filter":
        "Ações para o filtro selecionado",
    "Ad blocking":
        "Bloqueio de anúncios",
    "Ad blocking is off, so the filter lists below have no effect.":
        "O bloqueio de anúncios está desativado, então as listas de filtros abaixo não têm efeito.",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "O AdGuard CLI baixa e instala a compilação mais recente.",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "O AdGuard CLI esquece a licença neste computador. Será necessário ativá-la novamente.",
    "AdGuard CLI logs":
        "Logs do AdGuard CLI",
    "AdGuard CLI update finished.":
        "Atualização do AdGuard CLI concluída.",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "Log do AdGuard Tray",
    "AdGuard doesn't filter these websites.":
        "O AdGuard não filtra estes sites.",
    "AdGuard is filtering this computer's traffic.":
        "O AdGuard está filtrando o tráfego deste computador.",
    "AdGuard restarts to load the new lists.":
        "O AdGuard será reiniciado para carregar as novas listas.",
    "AdGuard's reply did not say whether it is running.":
        "A resposta do AdGuard não indicou se ele está em execução.",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "O arquivo de configurações do AdGuard não foi encontrado ({}). Execute o adguard-cli uma vez para criá-lo.",
    "Add DNS filter by ID":
        "Adicionar filtro DNS por ID",
    "Add DNS filter from URL":
        "Adicionar filtro DNS de URL",
    "Add filter":
        "Adicionar filtro",
    "Add filter by ID":
        "Adicionar filtro por ID",
    "Add filter from URL":
        "Adicionar filtro de URL",
    "Add rule":
        "Adicionar regra",
    "Add to browsers":
        "Adicionar aos navegadores",
    "Add userscript":
        "Adicionar userscript",
    "Add userscript…":
        "Adicionar userscript…",
    "Add website":
        "Adicionar site",
    "Add…":
        "Adicionar…",
    "Advanced":
        "Avançado",
    "All available":
        "Todos os disponíveis",
    "Allow {}":
        "Permitir {}",
    "Also adds the certificate to this Firefox profile.":
        "Também adiciona o certificado a este perfil do Firefox.",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "Também em reinicializações e erros. Requer notify-send (libnotify) ou um serviço de notificações em execução, como dunst, mako ou o do KDE.",
    "Appearance":
        "Aparência",
    "Applies after AdGuard Tray restarts.":
        "Entra em vigor após reiniciar o AdGuard Tray.",
    "Apply":
        "Aplicar",
    "Apply your changes to AdGuard's settings before closing?":
        "Aplicar as alterações nas configurações do AdGuard antes de fechar?",
    "Applying them restarts AdGuard if protection is on.":
        "Ao aplicá-las, o AdGuard será reiniciado se a proteção estiver ativada.",
    "Asks GitHub for the newest release.":
        "Busca no GitHub a versão mais recente.",
    "At a glance":
        "Resumo",
    "Automatic":
        "Automático",
    "Automatic – filter all apps":
        "Automático – filtrar todos os aplicativos",
    "Benchmark":
        "Benchmark",
    "Beta":
        "Beta",
    "Block ECH in DNS records":
        "Bloquear ECH em registros DNS",
    "Block domains before a connection is made.":
        "Bloqueia domínios antes que a conexão seja estabelecida.",
    "Block {}":
        "Bloquear {}",
    "Blocked (24 h)":
        "Bloqueados (24 h)",
    "Browser list ({})":
        "Lista de navegadores ({})",
    "By ID or name…":
        "Por ID ou nome…",
    "Certificate":
        "Certificado",
    "Certificate checks":
        "Verificações de certificado",
    "Changes are collected in the bar at the bottom and applied together.":
        "As alterações são reunidas na barra inferior e aplicadas em conjunto.",
    "Check again":
        "Verificar novamente",
    "Check every":
        "Verificar a cada",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "Navegadores baseados em Chromium e Firefox mantêm o próprio repositório de certificados.",
    "Close":
        "Fechar",
    "Controls which AdGuard CLI build “{}” installs.":
        "Define qual compilação do AdGuard CLI é instalada por “{}”.",
    "Could not add the rule.":
        "Não foi possível adicionar a regra.",
    "Could not open {}":
        "Não foi possível abrir {}",
    "Could not read {}":
        "Não foi possível ler {}",
    "Could not refresh. Showing data from {}.":
        "Não foi possível recarregar. Mostrando dados de {}.",
    "Could not reset the history.":
        "Não foi possível redefinir o histórico.",
    "Could not restart AdGuard.":
        "Não foi possível reiniciar o AdGuard.",
    "Could not start protection.":
        "Não foi possível iniciar a proteção.",
    "Could not stop protection.":
        "Não foi possível parar a proteção.",
    "Create":
        "Criar",
    "Create certificate":
        "Criar certificado",
    "Custom":
        "Personalizado",
    "DNS filter lists":
        "Listas de filtros DNS",
    "DNS filtering":
        "Filtragem DNS",
    "DNS filtering is off, so these lists have no effect.":
        "A filtragem DNS está desativada, então estas listas não têm efeito.",
    "DNS servers":
        "Servidores DNS",
    "Dark":
        "Escuro",
    "Default":
        "Padrão",
    "Details":
        "Detalhes",
    "Discard":
        "Descartar",
    "Don't filter":
        "Não filtrar",
    "Don't trust":
        "Não confiar",
    "Downloads and installs the newest AdGuard CLI build.":
        "Baixa e instala a compilação mais recente do AdGuard CLI.",
    "Duration":
        "Duração",
    "Export…":
        "Exportar…",
    "Filter everything":
        "Filtrar tudo",
    "Filter in place":
        "Filtrar diretamente",
    "Filtering":
        "Filtragem",
    "Follow system":
        "Seguir o sistema",
    "From URL…":
        "De URL…",
    "Go to updates":
        "Ir para Atualizações",
    "HTTP proxy: {}":
        "Proxy HTTP: {}",
    "HTTPS filtering":
        "Filtragem HTTPS",
    "How much detail AdGuard Tray writes to its own log.":
        "Quantidade de detalhes que o AdGuard Tray escreve no próprio log.",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "Se um site não carregar, desative primeiro a filtragem de HTTP/3. As outras verificações protegem todos os sites – desative-as apenas se isso não resolver.",
    "Included":
        "Incluída",
    "Installed":
        "Instalados",
    "License":
        "Licença",
    "Light":
        "Claro",
    "Logs":
        "Logs",
    "MIT license":
        "Licença MIT",
    "Maintenance":
        "Manutenção",
    "Manual proxy":
        "Proxy manual",
    "Manual – only apps set to use the proxy":
        "Manual – só aplicativos configurados para usar o proxy",
    "More":
        "Mais",
    "Move down":
        "Mover para baixo",
    "Move up":
        "Mover para cima",
    "Network":
        "Rede",
    "Nightly":
        "Nightly",
    "No requests yet – AdGuard logs requests while protection is on.":
        "Nenhuma requisição ainda – o AdGuard registra as requisições enquanto a proteção estiver ativada.",
    "Not added":
        "Não adicionado",
    "Nothing matches your search.":
        "Nenhum resultado para a pesquisa.",
    "Notify me when protection turns on or off":
        "Notificar quando a proteção for ativada ou desativada",
    "Off":
        "Desativado",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "Afeta apenas navegadores que usam DoH ou DoT. Com “Desativado”, eles contornam a filtragem DNS do AdGuard.",
    "Open AdGuard Tray":
        "Abrir o AdGuard Tray",
    "Open exceptions":
        "Abrir exceções",
    "Open folder":
        "Abrir pasta",
    "Open release page":
        "Abrir página da versão",
    "Pages":
        "Páginas",
    "Performance":
        "Desempenho",
    "Protection":
        "Proteção",
    "Protection started.":
        "Proteção iniciada.",
    "Protection stopped.":
        "Proteção parada.",
    "Proxy mode":
        "Modo de proxy",
    "Redirect to AdGuard's DNS":
        "Redirecionar para o DNS do AdGuard",
    "Refresh this page (F5)":
        "Recarregar esta página (F5)",
    "Release (stable)":
        "Release (estável)",
    "Remove rule":
        "Remover regra",
    "Remove “{}”?":
        "Remover “{}”?",
    "Remove…":
        "Remover…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "Substituir as configurações atuais do AdGuard pelas contidas em {}?\n\nO AdGuard será reiniciado para aplicá-las.",
    "Reset history…":
        "Redefinir histórico…",
    "Reset…":
        "Redefinir…",
    "Restart AdGuard":
        "Reiniciar o AdGuard",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "As regras só se aplicam no modo de proxy automático. A primeira regra correspondente prevalece, então mantenha \"*\" por último.",
    "Safe Browsing":
        "Safe Browsing",
    "Save anyway":
        "Salvar mesmo assim",
    "Saved. AdGuard restarts to apply the change.":
        "Salvo. O AdGuard será reiniciado para aplicar a alteração.",
    "Saved. Applies after AdGuard Tray restarts.":
        "Salvo. Entra em vigor após reiniciar o AdGuard Tray.",
    "Saved. The change applies when protection is turned on.":
        "Salvo. A alteração será aplicada quando a proteção for ativada.",
    "Secure DNS and ECH":
        "DNS seguro e ECH",
    "Secure DNS filtering":
        "Filtragem de DNS seguro",
    "Set the path in Settings":
        "Defina o caminho em Configurações",
    "Settings":
        "Configurações",
    "Show":
        "Mostrar",
    "Show recent entries":
        "Mostrar entradas recentes",
    "Skip HTTPS filtering":
        "Ignorar filtragem HTTPS",
    "Some counts could not be loaded.":
        "Não foi possível carregar algumas contagens.",
    "Source code":
        "Código-fonte",
    "Start AdGuard Tray when I log in":
        "Iniciar o AdGuard Tray ao entrar na sessão",
    "Startup":
        "Inicialização",
    "Status checks":
        "Verificações de status",
    "Stealth mode":
        "Modo oculto",
    "System":
        "Sistema",
    "The new lists load when protection is turned on.":
        "As novas listas serão carregadas quando a proteção for ativada.",
    "Theme":
        "Tema",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "Isso desativa a filtragem de HTTP/3, as verificações OCSP, o Certificate Transparency e a filtragem de DNS seguro. Certificados revogados ou emitidos incorretamente passam despercebidos, e os navegadores podem resolver nomes sem passar pelo filtro DNS do AdGuard.",
    "Time range":
        "Período",
    "To keep it but stop using it, switch it off instead.":
        "Para mantê-lo sem usá-lo, desative-o em vez disso.",
    "Top lists":
        "Mais frequentes",
    "Trust":
        "Confiar",
    "Trust “{}”?":
        "Confiar em “{}”?",
    "Trust…":
        "Confiar…",
    "Turn off all strict checks…":
        "Desativar todas as verificações rigorosas…",
    "Undo":
        "Desfazer",
    "Unknown":
        "Desconhecido",
    "Unsaved changes":
        "Alterações não salvas",
    "Update AdGuard CLI…":
        "Atualizar o AdGuard CLI…",
    "Update channel: {}":
        "Canal de atualização: {}",
    "Updated {}":
        "Atualizado em {}",
    "Updates":
        "Atualizações",
    "Used in manual mode only.":
        "Usado apenas no modo manual.",
    "Userscripts update together with filters.":
        "Os userscripts são atualizados junto com os filtros.",
    "Uses XDG autostart (~/.config/autostart).":
        "Usa a inicialização automática do XDG (~/.config/autostart).",
    "Waiting for authorization…":
        "Aguardando autorização…",
    "Website exceptions":
        "Exceções de sites",
    "Websites":
        "Sites",
    "example.com or a link":
        "example.com ou um link",
    "expires {}":
        "expira em {}",
    "of {} requests in the last 24 hours":
        "de {} requisições nas últimas 24 horas",
    "{} of {} DNS filters on":
        "{} de {} filtros DNS ativos",
    "{} of {} filters on":
        "{} de {} filtros ativos",
    "{} of {} on":
        "{} de {} ativos",
    "{} unsaved changes to AdGuard's settings":
        "{} alterações não salvas nas configurações do AdGuard",
    "“Follow system” uses your desktop's light or dark setting.":
        "“Seguir o sistema” usa o modo claro ou escuro da área de trabalho.",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "Ativa",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "O certificado do AdGuard será adicionado a todos os perfis de navegador encontrados neste sistema.\n\nIsso permite que o AdGuard inspecione o tráfego HTTPS nesses navegadores. Feche os navegadores primeiro – eles leem o repositório de certificados ao iniciar.",
    "Allow":
        "Permitir",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "Aplique ou descarte primeiro as alterações nas configurações do AdGuard e depois reinicie.",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "Automático: o AdGuard redireciona todo o tráfego dos aplicativos para si mesmo via iptables. Manual: o AdGuard só escuta nas portas SOCKS5 e HTTP abaixo.",
    "Block":
        "Bloquear",
    "Browser API blocking":
        "Bloqueio de APIs do navegador",
    "CRLite":
        "CRLite",
    "Cancel":
        "Cancelar",
    "Computers":
        "Computadores",
    "Could not change the autostart entry.":
        "Não foi possível alterar a entrada de inicialização automática.",
    "Could not export the logs.":
        "Não foi possível exportar os logs.",
    "Could not export the settings.":
        "Não foi possível exportar as configurações.",
    "Could not reset the license.":
        "Não foi possível redefinir a licença.",
    "Could not retrieve license info.":
        "Não foi possível obter as informações da licença.",
    "Could not run the benchmark.":
        "Não foi possível executar o benchmark.",
    "Could not save the settings.":
        "Não foi possível salvar as configurações.",
    "Could not set the update channel.":
        "Não foi possível definir o canal de atualização.",
    "Could not update AdGuard CLI.":
        "Não foi possível atualizar o AdGuard CLI.",
    "Could not update the filters.":
        "Não foi possível atualizar os filtros.",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "Servidor DNS upstream.\n'default' = DNS do sistema.\nExemplos: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com",
    "Expiration date":
        "Data de expiração",
    "Expires":
        "Expira em",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "HTTP/3 reativado nos perfis do Firefox – reinicie o navegador.",
    "License key":
        "Chave de licença",
    "License type":
        "Tipo de licença",
    "Manual":
        "Manual",
    "No exceptions.":
        "Nenhuma exceção.",
    "OK":
        "OK",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "Ativado: o AdGuard filtra o HTTP/3 (QUIC) por conta própria – experimental, e alguns\nnavegadores recusam de qualquer forma o HTTP/3 com um certificado instalado pelo usuário.\nDesativado: o AdGuard bloqueia o QUIC em vez disso, e os navegadores voltam a usar o HTTP/2,\nque é filtrado de forma confiável.\nEm ambos os casos, isso só se aplica no modo automático – no modo manual,\no tráfego HTTP/3 nunca chega ao AdGuard.",
    "Owner":
        "Proprietário",
    "Personal":
        "Pessoal",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "Modo de proxy: {} – a porta UDP 443 é redirecionada para o AdGuard.",
    "Save adguard-cli path":
        "Salvar o caminho do adguard-cli",
    "Search domains or rules…":
        "Pesquisar domínios ou regras…",
    "Settings file":
        "Arquivo de configurações",
    "Status":
        "Status",
    "Trial":
        "Avaliação",
    "Turn HTTP/3 back on in Firefox profiles":
        "Reativar HTTP/3 nos perfis do Firefox",
    "Turn off":
        "Desativar",
    "Turn off HTTP/3 in Firefox profiles":
        "Desativar HTTP/3 nos perfis do Firefox",
    "Turn off HTTP/3 in Firefox profiles…":
        "Desativar HTTP/3 nos perfis do Firefox…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "Desativar HTTP/3 em {} perfil(is) da família Firefox?\n\nO tráfego deles passará a usar HTTP/2, que o AdGuard consegue filtrar. Reinicie o navegador depois.",
    "Turn off all strict checks":
        "Desativar todas as verificações rigorosas",
    "Unavailable until AdGuard CLI reports its current channel.":
        "Indisponível até que o AdGuard CLI informe o canal atual.",
    "Update AdGuard CLI":
        "Atualizar o AdGuard CLI",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "Usadas apenas no modo automático. Intervalos (80:5221,5300:49151) ou portas individuais (80,443,8080).",
    "{} of {}":
        "{} de {}",
    "{} of {} userscripts on":
        "{} de {} userscripts ativos",
    "{}% blocked":
        "{}% bloqueado",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "Aborrecimentos",
    "General":
        "Geral",
    "Language-specific":
        "Por idioma",
    "Security":
        "Segurança",
    "Social widgets":
        "Widgets sociais",
    "Expired":
        "Expirada",
    "Autostart on login":
        "Iniciar automaticamente ao entrar",
    "Add app rule":
        "Adicionar regra de aplicativo",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "Curingas funcionam, ex.: *steam* ou *EasyAntiCheat*.",
    "There is already a rule for '{}'.":
        "Já existe uma regra para “{}”.",
    "AdGuard settings":
        "Configurações do AdGuard",
    "Ads and trackers are not blocked until you enable protection.":
        "Anúncios e rastreadores não são bloqueados até que a proteção seja ativada.",
    "Could not import the settings.":
        "Não foi possível importar as configurações.",
    "Disable protection":
        "Desativar proteção",
    "Enable protection":
        "Ativar proteção",
    "Export and import":
        "Exportar e importar",
    "Features":
        "Recursos",
    "Import settings":
        "Importar configurações",
    "Import settings from…":
        "Importar configurações de…",
    "Import settings…":
        "Importar configurações…",
    "Import…":
        "Importar…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "Salvar filtros, regras e configuração em um arquivo zip ou carregá-los de um arquivo zip.",
    "Update":
        "Atualizar",
    "Version":
        "Versão",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "{} não é uma exportação de configurações. Escolha um arquivo salvo com “Exportar” em “Configurações do AdGuard”.",

    # ── AdGuard VPN, outbound proxy, install ──────────────────────────
    "Press Enter to close this window.":
        "Pressione Enter para fechar esta janela.",
    "No terminal app was found. The install command is on the clipboard: paste it into a terminal.":
        "Nenhum aplicativo de terminal foi encontrado. O comando de instalação está na área de transferência: cole-o em um terminal.",
    "Finish the installation in the terminal, then press Refresh.":
        "Conclua a instalação no terminal e depois clique em Recarregar.",
    "Open in a terminal":
        "Abrir em um terminal",
    "AdGuard VPN":
        "AdGuard VPN",
    "AdGuard's VPN for Linux (adguardvpn-cli) runs next to AdGuard CLI. AdGuard Tray checks that their settings fit together; it does not connect the VPN or log in.":
        "O AdGuard VPN para Linux (adguardvpn-cli) é executado junto com o AdGuard CLI. O AdGuard Tray verifica se as configurações dos dois são compatíveis; ele não conecta a VPN nem faz login.",
    "Install…":
        "Instalar…",
    "Outbound proxy":
        "Proxy de saída",
    "AdGuard sends its own connections through this proxy, for example through AdGuard VPN in SOCKS5 mode.":
        "O AdGuard envia as próprias conexões por este proxy, por exemplo pelo AdGuard VPN no modo SOCKS5.",
    "Use an outbound proxy":
        "Usar um proxy de saída",
    "Host":
        "Host",
    "Port":
        "Porta",
    "Not installed.":
        "Não instalado.",
    "AdGuard VPN is set to TUN mode while AdGuard filters in automatic mode. Connected like this, traffic loops between the two – AdGuard does not support this combination.":
        "O AdGuard VPN está no modo TUN enquanto o AdGuard filtra no modo automático. Com a VPN conectada assim, o tráfego entra em loop entre os dois – o AdGuard não oferece suporte a essa combinação.",
    "AdGuard VPN now uses SOCKS5 mode. Press Apply to send AdGuard's traffic through it, and reconnect AdGuard VPN if it is connected.":
        "O AdGuard VPN agora usa o modo SOCKS5. Clique em Aplicar para enviar o tráfego do AdGuard por ele e reconecte o AdGuard VPN se estiver conectado.",
    "AdGuard VPN CLI":
        "AdGuard VPN CLI",
    "Installed, but its settings could not be read: {}":
        "Instalado, mas não foi possível ler as configurações: {}",
    "Route AdGuard through the VPN":
        "Encaminhar o tráfego do AdGuard pela VPN",
    "Could not switch AdGuard VPN to SOCKS5 mode.":
        "Não foi possível mudar o AdGuard VPN para o modo SOCKS5.",
    "Installed · SOCKS5 mode on {}:{}":
        "Instalado · modo SOCKS5 em {}:{}",
    "Installed · TUN mode":
        "Instalado · modo TUN",
    "Installed · {} mode":
        "Instalado · modo {}",
}
