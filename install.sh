#!/usr/bin/env bash
# AdGuard Tray – installer for Arch, Fedora, Debian/Ubuntu and openSUSE
# Run as normal user (sudo is used only where needed).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_PREFIX="${HOME}/.local"
BIN_DIR="${INSTALL_PREFIX}/bin"
LIB_DIR="${INSTALL_PREFIX}/lib/adguard-tray"
DESKTOP_DIR="${HOME}/.local/share/applications"

# ── Colour helpers ─────────────────────────────────────────────────────────
green()  { printf '\033[1;32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[1;33m%s\033[0m\n' "$*"; }
red()    { printf '\033[1;31m%s\033[0m\n' "$*"; }
info()   { printf '  → %s\n' "$*"; }

# ── Uninstall ──────────────────────────────────────────────────────────────
if [[ "${1:-}" == "--uninstall" ]]; then
    green "==> Removing adguard-tray"
    # Anchored so a wrapper that merely mentions the command (a debugger,
    # bash -c) is left alone; the path prefix covers /usr/bin/python3 launchers.
    pkill -f "^([^[:space:]]*/)?python3 ${LIB_DIR}/adguard-tray\.py" 2>/dev/null || true
    rm -rf "${LIB_DIR}"
    rm -f "${BIN_DIR}/adguard-tray"
    rm -f "${DESKTOP_DIR}/adguard-tray.desktop"
    rm -f "${HOME}/.config/autostart/adguard-tray.desktop"
    update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
    info "removed application, launcher, desktop entry and autostart"
    info "kept: ~/.config/adguard-tray (settings), ~/.local/share/adguard-tray (logs)"
    green "✓ Uninstalled"
    exit 0
fi

# ── 1. Dependency check ────────────────────────────────────────────────────
green "==> Checking dependencies"

# One interpreter for the checks and for the launcher. The distro packages go
# into /usr/bin/python3; a venv or pyenv first on PATH would otherwise pass the
# checks here and then be missing when the tray starts at login.
pick_python() {
    if [[ -x /usr/bin/python3 ]]; then PYTHON=/usr/bin/python3
    else PYTHON="$(command -v python3 || echo python3)"; fi
}
pick_python

# Checked by what the app needs rather than by package name: the names differ
# per distro, and an installed package does not always mean the piece is there
# (openSUSE's polkit ships no pkexec, and its python3-PyQt6 pulls in a Python
# without sqlite3).
check_deps() {
    local ok=0
    if "$PYTHON" -c 'import PyQt6.QtWidgets' &>/dev/null; then info "PyQt6 ✓"; else yellow "  PyQt6 missing"; ok=1; fi
    if "$PYTHON" -c 'import yaml' &>/dev/null; then info "PyYAML ✓"; else yellow "  PyYAML missing"; ok=1; fi
    if "$PYTHON" -c 'import sqlite3' &>/dev/null; then info "sqlite3 ✓"; else yellow "  Python sqlite3 module missing"; ok=1; fi
    # Without Qt's SVG image plugin the Manager's sidebar has no icons.
    if "$PYTHON" -c 'import sys; from PyQt6.QtGui import QImageReader
sys.exit(b"svg" not in [bytes(f) for f in QImageReader.supportedImageFormats()])' &>/dev/null; then
        info "Qt SVG plugin ✓"; else yellow "  Qt SVG image plugin missing"; ok=1; fi
    if command -v pkexec &>/dev/null; then info "pkexec ✓"; else yellow "  pkexec (polkit) missing"; ok=1; fi
    if command -v notify-send &>/dev/null; then info "notify-send ✓"; else yellow "  notify-send (libnotify) missing"; ok=1; fi
    return "$ok"
}

# The distro comes from os-release, not from whichever tool happens to exist:
# Debian and Ubuntu package an arcade game as /usr/games/pacman.
distro_family() {
    local id="" like="" file=/etc/os-release
    [[ -r "$file" ]] || file=/usr/lib/os-release
    if [[ -r "$file" ]]; then
        # shellcheck source=/dev/null
        id="$(. "$file" && echo "${ID:-}")"
        # shellcheck source=/dev/null
        like="$(. "$file" && echo "${ID_LIKE:-}")"
    fi
    # Enterprise releases claim Fedora or openSUSE ancestry but ship an older
    # Python and none of these package names; guessing there would only
    # produce a failing command.
    case "$id" in
        rhel|centos|rocky|almalinux|ol|sles|sled|sles_sap) echo unknown; return ;;
    esac
    case " ${id} ${like} " in
        *" arch "*)                             echo arch ;;
        *" fedora "*)                           echo fedora ;;
        *" debian "*|*" ubuntu "*)              echo debian ;;
        *" suse "*|*" opensuse "*|*opensuse-*)  echo suse ;;
        *)                                      echo unknown ;;
    esac
}

FAMILY="$(distro_family)"
case "$FAMILY" in
    arch)   PKGS=(python-pyqt6 qt6-svg python-yaml polkit libnotify)
            INSTALL=(pacman -S --needed --noconfirm) ;;
    fedora) PKGS=(python3 python3-pyqt6-base qt6-qtsvg python3-pyyaml polkit libnotify)
            INSTALL=(dnf install -y) ;;
    debian) PKGS=(python3 python3-pyqt6 libqt6svg6 python3-yaml pkexec libnotify-bin)
            INSTALL=(apt-get install -y) ;;
    suse)   PKGS=(python3 python3-PyQt6 libQt6Svg6 python3-PyYAML pkexec libnotify-tools)
            INSTALL=(zypper --non-interactive install) ;;
    *)      PKGS=(); INSTALL=() ;;
