"""Stealth mode – AdGuard's tracking protection (proxy.yaml `stealthmode`)."""

from .i18n import _t
from .proxy_settings import add_spin, add_switch, gate, guard
from .ui import Page, one_line

SM = "stealthmode"


class StealthTab(Page):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(parent=parent)
        s = ctx.settings

        master_card = self.section()
        master = add_switch(master_card, s, (SM, "enabled"), False, _t("Stealth mode"),
                            _t("Master switch for all tracking protection features below."))

        cookies = self.section(_t("Cookies"))
        third = add_switch(cookies, s, (SM, "block_third_party_cookies"), True,
                           _t("Block third-party cookies"),
                           one_line(_t("Delete third-party cookies after a set time.\nPrevents cross-site tracking.")))
        third_min = add_spin(cookies, s, (SM, "block_third_party_cookies_min"), 180,
                             _t("Lifetime (minutes):").rstrip(":："),
                             _t("0 = block immediately. Default: 180 minutes."), 0, 43200)
        first = add_switch(cookies, s, (SM, "block_first_party_cookies"), False,
                           _t("Block first-party cookies"),
                           one_line(_t("Delete all cookies (including first-party) after a set time.\n"
                                           "Warning: this logs you out of every site.")))
        first_min = add_spin(cookies, s, (SM, "block_first_party_cookies_min"), 4320,
                             _t("Lifetime (minutes):").rstrip(":："),
                             _t("0 = block immediately. Default: 4320 minutes (3 days)."), 0, 43200)
        gate(third.switch, third_min)
        gate(first.switch, first_min)

        privacy = self.section(_t("Privacy"))
        for key, default, title, tip in (
            ("hide_user_agent", True, "Hide / reduce User-Agent",
             "Strips identifying bits from the User-Agent.\nReduces fingerprinting."),
            ("hide_search_queries", True, "Hide search queries in referrer",
             "Hides your search terms when clicking from a search engine to a website."),
            ("remove_referrer_from_third_party_requests", True,
             "Remove referrer from third-party requests",
             "Prevents third-party sites from knowing which page you came from."),
            ("send_do_not_track_signals", True, "Send Do-Not-Track signal",
             "Sends DNT header with requests.\nNote: Most sites ignore this, but some respect it."),
            ("disable_third_party_cache", True, "Disable third-party ETag cache",
             "Prevents tracking via ETag caching in third-party content."),
            ("block_third_party_authorization", True, "Block third-party Authorization header",
             "Blocks the Authorization header in third-party requests to prevent tracking."),
            ("remove_x_client_data_header", True, "Remove X-Client-Data header",
             "Removes the X-Client-Data header sent by Chrome to Google services."),
        ):
            add_switch(privacy, s, (SM, key), default, _t(title), one_line(_t(tip)))

        apis = self.section(_t("Browser API blocking"))
        for key, default, title, tip in (
            ("block_web_rtc", False, "Block WebRTC",
             "Prevents IP leaks via WebRTC.\nMay break video calls and some web apps."),
            ("block_browser_push_api", True, "Block Push API",
             "Blocks browser push notifications from websites."),
            ("block_browser_location_api", True, "Block Location API",
             "Prevents websites from accessing your GPS location."),
            ("block_browser_flash", True, "Block Flash", "Blocks the Flash plugin."),
            ("block_browser_java", True, "Block Java",
             "Disables Java plugins. JavaScript remains enabled."),
        ):
            add_switch(apis, s, (SM, key), default, _t(title), one_line(_t(tip)))

        dpi = self.section(_t("Anti-DPI"))
        add_switch(dpi, s, (SM, "anti_dpi", "enabled"), False, _t("Enable Anti-DPI"),
                   one_line(_t("Alters outgoing packet data to bypass Deep Packet Inspection.\n"
                               "Useful in countries with internet censorship.")))

        gate(master.switch, cookies, privacy, apis, dpi)
        guard(self, s)
        self.finish()
