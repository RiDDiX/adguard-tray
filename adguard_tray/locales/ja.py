"""Japanese."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "言語",
    "English":                           "英語",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "有効 – 保護が動作中",
    "Inactive – Protection stopped":        "無効 – 保護は停止中",
    "Error retrieving status":              "状態の取得エラー",
    "adguard-cli not found":                "adguard-cliが見つかりません",
    "Unknown status":                       "不明な状態",
    "Checking status…":                     "状態を確認中…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "再起動",
    "Filters":                              "フィルタ",
    "Loading…":                             "読み込み中…",
    "Manage filters…":                      "フィルタの管理…",
    "No userscripts installed":             "インストールされているユーザースクリプトはありません",
    "Manage userscripts…":                  "ユーザースクリプトの管理…",
    "Quit":                                 "終了",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "有効",
    "inactive":                             "無効",
    "System-wide filtering: {}":            "システム全体のフィルタリング：{}",
    "Error: {}":                            "エラー：{}",
    "AdGuard Tray – Error":                 "AdGuard Tray – エラー",
    "AdGuard is now active – protection running.":
        "AdGuardが有効になりました。保護が動作中です。",
    "AdGuard has been stopped.":
        "AdGuardが停止しました。",
    "Could not retrieve status.":
        "状態を取得できませんでした。",
    "Command failed":                       "コマンドの実行に失敗しました",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " 秒",
    "How often adguard-cli status is checked automatically.":
        "adguard-cliの状態を自動で確認する間隔です。",
    "Log level:":                           "ログレベル：",
    "adguard-cli path:":                    "adguard-cliのパス：",
    "auto-detect via PATH":                 "PATHから自動検出",
    "Browse…":                              "参照…",
    "Select adguard-cli binary":            "adguard-cliのバイナリを選択",
    "Notifications":                        "通知",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "フィルタを更新",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "すべてのフィルタ、DNSフィルタ、ユーザースクリプト、\nSafebrowsingV2、CRLiteを更新し、アプリのアップデートを確認します。",
    "No filters found.":                    "フィルタが見つかりません。",
    "Updating filters… (can take up to 2 minutes)":
        "フィルタを更新中…（最大2分かかる場合があります）",
    "Update completed.":                    "更新が完了しました。",
    "Update failed.":                       "更新に失敗しました。",
    "Installing: {}":                       "インストール中：{}",
    "Filter installed.":                    "フィルタをインストールしました。",
    "Remove":                               "削除",
    "Remove filter":                        "フィルタを削除",
    "Filter {} removed.":                   "フィルタ「{}」を削除しました。",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        ".jsファイルへの直接URLからユーザースクリプトをインストール",
    "No userscripts installed.":            "インストールされているユーザースクリプトはありません。",
    "Userscript URL (direct .js URL):":     "ユーザースクリプトのURL（.jsファイルへの直接URL）：",
    "Userscript installed.":                "ユーザースクリプトをインストールしました。",
    'Remove "{}"':                          "「{}」を削除",
    "Remove userscript":                    "ユーザースクリプトを削除",
    "'{}' removed.":                        "「{}」を削除しました。",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "adguard-cliが見つかりませんでした。\n公式スクリプトまたはAURからインストールしてください：\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "状態の取得中に不明なエラーが発生しました",
    "AdGuard {} ok":                        "AdGuard {}：成功",
    "AdGuard via systemctl {} ok":          "AdGuard（systemctl {}）：成功",
    "'{}' failed – insufficient privileges?":
        "「{}」に失敗しました。権限が不足している可能性があります",
    "Could not retrieve filter list":
        "フィルタリストを取得できませんでした",
    "Filter {} enabled":                    "フィルタ{}を有効にしました",
    "Could not enable filter {}":           "フィルタ{}を有効にできませんでした",
    "Filter {} disabled":                   "フィルタ{}を無効にしました",
    "Could not disable filter {}":
        "フィルタ{}を無効にできませんでした",
    "Filter installed":                     "フィルタをインストールしました",
    "Installation failed":                  "インストールに失敗しました",
    "Filter {} removed":                    "フィルタ{}を削除しました",
    "Could not remove filter {}":
        "フィルタ{}を削除できませんでした",
    "Filters updated":                      "フィルタを更新しました",
    "Update failed":                        "更新に失敗しました",
    "Could not retrieve userscript list":
        "ユーザースクリプトの一覧を取得できませんでした",
    "Userscript '{}' enabled":              "ユーザースクリプト「{}」を有効にしました",
    "Could not enable userscript '{}'":
        "ユーザースクリプト「{}」を有効にできませんでした",
    "Userscript '{}' disabled":             "ユーザースクリプト「{}」を無効にしました",
    "Could not disable userscript '{}'":
        "ユーザースクリプト「{}」を無効にできませんでした",
    "Userscript '{}' removed":              "ユーザースクリプト「{}」を削除しました",
    "Could not remove userscript '{}'":
        "ユーザースクリプト「{}」を削除できませんでした",
    "Userscript installed":                 "ユーザースクリプトをインストールしました",
    "Other":                                "その他",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "フィルタを検索…",
    "Search userscripts…":              "ユーザースクリプトを検索…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "proxy.yamlを読み込めませんでした。\nパス：{}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "アプリ",
    "Mode:":                            "モード：",
    "Filtered ports:":                  "フィルタリング対象ポート：",
    "SOCKS5 port:":                     "SOCKS5ポート：",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "手動モード用のSOCKS5プロキシポートです。\n無効にするには-1に設定してください。",
    "HTTP port:":                       "HTTPポート：",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "手動モード用のHTTPプロキシポートです。\n無効にするには-1に設定してください。",
    "Listen address:":                  "待ち受けアドレス：",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "プロキシが待ち受けるアドレスです。\n127.0.0.1 = ローカルのみ。0.0.0.0 = すべてのインターフェイス（認証が必要）。",
    "Worker threads:":                  "ワーカースレッド数：",
    "Number of proxy worker threads.":  "プロキシのワーカースレッド数です。",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "HTTPSトラフィックを復号してフィルタリングします。\nhttpsサイトの広告をブロックするために必要です。\nシステムに信頼済みのルート証明書がインストールされている必要があります。",
    "Enable TLS 1.3":                   "TLS 1.3を有効化",
    "Enable TLS 1.3 support for filtered connections.":
        "フィルタリング対象の接続でTLS 1.3のサポートを有効にします。",
    "Filter HTTP/3 (QUIC) – experimental":
        "HTTP/3（QUIC）をフィルタリング – 試験的",
    "OCSP certificate checks":          "OCSP証明書チェック",
    "Enforce Certificate Transparency": "Certificate Transparencyを強制",
    "Filter EV certificate sites":      "EV証明書のサイトもフィルタリング",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "デフォルトでは、拡張検証（EV）証明書を使うサイトはフィルタリングされません。\n有効にすると、これらのサイト（銀行のサイトなど）もフィルタリングします。",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello (ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "ECHを有効にしてプライバシーを強化します。\nDNSフィルタリングが有効になっている必要があります。",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "DNSクエリをフィルタリングし、DNSレベルで広告やトラッカーをブロックします。\nアップストリームを設定できるローカルDNSプロキシを使用します。",
    "Upstream:":                        "アップストリーム：",
    "Fallbacks:":                       "フォールバック：",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "フォールバック用のDNSサーバーです（プライマリのアップストリームが失敗した場合に使用）。\n'default' = システムのDNS。スペース区切りのリストです。\n例：default 1.1.1.1",
    "Bootstraps:":                      "ブートストラップ：",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "アップストリームのホスト名を解決するためのブートストラップDNSです。\n'default' = システムのDNSのIP。IPアドレスのみ指定できます。\n例：default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "SVCB/HTTPSのDNSレコードからECHパラメーターを削除します。\nHTTPSフィルタリングを自動検出しないブラウザを使う場合にのみ有効にしてください。",
    "Master switch for all tracking protection features below.":
        "以下のすべてのトラッキング防止機能をまとめてオン/オフします。",
    "Cookies":                          "クッキー",
    "Block third-party cookies":        "サードパーティクッキーをブロック",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "サードパーティクッキーを一定時間後に削除します。\nクロスサイトトラッキングを防ぎます。",
    "Lifetime (minutes):":              "ライフタイム（分）：",
    "0 = block immediately. Default: 180 minutes.":
        "0 = 即時ブロック。デフォルト：180分。",
    "Block first-party cookies":        "ファーストパーティクッキーをブロック",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "すべてのクッキー（ファーストパーティを含む）を一定時間後に削除します。\n警告：すべてのサイトからログアウトされます。",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = 即時ブロック。デフォルト：4320分（3日）。",
    "Privacy":                          "プライバシー",
    "Hide / reduce User-Agent":         "User-Agentを非表示・簡略化",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "User-Agentから個人の識別につながる情報を取り除きます。\nフィンガープリンティングを抑制します。",
    "Hide search queries in referrer":  "リファラー内の検索クエリを非表示",
    "Hides your search terms when clicking from a search engine to a website.":
        "検索エンジンからサイトに移動する際に、検索キーワードを非表示にします。",
    "Remove referrer from third-party requests":
        "サードパーティリクエストのリファラーを削除",
    "Prevents third-party sites from knowing which page you came from.":
        "どのページから移動してきたかをサードパーティのサイトに知られないようにします。",
    "Send Do-Not-Track signal":         "トラッキング拒否（DNT）シグナルを送信",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "リクエストにDNTヘッダーを付けて送信します。\n注意：多くのサイトは無視しますが、尊重するサイトもあります。",
    "Disable third-party ETag cache":   "サードパーティのETagキャッシュを無効化",
    "Prevents tracking via ETag caching in third-party content.":
        "サードパーティコンテンツのETagキャッシュを利用したトラッキングを防ぎます。",
    "Block third-party Authorization header":
        "サードパーティのAuthorizationヘッダーをブロック",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "トラッキングを防ぐため、サードパーティリクエストのAuthorizationヘッダーをブロックします。",
    "Remove X-Client-Data header":      "X-Client-Dataヘッダーを削除",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "ChromeがGoogleのサービスに送信するX-Client-Dataヘッダーを削除します。",
    "Block WebRTC":                     "WebRTCをブロック",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "WebRTC経由のIPアドレス漏えいを防ぎます。\nビデオ通話や一部のウェブアプリが動作しなくなる場合があります。",
    "Block Push API":                   "プッシュAPIをブロック",
    "Blocks browser push notifications from websites.":
        "ウェブサイトからのブラウザのプッシュ通知をブロックします。",
    "Block Location API":               "位置情報APIをブロック",
    "Prevents websites from accessing your GPS location.":
        "ウェブサイトがGPSの位置情報にアクセスするのを防ぎます。",
    "Block Flash":                      "Flashをブロック",
    "Blocks the Flash plugin.":
        "Flashプラグインをブロックします。",
    "Block Java":                       "Javaをブロック",
    "Disables Java plugins. JavaScript remains enabled.":
        "Javaプラグインを無効にします。JavaScriptは有効のままです。",
    "Anti-DPI":                         "DPI対策",
    "Enable Anti-DPI":                  "DPI対策を有効化",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "送信パケットのデータを変更して、ディープパケットインスペクション（DPI）を回避します。\nインターネット検閲がある国で役立ちます。",
    "App pattern":
        "アプリのパターン",
    "Skip outbound proxy":              "送信プロキシを経由しない",
    "Don't route this app's traffic through outbound proxy":
        "このアプリのトラフィックを送信プロキシ経由にしない",
    "Browser list included from {}":    "ブラウザリストの読み込み元：{}",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "組み込みのブラウザリストとワイルドカード（*）ルールは削除できません。",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "悪意のあるウェブサイトやフィッシングサイトについて警告します。\nAdGuardのセーフブラウジングデータベースを使用します。",
    "Send anonymous statistics":        "匿名の統計情報を送信",
    "Send anonymous lookups to AdGuard.":
        "照会内容を匿名でAdGuardに送信します。",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "MozillaのCRLiteを使って証明書の失効を確認します。\n従来のCRL/OCSPチェックより高速で、信頼性も高い方式です。",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "HTTP/HTTPSリクエストに広告ブロックのフィルタリングルールを適用します。",
    "Save failed":                      "保存に失敗しました",
    "Could not save proxy.yaml:\n{}":   "proxy.yamlを保存できませんでした：\n{}",
    "Restarting AdGuard…":              "AdGuardを再起動中…",
    "AdGuard restarted.":               "AdGuardを再起動しました。",
    "Restart failed: {}":               "再起動に失敗しました：{}",
    "Unknown error":                    "不明なエラー",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "追加",
    "Search exceptions…":               "例外を検索…",
    "1 exception":                      "例外：1件",
    "{} exceptions":                    "例外：{}件",
    "'{}' is not a valid domain or IP address.":
        "「{}」は有効なドメインまたはIPアドレスではありません。",
    "'{}' is already in the list.":     "「{}」はすでにリストにあります。",
    "Could not save exceptions:\n{}":
        "例外を保存できませんでした：\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "概要",
    "Userscripts":                      "ユーザースクリプト",
    "Exceptions":                       "例外",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "ライセンスをリセット",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "HTTPSフィルタリング用のルートCA証明書を生成します。証明書はシステムにインストールし、信頼済みにする必要があります。",
    "Checking for updates…":            "アップデートを確認中…",
    "Firefox profile:":                 "Firefoxプロファイル：",
    "(optional) e.g. abcd1234.MyProfile":
        "（任意）例：abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "フィルタのIDまたは名前を入力してください：",
    "Filter added.":                    "フィルタを追加しました。",
    "Rename…":                          "名前を変更…",
    "Rename filter":                    "フィルタの名前を変更",
    "New title:":                       "新しいタイトル：",
    "Filter renamed.":                  "フィルタの名前を変更しました。",
    "Filter trust updated.":            "フィルタの信頼設定を更新しました。",
    "Filter URL:":                      "フィルタのURL：",
    "Title:":                           "タイトル：",
    "(optional)":                       "（任意）",
    "Trusted filter":                   "信頼済みフィルタ",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "DNSフィルタを検索…",
    "No DNS filters found.":            "DNSフィルタが見つかりません。",
    "DNS filter installed.":            "DNSフィルタをインストールしました。",
    "DNS filter added.":                "DNSフィルタを追加しました。",
    "Remove DNS filter":                "DNSフィルタを削除",
    "DNS filter {} removed.":           "DNSフィルタ「{}」を削除しました。",
    "Rename DNS filter":                "DNSフィルタの名前を変更",
    "DNS filter renamed.":              "DNSフィルタの名前を変更しました。",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "ログをエクスポート…",
    "Export AdGuard CLI logs to a zip file":
        "AdGuard CLIのログをzipファイルにエクスポート",
    "Export settings…":                 "設定をエクスポート…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "暗号処理とHTTPSフィルタリングのベンチマークを実行します。",
    "Run benchmark":                    "ベンチマークを実行",
    "Done.":                            "完了しました。",
    "Export logs to…":                  "ログのエクスポート先…",
    "Export settings to…":              "設定のエクスポート先…",
    "Zip files (*.zip);;All files (*)":
        "Zipファイル (*.zip);;すべてのファイル (*)",
    "Log file not found.":              "ログファイルが見つかりません。",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "DNSフィルタリストを取得できませんでした",
    "DNS filter {} enabled":            "DNSフィルタ{}を有効にしました",
    "Could not enable DNS filter {}":   "DNSフィルタ{}を有効にできませんでした",
    "DNS filter {} disabled":           "DNSフィルタ{}を無効にしました",
    "Could not disable DNS filter {}":  "DNSフィルタ{}を無効にできませんでした",
    "DNS filter installed":             "DNSフィルタをインストールしました",
    "DNS filter {} removed":            "DNSフィルタ{}を削除しました",
    "Could not remove DNS filter {}":   "DNSフィルタ{}を削除できませんでした",
    "DNS filter added":                 "DNSフィルタを追加しました",
    "Could not add DNS filter":         "DNSフィルタを追加できませんでした",
    "DNS filter title updated":         "DNSフィルタのタイトルを更新しました",
    "Could not set DNS filter title":   "DNSフィルタのタイトルを設定できませんでした",
    "Filter added":                     "フィルタを追加しました",
    "Could not add filter":             "フィルタを追加できませんでした",
    "Filter trust updated":             "フィルタの信頼設定を更新しました",
    "Could not update filter trust":    "フィルタの信頼設定を更新できませんでした",
    "Filter title updated":             "フィルタのタイトルを更新しました",
    "Could not set filter title":       "フィルタのタイトルを設定できませんでした",
    "License reset":                    "ライセンスをリセットしました",
    "Could not reset license":          "ライセンスをリセットできませんでした",
    "Could not retrieve license info":  "ライセンス情報を取得できませんでした",
    "Certificate generated":            "証明書を生成しました",
    "Certificate generation failed":    "証明書の生成に失敗しました",
    "Logs exported":                    "ログをエクスポートしました",
    "Log export failed":                "ログのエクスポートに失敗しました",
    "Settings exported":                "設定をエクスポートしました",
    "Settings export failed":           "設定のエクスポートに失敗しました",
    "Settings imported":                "設定をインポートしました",
    "Settings import failed":           "設定のインポートに失敗しました",
    "Update check completed":           "アップデートの確認が完了しました",
    "Update check failed":              "アップデートの確認に失敗しました",
    "Benchmark failed":                 "ベンチマークに失敗しました",
    "AdGuard stopped (forced)":         "AdGuardを強制停止しました",
    "Could not stop AdGuard – process may still be running":
        "AdGuardを停止できませんでした。プロセスがまだ動作している可能性があります",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "このシステムでadguard-cliが見つかりません。\n\n推奨されるインストール方法（公式）：\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n別の方法（Arch Linux AUR）：\n  paru -S adguard-cli-bin\n\nトレイは起動しますが、adguard-cliをインストールするまで開始/停止は機能しません。",
    "Copy install command":             "インストールコマンドをコピー",
    "Continue":                         "続行",
    "AdGuard Tray is already running":  "AdGuard Trayはすでに起動しています",
    "Only one instance can run at a time. Check your system tray.":
        "同時に起動できるインスタンスは1つだけです。システムトレイを確認してください。",
    "Authentication cancelled":         "認証がキャンセルされました",
    "Authorization failed":             "認証に失敗しました",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "サイトの証明書が失効していないかを確認します（OCSP）。\nAdGuardは非同期でチェックし、チェックに時間がかかる場合は\n接続をそのまま通すため、これが原因でサイトが表示されなくなることはまれです。\n問題の原因がこれだと特定できた場合を除き、オンのままにしてください。",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "Certificate Transparencyのチェックを強制します（ChromeのCTポリシー）。\n自身の証明書がCTに準拠していないサイトはフィルタリングされなくなり、\nブラウザが接続を拒否する場合があります。大規模なサイトは準拠しているため、\nこの設定の変更は、証明書エラーが表示されるサイトがある場合にのみ試してください。",
    "Sites that don't load":
        "読み込めないサイト",
    "Turn off HTTP/3 filtering":
        "HTTP/3フィルタリングをオフにする",
    "No filters installed":
        "インストールされているフィルタはありません",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "HTTP/3はファイアウォールルールによってブロックされています。ブラウザはHTTP/2を使用します。",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "フィルタリング対象外のアプリ（HTTP/3トラフィックもフィルタリングされません）：{}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuardが動作していないため、何もフィルタリングされていません。",
    "could not remove the previous certificate":
        "以前の証明書を削除できませんでした",
    "HTTP/3 state unknown":
        "HTTP/3の状態が不明",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "ファイアウォールルールが送信方向のUDP 443を拒否しているため、QUICは使用できません。",
    "Browser policy disables QUIC: {}":
        "ブラウザのポリシーでQUICが無効になっています：{}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "ブラウザはHTTP/3（UDP 443）経由でAdGuardを回避できます。",
    "Checking…":
        "確認中…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "proxy.yamlを読み込めませんでした。HTTP/3の状態は不明です。",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "HTTP/3をオフにしたFirefox系プロファイル：{}/{}",
    "HTTP/3 (QUIC)":
        "HTTP/3（QUIC）",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "HTTP/3はAdGuardによってブロックされています。ブラウザはフィルタリングされるHTTP/2にフォールバックします。",
    "HTTP/3 is filtered by AdGuard.":
        "HTTP/3はAdGuardによってフィルタリングされています。",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "FirefoxプロファイルでHTTP/3をオフにしました。ブラウザを再起動してください。",
    "HTTPS filtering is off – nothing is filtered.":
        "HTTPSフィルタリングがオフのため、何もフィルタリングされていません。",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "プロキシモード：{}。プロキシを経由するトラフィックのみがフィルタリングされますが、ブラウザはQUICをプロキシ経由で送信しません。",
    "unknown":
        "不明",
    "AdGuard's certificate was not found. Generate it first.":
        "AdGuardの証明書が見つかりません。先に証明書を作成してください。",
    "Certificate could not be installed in any browser.":
        "どのブラウザにも証明書をインストールできませんでした。",
    "Certificate installed for {} of {} stores.":
        "証明書をインストールしました（ストア：{}/{}）。",
    "Chromium-based browsers":
        "Chromium系ブラウザ",
    "No browser certificate stores found.":
        "ブラウザの証明書ストアが見つかりません。",
    "Restart your browsers for the certificate to take effect.":
        "証明書を反映させるには、ブラウザを再起動してください。",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "sudo/pkexecを使わずに実行してください。現在のユーザーのブラウザプロファイルにインストールされます",
    "certificate not found after import":
        "インポート後に証明書が見つかりません",
    "certutil not found – install the 'nss' package":
        "certutilが見つかりません。'nss'パッケージをインストールしてください",
    "not found":
        "見つかりません",
    "Could not read the filter list (unexpected CLI output).":
        "フィルタリストを読み込めませんでした（予期しないCLI出力）。",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "システムトレイが見つかりません。AdGuard Trayはアイコンなしで動作しています。パネルでトレイ/AppIndicatorを有効にしてください。",
    "URL must start with http:// or https://":
        "URLはhttp://またはhttps://で始まる必要があります",
    "adguard-cli path does not exist or is not executable.":
        "adguard-cliのパスが存在しないか、実行可能ではありません。",
    "That binary does not identify as adguard-cli. Save anyway?":
        "指定したバイナリはadguard-cliとして認識されません。このまま保存しますか？",
    "Update channel":                   "アップデートチャンネル",
    "Switching update channel to {}…":  "アップデートチャンネルを{}に切り替え中…",
    "Update channel set to {}":         "アップデートチャンネルを{}に設定しました",
    "Could not set update channel":     "アップデートチャンネルを設定できませんでした",
    "Invalid channel: {}":              "無効なチャンネル：{}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        "アクセスログはまだありません（{}）。AdGuardはトラフィックをフィルタリングするとログを書き込みます。システムサービスとして動作している場合、ログの所有者はrootになるため、ここからは読み取れません。",
    'Cannot read the access log ({}): {}':
        "アクセスログ（{}）を読み取れません：{}",
    'Blocked':
        "ブロック",
    'Blocked only':
        "ブロックのみ",
    "Refresh":
        "再読み込み",
    'Allow selected domain':
        "選択したドメインを許可",
    'Block selected domain':
        "選択したドメインをブロック",
    'Activity':
        "アクティビティ",
    'Time':
        "時刻",
    'Domain':
        "ドメイン",
    'Result':
        "結果",
    'Rule':
        "ルール",
    'Size':
        "サイズ",
    'Count':
        "件数",
    'Could not read the access log.':
        "アクセスログを読み取れませんでした。",
    '{} lines not understood':
        "解析できない行：{}件",
    'Not a valid domain: {}':
        "無効なドメインです：{}",
    'Source: {}':
        "ソース：{}",
    'Allowed':
        "許可",
    'Added rule: {}':
        "ルールを追加しました：{}",
    'Requests per hour, {} to {} · busiest hour: {}':
        "1時間あたりのリクエスト数（{}～{}） · ピーク時：{}件",
    'Last 24 hours':
        "過去24時間",
    'Last 7 days':
        "過去7日間",
    'Requests':
        "リクエスト",
    'Traffic':
        "トラフィック",

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        "バージョン{}が利用可能です（現在のバージョン：{}）。",
    'Application update':
        "アプリケーションのアップデート",
    'Check for update':
        "アップデートを確認",
    'Install update':
        "アップデートをインストール",
    'Installing update…':
        "アップデートをインストール中…",
    'Restart now':
        "今すぐ再起動",
    'Later':
        "後で",
    'You are running the latest version ({}).':
        "最新バージョン（{}）を使用しています。",
    'Installation not recognised':
        "インストール方法を判別できません",
    'Could not check for updates.':
        "アップデートを確認できませんでした。",
    'Update with: {}':
        "アップデートコマンド：{}",
    'Installed with the AUR package {}':
        "AURパッケージ{}でインストール済み",
    'Installed in {}':
        "インストール先：{}",
    'Running from a source checkout':
        "ソースチェックアウトから実行中",
    'Version {} installed. Restart adguard-tray to use it.':
        "バージョン{}をインストールしました。使用するにはadguard-trayを再起動してください。",
    'Unexpected answer from GitHub: {}':
        "GitHubからの予期しない応答：{}",
    'Download failed: {}':
        "ダウンロードに失敗しました：{}",
    'Could not unpack the download: {}':
        "ダウンロードしたファイルを展開できませんでした：{}",
    'This installation is managed elsewhere: {}':
        "このインストールは別の方法で管理されています：{}",
    'No permission to write to {}':
        "{}への書き込み権限がありません",
    'GitHub returned {}.':
        "GitHubから{}が返されました。",
    'No connection to GitHub: {}':
        "GitHubに接続できません：{}",
    'The download does not contain adguard-tray.':
        "ダウンロードしたファイルにadguard-trayが含まれていません。",
    'The download says version {} instead of {} – aborted.':
        "ダウンロードしたファイルのバージョンは{}です（想定：{}）。中止しました。",
    'GitHub is rate limiting this address. Try again later.':
        "GitHubがこのアドレスからのリクエストを制限しています。しばらくしてから再度お試しください。",
    'The download is larger than expected – aborted.':
        "ダウンロードしたファイルが想定より大きいため、中止しました。",
    'Update failed: {}':
        "アップデートに失敗しました：{}",
    'The archive contains unexpected paths – aborted.':
        "アーカイブに想定外のパスが含まれているため、中止しました。",
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        "アップデートに失敗し、以前のバージョンを復元できませんでした。{}から復元するか、次のコマンドで再インストールしてください：{}",
    'Last 30 days':
        "過去30日間",
    'All time':
        "全期間",
    'Modified':
        "変更済み",
    'Rules':
        "ルール",
    'Showing {} – show all':
        "{}を表示中 – すべて表示",
    'history {}':
        "履歴：{}",
    'Filter list ID: {}':
        "フィルタリストID：{}",
    'App':
        "アプリ",
    'Protocol':
        "プロトコル",
    'Type':
        "種類",
    'Reset history':
        "履歴をリセット",
    'Delete the stored history and read the log again.':
        "保存された履歴を削除し、ログを再度読み込みます。",
    'Delete the stored history? Only what the log still holds can be read back.':
        "保存された履歴を削除しますか？再度読み込めるのは、ログに残っている分だけです。",
    'History is not being updated: {}':
        "履歴が更新されていません：{}",

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "AdGuardの設定に未保存の変更が1件あります",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "信頼済みフィルタは、閲覧中のページでスクリプトを実行できます。よく知っている提供元のリストのみ信頼してください。",
    "About":
        "情報",
    "Actions for the selected filter":
        "選択したフィルタの操作",
    "Ad blocking":
        "広告ブロック",
    "Ad blocking is off, so the filter lists below have no effect.":
        "広告ブロックがオフのため、以下のフィルタリストは機能しません。",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLIが最新ビルドをダウンロードしてインストールします。",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "このコンピューター上のライセンス情報がAdGuard CLIから削除されます。再度アクティベートする必要があります。",
    "AdGuard CLI logs":
        "AdGuard CLIのログ",
    "AdGuard CLI update finished.":
        "AdGuard CLIのアップデートが完了しました。",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "AdGuard Trayのログ",
    "AdGuard doesn't filter these websites.":
        "AdGuardはこれらのウェブサイトをフィルタリングしません。",
    "AdGuard is filtering this computer's traffic.":
        "AdGuardがこのコンピューターのトラフィックをフィルタリングしています。",
    "AdGuard restarts to load the new lists.":
        "新しいリストを読み込むため、AdGuardが再起動します。",
    "AdGuard's reply did not say whether it is running.":
        "AdGuardの応答からは、動作中かどうかを判断できませんでした。",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "AdGuardの設定ファイルが見つかりません（{}）。作成するには、adguard-cliを一度実行してください。",
    "Add DNS filter by ID":
        "IDでDNSフィルタを追加",
    "Add DNS filter from URL":
        "URLからDNSフィルタを追加",
    "Add filter":
        "フィルタを追加",
    "Add filter by ID":
        "IDでフィルタを追加",
    "Add filter from URL":
        "URLからフィルタを追加",
    "Add rule":
        "ルールを追加",
    "Add to browsers":
        "ブラウザに追加",
    "Add userscript":
        "ユーザースクリプトを追加",
    "Add userscript…":
        "ユーザースクリプトを追加…",
    "Add website":
        "ウェブサイトを追加",
    "Add…":
        "追加…",
    "Advanced":
        "詳細設定",
    "All available":
        "すべて",
    "Allow {}":
        "{}を許可",
    "Also adds the certificate to this Firefox profile.":
        "このFirefoxプロファイルにも証明書を追加します。",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "再起動時やエラー発生時にも通知します。notify-send（libnotify）か、動作中の通知サービス（dunst、mako、KDE標準のものなど）が必要です。",
    "Appearance":
        "外観",
    "Applies after AdGuard Tray restarts.":
        "AdGuard Trayの再起動後に適用されます。",
    "Apply":
        "適用",
    "Apply your changes to AdGuard's settings before closing?":
        "閉じる前に、AdGuardの設定への変更を適用しますか？",
    "Applying them restarts AdGuard if protection is on.":
        "保護がオンの場合、適用するとAdGuardが再起動します。",
    "Asks GitHub for the newest release.":
        "GitHubで最新リリースを確認します。",
    "At a glance":
        "現在の状況",
    "Automatic":
        "自動",
    "Automatic – filter all apps":
        "自動 – すべてのアプリをフィルタリング",
    "Benchmark":
        "ベンチマーク",
    "Beta":
        "ベータ",
    "Block ECH in DNS records":
        "DNSレコードのECHをブロック",
    "Block domains before a connection is made.":
        "接続が確立される前にドメインをブロックします。",
    "Block {}":
        "{}をブロック",
    "Blocked (24 h)":
        "ブロック（24時間）",
    "Browser list ({})":
        "ブラウザリスト（{}）",
    "By ID or name…":
        "IDまたは名前で…",
    "Certificate":
        "証明書",
    "Certificate checks":
        "証明書チェック",
    "Changes are collected in the bar at the bottom and applied together.":
        "変更は下部のバーにまとめられ、一括で適用されます。",
    "Check again":
        "再確認",
    "Check every":
        "確認間隔",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "Chromium系とFirefox系のブラウザは、独自の証明書ストアを使用します。",
    "Close":
        "閉じる",
    "Controls which AdGuard CLI build “{}” installs.":
        "「{}」でインストールされるAdGuard CLIのビルドを指定します。",
    "Could not add the rule.":
        "ルールを追加できませんでした。",
    "Could not open {}":
        "{}を開けませんでした",
    "Could not read {}":
        "{}を読み込めませんでした",
    "Could not refresh. Showing data from {}.":
        "再読み込みできませんでした。{}時点のデータを表示しています。",
    "Could not reset the history.":
        "履歴をリセットできませんでした。",
    "Could not restart AdGuard.":
        "AdGuardを再起動できませんでした。",
    "Could not start protection.":
        "保護を開始できませんでした。",
    "Could not stop protection.":
        "保護を停止できませんでした。",
    "Create":
        "作成",
    "Create certificate":
        "証明書を作成",
    "Custom":
        "カスタム",
    "DNS filter lists":
        "DNSフィルタリスト",
    "DNS filtering":
        "DNSフィルタリング",
    "DNS filtering is off, so these lists have no effect.":
        "DNSフィルタリングがオフのため、これらのリストは機能しません。",
    "DNS servers":
        "DNSサーバー",
    "Dark":
        "ダーク",
    "Default":
        "デフォルト",
    "Details":
        "詳細",
    "Discard":
        "破棄",
    "Don't filter":
        "フィルタリングしない",
    "Don't trust":
        "信頼しない",
    "Downloads and installs the newest AdGuard CLI build.":
        "最新のAdGuard CLIビルドをダウンロードしてインストールします。",
    "Duration":
        "所要時間",
    "Export…":
        "エクスポート…",
    "Filter everything":
        "すべてフィルタリング",
    "Filter in place":
        "その場でフィルタリング",
    "Filtering":
        "フィルタリング",
    "Follow system":
        "システムに合わせる",
    "From URL…":
        "URLから…",
    "Go to updates":
        "アップデートへ移動",
    "HTTP proxy: {}":
        "HTTPプロキシ：{}",
    "HTTPS filtering":
        "HTTPSフィルタリング",
    "How much detail AdGuard Tray writes to its own log.":
        "AdGuard Trayのログに記録する内容の詳しさを設定します。",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "サイトが読み込めない場合は、まずHTTP/3フィルタリングをオフにしてください。その他のチェックはすべてのサイトを保護するものです。それでも解決しない場合にのみオフにしてください。",
    "Included":
        "組み込み",
    "Installed":
        "インストール済み",
    "License":
        "ライセンス",
    "Light":
        "ライト",
    "Logs":
        "ログ",
    "MIT license":
        "MITライセンス",
    "Maintenance":
        "メンテナンス",
    "Manual proxy":
        "手動プロキシ",
    "Manual – only apps set to use the proxy":
        "手動 – プロキシを使うよう設定したアプリのみ",
    "More":
        "その他の操作",
    "Move down":
        "下へ移動",
    "Move up":
        "上へ移動",
    "Network":
        "ネットワーク",
    "Nightly":
        "ナイトリー",
    "No requests yet – AdGuard logs requests while protection is on.":
        "まだリクエストはありません。保護がオンの間、AdGuardはリクエストを記録します。",
    "Not added":
        "未追加",
    "Nothing matches your search.":
        "一致する項目はありません。",
    "Notify me when protection turns on or off":
        "保護のオン/オフ時に通知する",
    "Off":
        "オフ",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "DoHまたはDoTを使用するブラウザにのみ影響します。「オフ」にすると、それらのブラウザはAdGuardのDNSフィルタリングを回避します。",
    "Open AdGuard Tray":
        "AdGuard Trayを開く",
    "Open exceptions":
        "例外を開く",
    "Open folder":
        "フォルダを開く",
    "Open release page":
        "リリースページを開く",
    "Pages":
        "ページ",
    "Performance":
        "パフォーマンス",
    "Protection":
        "保護",
    "Protection started.":
        "保護を開始しました。",
    "Protection stopped.":
        "保護を停止しました。",
    "Proxy mode":
        "プロキシモード",
    "Redirect to AdGuard's DNS":
        "AdGuardのDNSにリダイレクト",
    "Refresh this page (F5)":
        "このページを再読み込み（F5）",
    "Release (stable)":
        "リリース（安定版）",
    "Remove rule":
        "ルールを削除",
    "Remove “{}”?":
        "「{}」を削除しますか？",
    "Remove…":
        "削除…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "現在のAdGuardの設定を「{}」の設定に置き換えますか？\n\n設定を適用するためAdGuardが再起動します。",
    "Reset history…":
        "履歴をリセット…",
    "Reset…":
        "リセット…",
    "Restart AdGuard":
        "AdGuardを再起動",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "ルールは自動プロキシモードでのみ適用されます。最初に一致したルールが優先されるため、\"*\"は最後に置いてください。",
    "Safe Browsing":
        "セーフブラウジング",
    "Save anyway":
        "このまま保存",
    "Saved. AdGuard restarts to apply the change.":
        "保存しました。変更を適用するためAdGuardが再起動します。",
    "Saved. Applies after AdGuard Tray restarts.":
        "保存しました。AdGuard Trayの再起動後に適用されます。",
    "Saved. The change applies when protection is turned on.":
        "保存しました。変更は保護をオンにしたときに適用されます。",
    "Secure DNS and ECH":
        "セキュアDNSとECH",
    "Secure DNS filtering":
        "セキュアDNSフィルタリング",
    "Set the path in Settings":
        "「設定」でパスを指定",
    "Settings":
        "設定",
    "Show":
        "表示",
    "Show recent entries":
        "最近の項目を表示",
    "Skip HTTPS filtering":
        "HTTPSフィルタリングを除外",
    "Some counts could not be loaded.":
        "一部の件数を読み込めませんでした。",
    "Source code":
        "ソースコード",
    "Start AdGuard Tray when I log in":
        "ログイン時にAdGuard Trayを起動する",
    "Startup":
        "起動",
    "Status checks":
        "状態チェック",
    "Stealth mode":
        "ステルスモード",
    "System":
        "システム",
    "The new lists load when protection is turned on.":
        "新しいリストは保護をオンにしたときに読み込まれます。",
    "Theme":
        "テーマ",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "HTTP/3フィルタリング、OCSPチェック、Certificate Transparency、セキュアDNSフィルタリングがオフになります。失効した証明書や誤って発行された証明書が検出されなくなり、ブラウザはAdGuardのDNSフィルタを経由せずに名前解決できるようになります。",
    "Time range":
        "期間",
    "To keep it but stop using it, switch it off instead.":
        "削除せずに使用だけを停止するには、代わりにオフにしてください。",
    "Top lists":
        "ランキング",
    "Trust":
        "信頼",
    "Trust “{}”?":
        "「{}」を信頼しますか？",
    "Trust…":
        "信頼…",
    "Turn off all strict checks…":
        "厳格なチェックをすべてオフにする…",
    "Undo":
        "元に戻す",
    "Unknown":
        "不明",
    "Unsaved changes":
        "未保存の変更",
    "Update AdGuard CLI…":
        "AdGuard CLIを更新…",
    "Update channel: {}":
        "アップデートチャンネル：{}",
    "Updated {}":
        "更新日時：{}",
    "Updates":
        "アップデート",
    "Used in manual mode only.":
        "手動モードでのみ使用されます。",
    "Userscripts update together with filters.":
        "ユーザースクリプトはフィルタと一緒に更新されます。",
    "Uses XDG autostart (~/.config/autostart).":
        "XDGの自動起動（~/.config/autostart）を使用します。",
    "Waiting for authorization…":
        "認証を待っています…",
    "Website exceptions":
        "ウェブサイトの例外",
    "Websites":
        "ウェブサイト",
    "example.com or a link":
        "example.comまたはリンク",
    "expires {}":
        "有効期限：{}",
    "of {} requests in the last 24 hours":
        "過去24時間のリクエスト：{}件中",
    "{} of {} DNS filters on":
        "有効なDNSフィルタ：{}/{}",
    "{} of {} filters on":
        "有効なフィルタ：{}/{}",
    "{} of {} on":
        "有効：{}/{}",
    "{} unsaved changes to AdGuard's settings":
        "AdGuardの設定に未保存の変更が{}件あります",
    "“Follow system” uses your desktop's light or dark setting.":
        "「システムに合わせる」はデスクトップのライト/ダーク設定に従います。",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "有効",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "AdGuardの証明書を、このシステムで見つかったすべてのブラウザプロファイルに追加します。\n\nこれにより、AdGuardはこれらのブラウザのHTTPSトラフィックを検査できるようになります。ブラウザは起動時に証明書ストアを読み込むため、先にブラウザを閉じてください。",
    "Allow":
        "許可",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "AdGuardの設定への変更を先に適用するか破棄してから、再起動してください。",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "自動：AdGuardはiptablesを使ってすべてのアプリのトラフィックを自身にリダイレクトします。手動：AdGuardは下のSOCKS5ポートとHTTPポートでのみ待ち受けます。",
    "Block":
        "ブロック",
    "Browser API blocking":
        "ブラウザAPIのブロック",
    "CRLite":
        "CRLite",
    "Cancel":
        "キャンセル",
    "Computers":
        "コンピューター",
    "Could not change the autostart entry.":
        "自動起動の設定を変更できませんでした。",
    "Could not export the logs.":
        "ログをエクスポートできませんでした。",
    "Could not export the settings.":
        "設定をエクスポートできませんでした。",
    "Could not reset the license.":
        "ライセンスをリセットできませんでした。",
    "Could not retrieve license info.":
        "ライセンス情報を取得できませんでした。",
    "Could not run the benchmark.":
        "ベンチマークを実行できませんでした。",
    "Could not save the settings.":
        "設定を保存できませんでした。",
    "Could not set the update channel.":
        "アップデートチャンネルを設定できませんでした。",
    "Could not update AdGuard CLI.":
        "AdGuard CLIを更新できませんでした。",
    "Could not update the filters.":
        "フィルタを更新できませんでした。",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "DNSアップストリームサーバー。\n'default' = システムのDNS。\n例：1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com",
    "Expiration date":
        "有効期限",
    "Expires":
        "有効期限",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "FirefoxプロファイルでHTTP/3を再びオンにしました。ブラウザを再起動してください。",
    "License key":
        "ライセンスキー",
    "License type":
        "ライセンスの種類",
    "Manual":
        "手動",
    "No exceptions.":
        "例外はありません。",
    "OK":
        "OK",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "オン：AdGuard自身がHTTP/3（QUIC）をフィルタリングします（試験的機能）。ただし、\n一部のブラウザはユーザーがインストールした証明書経由のHTTP/3をそもそも拒否します。\nオフ：AdGuardは代わりにQUICをブロックし、ブラウザはHTTP/2にフォールバックします。\nHTTP/2は確実にフィルタリングされます。\nいずれの場合も、適用されるのは自動モードのみです。手動モードでは、\nHTTP/3のトラフィックがAdGuardに届くことはありません。",
    "Owner":
        "所有者",
    "Personal":
        "パーソナル",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "プロキシモードが{}のため、UDPポート443はAdGuardにリダイレクトされます。",
    "Save adguard-cli path":
        "adguard-cliのパスを保存",
    "Search domains or rules…":
        "ドメインまたはルールを検索…",
    "Settings file":
        "設定ファイル",
    "Status":
        "状態",
    "Trial":
        "試用版",
    "Turn HTTP/3 back on in Firefox profiles":
        "FirefoxプロファイルでHTTP/3を再びオンにする",
    "Turn off":
        "オフにする",
    "Turn off HTTP/3 in Firefox profiles":
        "FirefoxプロファイルでHTTP/3をオフにする",
    "Turn off HTTP/3 in Firefox profiles…":
        "FirefoxプロファイルでHTTP/3をオフにする…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "{}個のFirefox系プロファイルでHTTP/3をオフにしますか？\n\nトラフィックはHTTP/2を使用するようになり、AdGuardでフィルタリングできます。完了後にブラウザを再起動してください。",
    "Turn off all strict checks":
        "厳格なチェックをすべてオフにする",
    "Unavailable until AdGuard CLI reports its current channel.":
        "AdGuard CLIが現在のチャンネルを報告するまで利用できません。",
    "Update AdGuard CLI":
        "AdGuard CLIを更新",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "自動モードでのみ使用されます。範囲（80:5221,5300:49151）または単一のポート（80,443,8080）で指定します。",
    "{} of {}":
        "{}/{}",
    "{} of {} userscripts on":
        "有効なユーザースクリプト：{}/{}",
    "{}% blocked":
        "{}%をブロック",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "迷惑要素",
    "General":
        "一般",
    "Language-specific":
        "言語別",
    "Security":
        "セキュリティ",
    "Social widgets":
        "ソーシャルウィジェット",
    "Expired":
        "期限切れ",
    "Autostart on login":
        "ログイン時に自動起動",
    "Add app rule":
        "アプリのルールを追加",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "ワイルドカードが使えます（例：*steam*、*EasyAntiCheat*）。",
    "There is already a rule for '{}'.":
        "「{}」のルールはすでにあります。",
    "AdGuard settings":
        "AdGuardの設定",
    "Ads and trackers are not blocked until you enable protection.":
        "保護を有効にするまで、広告やトラッカーはブロックされません。",
    "Could not import the settings.":
        "設定をインポートできませんでした。",
    "Disable protection":
        "保護を無効化",
    "Enable protection":
        "保護を有効化",
    "Export and import":
        "エクスポートとインポート",
    "Features":
        "機能",
    "Import settings":
        "設定をインポート",
    "Import settings from…":
        "設定のインポート元…",
    "Import settings…":
        "設定をインポート…",
    "Import…":
        "インポート…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "フィルタ、ルール、設定をzipファイルに保存するか、zipファイルから読み込みます。",
    "Update":
        "更新",
    "Version":
        "バージョン",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "「{}」は設定のエクスポートファイルではありません。「AdGuardの設定」の「エクスポート…」で保存したファイルを選択してください。",
}
