"""Russian."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "Язык",
    "English":                           "Английский",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "Активно — защита работает",
    "Inactive – Protection stopped":        "Неактивно — защита остановлена",
    "Error retrieving status":              "Ошибка получения статуса",
    "adguard-cli not found":                "adguard-cli не найден",
    "Unknown status":                       "Статус неизвестен",
    "Checking status…":                     "Проверка статуса…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "Перезапустить",
    "Filters":                              "Фильтры",
    "Loading…":                             "Загрузка…",
    "Manage filters…":                      "Управление фильтрами…",
    "No userscripts installed":             "Пользовательские скрипты не установлены",
    "Manage userscripts…":                  "Управление пользовательскими скриптами…",
    "Quit":                                 "Выйти",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "активна",
    "inactive":                             "неактивна",
    "System-wide filtering: {}":            "Системная фильтрация: {}",
    "Error: {}":                            "Ошибка: {}",
    "AdGuard Tray – Error":                 "AdGuard Tray — ошибка",
    "AdGuard is now active – protection running.":
        "AdGuard активен — защита работает.",
    "AdGuard has been stopped.":
        "AdGuard остановлен.",
    "Could not retrieve status.":
        "Не удалось получить статус.",
    "Command failed":                       "Не удалось выполнить команду",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " с",
    "How often adguard-cli status is checked automatically.":
        "Как часто автоматически проверяется статус adguard-cli.",
    "Log level:":                           "Уровень журналирования:",
    "adguard-cli path:":                    "Путь к adguard-cli:",
    "auto-detect via PATH":                 "автоопределение через PATH",
    "Browse…":                              "Выбрать…",
    "Select adguard-cli binary":            "Выбор исполняемого файла adguard-cli",
    "Notifications":                        "Уведомления",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "Обновить фильтры",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "Обновляет все фильтры, DNS-фильтры, пользовательские скрипты,\nSafebrowsingV2, CRLite и проверяет обновления программы.",
    "No filters found.":                    "Фильтры не найдены.",
    "Updating filters… (can take up to 2 minutes)":
        "Обновление фильтров… (может занять до 2 минут)",
    "Update completed.":                    "Обновление завершено.",
    "Update failed.":                       "Не удалось выполнить обновление.",
    "Installing: {}":                       "Установка: {}",
    "Filter installed.":                    "Фильтр установлен.",
    "Remove":                               "Удалить",
    "Remove filter":                        "Удалить фильтр",
    "Filter {} removed.":                   "Фильтр {} удалён.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        "Установить пользовательский скрипт по прямому URL файла .js",
    "No userscripts installed.":            "Пользовательские скрипты не установлены.",
    "Userscript URL (direct .js URL):":     "URL пользовательского скрипта (прямой URL файла .js):",
    "Userscript installed.":                "Пользовательский скрипт установлен.",
    'Remove "{}"':                          "Удалить «{}»",
    "Remove userscript":                    "Удалить пользовательский скрипт",
    "'{}' removed.":                        "Пользовательский скрипт «{}» удалён.",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "adguard-cli не найден.\nУстановите его с помощью официального скрипта или из AUR:\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "Неизвестная ошибка при получении статуса",
    "AdGuard {} ok":                        "Команда AdGuard {} выполнена",
    "AdGuard via systemctl {} ok":          "AdGuard: команда systemctl {} выполнена",
    "'{}' failed – insufficient privileges?":
        "Не удалось выполнить «{}» — недостаточно прав?",
    "Could not retrieve filter list":
        "Не удалось получить список фильтров",
    "Filter {} enabled":                    "Фильтр {} включён",
    "Could not enable filter {}":           "Не удалось включить фильтр {}",
    "Filter {} disabled":                   "Фильтр {} выключен",
    "Could not disable filter {}":
        "Не удалось выключить фильтр {}",
    "Filter installed":                     "Фильтр установлен",
    "Installation failed":                  "Ошибка установки",
    "Filter {} removed":                    "Фильтр {} удалён",
    "Could not remove filter {}":
        "Не удалось удалить фильтр {}",
    "Filters updated":                      "Фильтры обновлены",
    "Update failed":                        "Ошибка обновления",
    "Could not retrieve userscript list":
        "Не удалось получить список пользовательских скриптов",
    "Userscript '{}' enabled":              "Пользовательский скрипт «{}» включён",
    "Could not enable userscript '{}'":
        "Не удалось включить пользовательский скрипт «{}»",
    "Userscript '{}' disabled":             "Пользовательский скрипт «{}» выключен",
    "Could not disable userscript '{}'":
        "Не удалось выключить пользовательский скрипт «{}»",
    "Userscript '{}' removed":              "Пользовательский скрипт «{}» удалён",
    "Could not remove userscript '{}'":
        "Не удалось удалить пользовательский скрипт «{}»",
    "Userscript installed":                 "Пользовательский скрипт установлен",
    "Other":                                "Другие",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "Поиск фильтров…",
    "Search userscripts…":              "Поиск пользовательских скриптов…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "Не удалось загрузить proxy.yaml.\nПуть: {}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "Приложения",
    "Mode:":                            "Режим:",
    "Filtered ports:":                  "Фильтруемые порты:",
    "SOCKS5 port:":                     "Порт SOCKS5:",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "Порт SOCKS5-прокси для ручного режима.\nУкажите -1, чтобы отключить.",
    "HTTP port:":                       "Порт HTTP:",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "Порт HTTP-прокси для ручного режима.\nУкажите -1, чтобы отключить.",
    "Listen address:":                  "Адрес прослушивания:",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "Адрес, на котором прокси принимает подключения.\n127.0.0.1 = только локально. 0.0.0.0 = все интерфейсы (требуется аутентификация).",
    "Worker threads:":                  "Рабочие потоки:",
    "Number of proxy worker threads.":  "Количество рабочих потоков прокси.",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "Расшифровывать и фильтровать HTTPS-трафик.\nНеобходимо для блокировки рекламы на сайтах с HTTPS.\nТребуется доверенный корневой сертификат, установленный в системе.",
    "Enable TLS 1.3":                   "Включить TLS 1.3",
    "Enable TLS 1.3 support for filtered connections.":
        "Включить поддержку TLS 1.3 для фильтруемых соединений.",
    "Filter HTTP/3 (QUIC) – experimental":
        "Фильтровать HTTP/3 (QUIC) — экспериментально",
    "OCSP certificate checks":          "Проверка сертификатов через OCSP",
    "Enforce Certificate Transparency": "Требовать Certificate Transparency",
    "Filter EV certificate sites":      "Фильтровать сайты с EV-сертификатами",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "По умолчанию сайты с EV-сертификатами (Extended Validation) не фильтруются.\nВключите, чтобы фильтровать и их (например, сайты банков).",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "Включить ECH для большей конфиденциальности.\nТребуется включённая DNS-фильтрация.",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "Фильтровать DNS-запросы, чтобы блокировать рекламу и трекеры на уровне DNS.\nИспользуется локальный DNS-прокси с настраиваемыми upstream-серверами.",
    "Upstream:":                        "Upstream-сервер:",
    "Fallbacks:":                       "Резервные серверы:",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "Резервные DNS-серверы (используются, если основной upstream-сервер недоступен).\n'default' = системный DNS. Список через пробел.\nПример: default 1.1.1.1",
    "Bootstraps:":                      "Bootstrap-серверы:",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "Bootstrap-серверы DNS для разрешения имён upstream-серверов.\n'default' = IP-адреса системного DNS. Допускаются только IP-адреса.\nПример: default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "Удалять параметр ECH из DNS-записей SVCB/HTTPS.\nВключайте только для браузеров, которые не распознают HTTPS-фильтрацию автоматически.",
    "Master switch for all tracking protection features below.":
        "Главный переключатель всех функций защиты от трекинга ниже.",
    "Cookies":                          "Файлы cookie",
    "Block third-party cookies":        "Блокировать сторонние файлы cookie",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "Удалять сторонние файлы cookie через заданное время.\nПредотвращает межсайтовое отслеживание.",
    "Lifetime (minutes):":              "Срок хранения (мин):",
    "0 = block immediately. Default: 180 minutes.":
        "0 = блокировать сразу. По умолчанию: 180 минут.",
    "Block first-party cookies":        "Блокировать собственные файлы cookie",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "Удалять все файлы cookie (включая собственные) через заданное время.\nВнимание: вы выйдете из учётных записей на всех сайтах.",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = блокировать сразу. По умолчанию: 4320 минут (3 дня).",
    "Privacy":                          "Конфиденциальность",
    "Hide / reduce User-Agent":         "Скрывать / сокращать User-Agent",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "Удаляет идентифицирующие сведения из User-Agent.\nЗатрудняет снятие цифрового отпечатка.",
    "Hide search queries in referrer":  "Скрывать поисковые запросы в реферере",
    "Hides your search terms when clicking from a search engine to a website.":
        "Скрывает ваши поисковые запросы при переходе с поисковой системы на сайт.",
    "Remove referrer from third-party requests":
        "Удалять реферер из сторонних запросов",
    "Prevents third-party sites from knowing which page you came from.":
        "Не даёт сторонним сайтам узнать, с какой страницы вы пришли.",
    "Send Do-Not-Track signal":         "Отправлять сигнал Do-Not-Track",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "Отправляет заголовок DNT вместе с запросами.\nПримечание: большинство сайтов его игнорируют, но некоторые учитывают.",
    "Disable third-party ETag cache":   "Отключать кеш ETag для сторонних запросов",
    "Prevents tracking via ETag caching in third-party content.":
        "Предотвращает отслеживание через кеширование ETag в стороннем контенте.",
    "Block third-party Authorization header":
        "Блокировать заголовок Authorization в сторонних запросах",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "Блокирует заголовок Authorization в сторонних запросах для защиты от отслеживания.",
    "Remove X-Client-Data header":      "Удалять заголовок X-Client-Data",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "Удаляет заголовок X-Client-Data, который Chrome отправляет сервисам Google.",
    "Block WebRTC":                     "Блокировать WebRTC",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "Предотвращает утечку IP-адреса через WebRTC.\nМожет нарушить работу видеозвонков и некоторых веб-приложений.",
    "Block Push API":                   "Блокировать Push API",
    "Blocks browser push notifications from websites.":
        "Блокирует push-уведомления браузера от сайтов.",
    "Block Location API":               "Блокировать Location API",
    "Prevents websites from accessing your GPS location.":
        "Запрещает сайтам доступ к вашему местоположению по GPS.",
    "Block Flash":                      "Блокировать Flash",
    "Blocks the Flash plugin.":
        "Блокирует плагин Flash.",
    "Block Java":                       "Блокировать Java",
    "Disables Java plugins. JavaScript remains enabled.":
        "Отключает плагины Java. JavaScript остаётся включённым.",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "Включить Anti-DPI",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "Изменяет данные исходящих пакетов для обхода глубокой инспекции пакетов (DPI).\nПолезно в странах с интернет-цензурой.",
    "App pattern":
        "Шаблон приложения",
    "Skip outbound proxy":              "Обходить исходящий прокси",
    "Don't route this app's traffic through outbound proxy":
        "Не направлять трафик этого приложения через исходящий прокси",
    "Browser list included from {}":    "Источник списка браузеров: {}",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "Подключаемый список браузеров и правило с подстановочным знаком (*) удалить нельзя.",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "Предупреждает об опасных сайтах и фишинге.\nИспользует базу вредоносных и фишинговых сайтов AdGuard.",
    "Send anonymous statistics":        "Отправлять анонимную статистику",
    "Send anonymous lookups to AdGuard.":
        "Отправлять в AdGuard анонимные запросы на проверку.",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "Проверка отзыва сертификатов с помощью CRLite от Mozilla.\nБыстрее и надёжнее традиционных проверок CRL/OCSP.",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "Применять правила блокировки рекламы к HTTP/HTTPS-запросам.",
    "Save failed":                      "Ошибка сохранения",
    "Could not save proxy.yaml:\n{}":   "Не удалось сохранить proxy.yaml:\n{}",
    "Restarting AdGuard…":              "Перезапуск AdGuard…",
    "AdGuard restarted.":               "AdGuard перезапущен.",
    "Restart failed: {}":               "Ошибка перезапуска: {}",
    "Unknown error":                    "Неизвестная ошибка",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "Добавить",
    "Search exceptions…":               "Поиск исключений…",
    "1 exception":                      "Исключений: 1",
    "{} exceptions":                    "Исключений: {}",
    "'{}' is not a valid domain or IP address.":
        "Недопустимый домен или IP-адрес: «{}».",
    "'{}' is already in the list.":     "Запись «{}» уже есть в списке.",
    "Could not save exceptions:\n{}":
        "Не удалось сохранить исключения:\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "Обзор",
    "Userscripts":                      "Пользовательские скрипты",
    "Exceptions":                       "Исключения",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "Сбросить лицензию",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "Создание корневого CA-сертификата для HTTPS-фильтрации. Сертификат должен быть установлен в системе и отмечен как доверенный.",
    "Checking for updates…":            "Проверка обновлений…",
    "Firefox profile:":                 "Профиль Firefox:",
    "(optional) e.g. abcd1234.MyProfile":
        "(необязательно), например abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "Введите ID или название фильтра:",
    "Filter added.":                    "Фильтр добавлен.",
    "Rename…":                          "Переименовать…",
    "Rename filter":                    "Переименовать фильтр",
    "New title:":                       "Новое название:",
    "Filter renamed.":                  "Фильтр переименован.",
    "Filter trust updated.":            "Доверие к фильтру изменено.",
    "Filter URL:":                      "URL фильтра:",
    "Title:":                           "Название:",
    "(optional)":                       "(необязательно)",
    "Trusted filter":                   "Доверенный фильтр",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "Поиск DNS-фильтров…",
    "No DNS filters found.":            "DNS-фильтры не найдены.",
    "DNS filter installed.":            "DNS-фильтр установлен.",
    "DNS filter added.":                "DNS-фильтр добавлен.",
    "Remove DNS filter":                "Удалить DNS-фильтр",
    "DNS filter {} removed.":           "DNS-фильтр {} удалён.",
    "Rename DNS filter":                "Переименовать DNS-фильтр",
    "DNS filter renamed.":              "DNS-фильтр переименован.",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "Экспортировать журналы…",
    "Export AdGuard CLI logs to a zip file":
        "Экспорт журналов AdGuard CLI в zip-архив",
    "Export settings…":                 "Экспортировать настройки…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "Замер скорости шифрования и HTTPS-фильтрации.",
    "Run benchmark":                    "Запустить тест",
    "Done.":                            "Готово.",
    "Export logs to…":                  "Экспорт журналов в…",
    "Export settings to…":              "Экспорт настроек в…",
    "Zip files (*.zip);;All files (*)":
        "Zip-архивы (*.zip);;Все файлы (*)",
    "Log file not found.":              "Файл журнала не найден.",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "Не удалось получить список DNS-фильтров",
    "DNS filter {} enabled":            "DNS-фильтр {} включён",
    "Could not enable DNS filter {}":   "Не удалось включить DNS-фильтр {}",
    "DNS filter {} disabled":           "DNS-фильтр {} выключен",
    "Could not disable DNS filter {}":  "Не удалось выключить DNS-фильтр {}",
    "DNS filter installed":             "DNS-фильтр установлен",
    "DNS filter {} removed":            "DNS-фильтр {} удалён",
    "Could not remove DNS filter {}":   "Не удалось удалить DNS-фильтр {}",
    "DNS filter added":                 "DNS-фильтр добавлен",
    "Could not add DNS filter":         "Не удалось добавить DNS-фильтр",
    "DNS filter title updated":         "Название DNS-фильтра изменено",
    "Could not set DNS filter title":   "Не удалось задать название DNS-фильтра",
    "Filter added":                     "Фильтр добавлен",
    "Could not add filter":             "Не удалось добавить фильтр",
    "Filter trust updated":             "Доверие к фильтру изменено",
    "Could not update filter trust":    "Не удалось изменить доверие к фильтру",
    "Filter title updated":             "Название фильтра изменено",
    "Could not set filter title":       "Не удалось задать название фильтра",
    "License reset":                    "Лицензия сброшена",
    "Could not reset license":          "Не удалось сбросить лицензию",
    "Could not retrieve license info":  "Не удалось получить сведения о лицензии",
    "Certificate generated":            "Сертификат создан",
    "Certificate generation failed":    "Не удалось создать сертификат",
    "Logs exported":                    "Журналы экспортированы",
    "Log export failed":                "Не удалось экспортировать журналы",
    "Settings exported":                "Настройки экспортированы",
    "Settings export failed":           "Не удалось экспортировать настройки",
    "Settings imported":                "Настройки импортированы",
    "Settings import failed":           "Не удалось импортировать настройки",
    "Update check completed":           "Проверка обновлений завершена",
    "Update check failed":              "Не удалось проверить обновления",
    "Benchmark failed":                 "Не удалось выполнить тест производительности",
    "AdGuard stopped (forced)":         "AdGuard остановлен (принудительно)",
    "Could not stop AdGuard – process may still be running":
        "Не удалось остановить AdGuard — процесс, возможно, ещё работает",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "adguard-cli не найден в системе.\n\nРекомендуемый способ установки (официальный):\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\nАльтернативный способ (AUR для Arch Linux):\n  paru -S adguard-cli-bin\n\nAdGuard Tray запустится, но запуск и остановка защиты не будут работать, пока не установлен adguard-cli.",
    "Copy install command":             "Копировать команду установки",
    "Continue":                         "Продолжить",
    "AdGuard Tray is already running":  "AdGuard Tray уже запущен",
    "Only one instance can run at a time. Check your system tray.":
        "Одновременно может работать только один экземпляр. Проверьте системный лоток.",
    "Authentication cancelled":         "Аутентификация отменена",
    "Authorization failed":             "Ошибка авторизации",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "Проверять, не отозван ли сертификат сайта (OCSP).\nAdGuard проверяет асинхронно и пропускает соединение, если\nпроверка идёт долго, поэтому сайты из-за неё редко перестают работать —\nне выключайте её, пока не убедитесь, что проблема именно в ней.",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "Принудительно проверять Certificate Transparency (политика CT в Chrome).\nСайты, чей сертификат не соответствует CT, перестают фильтроваться,\nи браузер может их отклонить. Крупные сайты соответствуют CT, поэтому\nвыключайте эту проверку, только если сайт выдаёт ошибку сертификата.",
    "Sites that don't load":
        "Сайты, которые не загружаются",
    "Turn off HTTP/3 filtering":
        "Выключить фильтрацию HTTP/3",
    "No filters installed":
        "Нет установленных фильтров",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "HTTP/3 заблокирован правилом брандмауэра; браузеры используют HTTP/2.",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "Приложения, исключённые из фильтрации (их HTTP/3-трафик тоже не фильтруется): {}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuard не запущен — ничего не фильтруется.",
    "could not remove the previous certificate":
        "не удалось удалить предыдущий сертификат",
    "HTTP/3 state unknown":
        "Состояние HTTP/3 неизвестно",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "Правило брандмауэра отклоняет исходящий трафик на UDP-порт 443, поэтому QUIC использовать нельзя.",
    "Browser policy disables QUIC: {}":
        "QUIC отключён политикой браузера: {}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "Браузеры могут обходить AdGuard через HTTP/3 (UDP 443).",
    "Checking…":
        "Проверка…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "Не удалось прочитать proxy.yaml — состояние HTTP/3 неизвестно.",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "Профили браузеров семейства Firefox с выключенным HTTP/3: {} из {}",
    "HTTP/3 (QUIC)":
        "HTTP/3 (QUIC)",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "AdGuard блокирует HTTP/3; браузеры переходят на фильтруемый HTTP/2.",
    "HTTP/3 is filtered by AdGuard.":
        "AdGuard фильтрует HTTP/3.",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "HTTP/3 выключен в профилях Firefox — перезапустите браузер.",
    "HTTPS filtering is off – nothing is filtered.":
        "HTTPS-фильтрация выключена — ничего не фильтруется.",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "Режим прокси: {} — фильтруется только трафик, идущий через прокси, а QUIC браузеры через него не отправляют.",
    "unknown":
        "неизвестно",
    "AdGuard's certificate was not found. Generate it first.":
        "Сертификат AdGuard не найден. Сначала создайте его.",
    "Certificate could not be installed in any browser.":
        "Не удалось установить сертификат ни в один браузер.",
    "Certificate installed for {} of {} stores.":
        "Сертификат установлен в хранилища: {} из {}.",
    "Chromium-based browsers":
        "Браузеры на основе Chromium",
    "No browser certificate stores found.":
        "Хранилища сертификатов браузеров не найдены.",
    "Restart your browsers for the certificate to take effect.":
        "Перезапустите браузеры, чтобы сертификат начал действовать.",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "Запускайте без sudo/pkexec — сертификат устанавливается в ваши собственные профили браузеров",
    "certificate not found after import":
        "сертификат не найден после импорта",
    "certutil not found – install the 'nss' package":
        "certutil не найден — установите пакет «nss»",
    "not found":
        "не найдено",
    "Could not read the filter list (unexpected CLI output).":
        "Не удалось прочитать список фильтров (неожиданный вывод CLI).",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "Системный лоток не найден. AdGuard Tray работает без значка — включите системный лоток или AppIndicator на панели.",
    "URL must start with http:// or https://":
        "URL должен начинаться с http:// или https://",
    "adguard-cli path does not exist or is not executable.":
        "Путь к adguard-cli не существует или файл не является исполняемым.",
    "That binary does not identify as adguard-cli. Save anyway?":
        "Этот исполняемый файл не определяется как adguard-cli. Всё равно сохранить?",
    "Update channel":                   "Канал обновления",
    "Switching update channel to {}…":  "Переключение канала обновления на «{}»…",
    "Update channel set to {}":         "Выбран канал обновления: {}",
    "Could not set update channel":     "Не удалось задать канал обновления",
    "Invalid channel: {}":              "Недопустимый канал: {}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        "Журнала запросов пока нет ({}). AdGuard создаёт его, как только отфильтрует трафик; если AdGuard работает как системная служба, журнал принадлежит root, и AdGuard Tray не может его прочитать.",
    'Cannot read the access log ({}): {}':
        "Не удалось прочитать журнал запросов ({}): {}",
    'Blocked':
        "Заблокировано",
    'Blocked only':
        "Только заблокированные",
    "Refresh":
        "Обновить",
    'Allow selected domain':
        "Разрешить выбранный домен",
    'Block selected domain':
        "Блокировать выбранный домен",
    'Activity':
        "Активность",
    'Time':
        "Время",
    'Domain':
        "Домен",
    'Result':
        "Результат",
    'Rule':
        "Правило",
    'Size':
        "Размер",
    'Count':
        "Количество",
    'Could not read the access log.':
        "Не удалось прочитать журнал запросов.",
    '{} lines not understood':
        "Нераспознанных строк: {}",
    'Not a valid domain: {}':
        "Недопустимый домен: {}",
    'Source: {}':
        "Источник: {}",
    'Allowed':
        "Разрешено",
    'Added rule: {}':
        "Добавлено правило: {}",
    'Requests per hour, {} to {} · busiest hour: {}':
        "Запросы по часам, с {} по {} · пиковый час: {}",
    'Last 24 hours':
        "Последние 24 часа",
    'Last 7 days':
        "Последние 7 дней",
    'Requests':
        "Запросы",
    'Traffic':
        "Трафик",

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        "Доступна версия {} (у вас {}).",
    'Application update':
        "Обновление программы",
    'Check for update':
        "Проверить обновления",
    'Install update':
        "Установить обновление",
    'Installing update…':
        "Установка обновления…",
    'Restart now':
        "Перезапустить сейчас",
    'Later':
        "Позже",
    'You are running the latest version ({}).':
        "Установлена последняя версия ({}).",
    'Installation not recognised':
        "Способ установки не распознан",
    'Could not check for updates.':
        "Не удалось проверить обновления.",
    'Update with: {}':
        "Для обновления выполните: {}",
    'Installed with the AUR package {}':
        "Установлено из пакета AUR {}",
    'Installed in {}':
        "Установлено в {}",
    'Running from a source checkout':
        "Запущено из рабочей копии исходного кода",
    'Version {} installed. Restart adguard-tray to use it.':
        "Версия {} установлена. Перезапустите adguard-tray, чтобы начать её использовать.",
    'Unexpected answer from GitHub: {}':
        "Неожиданный ответ от GitHub: {}",
    'Download failed: {}':
        "Ошибка загрузки: {}",
    'Could not unpack the download: {}':
        "Не удалось распаковать загруженный архив: {}",
    'This installation is managed elsewhere: {}':
        "Эта установка управляется другими средствами: {}",
    'No permission to write to {}':
        "Нет прав на запись в {}",
    'GitHub returned {}.':
        "Ответ GitHub: {}.",
    'No connection to GitHub: {}':
        "Нет подключения к GitHub: {}",
    'The download does not contain adguard-tray.':
        "Загруженный архив не содержит adguard-tray.",
    'The download says version {} instead of {} – aborted.':
        "В загруженном архиве версия {} вместо {} — обновление прервано.",
    'GitHub is rate limiting this address. Try again later.':
        "GitHub ограничивает число запросов с этого адреса. Попробуйте позже.",
    'The download is larger than expected – aborted.':
        "Загруженный файл больше ожидаемого — обновление прервано.",
    'Update failed: {}':
        "Ошибка обновления: {}",
    'The archive contains unexpected paths – aborted.':
        "Архив содержит неожиданные пути — обновление прервано.",
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        "Ошибка обновления; старую версию восстановить не удалось. Восстановите её из {} или переустановите командой: {}",
    'Last 30 days':
        "Последние 30 дней",
    'All time':
        "Всё время",
    'Modified':
        "Изменено",
    'Rules':
        "Правила",
    'Showing {} – show all':
        "Только {} — показать все",
    'history {}':
        "история: {}",
    'Filter list ID: {}':
        "ID фильтра: {}",
    'App':
        "Приложение",
    'Protocol':
        "Протокол",
    'Type':
        "Тип",
    'Reset history':
        "Очистить историю",
    'Delete the stored history and read the log again.':
        "Удалить сохранённую историю и заново прочитать журнал.",
    'Delete the stored history? Only what the log still holds can be read back.':
        "Удалить сохранённую историю? Восстановить можно будет только то, что ещё есть в журнале.",
    'History is not being updated: {}':
        "История не обновляется: {}",

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "Несохранённых изменений в настройках AdGuard: 1",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "Доверенный фильтр может запускать скрипты на посещаемых вами страницах. Доверяйте только фильтрам из известных вам источников.",
    "About":
        "О программе",
    "Actions for the selected filter":
        "Действия с выбранным фильтром",
    "Ad blocking":
        "Блокировка рекламы",
    "Ad blocking is off, so the filter lists below have no effect.":
        "Блокировка рекламы выключена, поэтому фильтры ниже не действуют.",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLI скачает и установит свою новейшую сборку.",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "AdGuard CLI сбросит лицензию на этом компьютере. Вам придётся активировать её снова.",
    "AdGuard CLI logs":
        "Журналы AdGuard CLI",
    "AdGuard CLI update finished.":
        "Обновление AdGuard CLI завершено.",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "Журнал AdGuard Tray",
    "AdGuard doesn't filter these websites.":
        "AdGuard не фильтрует эти сайты.",
    "AdGuard is filtering this computer's traffic.":
        "AdGuard фильтрует трафик этого компьютера.",
    "AdGuard restarts to load the new lists.":
        "AdGuard перезапустится, чтобы загрузить новые фильтры.",
    "AdGuard's reply did not say whether it is running.":
        "Из ответа AdGuard неясно, запущен ли он.",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "Файл настроек AdGuard не найден ({}). Запустите adguard-cli один раз, чтобы создать его.",
    "Add DNS filter by ID":
        "Добавить DNS-фильтр по ID",
    "Add DNS filter from URL":
        "Добавить DNS-фильтр по URL",
    "Add filter":
        "Добавить фильтр",
    "Add filter by ID":
        "Добавить фильтр по ID",
    "Add filter from URL":
        "Добавить фильтр по URL",
    "Add rule":
        "Добавить правило",
    "Add to browsers":
        "Добавить в браузеры",
    "Add userscript":
        "Добавить пользовательский скрипт",
    "Add userscript…":
        "Добавить пользовательский скрипт…",
    "Add website":
        "Добавить сайт",
    "Add…":
        "Добавить…",
    "Advanced":
        "Дополнительно",
    "All available":
        "Все доступные",
    "Allow {}":
        "Разрешить {}",
    "Also adds the certificate to this Firefox profile.":
        "Также добавляет сертификат в этот профиль Firefox.",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "Также при перезапусках и ошибках. Требуется notify-send (libnotify) или запущенная служба уведомлений, например dunst, mako или служба KDE.",
    "Appearance":
        "Внешний вид",
    "Applies after AdGuard Tray restarts.":
        "Вступит в силу после перезапуска AdGuard Tray.",
    "Apply":
        "Применить",
    "Apply your changes to AdGuard's settings before closing?":
        "Применить изменения в настройках AdGuard перед закрытием?",
    "Applying them restarts AdGuard if protection is on.":
        "Если защита включена, AdGuard перезапустится при применении изменений.",
    "Asks GitHub for the newest release.":
        "Запрашивает у GitHub последний выпуск.",
    "At a glance":
        "Сводка",
    "Automatic":
        "Автоматически",
    "Automatic – filter all apps":
        "Автоматический — фильтровать все приложения",
    "Benchmark":
        "Тест производительности",
    "Beta":
        "Бета",
    "Block ECH in DNS records":
        "Блокировать ECH в DNS-записях",
    "Block domains before a connection is made.":
        "Блокирует домены ещё до установки соединения.",
    "Block {}":
        "Блокировать {}",
    "Blocked (24 h)":
        "Заблокировано (24 ч)",
    "Browser list ({})":
        "Список браузеров ({})",
    "By ID or name…":
        "По ID или названию…",
    "Certificate":
        "Сертификат",
    "Certificate checks":
        "Проверки сертификатов",
    "Changes are collected in the bar at the bottom and applied together.":
        "Изменения собираются на панели внизу и применяются вместе.",
    "Check again":
        "Проверить снова",
    "Check every":
        "Интервал проверки",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "Браузеры на основе Chromium и Firefox используют собственное хранилище сертификатов.",
    "Close":
        "Закрыть",
    "Controls which AdGuard CLI build “{}” installs.":
        "Определяет, какую сборку AdGuard CLI устанавливает кнопка «{}».",
    "Could not add the rule.":
        "Не удалось добавить правило.",
    "Could not open {}":
        "Не удалось открыть {}",
    "Could not read {}":
        "Не удалось прочитать {}",
    "Could not refresh. Showing data from {}.":
        "Не удалось обновить. Показаны данные по состоянию на {}.",
    "Could not reset the history.":
        "Не удалось очистить историю.",
    "Could not restart AdGuard.":
        "Не удалось перезапустить AdGuard.",
    "Could not start protection.":
        "Не удалось запустить защиту.",
    "Could not stop protection.":
        "Не удалось остановить защиту.",
    "Create":
        "Создать",
    "Create certificate":
        "Создать сертификат",
    "Custom":
        "Свой",
    "DNS filter lists":
        "DNS-фильтры",
    "DNS filtering":
        "DNS-фильтрация",
    "DNS filtering is off, so these lists have no effect.":
        "DNS-фильтрация выключена, поэтому эти фильтры не действуют.",
    "DNS servers":
        "DNS-серверы",
    "Dark":
        "Тёмная",
    "Default":
        "По умолчанию",
    "Details":
        "Подробнее",
    "Discard":
        "Сбросить",
    "Don't filter":
        "Не фильтровать",
    "Don't trust":
        "Не доверять",
    "Downloads and installs the newest AdGuard CLI build.":
        "Скачивает и устанавливает новейшую сборку AdGuard CLI.",
    "Duration":
        "Длительность",
    "Export…":
        "Экспортировать…",
    "Filter everything":
        "Фильтровать всё",
    "Filter in place":
        "Фильтровать на месте",
    "Filtering":
        "Фильтрация",
    "Follow system":
        "Как в системе",
    "From URL…":
        "По URL…",
    "Go to updates":
        "К обновлениям",
    "HTTP proxy: {}":
        "HTTP-прокси: {}",
    "HTTPS filtering":
        "HTTPS-фильтрация",
    "How much detail AdGuard Tray writes to its own log.":
        "Насколько подробно AdGuard Tray записывает события в свой журнал.",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "Если сайт не загружается, сначала выключите фильтрацию HTTP/3. Остальные проверки защищают все сайты — выключайте их, только если это не помогло.",
    "Included":
        "Подключён",
    "Installed":
        "Установленные",
    "License":
        "Лицензия",
    "Light":
        "Светлая",
    "Logs":
        "Журналы",
    "MIT license":
        "Лицензия MIT",
    "Maintenance":
        "Обслуживание",
    "Manual proxy":
        "Ручной режим прокси",
    "Manual – only apps set to use the proxy":
        "Ручной — только приложения, настроенные на прокси",
    "More":
        "Ещё",
    "Move down":
        "Переместить вниз",
    "Move up":
        "Переместить вверх",
    "Network":
        "Сеть",
    "Nightly":
        "Nightly",
    "No requests yet – AdGuard logs requests while protection is on.":
        "Запросов пока нет — AdGuard записывает запросы, пока защита включена.",
    "Not added":
        "Не добавлен",
    "Nothing matches your search.":
        "Ничего не найдено.",
    "Notify me when protection turns on or off":
        "Уведомлять о включении и выключении защиты",
    "Off":
        "Выкл.",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "Влияет только на браузеры, использующие DoH или DoT. При значении «Выкл.» они обходят DNS-фильтрацию AdGuard.",
    "Open AdGuard Tray":
        "Открыть AdGuard Tray",
    "Open exceptions":
        "Открыть исключения",
    "Open folder":
        "Открыть папку",
    "Open release page":
        "Открыть страницу выпуска",
    "Pages":
        "Страницы",
    "Performance":
        "Производительность",
    "Protection":
        "Защита",
    "Protection started.":
        "Защита запущена.",
    "Protection stopped.":
        "Защита остановлена.",
    "Proxy mode":
        "Режим прокси",
    "Redirect to AdGuard's DNS":
        "Перенаправлять на DNS AdGuard",
    "Refresh this page (F5)":
        "Обновить страницу (F5)",
    "Release (stable)":
        "Релиз (стабильный)",
    "Remove rule":
        "Удалить правило",
    "Remove “{}”?":
        "Удалить «{}»?",
    "Remove…":
        "Удалить…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "Заменить текущие настройки AdGuard настройками из файла {}?\n\nAdGuard перезапустится, чтобы применить их.",
    "Reset history…":
        "Очистить историю…",
    "Reset…":
        "Сбросить…",
    "Restart AdGuard":
        "Перезапустить AdGuard",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "Правила действуют только в автоматическом режиме прокси. Применяется первое подходящее правило, поэтому правило \"*\" должно быть последним.",
    "Safe Browsing":
        "Защита от фишинга",
    "Save anyway":
        "Всё равно сохранить",
    "Saved. AdGuard restarts to apply the change.":
        "Сохранено. AdGuard перезапустится, чтобы применить изменение.",
    "Saved. Applies after AdGuard Tray restarts.":
        "Сохранено. Изменение вступит в силу после перезапуска AdGuard Tray.",
    "Saved. The change applies when protection is turned on.":
        "Сохранено. Изменение вступит в силу после включения защиты.",
    "Secure DNS and ECH":
        "Защищённый DNS и ECH",
    "Secure DNS filtering":
        "Фильтрация защищённого DNS",
    "Set the path in Settings":
        "Указать путь в разделе «Настройки»",
    "Settings":
        "Настройки",
    "Show":
        "Показать",
    "Show recent entries":
        "Показать последние записи",
    "Skip HTTPS filtering":
        "Без HTTPS-фильтрации",
    "Some counts could not be loaded.":
        "Не удалось загрузить некоторые показатели.",
    "Source code":
        "Исходный код",
    "Start AdGuard Tray when I log in":
        "Запускать AdGuard Tray при входе в систему",
    "Startup":
        "Запуск",
    "Status checks":
        "Проверка статуса",
    "Stealth mode":
        "Антитрекинг",
    "System":
        "Система",
    "The new lists load when protection is turned on.":
        "Новые фильтры загрузятся после включения защиты.",
    "Theme":
        "Тема",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "Будут выключены фильтрация HTTP/3, проверки OCSP, Certificate Transparency и фильтрация защищённого DNS. Отозванные или ошибочно выпущенные сертификаты останутся незамеченными, а браузеры смогут разрешать имена в обход DNS-фильтра AdGuard.",
    "Time range":
        "Период",
    "To keep it but stop using it, switch it off instead.":
        "Если хотите оставить его, но не использовать, выключите его вместо удаления.",
    "Top lists":
        "Топ-списки",
    "Trust":
        "Доверять",
    "Trust “{}”?":
        "Доверять «{}»?",
    "Trust…":
        "Доверять…",
    "Turn off all strict checks…":
        "Выключить все строгие проверки…",
    "Undo":
        "Отменить",
    "Unknown":
        "Неизвестно",
    "Unsaved changes":
        "Несохранённые изменения",
    "Update AdGuard CLI…":
        "Обновить AdGuard CLI…",
    "Update channel: {}":
        "Канал обновления: {}",
    "Updated {}":
        "Обновлено: {}",
    "Updates":
        "Обновления",
    "Used in manual mode only.":
        "Используется только в ручном режиме.",
    "Userscripts update together with filters.":
        "Пользовательские скрипты обновляются вместе с фильтрами.",
    "Uses XDG autostart (~/.config/autostart).":
        "Используется автозапуск XDG (~/.config/autostart).",
    "Waiting for authorization…":
        "Ожидание авторизации…",
    "Website exceptions":
        "Исключения для сайтов",
    "Websites":
        "Сайты",
    "example.com or a link":
        "example.com или ссылка",
    "expires {}":
        "истекает {}",
    "of {} requests in the last 24 hours":
        "всего запросов за 24 часа: {}",
    "{} of {} DNS filters on":
        "Включено DNS-фильтров: {} из {}",
    "{} of {} filters on":
        "Включено фильтров: {} из {}",
    "{} of {} on":
        "Включено: {} из {}",
    "{} unsaved changes to AdGuard's settings":
        "Несохранённых изменений в настройках AdGuard: {}",
    "“Follow system” uses your desktop's light or dark setting.":
        "Вариант «Как в системе» использует светлое или тёмное оформление рабочего стола.",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "Активна",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "Сертификат AdGuard будет добавлен во все профили браузеров, найденные в этой системе.\n\nЭто позволит AdGuard проверять HTTPS-трафик в этих браузерах. Сначала закройте браузеры — они читают хранилище сертификатов при запуске.",
    "Allow":
        "Разрешить",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "Сначала примените или сбросьте изменения в настройках AdGuard, а затем перезапустите программу.",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "Автоматический: AdGuard перенаправляет на себя трафик всех приложений через iptables. Ручной: AdGuard только прослушивает порты SOCKS5 и HTTP, указанные ниже.",
    "Block":
        "Блокировать",
    "Browser API blocking":
        "Блокировка API браузера",
    "CRLite":
        "CRLite",
    "Cancel":
        "Отмена",
    "Computers":
        "Компьютеры",
    "Could not change the autostart entry.":
        "Не удалось изменить запись автозапуска.",
    "Could not export the logs.":
        "Не удалось экспортировать журналы.",
    "Could not export the settings.":
        "Не удалось экспортировать настройки.",
    "Could not reset the license.":
        "Не удалось сбросить лицензию.",
    "Could not retrieve license info.":
        "Не удалось получить сведения о лицензии.",
    "Could not run the benchmark.":
        "Не удалось выполнить тест производительности.",
    "Could not save the settings.":
        "Не удалось сохранить настройки.",
    "Could not set the update channel.":
        "Не удалось задать канал обновления.",
    "Could not update AdGuard CLI.":
        "Не удалось обновить AdGuard CLI.",
    "Could not update the filters.":
        "Не удалось обновить фильтры.",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "Upstream DNS-сервер.\n'default' = системный DNS.\nПримеры: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com",
    "Expiration date":
        "Дата окончания",
    "Expires":
        "Истекает",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "HTTP/3 снова включён в профилях Firefox — перезапустите браузер.",
    "License key":
        "Лицензионный ключ",
    "License type":
        "Тип лицензии",
    "Manual":
        "Ручной",
    "No exceptions.":
        "Исключений нет.",
    "OK":
        "OK",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "Вкл.: AdGuard сам фильтрует HTTP/3 (QUIC) — экспериментально, к тому же некоторые\nбраузеры всё равно не принимают HTTP/3 через сертификат, установленный пользователем.\nВыкл.: AdGuard вместо этого блокирует QUIC, и браузеры переходят на HTTP/2,\nкоторый надёжно фильтруется.\nВ обоих случаях это действует только в автоматическом режиме — в ручном режиме\nHTTP/3-трафик вообще не доходит до AdGuard.",
    "Owner":
        "Владелец",
    "Personal":
        "Персональная",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "Режим прокси: {} — UDP-порт 443 перенаправляется на AdGuard.",
    "Save adguard-cli path":
        "Сохранить путь к adguard-cli",
    "Search domains or rules…":
        "Поиск доменов или правил…",
    "Settings file":
        "Файл настроек",
    "Status":
        "Статус",
    "Trial":
        "Пробная",
    "Turn HTTP/3 back on in Firefox profiles":
        "Снова включить HTTP/3 в профилях Firefox",
    "Turn off":
        "Выключить",
    "Turn off HTTP/3 in Firefox profiles":
        "Выключить HTTP/3 в профилях Firefox",
    "Turn off HTTP/3 in Firefox profiles…":
        "Выключить HTTP/3 в профилях Firefox…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "Выключить HTTP/3 в профилях браузеров семейства Firefox (количество: {})?\n\nИх трафик пойдёт через HTTP/2, который AdGuard может фильтровать. После этого перезапустите браузер.",
    "Turn off all strict checks":
        "Выключить все строгие проверки",
    "Unavailable until AdGuard CLI reports its current channel.":
        "Недоступно, пока AdGuard CLI не сообщит текущий канал.",
    "Update AdGuard CLI":
        "Обновить AdGuard CLI",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "Используется только в автоматическом режиме. Диапазоны (80:5221,5300:49151) или отдельные порты (80,443,8080).",
    "{} of {}":
        "{} из {}",
    "{} of {} userscripts on":
        "Включено скриптов: {} из {}",
    "{}% blocked":
        "{} % заблокировано",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "Раздражители",
    "General":
        "Общие",
    "Language-specific":
        "Языковые",
    "Security":
        "Безопасность",
    "Social widgets":
        "Виджеты соцсетей",
    "Expired":
        "Истекла",
    "Autostart on login":
        "Автозапуск при входе в систему",
    "Add app rule":
        "Добавить правило для приложения",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "Можно использовать подстановочные знаки, например *steam* или *EasyAntiCheat*.",
    "There is already a rule for '{}'.":
        "Правило для «{}» уже существует.",
    "AdGuard settings":
        "Настройки AdGuard",
    "Ads and trackers are not blocked until you enable protection.":
        "Реклама и трекеры не блокируются, пока вы не включите защиту.",
    "Could not import the settings.":
        "Не удалось импортировать настройки.",
    "Disable protection":
        "Выключить защиту",
    "Enable protection":
        "Включить защиту",
    "Export and import":
        "Экспорт и импорт",
    "Features":
        "Функции",
    "Import settings":
        "Импортировать настройки",
    "Import settings from…":
        "Импорт настроек из…",
    "Import settings…":
        "Импортировать настройки…",
    "Import…":
        "Импортировать…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "Сохранить фильтры, правила и конфигурацию в zip-архив или загрузить их из него.",
    "Update":
        "Обновить",
    "Version":
        "Версия",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "Файл {} не содержит экспортированных настроек. Выберите файл, сохранённый кнопкой «Экспортировать…» в разделе «Настройки AdGuard».",

    # ── AdGuard VPN, outbound proxy, install ──────────────────────────
    "Press Enter to close this window.":
        "Нажмите Enter, чтобы закрыть это окно.",
    "No terminal app was found. The install command is on the clipboard: paste it into a terminal.":
        "Приложение терминала не найдено. Команда установки скопирована в буфер обмена: вставьте её в терминал.",
    "Finish the installation in the terminal, then press Refresh.":
        "Завершите установку в терминале, затем нажмите «Обновить».",
    "Open in a terminal":
        "Открыть в терминале",
    "AdGuard VPN":
        "AdGuard VPN",
    "AdGuard's VPN for Linux (adguardvpn-cli) runs next to AdGuard CLI. AdGuard Tray checks that their settings fit together; it does not connect the VPN or log in.":
        "VPN от AdGuard для Linux (adguardvpn-cli) работает вместе с AdGuard CLI. AdGuard Tray проверяет, согласованы ли их настройки, но не подключает VPN и не выполняет вход в учётную запись.",
    "Install…":
        "Установить…",
    "Outbound proxy":
        "Исходящий прокси",
    "AdGuard sends its own connections through this proxy, for example through AdGuard VPN in SOCKS5 mode.":
        "AdGuard направляет собственные подключения через этот прокси, например через AdGuard VPN в режиме SOCKS5.",
    "Use an outbound proxy":
        "Использовать исходящий прокси",
    "Host":
        "Хост",
    "Port":
        "Порт",
    "Not installed.":
        "Не установлено.",
    "AdGuard VPN is set to TUN mode while AdGuard filters in automatic mode. Connected like this, traffic loops between the two – AdGuard does not support this combination.":
        "AdGuard VPN настроен на режим TUN, а AdGuard фильтрует трафик в автоматическом режиме. При таком подключении трафик зацикливается между ними — AdGuard не поддерживает такое сочетание.",
    "AdGuard VPN now uses SOCKS5 mode. Press Apply to send AdGuard's traffic through it, and reconnect AdGuard VPN if it is connected.":
        "AdGuard VPN теперь использует режим SOCKS5. Нажмите «Применить», чтобы направить через него трафик AdGuard, и переподключите AdGuard VPN, если он подключён.",
    "AdGuard VPN CLI":
        "AdGuard VPN CLI",
    "Installed, but its settings could not be read: {}":
        "Установлено, но не удалось прочитать настройки: {}",
    "Route AdGuard through the VPN":
        "Направить AdGuard через VPN",
    "Could not switch AdGuard VPN to SOCKS5 mode.":
        "Не удалось переключить AdGuard VPN в режим SOCKS5.",
    "Installed · SOCKS5 mode on {}:{}":
        "Установлено · режим SOCKS5 на {}:{}",
    "Installed · TUN mode":
        "Установлено · режим TUN",
    "Installed · {} mode":
        "Установлено · режим {}",
}
