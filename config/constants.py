from enum import Enum

class AppIcons(Enum):
    """Default icons for the app. """
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
    SETTING = ":material/settings:"
    FILTER = ":material/filter_list:"
    NEWS = ":material/newspaper:"
    CALENDAR = ":material/calendar_month:"
    NO_IMAGE_DATA_URL = "https://storage.googleapis.com/replit/images/1608749573246_3ecaeb5cdbf14cd5f1ad8c48673dd7ce.png"


class AppMessages(Enum):
    """Default messages for the app. """
    LOAD_DATA = "Gather Data..."
    BARO_LOCKED = "This will unlock when he comes back to a relay."
    VARZIA_BROWSE = "Click to browse wares."
    MARKET_TOOL_TIP = "Go to warframe.market."
    OFFER_STATUS_TOOLTIP = "Include all trades when empty."
    OFFER_TYPE_TOOLTIP = "WTS: sell offers, WTB: buy offers. Default to WTS if empty."
    PROGRESS = "Operation in progress. Please wait."
    GOTO_WIKI = "Go to Warframe Wiki."

    @staticmethod
    def delta_datetime_message(days,hours, minutes):
        """Return delta time formatted message. """
        return f"{days}d, {hours}h, {minutes}m"

    @staticmethod
    def delta_time_message(hours, minutes):
        """Return delta time formatted message. """
        return f"{hours}h:{minutes}m"


class AppLabels(Enum):
    """Default button, widget labels for the app. """
    BROWSE = "Browse"
    RELOAD = "Reload"
    DETAIL_MARKET = "Details"
    STATUS = "Status"
    TYPE = "Type"
    DEFAULT_TYPE = "WTS"
    DEFAULT_STATUS = "Ingame"
    INSPECT = "Inspect"
    MARKET = "Market"
    WIKI = "Wiki"
    REPORT = "Report"
    REPUTATION = "Reputation threshold: "
    NUMBER_OF_TRADES = "Number of trades per page: "
    PRIME_SELECT = "Choose up to 2 Primes."
    RELIC_SELECT = "Choose a relic. "
    REWARD_SELECT = "Choose a reward to inspect: "


class AppPages(Enum):
    """The Web app pages locations. """
    HOME = "components/pages/home.py"
    ERROR = "components/pages/error.py"
    NOTFOUND = "components/pages/not_found.py"
    RELICS = "components/pages/relics.py"
    NEWS = "components/pages/news.py"
    RIVENS = "components/pages/riven.py"
    MARKET = "components/pages/market.py"
    VARZIA = "components/pages/varzia.py"
    BARO = "components/pages/baro.py"
    ISSUE = "https://github.com/rqkun/void_pet/issues"

class AppExports(Enum):
    """The Web app pages locations. """
    DRONES = {
        "path": "static/exports/ExportDrones_en.json",
        "object_name": "ExportDrones"
    }
    COSMETICS = {
        "path": "static/exports/ExportCustoms_en.json",
        "object_name": "ExportCustoms"
    }
    FLAVOURS = {
        "path": "static/exports/ExportFlavour_en.json",
        "object_name": "ExportFlavour"
    }
    BUNDLES = {
        "path": "static/exports/ExportFusionBundles_en.json",
        "object_name": "ExportFusionBundles"
    }
    GEARS = {
        "path": "static/exports/ExportGear_en.json",
        "object_name": "ExportGear"
    }
    KEYS = {
        "path": "static/exports/ExportKeys_en.json",
        "object_name": "ExportKeys"
    }
    MANIFEST = {
        "path": "static/exports/ExportManifest.json",
        "object_name": "Manifest"
    }
    RECIPES = {
        "path": "static/exports/ExportRecipes_en.json",
        "object_name": "ExportRecipes"
    }
    REGIONS = {
        "path": "static/exports/ExportRegions_en.json",
        "object_name": "ExportRegions"
    }
    RELIC_ARCANE = {
        "path": "static/exports/ExportRelicArcane_en.json",
        "object_name": "ExportRelicArcane"
    }
    RESOURCES = {
        "path": "static/exports/ExportResources_en.json",
        "object_name": "ExportResources"
    }
    SENTINELS = {
        "path": "static/exports/ExportSentinels_en.json",
        "object_name": "ExportSentinels"
    }
    SORTIES = {
        "path": "static/exports/ExportSortieRewards_en.json",
        "object_name": "ExportSortieRewards"
    }
    NIGHTWAVE = {
        "path": "static/exports/ExportSortieRewards_en.json",
        "object_name": "ExportNightwave"
    }
    RAILJACK = {
        "path": "static/exports/ExportSortieRewards_en.json",
        "object_name": "ExportRailjack"
    }
    INTRINSICS = {
        "path": "static/exports/ExportSortieRewards_en.json",
        "object_name": "ExportIntrinsics"
    }
    OTHER = {
        "path": "static/exports/ExportSortieRewards_en.json",
        "object_name": "ExportOther"
    }
    UPGRADES = {
        "path": "static/exports/ExportUpgrades_en.json",
        "object_name": "ExportUpgrades"
    }
    MOD_SET = {
        "path": "static/exports/ExportUpgrades_en.json",
        "object_name": "ExportModSet"
    }
    AVIONICS = {
        "path": "static/exports/ExportUpgrades_en.json",
        "object_name": "ExportAvionics"
    }
    FOCUS_UPGRADES = {
        "path": "static/exports/ExportUpgrades_en.json",
        "object_name": "ExportFocusUpgrades"
    }
    WARFRAMES = {
        "path": "static/exports/ExportWarframes_en.json",
        "object_name": "ExportWarframes"
    }
    ABILITIES = {
        "path": "static/exports/ExportWarframes_en.json",
        "object_name": "ExportAbilities"
    }
    WEAPONS = {
        "path": "static/exports/ExportWeapons_en.json",
        "object_name": "ExportWeapons"
    }
    RAILJACK_WEAPONS = {
        "path": "static/exports/ExportWeapons_en.json",
        "object_name": "ExportRailjackWeapons"
    }
    

class Warframe(Enum):
    """Warframe APIs and images. """
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
    STATUS_API = {
        "api" : "https://api.warframestat.us"
    }
    MARKET_API = {
        "api" : "https://api.warframe.market/v1",
        "static" : "https://warframe.market/static/assets/",
        "url" : "https://warframe.market/items/",
        "base" : "https://warframe.market/"
    }
    PUBLIC_EXPORT_API ={
        "api": "http://content.warframe.com/PublicExport",
        "index": "https://origin.warframe.com/PublicExport/index_en.txt.lzma"
    }
    
    ONLINE_STATUS ={
        "list": ["offline", "ingame", "online"],
        "priority" : {"ingame": 0, "online": 1, "offline": 2}
    }
    GAME_ICON = "https://wiki.warframe.com/images/IconLotus.png"
    MODE_ICONS = {
        "INVASION": "https://wiki.warframe.com/images/InvasionIcon.png",
        "ALERT": "https://wiki.warframe.com/images/IconLotus.png",
        "OPEN_WORLD": "https://wiki.warframe.com/images/ReputationLarge.png",
        "QUEST":"https://wiki.warframe.com/images/IconQuest.png",
    }
    
    @staticmethod
    def get_wiki_url(string, type =None):
        """Return the wiki url of a certain item. """
        wiki_url = string.replace(" ","_")
        if type is not None:
            if type == "Skin":
                if "Syandana" in string:
                    wiki_url = "Syandana"
            if type == "Ship Decoration":
                if "Noggle" in string:
                    wiki_url = "Orbiter#Noggles"

        return f"https://wiki.warframe.com/w/{wiki_url}"