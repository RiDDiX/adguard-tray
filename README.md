# adguard-tray

System tray app for [adguard-cli](https://adguard.com/en/adguard-linux/overview.html) on Linux. Built because there was nothing decent for KDE Plasma or Hyprland — just a terminal and a service.

Works on Wayland and X11. Written in Python + PyQt6.

The UI language is detected automatically from the system locale. English is the default; German is included as an additional translation.

---

## What it does

- Shows AdGuard status in the tray (green = running, grey = stopped, red = error)
- Start / stop / restart from the tray menu
- Toggle individual filters without opening a terminal
- Search / filter in the filter and userscript management dialogs
- Manage userscripts (install, enable/disable, remove)
- Update all filters with one click
- Install custom filter lists by URL
- Desktop notifications when status changes (with dedup to prevent spam)
- Autostart toggle right in the tray menu
- `--version` / `-V` flag

---

## Requirements

- `python` >= 3.11
- `python-pyqt6`
- `libnotify` (for notifications)
- `adguard-cli` — install via **official script** (recommended) or [AUR: adguard-cli-bin](https://aur.archlinux.org/packages/adguard-cli-bin)

### Installing adguard-cli

Recommended (official upstream):
```bash
curl -fsSL https://raw.githubusercontent.com/AdguardTeam/AdGuardCLI/release/install.sh | sh -s -- -v
```

Alternative (Arch Linux AUR):
```bash
paru -S adguard-cli-bin
```

If adguard-cli is not found at startup, the app shows a helpful dialog with install instructions and a copy-to-clipboard button.

---

## Install

```bash
sudo pacman -S python-pyqt6 libnotify
git clone https://github.com/RiDDiX/adguard-tray.git
cd adguard-tray
bash install.sh
```

If `~/.local/bin` isn't in your PATH yet (fish):
```bash
fish_add_path ~/.local/bin
```

Then just run:
```bash
adguard-tray
```

---

## Autostart

Either tick **"Autostart on login"** in the tray menu, or add it via KDE System Settings → Autostart.

The entry goes to `~/.config/autostart/adguard-tray.desktop` (standard XDG autostart).

---

## Tray menu

```
● Status: Active – Protection running
──────────────────────────────
  Toggle
  Disable
  Restart
──────────────────────────────
  Filters         ▶  (live list with checkboxes)
    └ Manage filters…
  Userscripts     ▶  (live list with checkboxes)
    └ Manage userscripts…
──────────────────────────────
  Refresh status
──────────────────────────────
  Settings…
  Autostart on login  [✓]
──────────────────────────────
  Quit
```

---

## Privilege escalation

Start/stop requires root. The app tries in order:

1. `adguard-cli start/stop` directly
2. `pkexec adguard-cli start/stop` (polkit dialog)
3. `pkexec systemctl start/stop adguard-cli`

---

## Config

`~/.config/adguard-tray/config.json` — created automatically on first run.

```json
{
  "refresh_interval": 30,
  "notifications_enabled": true,
  "log_level": "INFO",
  "adguard_cli_path": ""
}
```

- **adguard_cli_path**: Leave empty to auto-detect via PATH. Set to a full path (e.g. `/opt/adguard-cli/adguard-cli`) if installed in a non-standard location.

Logs go to `~/.local/share/adguard-tray/adguard-tray.log` (auto-rotated, 5 MB max, 3 backups).

---

## Hyprland

Needs a tray-capable status bar. With waybar, make sure `"tray"` is in your bar modules:

```json
"tray": { "spacing": 8 }
```

---

## Compatibility

| Environment | Works |
|---|---|
| KDE Plasma 6 Wayland | ✅ |
| KDE Plasma 6 X11 | ✅ |
| Hyprland + waybar | ✅ |
| GNOME | needs AppIndicator extension |

---

## License

MIT
