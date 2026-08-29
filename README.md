# adguard-tray

System tray app for [adguard-cli](https://adguard.com/en/adguard-linux/overview.html) on Linux. Built because there was nothing decent for KDE Plasma or Hyprland — just a terminal and a service.

Works on Wayland and X11. Written in Python + PyQt6.

The UI language is detected automatically from the system locale (override in Settings). English is the default; German and Simplified Chinese are included.

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
- Activity view: requests, blocked/allowed counts and top domains read from adguard-cli's access log
- Install the HTTPS certificate into Chromium-based browsers (Brave, Chrome, ungoogled-chromium, Vivaldi, …) and Firefox-family profiles
- HTTP/3 (QUIC) check: tells you when browsers can bypass filtering
- Guided settings for sites that refuse to load behind the proxy
- `--version` / `-V` flag

---

## Requirements

- `python` >= 3.11
- `python-pyqt6`
- `python-yaml`
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
sudo pacman -S python-pyqt6 python-yaml libnotify
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
  Enable / Disable     (whichever applies)
  Restart
──────────────────────────────
  Filters         ▶  (live list with checkboxes)
    └ Manage filters…
  Userscripts     ▶  (live list with checkboxes)
    └ Manage userscripts…
──────────────────────────────
  Refresh status
──────────────────────────────
  Open Manager…         (full tabbed GUI)
  Activity…             (requests from the access log)
  AdGuard Configuration…(proxy.yaml editor)
  Website Exceptions…
  Settings…
  Autostart on login  [✓]
──────────────────────────────
  adguard-tray vX.Y.Z · CLI vA.B.C
  Quit
```

---

## Privilege escalation

Start/stop requires root. The app tries in order:

1. `adguard-cli start/stop` directly
2. `pkexec adguard-cli start/stop` (polkit dialog)
3. `pkexec systemctl start/stop adguard-cli`

---

## HTTPS certificate

`adguard-cli cert` adds AdGuard's root certificate to the system trust store,
which covers Firefox's default profile and WebKit browsers. Chromium-based
browsers keep their own certificate store and ignore the system one, so HTTPS
filtering silently does nothing there.

The Manager's **Overview** tab has *Install certificate in browsers…*, which
imports the certificate into every browser certificate store it finds:

- `~/.pki/nssdb` and `~/.local/share/pki/nssdb` (Chromium 146+ prefers the latter) — created when missing
- Flatpak and Snap browser stores
- Firefox, LibreWolf, Waterfox and Zen profiles listed in their `profiles.ini`

It needs `certutil` (Arch: `nss`); the copy shipped with adguard-cli is used as
a fallback. Browsers read the store at startup, so restart them afterwards.

This installs a certificate authority that lets AdGuard read those browsers'
HTTPS traffic — the same trade-off HTTPS filtering always makes.

## Websites don't load with HTTPS filtering on

Change **one** setting at a time in *AdGuard Configuration → HTTPS*, save, and
retry — the four below are listed in the order worth trying, not as four causes
of the same problem.

**1. Filter HTTP/3 (QUIC) – experimental.** The documented one: AdGuard states
that Chrome-based browsers do not accept user certificates, so HTTP/3 filtering
is unsupported there. Turning it off costs nothing on Chromium and is the first
thing to try. There is a button for it in the *Sites that don't load* section.

**2. Enforce Certificate Transparency.** AdGuard stops filtering a site whose
own certificate does not satisfy Chrome's CT policy, and the browser may then
refuse it. Big sites are CT-compliant, so this only explains a failure when the
browser actually reports a certificate error.

**3. Secure DNS filtering.** Only affects browsers using DoH/DoT. Relevant when
name resolution itself breaks, not when a single site fails to render. Setting
it to `off` also lets browsers resolve past AdGuard's DNS filtering.

**4. OCSP certificate checks.** Least likely: AdGuard checks revocation
asynchronously and lets the connection through when the check is slow.

The *Turn off all strict checks* button does 2–4 at once. It is the blunt
option: revoked or mis-issued certificates then go unnoticed on **every**
connection, not just the site that was broken. Prefer switching a single
setting, and switch it back once the real cause is known.

## Activity

The Manager's Activity tab shows what AdGuard did with each request: domain,
whether a rule matched, which rule, response size and duration. It also lists
the most frequently blocked domains and the request count per hour, and lets
you allow or block the selected domain with one click (the rule goes into
`user.txt`).

The data comes from adguard-cli's access log – `access_log_file` in
`proxy.yaml`, by default `~/.local/share/adguard-cli/logs/access.log`. That log
is the only per-request record adguard-cli keeps; there is no statistics
command and no API. Two consequences:

- Nothing is shown before AdGuard has filtered traffic, because the log does
  not exist yet.
- When AdGuard runs as a system service, the log belongs to root and cannot be
  read from the desktop session. The tab says so instead of showing zero.

The log format is undocumented, so the parser reads the parts that carry
meaning (request line, size, duration, matched rule) and counts lines it cannot
read instead of guessing. Blocked versus allowed is derived from the rule
itself: `@@` marks an exception in AdGuard's syntax.

---

## HTTP/3 (QUIC)

Browsers prefer HTTP/3 over UDP port 443. What AdGuard does with it depends on
the proxy mode in `proxy.yaml`:

| Proxy mode | HTTP/3 |
|---|---|
| `auto` | UDP 443 is redirected into AdGuard. `https_filtering.http3_filtering_enabled: true` filters HTTP/3, `false` **blocks** QUIC so browsers fall back to HTTP/2 — which is filtered reliably, so `false` is the safer setting |
| `manual` | Nothing touches UDP 443. Browsers reach sites directly over HTTP/3 and that traffic is **not filtered** |

The Manager's **Diagnostics** tab shows which case applies, whether a firewall
rule or a browser policy blocks QUIC, and can switch HTTP/3 off in Firefox-family
profiles (writes `network.http.http3.enable` to the profile's `user.js`).

Chromium-based browsers have no per-user switch; the options are
`chrome://flags/#enable-quic` → *Disabled* per browser, or a system-wide policy:

```bash
# Brave: /etc/brave/policies/managed/ — Chrome: /etc/opt/chrome/policies/managed/
# Chromium/ungoogled-chromium/Vivaldi: /etc/chromium/policies/managed/
sudo mkdir -p /etc/brave/policies/managed
echo '{ "QuicAllowed": false }' | sudo tee /etc/brave/policies/managed/quic.json
```

Blocking UDP 443 in the firewall also works, but it breaks DNS-over-QUIC,
WireGuard on port 443 and some video calls — so the app does not do it for you.

## Config

`~/.config/adguard-tray/config.json` — written when you save the Settings dialog; defaults apply until then.

```json
{
  "refresh_interval": 30,
  "notifications_enabled": true,
  "log_level": "INFO",
  "adguard_cli_path": "",
  "language": ""
}
```

- **adguard_cli_path**: Leave empty to auto-detect via PATH. Set to a full path (e.g. `/opt/adguard-cli/adguard-cli`) if installed in a non-standard location.
- **language**: Leave empty to follow the system locale, or set `en`, `de` or `zh`.

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

## Support

If this saves you a trip to the terminal, you can buy me a coffee:

- [PayPal](https://www.paypal.me/RiDDiX93)
- [Ko-fi](https://ko-fi.com/riddix)
- GitHub Sponsors — the **Sponsor** button at the top of the repo

---

## License

MIT
