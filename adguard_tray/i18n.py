"""
Lightweight internationalisation.

Detects the system locale and provides a ``_t()`` translation function.
English is the default language; additional translations are stored as
simple dictionaries.  Falls back to the English key when no translation
exists for the active locale.
"""

import locale
import os

# ── Locale detection ──────────────────────────────────────────────────────

def _detect_language() -> str:
    """Return a 2-letter language code based on the system locale."""
    for var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        val = os.environ.get(var, "")
        if val:
            lang = val.split("_")[0].split(".")[0].split(":")[0].lower()
            if lang and lang not in ("c", "posix"):
                return lang
    try:
        lang, _ = locale.getlocale()
        if lang:
            return lang.split("_")[0].lower()
    except (ValueError, AttributeError):
        pass
    return "en"


_LANG = _detect_language()

# ── German translations ───────────────────────────────────────────────────

_DE: dict[str, str] = {
    # ── tray.py – status labels ───────────────────────────────────────────
    "Active – Protection running":          "Aktiv – Schutz läuft",
    "Inactive – Protection stopped":        "Inaktiv – Schutz gestoppt",
    "Error retrieving status":              "Fehler beim Statusabruf",
    "adguard-cli not found":                "adguard-cli nicht gefunden",
    "Unknown status":                       "Status unbekannt",
    "Checking status…":                     "Status wird abgefragt…",

    # ── tray.py – menu items ──────────────────────────────────────────────
    "Toggle":                               "Umschalten",
    "Enable":                               "Aktivieren",
    "Disable":                              "Deaktivieren",
    "Restart":                              "Neu starten",
    "Filters":                              "Filter",
    "Loading…":                             "Wird geladen…",
    "Manage filters…":                      "Filter verwalten…",
    "No userscripts installed":             "Keine Userscripts installiert",
    "Manage userscripts…":                  "Userscripts verwalten…",
    "Refresh status":                       "Status aktualisieren",
    "Settings…":                            "Einstellungen…",
    "Autostart on login":                   "Autostart beim Login",
    "Quit":                                 "Beenden",

    # ── tray.py – tooltips & notifications ────────────────────────────────
    "active":                               "aktiv",
    "inactive":                             "inaktiv",
    "System-wide filtering: {}":            "Systemweites Filtern: {}",
    "Error: {}":                            "Fehler: {}",
    "AdGuard Tray – Error":                 "AdGuard Tray – Fehler",
    "AdGuard is now active – protection running.":
        "AdGuard ist jetzt aktiv – Schutz läuft.",
    "AdGuard has been stopped.":
        "AdGuard wurde gestoppt.",
    "Could not retrieve status.":
        "Status konnte nicht abgerufen werden.",
    "Command failed":                       "Befehl fehlgeschlagen",

    # ── settings_dialog.py ────────────────────────────────────────────────
    "AdGuard Tray – Settings":              "AdGuard Tray – Einstellungen",
    "Status Refresh":                       "Status-Aktualisierung",
    " seconds":                             " Sekunden",
    "How often adguard-cli status is checked automatically.":
        "Wie häufig der Status von adguard-cli automatisch abgefragt wird.",
    "Interval:":                            "Intervall:",
    "Notifications":                        "Benachrichtigungen",
    "Desktop notification on status change":
        "Desktop-Benachrichtigung bei Statusänderung",
    "<small>Requires <i>libnotify</i> / <i>notify-send</i> or an "
    "active notification service (dunst, mako, KDE).</small>":
        "<small>Benötigt <i>libnotify</i> / <i>notify-send</i> oder einen "
        "aktiven Benachrichtigungsdienst (dunst, mako, KDE).</small>",
    "Autostart":                            "Autostart",
    "Start automatically on desktop login (XDG Autostart)":
        "Beim Desktop-Login automatisch starten (XDG Autostart)",
    "<small>Creates <i>~/.config/autostart/adguard-tray.desktop</i>.<br>"
    "Works on KDE Plasma, GNOME, Hyprland (with xdg-autostart-impl) "
    "and other XDG-compliant environments.</small>":
        "<small>Erstellt <i>~/.config/autostart/adguard-tray.desktop</i>.<br>"
        "Funktioniert auf KDE Plasma, GNOME, Hyprland (mit xdg-autostart-impl) "
        "und anderen XDG-konformen Umgebungen.</small>",

    # ── filters_dialog.py ─────────────────────────────────────────────────
    "AdGuard Tray – Manage Filters":        "AdGuard Tray – Filter verwalten",
    "Update filters":                       "Filter aktualisieren",
    "Updates all filters, DNS filters, userscripts,\n"
    "SafebrowsingV2, CRLite and checks for app updates.":
        "Aktualisiert alle Filter, DNS-Filter, Userscripts,\n"
        "SafebrowsingV2, CRLite und prüft auf App-Updates.",
    "Add custom filter…":                   "Eigenen Filter hinzufügen…",
    "Install custom filter by URL":         "Custom-Filter per URL installieren",
    "↺ Reload":                             "↺ Neu laden",
    "Loading filters…":                     "Filter werden geladen…",
    "No filters found.":                    "Keine Filter gefunden.",
    "{} of {} filters active":              "{} von {} Filtern aktiv",
    "Filter":                               "Filter",
    "ID":                                   "ID",
    "Last updated":                         "Zuletzt aktualisiert",
    "Enabling filter {}…":                  "Filter {} wird aktiviert…",
    "Disabling filter {}…":                 "Filter {} wird deaktiviert…",
    "Filter {} enabled.":                   "Filter {} aktiviert.",
    "Filter {} disabled.":                  "Filter {} deaktiviert.",
    "Updating filters…":                    "Filter werden aktualisiert…",
    "Update completed.":                    "Aktualisierung abgeschlossen.",
    "Update failed.":                       "Aktualisierung fehlgeschlagen.",
    "Add Custom Filter":                    "Eigenen Filter hinzufügen",
    "Filter URL (direct .txt URL of the filter list):":
        "Filter-URL (direkte .txt-URL der Filterliste):",
    "Installing: {}":                       "Installiere: {}",
    "Filter installed.":                    "Filter installiert.",
    "Remove":                               "Entfernen",
    "Remove filter":                        "Filter entfernen",
    'Really remove filter "{}"?':           'Filter «{}» wirklich entfernen?',
    "Removing filter {}…":                  "Filter {} wird entfernt…",
    "Filter {} removed.":                   "Filter {} entfernt.",

    # ── userscripts_dialog.py ─────────────────────────────────────────────
    "AdGuard Tray – Userscripts":           "AdGuard Tray – Userscripts",
    "Install (URL)…":                       "Installieren (URL)…",
    "Install userscript from a direct .js URL":
        "Userscript von einer direkten .js-URL installieren",
    "Userscript":                           "Userscript",
    "ID / Name":                            "ID / Name",
    "<small>Right-click a userscript to remove it.<br>"
    "Userscripts are automatically updated when running "
    "<i>Update filters</i>.</small>":
        "<small>Rechtsklick auf ein Userscript zum Entfernen.<br>"
        "Userscripts werden bei <i>Filter aktualisieren</i> "
        "automatisch mit aktualisiert.</small>",
    "Loading userscripts…":                 "Userscripts werden geladen…",
    "No userscripts installed.":            "Keine Userscripts installiert.",
    "{} of {} userscripts active":          "{} von {} Userscripts aktiv",
    "Enabling userscript '{}'…":            "Userscript '{}' wird aktiviert…",
    "Disabling userscript '{}'…":           "Userscript '{}' wird deaktiviert…",
    "Userscript '{}' enabled.":             "Userscript '{}' aktiviert.",
    "Userscript '{}' disabled.":            "Userscript '{}' deaktiviert.",
    "Install Userscript":                   "Userscript installieren",
    "Userscript URL (direct .js URL):":     "Userscript-URL (direkte .js-URL):",
    "Userscript installed.":                "Userscript installiert.",
    'Remove "{}"':                          '«{}» entfernen',
    "Remove userscript":                    "Userscript entfernen",
    'Really remove userscript "{}"?':       'Userscript «{}» wirklich entfernen?',
    "Removing '{}'…":                       "Entferne '{}'…",
    "'{}' removed.":                        "'{}' entfernt.",

    # ── cli.py ────────────────────────────────────────────────────────────
    "adguard-cli was not found.\n"
    "Install it with: paru -S adguard-cli-bin":
        "adguard-cli wurde nicht gefunden.\n"
        "Installiere es mit: paru -S adguard-cli-bin",
    "Unknown error retrieving status":
        "Unbekannter Fehler beim Statusabruf",
    "AdGuard {} successful":                "AdGuard {} erfolgreich",
    "AdGuard via systemctl {} successful":  "AdGuard via systemctl {} erfolgreich",
    "'{}' failed – insufficient privileges?":
        "'{}' fehlgeschlagen – Rechte unzureichend?",
    "Could not retrieve filter list":
        "Filter-Liste konnte nicht abgerufen werden",
    "Filter {} enabled":                    "Filter {} aktiviert",
    "Could not enable filter {}":           "Filter {} konnte nicht aktiviert werden",
    "Filter {} disabled":                   "Filter {} deaktiviert",
    "Could not disable filter {}":
        "Filter {} konnte nicht deaktiviert werden",
    "Filter installed":                     "Filter installiert",
    "Installation failed":                  "Installation fehlgeschlagen",
    "Filter {} removed":                    "Filter {} entfernt",
    "Could not remove filter {}":
        "Filter {} konnte nicht entfernt werden",
    "Filters updated":                      "Filter aktualisiert",
    "Update failed":                        "Update fehlgeschlagen",
    "Could not retrieve userscript list":
        "Userscript-Liste konnte nicht abgerufen werden",
    "Userscript '{}' enabled":              "Userscript '{}' aktiviert",
    "Could not enable userscript '{}'":
        "Userscript '{}' konnte nicht aktiviert werden",
    "Userscript '{}' disabled":             "Userscript '{}' deaktiviert",
    "Could not disable userscript '{}'":
        "Userscript '{}' konnte nicht deaktiviert werden",
    "Userscript '{}' removed":              "Userscript '{}' entfernt",
    "Could not remove userscript '{}'":
        "Userscript '{}' konnte nicht entfernt werden",
    "Userscript installed":                 "Userscript installiert",
    "Other":                                "Sonstige",

    # ── main.py ───────────────────────────────────────────────────────────
    "System tray not available":
        "Kein System-Tray verfügbar",
    "The system tray is not available in this desktop environment.\n\n"
    "On Hyprland: waybar with the [tray] module enabled or sfwbar is required.\n"
    "On KDE Plasma it should work out of the box.":
        "Das System-Tray ist in dieser Desktop-Umgebung nicht verfügbar.\n\n"
        "Unter Hyprland: waybar mit aktiviertem [tray]-Modul oder sfwbar benötigt.\n"
        "Unter KDE Plasma sollte es sofort funktionieren.",
}

# ── Translation registry ──────────────────────────────────────────────────

_TRANSLATIONS: dict[str, dict[str, str]] = {
    "de": _DE,
}

_CURRENT: dict[str, str] = _TRANSLATIONS.get(_LANG, {})


def _t(key: str, *args: object) -> str:
    """Return the translated string, optionally formatted with *args*."""
    text = _CURRENT.get(key, key)
    if args:
        return text.format(*args)
    return text
