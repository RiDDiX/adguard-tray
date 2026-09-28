"""Ukrainian."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "Мова",
    "English":                           "Англійська",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "Активно – захист працює",
    "Inactive – Protection stopped":        "Неактивно – захист зупинено",
    "Error retrieving status":              "Помилка отримання стану",
    "adguard-cli not found":                "adguard-cli не знайдено",
    "Unknown status":                       "Невідомий стан",
    "Checking status…":                     "Перевірка стану…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "Перезапустити",
    "Filters":                              "Фільтри",
    "Loading…":                             "Завантаження…",
    "Manage filters…":                      "Керувати фільтрами…",
    "No userscripts installed":             "Немає встановлених користувацьких скриптів",
    "Manage userscripts…":                  "Керувати користувацькими скриптами…",
    "Quit":                                 "Вийти",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "увімкнено",
    "inactive":                             "вимкнено",
    "System-wide filtering: {}":            "Загальносистемне фільтрування: {}",
    "Error: {}":                            "Помилка: {}",
    "AdGuard Tray – Error":                 "AdGuard Tray – помилка",
    "AdGuard is now active – protection running.":
        "AdGuard увімкнено – захист працює.",
    "AdGuard has been stopped.":
        "AdGuard зупинено.",
    "Could not retrieve status.":
        "Не вдалося отримати стан.",
    "Command failed":                       "Не вдалося виконати команду",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " с",
    "How often adguard-cli status is checked automatically.":
        "Як часто автоматично перевіряється стан adguard-cli.",
    "Log level:":                           "Рівень журналювання:",
    "adguard-cli path:":                    "Шлях до adguard-cli:",
    "auto-detect via PATH":                 "автовизначення через PATH",
    "Browse…":                              "Вибрати…",
    "Select adguard-cli binary":            "Виберіть виконуваний файл adguard-cli",
    "Notifications":                        "Сповіщення",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "Оновити фільтри",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "Оновлює всі фільтри, DNS-фільтри, користувацькі скрипти,\nSafebrowsingV2, CRLite і перевіряє наявність оновлень програми.",
    "No filters found.":                    "Фільтрів не знайдено.",
    "Updating filters… (can take up to 2 minutes)":
        "Оновлення фільтрів… (може тривати до 2 хвилин)",
    "Update completed.":                    "Оновлення завершено.",
    "Update failed.":                       "Помилка оновлення.",
    "Installing: {}":                       "Встановлення: {}",
    "Filter installed.":                    "Фільтр встановлено.",
    "Remove":                               "Вилучити",
    "Remove filter":                        "Вилучити фільтр",
    "Filter {} removed.":                   "Фільтр {} вилучено.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        "Встановити користувацький скрипт за прямим посиланням на .js",
    "No userscripts installed.":            "Немає встановлених користувацьких скриптів.",
    "Userscript URL (direct .js URL):":     "URL користувацького скрипту (пряме посилання на .js):",
    "Userscript installed.":                "Користувацький скрипт встановлено.",
    'Remove "{}"':                          "Вилучити «{}»",
    "Remove userscript":                    "Вилучити користувацький скрипт",
    "'{}' removed.":                        "«{}» вилучено.",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "adguard-cli не знайдено.\nВстановіть його за допомогою офіційного скрипту або з AUR:\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "Невідома помилка отримання стану",
    "AdGuard {} ok":                        "AdGuard {}: успішно",
    "AdGuard via systemctl {} ok":          "AdGuard через systemctl {}: успішно",
    "'{}' failed – insufficient privileges?":
        "Не вдалося виконати «{}» – недостатньо прав?",
    "Could not retrieve filter list":
        "Не вдалося отримати список фільтрів",
    "Filter {} enabled":                    "Фільтр {} увімкнено",
    "Could not enable filter {}":           "Не вдалося увімкнути фільтр {}",
    "Filter {} disabled":                   "Фільтр {} вимкнено",
    "Could not disable filter {}":
        "Не вдалося вимкнути фільтр {}",
    "Filter installed":                     "Фільтр встановлено",
    "Installation failed":                  "Помилка встановлення",
    "Filter {} removed":                    "Фільтр {} вилучено",
    "Could not remove filter {}":
        "Не вдалося вилучити фільтр {}",
    "Filters updated":                      "Фільтри оновлено",
    "Update failed":                        "Помилка оновлення",
    "Could not retrieve userscript list":
        "Не вдалося отримати список користувацьких скриптів",
    "Userscript '{}' enabled":              "Користувацький скрипт «{}» увімкнено",
    "Could not enable userscript '{}'":
        "Не вдалося увімкнути користувацький скрипт «{}»",
    "Userscript '{}' disabled":             "Користувацький скрипт «{}» вимкнено",
    "Could not disable userscript '{}'":
        "Не вдалося вимкнути користувацький скрипт «{}»",
    "Userscript '{}' removed":              "Користувацький скрипт «{}» вилучено",
    "Could not remove userscript '{}'":
        "Не вдалося вилучити користувацький скрипт «{}»",
    "Userscript installed":                 "Користувацький скрипт встановлено",
    "Other":                                "Інше",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "Пошук фільтрів…",
    "Search userscripts…":              "Пошук користувацьких скриптів…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "Не вдалося завантажити proxy.yaml.\nШлях: {}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "Застосунки",
    "Mode:":                            "Режим:",
    "Filtered ports:":                  "Фільтровані порти:",
    "SOCKS5 port:":                     "Порт SOCKS5:",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "Порт SOCKS5-проксі для ручного режиму.\nУкажіть -1, щоб вимкнути.",
    "HTTP port:":                       "Порт HTTP:",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "Порт HTTP-проксі для ручного режиму.\nУкажіть -1, щоб вимкнути.",
    "Listen address:":                  "Адреса прослуховування:",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "Адреса, яку прослуховує проксі.\n127.0.0.1 = лише локально. 0.0.0.0 = усі інтерфейси (потрібна автентифікація).",
    "Worker threads:":                  "Робочі потоки:",
    "Number of proxy worker threads.":  "Кількість робочих потоків проксі.",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "Розшифровувати й фільтрувати HTTPS-трафік.\nПотрібно для блокування реклами на сайтах з https.\nПотребує довіреного кореневого сертифіката, встановленого в системі.",
    "Enable TLS 1.3":                   "Увімкнути TLS 1.3",
    "Enable TLS 1.3 support for filtered connections.":
        "Увімкнути підтримку TLS 1.3 для фільтрованих з’єднань.",
    "Filter HTTP/3 (QUIC) – experimental":
        "Фільтрувати HTTP/3 (QUIC) – експериментально",
    "OCSP certificate checks":          "Перевірки сертифікатів OCSP",
    "Enforce Certificate Transparency": "Вимагати Certificate Transparency",
    "Filter EV certificate sites":      "Фільтрувати сайти з EV-сертифікатами",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "Типово сайти із сертифікатами Extended Validation не фільтруються.\nУвімкніть, щоб фільтрувати і їх (напр. сайти банків).",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "Увімкнути ECH для кращої конфіденційності.\nПотребує ввімкненого DNS-фільтрування.",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "Фільтрувати запити DNS, щоб блокувати рекламу й трекери на рівні DNS.\nВикористовує локальний DNS-проксі з налаштовуваними основними серверами.",
    "Upstream:":                        "Основний сервер:",
    "Fallbacks:":                       "Резервні сервери:",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "Резервні DNS-сервери (використовуються, коли основний сервер недоступний).\n'default' = системний DNS. Список через пробіл.\nПриклад: default 1.1.1.1",
    "Bootstraps:":                      "Bootstrap-сервери:",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "Bootstrap-DNS для визначення IP-адрес основних серверів за іменами хостів.\n'default' = IP-адреси системного DNS. Дозволено лише IP-адреси.\nПриклад: default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "Вилучати параметр ECH із DNS-записів SVCB/HTTPS.\nУвімкніть лише для браузерів, які не виявляють HTTPS-фільтрування автоматично.",
    "Master switch for all tracking protection features below.":
        "Головний перемикач для всіх наведених нижче функцій захисту від відстеження.",
    "Cookies":                          "Файли cookie",
    "Block third-party cookies":        "Блокувати файли cookie третіх сторін",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "Видаляти файли cookie третіх сторін через заданий час.\nЗапобігає міжсайтовому відстеженню.",
    "Lifetime (minutes):":              "Строк дії (хв):",
    "0 = block immediately. Default: 180 minutes.":
        "0 = блокувати відразу. Типово: 180 хвилин.",
    "Block first-party cookies":        "Блокувати файли cookie основного сайту",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "Видаляти всі файли cookie (зокрема основного сайту) через заданий час.\nУвага: це призведе до виходу з усіх сайтів.",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = блокувати відразу. Типово: 4320 хвилин (3 дні).",
    "Privacy":                          "Конфіденційність",
    "Hide / reduce User-Agent":         "Приховувати / скорочувати User-Agent",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "Вилучає з User-Agent дані, які можуть вас ідентифікувати.\nУскладнює визначення цифрового відбитка.",
    "Hide search queries in referrer":  "Приховувати пошукові запити в реферері",
    "Hides your search terms when clicking from a search engine to a website.":
        "Приховує ваші пошукові запити під час переходу з пошукової системи на сайт.",
    "Remove referrer from third-party requests":
        "Вилучати реферер із запитів третіх сторін",
    "Prevents third-party sites from knowing which page you came from.":
        "Не дає сайтам третіх сторін дізнатися, з якої сторінки ви прийшли.",
    "Send Do-Not-Track signal":         "Надсилати сигнал Do-Not-Track",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "Надсилає заголовок DNT разом із запитами.\nПримітка: більшість сайтів його ігнорує, але деякі враховують.",
    "Disable third-party ETag cache":   "Вимкнути кеш ETag третіх сторін",
    "Prevents tracking via ETag caching in third-party content.":
        "Запобігає відстеженню через кешування ETag у вмісті третіх сторін.",
    "Block third-party Authorization header":
        "Блокувати заголовок Authorization третіх сторін",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "Блокує заголовок Authorization у запитах третіх сторін, щоб запобігти відстеженню.",
    "Remove X-Client-Data header":      "Вилучати заголовок X-Client-Data",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "Вилучає заголовок X-Client-Data, який Chrome надсилає сервісам Google.",
    "Block WebRTC":                     "Блокувати WebRTC",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "Запобігає витоку IP-адреси через WebRTC.\nМоже порушити роботу відеодзвінків і деяких вебзастосунків.",
    "Block Push API":                   "Блокувати Push API",
    "Blocks browser push notifications from websites.":
        "Блокує push-сповіщення браузера від сайтів.",
    "Block Location API":               "Блокувати Location API",
    "Prevents websites from accessing your GPS location.":
        "Не дає сайтам доступу до вашого місцезнаходження GPS.",
    "Block Flash":                      "Блокувати Flash",
    "Blocks the Flash plugin.":
        "Блокує додаток Flash.",
    "Block Java":                       "Блокувати Java",
    "Disables Java plugins. JavaScript remains enabled.":
        "Вимикає додатки Java. JavaScript залишається ввімкненим.",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "Увімкнути Anti-DPI",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "Змінює дані вихідних пакетів, щоб обійти глибоку перевірку пакетів (DPI).\nКорисно в країнах з інтернет-цензурою.",
    "App pattern":
        "Шаблон застосунку",
    "Skip outbound proxy":              "Оминати вихідний проксі",
    "Don't route this app's traffic through outbound proxy":
        "Не спрямовувати трафік цього застосунку через вихідний проксі",
    "Browser list included from {}":    "Список браузерів включено з файлу {}",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "Включений список браузерів і правило із символом-замінником (*) вилучити не можна.",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "Попереджає про шкідливі та фішингові сайти.\nВикористовує базу даних Безпечного перегляду AdGuard.",
    "Send anonymous statistics":        "Надсилати анонімну статистику",
    "Send anonymous lookups to AdGuard.":
        "Надсилати анонімні запити перевірки до AdGuard.",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "Перевірка відкликання сертифікатів за допомогою CRLite від Mozilla.\nШвидша й надійніша за традиційні перевірки CRL/OCSP.",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "Застосовувати правила блокування реклами до запитів HTTP/HTTPS.",
    "Save failed":                      "Не вдалося зберегти",
    "Could not save proxy.yaml:\n{}":   "Не вдалося зберегти proxy.yaml:\n{}",
    "Restarting AdGuard…":              "Перезапуск AdGuard…",
    "AdGuard restarted.":               "AdGuard перезапущено.",
    "Restart failed: {}":               "Помилка перезапуску: {}",
    "Unknown error":                    "Невідома помилка",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "Додати",
    "Search exceptions…":               "Пошук винятків…",
    "1 exception":                      "1 виняток",
    "{} exceptions":                    "Винятки: {}",
    "'{}' is not a valid domain or IP address.":
        "«{}» не є коректним доменом або IP-адресою.",
    "'{}' is already in the list.":     "«{}» уже є в списку.",
    "Could not save exceptions:\n{}":
        "Не вдалося зберегти винятки:\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "Огляд",
    "Userscripts":                      "Користувацькі скрипти",
    "Exceptions":                       "Винятки",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "Скинути ліцензію",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "Створити кореневий сертифікат CA для HTTPS-фільтрування. Сертифікат потрібно встановити у вашій системі та позначити як довірений.",
    "Checking for updates…":            "Пошук оновлень…",
    "Firefox profile:":                 "Профіль Firefox:",
    "(optional) e.g. abcd1234.MyProfile":
        "(необов’язково) напр. abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "Введіть ID або назву фільтра:",
    "Filter added.":                    "Фільтр додано.",
    "Rename…":                          "Перейменувати…",
    "Rename filter":                    "Перейменувати фільтр",
    "New title:":                       "Нова назва:",
    "Filter renamed.":                  "Фільтр перейменовано.",
    "Filter trust updated.":            "Рівень довіри до фільтра оновлено.",
    "Filter URL:":                      "URL фільтра:",
    "Title:":                           "Назва:",
    "(optional)":                       "(необов’язково)",
    "Trusted filter":                   "Довірений фільтр",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "Пошук DNS-фільтрів…",
    "No DNS filters found.":            "DNS-фільтрів не знайдено.",
    "DNS filter installed.":            "DNS-фільтр встановлено.",
    "DNS filter added.":                "DNS-фільтр додано.",
    "Remove DNS filter":                "Вилучити DNS-фільтр",
    "DNS filter {} removed.":           "DNS-фільтр {} вилучено.",
    "Rename DNS filter":                "Перейменувати DNS-фільтр",
    "DNS filter renamed.":              "DNS-фільтр перейменовано.",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "Експортувати журнали…",
    "Export AdGuard CLI logs to a zip file":
        "Експортувати журнали AdGuard CLI у zip-файл",
    "Export settings…":                 "Експортувати налаштування…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "Запустити тест продуктивності криптографії та HTTPS-фільтрування.",
    "Run benchmark":                    "Запустити тест",
    "Done.":                            "Готово.",
    "Export logs to…":                  "Експортувати журнали до…",
    "Export settings to…":              "Експортувати налаштування до…",
    "Zip files (*.zip);;All files (*)":
        "Zip-файли (*.zip);;Усі файли (*)",
    "Log file not found.":              "Файл журналу не знайдено.",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "Не вдалося отримати список DNS-фільтрів",
    "DNS filter {} enabled":            "DNS-фільтр {} увімкнено",
    "Could not enable DNS filter {}":   "Не вдалося увімкнути DNS-фільтр {}",
    "DNS filter {} disabled":           "DNS-фільтр {} вимкнено",
    "Could not disable DNS filter {}":  "Не вдалося вимкнути DNS-фільтр {}",
    "DNS filter installed":             "DNS-фільтр встановлено",
    "DNS filter {} removed":            "DNS-фільтр {} вилучено",
    "Could not remove DNS filter {}":   "Не вдалося вилучити DNS-фільтр {}",
    "DNS filter added":                 "DNS-фільтр додано",
    "Could not add DNS filter":         "Не вдалося додати DNS-фільтр",
    "DNS filter title updated":         "Назву DNS-фільтра оновлено",
    "Could not set DNS filter title":   "Не вдалося задати назву DNS-фільтра",
    "Filter added":                     "Фільтр додано",
    "Could not add filter":             "Не вдалося додати фільтр",
    "Filter trust updated":             "Рівень довіри до фільтра оновлено",
    "Could not update filter trust":    "Не вдалося оновити рівень довіри до фільтра",
    "Filter title updated":             "Назву фільтра оновлено",
    "Could not set filter title":       "Не вдалося задати назву фільтра",
    "License reset":                    "Ліцензію скинуто",
    "Could not reset license":          "Не вдалося скинути ліцензію",
    "Could not retrieve license info":  "Не вдалося отримати відомості про ліцензію",
    "Certificate generated":            "Сертифікат створено",
    "Certificate generation failed":    "Помилка створення сертифіката",
    "Logs exported":                    "Журнали експортовано",
    "Log export failed":                "Помилка експорту журналів",
    "Settings exported":                "Налаштування експортовано",
    "Settings export failed":           "Помилка експорту налаштувань",
    "Settings imported":                "Налаштування імпортовано",
    "Settings import failed":           "Помилка імпорту налаштувань",
    "Update check completed":           "Перевірку оновлень завершено",
    "Update check failed":              "Не вдалося перевірити оновлення",
    "Benchmark failed":                 "Помилка тесту продуктивності",
    "AdGuard stopped (forced)":         "AdGuard зупинено (примусово)",
    "Could not stop AdGuard – process may still be running":
        "Не вдалося зупинити AdGuard – процес, можливо, досі працює",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "adguard-cli не знайдено в цій системі.\n\nРекомендований спосіб встановлення (офіційний):\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\nАльтернативний спосіб (Arch Linux AUR):\n  paru -S adguard-cli-bin\n\nAdGuard Tray завантажиться, але запуск і зупинка не працюватимуть, доки не буде встановлено adguard-cli.",
    "Copy install command":             "Копіювати команду встановлення",
    "Continue":                         "Продовжити",
    "AdGuard Tray is already running":  "AdGuard Tray уже запущено",
    "Only one instance can run at a time. Check your system tray.":
        "Одночасно може працювати лише один екземпляр. Перевірте системний лоток.",
    "Authentication cancelled":         "Автентифікацію скасовано",
    "Authorization failed":             "Помилка авторизації",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "Перевіряти, чи не відкликано сертифікат сайту (OCSP).\nAdGuard перевіряє асинхронно й пропускає з’єднання, якщо\nперевірка триває довго, тож це рідко порушує роботу сайтів – не вимикайте\nїї, якщо не з’ясували, що проблема саме в ній.",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "Вимагати перевірок Certificate Transparency (політика CT у Chrome).\nСайти, чий власний сертифікат не відповідає вимогам CT, перестають\nфільтруватися, і браузер може їх відхилити. Великі сайти відповідають\nвимогам, тож вимикайте це лише для сайту, що показує помилку сертифіката.",
    "Sites that don't load":
        "Сайти, що не завантажуються",
    "Turn off HTTP/3 filtering":
        "Вимкнути фільтрування HTTP/3",
    "No filters installed":
        "Немає встановлених фільтрів",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "Протокол HTTP/3 заблоковано правилом брандмауера; браузери використовують HTTP/2.",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "Застосунки, для яких вимкнено фільтрування (їхній трафік HTTP/3 також не фільтрується): {}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuard не працює – нічого не фільтрується.",
    "could not remove the previous certificate":
        "не вдалося вилучити попередній сертифікат",
    "HTTP/3 state unknown":
        "Стан HTTP/3 невідомий",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "Правило брандмауера відхиляє вихідний трафік UDP 443, тому QUIC недоступний.",
    "Browser policy disables QUIC: {}":
        "Політика браузера вимикає QUIC: {}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "Браузери можуть оминати AdGuard через HTTP/3 (UDP 443).",
    "Checking…":
        "Перевірка…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "Не вдалося прочитати proxy.yaml – стан HTTP/3 невідомий.",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "Профілі сімейства Firefox із вимкненим HTTP/3: {} з {}",
    "HTTP/3 (QUIC)":
        "HTTP/3 (QUIC)",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "AdGuard блокує HTTP/3; браузери переходять на HTTP/2, який фільтрується.",
    "HTTP/3 is filtered by AdGuard.":
        "AdGuard фільтрує HTTP/3.",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "HTTP/3 вимкнено в профілях Firefox – перезапустіть браузер.",
    "HTTPS filtering is off – nothing is filtered.":
        "HTTPS-фільтрування вимкнено – нічого не фільтрується.",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "Режим проксі: {} – фільтрується лише трафік, що йде через проксі, а QUIC браузери через нього не надсилають.",
    "unknown":
        "невідомо",
    "AdGuard's certificate was not found. Generate it first.":
        "Сертифікат AdGuard не знайдено. Спочатку створіть його.",
    "Certificate could not be installed in any browser.":
        "Не вдалося встановити сертифікат у жоден браузер.",
    "Certificate installed for {} of {} stores.":
        "Сертифікат встановлено у сховища: {} з {}.",
    "Chromium-based browsers":
        "Браузери на основі Chromium",
    "No browser certificate stores found.":
        "Сховищ сертифікатів браузерів не знайдено.",
    "Restart your browsers for the certificate to take effect.":
        "Перезапустіть браузери, щоб сертифікат почав діяти.",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "Запустіть це без sudo/pkexec – сертифікат встановлюється у ваші власні профілі браузерів",
    "certificate not found after import":
        "сертифікат не знайдено після імпорту",
    "certutil not found – install the 'nss' package":
        "certutil не знайдено – встановіть пакунок «nss»",
    "not found":
        "не знайдено",
    "Could not read the filter list (unexpected CLI output).":
        "Не вдалося прочитати список фільтрів (неочікуваний вивід CLI).",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "Системний лоток не знайдено. AdGuard Tray працює без значка — увімкніть лоток/AppIndicator на панелі.",
    "URL must start with http:// or https://":
        "URL має починатися з http:// або https://",
    "adguard-cli path does not exist or is not executable.":
        "Шлях до adguard-cli не існує або файл не є виконуваним.",
    "That binary does not identify as adguard-cli. Save anyway?":
        "Цей виконуваний файл не ідентифікує себе як adguard-cli. Усе одно зберегти?",
    "Update channel":                   "Канал оновлень",
    "Switching update channel to {}…":  "Перемикання каналу оновлень: {}…",
    "Update channel set to {}":         "Встановлено канал оновлень: {}",
    "Could not set update channel":     "Не вдалося встановити канал оновлень",
    "Invalid channel: {}":              "Некоректний канал: {}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        "Журналу доступу ще немає ({}). AdGuard створює його, щойно відфільтрує трафік; якщо AdGuard працює як системна служба, журнал належить root і тут недоступний для читання.",
    'Cannot read the access log ({}): {}':
        "Не вдалося прочитати журнал доступу ({}): {}",
    'Blocked':
        "Заблоковано",
    'Blocked only':
        "Лише заблоковані",
    "Refresh":
        "Оновити",
    'Allow selected domain':
        "Дозволити вибраний домен",
    'Block selected domain':
        "Заблокувати вибраний домен",
    'Activity':
        "Активність",
    'Time':
        "Час",
    'Domain':
        "Домен",
    'Result':
        "Результат",
    'Rule':
        "Правило",
    'Size':
        "Розмір",
    'Count':
        "Кількість",
    'Could not read the access log.':
        "Не вдалося прочитати журнал доступу.",
    '{} lines not understood':
        "Нерозпізнані рядки: {}",
    'Not a valid domain: {}':
        "Некоректний домен: {}",
    'Source: {}':
        "Джерело: {}",
    'Allowed':
        "Дозволено",
    'Added rule: {}':
        "Додано правило: {}",
    'Requests per hour, {} to {} · busiest hour: {}':
        "Запити за годинами, {} – {} · пікова година: {}",
    'Last 24 hours':
        "Останні 24 години",
    'Last 7 days':
        "Останні 7 днів",
    'Requests':
        "Запити",
    'Traffic':
        "Трафік",

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        "Доступна версія {} (у вас {}).",
    'Application update':
        "Оновлення програми",
    'Check for update':
        "Перевірити оновлення",
    'Install update':
        "Встановити оновлення",
    'Installing update…':
        "Встановлення оновлення…",
    'Restart now':
        "Перезапустити зараз",
    'Later':
        "Пізніше",
    'You are running the latest version ({}).':
        "У вас найновіша версія ({}).",
    'Installation not recognised':
        "Спосіб встановлення не розпізнано",
    'Could not check for updates.':
        "Не вдалося перевірити оновлення.",
    'Update with: {}':
        "Команда оновлення: {}",
    'Installed with the AUR package {}':
        "Встановлено з пакунка AUR {}",
    'Installed in {}':
        "Встановлено в теці {}",
    'Running from a source checkout':
        "Запущено з робочої копії вихідного коду",
    'Version {} installed. Restart adguard-tray to use it.':
        "Версію {} встановлено. Перезапустіть adguard-tray, щоб використовувати її.",
    'Unexpected answer from GitHub: {}':
        "Неочікувана відповідь від GitHub: {}",
    'Download failed: {}':
        "Помилка завантаження: {}",
    'Could not unpack the download: {}':
        "Не вдалося розпакувати завантажений файл: {}",
    'This installation is managed elsewhere: {}':
        "Цим встановленням керують в інший спосіб: {}",
    'No permission to write to {}':
        "Немає дозволу на запис до {}",
    'GitHub returned {}.':
        "GitHub повернув код {}.",
    'No connection to GitHub: {}':
        "Немає з’єднання з GitHub: {}",
    'The download does not contain adguard-tray.':
        "Завантажений файл не містить adguard-tray.",
    'The download says version {} instead of {} – aborted.':
        "Завантажений файл містить версію {} замість {} – перервано.",
    'GitHub is rate limiting this address. Try again later.':
        "GitHub обмежує частоту запитів із цієї адреси. Спробуйте пізніше.",
    'The download is larger than expected – aborted.':
        "Завантажений файл більший за очікуваний – перервано.",
    'Update failed: {}':
        "Помилка оновлення: {}",
    'The archive contains unexpected paths – aborted.':
        "Архів містить неочікувані шляхи – перервано.",
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        "Помилка оновлення: попередню версію відновити не вдалося. Відновіть її з теки {} або перевстановіть командою: {}",
    'Last 30 days':
        "Останні 30 днів",
    'All time':
        "Увесь час",
    'Modified':
        "Змінено",
    'Rules':
        "Правила",
    'Showing {} – show all':
        "Показано {} – показати все",
    'history {}':
        "історія: {}",
    'Filter list ID: {}':
        "ID списку фільтрування: {}",
    'App':
        "Застосунок",
    'Protocol':
        "Протокол",
    'Type':
        "Тип",
    'Reset history':
        "Скинути історію",
    'Delete the stored history and read the log again.':
        "Видалити збережену історію та знову прочитати журнал.",
    'Delete the stored history? Only what the log still holds can be read back.':
        "Видалити збережену історію? Відновити можна буде лише те, що ще є в журналі.",
    'History is not being updated: {}':
        "Історія не оновлюється: {}",

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "1 незбережена зміна в налаштуваннях AdGuard",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "Довірений фільтр може запускати скрипти на сторінках, які ви відвідуєте. Довіряйте лише спискам із відомих вам джерел.",
    "About":
        "Про програму",
    "Actions for the selected filter":
        "Дії з вибраним фільтром",
    "Ad blocking":
        "Блокування реклами",
    "Ad blocking is off, so the filter lists below have no effect.":
        "Блокування реклами вимкнено, тому наведені нижче списки фільтрування не діють.",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLI завантажить і встановить свою найновішу збірку.",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "AdGuard CLI забуде ліцензію на цьому комп’ютері. Вам доведеться активувати її знову.",
    "AdGuard CLI logs":
        "Журнали AdGuard CLI",
    "AdGuard CLI update finished.":
        "Оновлення AdGuard CLI завершено.",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "Журнал AdGuard Tray",
    "AdGuard doesn't filter these websites.":
        "AdGuard не фільтрує ці сайти.",
    "AdGuard is filtering this computer's traffic.":
        "AdGuard фільтрує трафік цього комп’ютера.",
    "AdGuard restarts to load the new lists.":
        "AdGuard перезапуститься, щоб завантажити нові списки.",
    "AdGuard's reply did not say whether it is running.":
        "З відповіді незрозуміло, чи AdGuard працює.",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "Файл налаштувань AdGuard не знайдено ({}). Запустіть adguard-cli один раз, щоб створити його.",
    "Add DNS filter by ID":
        "Додати DNS-фільтр за ID",
    "Add DNS filter from URL":
        "Додати DNS-фільтр за URL",
    "Add filter":
        "Додати фільтр",
    "Add filter by ID":
        "Додати фільтр за ID",
    "Add filter from URL":
        "Додати фільтр за URL",
    "Add rule":
        "Додати правило",
    "Add to browsers":
        "Додати до браузерів",
    "Add userscript":
        "Додати користувацький скрипт",
    "Add userscript…":
        "Додати користувацький скрипт…",
    "Add website":
        "Додати сайт",
    "Add…":
        "Додати…",
    "Advanced":
        "Додатково",
    "All available":
        "Усі доступні",
    "Allow {}":
        "Дозволити {}",
    "Also adds the certificate to this Firefox profile.":
        "Також додає сертифікат до цього профілю Firefox.",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "Також про перезапуски та помилки. Потрібен notify-send (libnotify) або запущена служба сповіщень, як-от dunst, mako чи служба KDE.",
    "Appearance":
        "Вигляд",
    "Applies after AdGuard Tray restarts.":
        "Застосовується після перезапуску AdGuard Tray.",
    "Apply":
        "Застосувати",
    "Apply your changes to AdGuard's settings before closing?":
        "Застосувати зміни в налаштуваннях AdGuard перед закриттям?",
    "Applying them restarts AdGuard if protection is on.":
        "Якщо захист увімкнено, після застосування змін AdGuard перезапуститься.",
    "Asks GitHub for the newest release.":
        "Запитує в GitHub найновіший випуск.",
    "At a glance":
        "Коротко",
    "Automatic":
        "Автоматично",
    "Automatic – filter all apps":
        "Автоматичний – фільтрувати всі застосунки",
    "Benchmark":
        "Тест продуктивності",
    "Beta":
        "Бета",
    "Block ECH in DNS records":
        "Блокувати ECH у записах DNS",
    "Block domains before a connection is made.":
        "Блокування доменів ще до встановлення з’єднання.",
    "Block {}":
        "Заблокувати {}",
    "Blocked (24 h)":
        "Заблоковано (24 год)",
    "Browser list ({})":
        "Список браузерів ({})",
    "By ID or name…":
        "За ID або назвою…",
    "Certificate":
        "Сертифікат",
    "Certificate checks":
        "Перевірки сертифікатів",
    "Changes are collected in the bar at the bottom and applied together.":
        "Зміни збираються на панелі внизу й застосовуються разом.",
    "Check again":
        "Перевірити знову",
    "Check every":
        "Перевіряти кожні",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "Браузери на основі Chromium і Firefox мають власне сховище сертифікатів.",
    "Close":
        "Закрити",
    "Controls which AdGuard CLI build “{}” installs.":
        "Визначає, яку збірку AdGuard CLI встановлює кнопка «{}».",
    "Could not add the rule.":
        "Не вдалося додати правило.",
    "Could not open {}":
        "Не вдалося відкрити {}",
    "Could not read {}":
        "Не вдалося прочитати {}",
    "Could not refresh. Showing data from {}.":
        "Не вдалося оновити. Показано дані станом на {}.",
    "Could not reset the history.":
        "Не вдалося скинути історію.",
    "Could not restart AdGuard.":
        "Не вдалося перезапустити AdGuard.",
    "Could not start protection.":
        "Не вдалося увімкнути захист.",
    "Could not stop protection.":
        "Не вдалося вимкнути захист.",
    "Create":
        "Створити",
    "Create certificate":
        "Створити сертифікат",
    "Custom":
        "Власний",
    "DNS filter lists":
        "Списки DNS-фільтрування",
    "DNS filtering":
        "DNS-фільтрування",
    "DNS filtering is off, so these lists have no effect.":
        "DNS-фільтрування вимкнено, тому ці списки не діють.",
    "DNS servers":
        "DNS-сервери",
    "Dark":
        "Темна",
    "Default":
        "Типово",
    "Details":
        "Подробиці",
    "Discard":
        "Відкинути",
    "Don't filter":
        "Не фільтрувати",
    "Don't trust":
        "Не довіряти",
    "Downloads and installs the newest AdGuard CLI build.":
        "Завантажує та встановлює найновішу збірку AdGuard CLI.",
    "Duration":
        "Тривалість",
    "Export…":
        "Експортувати…",
    "Filter everything":
        "Фільтрувати все",
    "Filter in place":
        "Фільтрувати на місці",
    "Filtering":
        "Фільтрування",
    "Follow system":
        "Як у системі",
    "From URL…":
        "За URL…",
    "Go to updates":
        "Перейти до оновлень",
    "HTTP proxy: {}":
        "HTTP-проксі: {}",
    "HTTPS filtering":
        "HTTPS-фільтрування",
    "How much detail AdGuard Tray writes to its own log.":
        "Наскільки детально AdGuard Tray записує події до власного журналу.",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "Якщо сайт не завантажується, спочатку вимкніть фільтрування HTTP/3. Інші перевірки захищають усі сайти – вимикайте їх, лише якщо це не допомогло.",
    "Included":
        "Включено",
    "Installed":
        "Встановлені",
    "License":
        "Ліцензія",
    "Light":
        "Світла",
    "Logs":
        "Журнали",
    "MIT license":
        "Ліцензія MIT",
    "Maintenance":
        "Обслуговування",
    "Manual proxy":
        "Ручний проксі",
    "Manual – only apps set to use the proxy":
        "Ручний – лише застосунки, налаштовані на проксі",
    "More":
        "Більше",
    "Move down":
        "Пересунути вниз",
    "Move up":
        "Пересунути вгору",
    "Network":
        "Мережа",
    "Nightly":
        "Нічний",
    "No requests yet – AdGuard logs requests while protection is on.":
        "Запитів поки немає – AdGuard записує запити, доки захист увімкнено.",
    "Not added":
        "Не додано",
    "Nothing matches your search.":
        "Нічого не знайдено.",
    "Notify me when protection turns on or off":
        "Сповіщати про ввімкнення та вимкнення захисту",
    "Off":
        "Вимкнено",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "Стосується лише браузерів, що використовують DoH або DoT. Якщо вибрати «Вимкнено», вони оминатимуть DNS-фільтрування AdGuard.",
    "Open AdGuard Tray":
        "Відкрити AdGuard Tray",
    "Open exceptions":
        "Відкрити винятки",
    "Open folder":
        "Відкрити теку",
    "Open release page":
        "Відкрити сторінку випуску",
    "Pages":
        "Сторінки",
    "Performance":
        "Продуктивність",
    "Protection":
        "Захист",
    "Protection started.":
        "Захист увімкнено.",
    "Protection stopped.":
        "Захист вимкнено.",
    "Proxy mode":
        "Режим проксі",
    "Redirect to AdGuard's DNS":
        "Перенаправляти на DNS AdGuard",
    "Refresh this page (F5)":
        "Оновити цю сторінку (F5)",
    "Release (stable)":
        "Стабільний (release)",
    "Remove rule":
        "Вилучити правило",
    "Remove “{}”?":
        "Вилучити «{}»?",
    "Remove…":
        "Вилучити…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "Замінити поточні налаштування AdGuard налаштуваннями з файлу {}?\n\nAdGuard перезапуститься, щоб застосувати їх.",
    "Reset history…":
        "Скинути історію…",
    "Reset…":
        "Скинути…",
    "Restart AdGuard":
        "Перезапустити AdGuard",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "Правила діють лише в автоматичному режимі проксі. Спрацьовує перше відповідне правило, тому ставте \"*\" останнім.",
    "Safe Browsing":
        "Безпечний перегляд",
    "Save anyway":
        "Усе одно зберегти",
    "Saved. AdGuard restarts to apply the change.":
        "Збережено. AdGuard перезапуститься, щоб застосувати зміну.",
    "Saved. Applies after AdGuard Tray restarts.":
        "Збережено. Застосовується після перезапуску AdGuard Tray.",
    "Saved. The change applies when protection is turned on.":
        "Збережено. Зміна набуде чинності після ввімкнення захисту.",
    "Secure DNS and ECH":
        "Захищений DNS і ECH",
    "Secure DNS filtering":
        "Фільтрування захищеного DNS",
    "Set the path in Settings":
        "Укажіть шлях у «Налаштування»",
    "Settings":
        "Налаштування",
    "Show":
        "Показати",
    "Show recent entries":
        "Показати останні записи",
    "Skip HTTPS filtering":
        "Пропускати HTTPS-фільтрування",
    "Some counts could not be loaded.":
        "Не вдалося завантажити деякі показники.",
    "Source code":
        "Вихідний код",
    "Start AdGuard Tray when I log in":
        "Запускати AdGuard Tray після входу в систему",
    "Startup":
        "Запуск",
    "Status checks":
        "Перевірки стану",
    "Stealth mode":
        "Антитрекінг",
    "System":
        "Система",
    "The new lists load when protection is turned on.":
        "Нові списки буде завантажено після ввімкнення захисту.",
    "Theme":
        "Тема",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "Буде вимкнено фільтрування HTTP/3, перевірки OCSP, Certificate Transparency і фільтрування захищеного DNS. Тоді відкликані або помилково видані сертифікати залишатимуться непоміченими, а браузери зможуть визначати адреси в обхід DNS-фільтра AdGuard.",
    "Time range":
        "Часовий проміжок",
    "To keep it but stop using it, switch it off instead.":
        "Щоб залишити, але не використовувати, просто вимкніть його.",
    "Top lists":
        "Найчастіші",
    "Trust":
        "Довіряти",
    "Trust “{}”?":
        "Довіряти «{}»?",
    "Trust…":
        "Довіряти…",
    "Turn off all strict checks…":
        "Вимкнути всі суворі перевірки…",
    "Undo":
        "Вернути",
    "Unknown":
        "Невідомо",
    "Unsaved changes":
        "Незбережені зміни",
    "Update AdGuard CLI…":
        "Оновити AdGuard CLI…",
    "Update channel: {}":
        "Канал оновлень: {}",
    "Updated {}":
        "Оновлено {}",
    "Updates":
        "Оновлення",
    "Used in manual mode only.":
        "Використовується лише в ручному режимі.",
    "Userscripts update together with filters.":
        "Скрипти оновлюються разом із фільтрами.",
    "Uses XDG autostart (~/.config/autostart).":
        "Використовує автозапуск XDG (~/.config/autostart).",
    "Waiting for authorization…":
        "Очікування авторизації…",
    "Website exceptions":
        "Винятки для сайтів",
    "Websites":
        "Сайти",
    "example.com or a link":
        "example.com або посилання",
    "expires {}":
        "дійсна до {}",
    "of {} requests in the last 24 hours":
        "Усього запитів за останні 24 години: {}",
    "{} of {} DNS filters on":
        "DNS-фільтри: увімкнено {} з {}",
    "{} of {} filters on":
        "Фільтри: увімкнено {} з {}",
    "{} of {} on":
        "Увімкнено: {} з {}",
    "{} unsaved changes to AdGuard's settings":
        "Незбережені зміни в налаштуваннях AdGuard: {}",
    "“Follow system” uses your desktop's light or dark setting.":
        "Варіант «Як у системі» бере світлу або темну тему з налаштувань вашого робочого середовища.",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "Активна",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "Сертифікат AdGuard буде додано до всіх профілів браузерів, знайдених у цій системі.\n\nЦе дасть змогу AdGuard перевіряти HTTPS-трафік у цих браузерах. Спочатку закрийте браузери – вони зчитують сховище сертифікатів під час запуску.",
    "Allow":
        "Дозволити",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "Спочатку застосуйте або відкиньте зміни в налаштуваннях AdGuard, а потім перезапустіть.",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "Автоматичний: AdGuard перенаправляє на себе трафік усіх застосунків через iptables. Ручний: AdGuard лише прослуховує порти SOCKS5 і HTTP, указані нижче.",
    "Block":
        "Заблокувати",
    "Browser API blocking":
        "Блокування API браузера",
    "CRLite":
        "CRLite",
    "Cancel":
        "Скасувати",
    "Computers":
        "Комп’ютери",
    "Could not change the autostart entry.":
        "Не вдалося змінити запис автозапуску.",
    "Could not export the logs.":
        "Не вдалося експортувати журнали.",
    "Could not export the settings.":
        "Не вдалося експортувати налаштування.",
    "Could not reset the license.":
        "Не вдалося скинути ліцензію.",
    "Could not retrieve license info.":
        "Не вдалося отримати відомості про ліцензію.",
    "Could not run the benchmark.":
        "Не вдалося запустити тест продуктивності.",
    "Could not save the settings.":
        "Не вдалося зберегти налаштування.",
    "Could not set the update channel.":
        "Не вдалося встановити канал оновлень.",
    "Could not update AdGuard CLI.":
        "Не вдалося оновити AdGuard CLI.",
    "Could not update the filters.":
        "Не вдалося оновити фільтри.",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "Основний DNS-сервер.\n'default' = системний DNS.\nПриклади: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com",
    "Expiration date":
        "Дата закінчення",
    "Expires":
        "Дійсна до",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "HTTP/3 знову ввімкнено у профілях Firefox – перезапустіть браузер.",
    "License key":
        "Ліцензійний ключ",
    "License type":
        "Тип ліцензії",
    "Manual":
        "Ручний",
    "No exceptions.":
        "Винятків немає.",
    "OK":
        "Гаразд",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "Увімкнено: AdGuard сам фільтрує HTTP/3 (QUIC) – це експериментальна функція, і деякі\nбраузери однаково відмовляються від HTTP/3 із сертифікатом, установленим користувачем.\nВимкнено: AdGuard натомість блокує QUIC, і браузери переходять на HTTP/2,\nякий надійно фільтрується.\nУ будь-якому разі це діє лише в автоматичному режимі – у ручному режимі\nтрафік HTTP/3 взагалі не надходить до AdGuard.",
    "Owner":
        "Власник",
    "Personal":
        "Особиста",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "Режим проксі: {} – UDP-порт 443 перенаправлено на AdGuard.",
    "Save adguard-cli path":
        "Зберегти шлях до adguard-cli",
    "Search domains or rules…":
        "Пошук доменів або правил…",
    "Settings file":
        "Файл налаштувань",
    "Status":
        "Стан",
    "Trial":
        "Пробна",
    "Turn HTTP/3 back on in Firefox profiles":
        "Знову ввімкнути HTTP/3 у профілях Firefox",
    "Turn off":
        "Вимкнути",
    "Turn off HTTP/3 in Firefox profiles":
        "Вимкнути HTTP/3 у профілях Firefox",
    "Turn off HTTP/3 in Firefox profiles…":
        "Вимкнути HTTP/3 у профілях Firefox…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "Вимкнути HTTP/3 у профілях сімейства Firefox (кількість: {})?\n\nТоді їхній трафік використовуватиме HTTP/2, який AdGuard може фільтрувати. Після цього перезапустіть браузер.",
    "Turn off all strict checks":
        "Вимкнути всі суворі перевірки",
    "Unavailable until AdGuard CLI reports its current channel.":
        "Недоступно, доки AdGuard CLI не повідомить поточний канал.",
    "Update AdGuard CLI":
        "Оновити AdGuard CLI",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "Використовується лише в автоматичному режимі. Діапазони (80:5221,5300:49151) або окремі порти (80,443,8080).",
    "{} of {}":
        "{} з {}",
    "{} of {} userscripts on":
        "Скрипти: увімкнено {} з {}",
    "{}% blocked":
        "{}% заблоковано",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "Роздратування",
    "General":
        "Загальні",
    "Language-specific":
        "Мовні",
    "Security":
        "Безпека",
    "Social widgets":
        "Віджети соцмереж",
    "Expired":
        "Термін дії минув",
    "Autostart on login":
        "Автозапуск після входу",
    "Add app rule":
        "Додати правило для застосунку",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "Можна використовувати символи-замінники, напр. *steam* або *EasyAntiCheat*.",
    "There is already a rule for '{}'.":
        "Правило для «{}» уже існує.",
    "AdGuard settings":
        "Налаштування AdGuard",
    "Ads and trackers are not blocked until you enable protection.":
        "Реклама й трекери не блокуються, доки ви не ввімкнете захист.",
    "Could not import the settings.":
        "Не вдалося імпортувати налаштування.",
    "Disable protection":
        "Вимкнути захист",
    "Enable protection":
        "Увімкнути захист",
    "Export and import":
        "Експорт та імпорт",
    "Features":
        "Функції",
    "Import settings":
        "Імпортувати налаштування",
    "Import settings from…":
        "Імпортувати налаштування з…",
    "Import settings…":
        "Імпортувати налаштування…",
    "Import…":
        "Імпортувати…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "Фільтри, правила й конфігурацію можна зберегти в zip-файл або завантажити з нього.",
    "Update":
        "Оновити",
    "Version":
        "Версія",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "Файл {} не містить експортованих налаштувань. Виберіть файл, збережений за допомогою «Експортувати…» у розділі «Налаштування AdGuard».",

    # ── AdGuard VPN, outbound proxy, install ──────────────────────────
    "Press Enter to close this window.":
        "Натисніть Enter, щоб закрити це вікно.",
    "No terminal app was found. The install command is on the clipboard: paste it into a terminal.":
        "Не знайдено жодного термінала. Команду встановлення скопійовано в буфер обміну: вставте її в термінал.",
    "Finish the installation in the terminal, then press Refresh.":
        "Завершіть встановлення в терміналі, а потім натисніть «Оновити».",
    "Open in a terminal":
        "Відкрити в терміналі",
    "AdGuard VPN":
        "AdGuard VPN",
    "AdGuard's VPN for Linux (adguardvpn-cli) runs next to AdGuard CLI. AdGuard Tray checks that their settings fit together; it does not connect the VPN or log in.":
        "VPN від AdGuard для Linux (adguardvpn-cli) працює поряд з AdGuard CLI. AdGuard Tray перевіряє, чи узгоджені їхні налаштування; він не підключає VPN і не виконує вхід.",
    "Install…":
        "Встановити…",
    "Outbound proxy":
        "Вихідний проксі",
    "AdGuard sends its own connections through this proxy, for example through AdGuard VPN in SOCKS5 mode.":
        "AdGuard спрямовує власні з’єднання через цей проксі, наприклад, через AdGuard VPN у режимі SOCKS5.",
    "Use an outbound proxy":
        "Використовувати вихідний проксі",
    "Host":
        "Хост",
    "Port":
        "Порт",
    "Not installed.":
        "Не встановлено.",
    "AdGuard VPN is set to TUN mode while AdGuard filters in automatic mode. Connected like this, traffic loops between the two – AdGuard does not support this combination.":
        "AdGuard VPN налаштовано на режим TUN, тоді як AdGuard фільтрує в автоматичному режимі. За такого підключення трафік зациклюється між ними – AdGuard не підтримує таке поєднання.",
    "AdGuard VPN now uses SOCKS5 mode. Press Apply to send AdGuard's traffic through it, and reconnect AdGuard VPN if it is connected.":
        "Тепер AdGuard VPN працює в режимі SOCKS5. Натисніть «Застосувати», щоб спрямувати трафік AdGuard через нього, і перепідключіть AdGuard VPN, якщо його підключено.",
    "AdGuard VPN CLI":
        "AdGuard VPN CLI",
    "Installed, but its settings could not be read: {}":
        "Встановлено, але не вдалося прочитати налаштування: {}",
    "Route AdGuard through the VPN":
        "Спрямувати AdGuard через VPN",
    "Could not switch AdGuard VPN to SOCKS5 mode.":
        "Не вдалося перемкнути AdGuard VPN у режим SOCKS5.",
    "Installed · SOCKS5 mode on {}:{}":
        "Встановлено · режим SOCKS5 на {}:{}",
    "Installed · TUN mode":
        "Встановлено · режим TUN",
    "Installed · {} mode":
        "Встановлено · режим {}",
}
