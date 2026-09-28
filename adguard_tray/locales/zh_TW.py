"""Traditional Chinese (Taiwan, also used for Hong Kong and Macau)."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "語言",
    "English":                           "英文",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "已啟用 – 防護執行中",
    "Inactive – Protection stopped":        "未啟用 – 防護已停止",
    "Error retrieving status":              "取得狀態時發生錯誤",
    "adguard-cli not found":                "找不到 adguard-cli",
    "Unknown status":                       "未知狀態",
    "Checking status…":                     "正在檢查狀態…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "重新啟動",
    "Filters":                              "過濾器",
    "Loading…":                             "正在載入…",
    "Manage filters…":                      "管理過濾器…",
    "No userscripts installed":             "未安裝任何使用者腳本",
    "Manage userscripts…":                  "管理使用者腳本…",
    "Quit":                                 "結束",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "已啟用",
    "inactive":                             "未啟用",
    "System-wide filtering: {}":            "全系統過濾：{}",
    "Error: {}":                            "錯誤：{}",
    "AdGuard Tray – Error":                 "AdGuard Tray – 錯誤",
    "AdGuard is now active – protection running.":
        "AdGuard 已啟用 – 防護執行中。",
    "AdGuard has been stopped.":
        "AdGuard 已停止。",
    "Could not retrieve status.":
        "無法取得狀態。",
    "Command failed":                       "命令執行失敗",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " 秒",
    "How often adguard-cli status is checked automatically.":
        "自動檢查 adguard-cli 狀態的頻率。",
    "Log level:":                           "記錄等級：",
    "adguard-cli path:":                    "adguard-cli 路徑：",
    "auto-detect via PATH":                 "透過 PATH 自動偵測",
    "Browse…":                              "瀏覽…",
    "Select adguard-cli binary":            "選取 adguard-cli 執行檔",
    "Notifications":                        "通知",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "更新過濾器",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "更新所有過濾器、DNS 過濾器、使用者腳本、\nSafebrowsingV2 與 CRLite，並檢查應用程式更新。",
    "No filters found.":                    "找不到過濾器。",
    "Updating filters… (can take up to 2 minutes)":
        "正在更新過濾器…（最多可能需要 2 分鐘）",
    "Update completed.":                    "更新完成。",
    "Update failed.":                       "更新失敗。",
    "Installing: {}":                       "正在安裝：{}",
    "Filter installed.":                    "已安裝過濾器。",
    "Remove":                               "移除",
    "Remove filter":                        "移除過濾器",
    "Filter {} removed.":                   "過濾器 {} 已移除。",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        "從直接指向 .js 檔案的 URL 安裝使用者腳本",
    "No userscripts installed.":            "未安裝任何使用者腳本。",
    "Userscript URL (direct .js URL):":     "使用者腳本 URL（直接指向 .js 檔案的 URL）：",
    "Userscript installed.":                "已安裝使用者腳本。",
    'Remove "{}"':                          "移除「{}」",
    "Remove userscript":                    "移除使用者腳本",
    "'{}' removed.":                        "已移除「{}」。",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "找不到 adguard-cli。\n請透過官方指令碼或 AUR 安裝：\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "取得狀態時發生未知錯誤",
    "AdGuard {} ok":                        "AdGuard {} 成功",
    "AdGuard via systemctl {} ok":          "透過 systemctl {} AdGuard 成功",
    "'{}' failed – insufficient privileges?":
        "「{}」失敗 – 權限不足？",
    "Could not retrieve filter list":
        "無法取得過濾器清單",
    "Filter {} enabled":                    "過濾器 {} 已啟用",
    "Could not enable filter {}":           "無法啟用過濾器 {}",
    "Filter {} disabled":                   "過濾器 {} 已停用",
    "Could not disable filter {}":
        "無法停用過濾器 {}",
    "Filter installed":                     "已安裝過濾器",
    "Installation failed":                  "安裝失敗",
    "Filter {} removed":                    "過濾器 {} 已移除",
    "Could not remove filter {}":
        "無法移除過濾器 {}",
    "Filters updated":                      "已更新過濾器",
    "Update failed":                        "更新失敗",
    "Could not retrieve userscript list":
        "無法取得使用者腳本清單",
    "Userscript '{}' enabled":              "使用者腳本「{}」已啟用",
    "Could not enable userscript '{}'":
        "無法啟用使用者腳本「{}」",
    "Userscript '{}' disabled":             "使用者腳本「{}」已停用",
    "Could not disable userscript '{}'":
        "無法停用使用者腳本「{}」",
    "Userscript '{}' removed":              "使用者腳本「{}」已移除",
    "Could not remove userscript '{}'":
        "無法移除使用者腳本「{}」",
    "Userscript installed":                 "已安裝使用者腳本",
    "Other":                                "其他",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "搜尋過濾器…",
    "Search userscripts…":              "搜尋使用者腳本…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "無法載入 proxy.yaml。\n路徑：{}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "應用程式",
    "Mode:":                            "模式：",
    "Filtered ports:":                  "已過濾的連接埠：",
    "SOCKS5 port:":                     "SOCKS5 連接埠：",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "手動模式使用的 SOCKS5 代理連接埠。\n設為 -1 即可停用。",
    "HTTP port:":                       "HTTP 連接埠：",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "手動模式使用的 HTTP 代理連接埠。\n設為 -1 即可停用。",
    "Listen address:":                  "監聽位址：",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "代理伺服器監聽的位址。\n127.0.0.1 = 僅限本機。0.0.0.0 = 所有介面（需要身分驗證）。",
    "Worker threads:":                  "工作執行緒：",
    "Number of proxy worker threads.":  "代理伺服器的工作執行緒數量。",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "解密並過濾 HTTPS 流量。\n封鎖 https 網站上的廣告時需要此功能。\n系統上必須安裝受信任的根憑證。",
    "Enable TLS 1.3":                   "啟用 TLS 1.3",
    "Enable TLS 1.3 support for filtered connections.":
        "為已過濾的連線啟用 TLS 1.3 支援。",
    "Filter HTTP/3 (QUIC) – experimental":
        "過濾 HTTP/3（QUIC）– 實驗性功能",
    "OCSP certificate checks":          "OCSP 憑證檢查",
    "Enforce Certificate Transparency": "強制執行憑證透明度",
    "Filter EV certificate sites":      "過濾使用 EV 憑證的網站",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "預設不會過濾使用延伸驗證（EV）憑證的網站。\n啟用此選項即可一併過濾這些網站（例如銀行網站）。",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello（ECH）",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "啟用 ECH 以提升隱私。\n需要啟用 DNS 過濾。",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "過濾 DNS 查詢，在 DNS 層級封鎖廣告與追蹤器。\n使用本機 DNS 代理伺服器，上游伺服器可自行設定。",
    "Upstream:":                        "上游：",
    "Fallbacks:":                       "備用伺服器：",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "備用 DNS 伺服器（主要上游伺服器失效時使用）。\n'default' = 系統 DNS。以空格分隔的清單。\n範例：default 1.1.1.1",
    "Bootstraps:":                      "引導伺服器：",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "用於解析上游伺服器主機名稱的引導 DNS。\n'default' = 系統 DNS 的 IP。僅允許 IP 位址。\n範例：default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "從 SVCB/HTTPS DNS 記錄中移除 ECH 參數。\n僅在瀏覽器無法自動偵測 HTTPS 過濾時啟用。",
    "Master switch for all tracking protection features below.":
        "下方所有追蹤防護功能的總開關。",
    "Cookies":                          "Cookie",
    "Block third-party cookies":        "封鎖第三方 Cookie",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "在設定的時間後刪除第三方 Cookie。\n防止跨網站追蹤。",
    "Lifetime (minutes):":              "存留時間（分鐘）：",
    "0 = block immediately. Default: 180 minutes.":
        "0 = 立即封鎖。預設：180 分鐘。",
    "Block first-party cookies":        "封鎖第一方 Cookie",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "在設定的時間後刪除所有 Cookie（包括第一方）。\n警告：這會讓您登出所有網站。",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = 立即封鎖。預設：4320 分鐘（3 天）。",
    "Privacy":                          "隱私",
    "Hide / reduce User-Agent":         "隱藏/精簡 User-Agent",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "移除 User-Agent 中可識別身分的資訊。\n減少被指紋辨識的機會。",
    "Hide search queries in referrer":  "隱藏參照網址中的搜尋查詢",
    "Hides your search terms when clicking from a search engine to a website.":
        "從搜尋引擎點選前往網站時，隱藏搜尋字詞。",
    "Remove referrer from third-party requests":
        "移除第三方請求中的參照網址",
    "Prevents third-party sites from knowing which page you came from.":
        "防止第三方網站得知您來自哪個頁面。",
    "Send Do-Not-Track signal":         "傳送 Do-Not-Track 訊號",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "在請求中附帶 DNT 標頭。\n注意：大多數網站會忽略此訊號，但仍有部分網站會遵守。",
    "Disable third-party ETag cache":   "停用第三方 ETag 快取",
    "Prevents tracking via ETag caching in third-party content.":
        "防止透過第三方內容的 ETag 快取進行追蹤。",
    "Block third-party Authorization header":
        "封鎖第三方 Authorization 標頭",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "封鎖第三方請求中的 Authorization 標頭，以防止追蹤。",
    "Remove X-Client-Data header":      "移除 X-Client-Data 標頭",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "移除 Chrome 傳送給 Google 服務的 X-Client-Data 標頭。",
    "Block WebRTC":                     "封鎖 WebRTC",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "防止透過 WebRTC 洩漏 IP。\n可能導致視訊通話與部分網頁應用程式無法正常運作。",
    "Block Push API":                   "封鎖 Push API",
    "Blocks browser push notifications from websites.":
        "封鎖網站傳送的瀏覽器推播通知。",
    "Block Location API":               "封鎖位置 API",
    "Prevents websites from accessing your GPS location.":
        "防止網站存取您的 GPS 位置。",
    "Block Flash":                      "封鎖 Flash",
    "Blocks the Flash plugin.":
        "封鎖 Flash 外掛程式。",
    "Block Java":                       "封鎖 Java",
    "Disables Java plugins. JavaScript remains enabled.":
        "停用 Java 外掛程式。JavaScript 仍維持啟用。",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "啟用 Anti-DPI",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "修改傳出的封包資料，以規避深度封包檢測。\n適用於有網路審查的國家或地區。",
    "App pattern":
        "應用程式比對模式",
    "Skip outbound proxy":              "略過對外代理",
    "Don't route this app's traffic through outbound proxy":
        "不透過對外代理轉送此應用程式的流量",
    "Browser list included from {}":    "瀏覽器清單來源：{}",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "無法移除瀏覽器納入清單與萬用字元（*）規則。",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "針對惡意網站與網路釣魚網站發出警告。\n使用 AdGuard 的瀏覽安全資料庫。",
    "Send anonymous statistics":        "傳送匿名統計資料",
    "Send anonymous lookups to AdGuard.":
        "將匿名查詢傳送給 AdGuard。",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "使用 Mozilla 的 CRLite 進行憑證撤銷檢查。\n比傳統的 CRL/OCSP 檢查更快、更可靠。",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "將廣告封鎖過濾規則套用至 HTTP/HTTPS 請求。",
    "Save failed":                      "儲存失敗",
    "Could not save proxy.yaml:\n{}":   "無法儲存 proxy.yaml：\n{}",
    "Restarting AdGuard…":              "正在重新啟動 AdGuard…",
    "AdGuard restarted.":               "AdGuard 已重新啟動。",
    "Restart failed: {}":               "重新啟動失敗：{}",
    "Unknown error":                    "未知錯誤",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "新增",
    "Search exceptions…":               "搜尋例外…",
    "1 exception":                      "1 個例外",
    "{} exceptions":                    "{} 個例外",
    "'{}' is not a valid domain or IP address.":
        "「{}」不是有效的網域或 IP 位址。",
    "'{}' is already in the list.":     "「{}」已在清單中。",
    "Could not save exceptions:\n{}":
        "無法儲存例外：\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "概覽",
    "Userscripts":                      "使用者腳本",
    "Exceptions":                       "例外",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "重設授權",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "產生用於 HTTPS 過濾的根 CA 憑證。此憑證必須安裝在系統上並設為受信任。",
    "Checking for updates…":            "正在檢查更新…",
    "Firefox profile:":                 "Firefox 設定檔：",
    "(optional) e.g. abcd1234.MyProfile":
        "（選用）例如 abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "輸入過濾器 ID 或名稱：",
    "Filter added.":                    "已新增過濾器。",
    "Rename…":                          "重新命名…",
    "Rename filter":                    "重新命名過濾器",
    "New title:":                       "新標題：",
    "Filter renamed.":                  "已重新命名過濾器。",
    "Filter trust updated.":            "已更新過濾器信任設定。",
    "Filter URL:":                      "過濾器 URL：",
    "Title:":                           "標題：",
    "(optional)":                       "（選用）",
    "Trusted filter":                   "受信任的過濾器",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "搜尋 DNS 過濾器…",
    "No DNS filters found.":            "找不到 DNS 過濾器。",
    "DNS filter installed.":            "已安裝 DNS 過濾器。",
    "DNS filter added.":                "已新增 DNS 過濾器。",
    "Remove DNS filter":                "移除 DNS 過濾器",
    "DNS filter {} removed.":           "DNS 過濾器 {} 已移除。",
    "Rename DNS filter":                "重新命名 DNS 過濾器",
    "DNS filter renamed.":              "已重新命名 DNS 過濾器。",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "匯出記錄檔…",
    "Export AdGuard CLI logs to a zip file":
        "將 AdGuard CLI 記錄檔匯出為 zip 檔",
    "Export settings…":                 "匯出設定…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "執行加密與 HTTPS 過濾效能測試。",
    "Run benchmark":                    "執行效能測試",
    "Done.":                            "完成。",
    "Export logs to…":                  "匯出記錄檔至…",
    "Export settings to…":              "匯出設定至…",
    "Zip files (*.zip);;All files (*)":
        "Zip 檔案 (*.zip);;所有檔案 (*)",
    "Log file not found.":              "找不到記錄檔。",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "無法取得 DNS 過濾器清單",
    "DNS filter {} enabled":            "DNS 過濾器 {} 已啟用",
    "Could not enable DNS filter {}":   "無法啟用 DNS 過濾器 {}",
    "DNS filter {} disabled":           "DNS 過濾器 {} 已停用",
    "Could not disable DNS filter {}":  "無法停用 DNS 過濾器 {}",
    "DNS filter installed":             "已安裝 DNS 過濾器",
    "DNS filter {} removed":            "DNS 過濾器 {} 已移除",
    "Could not remove DNS filter {}":   "無法移除 DNS 過濾器 {}",
    "DNS filter added":                 "已新增 DNS 過濾器",
    "Could not add DNS filter":         "無法新增 DNS 過濾器",
    "DNS filter title updated":         "已更新 DNS 過濾器標題",
    "Could not set DNS filter title":   "無法設定 DNS 過濾器標題",
    "Filter added":                     "已新增過濾器",
    "Could not add filter":             "無法新增過濾器",
    "Filter trust updated":             "已更新過濾器信任設定",
    "Could not update filter trust":    "無法更新過濾器信任設定",
    "Filter title updated":             "已更新過濾器標題",
    "Could not set filter title":       "無法設定過濾器標題",
    "License reset":                    "已重設授權",
    "Could not reset license":          "無法重設授權",
    "Could not retrieve license info":  "無法取得授權資訊",
    "Certificate generated":            "已產生憑證",
    "Certificate generation failed":    "憑證產生失敗",
    "Logs exported":                    "已匯出記錄檔",
    "Log export failed":                "記錄檔匯出失敗",
    "Settings exported":                "已匯出設定",
    "Settings export failed":           "設定匯出失敗",
    "Settings imported":                "已匯入設定",
    "Settings import failed":           "設定匯入失敗",
    "Update check completed":           "已完成更新檢查",
    "Update check failed":              "更新檢查失敗",
    "Benchmark failed":                 "效能測試失敗",
    "AdGuard stopped (forced)":         "AdGuard 已停止（強制）",
    "Could not stop AdGuard – process may still be running":
        "無法停止 AdGuard – 處理程序可能仍在執行",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "在此系統上找不到 adguard-cli。\n\n建議的安裝方式（官方）：\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n替代方式（Arch Linux AUR）：\n  paru -S adguard-cli-bin\n\nAdGuard Tray 仍會載入，但在安裝 adguard-cli 之前無法啟動或停止防護。",
    "Copy install command":             "複製安裝命令",
    "Continue":                         "繼續",
    "AdGuard Tray is already running":  "AdGuard Tray 已在執行中",
    "Only one instance can run at a time. Check your system tray.":
        "一次只能執行一個執行個體。請查看系統匣。",
    "Authentication cancelled":         "已取消身分驗證",
    "Authorization failed":             "授權失敗",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "檢查網站的憑證是否已撤銷（OCSP）。\nAdGuard 會以非同步方式檢查，檢查太慢時會先放行連線，\n因此很少導致網站無法開啟。\n除非已確定問題出在這裡，否則請保持開啟。",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "強制執行憑證透明度檢查（Chrome 的 CT 政策）。\n自身憑證不符合 CT 規範的網站將不再被過濾，\n且瀏覽器可能拒絕開啟。大型網站皆符合規範，\n因此只有在網站回報憑證錯誤時才需要調整此項。",
    "Sites that don't load":
        "無法載入的網站",
    "Turn off HTTP/3 filtering":
        "關閉 HTTP/3 過濾",
    "No filters installed":
        "未安裝任何過濾器",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "防火牆規則已封鎖 HTTP/3；瀏覽器會改用 HTTP/2。",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "排除在過濾之外的應用程式（其 HTTP/3 流量也不會被過濾）：{}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuard 未執行 – 不會過濾任何內容。",
    "could not remove the previous certificate":
        "無法移除先前的憑證",
    "HTTP/3 state unknown":
        "HTTP/3 狀態未知",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "防火牆規則拒絕對外的 UDP 443，因此無法使用 QUIC。",
    "Browser policy disables QUIC: {}":
        "瀏覽器政策已停用 QUIC：{}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "瀏覽器可透過 HTTP/3（UDP 443）繞過 AdGuard。",
    "Checking…":
        "正在檢查…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "無法讀取 proxy.yaml – HTTP/3 狀態未知。",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "已關閉 HTTP/3 的 Firefox 系列設定檔：{}/{}",
    "HTTP/3 (QUIC)":
        "HTTP/3（QUIC）",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "AdGuard 已封鎖 HTTP/3；瀏覽器會改用經過過濾的 HTTP/2。",
    "HTTP/3 is filtered by AdGuard.":
        "HTTP/3 由 AdGuard 過濾。",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "已在 Firefox 設定檔中關閉 HTTP/3 – 請重新啟動瀏覽器。",
    "HTTPS filtering is off – nothing is filtered.":
        "HTTPS 過濾已關閉 – 不會過濾任何內容。",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "代理模式：{} – 只有經由代理伺服器傳送的流量才會被過濾，而瀏覽器不會透過代理伺服器傳送 QUIC。",
    "unknown":
        "未知",
    "AdGuard's certificate was not found. Generate it first.":
        "找不到 AdGuard 的憑證。請先產生憑證。",
    "Certificate could not be installed in any browser.":
        "無法在任何瀏覽器中安裝憑證。",
    "Certificate installed for {} of {} stores.":
        "已在 {}/{} 個憑證存放區中安裝憑證。",
    "Chromium-based browsers":
        "以 Chromium 為基礎的瀏覽器",
    "No browser certificate stores found.":
        "找不到瀏覽器憑證存放區。",
    "Restart your browsers for the certificate to take effect.":
        "請重新啟動瀏覽器，讓憑證生效。",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "請勿使用 sudo/pkexec 執行 – 憑證會安裝到您自己的瀏覽器設定檔",
    "certificate not found after import":
        "匯入後找不到憑證",
    "certutil not found – install the 'nss' package":
        "找不到 certutil – 請安裝「nss」套件",
    "not found":
        "找不到",
    "Could not read the filter list (unexpected CLI output).":
        "無法讀取過濾器清單（CLI 輸出不符預期）。",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "找不到系統匣。AdGuard Tray 正在以無圖示模式執行 — 請在面板中啟用系統匣/AppIndicator。",
    "URL must start with http:// or https://":
        "URL 必須以 http:// 或 https:// 開頭",
    "adguard-cli path does not exist or is not executable.":
        "adguard-cli 路徑不存在或無法執行。",
    "That binary does not identify as adguard-cli. Save anyway?":
        "此執行檔看起來不是 adguard-cli。仍要儲存嗎？",
    "Update channel":                   "更新頻道",
    "Switching update channel to {}…":  "正在將更新頻道切換為 {}…",
    "Update channel set to {}":         "已將更新頻道設為 {}",
    "Could not set update channel":     "無法設定更新頻道",
    "Invalid channel: {}":              "無效的頻道：{}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        "尚無存取記錄（{}）。AdGuard 過濾流量後才會寫入此記錄；若 AdGuard 以系統服務執行，記錄檔屬於 root，無法在此讀取。",
    'Cannot read the access log ({}): {}':
        "無法讀取存取記錄（{}）：{}",
    'Blocked':
        "已封鎖",
    'Blocked only':
        "僅顯示已封鎖",
    "Refresh":
        "重新整理",
    'Allow selected domain':
        "允許所選網域",
    'Block selected domain':
        "封鎖所選網域",
    'Activity':
        "活動",
    'Time':
        "時間",
    'Domain':
        "網域",
    'Result':
        "結果",
    'Rule':
        "規則",
    'Size':
        "大小",
    'Count':
        "次數",
    'Could not read the access log.':
        "無法讀取存取記錄。",
    '{} lines not understood':
        "{} 行無法解析",
    'Not a valid domain: {}':
        "無效的網域：{}",
    'Source: {}':
        "來源：{}",
    'Allowed':
        "已允許",
    'Added rule: {}':
        "已新增規則：{}",
    'Requests per hour, {} to {} · busiest hour: {}':
        "每小時請求數，{} 至 {} · 最繁忙時段：{}",
    'Last 24 hours':
        "最近 24 小時",
    'Last 7 days':
        "最近 7 天",
    'Requests':
        "請求",
    'Traffic':
        "流量",

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        "已有新版本 {}（目前版本 {}）。",
    'Application update':
        "應用程式更新",
    'Check for update':
        "檢查更新",
    'Install update':
        "安裝更新",
    'Installing update…':
        "正在安裝更新…",
    'Restart now':
        "立即重新啟動",
    'Later':
        "稍後",
    'You are running the latest version ({}).':
        "目前已是最新版本（{}）。",
    'Installation not recognised':
        "無法辨識安裝方式",
    'Could not check for updates.':
        "無法檢查更新。",
    'Update with: {}':
        "更新命令：{}",
    'Installed with the AUR package {}':
        "透過 AUR 套件 {} 安裝",
    'Installed in {}':
        "安裝位置：{}",
    'Running from a source checkout':
        "從原始碼目錄執行",
    'Version {} installed. Restart adguard-tray to use it.':
        "已安裝版本 {}。請重新啟動 adguard-tray 以使用新版本。",
    'Unexpected answer from GitHub: {}':
        "GitHub 傳回非預期的回應：{}",
    'Download failed: {}':
        "下載失敗：{}",
    'Could not unpack the download: {}':
        "無法解壓縮下載內容：{}",
    'This installation is managed elsewhere: {}':
        "此安裝由其他方式管理：{}",
    'No permission to write to {}':
        "無權寫入 {}",
    'GitHub returned {}.':
        "GitHub 傳回 {}。",
    'No connection to GitHub: {}':
        "無法連線至 GitHub：{}",
    'The download does not contain adguard-tray.':
        "下載內容不包含 adguard-tray。",
    'The download says version {} instead of {} – aborted.':
        "下載內容的版本為 {}，而非 {} – 已中止。",
    'GitHub is rate limiting this address. Try again later.':
        "GitHub 正在限制此位址的請求速率。請稍後再試。",
    'The download is larger than expected – aborted.':
        "下載內容大於預期 – 已中止。",
    'Update failed: {}':
        "更新失敗：{}",
    'The archive contains unexpected paths – aborted.':
        "壓縮檔包含非預期的路徑 – 已中止。",
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        "更新失敗，且無法還原舊版本。請從 {} 還原，或使用以下命令重新安裝：{}",
    'Last 30 days':
        "最近 30 天",
    'All time':
        "全部時間",
    'Modified':
        "已修改",
    'Rules':
        "規則",
    'Showing {} – show all':
        "目前顯示 {} – 顯示全部",
    'history {}':
        "歷史記錄 {}",
    'Filter list ID: {}':
        "過濾清單 ID：{}",
    'App':
        "應用程式",
    'Protocol':
        "通訊協定",
    'Type':
        "類型",
    'Reset history':
        "重設歷史記錄",
    'Delete the stored history and read the log again.':
        "刪除已儲存的歷史記錄，並重新讀取記錄檔。",
    'Delete the stored history? Only what the log still holds can be read back.':
        "要刪除已儲存的歷史記錄嗎？只能重新讀取記錄檔中仍保留的內容。",
    'History is not being updated: {}':
        "歷史記錄未更新：{}",

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "AdGuard 設定有 1 項未儲存的變更",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "受信任的過濾器可在您造訪的網頁中執行腳本。請只信任來自已知來源的清單。",
    "About":
        "關於",
    "Actions for the selected filter":
        "所選過濾器的動作",
    "Ad blocking":
        "廣告封鎖",
    "Ad blocking is off, so the filter lists below have no effect.":
        "廣告封鎖已關閉，因此下方的過濾清單不會生效。",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLI 會下載並安裝其最新版本。",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "AdGuard CLI 會清除此電腦上的授權。您必須重新啟用授權。",
    "AdGuard CLI logs":
        "AdGuard CLI 記錄檔",
    "AdGuard CLI update finished.":
        "已完成 AdGuard CLI 更新。",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "AdGuard Tray 記錄",
    "AdGuard doesn't filter these websites.":
        "AdGuard 不會過濾這些網站。",
    "AdGuard is filtering this computer's traffic.":
        "AdGuard 正在過濾這台電腦的流量。",
    "AdGuard restarts to load the new lists.":
        "AdGuard 會重新啟動以載入新清單。",
    "AdGuard's reply did not say whether it is running.":
        "無法從 AdGuard 的回應判斷其是否正在執行。",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "找不到 AdGuard 的設定檔（{}）。請先執行一次 adguard-cli 以建立設定檔。",
    "Add DNS filter by ID":
        "依 ID 新增 DNS 過濾器",
    "Add DNS filter from URL":
        "從 URL 新增 DNS 過濾器",
    "Add filter":
        "新增過濾器",
    "Add filter by ID":
        "依 ID 新增過濾器",
    "Add filter from URL":
        "從 URL 新增過濾器",
    "Add rule":
        "新增規則",
    "Add to browsers":
        "新增至瀏覽器",
    "Add userscript":
        "新增使用者腳本",
    "Add userscript…":
        "新增使用者腳本…",
    "Add website":
        "新增網站",
    "Add…":
        "新增…",
    "Advanced":
        "進階",
    "All available":
        "全部可用",
    "Allow {}":
        "允許 {}",
    "Also adds the certificate to this Firefox profile.":
        "同時將憑證新增至此 Firefox 設定檔。",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "重新啟動和發生錯誤時也會通知。需要 notify-send（libnotify）或執行中的通知服務，例如 dunst、mako 或 KDE 的通知服務。",
    "Appearance":
        "外觀",
    "Applies after AdGuard Tray restarts.":
        "重新啟動 AdGuard Tray 後生效。",
    "Apply":
        "套用",
    "Apply your changes to AdGuard's settings before closing?":
        "關閉前要將變更套用至 AdGuard 設定嗎？",
    "Applying them restarts AdGuard if protection is on.":
        "若防護已開啟，套用變更會重新啟動 AdGuard。",
    "Asks GitHub for the newest release.":
        "向 GitHub 查詢最新發行版本。",
    "At a glance":
        "概況",
    "Automatic":
        "自動",
    "Automatic – filter all apps":
        "自動 – 過濾所有應用程式",
    "Benchmark":
        "效能測試",
    "Beta":
        "測試版",
    "Block ECH in DNS records":
        "在 DNS 記錄中封鎖 ECH",
    "Block domains before a connection is made.":
        "在建立連線之前封鎖網域。",
    "Block {}":
        "封鎖 {}",
    "Blocked (24 h)":
        "已封鎖（24 小時）",
    "Browser list ({})":
        "瀏覽器清單（{}）",
    "By ID or name…":
        "依 ID 或名稱新增…",
    "Certificate":
        "憑證",
    "Certificate checks":
        "憑證檢查",
    "Changes are collected in the bar at the bottom and applied together.":
        "變更會彙整在底部列中，並一起套用。",
    "Check again":
        "重新檢查",
    "Check every":
        "檢查間隔",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "以 Chromium 和 Firefox 為基礎的瀏覽器使用各自的憑證存放區。",
    "Close":
        "關閉",
    "Controls which AdGuard CLI build “{}” installs.":
        "控制「{}」會安裝哪個 AdGuard CLI 版本。",
    "Could not add the rule.":
        "無法新增規則。",
    "Could not open {}":
        "無法開啟 {}",
    "Could not read {}":
        "無法讀取 {}",
    "Could not refresh. Showing data from {}.":
        "無法重新整理。目前顯示 {} 時的資料。",
    "Could not reset the history.":
        "無法重設歷史記錄。",
    "Could not restart AdGuard.":
        "無法重新啟動 AdGuard。",
    "Could not start protection.":
        "無法啟動防護。",
    "Could not stop protection.":
        "無法停止防護。",
    "Create":
        "建立",
    "Create certificate":
        "建立憑證",
    "Custom":
        "自訂",
    "DNS filter lists":
        "DNS 過濾清單",
    "DNS filtering":
        "DNS 過濾",
    "DNS filtering is off, so these lists have no effect.":
        "DNS 過濾已關閉，因此這些清單不會生效。",
    "DNS servers":
        "DNS 伺服器",
    "Dark":
        "深色",
    "Default":
        "預設",
    "Details":
        "詳細資訊",
    "Discard":
        "捨棄",
    "Don't filter":
        "不過濾",
    "Don't trust":
        "不信任",
    "Downloads and installs the newest AdGuard CLI build.":
        "下載並安裝最新的 AdGuard CLI 版本。",
    "Duration":
        "耗時",
    "Export…":
        "匯出…",
    "Filter everything":
        "全部過濾",
    "Filter in place":
        "就地過濾",
    "Filtering":
        "過濾",
    "Follow system":
        "跟隨系統",
    "From URL…":
        "從 URL 新增…",
    "Go to updates":
        "前往更新",
    "HTTP proxy: {}":
        "HTTP 代理：{}",
    "HTTPS filtering":
        "HTTPS 過濾",
    "How much detail AdGuard Tray writes to its own log.":
        "AdGuard Tray 寫入自身記錄的詳細程度。",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "若網站無法載入，請先關閉 HTTP/3 過濾。其他檢查會保護所有網站，請僅在上述方法無效時才關閉它們。",
    "Included":
        "已包含",
    "Installed":
        "已安裝",
    "License":
        "授權",
    "Light":
        "淺色",
    "Logs":
        "記錄檔",
    "MIT license":
        "MIT 授權條款",
    "Maintenance":
        "維護",
    "Manual proxy":
        "手動代理",
    "Manual – only apps set to use the proxy":
        "手動 – 僅限設定為使用代理的應用程式",
    "More":
        "更多",
    "Move down":
        "下移",
    "Move up":
        "上移",
    "Network":
        "網路",
    "Nightly":
        "每夜版",
    "No requests yet – AdGuard logs requests while protection is on.":
        "尚無請求 – 防護開啟時，AdGuard 會記錄請求。",
    "Not added":
        "未新增",
    "Nothing matches your search.":
        "找不到符合的結果。",
    "Notify me when protection turns on or off":
        "防護開啟或關閉時通知我",
    "Off":
        "關閉",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "僅影響使用 DoH 或 DoT 的瀏覽器。設為「關閉」時，這些瀏覽器可繞過 AdGuard 的 DNS 過濾。",
    "Open AdGuard Tray":
        "開啟 AdGuard Tray",
    "Open exceptions":
        "開啟例外",
    "Open folder":
        "開啟資料夾",
    "Open release page":
        "開啟發行頁面",
    "Pages":
        "頁面",
    "Performance":
        "效能",
    "Protection":
        "防護",
    "Protection started.":
        "防護已啟動。",
    "Protection stopped.":
        "防護已停止。",
    "Proxy mode":
        "代理模式",
    "Redirect to AdGuard's DNS":
        "重新導向至 AdGuard 的 DNS",
    "Refresh this page (F5)":
        "重新整理此頁面（F5）",
    "Release (stable)":
        "正式版（穩定）",
    "Remove rule":
        "移除規則",
    "Remove “{}”?":
        "要移除「{}」嗎？",
    "Remove…":
        "移除…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "要以 {} 中的設定取代目前的 AdGuard 設定嗎？\n\nAdGuard 將重新啟動以套用這些設定。",
    "Reset history…":
        "重設歷史記錄…",
    "Reset…":
        "重設…",
    "Restart AdGuard":
        "重新啟動 AdGuard",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "規則僅在自動代理模式下生效。系統會套用第一條符合的規則，因此請將 \"*\" 放在最後。",
    "Safe Browsing":
        "瀏覽安全",
    "Save anyway":
        "仍要儲存",
    "Saved. AdGuard restarts to apply the change.":
        "已儲存。AdGuard 將重新啟動以套用變更。",
    "Saved. Applies after AdGuard Tray restarts.":
        "已儲存。重新啟動 AdGuard Tray 後生效。",
    "Saved. The change applies when protection is turned on.":
        "已儲存。變更將在開啟防護後生效。",
    "Secure DNS and ECH":
        "安全 DNS 與 ECH",
    "Secure DNS filtering":
        "安全 DNS 過濾",
    "Set the path in Settings":
        "在「設定」中指定路徑",
    "Settings":
        "設定",
    "Show":
        "顯示",
    "Show recent entries":
        "顯示最近記錄",
    "Skip HTTPS filtering":
        "略過 HTTPS 過濾",
    "Some counts could not be loaded.":
        "無法載入部分統計數字。",
    "Source code":
        "原始碼",
    "Start AdGuard Tray when I log in":
        "登入時啟動 AdGuard Tray",
    "Startup":
        "啟動",
    "Status checks":
        "狀態檢查",
    "Stealth mode":
        "隱身模式",
    "System":
        "系統",
    "The new lists load when protection is turned on.":
        "開啟防護後將載入新清單。",
    "Theme":
        "主題",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "這會關閉 HTTP/3 過濾、OCSP 檢查、憑證透明度和安全 DNS 過濾。屆時已撤銷或誤發的憑證將不會被察覺，瀏覽器也能繞過 AdGuard 的 DNS 過濾器進行解析。",
    "Time range":
        "時間範圍",
    "To keep it but stop using it, switch it off instead.":
        "若要保留但不再使用，請改為將其關閉。",
    "Top lists":
        "排行榜",
    "Trust":
        "信任",
    "Trust “{}”?":
        "要信任「{}」嗎？",
    "Trust…":
        "信任…",
    "Turn off all strict checks…":
        "關閉所有嚴格檢查…",
    "Undo":
        "復原",
    "Unknown":
        "未知",
    "Unsaved changes":
        "未儲存的變更",
    "Update AdGuard CLI…":
        "更新 AdGuard CLI…",
    "Update channel: {}":
        "更新頻道：{}",
    "Updated {}":
        "更新於 {}",
    "Updates":
        "更新",
    "Used in manual mode only.":
        "僅在手動模式下使用。",
    "Userscripts update together with filters.":
        "使用者腳本會與過濾器一起更新。",
    "Uses XDG autostart (~/.config/autostart).":
        "使用 XDG 自動啟動（~/.config/autostart）。",
    "Waiting for authorization…":
        "正在等待授權…",
    "Website exceptions":
        "網站例外",
    "Websites":
        "網站",
    "example.com or a link":
        "example.com 或連結",
    "expires {}":
        "{} 到期",
    "of {} requests in the last 24 hours":
        "最近 24 小時共 {} 個請求",
    "{} of {} DNS filters on":
        "已開啟 {}/{} 個 DNS 過濾器",
    "{} of {} filters on":
        "已開啟 {}/{} 個過濾器",
    "{} of {} on":
        "已開啟 {}/{}",
    "{} unsaved changes to AdGuard's settings":
        "AdGuard 設定有 {} 項未儲存的變更",
    "“Follow system” uses your desktop's light or dark setting.":
        "「跟隨系統」會使用桌面的淺色或深色設定。",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "有效",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "AdGuard 的憑證將新增至此系統上找到的所有瀏覽器設定檔。\n\n這樣 AdGuard 才能檢查這些瀏覽器的 HTTPS 流量。請先關閉瀏覽器 – 瀏覽器會在啟動時讀取憑證存放區。",
    "Allow":
        "允許",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "請先套用或捨棄對 AdGuard 設定的變更，再重新啟動。",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "自動：AdGuard 透過 iptables 將所有應用程式的流量重新導向至自身。手動：AdGuard 僅監聽下方的 SOCKS5 與 HTTP 連接埠。",
    "Block":
        "封鎖",
    "Browser API blocking":
        "瀏覽器 API 封鎖",
    "CRLite":
        "CRLite",
    "Cancel":
        "取消",
    "Computers":
        "電腦",
    "Could not change the autostart entry.":
        "無法變更自動啟動項目。",
    "Could not export the logs.":
        "無法匯出記錄檔。",
    "Could not export the settings.":
        "無法匯出設定。",
    "Could not reset the license.":
        "無法重設授權。",
    "Could not retrieve license info.":
        "無法取得授權資訊。",
    "Could not run the benchmark.":
        "無法執行效能測試。",
    "Could not save the settings.":
        "無法儲存設定。",
    "Could not set the update channel.":
        "無法設定更新頻道。",
    "Could not update AdGuard CLI.":
        "無法更新 AdGuard CLI。",
    "Could not update the filters.":
        "無法更新過濾器。",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "DNS 上游伺服器。\n'default' = 系統 DNS。\n範例：1.1.1.1、https://dns.google/dns-query、\ntls://dns.adguard.com、quic://dns.adguard.com",
    "Expiration date":
        "到期日",
    "Expires":
        "到期",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "已在 Firefox 設定檔中重新開啟 HTTP/3 – 請重新啟動瀏覽器。",
    "License key":
        "授權金鑰",
    "License type":
        "授權類型",
    "Manual":
        "手動",
    "No exceptions.":
        "沒有例外。",
    "OK":
        "確定",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "開啟：AdGuard 自行過濾 HTTP/3（QUIC）– 實驗性功能，且部分\n瀏覽器本來就不接受透過使用者安裝的憑證使用 HTTP/3。\n關閉：AdGuard 改為封鎖 QUIC，讓瀏覽器改用 HTTP/2，\n而 HTTP/2 可穩定過濾。\n無論哪種設定，都只在自動模式下適用 – 在手動模式下，\nHTTP/3 流量根本不會送達 AdGuard。",
    "Owner":
        "擁有者",
    "Personal":
        "個人版",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "代理模式：{} – UDP 連接埠 443 會重新導向至 AdGuard。",
    "Save adguard-cli path":
        "儲存 adguard-cli 路徑",
    "Search domains or rules…":
        "搜尋網域或規則…",
    "Settings file":
        "設定檔",
    "Status":
        "狀態",
    "Trial":
        "試用版",
    "Turn HTTP/3 back on in Firefox profiles":
        "在 Firefox 設定檔中重新開啟 HTTP/3",
    "Turn off":
        "關閉",
    "Turn off HTTP/3 in Firefox profiles":
        "在 Firefox 設定檔中關閉 HTTP/3",
    "Turn off HTTP/3 in Firefox profiles…":
        "在 Firefox 設定檔中關閉 HTTP/3…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "要在 {} 個 Firefox 系列設定檔中關閉 HTTP/3 嗎？\n\n之後其流量會改用 HTTP/2，而 AdGuard 可以過濾 HTTP/2。完成後請重新啟動瀏覽器。",
    "Turn off all strict checks":
        "關閉所有嚴格檢查",
    "Unavailable until AdGuard CLI reports its current channel.":
        "在 AdGuard CLI 回報目前的更新頻道之前無法使用。",
    "Update AdGuard CLI":
        "更新 AdGuard CLI",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "僅在自動模式下使用。可填寫範圍（80:5221,5300:49151）或單一連接埠（80,443,8080）。",
    "{} of {}":
        "{}/{}",
    "{} of {} userscripts on":
        "已開啟 {}/{} 個使用者腳本",
    "{}% blocked":
        "已封鎖 {}%",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "惱人元素",
    "General":
        "一般",
    "Language-specific":
        "語言特定",
    "Security":
        "安全",
    "Social widgets":
        "社群小工具",
    "Expired":
        "已過期",
    "Autostart on login":
        "登入時自動啟動",
    "Add app rule":
        "新增應用程式規則",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "支援萬用字元，例如 *steam* 或 *EasyAntiCheat*。",
    "There is already a rule for '{}'.":
        "已有適用於「{}」的規則。",
    "AdGuard settings":
        "AdGuard 設定",
    "Ads and trackers are not blocked until you enable protection.":
        "啟用防護後才會封鎖廣告和追蹤器。",
    "Could not import the settings.":
        "無法匯入設定。",
    "Disable protection":
        "停用防護",
    "Enable protection":
        "啟用防護",
    "Export and import":
        "匯出與匯入",
    "Features":
        "功能",
    "Import settings":
        "匯入設定",
    "Import settings from…":
        "從…匯入設定",
    "Import settings…":
        "匯入設定…",
    "Import…":
        "匯入…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "將過濾器、規則和設定儲存為 zip 檔，或從 zip 檔載入。",
    "Update":
        "更新",
    "Version":
        "版本",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "{} 不是設定匯出檔。請選擇在「AdGuard 設定」下使用「匯出…」儲存的檔案。",

    # ── AdGuard VPN, outbound proxy, install ──────────────────────────
    "Press Enter to close this window.":
        "按 Enter 鍵關閉此視窗。",
    "No terminal app was found. The install command is on the clipboard: paste it into a terminal.":
        "找不到終端機應用程式。安裝命令已複製到剪貼簿，請將其貼到終端機中執行。",
    "Finish the installation in the terminal, then press Refresh.":
        "請在終端機中完成安裝，然後按下「重新整理」。",
    "Open in a terminal":
        "在終端機中開啟",
    "AdGuard VPN":
        "AdGuard VPN",
    "AdGuard's VPN for Linux (adguardvpn-cli) runs next to AdGuard CLI. AdGuard Tray checks that their settings fit together; it does not connect the VPN or log in.":
        "AdGuard 的 Linux 版 VPN（adguardvpn-cli）會與 AdGuard CLI 並行運作。AdGuard Tray 會檢查兩者的設定是否相容，但不會連線到 VPN，也不會登入。",
    "Install…":
        "安裝…",
    "Outbound proxy":
        "對外代理",
    "AdGuard sends its own connections through this proxy, for example through AdGuard VPN in SOCKS5 mode.":
        "AdGuard 會透過此代理傳送自身的連線，例如透過 SOCKS5 模式的 AdGuard VPN。",
    "Use an outbound proxy":
        "使用對外代理",
    "Host":
        "主機",
    "Port":
        "連接埠",
    "Not installed.":
        "未安裝。",
    "AdGuard VPN is set to TUN mode while AdGuard filters in automatic mode. Connected like this, traffic loops between the two – AdGuard does not support this combination.":
        "AdGuard VPN 已設為 TUN 模式，而 AdGuard 正以自動模式過濾。若在此狀態下連線，流量會在兩者之間形成迴圈 – AdGuard 不支援這種組合。",
    "AdGuard VPN now uses SOCKS5 mode. Press Apply to send AdGuard's traffic through it, and reconnect AdGuard VPN if it is connected.":
        "AdGuard VPN 現在使用 SOCKS5 模式。按下「套用」即可讓 AdGuard 的流量經由它傳送；若 AdGuard VPN 已連線，請重新連線。",
    "AdGuard VPN CLI":
        "AdGuard VPN CLI",
    "Installed, but its settings could not be read: {}":
        "已安裝，但無法讀取其設定：{}",
    "Route AdGuard through the VPN":
        "透過 VPN 轉送 AdGuard 流量",
    "Could not switch AdGuard VPN to SOCKS5 mode.":
        "無法將 AdGuard VPN 切換為 SOCKS5 模式。",
    "Installed · SOCKS5 mode on {}:{}":
        "已安裝 · SOCKS5 模式（{}:{}）",
    "Installed · TUN mode":
        "已安裝 · TUN 模式",
    "Installed · {} mode":
        "已安裝 · {} 模式",
}
