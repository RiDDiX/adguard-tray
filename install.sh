#!/usr/bin/env bash
# AdGuard Tray – Arch Linux installer
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

# ── 1. Dependency check ────────────────────────────────────────────────────
green "==> Checking dependencies"

if ! pacman -Qi python-pyqt6 &>/dev/null; then
    yellow "  python-pyqt6 not found – installing..."
    sudo pacman -S --needed --noconfirm python-pyqt6
else
    info "python-pyqt6 ✓"
fi

if ! command -v notify-send &>/dev/null; then
    yellow "  libnotify (notify-send) not found – installing..."
    sudo pacman -S --needed --noconfirm libnotify
else
    info "notify-send ✓"
fi

if ! command -v adguard-cli &>/dev/null; then
    red "  WARNING: adguard-cli not found."
    red "  Install via official script:"
    red "    curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v"
    red "  Or via AUR:  paru -S adguard-cli-bin"
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
exec python3 "${LIB_DIR}/adguard-tray.py" "\$@"
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
green "✓ Installation complete!"
echo ""
echo "  Run:        adguard-tray"
echo "  Direct:     python3 ${LIB_DIR}/adguard-tray.py"
echo "  Log:        ~/.local/share/adguard-tray/adguard-tray.log"
echo "  Config:     ~/.config/adguard-tray/config.json"
echo ""
echo "  Autostart via KDE System Settings or:"
echo "  Settings menu in the tray icon → enable Autostart"
echo ""
