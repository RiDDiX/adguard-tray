# adguard-tray

System tray app for [adguard-cli](https://adguard.com/en/adguard-linux/overview.html) on Linux. Built because there was nothing decent for KDE Plasma or Hyprland — just a terminal and a service.

Works on Wayland and X11. Written in Python + PyQt6.

The UI language is detected automatically from the system locale (override in Settings). English is the default; German and Simplified Chinese are included. Light and dark mode follow the desktop's setting while the app runs (override in Settings → Appearance).

---

## What it does

- Shows AdGuard status in the tray (green = running, grey = stopped, red = error)
- Start / stop / restart from the tray menu
- Toggle individual filters without opening a terminal
- Manager window with a sidebar: Overview, Activity, Filters, DNS, Userscripts, Exceptions, HTTPS, Stealth mode, Network, Maintenance, Settings, About — every adguard-cli setting on the page it belongs to, no nested dialogs
- Changes to AdGuard's own settings collect in one Apply bar, so several switches cost one restart
- Manage userscripts (install, enable/disable, remove)
- Update all filters with one click
- Install custom filter lists by URL
- Desktop notifications when status changes (with dedup to prevent spam)
- Start at login from Settings → Startup
- Light and dark mode that follow the desktop (KDE Plasma, GNOME, Hyprland), with a manual override
- Activity dashboard: requests, blocked/allowed/modified counts, traffic, per-hour chart, top-10 lists and a searchable request log, kept in a local database so history survives adguard-cli's log rotation
- Update check for adguard-tray itself, with one-click install where the files belong to us
- Install the HTTPS certificate into Chromium-based browsers (Brave, Chrome, ungoogled-chromium, Vivaldi, …) and Firefox-family profiles
- HTTP/3 (QUIC) check: tells you when browsers can bypass filtering
- Guided settings for sites that refuse to load behind the proxy
- `--version`, `--check-update` and `--update` flags

---

## Requirements

- Python >= 3.11 (with its sqlite3 module), PyQt6 and PyYAML
- polkit (`pkexec`) and libnotify (`notify-send`)
- `adguard-cli` — install via **official script** (recommended) or [AUR: adguard-cli-bin](https://aur.archlinux.org/packages/adguard-cli-bin)

`install.sh` installs everything except adguard-cli for you. These are the
packages it uses:

| Distribution | Packages |
|---|---|
| Arch and derivatives | `python-pyqt6 python-yaml polkit libnotify` |
| Fedora | `python3 python3-pyqt6-base python3-pyyaml polkit libnotify` |
| Debian 12+ / Ubuntu 24.04+ | `python3 python3-pyqt6 python3-yaml pkexec libnotify-bin` (Ubuntu: from universe) |
| openSUSE Tumbleweed | `python3 python3-PyQt6 python3-PyYAML pkexec libnotify-tools` |

Older releases such as Ubuntu 22.04 or openSUSE Leap 15 do not package PyQt6
for a recent enough Python; the installer stops there without changing anything.

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

The installer checks what is missing, installs it with your distribution's
package manager, and puts the app under `~/.local`. It only asks for your
password (through sudo) when something actually has to be installed.

In one line, without git:
```bash
d=$(mktemp -d) && curl -fsSL https://github.com/RiDDiX/adguard-tray/archive/refs/heads/main.tar.gz | tar xz -C "$d" && bash "$d/adguard-tray-main/install.sh"
```

Or from a clone:
```bash
git clone https://github.com/RiDDiX/adguard-tray.git
cd adguard-tray
bash install.sh
```

On Arch the AUR package works as well: `paru -S adguard-tray`.

On Fedora Silverblue or Kinoite, `/usr` is read-only, so the installer prints
the `rpm-ostree install` line for the missing packages instead of installing
them.

If `~/.local/bin` isn't in your PATH yet (fish):
```bash
fish_add_path ~/.local/bin
```

Then just run:
```bash
adguard-tray
```

---

## Updating adguard-tray

The About page has an **Updates** section: it shows the installed
version, how this copy was installed, and checks GitHub for a newer release
when you ask it to. Nothing is contacted unless you press the button.

What happens next depends on who owns the files:

```bash
adguard-tray --check-update   # print whether a newer release exists
adguard-tray --update         # install it (only for ~/.local installations)
```

Installed from the AUR, the package manager owns the files, so the app shows
the command for your helper (`paru -Syu adguard-tray`) instead of overwriting
them behind pacman's back. Running from a git checkout it points at
`git pull && bash install.sh`. Only an installation made by `install.sh` into
`~/.local/lib/adguard-tray` is replaced directly: the release tarball is
downloaded, checked that it really carries the version that was announced, and
swapped in with the old copy kept until the swap worked. Restart the app
afterwards — the running process still has the old modules loaded.

---

## Autostart

Turn on **Settings → Startup → Start AdGuard Tray when I log in**, or add it via KDE System Settings → Autostart.

The entry goes to `~/.config/autostart/adguard-tray.desktop` (standard XDG autostart).

---

## Tray menu

```
● Active – Protection running   (opens the Overview)
  Stop protection / Start protection   (whichever applies)
  Restart AdGuard
──────────────────────────────
  Filters         ▶  (live list with checkboxes)
    └ Manage filters…
  Userscripts     ▶  (live list with checkboxes)
    └ Manage userscripts…
──────────────────────────────
  Open AdGuard Tray
  Activity
  Website exceptions
  Settings
──────────────────────────────
  adguard-tray vX.Y.Z · CLI vA.B.C
  Quit
```

A left click on the tray icon opens the Manager as well.

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

The Manager's **HTTPS** page has *Add to browsers…*, which
imports the certificate into every browser certificate store it finds:

- `~/.pki/nssdb` and `~/.local/share/pki/nssdb` (Chromium 146+ prefers the latter) — created when missing
- Flatpak and Snap browser stores
- Firefox, LibreWolf, Waterfox and Zen profiles listed in their `profiles.ini`

It needs `certutil` (Arch: `nss`, Fedora: `nss-tools`, Debian/Ubuntu:
`libnss3-tools`, openSUSE: `mozilla-nss-tools`); the copy shipped with
adguard-cli is used as a fallback. Browsers read the store at startup, so
restart them afterwards.

This installs a certificate authority that lets AdGuard read those browsers'
HTTPS traffic — the same trade-off HTTPS filtering always makes.

## Websites don't load with HTTPS filtering on

Change **one** setting at a time on the Manager's *HTTPS* page, apply, and
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

The Manager's Activity page is a traffic dashboard: counters for requests,
blocked, allowed, modified and traffic; a bar chart of the requests per hour,
blocked and allowed stacked; top-10 lists for most blocked, most
requested, most traffic and most-hit rules; and a searchable request list.
Click a domain in any list to drill into it, and allow or block the selected
domain straight from the table.

The range selector covers the last 24 hours, 7 days, 30 days and all time.

### Where the numbers come from

adguard-cli has no statistics command, no query log and no API. The only
per-request record is the access log named by `access_log_file` in
`proxy.yaml`, and adguard-cli rotates it itself: past 10 MiB it renames
`access.log` to `access.log.1` and shifts the older generations down to
`access.log.9`. Those constants are compiled into the binary, so there is no
setting for them.

Reading the tail of that file therefore only ever shows a sliding window. So
the page reads the log *forward* instead, into a SQLite database at
`~/.local/share/adguard-tray/activity.db`, remembering how far it got. It
keeps three things:

- raw requests for up to 14 days, or 400 000 requests, whichever runs out
  first — these feed the request list and the drill-down
- per-domain and per-rule counts per hour for 90 days — these feed the top
  lists
- hourly totals, which are never deleted — this is what makes "last 30 days"
  and "all time" answerable

On the first run the rotated generations that are still on disk are read too,
so the history does not start empty. Afterwards, when the file being read is
renamed away, the remainder is picked up from the rotated copies before the
new file is read, including the case of several rollovers between two looks.
Only whole lines are consumed, because the daemon may be halfway through
writing the last one.

The catch worth knowing: **the log is only read while the Activity page
refreshes it.** If the Manager stays closed long enough for the log to rotate
through all ten generations, the requests in between are gone before anything
records them. Opening the page now and then is what keeps the history complete.

*More → Reset history* empties the database and reads the log again from what is
still on disk.

One known inaccuracy: log timestamps carry no time zone, so during the hour
that repeats when daylight saving ends, requests from the second pass land in
the first pass's hour.

### What it cannot show

The log format is undocumented. It was recovered by disassembling the function
that writes it, which formats fourteen fields — application, protocol, method,
URL, status, content type, filtering verdict, rule count, filter-list ID,
address, bytes, duration and the matched rule. The parser anchors on the parts
that cannot move — the quoted first field, the `…b` and `…ms` suffixes and the
` -- ` before the rule — and reads each remaining field only when its own
marker holds: a known protocol name, a three-digit status, an `ID=<n>`. A
field whose marker fails is left empty instead of being guessed.

The one exception is blocked-versus-allowed: when the verdict field cannot be
read, it falls back to AdGuard's rule syntax, where `@@` marks an exception.
That fallback cannot tell a modified request from a blocked one.

Saved traffic is not shown: a blocked request never transfers the bytes it
would have, and the log does not record what they would have been. Grouping
domains into companies, as AdGuard's own apps do, needs a company database
that is not part of adguard-cli.

---

## HTTP/3 (QUIC)

Browsers prefer HTTP/3 over UDP port 443. What AdGuard does with it depends on
the proxy mode in `proxy.yaml`:

| Proxy mode | HTTP/3 |
|---|---|
| `auto` | UDP 443 is redirected into AdGuard. `https_filtering.http3_filtering_enabled: true` filters HTTP/3, `false` **blocks** QUIC so browsers fall back to HTTP/2 — which is filtered reliably, so `false` is the safer setting |
| `manual` | Nothing touches UDP 443. Browsers reach sites directly over HTTP/3 and that traffic is **not filtered** |

The HTTP/3 section of the Manager's **HTTPS** page shows which case applies, whether a firewall
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

## Light and dark mode

On KDE Plasma the app takes Plasma's colour scheme as it is — custom schemes and
the accent colour included — and follows a switch while it runs. The same goes
for a palette picked in qt5ct/qt6ct.

On GNOME, Hyprland, sway and similar sessions Qt keeps the colours it started
with and never reacts to the desktop's light/dark switch. There the app reads
the preference itself from the xdg desktop portal (`org.freedesktop.appearance`
`color-scheme`, the setting GNOME and most portal backends expose) and swaps in
its own light or dark palette when the two disagree.

If your session sets no preference or runs no portal, choose Light or Dark in
Settings → Appearance.

Checked on Qt 6.4 and 6.11 against a fake portal, with Qt's GTK, GNOME, portal
and generic platform themes, and with KDE Plasma 6 (plasma-integration and the
real portal) in a container. Not yet on a real GNOME or Hyprland desktop —
reports welcome.

## Config

`~/.config/adguard-tray/config.json` — written as soon as something changes on the Settings page; defaults apply until then.

```json
{
  "refresh_interval": 30,
  "notifications_enabled": true,
  "log_level": "INFO",
  "adguard_cli_path": "",
  "language": "",
  "appearance": ""
}
```

- **adguard_cli_path**: Leave empty to auto-detect via PATH. Set to a full path (e.g. `/opt/adguard-cli/adguard-cli`) if installed in a non-standard location.
- **language**: Leave empty to follow the system locale, or set `en`, `de` or `zh`.
- **appearance**: Leave empty to follow the desktop's light/dark setting, or set `light` or `dark`.

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
