"""XDG autostart entry for adguard-tray (~/.config/autostart/adguard-tray.desktop)."""

import logging
import shlex
from pathlib import Path

from ._allowlist import write_atomic

logger = logging.getLogger(__name__)

AUTOSTART_DIR = Path.home() / ".config" / "autostart"
AUTOSTART_FILE = AUTOSTART_DIR / "adguard-tray.desktop"


def autostart_enabled() -> bool:
    """True when the XDG autostart entry exists and isn't disabled in place.

    KDE's and GNOME's autostart tools keep the file and set Hidden=true /
    X-GNOME-Autostart-enabled=false instead of deleting it.
    """
    try:
        text = AUTOSTART_FILE.read_text(encoding="utf-8")
    except (OSError, ValueError):
        return False
    lowered = text.lower()
    return "hidden=true" not in lowered and "x-gnome-autostart-enabled=false" not in lowered


def set_autostart(enable: bool, exec_path) -> tuple[bool, str]:
    """Create or remove the entry. Returns (ok, error) so the UI can say why."""
    try:
        if enable:
            AUTOSTART_DIR.mkdir(parents=True, exist_ok=True)
            # Atomic: a half-written entry would still count as "enabled".
            write_atomic(AUTOSTART_FILE, desktop_entry(exec_path))
            logger.info("Autostart entry created: %s", AUTOSTART_FILE)
        else:
            AUTOSTART_FILE.unlink(missing_ok=True)
            logger.info("Autostart entry removed")
        return True, ""
    except OSError as exc:
        logger.error("Could not %s the autostart entry: %s", "create" if enable else "remove", exc)
        return False, str(exc)


def _xdg_quote(arg: str) -> str:
    """Quote one Exec argument per the XDG Desktop Entry spec."""
    if not arg or any(c in arg for c in ' \t"\'\\><~|&;$*?#()`'):
        escaped = arg.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$").replace("`", "\\`")
        return f'"{escaped}"'
    return arg


def desktop_entry(exec_path) -> str:
    """Autostart entry for *exec_path* (a string or an argv list).

    Exec arguments are quoted per the XDG spec, and TryExec points at the
    script rather than the interpreter, so the desktop skips a stale entry
    instead of failing silently at every login.
    """
    if isinstance(exec_path, str):
        try:
            parts = shlex.split(exec_path) or [exec_path]
        except ValueError:  # unbalanced quotes – treat it as one path
            parts = [exec_path]
    else:
        parts = list(exec_path) or [""]
    # "python3 /path/app.py" → check the script, not the interpreter
    tryexec = parts[1] if len(parts) > 1 and parts[0].endswith(("python", "python3")) else parts[0]
    return _DESKTOP_TEMPLATE.format(
        exec=" ".join(_xdg_quote(p) for p in parts), tryexec=tryexec
    )


_DESKTOP_TEMPLATE = """\
[Desktop Entry]
Type=Application
Name=AdGuard Tray
GenericName=AdGuard CLI Monitor
GenericName[de]=AdGuard CLI Überwachung
GenericName[zh_CN]=AdGuard CLI 监视器
GenericName[es]=Monitor de AdGuard CLI
GenericName[fr]=Moniteur AdGuard CLI
GenericName[it]=Monitor di AdGuard CLI
GenericName[ja]=AdGuard CLIモニター
GenericName[ko]=AdGuard CLI 모니터
GenericName[nl]=Monitor voor AdGuard CLI
GenericName[pl]=Monitor AdGuard CLI
GenericName[pt_BR]=Monitor do AdGuard CLI
GenericName[ru]=Монитор AdGuard CLI
GenericName[tr]=AdGuard CLI denetleyicisi
GenericName[uk]=Монітор AdGuard CLI
GenericName[zh_TW]=AdGuard CLI 監控工具
Comment=System tray monitor and controller for adguard-cli
Comment[de]=System tray Überwachung und Steuerung für adguard-cli
Comment[zh_CN]=adguard-cli 的系统托盘监视器和控制器
Comment[es]=Monitor y control de adguard-cli en la bandeja del sistema
Comment[fr]=Moniteur et contrôleur d’adguard-cli dans la zone de notification
Comment[it]=Monitor e controllo di adguard-cli nel vassoio di sistema
Comment[ja]=adguard-cliを監視・操作するシステムトレイアプリ
Comment[ko]=adguard-cli용 시스템 트레이 모니터 및 컨트롤러
Comment[nl]=Monitor en bediening voor adguard-cli in het systeemvak
Comment[pl]=Monitorowanie i sterowanie adguard-cli z tacki systemowej
Comment[pt_BR]=Monitor e controle do adguard-cli na bandeja do sistema
Comment[ru]=Мониторинг и управление adguard-cli из системного лотка
Comment[tr]=adguard-cli için sistem tepsisi izleme ve denetim aracı
Comment[uk]=Монітор і керування adguard-cli у системному лотку
Comment[zh_TW]=adguard-cli 的系統匣監控與控制工具
Exec={exec}
TryExec={tryexec}
Icon=security-high
Categories=Network;Security;System;
Keywords=adguard;dns;privacy;security;ad-blocker;filter;
Keywords[de]=adguard;dns;privatsphäre;sicherheit;werbeblocker;filter;steuerung
Keywords[zh_CN]=adguard;dns;隐私;安全;广告拦截;过滤器;控制器
Keywords[es]=adguard;dns;privacidad;seguridad;bloqueador de anuncios;filtro;control;
Keywords[fr]=adguard;dns;confidentialité;vie privée;sécurité;bloqueur de publicités;filtre;contrôleur;
Keywords[it]=adguard;dns;privacy;sicurezza;blocco annunci;adblock;filtro;controllo;
Keywords[ja]=adguard;dns;プライバシー;セキュリティ;広告ブロック;フィルタ;コントローラー;
Keywords[ko]=adguard;dns;개인정보 보호;보안;광고 차단;필터;컨트롤러;
Keywords[nl]=adguard;dns;privacy;beveiliging;advertentieblokker;adblocker;filter;bediening;
Keywords[pl]=adguard;dns;prywatność;bezpieczeństwo;blokowanie reklam;filtr;sterowanie;
Keywords[pt_BR]=adguard;dns;privacidade;segurança;bloqueador de anúncios;filtro;controle;
Keywords[ru]=adguard;dns;конфиденциальность;приватность;безопасность;блокировщик рекламы;фильтр;управление;
Keywords[tr]=adguard;dns;gizlilik;güvenlik;reklam engelleyici;filtre;denetleyici;
Keywords[uk]=adguard;dns;конфіденційність;безпека;блокувальник реклами;фільтр;керування;
Keywords[zh_TW]=adguard;dns;隱私;安全性;廣告封鎖;過濾器;控制器;
StartupNotify=false
X-GNOME-Autostart-enabled=true
"""
