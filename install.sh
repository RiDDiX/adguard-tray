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
green "==> Prüfe Abhängigkeiten"

if ! pacman -Qi python-pyqt6 &>/dev/null; then
    yellow "  python-pyqt6 nicht gefunden – wird installiert..."
    sudo pacman -S --needed --noconfirm python-pyqt6
else
    info "python-pyqt6 ✓"
fi

if ! command -v notify-send &>/dev/null; then
    yellow "  libnotify (notify-send) nicht gefunden – wird installiert..."
    sudo pacman -S --needed --noconfirm libnotify
else
    info "notify-send ✓"
fi

if ! command -v adguard-cli &>/dev/null; then
    red "  WARNUNG: adguard-cli nicht gefunden."
    red "  Installiere es zuerst:  paru -S adguard-cli-bin"
    echo ""
fi

# ── 2. Install application files ───────────────────────────────────────────
green "==> Installiere Anwendung nach ${LIB_DIR}"

mkdir -p "${LIB_DIR}" "${BIN_DIR}" "${DESKTOP_DIR}"

# Copy package
cp -r "${SCRIPT_DIR}/adguard_tray" "${LIB_DIR}/"
cp "${SCRIPT_DIR}/adguard-tray.py" "${LIB_DIR}/"

# ── 3. Create launcher script ──────────────────────────────────────────────
green "==> Erstelle Launcher ${BIN_DIR}/adguard-tray"

cat > "${BIN_DIR}/adguard-tray" << EOF
#!/usr/bin/env bash
exec python3 "${LIB_DIR}/adguard-tray.py" "\$@"
EOF
chmod +x "${BIN_DIR}/adguard-tray"

# ── 4. Desktop entry ────────────────────────────────────────────────────────
green "==> Installiere .desktop-Eintrag"

sed "s|Exec=.*|Exec=${BIN_DIR}/adguard-tray|" \
    "${SCRIPT_DIR}/adguard-tray.desktop" \
    > "${DESKTOP_DIR}/adguard-tray.desktop"

update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true

# ── 5. PATH hint ───────────────────────────────────────────────────────────
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
    yellow ""
    yellow "  HINWEIS: ${BIN_DIR} ist nicht in deinem PATH."
    yellow "  Füge folgendes zu ~/.config/fish/config.fish hinzu:"
    yellow "    fish_add_path ${BIN_DIR}"
    yellow "  Oder für bash/zsh zu ~/.bashrc / ~/.zshrc:"
    yellow "    export PATH=\"\$PATH:${BIN_DIR}\""
fi

# ── Done ───────────────────────────────────────────────────────────────────
echo ""
green "✓ Installation abgeschlossen!"
echo ""
echo "  Starten:    adguard-tray"
echo "  Direkt:     python3 ${LIB_DIR}/adguard-tray.py"
echo "  Log:        ~/.local/share/adguard-tray/adguard-tray.log"
echo "  Config:     ~/.config/adguard-tray/config.json"
echo ""
echo "  Autostart über KDE Systemeinstellungen oder:"
echo "  Einstellungen-Menü im Tray-Icon → Autostart aktivieren"
echo ""
