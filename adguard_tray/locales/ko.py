"""Korean."""

STRINGS: dict[str, str] = {
    # ── General ─────────────────────────────────────────────────────
    "Language":                          "언어",
    "English":                           "영어",

    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "활성 – 보호 실행 중",
    "Inactive – Protection stopped":        "비활성 – 보호 중지됨",
    "Error retrieving status":              "상태 조회 오류",
    "adguard-cli not found":                "adguard-cli를 찾을 수 없음",
    "Unknown status":                       "알 수 없는 상태",
    "Checking status…":                     "상태 확인 중…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Restart":                              "다시 시작",
    "Filters":                              "필터",
    "Loading…":                             "불러오는 중…",
    "Manage filters…":                      "필터 관리…",
    "No userscripts installed":             "설치된 사용자 스크립트 없음",
    "Manage userscripts…":                  "사용자 스크립트 관리…",
    "Quit":                                 "종료",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "활성",
    "inactive":                             "비활성",
    "System-wide filtering: {}":            "시스템 전체 필터링: {}",
    "Error: {}":                            "오류: {}",
    "AdGuard Tray – Error":                 "AdGuard Tray – 오류",
    "AdGuard is now active – protection running.":
        "AdGuard가 활성화되었습니다 – 보호가 실행 중입니다.",
    "AdGuard has been stopped.":
        "AdGuard가 중지되었습니다.",
    "Could not retrieve status.":
        "상태를 가져올 수 없습니다.",
    "Command failed":                       "명령 실패",

    # ── settings_dialog.py ────────────────────────────────────────────────
    " seconds":                             " 초",
    "How often adguard-cli status is checked automatically.":
        "adguard-cli 상태를 자동으로 확인하는 간격입니다.",
    "Log level:":                           "로그 수준:",
    "adguard-cli path:":                    "adguard-cli 경로:",
    "auto-detect via PATH":                 "PATH에서 자동 감지",
    "Browse…":                              "찾아보기…",
    "Select adguard-cli binary":            "adguard-cli 실행 파일 선택",
    "Notifications":                        "알림",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "Update filters":                       "필터 업데이트",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "모든 필터, DNS 필터, 사용자 스크립트,\nSafebrowsingV2, CRLite를 업데이트하고 앱 업데이트를 확인합니다.",
    "No filters found.":                    "필터가 없습니다.",
    "Updating filters… (can take up to 2 minutes)":
        "필터 업데이트 중… (최대 2분 걸릴 수 있음)",
    "Update completed.":                    "업데이트가 완료되었습니다.",
    "Update failed.":                       "업데이트에 실패했습니다.",
    "Installing: {}":                       "설치 중: {}",
    "Filter installed.":                    "필터를 설치했습니다.",
    "Remove":                               "제거",
    "Remove filter":                        "필터 제거",
    "Filter {} removed.":                   "필터({})를 제거했습니다.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "Install userscript from a direct .js URL":
        ".js 직접 URL에서 사용자 스크립트 설치",
    "No userscripts installed.":            "설치된 사용자 스크립트가 없습니다.",
    "Userscript URL (direct .js URL):":     "사용자 스크립트 URL(.js 직접 URL):",
    "Userscript installed.":                "사용자 스크립트를 설치했습니다.",
    'Remove "{}"':                          "“{}” 제거",
    "Remove userscript":                    "사용자 스크립트 제거",
    "'{}' removed.":                        "“{}” 사용자 스크립트를 제거했습니다.",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install via official script or AUR:\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n"
    "  paru -S adguard-cli-bin":
        "adguard-cli를 찾을 수 없습니다.\n공식 스크립트 또는 AUR로 설치하세요:\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n  paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "상태 조회 중 알 수 없는 오류",
    "AdGuard {} ok":                        "AdGuard {} 성공",
    "AdGuard via systemctl {} ok":          "AdGuard(systemctl {}) 성공",
    "'{}' failed – insufficient privileges?":
        "“{}” 실패 – 권한 부족?",
    "Could not retrieve filter list":
        "필터 목록 조회 실패",
    "Filter {} enabled":                    "필터 {} 활성화됨",
    "Could not enable filter {}":           "필터 {} 활성화 실패",
    "Filter {} disabled":                   "필터 {} 비활성화됨",
    "Could not disable filter {}":
        "필터 {} 비활성화 실패",
    "Filter installed":                     "필터 설치됨",
    "Installation failed":                  "설치 실패",
    "Filter {} removed":                    "필터 {} 제거됨",
    "Could not remove filter {}":
        "필터 {} 제거 실패",
    "Filters updated":                      "필터 업데이트됨",
    "Update failed":                        "업데이트 실패",
    "Could not retrieve userscript list":
        "사용자 스크립트 목록 조회 실패",
    "Userscript '{}' enabled":              "“{}” 사용자 스크립트 활성화됨",
    "Could not enable userscript '{}'":
        "“{}” 사용자 스크립트 활성화 실패",
    "Userscript '{}' disabled":             "“{}” 사용자 스크립트 비활성화됨",
    "Could not disable userscript '{}'":
        "“{}” 사용자 스크립트 비활성화 실패",
    "Userscript '{}' removed":              "“{}” 사용자 스크립트 제거됨",
    "Could not remove userscript '{}'":
        "“{}” 사용자 스크립트 제거 실패",
    "Userscript installed":                 "사용자 스크립트 설치됨",
    "Other":                                "기타",

    # ── search (filters_dialog / userscripts_dialog) ────────────────────
    "Search filters…":                  "필터 검색…",
    "Search userscripts…":              "사용자 스크립트 검색…",

    # ── proxy_config_dialog.py ───────────────────────────────────────────
    "Could not load proxy.yaml.\nPath: {}":
        "proxy.yaml 파일을 불러올 수 없습니다.\n경로: {}",
    "HTTPS":                            "HTTPS",
    "DNS":                              "DNS",
    "Apps":
        "앱",
    "Mode:":                            "모드:",
    "Filtered ports:":                  "필터링할 포트:",
    "SOCKS5 port:":                     "SOCKS5 포트:",
    "SOCKS5 proxy port for manual mode.\nSet to -1 to disable.":
        "수동 모드에서 사용할 SOCKS5 프록시 포트입니다.\n-1로 설정하면 비활성화됩니다.",
    "HTTP port:":                       "HTTP 포트:",
    "HTTP proxy port for manual mode.\nSet to -1 to disable.":
        "수동 모드에서 사용할 HTTP 프록시 포트입니다.\n-1로 설정하면 비활성화됩니다.",
    "Listen address:":                  "수신 주소:",
    "Address the proxy listens on.\n"
    "127.0.0.1 = local only. 0.0.0.0 = all interfaces (requires auth).":
        "프록시가 수신하는 주소입니다.\n127.0.0.1 = 로컬 전용. 0.0.0.0 = 모든 인터페이스(인증 필요).",
    "Worker threads:":                  "작업자 스레드:",
    "Number of proxy worker threads.":  "프록시 작업자 스레드 수입니다.",
    "Decrypt and filter HTTPS traffic.\nNeeded to block ads on https sites.\nRequires a trusted root certificate installed on the system.":
        "HTTPS 트래픽을 복호화하고 필터링합니다.\nhttps 사이트의 광고를 차단하려면 필요합니다.\n시스템에 신뢰할 수 있는 루트 인증서가 설치되어 있어야 합니다.",
    "Enable TLS 1.3":                   "TLS 1.3 활성화",
    "Enable TLS 1.3 support for filtered connections.":
        "필터링되는 연결에 TLS 1.3 지원을 활성화합니다.",
    "Filter HTTP/3 (QUIC) – experimental":
        "HTTP/3(QUIC) 필터링 – 실험적",
    "OCSP certificate checks":          "OCSP 인증서 검사",
    "Enforce Certificate Transparency": "인증서 투명성 강제 적용",
    "Filter EV certificate sites":      "EV 인증서 사이트 필터링",
    "By default, sites with Extended Validation certificates are not filtered.\n"
    "Enable this to filter them as well (e.g. banking sites).":
        "기본적으로 확장 검증(EV) 인증서를 사용하는 사이트는 필터링하지 않습니다.\n이러한 사이트도 필터링하려면 활성화하세요(예: 은행 사이트).",
    "Encrypted Client Hello (ECH)":     "Encrypted Client Hello(ECH)",
    "Enable ECH for better privacy.\nRequires DNS filtering to be enabled.":
        "ECH를 활성화하여 개인정보 보호를 강화합니다.\nDNS 필터링이 활성화되어 있어야 합니다.",
    "Filter DNS queries to block ads and trackers at the DNS level.\n"
    "Uses a local DNS proxy with configurable upstreams.":
        "DNS 쿼리를 필터링하여 DNS 수준에서 광고와 추적기를 차단합니다.\n업스트림을 설정할 수 있는 로컬 DNS 프록시를 사용합니다.",
    "Upstream:":                        "업스트림:",
    "Fallbacks:":                       "폴백:",
    "Fallback DNS servers (used when primary upstream fails).\n"
    "'default' = system DNS. Space-separated list.\n"
    "Example: default 1.1.1.1":
        "폴백 DNS 서버입니다(기본 업스트림에 장애가 있을 때 사용).\n'default' = 시스템 DNS. 공백으로 구분한 목록입니다.\n예: default 1.1.1.1",
    "Bootstraps:":                      "부트스트랩:",
    "Bootstrap DNS for resolving upstream hostnames.\n"
    "'default' = system DNS IPs. Only IP addresses allowed.\n"
    "Example: default 8.8.8.8 tls://1.1.1.1":
        "업스트림 호스트 이름을 확인하는 부트스트랩 DNS입니다.\n'default' = 시스템 DNS IP. IP 주소만 사용할 수 있습니다.\n예: default 8.8.8.8 tls://1.1.1.1",
    "Remove ECH parameter from SVCB/HTTPS DNS records.\n"
    "Enable only for browsers that don't auto-detect HTTPS filtering.":
        "SVCB/HTTPS DNS 레코드에서 ECH 매개변수를 제거합니다.\nHTTPS 필터링을 자동으로 감지하지 못하는 브라우저에서만 활성화하세요.",
    "Master switch for all tracking protection features below.":
        "아래 모든 추적 보호 기능을 한 번에 켜고 끄는 마스터 스위치입니다.",
    "Cookies":                          "쿠키",
    "Block third-party cookies":        "서드파티 쿠키 차단",
    "Delete third-party cookies after a set time.\nPrevents cross-site tracking.":
        "설정한 시간이 지나면 서드파티 쿠키를 삭제합니다.\n사이트 간 추적을 방지합니다.",
    "Lifetime (minutes):":              "유효 기간(분):",
    "0 = block immediately. Default: 180 minutes.":
        "0 = 즉시 차단. 기본값: 180분.",
    "Block first-party cookies":        "퍼스트파티 쿠키 차단",
    "Delete all cookies (including first-party) after a set time.\n"
    "Warning: this logs you out of every site.":
        "설정한 시간이 지나면 모든 쿠키(퍼스트파티 포함)를 삭제합니다.\n경고: 모든 사이트에서 로그아웃됩니다.",
    "0 = block immediately. Default: 4320 minutes (3 days).":
        "0 = 즉시 차단. 기본값: 4320분(3일).",
    "Privacy":                          "개인정보 보호",
    "Hide / reduce User-Agent":         "User-Agent 숨기기/축소",
    "Strips identifying bits from the User-Agent.\n"
    "Reduces fingerprinting.":
        "User-Agent에서 식별 정보를 제거합니다.\n핑거프린팅을 줄입니다.",
    "Hide search queries in referrer":  "리퍼러에서 검색어 숨기기",
    "Hides your search terms when clicking from a search engine to a website.":
        "검색 엔진에서 웹사이트로 이동할 때 검색어를 숨깁니다.",
    "Remove referrer from third-party requests":
        "서드파티 요청에서 리퍼러 제거",
    "Prevents third-party sites from knowing which page you came from.":
        "서드파티 사이트가 이전에 방문한 페이지를 알지 못하게 합니다.",
    "Send Do-Not-Track signal":         "추적 금지(DNT) 신호 전송",
    "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it.":
        "요청과 함께 DNT 헤더를 보냅니다.\n참고: 대부분의 사이트는 이를 무시하지만 일부 사이트는 따릅니다.",
    "Disable third-party ETag cache":   "서드파티 ETag 캐시 비활성화",
    "Prevents tracking via ETag caching in third-party content.":
        "서드파티 콘텐츠의 ETag 캐싱을 통한 추적을 방지합니다.",
    "Block third-party Authorization header":
        "서드파티 Authorization 헤더 차단",
    "Blocks the Authorization header in third-party requests to prevent tracking.":
        "서드파티 요청의 Authorization 헤더를 차단하여 추적을 방지합니다.",
    "Remove X-Client-Data header":      "X-Client-Data 헤더 제거",
    "Removes the X-Client-Data header sent by Chrome to Google services.":
        "Chrome이 Google 서비스로 보내는 X-Client-Data 헤더를 제거합니다.",
    "Block WebRTC":                     "WebRTC 차단",
    "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps.":
        "WebRTC를 통한 IP 유출을 방지합니다.\n화상 통화와 일부 웹 앱이 제대로 작동하지 않을 수 있습니다.",
    "Block Push API":                   "푸시 API 차단",
    "Blocks browser push notifications from websites.":
        "웹사이트의 브라우저 푸시 알림을 차단합니다.",
    "Block Location API":               "위치 API 차단",
    "Prevents websites from accessing your GPS location.":
        "웹사이트가 GPS 위치에 접근하지 못하게 합니다.",
    "Block Flash":                      "Flash 차단",
    "Blocks the Flash plugin.":
        "Flash 플러그인을 차단합니다.",
    "Block Java":                       "Java 차단",
    "Disables Java plugins. JavaScript remains enabled.":
        "Java 플러그인을 비활성화합니다. JavaScript는 계속 활성화됩니다.",
    "Anti-DPI":                         "Anti-DPI",
    "Enable Anti-DPI":                  "Anti-DPI 활성화",
    "Alters outgoing packet data to bypass Deep Packet Inspection.\nUseful in countries with internet censorship.":
        "나가는 패킷 데이터를 변경하여 심층 패킷 검사(DPI)를 우회합니다.\n인터넷 검열이 있는 국가에서 유용합니다.",
    "App pattern":
        "앱 패턴",
    "Skip outbound proxy":              "아웃바운드 프록시 건너뛰기",
    "Don't route this app's traffic through outbound proxy":
        "이 앱의 트래픽을 아웃바운드 프록시로 보내지 않음",
    "Browser list included from {}":    "포함된 브라우저 목록(출처: {})",
    "The browser include-list and wildcard (*) rule cannot be removed.":
        "브라우저 포함 목록과 와일드카드(*) 규칙은 제거할 수 없습니다.",
    "Warns about malicious and phishing websites.\nUses AdGuard's Safe Browsing database.":
        "악성 및 피싱 웹사이트에 대해 경고합니다.\nAdGuard 브라우징 보안 데이터베이스를 사용합니다.",
    "Send anonymous statistics":        "익명 통계 전송",
    "Send anonymous lookups to AdGuard.":
        "AdGuard에 익명 조회 정보를 보냅니다.",
    "Certificate revocation checking using Mozilla's CRLite.\nFaster and more reliable than traditional CRL/OCSP checks.":
        "Mozilla의 CRLite를 사용하여 인증서 폐기 여부를 확인합니다.\n기존 CRL/OCSP 검사보다 빠르고 안정적입니다.",
    "Apply ad-blocking filter rules to HTTP/HTTPS requests.":
        "HTTP/HTTPS 요청에 광고 차단 필터 규칙을 적용합니다.",
    "Save failed":                      "저장 실패",
    "Could not save proxy.yaml:\n{}":   "proxy.yaml 파일을 저장하지 못했습니다:\n{}",
    "Restarting AdGuard…":              "AdGuard 다시 시작 중…",
    "AdGuard restarted.":               "AdGuard가 다시 시작되었습니다.",
    "Restart failed: {}":               "다시 시작 실패: {}",
    "Unknown error":                    "알 수 없는 오류",

    # ── exceptions_dialog.py ────────────────────────────────────────────
    "Add":                              "추가",
    "Search exceptions…":               "예외 검색…",
    "1 exception":                      "예외 1개",
    "{} exceptions":                    "예외 {}개",
    "'{}' is not a valid domain or IP address.":
        "“{}” 항목은 유효한 도메인이나 IP 주소가 아닙니다.",
    "'{}' is already in the list.":     "“{}” 항목이 이미 목록에 있습니다.",
    "Could not save exceptions:\n{}":
        "예외를 저장하지 못했습니다:\n{}",

    # ── manager_window.py ──────────────────────────────────────────────────
    "Overview":                         "개요",
    "Userscripts":                      "사용자 스크립트",
    "Exceptions":                       "예외",

    # ── overview_tab.py ──────────────────────────────────────────────────
    "Reset license":                    "라이선스 초기화",
    "Generate a root CA certificate for HTTPS filtering. "
    "The certificate must be installed and trusted on your system.":
        "HTTPS 필터링에 사용할 루트 CA 인증서를 생성합니다. 인증서를 시스템에 설치하고 신뢰하도록 설정해야 합니다.",
    "Checking for updates…":            "업데이트 확인 중…",
    "Firefox profile:":                 "Firefox 프로필:",
    "(optional) e.g. abcd1234.MyProfile":
        "(선택 사항) 예: abcd1234.MyProfile",

    # ── filters_tab.py ───────────────────────────────────────────────────
    "Enter filter ID or name:":         "필터 ID 또는 이름을 입력하세요:",
    "Filter added.":                    "필터를 추가했습니다.",
    "Rename…":                          "이름 바꾸기…",
    "Rename filter":                    "필터 이름 바꾸기",
    "New title:":                       "새 이름:",
    "Filter renamed.":                  "필터 이름을 바꿨습니다.",
    "Filter trust updated.":            "필터 신뢰 설정을 변경했습니다.",
    "Filter URL:":                      "필터 URL:",
    "Title:":                           "이름:",
    "(optional)":                       "(선택 사항)",
    "Trusted filter":                   "신뢰할 수 있는 필터",

    # ── dns_filters_tab.py ───────────────────────────────────────────────
    "Search DNS filters…":              "DNS 필터 검색…",
    "No DNS filters found.":            "DNS 필터가 없습니다.",
    "DNS filter installed.":            "DNS 필터를 설치했습니다.",
    "DNS filter added.":                "DNS 필터를 추가했습니다.",
    "Remove DNS filter":                "DNS 필터 제거",
    "DNS filter {} removed.":           "DNS 필터({})를 제거했습니다.",
    "Rename DNS filter":                "DNS 필터 이름 바꾸기",
    "DNS filter renamed.":              "DNS 필터 이름을 바꿨습니다.",

    # ── config_tab.py ────────────────────────────────────────────────────

    # ── diagnostics_tab.py ───────────────────────────────────────────────
    "Export logs…":                     "로그 내보내기…",
    "Export AdGuard CLI logs to a zip file":
        "AdGuard CLI 로그를 zip 파일로 내보냅니다",
    "Export settings…":                 "설정 내보내기…",
    "Run a cryptographic and HTTPS filtering benchmark.":
        "암호화 및 HTTPS 필터링 벤치마크를 실행합니다.",
    "Run benchmark":                    "벤치마크 실행",
    "Done.":                            "완료되었습니다.",
    "Export logs to…":                  "로그를 내보낼 위치…",
    "Export settings to…":              "설정을 내보낼 위치…",
    "Zip files (*.zip);;All files (*)":
        "zip 파일 (*.zip);;모든 파일 (*)",
    "Log file not found.":              "로그 파일을 찾을 수 없습니다.",

    # ── cli.py (new methods) ─────────────────────────────────────────────
    "Could not retrieve DNS filter list":
        "DNS 필터 목록 조회 실패",
    "DNS filter {} enabled":            "DNS 필터 {} 활성화됨",
    "Could not enable DNS filter {}":   "DNS 필터 {} 활성화 실패",
    "DNS filter {} disabled":           "DNS 필터 {} 비활성화됨",
    "Could not disable DNS filter {}":  "DNS 필터 {} 비활성화 실패",
    "DNS filter installed":             "DNS 필터 설치됨",
    "DNS filter {} removed":            "DNS 필터 {} 제거됨",
    "Could not remove DNS filter {}":   "DNS 필터 {} 제거 실패",
    "DNS filter added":                 "DNS 필터 추가됨",
    "Could not add DNS filter":         "DNS 필터 추가 실패",
    "DNS filter title updated":         "DNS 필터 이름 변경됨",
    "Could not set DNS filter title":   "DNS 필터 이름 설정 실패",
    "Filter added":                     "필터 추가됨",
    "Could not add filter":             "필터 추가 실패",
    "Filter trust updated":             "필터 신뢰 설정 변경됨",
    "Could not update filter trust":    "필터 신뢰 설정 변경 실패",
    "Filter title updated":             "필터 이름 변경됨",
    "Could not set filter title":       "필터 이름 설정 실패",
    "License reset":                    "라이선스 초기화됨",
    "Could not reset license":          "라이선스 초기화 실패",
    "Could not retrieve license info":  "라이선스 정보 조회 실패",
    "Certificate generated":            "인증서 생성됨",
    "Certificate generation failed":    "인증서 생성 실패",
    "Logs exported":                    "로그 내보냄",
    "Log export failed":                "로그 내보내기 실패",
    "Settings exported":                "설정 내보냄",
    "Settings export failed":           "설정 내보내기 실패",
    "Settings imported":                "설정 가져옴",
    "Settings import failed":           "설정 가져오기 실패",
    "Update check completed":           "업데이트 확인 완료",
    "Update check failed":              "업데이트 확인 실패",
    "Benchmark failed":                 "벤치마크 실패",
    "AdGuard stopped (forced)":         "AdGuard 중지됨(강제)",
    "Could not stop AdGuard – process may still be running":
        "AdGuard 중지 실패 – 프로세스가 아직 실행 중일 수 있음",

    # ── main.py ───────────────────────────────────────────────────────────
    "adguard-cli could not be found on this system.\n\n"
    "Recommended install method (official):\n"
    "  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n"
    "Alternative (Arch Linux AUR):\n"
    "  paru -S adguard-cli-bin\n\n"
    "Tray loads, but start/stop won't work until adguard-cli is installed.":
        "이 시스템에서 adguard-cli를 찾을 수 없습니다.\n\n권장 설치 방법(공식):\n  curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v\n\n다른 방법(Arch Linux AUR):\n  paru -S adguard-cli-bin\n\n트레이는 실행되지만 adguard-cli를 설치하기 전에는 시작/중지가 작동하지 않습니다.",
    "Copy install command":             "설치 명령 복사",
    "Continue":                         "계속",
    "AdGuard Tray is already running":  "AdGuard Tray가 이미 실행 중",
    "Only one instance can run at a time. Check your system tray.":
        "한 번에 하나의 인스턴스만 실행할 수 있습니다. 시스템 트레이를 확인하세요.",
    "Authentication cancelled":         "인증 취소됨",
    "Authorization failed":             "인증 실패",
    "Check whether a site's certificate was revoked (OCSP).\nAdGuard checks asynchronously and lets the connection through if\nthe check is slow, so this rarely breaks a site – leave it on\nunless you have narrowed a problem down to it.":
        "사이트 인증서가 폐기되었는지 확인합니다(OCSP).\nAdGuard는 비동기로 확인하고 확인이 느리면 연결을 그대로\n허용하므로 이 기능 때문에 사이트가 안 열리는 일은 드뭅니다 –\n문제의 원인이 이 기능으로 좁혀진 경우가 아니면 켜 두세요.",
    "Enforce Certificate Transparency checks (Chrome's CT policy).\nSites whose own certificate is not CT-compliant stop being filtered\nand the browser may refuse them. Large sites are compliant, so try\nthis only for a site that reports a certificate error.":
        "인증서 투명성(Certificate Transparency) 검사를 강제 적용합니다(Chrome의 CT 정책).\n자체 인증서가 CT를 준수하지 않는 사이트는 더 이상 필터링되지 않으며\n브라우저가 접속을 거부할 수 있습니다. 대형 사이트는 CT를 준수하므로\n이 설정은 인증서 오류가 표시되는 사이트가 있을 때만 바꿔 보세요.",
    "Sites that don't load":
        "열리지 않는 사이트",
    "Turn off HTTP/3 filtering":
        "HTTP/3 필터링 끄기",
    "No filters installed":
        "설치된 필터 없음",
    "HTTP/3 is blocked by a firewall rule; browsers use HTTP/2.":
        "방화벽 규칙이 HTTP/3 연결을 차단하므로 브라우저는 HTTP/2를 사용합니다.",
    "Apps excluded from filtering (their HTTP/3 traffic is not filtered either): {}":
        "필터링에서 제외된 앱(HTTP/3 트래픽도 필터링되지 않음): {}",
    "AdGuard is not running – nothing is filtered.":
        "AdGuard가 실행 중이 아닙니다 – 아무것도 필터링되지 않습니다.",
    "could not remove the previous certificate":
        "이전 인증서를 제거하지 못함",
    "HTTP/3 state unknown":
        "HTTP/3 상태를 알 수 없음",
    "A firewall rule rejects outgoing UDP 443, so QUIC cannot be used.":
        "방화벽 규칙이 나가는 UDP 443 연결을 거부하므로 QUIC 프로토콜을 사용할 수 없습니다.",
    "Browser policy disables QUIC: {}":
        "브라우저 정책으로 QUIC 비활성화됨: {}",
    "Browsers can bypass AdGuard over HTTP/3 (UDP 443).":
        "브라우저가 HTTP/3(UDP 443) 연결로 AdGuard를 우회할 수 있습니다.",
    "Checking…":
        "확인 중…",
    "Could not read proxy.yaml – HTTP/3 state unknown.":
        "proxy.yaml 파일을 읽을 수 없습니다 – HTTP/3 상태를 알 수 없습니다.",
    "Firefox-family profiles with HTTP/3 switched off: {} of {}":
        "HTTP/3 설정을 끈 Firefox 계열 프로필: {}/{}",
    "HTTP/3 (QUIC)":
        "HTTP/3(QUIC)",
    "HTTP/3 is blocked by AdGuard; browsers fall back to filtered HTTP/2.":
        "AdGuard가 HTTP/3 연결을 차단하므로 브라우저는 필터링되는 HTTP/2로 전환합니다.",
    "HTTP/3 is filtered by AdGuard.":
        "AdGuard가 HTTP/3 트래픽을 필터링합니다.",
    "HTTP/3 switched off in Firefox profiles – restart the browser.":
        "Firefox 프로필에서 HTTP/3 설정을 껐습니다 – 브라우저를 다시 시작하세요.",
    "HTTPS filtering is off – nothing is filtered.":
        "HTTPS 필터링이 꺼져 있습니다 – 아무것도 필터링되지 않습니다.",
    "Proxy mode: {} – only traffic sent through the proxy is filtered, and browsers do not send QUIC through it.":
        "프록시 모드: {} – 프록시를 거치는 트래픽만 필터링되며, 브라우저는 QUIC 트래픽을 프록시로 보내지 않습니다.",
    "unknown":
        "알 수 없음",
    "AdGuard's certificate was not found. Generate it first.":
        "AdGuard 인증서를 찾을 수 없습니다. 먼저 인증서를 생성하세요.",
    "Certificate could not be installed in any browser.":
        "어떤 브라우저에도 인증서를 설치하지 못했습니다.",
    "Certificate installed for {} of {} stores.":
        "인증서 저장소 {1}개 중 {0}개에 인증서를 설치했습니다.",
    "Chromium-based browsers":
        "Chromium 기반 브라우저",
    "No browser certificate stores found.":
        "브라우저 인증서 저장소를 찾을 수 없습니다.",
    "Restart your browsers for the certificate to take effect.":
        "인증서를 적용하려면 브라우저를 다시 시작하세요.",
    "Run this without sudo/pkexec – it installs into your own browser profiles":
        "sudo/pkexec 없이 실행하세요 – 현재 사용자의 브라우저 프로필에 설치됩니다",
    "certificate not found after import":
        "가져온 후 인증서를 찾을 수 없음",
    "certutil not found – install the 'nss' package":
        "certutil을 찾을 수 없음 – “nss” 패키지를 설치하세요",
    "not found":
        "찾을 수 없음",
    "Could not read the filter list (unexpected CLI output).":
        "필터 목록을 읽을 수 없습니다(예상하지 못한 CLI 출력).",
    "No system tray found. AdGuard Tray is running without an icon — enable a tray/AppIndicator in your panel.":
        "시스템 트레이를 찾을 수 없습니다. AdGuard Tray가 아이콘 없이 실행 중입니다 — 패널에서 트레이/AppIndicator를 활성화하세요.",
    "URL must start with http:// or https://":
        "URL은 http:// 또는 https://로 시작해야 합니다",
    "adguard-cli path does not exist or is not executable.":
        "adguard-cli 경로가 존재하지 않거나 실행 가능한 파일이 아닙니다.",
    "That binary does not identify as adguard-cli. Save anyway?":
        "이 실행 파일은 adguard-cli로 확인되지 않습니다. 그래도 저장하시겠습니까?",
    "Update channel":                   "업데이트 채널",
    "Switching update channel to {}…":  "업데이트 채널을 {} 채널로 전환 중…",
    "Update channel set to {}":         "업데이트 채널 설정됨: {}",
    "Could not set update channel":     "업데이트 채널 설정 실패",
    "Invalid channel: {}":              "잘못된 채널: {}",

    # ── Activity ──────────────────────────────────────────────────────────
    'No access log yet ({}). AdGuard writes it once it has filtered traffic; when it runs as a system service the log belongs to root and is not readable here.':
        "아직 액세스 로그가 없습니다({}). AdGuard는 트래픽을 필터링하면 로그를 기록합니다. 시스템 서비스로 실행되는 경우 로그 소유자가 root이므로 여기에서 읽을 수 없습니다.",
    'Cannot read the access log ({}): {}':
        "액세스 로그를 읽을 수 없습니다({}): {}",
    'Blocked':
        "차단됨",
    'Blocked only':
        "차단된 항목만",
    "Refresh":
        "새로고침",
    'Allow selected domain':
        "선택한 도메인 허용",
    'Block selected domain':
        "선택한 도메인 차단",
    'Activity':
        "활동",
    'Time':
        "시간",
    'Domain':
        "도메인",
    'Result':
        "결과",
    'Rule':
        "규칙",
    'Size':
        "크기",
    'Count':
        "횟수",
    'Could not read the access log.':
        "액세스 로그를 읽을 수 없습니다.",
    '{} lines not understood':
        "해석하지 못한 줄 {}개",
    'Not a valid domain: {}':
        "유효한 도메인이 아님: {}",
    'Source: {}':
        "출처: {}",
    'Allowed':
        "허용됨",
    'Added rule: {}':
        "추가한 규칙: {}",
    'Requests per hour, {} to {} · busiest hour: {}':
        "시간당 요청, {}~{} · 요청이 가장 많은 시간: {}",
    'Last 24 hours':
        "최근 24시간",
    'Last 7 days':
        "최근 7일",
    'Requests':
        "요청",
    'Traffic':
        "트래픽",

    # ── Application update ────────────────────────────────────────────────
    'Version {} is available (you have {}).':
        "새 버전이 있습니다: {} (현재 버전: {}).",
    'Application update':
        "앱 업데이트",
    'Check for update':
        "업데이트 확인",
    'Install update':
        "업데이트 설치",
    'Installing update…':
        "업데이트 설치 중…",
    'Restart now':
        "지금 다시 시작",
    'Later':
        "나중에",
    'You are running the latest version ({}).':
        "최신 버전을 사용 중입니다({}).",
    'Installation not recognised':
        "설치 방식을 알 수 없음",
    'Could not check for updates.':
        "업데이트를 확인하지 못했습니다.",
    'Update with: {}':
        "업데이트 명령: {}",
    'Installed with the AUR package {}':
        "AUR 패키지로 설치됨: {}",
    'Installed in {}':
        "설치 위치: {}",
    'Running from a source checkout':
        "소스 체크아웃에서 실행 중",
    'Version {} installed. Restart adguard-tray to use it.':
        "버전 {} 설치가 완료되었습니다. 새 버전을 사용하려면 adguard-tray를 다시 시작하세요.",
    'Unexpected answer from GitHub: {}':
        "GitHub의 예기치 않은 응답: {}",
    'Download failed: {}':
        "다운로드 실패: {}",
    'Could not unpack the download: {}':
        "다운로드 압축 해제 실패: {}",
    'This installation is managed elsewhere: {}':
        "이 설치는 다른 곳에서 관리됩니다: {}",
    'No permission to write to {}':
        "쓰기 권한 없음: {}",
    'GitHub returned {}.':
        "GitHub에서 {} 응답을 반환했습니다.",
    'No connection to GitHub: {}':
        "GitHub에 연결할 수 없음: {}",
    'The download does not contain adguard-tray.':
        "다운로드한 파일에 adguard-tray가 없습니다.",
    'The download says version {} instead of {} – aborted.':
        "다운로드한 파일의 버전이 다릅니다(받은 버전: {}, 예상 버전: {}) – 중단되었습니다.",
    'GitHub is rate limiting this address. Try again later.':
        "GitHub에서 이 주소의 요청 횟수를 제한하고 있습니다. 나중에 다시 시도하세요.",
    'The download is larger than expected – aborted.':
        "다운로드한 파일이 예상보다 큽니다 – 중단되었습니다.",
    'Update failed: {}':
        "업데이트 실패: {}",
    'The archive contains unexpected paths – aborted.':
        "아카이브에 예기치 않은 경로가 있습니다 – 중단되었습니다.",
    'Update failed and the old version could not be restored. Restore it from {} or reinstall with: {}':
        "업데이트에 실패했으며 이전 버전을 복원하지 못했습니다. 백업({})에서 복원하거나 다음 명령으로 다시 설치하세요: {}",
    'Last 30 days':
        "최근 30일",
    'All time':
        "전체 기간",
    'Modified':
        "수정됨",
    'Rules':
        "규칙",
    'Showing {} – show all':
        "{}만 표시 중 – 모두 표시",
    'history {}':
        "기록 {}",
    'Filter list ID: {}':
        "필터 목록 ID: {}",
    'App':
        "앱",
    'Protocol':
        "프로토콜",
    'Type':
        "유형",
    'Reset history':
        "기록 초기화",
    'Delete the stored history and read the log again.':
        "저장된 기록을 삭제하고 로그를 다시 읽습니다.",
    'Delete the stored history? Only what the log still holds can be read back.':
        "저장된 기록을 삭제하시겠습니까? 로그에 아직 남아 있는 항목만 다시 읽어 올 수 있습니다.",
    'History is not being updated: {}':
        "기록이 업데이트되지 않음: {}",

    # ── Manager redesign: pages, sidebar, apply bar ────────────────
    "1 unsaved change to AdGuard's settings":
        "AdGuard 설정에 저장하지 않은 변경 사항 1개",
    "A trusted filter can run scripts in the pages you visit. Only trust lists from sources you know.":
        "신뢰할 수 있는 필터는 방문하는 페이지에서 스크립트를 실행할 수 있습니다. 출처를 아는 목록만 신뢰하세요.",
    "About":
        "정보",
    "Actions for the selected filter":
        "선택한 필터에 대한 작업",
    "Ad blocking":
        "광고 차단",
    "Ad blocking is off, so the filter lists below have no effect.":
        "광고 차단이 꺼져 있어 아래 필터 목록이 적용되지 않습니다.",
    "AdGuard CLI":
        "AdGuard CLI",
    "AdGuard CLI downloads and installs its newest build.":
        "AdGuard CLI가 최신 빌드를 다운로드하여 설치합니다.",
    "AdGuard CLI forgets the license on this computer. You will have to activate it again.":
        "AdGuard CLI가 이 컴퓨터에서 라이선스 정보를 삭제합니다. 라이선스를 다시 활성화해야 합니다.",
    "AdGuard CLI logs":
        "AdGuard CLI 로그",
    "AdGuard CLI update finished.":
        "AdGuard CLI 업데이트가 완료되었습니다.",
    "AdGuard Tray":
        "AdGuard Tray",
    "AdGuard Tray log":
        "AdGuard Tray 로그",
    "AdGuard doesn't filter these websites.":
        "AdGuard는 이 웹사이트를 필터링하지 않습니다.",
    "AdGuard is filtering this computer's traffic.":
        "AdGuard가 이 컴퓨터의 트래픽을 필터링하고 있습니다.",
    "AdGuard restarts to load the new lists.":
        "새 목록을 불러오기 위해 AdGuard가 다시 시작됩니다.",
    "AdGuard's reply did not say whether it is running.":
        "AdGuard의 응답에 실행 여부가 나와 있지 않습니다.",
    "AdGuard's settings file was not found ({}). Run adguard-cli once to create it.":
        "AdGuard 설정 파일을 찾을 수 없습니다({}). 설정 파일을 만들려면 adguard-cli를 한 번 실행하세요.",
    "Add DNS filter by ID":
        "ID로 DNS 필터 추가",
    "Add DNS filter from URL":
        "URL에서 DNS 필터 추가",
    "Add filter":
        "필터 추가",
    "Add filter by ID":
        "ID로 필터 추가",
    "Add filter from URL":
        "URL에서 필터 추가",
    "Add rule":
        "규칙 추가",
    "Add to browsers":
        "브라우저에 추가",
    "Add userscript":
        "사용자 스크립트 추가",
    "Add userscript…":
        "사용자 스크립트 추가…",
    "Add website":
        "웹사이트 추가",
    "Add…":
        "추가…",
    "Advanced":
        "고급",
    "All available":
        "사용 가능한 전체",
    "Allow {}":
        "{} 허용",
    "Also adds the certificate to this Firefox profile.":
        "이 Firefox 프로필에도 인증서를 추가합니다.",
    "Also on restarts and errors. Needs notify-send (libnotify) or a running notification service such as dunst, mako or KDE's.":
        "다시 시작하거나 오류가 발생할 때도 알립니다. notify-send(libnotify) 또는 실행 중인 알림 서비스(dunst, mako, KDE 알림 서비스 등)가 필요합니다.",
    "Appearance":
        "모양",
    "Applies after AdGuard Tray restarts.":
        "AdGuard Tray를 다시 시작한 후 적용됩니다.",
    "Apply":
        "적용",
    "Apply your changes to AdGuard's settings before closing?":
        "닫기 전에 AdGuard 설정의 변경 사항을 적용하시겠습니까?",
    "Applying them restarts AdGuard if protection is on.":
        "보호가 켜져 있으면 적용할 때 AdGuard가 다시 시작됩니다.",
    "Asks GitHub for the newest release.":
        "GitHub에서 최신 릴리스를 확인합니다.",
    "At a glance":
        "한눈에 보기",
    "Automatic":
        "자동",
    "Automatic – filter all apps":
        "자동 – 모든 앱 필터링",
    "Benchmark":
        "벤치마크",
    "Beta":
        "베타",
    "Block ECH in DNS records":
        "DNS 레코드의 ECH 차단",
    "Block domains before a connection is made.":
        "연결이 이루어지기 전에 도메인을 차단합니다.",
    "Block {}":
        "{} 차단",
    "Blocked (24 h)":
        "차단됨(24시간)",
    "Browser list ({})":
        "브라우저 목록({})",
    "By ID or name…":
        "ID 또는 이름으로…",
    "Certificate":
        "인증서",
    "Certificate checks":
        "인증서 검사",
    "Changes are collected in the bar at the bottom and applied together.":
        "변경 사항은 아래쪽 막대에 모였다가 한꺼번에 적용됩니다.",
    "Check again":
        "다시 확인",
    "Check every":
        "확인 간격",
    "Chromium- and Firefox-based browsers keep their own certificate store.":
        "Chromium 및 Firefox 기반 브라우저는 자체 인증서 저장소를 사용합니다.",
    "Close":
        "닫기",
    "Controls which AdGuard CLI build “{}” installs.":
        "“{}” 실행 시 설치되는 AdGuard CLI 빌드를 정합니다.",
    "Could not add the rule.":
        "규칙을 추가하지 못했습니다.",
    "Could not open {}":
        "열 수 없음: {}",
    "Could not read {}":
        "읽을 수 없음: {}",
    "Could not refresh. Showing data from {}.":
        "새로고침하지 못했습니다. {} 기준 데이터를 표시합니다.",
    "Could not reset the history.":
        "기록을 초기화하지 못했습니다.",
    "Could not restart AdGuard.":
        "AdGuard를 다시 시작하지 못했습니다.",
    "Could not start protection.":
        "보호를 시작하지 못했습니다.",
    "Could not stop protection.":
        "보호를 중지하지 못했습니다.",
    "Create":
        "생성",
    "Create certificate":
        "인증서 생성",
    "Custom":
        "사용자 지정",
    "DNS filter lists":
        "DNS 필터 목록",
    "DNS filtering":
        "DNS 필터링",
    "DNS filtering is off, so these lists have no effect.":
        "DNS 필터링이 꺼져 있어 이 목록이 적용되지 않습니다.",
    "DNS servers":
        "DNS 서버",
    "Dark":
        "다크",
    "Default":
        "기본값",
    "Details":
        "자세히",
    "Discard":
        "버리기",
    "Don't filter":
        "필터링 안 함",
    "Don't trust":
        "신뢰 안 함",
    "Downloads and installs the newest AdGuard CLI build.":
        "최신 AdGuard CLI 빌드를 다운로드하여 설치합니다.",
    "Duration":
        "소요 시간",
    "Export…":
        "내보내기…",
    "Filter everything":
        "모두 필터링",
    "Filter in place":
        "직접 필터링",
    "Filtering":
        "필터링",
    "Follow system":
        "시스템 설정 따르기",
    "From URL…":
        "URL에서…",
    "Go to updates":
        "업데이트로 이동",
    "HTTP proxy: {}":
        "HTTP 프록시: {}",
    "HTTPS filtering":
        "HTTPS 필터링",
    "How much detail AdGuard Tray writes to its own log.":
        "AdGuard Tray가 자체 로그에 기록하는 정보의 상세 수준입니다.",
    "ID {}":
        "ID {}",
    "If a site doesn't load, turn off HTTP/3 filtering first. The other checks protect every site – turn them off only if that didn't help.":
        "사이트가 로드되지 않으면 먼저 HTTP/3 필터링을 끄세요. 나머지 검사는 모든 사이트를 보호합니다 – 그래도 해결되지 않을 때만 끄세요.",
    "Included":
        "포함됨",
    "Installed":
        "설치됨",
    "License":
        "라이선스",
    "Light":
        "라이트",
    "Logs":
        "로그",
    "MIT license":
        "MIT 라이선스",
    "Maintenance":
        "유지 관리",
    "Manual proxy":
        "수동 프록시",
    "Manual – only apps set to use the proxy":
        "수동 – 프록시를 사용하도록 설정된 앱만",
    "More":
        "더 보기",
    "Move down":
        "아래로 이동",
    "Move up":
        "위로 이동",
    "Network":
        "네트워크",
    "Nightly":
        "나이틀리",
    "No requests yet – AdGuard logs requests while protection is on.":
        "아직 요청 없음 – 보호가 켜져 있는 동안 AdGuard가 요청을 기록합니다.",
    "Not added":
        "추가되지 않음",
    "Nothing matches your search.":
        "검색 결과가 없습니다.",
    "Notify me when protection turns on or off":
        "보호가 켜지거나 꺼지면 알림",
    "Off":
        "사용 안 함",
    "Only affects browsers that use DoH or DoT. Off lets them bypass AdGuard's DNS filtering.":
        "DoH 또는 DoT를 사용하는 브라우저에만 적용됩니다. “사용 안 함”으로 설정하면 브라우저가 AdGuard의 DNS 필터링을 우회합니다.",
    "Open AdGuard Tray":
        "AdGuard Tray 열기",
    "Open exceptions":
        "예외 열기",
    "Open folder":
        "폴더 열기",
    "Open release page":
        "릴리스 페이지 열기",
    "Pages":
        "페이지",
    "Performance":
        "성능",
    "Protection":
        "보호",
    "Protection started.":
        "보호를 시작했습니다.",
    "Protection stopped.":
        "보호를 중지했습니다.",
    "Proxy mode":
        "프록시 모드",
    "Redirect to AdGuard's DNS":
        "AdGuard의 DNS로 리디렉션",
    "Refresh this page (F5)":
        "이 페이지 새로고침(F5)",
    "Release (stable)":
        "릴리스(안정)",
    "Remove rule":
        "규칙 제거",
    "Remove “{}”?":
        "“{}” 항목을 제거하시겠습니까?",
    "Remove…":
        "제거…",
    "Replace the current AdGuard settings with the ones in {}?\n\nAdGuard restarts to apply them.":
        "{} 파일의 설정으로 현재 AdGuard 설정을 바꾸시겠습니까?\n\nAdGuard가 다시 시작되어 설정이 적용됩니다.",
    "Reset history…":
        "기록 초기화…",
    "Reset…":
        "초기화…",
    "Restart AdGuard":
        "AdGuard 다시 시작",
    "Rules apply only in automatic proxy mode. The first matching rule wins, so keep \"*\" last.":
        "규칙은 자동 프록시 모드에서만 적용됩니다. 처음 일치하는 규칙이 우선하므로 \"*\" 규칙은 맨 마지막에 두세요.",
    "Safe Browsing":
        "브라우징 보안",
    "Save anyway":
        "그래도 저장",
    "Saved. AdGuard restarts to apply the change.":
        "저장했습니다. AdGuard가 다시 시작되어 변경 사항이 적용됩니다.",
    "Saved. Applies after AdGuard Tray restarts.":
        "저장했습니다. AdGuard Tray를 다시 시작한 후 적용됩니다.",
    "Saved. The change applies when protection is turned on.":
        "저장했습니다. 보호를 켜면 변경 사항이 적용됩니다.",
    "Secure DNS and ECH":
        "보안 DNS 및 ECH",
    "Secure DNS filtering":
        "보안 DNS 필터링",
    "Set the path in Settings":
        "“설정”에서 경로를 지정하세요",
    "Settings":
        "설정",
    "Show":
        "표시",
    "Show recent entries":
        "최근 항목 표시",
    "Skip HTTPS filtering":
        "HTTPS 필터링 건너뛰기",
    "Some counts could not be loaded.":
        "일부 통계를 불러오지 못했습니다.",
    "Source code":
        "소스 코드",
    "Start AdGuard Tray when I log in":
        "로그인할 때 AdGuard Tray 시작",
    "Startup":
        "시작",
    "Status checks":
        "상태 확인",
    "Stealth mode":
        "스텔스 모드",
    "System":
        "시스템",
    "The new lists load when protection is turned on.":
        "보호를 켜면 새 목록을 불러옵니다.",
    "Theme":
        "테마",
    "This turns off HTTP/3 filtering, OCSP checks, Certificate Transparency and secure DNS filtering. Revoked or mis-issued certificates then go unnoticed, and browsers can resolve past AdGuard's DNS filter.":
        "HTTP/3 필터링, OCSP 검사, 인증서 투명성(Certificate Transparency), 보안 DNS 필터링이 꺼집니다. 그러면 폐기되었거나 잘못 발급된 인증서를 알아차릴 수 없고, 브라우저가 AdGuard의 DNS 필터를 우회하여 이름을 확인할 수 있습니다.",
    "Time range":
        "기간",
    "To keep it but stop using it, switch it off instead.":
        "유지하면서 사용만 중지하려면 제거 대신 끄세요.",
    "Top lists":
        "상위 목록",
    "Trust":
        "신뢰",
    "Trust “{}”?":
        "“{}” 필터를 신뢰하시겠습니까?",
    "Trust…":
        "신뢰…",
    "Turn off all strict checks…":
        "모든 엄격한 검사 끄기…",
    "Undo":
        "되돌리기",
    "Unknown":
        "알 수 없음",
    "Unsaved changes":
        "저장하지 않은 변경 사항",
    "Update AdGuard CLI…":
        "AdGuard CLI 업데이트…",
    "Update channel: {}":
        "업데이트 채널: {}",
    "Updated {}":
        "업데이트: {}",
    "Updates":
        "업데이트",
    "Used in manual mode only.":
        "수동 모드에서만 사용됩니다.",
    "Userscripts update together with filters.":
        "사용자 스크립트는 필터와 함께 업데이트됩니다.",
    "Uses XDG autostart (~/.config/autostart).":
        "XDG 자동 시작(~/.config/autostart)을 사용합니다.",
    "Waiting for authorization…":
        "인증 대기 중…",
    "Website exceptions":
        "웹사이트 예외",
    "Websites":
        "웹사이트",
    "example.com or a link":
        "example.com 또는 링크",
    "expires {}":
        "만료일: {}",
    "of {} requests in the last 24 hours":
        "최근 24시간 요청 {}건 중",
    "{} of {} DNS filters on":
        "켜진 DNS 필터 {}/{}",
    "{} of {} filters on":
        "켜진 필터 {}/{}",
    "{} of {} on":
        "{}/{} 켜짐",
    "{} unsaved changes to AdGuard's settings":
        "AdGuard 설정에 저장하지 않은 변경 사항 {}개",
    "“Follow system” uses your desktop's light or dark setting.":
        "“시스템 설정 따르기”는 데스크톱의 라이트 또는 다크 설정을 사용합니다.",

    # ── Manager redesign, second round ─────────────────────────────
    "Active":
        "활성",
    "AdGuard's certificate will be added to every browser profile found on this system.\n\nThis allows AdGuard to inspect HTTPS traffic in those browsers. Close your browsers first – they read the certificate store at startup.":
        "이 시스템에서 찾은 모든 브라우저 프로필에 AdGuard 인증서가 추가됩니다.\n\n이렇게 하면 AdGuard가 해당 브라우저의 HTTPS 트래픽을 검사할 수 있습니다. 먼저 브라우저를 닫으세요 – 브라우저는 시작할 때 인증서 저장소를 읽습니다.",
    "Allow":
        "허용",
    "Apply or discard your changes to AdGuard's settings first, then restart.":
        "먼저 AdGuard 설정의 변경 사항을 적용하거나 버린 후 다시 시작하세요.",
    "Automatic: AdGuard redirects all app traffic to itself via iptables. Manual: AdGuard only listens on the SOCKS5 and HTTP ports below.":
        "자동: AdGuard가 iptables를 사용해 모든 앱 트래픽을 AdGuard로 리디렉션합니다. 수동: AdGuard가 아래의 SOCKS5 및 HTTP 포트에서만 수신합니다.",
    "Block":
        "차단",
    "Browser API blocking":
        "브라우저 API 차단",
    "CRLite":
        "CRLite",
    "Cancel":
        "취소",
    "Computers":
        "컴퓨터",
    "Could not change the autostart entry.":
        "자동 시작 항목을 변경하지 못했습니다.",
    "Could not export the logs.":
        "로그를 내보내지 못했습니다.",
    "Could not export the settings.":
        "설정을 내보내지 못했습니다.",
    "Could not reset the license.":
        "라이선스를 초기화하지 못했습니다.",
    "Could not retrieve license info.":
        "라이선스 정보를 가져올 수 없습니다.",
    "Could not run the benchmark.":
        "벤치마크를 실행하지 못했습니다.",
    "Could not save the settings.":
        "설정을 저장하지 못했습니다.",
    "Could not set the update channel.":
        "업데이트 채널을 설정하지 못했습니다.",
    "Could not update AdGuard CLI.":
        "AdGuard CLI를 업데이트하지 못했습니다.",
    "Could not update the filters.":
        "필터를 업데이트하지 못했습니다.",
    "DNS upstream server.\n'default' = system DNS.\nExamples: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com":
        "업스트림 DNS 서버입니다.\n'default' = 시스템 DNS.\n예: 1.1.1.1, https://dns.google/dns-query,\ntls://dns.adguard.com, quic://dns.adguard.com",
    "Expiration date":
        "만료일",
    "Expires":
        "만료",
    "HTTP/3 turned back on in Firefox profiles – restart the browser.":
        "Firefox 프로필에서 HTTP/3을 다시 켰습니다 – 브라우저를 다시 시작하세요.",
    "License key":
        "라이선스 키",
    "License type":
        "라이선스 유형",
    "Manual":
        "수동",
    "No exceptions.":
        "예외가 없습니다.",
    "OK":
        "확인",
    "On: AdGuard filters HTTP/3 (QUIC) itself – experimental, and some\nbrowsers refuse HTTP/3 through a user-installed certificate anyway.\nOff: AdGuard blocks QUIC instead, so browsers fall back to HTTP/2,\nwhich is filtered reliably.\nEither way this only applies in automatic mode – in manual mode\nHTTP/3 traffic never reaches AdGuard.":
        "켜짐: AdGuard가 HTTP/3(QUIC)을 직접 필터링합니다 – 실험적 기능이며, 일부\n브라우저는 사용자가 설치한 인증서를 통한 HTTP/3 연결을 어차피 거부합니다.\n꺼짐: AdGuard가 대신 QUIC을 차단하므로 브라우저가 HTTP/2로 전환하며,\nHTTP/2는 안정적으로 필터링됩니다.\n어느 쪽이든 자동 모드에서만 적용됩니다 – 수동 모드에서는\nHTTP/3 트래픽이 AdGuard에 전혀 도달하지 않습니다.",
    "Owner":
        "소유자",
    "Personal":
        "개인용",
    "Proxy mode: {} – UDP port 443 is redirected to AdGuard.":
        "프록시 모드: {} – UDP 포트 443이 AdGuard로 리디렉션됩니다.",
    "Save adguard-cli path":
        "adguard-cli 경로 저장",
    "Search domains or rules…":
        "도메인 또는 규칙 검색…",
    "Settings file":
        "설정 파일",
    "Status":
        "상태",
    "Trial":
        "체험판",
    "Turn HTTP/3 back on in Firefox profiles":
        "Firefox 프로필에서 HTTP/3 다시 켜기",
    "Turn off":
        "끄기",
    "Turn off HTTP/3 in Firefox profiles":
        "Firefox 프로필에서 HTTP/3 끄기",
    "Turn off HTTP/3 in Firefox profiles…":
        "Firefox 프로필에서 HTTP/3 끄기…",
    "Turn off HTTP/3 in {} Firefox-family profile(s)?\n\nTheir traffic then uses HTTP/2, which AdGuard can filter. Restart the browser afterwards.":
        "Firefox 계열 프로필 {}개에서 HTTP/3을 끄시겠습니까?\n\n그러면 해당 트래픽은 AdGuard가 필터링할 수 있는 HTTP/2를 사용합니다. 완료 후 브라우저를 다시 시작하세요.",
    "Turn off all strict checks":
        "모든 엄격한 검사 끄기",
    "Unavailable until AdGuard CLI reports its current channel.":
        "AdGuard CLI가 현재 채널을 알려 줄 때까지 사용할 수 없습니다.",
    "Update AdGuard CLI":
        "AdGuard CLI 업데이트",
    "Used in automatic mode only. Ranges (80:5221,5300:49151) or single ports (80,443,8080).":
        "자동 모드에서만 사용됩니다. 범위(80:5221,5300:49151) 또는 개별 포트(80,443,8080)를 입력하세요.",
    "{} of {}":
        "{}/{}",
    "{} of {} userscripts on":
        "켜진 사용자 스크립트 {}/{}",
    "{}% blocked":
        "{}% 차단됨",

    # ── Printed by adguard-cli and looked up at runtime (filter groups, licence) ──
    "Annoyances":
        "방해 요소",
    "General":
        "일반",
    "Language-specific":
        "특정 언어",
    "Security":
        "보안",
    "Social widgets":
        "소셜 위젯",
    "Expired":
        "만료됨",
    "Autostart on login":
        "로그인 시 자동 시작",
    "Add app rule":
        "앱 규칙 추가",
    "Wildcards work, e.g. *steam* or *EasyAntiCheat*.":
        "와일드카드를 쓸 수 있습니다(예: *steam*, *EasyAntiCheat*).",
    "There is already a rule for '{}'.":
        "“{}”에 대한 규칙이 이미 있습니다.",
    "AdGuard settings":
        "AdGuard 설정",
    "Ads and trackers are not blocked until you enable protection.":
        "보호를 활성화해야 광고와 추적기가 차단됩니다.",
    "Could not import the settings.":
        "설정을 가져오지 못했습니다.",
    "Disable protection":
        "보호 비활성화",
    "Enable protection":
        "보호 활성화",
    "Export and import":
        "내보내기 및 가져오기",
    "Features":
        "기능",
    "Import settings":
        "설정 가져오기",
    "Import settings from…":
        "설정을 가져올 파일 선택…",
    "Import settings…":
        "설정 가져오기…",
    "Import…":
        "가져오기…",
    "Save filters, rules and configuration to a zip file, or load them from one.":
        "필터, 규칙, 구성을 zip 파일로 저장하거나 zip 파일에서 불러옵니다.",
    "Update":
        "업데이트",
    "Version":
        "버전",
    "{} is not a settings export. Choose a file saved with Export under AdGuard settings.":
        "{} 파일은 내보낸 설정 파일이 아닙니다. “AdGuard 설정”의 “내보내기”로 저장한 파일을 선택하세요.",
}