esac

as_root() {
    if [[ ${EUID} -eq 0 ]]; then
        "$@"
    elif command -v sudo &>/dev/null; then
        sudo "$@"
    else
        return 127
    fi
}

manual_hint() {
    red "  Install the missing pieces yourself, then run this script again:"
    if [[ ${#PKGS[@]} -gt 0 ]]; then
        local prefix="sudo "
        [[ ${EUID} -eq 0 ]] && prefix=""
        [[ "$FAMILY" == debian ]] && red "    ${prefix}apt-get update"
        red "    ${prefix}${INSTALL[*]} ${PKGS[*]}"
        [[ ${EUID} -ne 0 ]] && ! command -v sudo &>/dev/null && red "  (as root – sudo is not installed)"
    else
        red "    Python 3.11 or newer with its sqlite3 module, PyQt6 (with Qt's SVG plugin) and PyYAML,"
        red "    polkit (pkexec) and libnotify (notify-send)"
    fi
    return 0
}

python_too_old() {
    [[ -x "$PYTHON" ]] || command -v "$PYTHON" &>/dev/null || return 1
    ! "$PYTHON" -c 'import sys; sys.exit(sys.version_info < (3, 11))' &>/dev/null
}

if python_too_old; then
    red "  Python 3.11 or newer is required, found: $("$PYTHON" --version 2>&1)"
    exit 1
fi

if ! check_deps; then
    if [[ ${#PKGS[@]} -eq 0 ]]; then
        red "  This distribution is not recognised, so nothing was installed."
        manual_hint
        exit 1
    fi
    if [[ -e /run/ostree-booted ]]; then
        # Fedora Kinoite/Silverblue: /usr is read-only, dnf cannot change it.
        red "  This is an image-based system; packages are layered with rpm-ostree:"
        red "    rpm-ostree install ${PKGS[*]}"
        red "  Reboot afterwards, then run this script again."
        exit 1
    fi
    yellow "  Installing: ${PKGS[*]}"
    installed=0
    if [[ "$FAMILY" == debian ]]; then
        as_root apt-get update && as_root "${INSTALL[@]}" "${PKGS[@]}" && installed=1
    else
        as_root "${INSTALL[@]}" "${PKGS[@]}" && installed=1
    fi
    if [[ $installed -eq 0 ]]; then
        red "  Could not install the packages – the output above says why."
        manual_hint
        exit 1
    fi
    pick_python
    if ! check_deps; then
        red "  Still missing after installing (checked with ${PYTHON})."
        exit 1
    fi
fi

if python_too_old || ! "$PYTHON" -c '' &>/dev/null; then
    red "  Python 3.11 or newer is required, found: $("$PYTHON" --version 2>&1)"
    exit 1
fi

if ! command -v adguard-cli &>/dev/null; then
    red "  WARNING: adguard-cli not found."
    red "  Install via official script:"
    red "    curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v"
    if [[ "$FAMILY" == arch ]]; then
        red "  Or via AUR:  paru -S adguard-cli-bin"
    fi
    echo ""
fi

# ── 2. Install application files ───────────────────────────────────────────
if [[ -f "${LIB_DIR}/adguard-tray.py" ]]; then
    info "Existing installation detected in ${LIB_DIR} – upgrading"
fi

green "==> Installing application to ${LIB_DIR}"

mkdir -p "${LIB_DIR}" "${BIN_DIR}" "${DESKTOP_DIR}"

# Clean previous install to avoid stale files
rm -rf "${LIB_DIR}/adguard_tray"

# Copy package
cp -r "${SCRIPT_DIR}/adguard_tray" "${LIB_DIR}/"
cp "${SCRIPT_DIR}/adguard-tray.py" "${LIB_DIR}/"

# ── 3. Create launcher script ──────────────────────────────────────────────
green "==> Creating launcher ${BIN_DIR}/adguard-tray"

cat > "${BIN_DIR}/adguard-tray" << EOF
#!/usr/bin/env bash
exec "${PYTHON}" "${LIB_DIR}/adguard-tray.py" "\$@"
EOF
chmod +x "${BIN_DIR}/adguard-tray"

# ── 4. Desktop entry ────────────────────────────────────────────────────────
green "==> Installing .desktop entry"

sed "s|Exec=.*|Exec=${BIN_DIR}/adguard-tray|" \
    "${SCRIPT_DIR}/adguard-tray.desktop" \
    > "${DESKTOP_DIR}/adguard-tray.desktop"

update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true

# ── 5. PATH hint ───────────────────────────────────────────────────────────
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
    yellow ""
    yellow "  NOTE: ${BIN_DIR} is not in your PATH."
    yellow "  Add the following to ~/.config/fish/config.fish:"
    yellow "    fish_add_path ${BIN_DIR}"
    yellow "  Or for bash/zsh add to ~/.bashrc / ~/.zshrc:"
    yellow "    export PATH=\"\$PATH:${BIN_DIR}\""
fi

# ── Done ───────────────────────────────────────────────────────────────────
echo ""
green "✓ Installation complete"
echo ""
echo "  Run:        adguard-tray"
echo "  Uninstall:  bash install.sh --uninstall"
echo "  Direct:     ${PYTHON} ${LIB_DIR}/adguard-tray.py"
echo "  Log:        ~/.local/share/adguard-tray/adguard-tray.log"
echo "  Config:     ~/.config/adguard-tray/config.json"
echo ""
echo "  Autostart via KDE System Settings or:"
echo "  Settings menu in the tray icon → enable Autostart"
echo ""
