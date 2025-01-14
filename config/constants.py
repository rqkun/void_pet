from enum import Enum

class AppIcons(Enum):
    MAIN_APP = ":material/token:"
    ERROR = ":material/error:"
    WARNING = ":material/warning:"
    SUCCESS =":material/check_circle:"
    SYNC = ":material/sync:"
    MENU = ":material/menu:"
    HOME = ":material/home:"
    VARZIA = ":material/shopping_cart_checkout:"
    ISSUES = ":material/bug_report:"
    WIKI =":material/import_contacts:"
    EXTERNAL =":material/open_in_new:"
    MARKET = ":material/storefront:"
    INSPECT = ":material/search:"
    #
    PLATINUM = "https://static.wikia.nocookie.net/warframe/images/e/e7/PlatinumLarge.png"
    DUCAT = "https://static.wikia.nocookie.net/warframe/images/d/d5/OrokinDucats.png"
    AYA ="https://static.wikia.nocookie.net/warframe/images/4/45/Aya.png"

class AppMessages(Enum):
    LOAD_DATA = "Gather Data..."
    BARO_LOCKED = "This will unlock when he comes back to a relay."
    VARZIA_BROWSE = "Click to browse wares."
    MARKET_TOOL_TIP = "Go to warframe.market."
    OFFER_STATUS_TOOLTIP = "Include all trades when empty."
    OFFER_TYPE_TOOLTIP = "WTS: sell offers, WTB: buy offers. Default to WTS if empty."
    PROGRESS = "Operation in progress. Please wait."
    GOTO_WIKI = "Go to Warframe Wiki."
    
    @staticmethod
    def index_relic_message(item_name):
        return f"Indexed: {item_name}"
    @staticmethod
    def location_message(location):
        return f"Place: `{location}`"
    
    @staticmethod
    def end_time_message(date):
        return f"Leave: `{date}`"
    
    @staticmethod
    def start_time_message(date):
        return f"Arrive: `{date}`"
    
    @staticmethod
    def delta_time_message(days,hours, minutes):
        return f"{days} days, {hours} hours, {minutes} minutes"

class AppLabels(Enum):
    BROWSE = "Browse"
    RELOAD = "Reload"
    DETAIL_MARKET = "Details"
    STATUS = "Status"
    TYPE = "Type"
    DEFAULT_TYPE = "WTS"
    DEFAULT_STATUS = "All"
    INSPECT = "Inspect"
    MARKET = "Market"
    WIKI = "Wiki"
    REPORT = "Report"
    REPUTATION = "Reputation threshold: "
    NUMBER_OF_TRADES = "Number of Trades: "
    PRIME_SELECT = "Choose a Prime."
    RELIC_SELECT = "Choose a relic to inspect it's rewards: "
    REWARD_SELECT = "Choose a reward to inspect: "
    
    @staticmethod
    def status_options():
        return ["All", "Online", "Offline", "Ingame"]
    @staticmethod
    def type_options():
        return ["WTS","WTB"]
    
    
class AppPages(Enum):
    HOME = "components/pages/home.py"
    ERROR = "components/pages/error.py"
    VARZIA = "components/pages/varzia.py"
    ISSUE = "https://github.com/rqkun/void_pet/issues"

class Warframe(Enum):
    BARO = {
        "name" : "Baro Ki'Teer",
        "image" : "static/image/baro.png"
    }
    VARZIA = {
        "name" : "Variza",
        "image" : "static/image/varzia.png"
    }
    STATUS = {
        "api" : "https://api.warframestat.us"
    }
    MARKET = {
        "api" : "https://api.warframe.market/v1",
        "static" : "https://warframe.market/static/assets",
        "url" : "https://warframe.market/items"
    }
    
    @staticmethod
    def get_wiki_url(string):
        wiki_url = string.replace(" ","_")
        return f"https://warframe.fandom.com/wiki/{wiki_url}"