# adguard-tray

System tray app for [adguard-cli](https://adguard.com/en/adguard-linux/overview.html) on Linux. Built because there was nothing decent for KDE Plasma or Hyprland — just a terminal and a service.

Works on Wayland and X11. Written in Python + PyQt6.

---

## What it does

- Shows AdGuard status in the tray (green = running, grey = stopped, red = error)
- Start / stop / restart from the tray menu
- Toggle individual filters without opening a terminal
- Manage userscripts (install, enable/disable, remove)
- Update all filters with one click
- Install custom filter lists by URL
- Desktop notifications when status changes
- Autostart toggle right in the tray menu

---

## Requirements

- `python` >= 3.11
- `python-pyqt6`
- `libnotify` (for notifications)
- `adguard-cli` — [AUR: adguard-cli-bin](https://aur.archlinux.org/packages/adguard-cli-bin)

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

Either tick **"Autostart beim Login"** in the tray menu, or add it via KDE Systemeinstellungen → Autostart.

The entry goes to `~/.config/autostart/adguard-tray.desktop` (standard XDG autostart).

---

## Tray menu

```
● Status: Aktiv – Schutz läuft
──────────────────────────────
  Umschalten
  Deaktivieren
  Neu starten
──────────────────────────────
  Filter          ▶  (live list with checkboxes)
    └ Filter verwalten…
  Userscripts     ▶  (live list with checkboxes)
    └ Userscripts verwalten…
──────────────────────────────
  Status aktualisieren
──────────────────────────────
  Einstellungen…
  Autostart beim Login  [✓]
──────────────────────────────
  Beenden
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
  "log_level": "INFO"
}
```

Logs go to `~/.local/share/adguard-tray/adguard-tray.log`.

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
