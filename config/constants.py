from enum import Enum

class AppIcons(Enum):
    """ Default icons for the app. """
    MAIN_APP = ":material/token:"
    ERROR = ":material/error:"
    WARNING = ":material/warning:"
    SUCCESS =":material/check_circle:"
    SYNC = ":material/sync:"
    MENU = ":material/menu:"
    HOME = ":material/home:"
    VARZIA = ":material/local_convenience_store:"
    BARO = ":coin:"
    ISSUES = ":material/bug_report:"
    WIKI =":material/import_contacts:"
    EXTERNAL =":material/open_in_new:"
    MARKET = ":material/storefront:"
    INSPECT = ":material/search:"
    INFO = ":material/info:"
    AYA = ":droplet:"
    NO_IMAGE_DATA_URL = "https://cdn-icons-png.flaticon.com/512/7466/7466140.png"

class AppMessages(Enum):
    """ Default messages for the app. """
    LOAD_DATA = "Gather Data..."
    BARO_LOCKED = "This will unlock when he comes back to a relay."
    VARZIA_BROWSE = "Click to browse wares."
    MARKET_TOOL_TIP = "Go to warframe.market."
    OFFER_STATUS_TOOLTIP = "Include all trades when empty."
    OFFER_TYPE_TOOLTIP = "WTS: sell offers, WTB: buy offers. Default to WTS if empty."
    PROGRESS = "Operation in progress. Please wait."
    GOTO_WIKI = "Go to Warframe Wiki."
    
    @staticmethod
    def baro_time_message(date):
        """ Return arrival date of baro formatted message. """
        return f"Baro will arrive after: `{date}`"
    
    @staticmethod
    def index_relic_message(item_name):
        """ Return progress message for indexing relic. """
        return f"Indexed: {item_name}"
    @staticmethod
    def location_message(location):
        """ Return location formatted message. """
        return f"Node: `{location}`"
    
    @staticmethod
    def end_time_message(date):
        """ Return leaving date formatted message. """
        return f"Leave: `{date}`"
    
    @staticmethod
    def start_time_message(date):
        """ Return arrival date formatted message. """
        return f"Arrive: `{date}`"
    
    @staticmethod
    def delta_datetime_message(days,hours, minutes):
        """ Return delta time formatted message. """
        return f"{days}d, {hours}h, {minutes}m"
    @staticmethod
    def delta_time_message(hours, minutes):
        """ Return delta time formatted message. """
        return f"{hours}h:{minutes}m"
    
class AppLabels(Enum):
    """ Default button, widget labels for the app. """
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
    RELIC_SELECT = "Choose a relic. "
    REWARD_SELECT = "Choose a reward to inspect: "
    
    @staticmethod
    def status_options():
        """ Return the labels of options for online status widget. """
        return ["All", "Online", "Offline", "Ingame"]
    @staticmethod
    def type_options():
        """ Return the labels of options for the order type widget. """
        return ["WTS","WTB"]
    
    
class AppPages(Enum):
    """ The Web app pages locations. """
    HOME = "components/pages/home.py"
    ERROR = "components/pages/error.py"
    AYA = "components/pages/aya.py"
    VARZIA = "components/pages/varzia.py"
    BARO = "components/pages/baro.py"
    ISSUE = "https://github.com/rqkun/void_pet/issues"

class AppExports(Enum):
    """ The Web app pages locations. """
    COSMETICS = "datasources/exports/ExportCustoms_en.json"
    DRONES = "datasources/exports/ExportDrones_en.json"
    FLAVOURS = "datasources/exports/ExportFlavour_en.json"
    BUNDLES = "datasources/exports/ExportFusionBundles_en.json"
    GEARS = "datasources/exports/ExportGear_en.json"
    KEYS = "datasources/exports/ExportKeys_en.json"
    MANIFEST = "datasources/exports/ExportManifest.json"
    RECIPES = "datasources/exports/ExportRecipes_en.json"
    REGIONS = "datasources/exports/ExportRegions_en.json"
    RELIC_ARCANE = "datasources/exports/ExportRelicArcane_en.json"
    RESOURCES = "datasources/exports/ExportResources_en.json"
    SENTIELS = "datasources/exports/ExportSentinels_en.json"
    SORTIES = "datasources/exports/ExportSortieRewards_en.json"
    UPGRADES = "datasources/exports/ExportUpgrades_en.json"
    WARFRAMES = "datasources/exports/ExportWarframes_en.json"
    WEAPONS = "datasources/exports/ExportWeapons_en.json"

class Warframe(Enum):
    """ Warframe APIs and images. """
    PLATINUM = {
        "name": "Platinum",
        "image": "https://static.wikia.nocookie.net/warframe/images/e/e7/PlatinumLarge.png"
    } 
    DUCAT = {
        "name": "Ducat",
        "image": "https://static.wikia.nocookie.net/warframe/images/d/d5/OrokinDucats.png"
    }
    CREDITS = {
        "name": "Credits",
        "image": "https://static.wikia.nocookie.net/warframe/images/2/2b/Credits.png"
    }
    AYA = {
        "name": "Aya",
        "image": "https://static.wikia.nocookie.net/warframe/images/4/45/Aya.png"
    }
    REGAL_AYA = {
        "name": "Regal Aya",
        "image": "https://static.wikia.nocookie.net/warframe/images/f/f0/RegalAya.png"
    }
    BARO = {
        "name" : "Baro Ki'Teer",
        "uniqueName" : "/Lotus/Types/StoreItems/AvatarImages/ImageBaroKiteer", 
        "image" : "datasources/images/baro.png"
    }
    VARZIA = {
        "name" : "Variza",
        "uniqueName" : "/Lotus/Types/StoreItems/Packages/MegaPrimeVault/LastChanceItemA", 
        "image" : "datasources/images/varzia.png"
    }
    STATUS = {
        "api" : "https://api.warframestat.us"
    }
    MARKET = {
        "api" : "https://api.warframe.market/v1",
        "static" : "https://warframe.market/static/assets",
        "url" : "https://warframe.market/items"
    }
    PUBLIC_EXPORT ={
        "api": "http://content.warframe.com/PublicExport",
        "index": "https://origin.warframe.com/PublicExport/index_en.txt.lzma"
    }
    @staticmethod
    def get_wiki_url(string):
        """ Return the wiki url of a certain item. """
        wiki_url = string.replace(" ","_")
        return f"https://warframe.fandom.com/wiki/{wiki_url}"