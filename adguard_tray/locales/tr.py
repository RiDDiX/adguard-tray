"""Turkish."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "Dil",
    "English":                           "English",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "Etkin – Koruma çalışıyor",
    "Inactive – Protection stopped":        "Etkin değil – Koruma durdu",
    "Error retrieving status":              "Durum alınırken hata oluştu",
    "adguard-cli not found":                "adguard-cli bulunamadı",
    "Unknown status":                       "Bilinmeyen durum",
    "Checking status…":                     "Durum denetleniyor…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "Yeniden başlat",
    "Filters":                              "Filtreler",
    "Loading…":                             "Yükleniyor…",
    "Manage filters…":                      "Filtreleri yönet…",
    "No userscripts installed":             "Kurulu kullanıcı betiği yok",
    "Manage userscripts…":                  "Kullanıcı betiklerini yönet…",
    "Quit":                                 "Çık",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "etkin",
    "inactive":                             "etkin değil",
    "System-wide filtering: {}":            "Sistem genelinde filtreleme: {}",
    "Error: {}":                            "Hata: {}",
    "AdGuard Tray – Error":                 "AdGuard Tray – Hata",
    "AdGuard is now active – protection running.":
        "AdGuard artık etkin – koruma çalışıyor.",
    "AdGuard has been stopped.":
        "AdGuard durduruldu.",
    "Could not retrieve status.":
        "Durum alınamadı.",
    "Command failed":                       "Komut başarısız oldu",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " saniye",
    "How often adguard-cli status is checked automatically.":
        "adguard-cli durumunun ne sıklıkla otomatik olarak denetleneceğini belirler.",
    "Log level:":                           "Günlük düzeyi:",
    "adguard-cli path:":                    "adguard-cli yolu:",
    "auto-detect via PATH":                 "PATH üzerinden otomatik algılama",
    "Browse…":                              "Gözat…",
    "Select adguard-cli binary":            "adguard-cli çalıştırılabilir dosyasını seç",
    "Notifications":                        "Bildirimler",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "Filtreleri güncelle",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "Tüm filtreleri, DNS filtrelerini, kullanıcı betiklerini,\nSafebrowsingV2 ve CRLite verilerini günceller ve uygulama güncellemelerini denetler.",
    "No filters found.":                    "Filtre bulunamadı.",
    "Updating filters… (can take up to 2 minutes)":
        "Filtreler güncelleniyor… (2 dakikaya kadar sürebilir)",
    "Update completed.":                    "Güncelleme tamamlandı.",
    "Update failed.":                       "Güncelleme başarısız oldu.",
    "Installing: {}":                       "Kuruluyor: {}",
    "Filter installed.":                    "Filtre kuruldu.",
    "Remove":                               "Kaldır",
    "Remove filter":                        "Filtreyi kaldır",
    "Filter {} removed.":                   "Filtre kaldırıldı: {}.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        "Doğrudan bir .js URL'sinden kullanıcı betiği kurar",
    "No userscripts installed.":            "Kurulu kullanıcı betiği yok.",
    "Userscript URL (direct .js URL):":     "Kullanıcı betiği URL'si (doğrudan .js URL'si):",
    "Userscript installed.":                "Kullanıcı betiği kuruldu.",
    'Remove "{}"':                          "“{}” öğesini kaldır",
    "Remove userscript":                    "Kullanıcı betiğini kaldır",
    "'{}' removed.":                        "“{}” kaldırıldı.",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "adguard-cli bulunamadı.\nResmi betik veya AUR üzerinden kurun:\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "Durum alınırken bilinmeyen hata oluştu",
    "AdGuard {} ok":                        "AdGuard {}: başarılı",
    "AdGuard via systemctl {} ok":          "AdGuard (systemctl {}): başarılı",
    "'{}' failed – insufficient privileges?":
        "“{}” başarısız oldu – yetkiler yetersiz mi?",
    "Could not retrieve filter list":
        "Filtre listesi alınamadı",
    "Filter {} enabled":                    "Filtre etkinleştirildi: {}",
    "Could not enable filter {}":           "Filtre etkinleştirilemedi: {}",
    "Filter {} disabled":                   "Filtre devre dışı bırakıldı: {}",
    "Could not disable filter {}":
        "Filtre devre dışı bırakılamadı: {}",
    "Filter installed":                     "Filtre kuruldu",
    "Installation failed":                  "Kurulum başarısız oldu",
    "Filter {} removed":                    "Filtre kaldırıldı: {}",
    "Could not remove filter {}":
        "Filtre kaldırılamadı: {}",
    "Filters updated":                      "Filtreler güncellendi",
    "Update failed":                        "Güncelleme başarısız oldu",
    "Could not retrieve userscript list":
        "Kullanıcı betiği listesi alınamadı",
    "Userscript '{}' enabled":              "Kullanıcı betiği etkinleştirildi: “{}”",
    "Could not enable userscript '{}'":
        "Kullanıcı betiği etkinleştirilemedi: “{}”",
    "Userscript '{}' disabled":             "Kullanıcı betiği devre dışı bırakıldı: “{}”",
    "Could not disable userscript '{}'":
        "Kullanıcı betiği devre dışı bırakılamadı: “{}”",
    "Userscript '{}' removed":              "Kullanıcı betiği kaldırıldı: “{}”",
    "Could not remove userscript '{}'":
        "Kullanıcı betiği kaldırılamadı: “{}”",
    "Userscript installed":                 "Kullanıcı betiği kuruldu",
    "Other":                                "Diğer",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "Filtrelerde ara…",
    "Search userscripts…":              "Kullanıcı betiklerinde ara…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "proxy.yaml dosyası yüklenemedi.\nYol: {}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "Uygulamalar",
    "Mode:":                            "Mod:",
    "Filtered ports:":                  "Filtrelenen portlar:",
    "SOCKS5 port:":                     "SOCKS5 portu:",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "El ile mod için SOCKS5 proxy portu.\nDevre dışı bırakmak için -1 olarak ayarlayın.",
    "HTTP port:":                       "HTTP portu:",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "El ile mod için HTTP proxy portu.\nDevre dışı bırakmak için -1 olarak ayarlayın.",
    "Listen address:":                  "Dinleme adresi:",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "Proxy'nin dinlediği adres.\n127.0.0.1 = yalnızca yerel. 0.0.0.0 = tüm arayüzler (kimlik doğrulama gerekir).",
    "Worker threads:":                  "İş parçacıkları:",
    "Number of proxy worker threads.":  "Proxy iş parçacığı sayısı.",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "HTTPS trafiğinin şifresini çözer ve filtreler.\nHTTPS sitelerinde reklamları engellemek için gereklidir.\nSistemde kurulu, güvenilir bir kök sertifika gerektirir.",
    "Enable TLS 1.3":                   "TLS 1.3 desteğini etkinleştir",
    "Enable TLS 1.3 support for filtered connections.":
        "Filtrelenen bağlantılar için TLS 1.3 desteğini etkinleştirir.",
    "Filter HTTP/3 (QUIC) – experimental":
        "HTTP/3 (QUIC) trafiğini filtrele – deneysel",
    "OCSP certificate checks":          "OCSP sertifika denetimleri",
    "Enforce Certificate Transparency": "Certificate Transparency denetimini zorunlu kıl",
    "Filter EV certificate sites":      "EV sertifikalı siteleri filtrele",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "Varsayılan olarak, Genişletilmiş Doğrulama (EV) sertifikalı siteler filtrelenmez.\nBunları da filtrelemek için etkinleştirin (örn. banka siteleri).",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "Daha iyi gizlilik için ECH'yi etkinleştirir.\nDNS filtrelemenin etkin olmasını gerektirir.",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "Reklamları ve izleyicileri DNS düzeyinde engellemek için DNS sorgularını filtreler.\nÜst kaynakları yapılandırılabilen yerel bir DNS proxy'si kullanır.",
    "Upstream:":                        "Üst kaynak:",
    "Fallbacks:":                       "Yedekler:",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "Yedek DNS sunucuları (birincil üst kaynak başarısız olduğunda kullanılır).\n'default' = sistem DNS'i. Boşlukla ayrılmış liste.\nÖrnek: default 1.1.1.1",
    "Bootstraps:":                      "Önyükleme:",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "Üst kaynak ana makine adlarını çözümlemek için önyükleme DNS'i.\n'default' = sistem DNS IP'leri. Yalnızca IP adreslerine izin verilir.\nÖrnek: default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "SVCB/HTTPS DNS kayıtlarından ECH parametresini kaldırır.\nYalnızca HTTPS filtrelemeyi otomatik algılamayan tarayıcılar için etkinleştirin.",
    "Master switch for all tracking protection features below.":
        "Aşağıdaki tüm izleme koruması özelliklerinin ana anahtarı.",
    "Cookies":                          "Çerezler",
    "Block third-party cookies":        "Üçüncü taraf çerezlerini engelle",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "Üçüncü taraf çerezlerini belirli bir süre sonra siler.\nSiteler arası izlemeyi önler.",
    "Lifetime (minutes):":              "Ömür (dakika):",
    "0 = block immediately. Default: 180 minutes.":
        "0 = hemen engelle. Varsayılan: 180 dakika.",
    "Block first-party cookies":        "Birinci taraf çerezlerini engelle",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "Tüm çerezleri (birinci taraf dahil) belirli bir süre sonra siler.\nUyarı: Bu, tüm sitelerdeki oturumlarınızı kapatır.",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = hemen engelle. Varsayılan: 4320 dakika (3 gün).",
    "Privacy":                          "Gizlilik",
    "Hide / reduce User-Agent":         "User-Agent bilgisini gizle / kısalt",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "User-Agent bilgisinden tanımlayıcı kısımları çıkarır.\nParmak izi çıkarmayı zorlaştırır.",
    "Hide search queries in referrer":  "Referrer'daki arama sorgularını gizle",
    "Hides your search terms when clicking from a search engine to a website.":
        "Arama motorundan bir web sitesine geçtiğinizde arama terimlerinizi gizler.",
    "Remove referrer from third-party requests":
        "Üçüncü taraf isteklerinden referrer'ı kaldır",
    "Prevents third-party sites from knowing which page you came from.":
        "Üçüncü taraf sitelerin hangi sayfadan geldiğinizi bilmesini önler.",
    "Send Do-Not-Track signal":         "Do-Not-Track sinyali gönder",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "İsteklerle birlikte DNT başlığı gönderir.\nNot: Çoğu site bunu yok sayar, ancak bazıları dikkate alır.",
    "Disable third-party ETag cache":   "Üçüncü taraf ETag önbelleğini devre dışı bırak",
    "Prevents tracking via ETag caching in third-party content.":
        "Üçüncü taraf içeriklerde ETag önbelleği yoluyla izlemeyi önler.",
    "Block third-party Authorization header":
        "Üçüncü taraf Authorization başlığını engelle",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "İzlemeyi önlemek için üçüncü taraf isteklerindeki Authorization başlığını engeller.",
    "Remove X-Client-Data header":      "X-Client-Data başlığını kaldır",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "Chrome'un Google hizmetlerine gönderdiği X-Client-Data başlığını kaldırır.",
    "Block WebRTC":                     "WebRTC'yi engelle",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "WebRTC üzerinden IP sızıntılarını önler.\nGörüntülü aramaları ve bazı web uygulamalarını bozabilir.",
    "Block Push API":                   "Push API'yi engelle",
    "Blocks browser push notifications from websites.":
        "Web sitelerinden gelen tarayıcı anlık bildirimlerini engeller.",
    "Block Location API":               "Konum API'sini engelle",
    "Prevents websites from accessing your GPS location.":
        "Web sitelerinin GPS konumunuza erişmesini önler.",
    "Block Flash":                      "Flash'ı engelle",
    "Blocks the Flash plugin.":
        "Flash eklentisini engeller.",
    "Block Java":                       "Java'yı engelle",
    "Disables Java plugins. JavaScript remains enabled.":
        "Java eklentilerini devre dışı bırakır. JavaScript etkin kalır.",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "Anti-DPI özelliğini etkinleştir",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "Derin Paket İnceleme (DPI) engelini aşmak için giden paket verilerini değiştirir.\nİnternet sansürü olan ülkelerde işe yarar.",
    "App pattern":
        "Uygulama deseni",
    "Skip outbound proxy":              "Giden proxy'yi atla",
    "Don't route this app's traffic through outbound proxy":
        "Bu uygulamanın trafiği giden proxy üzerinden yönlendirilmez",
    "Browser list included from {}":    "Tarayıcı listesinin kaynağı: {}",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "Tarayıcı dahil etme listesi ve joker karakter (*) kuralı kaldırılamaz.",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "Kötü amaçlı ve kimlik avı sitelerine karşı uyarır.\nAdGuard'ın Güvenli gezinti veritabanını kullanır.",
    "Send anonymous statistics":        "Anonim istatistik gönder",
    "Send anonymous lookups to AdGuard.":
        "AdGuard'a anonim sorgular gönderir.",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "Mozilla CRLite ile sertifika iptal denetimi.\nGeleneksel CRL/OCSP denetimlerinden daha hızlı ve güvenilirdir.",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "Reklam engelleme filtre kurallarını HTTP/HTTPS isteklerine uygular.",
    "Save failed":                      "Kaydedilemedi",
    "Could not save proxy.yaml:\n{}":   "proxy.yaml dosyası kaydedilemedi:\n{}",
    "Restarting AdGuard…":              "AdGuard yeniden başlatılıyor…",
    "AdGuard restarted.":               "AdGuard yeniden başlatıldı.",
    "Restart failed: {}":               "Yeniden başlatma başarısız oldu: {}",
    "Unknown error":                    "Bilinmeyen hata",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "Ekle",
    "Search exceptions…":               "İstisnalarda ara…",
    "1 exception":                      "1 istisna",
    "{} exceptions":                    "{} istisna",
    "'{}' is not a valid domain or IP address.":
        "“{}” geçerli bir alan adı veya IP adresi değil.",
    "'{}' is already in the list.":     "“{}” zaten listede.",
    "Could not save exceptions:\n{}":
        "İstisnalar kaydedilemedi:\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "Genel bakış",
    "Userscripts":                      "Kullanıcı betikleri",
    "Exceptions":                       "İstisnalar",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "Lisansı sıfırla",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "HTTPS filtreleme için bir kök CA sertifikası oluşturur. Sertifikanın sisteminize kurulması ve güvenilir olarak işaretlenmesi gerekir.",
    "Checking for updates…":            "Güncellemeler denetleniyor…",
    "Firefox profile:":                 "Firefox profili:",
    "(optional) e.g. abcd1234.MyProfile":
        "(isteğe bağlı) örn. abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "Filtre kimliğini veya adını girin:",
    "Filter added.":                    "Filtre eklendi.",
    "Rename…":                          "Yeniden adlandır…",
    "Rename filter":                    "Filtreyi yeniden adlandır",
    "New title:":                       "Yeni başlık:",
    "Filter renamed.":                  "Filtre yeniden adlandırıldı.",
    "Filter trust updated.":            "Filtre güven durumu güncellendi.",
    "Filter URL:":                      "Filtre URL'si:",
    "Title:":                           "Başlık:",
    "(optional)":                       "(isteğe bağlı)",
    "Trusted filter":                   "Güvenilir filtre",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "DNS filtrelerinde ara…",
    "No DNS filters found.":            "DNS filtresi bulunamadı.",
    "DNS filter installed.":            "DNS filtresi kuruldu.",
    "DNS filter added.":                "DNS filtresi eklendi.",
    "Remove DNS filter":                "DNS filtresini kaldır",
    "DNS filter {} removed.":           "DNS filtresi kaldırıldı: {}.",
    "Rename DNS filter":                "DNS filtresini yeniden adlandır",
    "DNS filter renamed.":              "DNS filtresi yeniden adlandırıldı.",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "Günlükleri dışa aktar…",
    "Export AdGuard CLI logs to a zip file":
        "AdGuard CLI günlüklerini zip dosyası olarak dışa aktarır",
    "Export settings…":                 "Ayarları dışa aktar…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "Şifreleme ve HTTPS filtreleme performans testi çalıştırır.",
    "Run benchmark":                    "Performans testini çalıştır",
    "Done.":                            "Tamamlandı.",
    "Export logs to…":                  "Günlüklerin kaydedileceği yer…",
    "Export settings to…":              "Ayarların kaydedileceği yer…",
    "Zip files (*.zip);;All files (*)":
        "Zip dosyaları (*.zip);;Tüm dosyalar (*)",
    "Log file not found.":              "Günlük dosyası bulunamadı.",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "DNS filtre listesi alınamadı",
    "DNS filter {} enabled":            "DNS filtresi etkinleştirildi: {}",
    "Could not enable DNS filter {}":   "DNS filtresi etkinleştirilemedi: {}",
    "DNS filter {} disabled":           "DNS filtresi devre dışı bırakıldı: {}",
    "Could not disable DNS filter {}":  "DNS filtresi devre dışı bırakılamadı: {}",
    "DNS filter installed":             "DNS filtresi kuruldu",
    "DNS filter {} removed":            "DNS filtresi kaldırıldı: {}",
    "Could not remove DNS filter {}":   "DNS filtresi kaldırılamadı: {}",
    "DNS filter added":                 "DNS filtresi eklendi",
    "Could not add DNS filter":         "DNS filtresi eklenemedi",
    "DNS filter title updated":         "DNS filtresi başlığı güncellendi",
    "Could not set DNS filter title":   "DNS filtresi başlığı ayarlanamadı",
    "Filter added":                     "Filtre eklendi",
    "Could not add filter":             "Filtre eklenemedi",
    "Filter trust updated":             "Filtre güven durumu güncellendi",
    "Could not update filter trust":    "Filtre güven durumu güncellenemedi",
    "Filter title updated":             "Filtre başlığı güncellendi",
    "Could not set filter title":       "Filtre başlığı ayarlanamadı",
    "License reset":                    "Lisans sıfırlandı",
    "Could not reset license":          "Lisans sıfırlanamadı",
    "Could not retrieve license info":  "Lisans bilgileri alınamadı",
    "Certificate generated":            "Sertifika oluşturuldu",
    "Certificate generation failed":    "Sertifika oluşturulamadı",
    "Logs exported":                    "Günlükler dışa aktarıldı",
    "Log export failed":                "Günlükler dışa aktarılamadı",
    "Settings exported":                "Ayarlar dışa aktarıldı",
    "Settings export failed":           "Ayarlar dışa aktarılamadı",
    "Settings imported":                "Ayarlar içe aktarıldı",
    "Settings import failed":           "Ayarlar içe aktarılamadı",
    "Update check completed":           "Güncelleme denetimi tamamlandı",
    "Update check failed":              "Güncelleme denetimi başarısız oldu",
    "Benchmark failed":                 "Performans testi başarısız oldu",
    "AdGuard stopped (forced)":         "AdGuard durduruldu (zorla)",
    "Could not stop AdGuard – process may still be running":
        "AdGuard durdurulamadı – süreç hâlâ çalışıyor olabilir",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "adguard-cli bu sistemde bulunamadı.\n\nÖnerilen kurulum yöntemi (resmi):\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\nAlternatif (Arch Linux AUR):\n  paru -S adguard-cli-bin\n\nTepsi simgesi yüklenir ancak adguard-cli kurulana kadar başlatma ve durdurma çalışmaz.",
    "Copy install command":             "Kurulum komutunu kopyala",
    "Continue":                         "Devam et",
    "AdGuard Tray is already running":  "AdGuard Tray zaten çalışıyor",
    "Only one instance can run at a time. Check your system tray.":
        "Aynı anda yalnızca bir örnek çalışabilir. Sistem tepsinizi kontrol edin.",
    "Authentication cancelled":         "Kimlik doğrulama iptal edildi",
    "Authorization failed":             "Yetkilendirme başarısız oldu",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "Bir sitenin sertifikasının iptal edilip edilmediğini denetler (OCSP).\nAdGuard denetimi eşzamansız yapar ve denetim uzun sürerse\nbağlantıya izin verir; bu yüzden bu ayar bir siteyi nadiren bozar –\nsorunun bu ayardan kaynaklandığını saptamadıkça açık bırakın.",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "Certificate Transparency denetimlerini zorunlu kılar (Chrome'un CT ilkesi).\nKendi sertifikası CT uyumlu olmayan siteler artık filtrelenmez\nve tarayıcı bunları reddedebilir. Büyük siteler uyumludur; bu yüzden\nbunu yalnızca sertifika hatası veren bir sitede deneyin.",
    "Sites that don't load":
        "Yüklenmeyen siteler",
    "Turn off HTTP/3 filtering":
        "HTTP/3 filtrelemeyi kapat",
    "No filters installed":
        "Kurulu filtre yok",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "HTTP/3, bir güvenlik duvarı kuralı tarafından engelleniyor; tarayıcılar HTTP/2 kullanıyor.",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "Filtrelemenin dışında tutulan uygulamalar (HTTP/3 trafikleri de filtrelenmez): {}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuard çalışmıyor – hiçbir şey filtrelenmiyor.",
    "could not remove the previous certificate":
        "önceki sertifika kaldırılamadı",
    "HTTP/3 state unknown":
        "HTTP/3 durumu bilinmiyor",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "Bir güvenlik duvarı kuralı giden UDP 443 trafiğini reddediyor, bu yüzden QUIC kullanılamıyor.",
    "Browser policy disables QUIC: {}":
        "Tarayıcı ilkesi QUIC'i devre dışı bırakıyor: {}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "Tarayıcılar HTTP/3 (UDP 443) üzerinden AdGuard'ı atlatabilir.",
    "Checking…":
        "Denetleniyor…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "proxy.yaml dosyası okunamadı – HTTP/3 durumu bilinmiyor.",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "HTTP/3'ün kapatıldığı Firefox ailesi profilleri: {} / {}",
    "HTTP/3 (QUIC)":
        "HTTP/3 (QUIC)",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "HTTP/3, AdGuard tarafından engelleniyor; tarayıcılar filtrelenen HTTP/2'ye geçiyor.",
    "HTTP/3 is filtered by AdGuard.":
        "HTTP/3, AdGuard tarafından filtreleniyor.",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "Firefox profillerinde HTTP/3 kapatıldı – tarayıcıyı yeniden başlatın.",
    "HTTPS filtering is off – nothing is filtered.":
        "HTTPS filtreleme kapalı – hiçbir şey filtrelenmiyor.",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "Proxy modu: {} – yalnızca proxy üzerinden gönderilen trafik filtrelenir ve tarayıcılar QUIC trafiğini proxy üzerinden göndermez.",
    "unknown":
        "bilinmiyor",
    "AdGuard's certificate was not found. Generate it first.":
        "AdGuard sertifikası bulunamadı. Önce sertifikayı oluşturun.",
    "Certificate could not be installed in any browser.":
        "Sertifika hiçbir tarayıcıya kurulamadı.",
    "Certificate installed for {} of {} stores.":
        "Sertifika {} / {} depoya kuruldu.",
    "Chromium-based browsers":
        "Chromium tabanlı tarayıcılar",
    "No browser certificate stores found.":
        "Tarayıcı sertifika deposu bulunamadı.",
    "Restart your browsers for the certificate to take effect.":
        "Sertifikanın etkili olması için tarayıcılarınızı yeniden başlatın.",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "Bunu sudo/pkexec olmadan çalıştırın – kurulum kendi tarayıcı profillerinize yapılır",
    "certificate not found after import":
        "içe aktarmadan sonra sertifika bulunamadı",
    "certutil not found – install the 'nss' package":
        "certutil bulunamadı – 'nss' paketini kurun",
    "not found":
        "bulunamadı",
    "Could not read the filter list (unexpected CLI output).":
        "Filtre listesi okunamadı (beklenmeyen CLI çıktısı).",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "Sistem tepsisi bulunamadı. AdGuard Tray simgesiz çalışıyor — panelinizde bir sistem tepsisi/AppIndicator etkinleştirin.",
    "URL must start with http:// or https://":
        "URL, http:// veya https:// ile başlamalıdır",
    "adguard-cli path does not exist or is not executable.":
        "adguard-cli yolu mevcut değil veya çalıştırılabilir değil.",
    "That binary does not identify as adguard-cli. Save anyway?":
        "Bu çalıştırılabilir dosya kendini adguard-cli olarak tanıtmıyor. Yine de kaydedilsin mi?",
    "Update channel":                   "Güncelleme kanalı",
    "Switching update channel to {}…":  "Güncelleme kanalı değiştiriliyor: {}…",
    "Update channel set to {}":         "Güncelleme kanalı ayarlandı: {}",
    "Could not set update channel":     "Güncelleme kanalı ayarlanamadı",
    "Invalid channel: {}":              "Geçersiz kanal: {}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        "Henüz erişim günlüğü yok ({}). AdGuard, trafiği filtrelemeye başladığında bu günlüğü yazar; sistem hizmeti olarak çalıştığında günlük root kullanıcısına aittir ve buradan okunamaz.",
    'Cannot read the access log ({}): {}':
        "Erişim günlüğü okunamıyor ({}): {}",
    'Blocked':
        "Engellenen",
    'Blocked only':
        "Yalnızca engellenenler",
    "Refresh":
        "Yenile",
    'Allow selected domain':
        "Seçili alan adına izin ver",
    'Block selected domain':
        "Seçili alan adını engelle",
    'Activity':
        "Etkinlik",
    'Time':
        "Zaman",
    'Domain':
        "Alan adı",
    'Result':
        "Sonuç",
    'Rule':
        "Kural",
    'Size':
        "Boyut",
    'Count':
        "Sayı",
    'Could not read the access log.':
        "Erişim günlüğü okunamadı.",
    '{} lines not understood':
        "Anlaşılamayan satır: {}",
    'Not a valid domain: {}':
        "Geçerli bir alan adı değil: {}",
    'Source: {}':
        "Kaynak: {}",
    'Allowed':
        "İzin verilen",
    'Added rule: {}':
        "Kural eklendi: {}",
    'Requests per hour, {} to {} · busiest hour: {}':
        "Saatlik istekler, {} – {} · en yoğun saat: {}",
    'Last 24 hours':
        "Son 24 saat",
    'Last 7 days':
        "Son 7 gün",
    'Requests':
        "İstekler",
    'Traffic':
        "Trafik",

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        "{} sürümü mevcut (kurulu sürüm: {}).",
    'Application update':
        "Uygulama güncellemesi",
    'Check for update':
        "Güncellemeleri denetle",
    'Install update':
        "Güncellemeyi kur",
    'Installing update…':
        "Güncelleme kuruluyor…",
    'Restart now':
        "Şimdi yeniden başlat",
    'Later':
        "Daha sonra",
    'You are running the latest version ({}).':
        "En son sürümü kullanıyorsunuz ({}).",
    'Installation not recognised':
        "Kurulum türü tanınmadı",
    'Could not check for updates.':
        "Güncellemeler denetlenemedi.",
    'Update with: {}':
        "Güncellemek için: {}",
    'Installed with the AUR package {}':
        "AUR paketiyle kuruldu: {}",
    'Installed in {}':
        "Kurulum konumu: {}",
    'Running from a source checkout':
        "Kaynak kod kopyasından çalışıyor",
    'Version {} installed. Restart adguard-tray to use it.':
        "{} sürümü kuruldu. Kullanmak için adguard-tray uygulamasını yeniden başlatın.",
    'Unexpected answer from GitHub: {}':
        "GitHub'dan beklenmeyen yanıt: {}",
    'Download failed: {}':
        "İndirme başarısız oldu: {}",
    'Could not unpack the download: {}':
        "İndirilen arşiv çıkarılamadı: {}",
    'This installation is managed elsewhere: {}':
        "Bu kurulum başka bir yerden yönetiliyor: {}",
    'No permission to write to {}':
        "{} konumuna yazma izni yok",
    'GitHub returned {}.':
        "GitHub yanıtı: {}.",
    'No connection to GitHub: {}':
        "GitHub'a bağlanılamadı: {}",
    'The download does not contain adguard-tray.':
        "İndirilen arşiv adguard-tray içermiyor.",
    'The download says version {} instead of {} – aborted.':
        "İndirilen sürüm {}, beklenen sürüm {} – iptal edildi.",
    'GitHub is rate limiting this address. Try again later.':
        "GitHub bu adresin isteklerini sınırlıyor. Daha sonra tekrar deneyin.",
    'The download is larger than expected – aborted.':
        "İndirilen dosya beklenenden büyük – iptal edildi.",
    'Update failed: {}':
        "Güncelleme başarısız oldu: {}",
    'The archive contains unexpected paths – aborted.':
        "Arşivde beklenmeyen yollar var – iptal edildi.",
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        "Güncelleme başarısız oldu ve eski sürüm geri yüklenemedi. Yedek konumu: {}. Eski sürümü oradan geri yükleyin veya şu komutla yeniden kurun: {}",
    'Last 30 days':
        "Son 30 gün",
    'All time':
        "Tüm zamanlar",
    'Modified':
        "Değiştirilen",
    'Rules':
        "Kurallar",
    'Showing {} – show all':
        "Gösterilen: {} – tümünü göster",
    'history {}':
        "geçmiş: {}",
    'Filter list ID: {}':
        "Filtre listesi kimliği: {}",
    'App':
        "Uygulama",
    'Protocol':
        "Protokol",
    'Type':
        "Tür",
    'Reset history':
        "Geçmişi sıfırla",
    'Delete the stored history and read the log again.':
        "Kayıtlı geçmişi siler ve günlüğü yeniden okur.",
    'Delete the stored history? Only what the log still holds can be read back.':
        "Kayıtlı geçmiş silinsin mi? Yalnızca günlükte hâlâ bulunan kayıtlar yeniden okunabilir.",
    'History is not being updated: {}':
        "Geçmiş güncellenmiyor: {}",

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "AdGuard ayarlarında 1 kaydedilmemiş değişiklik",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "Güvenilir bir filtre, ziyaret ettiğiniz sayfalarda betik çalıştırabilir. Yalnızca tanıdığınız kaynaklardan gelen listelere güvenin.",
    "About":
        "Hakkında",
    "Actions for the selected filter":
        "Seçili filtre için eylemler",
    "Ad blocking":
        "Reklam engelleme",
    "Ad blocking is off, so the filter lists below have no effect.":
        "Reklam engelleme kapalı, bu nedenle aşağıdaki filtre listeleri etkisizdir.",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLI en yeni derlemesini indirip kurar.",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "AdGuard CLI bu bilgisayardaki lisansı unutur. Lisansı yeniden etkinleştirmeniz gerekir.",
    "AdGuard CLI logs":
        "AdGuard CLI günlükleri",
    "AdGuard CLI update finished.":
        "AdGuard CLI güncellemesi tamamlandı.",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "AdGuard Tray günlüğü",
    "AdGuard doesn't filter these websites.":
        "AdGuard bu web sitelerini filtrelemez.",
    "AdGuard is filtering this computer's traffic.":
        "AdGuard bu bilgisayarın trafiğini filtreliyor.",
    "AdGuard restarts to load the new lists.":
        "AdGuard, yeni listeleri yüklemek için yeniden başlatılıyor.",
    "AdGuard's reply did not say whether it is running.":
        "AdGuard'ın yanıtından çalışıp çalışmadığı anlaşılamadı.",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "AdGuard ayarlar dosyası bulunamadı ({}). Oluşturmak için adguard-cli komutunu bir kez çalıştırın.",
    "Add DNS filter by ID":
        "Kimliğe göre DNS filtresi ekle",
    "Add DNS filter from URL":
        "URL'den DNS filtresi ekle",
    "Add filter":
        "Filtre ekle",
    "Add filter by ID":
        "Kimliğe göre filtre ekle",
    "Add filter from URL":
        "URL'den filtre ekle",
    "Add rule":
        "Kural ekle",
    "Add to browsers":
        "Tarayıcılara ekle",
    "Add userscript":
        "Kullanıcı betiği ekle",
    "Add userscript…":
        "Kullanıcı betiği ekle…",
    "Add website":
        "Web sitesi ekle",
    "Add…":
        "Ekle…",
    "Advanced":
        "Gelişmiş",
    "All available":
        "Tüm mevcut olanlar",
    "Allow {}":
        "İzin ver: {}",
    "Also adds the certificate to this Firefox profile.":
        "Sertifikayı bu Firefox profiline de ekler.",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "Yeniden başlatmalarda ve hatalarda da bildirir. Bunun için notify-send (libnotify) veya çalışan bir bildirim hizmeti (örn. dunst, mako ya da KDE'ninki) gerekir.",
    "Appearance":
        "Görünüm",
    "Applies after AdGuard Tray restarts.":
        "AdGuard Tray yeniden başlatıldıktan sonra geçerli olur.",
    "Apply":
        "Uygula",
    "Apply your changes to AdGuard's settings before closing?":
        "Kapatmadan önce AdGuard ayarlarındaki değişiklikler uygulansın mı?",
    "Applying them restarts AdGuard if protection is on.":
        "Koruma açıksa uygulandıklarında AdGuard yeniden başlatılır.",
    "Asks GitHub for the newest release.":
        "GitHub'dan en yeni sürümü sorgular.",
    "At a glance":
        "Bir bakışta",
    "Automatic":
        "Otomatik",
    "Automatic – filter all apps":
        "Otomatik – tüm uygulamaları filtrele",
    "Benchmark":
        "Performans testi",
    "Beta":
        "Beta",
    "Block ECH in DNS records":
        "DNS kayıtlarındaki ECH'yi engelle",
    "Block domains before a connection is made.":
        "Bağlantı kurulmadan önce alan adlarını engeller.",
    "Block {}":
        "Engelle: {}",
    "Blocked (24 h)":
        "Engellenen (24 sa)",
    "Browser list ({})":
        "Tarayıcı listesi ({})",
    "By ID or name…":
        "Kimlik veya ada göre…",
    "Certificate":
        "Sertifika",
    "Certificate checks":
        "Sertifika denetimleri",
    "Changes are collected in the bar at the bottom and applied together.":
        "Değişiklikler alttaki çubukta toplanır ve birlikte uygulanır.",
    "Check again":
        "Tekrar denetle",
    "Check every":
        "Denetim aralığı",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "Chromium ve Firefox tabanlı tarayıcıların kendi sertifika deposu vardır.",
    "Close":
        "Kapat",
    "Controls which AdGuard CLI build “{}” installs.":
        "“{}” işleminin hangi AdGuard CLI derlemesini kuracağını belirler.",
    "Could not add the rule.":
        "Kural eklenemedi.",
    "Could not open {}":
        "Açılamadı: {}",
    "Could not read {}":
        "Okunamadı: {}",
    "Could not refresh. Showing data from {}.":
        "Yenilenemedi. Saat {} itibarıyla olan veriler gösteriliyor.",
    "Could not reset the history.":
        "Geçmiş sıfırlanamadı.",
    "Could not restart AdGuard.":
        "AdGuard yeniden başlatılamadı.",
    "Could not start protection.":
        "Koruma başlatılamadı.",
    "Could not stop protection.":
        "Koruma durdurulamadı.",
    "Create":
        "Oluştur",
    "Create certificate":
        "Sertifika oluştur",
    "Custom":
        "Özel",
    "DNS filter lists":
        "DNS filtre listeleri",
    "DNS filtering":
        "DNS filtreleme",
    "DNS filtering is off, so these lists have no effect.":
        "DNS filtreleme kapalı, bu nedenle bu listeler etkisizdir.",
    "DNS servers":
        "DNS sunucuları",
    "Dark":
        "Koyu",
    "Default":
        "Varsayılan",
    "Details":
        "Ayrıntılar",
    "Discard":
        "Vazgeç",
    "Don't filter":
        "Filtreleme yapma",
    "Don't trust":
        "Güvenme",
    "Downloads and installs the newest AdGuard CLI build.":
        "En yeni AdGuard CLI derlemesini indirip kurar.",
    "Duration":
        "Süre",
    "Export…":
        "Dışa aktar…",
    "Filter everything":
        "Her şeyi filtrele",
    "Filter in place":
        "Yerinde filtrele",
    "Filtering":
        "Filtreleme",
    "Follow system":
        "Sisteme uy",
    "From URL…":
        "URL'den…",
    "Go to updates":
        "Güncellemelere git",
    "HTTP proxy: {}":
        "HTTP proxy: {}",
    "HTTPS filtering":
        "HTTPS filtreleme",
    "How much detail AdGuard Tray writes to its own log.":
        "AdGuard Tray'in kendi günlüğüne ne kadar ayrıntı yazacağını belirler.",
    "ID {}":
        "Kimlik: {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "Bir site yüklenmiyorsa önce HTTP/3 filtrelemeyi kapatın. Diğer denetimler tüm siteleri korur – bunları yalnızca bu işe yaramadıysa kapatın.",
    "Included":
        "Dahil edildi",
    "Installed":
        "Kurulu olanlar",
    "License":
        "Lisans",
    "Light":
        "Açık",
    "Logs":
        "Günlükler",
    "MIT license":
        "MIT lisansı",
    "Maintenance":
        "Bakım",
    "Manual proxy":
        "El ile proxy",
    "Manual – only apps set to use the proxy":
        "El ile – yalnızca proxy'yi kullanan uygulamalar",
    "More":
        "Daha fazla",
    "Move down":
        "Aşağı taşı",
    "Move up":
        "Yukarı taşı",
    "Network":
        "Ağ",
    "Nightly":
        "Nightly",
    "No requests yet – AdGuard logs requests while protection is on.":
        "Henüz istek yok – AdGuard, koruma açıkken istekleri günlüğe kaydeder.",
    "Not added":
        "Eklenmedi",
    "Nothing matches your search.":
        "Aramanızla eşleşen sonuç yok.",
    "Notify me when protection turns on or off":
        "Koruma açıldığında veya kapandığında bildir",
    "Off":
        "Kapalı",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "Yalnızca DoH veya DoT kullanan tarayıcıları etkiler. “Kapalı” seçeneğinde bu tarayıcılar AdGuard'ın DNS filtrelemesini atlayabilir.",
    "Open AdGuard Tray":
        "AdGuard Tray'i aç",
    "Open exceptions":
        "İstisnaları aç",
    "Open folder":
        "Klasörü aç",
    "Open release page":
        "Sürüm sayfasını aç",
    "Pages":
        "Sayfalar",
    "Performance":
        "Performans",
    "Protection":
        "Koruma",
    "Protection started.":
        "Koruma başlatıldı.",
    "Protection stopped.":
        "Koruma durduruldu.",
    "Proxy mode":
        "Proxy modu",
    "Redirect to AdGuard's DNS":
        "AdGuard DNS'ine yönlendir",
    "Refresh this page (F5)":
        "Bu sayfayı yenile (F5)",
    "Release (stable)":
        "Kararlı (release)",
    "Remove rule":
        "Kuralı kaldır",
    "Remove “{}”?":
        "“{}” kaldırılsın mı?",
    "Remove…":
        "Kaldır…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "Mevcut AdGuard ayarları, {} dosyasındaki ayarlarla değiştirilsin mi?\n\nAyarların uygulanması için AdGuard yeniden başlatılır.",
    "Reset history…":
        "Geçmişi sıfırla…",
    "Reset…":
        "Sıfırla…",
    "Restart AdGuard":
        "AdGuard'ı yeniden başlat",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "Kurallar yalnızca otomatik proxy modunda geçerlidir. İlk eşleşen kural uygulanır, bu yüzden \"*\" kuralını en sona koyun.",
    "Safe Browsing":
        "Güvenli gezinti",
    "Save anyway":
        "Yine de kaydet",
    "Saved. AdGuard restarts to apply the change.":
        "Kaydedildi. Değişikliğin uygulanması için AdGuard yeniden başlatılıyor.",
    "Saved. Applies after AdGuard Tray restarts.":
        "Kaydedildi. AdGuard Tray yeniden başlatıldıktan sonra geçerli olur.",
    "Saved. The change applies when protection is turned on.":
        "Kaydedildi. Değişiklik, koruma açıldığında geçerli olur.",
    "Secure DNS and ECH":
        "Güvenli DNS ve ECH",
    "Secure DNS filtering":
        "Güvenli DNS filtreleme",
    "Set the path in Settings":
        "Yolu “Ayarlar” sayfasında belirle",
    "Settings":
        "Ayarlar",
    "Show":
        "Göster",
    "Show recent entries":
        "Son girdileri göster",
    "Skip HTTPS filtering":
        "HTTPS filtrelemeyi atla",
    "Some counts could not be loaded.":
        "Bazı sayılar yüklenemedi.",
    "Source code":
        "Kaynak kodu",
    "Start AdGuard Tray when I log in":
        "Oturum açtığımda AdGuard Tray'i başlat",
    "Startup":
        "Başlangıç",
    "Status checks":
        "Durum denetimleri",
    "Stealth mode":
        "Gizlilik modu",
    "System":
        "Sistem",
    "The new lists load when protection is turned on.":
        "Yeni listeler, koruma açıldığında yüklenir.",
    "Theme":
        "Tema",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "Bu işlem HTTP/3 filtrelemeyi, OCSP denetimlerini, Certificate Transparency denetimini ve güvenli DNS filtrelemeyi kapatır. Bu durumda iptal edilmiş veya hatalı verilmiş sertifikalar fark edilmez ve tarayıcılar, AdGuard'ın DNS filtresini atlayarak alan adlarını çözümleyebilir.",
    "Time range":
        "Zaman aralığı",
    "To keep it but stop using it, switch it off instead.":
        "Kaldırmadan kullanmayı bırakmak istiyorsanız bunun yerine kapatın.",
    "Top lists":
        "En çok eşleşen listeler",
    "Trust":
        "Güven",
    "Trust “{}”?":
        "“{}” filtresine güvenilsin mi?",
    "Trust…":
        "Güven…",
    "Turn off all strict checks…":
        "Tüm katı denetimleri kapat…",
    "Undo":
        "Geri al",
    "Unknown":
        "Bilinmiyor",
    "Unsaved changes":
        "Kaydedilmemiş değişiklikler",
    "Update AdGuard CLI…":
        "AdGuard CLI'yı güncelle…",
    "Update channel: {}":
        "Güncelleme kanalı: {}",
    "Updated {}":
        "Güncellendi: {}",
    "Updates":
        "Güncellemeler",
    "Used in manual mode only.":
        "Yalnızca el ile modda kullanılır.",
    "Userscripts update together with filters.":
        "Kullanıcı betikleri filtrelerle birlikte güncellenir.",
    "Uses XDG autostart (~/.config/autostart).":
        "XDG otomatik başlatma kullanılır (~/.config/autostart).",
    "Waiting for authorization…":
        "Yetkilendirme bekleniyor…",
    "Website exceptions":
        "Web sitesi istisnaları",
    "Websites":
        "Web siteleri",
    "example.com or a link":
        "example.com veya bir bağlantı",
    "expires {}":
        "bitiş: {}",
    "of {} requests in the last 24 hours":
        "/ son 24 saatteki {} istek",
    "{} of {} DNS filters on":
        "Etkin DNS filtresi: {} / {}",
    "{} of {} filters on":
        "Etkin filtre: {} / {}",
    "{} of {} on":
        "Etkin: {} / {}",
    "{} unsaved changes to AdGuard's settings":
        "AdGuard ayarlarında kaydedilmemiş değişiklik: {}",
    "“Follow system” uses your desktop's light or dark setting.":
        "“Sisteme uy” seçeneği, masaüstünüzün açık veya koyu ayarını kullanır.",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "Etkin",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "AdGuard sertifikası, bu sistemde bulunan tüm tarayıcı profillerine eklenecek.\n\nBu sayede AdGuard, bu tarayıcılardaki HTTPS trafiğini inceleyebilir. Önce tarayıcılarınızı kapatın – sertifika deposunu açılışta okurlar.",
    "Allow":
        "İzin ver",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "Önce AdGuard ayarlarındaki değişikliklerinizi uygulayın ya da bunlardan vazgeçin, ardından yeniden başlatın.",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "Otomatik: AdGuard, tüm uygulama trafiğini iptables ile kendine yönlendirir. El ile: AdGuard yalnızca aşağıdaki SOCKS5 ve HTTP portlarını dinler.",
    "Block":
        "Engelle",
    "Browser API blocking":
        "Tarayıcı API engelleme",
    "CRLite":
        "CRLite",
    "Cancel":
        "İptal",
    "Computers":
        "Bilgisayarlar",
    "Could not change the autostart entry.":
        "Otomatik başlatma girdisi değiştirilemedi.",
    "Could not export the logs.":
        "Günlükler dışa aktarılamadı.",
    "Could not export the settings.":
        "Ayarlar dışa aktarılamadı.",
    "Could not reset the license.":
        "Lisans sıfırlanamadı.",
    "Could not retrieve license info.":
        "Lisans bilgisi alınamadı.",
    "Could not run the benchmark.":
        "Performans testi çalıştırılamadı.",
    "Could not save the settings.":
        "Ayarlar kaydedilemedi.",
    "Could not set the update channel.":
        "Güncelleme kanalı ayarlanamadı.",
    "Could not update AdGuard CLI.":
        "AdGuard CLI güncellenemedi.",
    "Could not update the filters.":
        "Filtreler güncellenemedi.",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "DNS üst kaynak sunucusu.\n'default' = sistem DNS'i.\nÖrnekler: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com",
    "Expiration date":
        "Bitiş tarihi",
    "Expires":
        "Bitiş",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "Firefox profillerinde HTTP/3 yeniden açıldı – tarayıcıyı yeniden başlatın.",
    "License key":
        "Lisans anahtarı",
    "License type":
        "Lisans türü",
    "Manual":
        "El ile",
    "No exceptions.":
        "İstisna yok.",
    "OK":
        "Tamam",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "Açık: AdGuard, HTTP/3 (QUIC) trafiğini kendisi filtreler – deneyseldir ve bazı\ntarayıcılar kullanıcının kurduğu bir sertifika üzerinden HTTP/3'ü zaten reddeder.\nKapalı: AdGuard bunun yerine QUIC'i engeller, böylece tarayıcılar\ngüvenilir biçimde filtrelenen HTTP/2'ye geri döner.\nHer iki durumda da bu yalnızca otomatik modda geçerlidir – el ile modda\nHTTP/3 trafiği AdGuard'a hiç ulaşmaz.",
    "Owner":
        "Sahip",
    "Personal":
        "Kişisel",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "Proxy modu: {} – UDP 443 portu AdGuard'a yönlendirilir.",
    "Save adguard-cli path":
        "adguard-cli yolunu kaydet",
    "Search domains or rules…":
        "Alan adı veya kural ara…",
    "Settings file":
        "Ayarlar dosyası",
    "Status":
        "Durum",
    "Trial":
        "Deneme",
    "Turn HTTP/3 back on in Firefox profiles":
        "Firefox profillerinde HTTP/3'ü yeniden aç",
    "Turn off":
        "Kapat",
    "Turn off HTTP/3 in Firefox profiles":
        "Firefox profillerinde HTTP/3'ü kapat",
    "Turn off HTTP/3 in Firefox profiles…":
        "Firefox profillerinde HTTP/3'ü kapat…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "Firefox ailesindeki {} profilde HTTP/3 kapatılsın mı?\n\nBu profillerin trafiği artık AdGuard'ın filtreleyebildiği HTTP/2 üzerinden geçer. Ardından tarayıcıyı yeniden başlatın.",
    "Turn off all strict checks":
        "Tüm katı denetimleri kapat",
    "Unavailable until AdGuard CLI reports its current channel.":
        "AdGuard CLI geçerli kanalını bildirene kadar kullanılamaz.",
    "Update AdGuard CLI":
        "AdGuard CLI'yı güncelle",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "Yalnızca otomatik modda kullanılır. Aralıklar (80:5221,5300:49151) veya tek portlar (80,443,8080).",
    "{} of {}":
        "{} / {}",
    "{} of {} userscripts on":
        "Etkin kullanıcı betiği: {} / {}",
    "{}% blocked":
        "%{} engellendi",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "Can sıkıcı öğeler",
    "General":
        "Genel",
    "Language-specific":
        "Dile özgü",
    "Security":
        "Güvenlik",
    "Social widgets":
        "Sosyal araçlar",
    "Expired":
        "Süresi doldu",
    "Autostart on login":
        "Oturum açılışında otomatik başlat",
    "Add app rule":
        "Uygulama kuralı ekle",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "Joker karakterler kullanılabilir, örn. *steam* veya *EasyAntiCheat*.",
    "There is already a rule for '{}'.":
        "“{}” için zaten bir kural var.",
    "AdGuard settings":
        "AdGuard ayarları",
    "Ads and trackers are not blocked until you enable protection.":
        "Korumayı etkinleştirene kadar reklamlar ve izleyiciler engellenmez.",
    "Could not import the settings.":
        "Ayarlar içe aktarılamadı.",
    "Disable protection":
        "Korumayı devre dışı bırak",
    "Enable protection":
        "Korumayı etkinleştir",
    "Export and import":
        "Dışa ve içe aktarma",
    "Features":
        "Özellikler",
    "Import settings":
        "Ayarları içe aktar",
    "Import settings from…":
        "Ayarların alınacağı dosya…",
    "Import settings…":
        "Ayarları içe aktar…",
    "Import…":
        "İçe aktar…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "Filtreleri, kuralları ve yapılandırmayı bir zip dosyasına kaydeder ya da bir zip dosyasından yükler.",
    "Update":
        "Güncelle",
    "Version":
        "Sürüm",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "Bu bir ayar dışa aktarım dosyası değil: {}. “AdGuard ayarları” bölümündeki “Dışa aktar…” düğmesiyle kaydedilmiş bir dosya seçin.",
}
