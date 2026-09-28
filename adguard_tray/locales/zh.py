"""Simplified Chinese."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "语言",
    "English":                           "英语",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "已激活 – 保护运行中",
    "Inactive – Protection stopped":        "未激活 – 保护已停止",
    "Error retrieving status":              "获取状态出错",
    "adguard-cli not found":                "未找到 adguard-cli",
    "Unknown status":                       "未知状态",
    "Checking status…":                     "正在检查状态…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "重启",
    "Filters":                              "过滤器",
    "Loading…":                             "加载中…",
    "Manage filters…":                      "管理过滤器…",
    "No userscripts installed":             "未安装用户脚本",
    "Manage userscripts…":                  "管理用户脚本…",
    "Quit":                                 "退出",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "已激活",
    "inactive":                             "未激活",
    "System-wide filtering: {}":            "系统范围过滤：{}",
    "Error: {}":                            "错误：{}",
    "AdGuard Tray – Error":                 "AdGuard Tray – 错误",
    "AdGuard is now active – protection running.":
        "AdGuard 现已激活 – 保护运行中。",
    "AdGuard has been stopped.":
        "AdGuard 已停止。",
    "Could not retrieve status.":
        "无法获取状态。",
    "Command failed":                       "命令失败",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " 秒",
    "How often adguard-cli status is checked automatically.":
        "自动检查 adguard-cli 状态的频率。",
    "Log level:":                           "日志级别：",
    "adguard-cli path:":                    "adguard-cli 路径：",
    "auto-detect via PATH":                 "通过 PATH 自动检测",
    "Browse…":                              "浏览…",
    "Select adguard-cli binary":            "选择 adguard-cli 二进制文件",
    "Notifications":                        "通知",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "更新过滤器",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "更新所有过滤器、DNS 过滤器、用户脚本，\n"
        "SafebrowsingV2、CRLite 并检查应用更新。",
    "No filters found.":                    "未找到过滤器。",
    "Updating filters… (can take up to 2 minutes)":
        "正在更新过滤器…（可能需要最多 2 分钟）",
    "Update completed.":                    "更新完成。",
    "Update failed.":                       "更新失败。",
    "Installing: {}":                       "正在安装：{}",
    "Filter installed.":                    "过滤器已安装。",
    "Remove":                               "移除",
    "Remove filter":                        "移除过滤器",
    "Filter {} removed.":                   "过滤器 {} 已移除。",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        "从直接的 .js URL 安装用户脚本",
    "No userscripts installed.":            "未安装用户脚本。",
    "Userscript URL (direct .js URL):":     "用户脚本 URL（直接 .js URL）：",
    "Userscript installed.":                "用户脚本已安装。",
    'Remove "{}"':                          "移除 “{}”",
    "Remove userscript":                    "移除用户脚本",
    "'{}' removed.":                        "'{}' 已移除。",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "未找到 adguard-cli。\n"
        "通过官方脚本或 AUR 安装：\n"
        "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
        "  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "获取状态时发生未知错误",
    "AdGuard {} ok":                        "AdGuard {} 正常",
    "AdGuard via systemctl {} ok":          "通过 systemctl 的 AdGuard {} 正常",
    "'{}' failed – insufficient privileges?":
        "'{}' 失败 – 权限不足？",
    "Could not retrieve filter list":
        "无法获取过滤器列表",
    "Filter {} enabled":                    "过滤器 {} 已启用",
    "Could not enable filter {}":           "无法启用过滤器 {}",
    "Filter {} disabled":                   "过滤器 {} 已禁用",
    "Could not disable filter {}":          "无法禁用过滤器 {}",
    "Filter installed":                     "过滤器已安装",
    "Installation failed":                  "安装失败",
    "Filter {} removed":                    "过滤器 {} 已移除",
    "Could not remove filter {}":          "无法移除过滤器 {}",
    "Filters updated":                      "过滤器已更新",
    "Update failed":                        "更新失败",
    "Could not retrieve userscript list":
        "无法获取用户脚本列表",
    "Userscript '{}' enabled":              "用户脚本 '{}' 已启用",
    "Could not enable userscript '{}'":
        "无法启用用户脚本 '{}'",
    "Userscript '{}' disabled":             "用户脚本 '{}' 已禁用",
    "Could not disable userscript '{}'":
        "无法禁用用户脚本 '{}'",
    "Userscript '{}' removed":              "用户脚本 '{}' 已移除",
    "Could not remove userscript '{}'":
        "无法移除用户脚本 '{}'",
    "Userscript installed":                 "用户脚本已安装",
    "Other":                                "其他",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "搜索过滤器…",
    "Search userscripts…":              "搜索用户脚本…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "无法加载 proxy.yaml。\n路径：{}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "应用程序",
    "Mode:":                            "模式：",
    "Filtered ports:":                  "过滤的端口：",
    "SOCKS5 port:":                     "SOCKS5 端口：",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "手动模式的 SOCKS5 代理端口。\n设置为 -1 以禁用。",
    "HTTP port:":                       "HTTP 端口：",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "手动模式的 HTTP 代理端口。\n设置为 -1 以禁用。",
    "Listen address:":                  "监听地址：",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "代理监听的地址。\n"
        "127.0.0.1 = 仅本地。0.0.0.0 = 所有接口（需要身份验证）。",
    "Worker threads:":                  "工作线程：",
    "Number of proxy worker threads.":  "代理工作线程数量。",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "解密并过滤 HTTPS 流量。\n需要阻止 https 网站上的广告。\n需要在系统上安装受信任的根证书。",
    "Enable TLS 1.3":                   "启用 TLS 1.3",
    "Enable TLS 1.3 support for filtered connections.":
        "为过滤的连接启用 TLS 1.3 支持。",
    "Filter HTTP/3 (QUIC) – experimental":
        "过滤 HTTP/3 (QUIC) – 实验性",
    "OCSP certificate checks":          "OCSP 证书检查",
    "Enforce Certificate Transparency": "强制证书透明度",
    "Filter EV certificate sites":      "过滤 EV 证书网站",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "默认情况下，具有扩展验证证书的网站不会被过滤。\n"
        "启用此选项以过滤它们（例如银行网站）。",
    "Encrypted Client Hello (ECH)":     "加密客户端 Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "启用 ECH 以获得更好的隐私。\n需要启用 DNS 过滤。",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "过滤 DNS 查询以在 DNS 级别阻止广告和跟踪器。\n"
        "使用具有可配置上游的本地 DNS 代理。",
    "Upstream:":                        "上游：",
    "Fallbacks:":                       "后备：",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "后备 DNS 服务器（当主上游失败时使用的）。\n"
        "'default' = 系统 DNS。空格分隔的列表。\n"
        "示例：default 1.1.1.1",
    "Bootstraps:":                      "引导：",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "用于解析上游主机名的引导 DNS。\n"
        "'default' = 系统 DNS IP。仅允许 IP 地址。\n"
        "示例：default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "从 SVCB/HTTPS DNS 记录中移除 ECH 参数。\n"
        "仅对无法自动检测 HTTPS 过滤的浏览器启用。",
    "Master switch for all tracking protection features below.":
        "以下所有跟踪保护功能的主开关。",
    "Cookies":                          "Cookie",
    "Block third-party cookies":        "阻止第三方 Cookie",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "在设定的时间后删除第三方 Cookie。\n防止跨站点跟踪。",
    "Lifetime (minutes):":              "生命周期（分钟）：",
    "0 = block immediately. Default: 180 minutes.":
        "0 = 立即阻止。默认：180 分钟。",
    "Block first-party cookies":        "阻止第一方 Cookie",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "在设定的时间后删除所有 Cookie（包括第一方）。\n"
        "警告：这将使你从所有网站退出登录。",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = 立即阻止。默认：4320 分钟（3 天）。",
    "Privacy":                          "隐私",
    "Hide / reduce User-Agent":         "隐藏 / 减少 User-Agent",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "从 User-Agent 中移除标识位。\n"
        "减少指纹识别。",
    "Hide search queries in referrer":  "在引用页中隐藏搜索查询",
    "Hides your search terms when clicking from a search engine to a website.":
        "从搜索引擎点击到网站时隐藏你的搜索词。",
    "Remove referrer from third-party requests":
        "从第三方请求中移除引用页",
    "Prevents third-party sites from knowing which page you came from.":
        "防止第三方网站知道你来自哪个页面。",
    "Send Do-Not-Track signal":         "发送 Do-Not-Track 信号",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "发送带有请求的 DNT 标头。\n注意：大多数网站会忽略此信号，但有些会尊重它。",
    "Disable third-party ETag cache":   "禁用第三方 ETag 缓存",
    "Prevents tracking via ETag caching in third-party content.":
        "防止通过第三方内容中的 ETag 缓存进行跟踪。",
    "Block third-party Authorization header":
        "阻止第三方 Authorization 标头",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "阻止第三方请求中的 Authorization 标头以防止跟踪。",
    "Remove X-Client-Data header":      "移除 X-Client-Data 标头",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "移除 Chrome 发送到 Google 服务的 X-Client-Data 标头。",
    "Block WebRTC":                     "阻止 WebRTC",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "防止通过 WebRTC 泄露 IP。\n可能会破坏视频通话和一些 Web 应用。",
    "Block Push API":                   "阻止 Push API",
    "Blocks browser push notifications from websites.":
        "阻止来自网站的浏览器推送通知。",
    "Block Location API":               "阻止位置 API",
    "Prevents websites from accessing your GPS location.":
        "防止网站访问你的 GPS 位置。",
    "Block Flash":                      "阻止 Flash",
    "Blocks the Flash plugin.":
        "阻止 Flash 插件。",
    "Block Java":                       "阻止 Java",
    "Disables Java plugins. JavaScript remains enabled.":
        "禁用 Java 插件。JavaScript 保持启用。",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "启用 Anti-DPI",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "更改传出数据包以绕过深度数据包检测。\n在存在互联网审查的国家/地区很有用。",
    "App pattern":
        "应用名称模式",
    "Skip outbound proxy":              "跳过出站代理",
    "Don't route this app's traffic through outbound proxy":
        "不要将此应用的流量通过出站代理路由",
    "Browser list included from {}":    "浏览器列表从 {} 包含",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "浏览器包含列表和通配符 (*) 规则无法移除。",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "警告恶意和钓鱼网站。\n使用 AdGuard 的安全浏览数据库。",
    "Send anonymous statistics":        "发送匿名统计信息",
    "Send anonymous lookups to AdGuard.":
        "向 AdGuard 发送匿名查询。",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "使用 Mozilla 的 CRLite 进行证书吊销检查。\n比传统的 CRL/OCSP 检查更快、更可靠。",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "将广告拦截过滤规则应用于 HTTP/HTTPS 请求。",
    "Save failed":                      "保存失败",
    "Could not save proxy.yaml:\n{}":   "无法保存 proxy.yaml：\n{}",
    "Restarting AdGuard…":              "正在重启 AdGuard…",
    "AdGuard restarted.":               "AdGuard 已重启。",
    "Restart failed: {}":               "重启失败：{}",
    "Unknown error":                    "未知错误",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "添加",
    "Search exceptions…":               "搜索例外…",
    "1 exception":                      "1 个例外",
    "{} exceptions":                    "{} 个例外",
    "'{}' is not a valid domain or IP address.":
        "'{}' 不是有效的域名或 IP 地址。",
    "'{}' is already in the list.":     "'{}' 已在列表中。",
    "Could not save exceptions:\n{}":
        "无法保存例外：\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "概览",
    "Userscripts":                      "用户脚本",
    "Exceptions":                       "例外",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "重置许可证",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "生成用于 HTTPS 过滤的根 CA 证书。"
        "证书必须在你的系统上安装并受信任。",
    "Checking for updates…":            "正在检查更新…",
    "Firefox profile:":                 "Firefox 配置文件：",
    "(optional) e.g. abcd1234.MyProfile":
        "（可选）例如 abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "输入过滤器 ID 或名称：",
    "Filter added.":                    "过滤器已添加。",
    "Rename…":                          "重命名…",
    "Rename filter":                    "重命名过滤器",
    "New title:":                       "新标题：",
    "Filter renamed.":                  "过滤器已重命名。",
    "Filter trust updated.":            "过滤器信任已更新。",
    "Filter URL:":                      "过滤器 URL：",
    "Title:":                           "标题：",
    "(optional)":                       "（可选）",
    "Trusted filter":                   "受信任的过滤器",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "搜索 DNS 过滤器…",
    "No DNS filters found.":            "未找到 DNS 过滤器。",
    "DNS filter installed.":            "DNS 过滤器已安装。",
    "DNS filter added.":                "DNS 过滤器已添加。",
    "Remove DNS filter":                "移除 DNS 过滤器",
    "DNS filter {} removed.":           "DNS 过滤器 {} 已移除。",
    "Rename DNS filter":                "重命名 DNS 过滤器",
    "DNS filter renamed.":              "DNS 过滤器已重命名。",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "导出日志…",
    "Export AdGuard CLI logs to a zip file":
        "将 AdGuard CLI 日志导出到 zip 文件",
    "Export settings…":                 "导出设置…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "运行加密和 HTTPS 过滤基准测试。",
    "Run benchmark":                    "运行基准测试",
    "Done.":                            "完成。",
    "Export logs to…":                  "导出日志到…",
    "Export settings to…":              "导出设置到…",
    "Zip files (*.zip);;All files (*)":
        "Zip 文件 (*.zip);;所有文件 (*)",
    "Log file not found.":              "未找到日志文件。",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "无法获取 DNS 过滤器列表",
    "DNS filter {} enabled":            "DNS 过滤器 {} 已启用",
    "Could not enable DNS filter {}":   "无法启用 DNS 过滤器 {}",
    "DNS filter {} disabled":           "DNS 过滤器 {} 已禁用",
    "Could not disable DNS filter {}":  "无法禁用 DNS 过滤器 {}",
    "DNS filter installed":             "DNS 过滤器已安装",
    "DNS filter {} removed":            "DNS 过滤器 {} 已移除",
    "Could not remove DNS filter {}":   "无法移除 DNS 过滤器 {}",
    "DNS filter added":                 "DNS 过滤器已添加",
    "Could not add DNS filter":         "无法添加 DNS 过滤器",
    "DNS filter title updated":         "DNS 过滤器标题已更新",
    "Could not set DNS filter title":   "无法设置 DNS 过滤器标题",
    "Filter added":                     "过滤器已添加",
    "Could not add filter":             "无法添加过滤器",
    "Filter trust updated":             "过滤器信任已更新",
    "Could not update filter trust":    "无法更新过滤器信任",
    "Filter title updated":             "过滤器标题已更新",
    "Could not set filter title":       "无法设置过滤器标题",
    "License reset":                    "许可证已重置",
    "Could not reset license":          "无法重置许可证",
    "Could not retrieve license info":  "无法获取许可证信息",
    "Certificate generated":            "证书已生成",
    "Certificate generation failed":    "证书生成失败",
    "Logs exported":                    "日志已导出",
    "Log export failed":                "日志导出失败",
    "Settings exported":                "设置已导出",
    "Settings export failed":           "设置导出失败",
    "Settings imported":                "设置已导入",
    "Settings import failed":           "设置导入失败",
    "Update check completed":           "更新检查完成",
    "Update check failed":              "更新检查失败",
    "Benchmark failed":                 "基准测试失败",
    "AdGuard stopped (forced)":         "AdGuard 已停止（强制）",
    "Could not stop AdGuard – process may still be running":
        "无法停止 AdGuard – 进程可能仍在运行",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "在此系统上未找到 adguard-cli。\n\n"
        "推荐的安装方法（官方）：\n"
        "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
        "替代方法（Arch Linux AUR）：\n"
        "  paru -S adguard-cli-bin\n\n"
        "托盘会加载，但在安装 adguard-cli 之前，启动/停止将不起作用。",
    "Copy install command":             "复制安装命令",
    "Continue":                         "继续",
    "AdGuard Tray is already running":  "AdGuard Tray 已在运行",
    "Only one instance can run at a time. Check your system tray.":
        "一次只能运行一个实例。请检查你的系统托盘。",
    "Authentication cancelled":         "身份验证已取消",
    "Authorization failed":             "授权失败",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "检查网站证书是否已被吊销（OCSP）。\nAdGuard 采用异步检查，检查缓慢时会放行连接，\n因此很少导致网站打不开 — 除非已确定问题出在这里，否则请保持开启。",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "强制执行证书透明度检查（Chrome 的 CT 策略）。\n自身证书不符合 CT 要求的网站将不再被过滤，浏览器可能拒绝访问。\n大型网站均符合要求，仅在网站报告证书错误时才尝试关闭。",
    "Sites that don't load":
        "无法加载的网站",
    "Turn off HTTP/3 filtering":
        "关闭 HTTP/3 过滤",
    "No filters installed":
        "未安装过滤器",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "防火墙规则阻止了 HTTP/3；浏览器将使用 HTTP/2。",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "已排除过滤的应用（其 HTTP/3 流量同样不被过滤）：{}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuard 未运行 — 不会过滤任何内容。",
    "could not remove the previous certificate":
        "无法移除先前的证书",
    "HTTP/3 state unknown":
        "HTTP/3 状态未知",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "防火墙规则拒绝出站 UDP 443，因此无法使用 QUIC。",
    "Browser policy disables QUIC: {}":
        "浏览器策略已禁用 QUIC：{}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "浏览器可通过 HTTP/3（UDP 443）绕过 AdGuard。",
    "Checking…":
        "正在检查…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "无法读取 proxy.yaml — HTTP/3 状态未知。",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "已关闭 HTTP/3 的 Firefox 系列配置文件：{} / {}",
    "HTTP/3 (QUIC)":
        "HTTP/3（QUIC）",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "AdGuard 阻止 HTTP/3；浏览器回退到受过滤的 HTTP/2。",
    "HTTP/3 is filtered by AdGuard.":
        "HTTP/3 由 AdGuard 过滤。",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "已在 Firefox 配置文件中关闭 HTTP/3 — 请重启浏览器。",
    "HTTPS filtering is off – nothing is filtered.":
        "HTTPS 过滤已关闭 — 不会过滤任何内容。",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "代理模式：{} — 只有经过代理的流量会被过滤，而浏览器不会通过代理发送 QUIC。",
    "unknown":
        "未知",
    "AdGuard's certificate was not found. Generate it first.":
        "未找到 AdGuard 证书。请先生成。",
    "Certificate could not be installed in any browser.":
        "无法在任何浏览器中安装证书。",
    "Certificate installed for {} of {} stores.":
        "已在 {} / {} 个证书库中安装证书。",
    "Chromium-based browsers":
        "基于 Chromium 的浏览器",
    "No browser certificate stores found.":
        "未找到浏览器证书库。",
    "Restart your browsers for the certificate to take effect.":
        "请重启浏览器以使证书生效。",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "请勿使用 sudo/pkexec 运行 — 证书会安装到你自己的浏览器配置文件中",
    "certificate not found after import":
        "导入后未找到证书",
    "certutil not found – install the 'nss' package":
        "未找到 certutil — 请安装 “nss” 软件包",
    "not found":
        "不存在",
    "Could not read the filter list (unexpected CLI output).":
        "无法读取过滤器列表（CLI 输出异常）。",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "未找到系统托盘。AdGuard Tray 正在无图标运行 — 请在面板中启用托盘/AppIndicator。",
    "URL must start with http:// or https://":
        "URL 必须以 http:// 或 https:// 开头",
    "adguard-cli path does not exist or is not executable.":
        "adguard-cli 路径不存在或不可执行。",
    "That binary does not identify as adguard-cli. Save anyway?":
        "该二进制文件未标识为 adguard-cli。仍然保存吗？",
    "Update channel":                   "更新通道",
    "Switching update channel to {}…":  "正在将更新通道切换到 {}…",
    "Update channel set to {}":         "更新通道已设置为 {}",
    "Could not set update channel":     "无法设置更新通道",
    "Invalid channel: {}":              "无效通道：{}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        '尚无访问日志（{}）。AdGuard 过滤流量后才会写入；若以系统服务运行，日志属于 root，此处无法读取。',
    'Cannot read the access log ({}): {}':
        '无法读取访问日志（{}）：{}',
    'Blocked':
        '已拦截',
    'Blocked only':
        '仅已拦截',
    'Refresh':
        '刷新',
    'Allow selected domain':
        '允许所选域名',
    'Block selected domain':
        '拦截所选域名',
    'Activity':
        '活动',
    'Time':
        '时间',
    'Domain':
        '域名',
    'Result':
        '结果',
    'Rule':
        '规则',
    'Size':
        '大小',
    'Count':
        '次数',
    'Could not read the access log.':
        '无法读取访问日志。',
    '{} lines not understood':
        '{} 行无法解析',
    'Not a valid domain: {}':
        '不是有效域名：{}',
    'Source: {}':
        '来源：{}',
    'Allowed':
        '已放行',
    'Added rule: {}':
        '已添加规则：{}',
    'Requests per hour, {} to {} · busiest hour: {}':
        '每小时请求数，{} 至 {} · 最繁忙时段：{}',
    'Last 24 hours':
        '最近 24 小时',
    'Last 7 days':
        '最近 7 天',
    'Requests':
        '请求',
    'Traffic':
        '流量',

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        '有新版本 {}（当前 {}）。',
    'Application update':
        '应用更新',
    'Check for update':
        '检查更新',
    'Install update':
        '安装更新',
    'Installing update…':
        '正在安装更新…',
    'Restart now':
        '立即重启',
    'Later':
        '稍后',
    'You are running the latest version ({}).':
        '已是最新版本（{}）。',
    'Installation not recognised':
        '无法识别安装方式',
    'Could not check for updates.':
        '无法检查更新。',
    'Update with: {}':
        '更新命令：{}',
    'Installed with the AUR package {}':
        '通过 AUR 软件包 {} 安装',
    'Installed in {}':
        '安装在 {}',
    'Running from a source checkout':
        '正在从源码目录运行',
    'Version {} installed. Restart adguard-tray to use it.':
        '已安装版本 {}。重启 adguard-tray 后生效。',
    'Unexpected answer from GitHub: {}':
        'GitHub 返回了意外的响应：{}',
    'Download failed: {}':
        '下载失败：{}',
    'Could not unpack the download: {}':
        '无法解压下载内容：{}',
    'This installation is managed elsewhere: {}':
        '此安装由其他方式管理：{}',
    'No permission to write to {}':
        '没有写入 {} 的权限',
    'GitHub returned {}.':
        'GitHub 返回 {}。',
    'No connection to GitHub: {}':
        '无法连接 GitHub：{}',
    'The download does not contain adguard-tray.':
        '下载内容不包含 adguard-tray。',
    'The download says version {} instead of {} – aborted.':
        '下载内容的版本是 {}，而非 {} — 已中止。',
    'GitHub is rate limiting this address. Try again later.':
        'GitHub 正在限制此地址的请求，请稍后重试。',
    'The download is larger than expected – aborted.':
        '下载内容超出预期大小 — 已中止。',
    'Update failed: {}':
        '更新失败：{}',
    'The archive contains unexpected paths – aborted.':
        '压缩包中包含异常路径 — 已中止。',
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        '更新失败，且未能恢复旧版本。请从 {} 恢复，或重新安装：{}',
    'Last 30 days':
        '最近 30 天',
    'All time':
        '全部时间',
    'Modified':
        '已修改',
    'Rules':
        '规则',
    'Showing {} – show all':
        '仅显示 {} — 显示全部',
    'history {}':
        '历史 {}',
    'Filter list ID: {}':
        '过滤列表 ID：{}',
    'App':
        '应用',
    'Protocol':
        '协议',
    'Type':
        '类型',
    'Reset history':
        '重置历史',
    'Delete the stored history and read the log again.':
        '删除已保存的历史并重新读取日志。',
    'Delete the stored history? Only what the log still holds can be read back.':
        '要删除已保存的历史吗？只有日志中仍存在的记录能被重新读取。',
    'History is not being updated: {}':
        '历史未在更新：{}',

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "AdGuard 设置有 1 项未保存的更改",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "受信任的过滤器可以在你访问的网页中运行脚本。只信任来自你了解的来源的列表。",
    "About":
        "关于",
    "Actions for the selected filter":
        "所选过滤器的操作",
    "Ad blocking":
        "广告拦截",
    "Ad blocking is off, so the filter lists below have no effect.":
        "广告拦截已关闭，下面的过滤器列表不会生效。",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLI 将下载并安装其最新版本。",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "AdGuard CLI 会在此计算机上移除许可证，之后需要重新激活。",
    "AdGuard CLI logs":
        "AdGuard CLI 日志",
    "AdGuard CLI update finished.":
        "AdGuard CLI 更新完成。",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "AdGuard Tray 日志",
    "AdGuard doesn't filter these websites.":
        "AdGuard 不过滤这些网站。",
    "AdGuard is filtering this computer's traffic.":
        "AdGuard 正在过滤此计算机的流量。",
    "AdGuard restarts to load the new lists.":
        "AdGuard 将重新启动以加载新列表。",
    "AdGuard's reply did not say whether it is running.":
        "无法从 AdGuard 的响应判断其是否正在运行。",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "未找到 AdGuard 的设置文件（{}）。请先运行一次 adguard-cli 以创建它。",
    "Add DNS filter by ID":
        "按 ID 添加 DNS 过滤器",
    "Add DNS filter from URL":
        "从 URL 添加 DNS 过滤器",
    "Add filter":
        "添加过滤器",
    "Add filter by ID":
        "按 ID 添加过滤器",
    "Add filter from URL":
        "从 URL 添加过滤器",
    "Add rule":
        "添加规则",
    "Add to browsers":
        "添加到浏览器",
    "Add userscript":
        "添加用户脚本",
    "Add userscript…":
        "添加用户脚本…",
    "Add website":
        "添加网站",
    "Add…":
        "添加…",
    "Advanced":
        "高级",
    "All available":
        "全部可用",
    "Allow {}":
        "允许 {}",
    "Also adds the certificate to this Firefox profile.":
        "同时将证书添加到此 Firefox 配置文件。",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "重启和出错时也会通知。需要 notify-send（libnotify）或正在运行的通知服务，例如 dunst、mako 或 KDE 自带的服务。",
    "Appearance":
        "外观",
    "Applies after AdGuard Tray restarts.":
        "重启 AdGuard Tray 后生效。",
    "Apply":
        "应用",
    "Apply your changes to AdGuard's settings before closing?":
        "关闭前要应用对 AdGuard 设置的更改吗？",
    "Applying them restarts AdGuard if protection is on.":
        "应用后，如果保护已开启，AdGuard 将重新启动。",
    "Asks GitHub for the newest release.":
        "向 GitHub 查询最新版本。",
    "At a glance":
        "概况",
    "Automatic":
        "自动",
    "Automatic – filter all apps":
        "自动 — 过滤所有应用",
    "Benchmark":
        "基准测试",
    "Beta":
        "测试版",
    "Block ECH in DNS records":
        "在 DNS 记录中阻止 ECH",
    "Block domains before a connection is made.":
        "在建立连接之前拦截域名。",
    "Block {}":
        "拦截 {}",
    "Blocked (24 h)":
        "已拦截（24 小时）",
    "Browser list ({})":
        "浏览器列表（{}）",
    "By ID or name…":
        "按 ID 或名称添加…",
    "Certificate":
        "证书",
    "Certificate checks":
        "证书检查",
    "Changes are collected in the bar at the bottom and applied together.":
        "更改会汇总在底部栏中，并一起应用。",
    "Check again":
        "重新检查",
    "Check every":
        "检查间隔",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "基于 Chromium 和 Firefox 的浏览器使用自己的证书库。",
    "Close":
        "关闭",
    "Controls which AdGuard CLI build “{}” installs.":
        "决定“{}”安装哪个 AdGuard CLI 版本。",
    "Could not add the rule.":
        "无法添加规则。",
    "Could not open {}":
        "无法打开 {}",
    "Could not read {}":
        "无法读取 {}",
    "Could not refresh. Showing data from {}.":
        "刷新失败。当前显示 {} 的数据。",
    "Could not reset the history.":
        "无法重置历史。",
    "Could not restart AdGuard.":
        "无法重启 AdGuard。",
    "Could not start protection.":
        "无法启动保护。",
    "Could not stop protection.":
        "无法停止保护。",
    "Create":
        "创建",
    "Create certificate":
        "创建证书",
    "Custom":
        "自定义",
    "DNS filter lists":
        "DNS 过滤器列表",
    "DNS filtering":
        "DNS 过滤",
    "DNS filtering is off, so these lists have no effect.":
        "DNS 过滤已关闭，这些列表不会生效。",
    "DNS servers":
        "DNS 服务器",
    "Dark":
        "深色",
    "Default":
        "默认",
    "Details":
        "详情",
    "Discard":
        "放弃",
    "Don't filter":
        "不过滤",
    "Don't trust":
        "不信任",
    "Downloads and installs the newest AdGuard CLI build.":
        "下载并安装最新的 AdGuard CLI 版本。",
    "Duration":
        "耗时",
    "Export…":
        "导出…",
    "Filter everything":
        "全部过滤",
    "Filter in place":
        "就地过滤",
    "Filtering":
        "过滤",
    "Follow system":
        "跟随系统",
    "From URL…":
        "从 URL 添加…",
    "Go to updates":
        "前往更新",
    "HTTP proxy: {}":
        "HTTP 代理：{}",
    "HTTPS filtering":
        "HTTPS 过滤",
    "How much detail AdGuard Tray writes to its own log.":
        "AdGuard Tray 写入自身日志的详细程度。",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "如果网站无法加载，请先关闭 HTTP/3 过滤。其他检查保护所有网站 — 仅在这样仍无效时才关闭它们。",
    "Included":
        "已包含",
    "Installed":
        "已安装",
    "License":
        "许可证",
    "Light":
        "浅色",
    "Logs":
        "日志",
    "MIT license":
        "MIT 许可证",
    "Maintenance":
        "维护",
    "Manual proxy":
        "手动代理",
    "Manual – only apps set to use the proxy":
        "手动 — 仅限设置为使用代理的应用",
    "More":
        "更多",
    "Move down":
        "下移",
    "Move up":
        "上移",
    "Network":
        "网络",
    "Nightly":
        "每夜版",
    "No requests yet – AdGuard logs requests while protection is on.":
        "暂无请求 — 保护开启时 AdGuard 会记录请求。",
    "Not added":
        "未添加",
    "Nothing matches your search.":
        "没有匹配的结果。",
    "Notify me when protection turns on or off":
        "保护开启或关闭时通知我",
    "Off":
        "关闭",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "仅影响使用 DoH 或 DoT 的浏览器。选择“关闭”会让它们绕过 AdGuard 的 DNS 过滤。",
    "Open AdGuard Tray":
        "打开 AdGuard Tray",
    "Open exceptions":
        "打开例外",
    "Open folder":
        "打开文件夹",
    "Open release page":
        "打开发布页面",
    "Pages":
        "页面",
    "Performance":
        "性能",
    "Protection":
        "保护",
    "Protection started.":
        "保护已启动。",
    "Protection stopped.":
        "保护已停止。",
    "Proxy mode":
        "代理模式",
    "Redirect to AdGuard's DNS":
        "重定向到 AdGuard 的 DNS",
    "Refresh this page (F5)":
        "刷新此页面 (F5)",
    "Release (stable)":
        "正式版（稳定）",
    "Remove rule":
        "移除规则",
    "Remove “{}”?":
        "移除 “{}”？",
    "Remove…":
        "移除…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "用 {} 中的设置替换当前的 AdGuard 设置？\n\nAdGuard 将重启以应用这些设置。",
    "Reset history…":
        "重置历史…",
    "Reset…":
        "重置…",
    "Restart AdGuard":
        "重启 AdGuard",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "规则仅在自动代理模式下生效。第一条匹配的规则生效，因此请将 \"*\" 放在最后。",
    "Safe Browsing":
        "安全浏览",
    "Save anyway":
        "仍然保存",
    "Saved. AdGuard restarts to apply the change.":
        "已保存。AdGuard 将重新启动以应用更改。",
    "Saved. Applies after AdGuard Tray restarts.":
        "已保存。重启 AdGuard Tray 后生效。",
    "Saved. The change applies when protection is turned on.":
        "已保存。更改将在开启保护后生效。",
    "Secure DNS and ECH":
        "安全 DNS 与 ECH",
    "Secure DNS filtering":
        "安全 DNS 过滤",
    "Set the path in Settings":
        "在设置中指定路径",
    "Settings":
        "设置",
    "Show":
        "显示",
    "Show recent entries":
        "显示最近的条目",
    "Skip HTTPS filtering":
        "跳过 HTTPS 过滤",
    "Some counts could not be loaded.":
        "部分统计数据无法加载。",
    "Source code":
        "源代码",
    "Start AdGuard Tray when I log in":
        "登录时启动 AdGuard Tray",
    "Startup":
        "启动",
    "Status checks":
        "状态检查",
    "Stealth mode":
        "隐身模式",
    "System":
        "系统",
    "The new lists load when protection is turned on.":
        "开启防护后将加载新列表。",
    "Theme":
        "主题",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "这将关闭 HTTP/3 过滤、OCSP 检查、证书透明度和安全 DNS 过滤。被吊销或错误签发的证书将不再被发现，浏览器也可绕过 AdGuard 的 DNS 过滤进行解析。",
    "Time range":
        "时间范围",
    "To keep it but stop using it, switch it off instead.":
        "如果想保留但不再使用，请改为将其关闭。",
    "Top lists":
        "排行榜",
    "Trust":
        "信任",
    "Trust “{}”?":
        "信任 “{}”？",
    "Trust…":
        "信任…",
    "Turn off all strict checks…":
        "关闭所有严格检查…",
    "Undo":
        "撤销",
    "Unknown":
        "未知",
    "Unsaved changes":
        "未保存的更改",
    "Update AdGuard CLI…":
        "更新 AdGuard CLI…",
    "Update channel: {}":
        "更新通道：{}",
    "Updated {}":
        "更新于 {}",
    "Updates":
        "更新",
    "Used in manual mode only.":
        "仅在手动模式下使用。",
    "Userscripts update together with filters.":
        "用户脚本会随过滤器一起更新。",
    "Uses XDG autostart (~/.config/autostart).":
        "使用 XDG 自动启动（~/.config/autostart）。",
    "Waiting for authorization…":
        "正在等待授权…",
    "Website exceptions":
        "网站例外",
    "Websites":
        "网站",
    "example.com or a link":
        "example.com 或链接",
    "expires {}":
        "到期日 {}",
    "of {} requests in the last 24 hours":
        "共 {} 个请求（最近 24 小时）",
    "{} of {} DNS filters on":
        "{} / {} 个 DNS 过滤器已开启",
    "{} of {} filters on":
        "{} / {} 个过滤器已开启",
    "{} of {} on":
        "已开启 {}/{}",
    "{} unsaved changes to AdGuard's settings":
        "AdGuard 设置有 {} 项未保存的更改",
    "“Follow system” uses your desktop's light or dark setting.":
        "“跟随系统”会使用桌面的浅色或深色设置。",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "有效",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "AdGuard 证书将被添加到本机找到的每个浏览器配置文件。\n\n这将允许 AdGuard 检查这些浏览器的 HTTPS 流量。请先关闭浏览器 — 它们在启动时读取证书库。",
    "Allow":
        "允许",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "请先应用或放弃对 AdGuard 设置的更改，然后再重启。",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "自动：AdGuard 通过 iptables 将所有应用的流量重定向到自身。手动：AdGuard 仅监听下方的 SOCKS5 和 HTTP 端口。",
    "Block":
        "拦截",
    "Browser API blocking":
        "浏览器 API 阻止",
    "CRLite":
        "CRLite",
    "Cancel":
        "取消",
    "Computers":
        "计算机",
    "Could not change the autostart entry.":
        "无法更改自动启动项。",
    "Could not export the logs.":
        "无法导出日志。",
    "Could not export the settings.":
        "无法导出设置。",
    "Could not reset the license.":
        "无法重置许可证。",
    "Could not retrieve license info.":
        "无法获取许可证信息。",
    "Could not run the benchmark.":
        "无法运行基准测试。",
    "Could not save the settings.":
        "无法保存设置。",
    "Could not set the update channel.":
        "无法设置更新通道。",
    "Could not update AdGuard CLI.":
        "无法更新 AdGuard CLI。",
    "Could not update the filters.":
        "无法更新过滤器。",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "DNS 上游服务器。\n'default' = 系统 DNS。\n示例：1.1.1.1、https://dns.google/dns-query、\ntls://dns.adguard.com、quic://dns.adguard.com",
    "Expiration date":
        "到期日期",
    "Expires":
        "到期",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "已在 Firefox 配置文件中重新开启 HTTP/3 — 请重启浏览器。",
    "License key":
        "许可证密钥",
    "License type":
        "许可证类型",
    "Manual":
        "手动",
    "No exceptions.":
        "没有例外。",
    "OK":
        "确定",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "开启：AdGuard 自行过滤 HTTP/3（QUIC）— 属实验功能，且部分浏览器\n本就拒绝通过用户安装的证书使用 HTTP/3。\n关闭：AdGuard 转为阻止 QUIC，浏览器回退到 HTTP/2，可被可靠过滤。\n两者都仅在自动模式下生效 — 在手动模式下，\nHTTP/3 流量根本不会到达 AdGuard。",
    "Owner":
        "所有者",
    "Personal":
        "个人版",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "代理模式：{} — UDP 443 端口被重定向到 AdGuard。",
    "Save adguard-cli path":
        "保存 adguard-cli 路径",
    "Search domains or rules…":
        "搜索域名或规则…",
    "Settings file":
        "设置文件",
    "Status":
        "状态",
    "Trial":
        "试用版",
    "Turn HTTP/3 back on in Firefox profiles":
        "在 Firefox 配置文件中重新开启 HTTP/3",
    "Turn off":
        "关闭",
    "Turn off HTTP/3 in Firefox profiles":
        "在 Firefox 配置文件中关闭 HTTP/3",
    "Turn off HTTP/3 in Firefox profiles…":
        "在 Firefox 配置文件中关闭 HTTP/3…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "在 {} 个 Firefox 系列配置文件中关闭 HTTP/3？\n\n其流量将改用 HTTP/2，AdGuard 可以过滤。之后请重启浏览器。",
    "Turn off all strict checks":
        "关闭所有严格检查",
    "Unavailable until AdGuard CLI reports its current channel.":
        "在 AdGuard CLI 报告当前通道之前不可用。",
    "Update AdGuard CLI":
        "更新 AdGuard CLI",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "仅在自动模式下使用。可填写范围（80:5221,5300:49151）或单个端口（80,443,8080）。",
    "{} of {}":
        "{}/{}",
    "{} of {} userscripts on":
        "{} / {} 个用户脚本已开启",
    "{}% blocked":
        "已拦截 {}%",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "烦扰内容",
    "General":
        "常规",
    "Language-specific":
        "特定语言",
    "Security":
        "安全",
    "Social widgets":
        "社交小组件",
    "Expired":
        "已过期",
    "Autostart on login":
        "登录时自动启动",
    "Add app rule":
        "添加应用程序规则",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "支持通配符，例如 *steam* 或 *EasyAntiCheat*。",
    "There is already a rule for '{}'.":
        "已存在“{}”的规则。",
    "AdGuard settings":
        "AdGuard 设置",
    "Ads and trackers are not blocked until you enable protection.":
        "启用保护后才会拦截广告和跟踪器。",
    "Could not import the settings.":
        "无法导入设置。",
    "Disable protection":
        "禁用保护",
    "Enable protection":
        "启用保护",
    "Export and import":
        "导出和导入",
    "Features":
        "功能",
    "Import settings":
        "导入设置",
    "Import settings from…":
        "从…导入设置",
    "Import settings…":
        "导入设置…",
    "Import…":
        "导入…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "将过滤器、规则和配置保存到 zip 文件，或从 zip 文件加载。",
    "Update":
        "更新",
    "Version":
        "版本",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "{} 不是设置导出文件。请选择在“AdGuard 设置”中通过“导出”保存的文件。",
}
