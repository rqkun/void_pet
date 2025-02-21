import asyncio
from collections import defaultdict
import streamlit as st
from config import structures
from config.constants import AppIcons, AppMessages, Warframe
from datasources import warframe_export,warframe_market,warframe_status
from utils import tools
import utils.api_services as api_services
from utils.tools import parse_item_string

def get_image_url(unique_name,is_full =True) -> str:
    """ Return image url from export.

    Args:
        unique_name (str): the identifier of an item.

    Returns:
        str: Item image url.
    """
    if 'image_manifest' not in st.session_state:
        st.session_state.image_manifest = warframe_export.open_manifest()
    if is_full:
        identifier = unique_name.split("/")
        identifier = "/".join(identifier[len(identifier)-3:])
    else:
        identifier = unique_name
    for item in st.session_state.image_manifest:
        if identifier in item["uniqueName"]:
            return Warframe.PUBLIC_EXPORT.value["api"] + item["textureLocation"]

    return AppIcons.NO_IMAGE_DATA_URL.value

def get_image_bytes(url) -> bytes:
    """ Get Image bytes from url.

    Args:
        url (str): Request Image Url

    Returns:
        bytes: ImageBytes
    """
    return api_services.get_image(url)

def export_relic(name,field):
    """ Return the relic from the public export file.

    Args:
        name (str): uniqueName or name of the item.
        field (string): uniqueName / name

    Returns:
        dict: The json of found relic item.
    """
    local_relic_data = warframe_export.open_relic_arcane()
    for item in local_relic_data:
        if name in item[field]:
            return item
    return None

def get_relic_reward(relic) -> dict:
    """ Return relic's rewards dictionary.

    Args:
        relic (dict): relic data

    Returns:
        dict: Dictionary of options in the relic's reward
    """
    relic_option={}

    if relic is None:
        return None
    for item in relic["rewards"]:
        value = structures.relic_reward_object(item["chance"],item["rarity"],item["item"]["name"],item["item"]["imageName"])
        if 'Forma Blueprint' not in item["item"]["name"]:
            relic_option[item["item"]["name"]] = value
    return relic_option

def get_relic(name, is_unique) -> dict:
    """ Return relic's data using name or uniqueName

    Args:
        name (str): name or uniqueName of the relic
        is_unique (bool): check wheter if the name arg is uniqueName or name

    Returns:
        dict: Json of relic's data
    """
    field = "name"
    relic ={}

    if is_unique:
        identifier = name.split("/")
        identifier = "/".join(identifier[len(identifier)-3:])
        field = "uniqueName"
        
    relic = warframe_status.relic_request(identifier, is_unique)[0]
    
    relic_export = export_relic(identifier,field)
    for i,item in enumerate(relic["rewards"]):
        item["item"]["uniqueName"] = relic_export["relicRewards"][i]["rewardName"]
        item["item"]["imageName"] = get_image_url(relic_export["relicRewards"][i]["rewardName"])
    return relic

def extract_relic_rewards(relic):
    
    relic_export = export_relic(relic["uniqueName"],"uniqueName")
    for i,item in enumerate(relic["rewards"]):
        if relic_export is None:
            return None
        item["item"]["uniqueName"] = relic_export["relicRewards"][i]["rewardName"]
        item["item"]["imageName"] = get_image_url(relic_export["relicRewards"][i]["rewardName"])
    return relic

def get_variza():
    """ Call the warframe status api for varzia data.

    Returns:
        dict: Json data of the api response.
    """
    return warframe_status.vault_traider_request()

def get_baro():
    """ Call the warframe status api for baro data.

    Returns:
        dict: Json data of the api response.
    """
    return warframe_status.void_traider_request()

def get_world_state():
    """ Call the warframe status api for world state data.

    Returns:
        dict: Json data of the api response.
    """
    return warframe_status.world_state_request()

def get_prime_list() -> list:
    """ Call the warframe status api for list of primes.

    Returns:
        list: A clean prime names list.
    """
    p_frame = warframe_status.prime_warframes_request()
    p_weapon = warframe_status.prime_weapons_request()
    
    return tools.clean_prime_names(p_frame, p_weapon)

def get_prime_resurgent_list(primes,relics_list) -> list:
    """ Get all of the current resurgent primes list using varzia data.

    Args:
        primes (list): List of prime
        relics_list (list): List of relics

    Returns:
        list: List of current resurgent primes
    """
    result = []
    prime = get_prime_list()
    for prime in primes:
        rewards = search_rewards([prime],relics_list)
        if len(rewards)>0:
            result.append(prime)
    return result

def search_rewards(search_keys,relics) -> dict:
    """ Return relic that have search_key as reward(s).

    Args:
        search_key (str): Key word for searching.
        relics (list): List of relics

    Returns:
        dict: Result of the search.
    """
    result = {}
    if len(search_keys) > 0 != "" and len(relics) :
        for item in relics:
            if 'rewards' in item:
                for reward in item['rewards']: 
                    if any( "_"+search_key.lower().replace(" ", "_") in "_" + reward["item"]["name"].lower().replace(" ", "_") for search_key in search_keys):
                        result[item["name"]] = item["uniqueName"]
    else:
        for item in relics:
            result[item["name"]] = item["uniqueName"]
    
    return result

def get_sortie_missions(data) -> dict:
    """ Get sortie's info

    Args:
        data (dict): World state data of sortie

    Returns:
        dict: Full sortie data,
        dict: List of sortie missions.
    """
    result = {}
    result_option = []
    for item in data["variants"]:
        result[item["missionType"]] = item
        result_option.append(item["missionType"])
    return result, result_option


def get_invasions_rewards(data) -> dict:
    """ Get Invasion's rewards info

    Args:
        data (dict): World state data of Invasions


    Returns:
        dict: Dictionary of rewards
    """
    result = defaultdict(int)
    for invasion in data:
        if invasion["attacker"]["faction"] != "Infested":
            name, count = parse_item_string(invasion["attacker"]["reward"]["asString"])
            result[name] += count

        
        name, count = parse_item_string(invasion["defender"]["reward"]["asString"])
        result[name] += count

    return result


def get_market_item(url_path):
    """ Get warframe.market API data for item.

    Args:
        url_path (str): Item path.

    Returns:
        dict: Json of the Item found.
    """
    piece_list = warframe_market.get_market_item(url_path)
    if len(piece_list["payload"]["item"]["items_in_set"]) >1:
        for item in piece_list["payload"]["item"]["items_in_set"]:
            if item['en']['item_name'].lower().replace("(Key)","").replace(" ","_").replace("-","_") == url_path:
                return item
    return piece_list["payload"]["item"]["items_in_set"][0]


def get_craftable_info(name):
    """ Get craftable item and it's components.

    Args:
        unique_name (str): Item uniqueName

    Returns:
        dict: Full item and it's images location.
    """
    if "QuestKey" in name:
        name=name.replace("Blueprint","")
    result = warframe_status.craftable_request(name)

    if len(result)>0:
        if 'components' in result[0]:
            for component in result[0]["components"]:
                component["imageName"] = get_image_url(component["uniqueName"])
        return result[0]
    else:
        return None

def extract_craftable_components(json_data):
    """ Getting components of a craftable items.

    Args:
        json_data (dict): main item data.

    Returns:
        dict: item data with components data attach to it.
    """
    if 'components' in json_data:
        for component in json_data["components"]:
            component["imageName"] = get_image_url(component["uniqueName"])
    return json_data

def get_frame_abilities_with_image(frame):
    """ Get warframe abilities with the ability images.

    Args:
        frame (str): Frame's name.

    Returns:
        dict: Full frame data and it's ability images location.
    """
    result = warframe_status.abilities_request(frame)

    if len(result)>0:
        for ability in result[0]["abilities"]:
            ability["imageName"] = get_image_url(ability["uniqueName"])
        return result[0]
    else:
        return None

def extract_frame_abilities(json_data):
    """ Get warframe abilities with the ability images.

    Args:
        json_data (dict): frame's data.

    Returns:
        dict: abilities data.
    """
    for ability in json_data["abilities"]:
        ability["imageName"] = get_image_url(ability["uniqueName"])
    return {
        "passive": json_data["passiveDescription"] if "passiveDescription" in json_data else "",
        "abilities": json_data["abilities"]
        }

def get_item(unique_name):
    """ Get item data using warframe status API.

    Args:
        unique_name (str): Item uniqueName

    Returns:
        dict: Full item and it's images location.
    """
    if "QuestKey" in unique_name:
        unique_name = unique_name.split("/")[-1]
        unique_name=unique_name.replace("Blueprint","")
    
    result = warframe_status.item_request(unique_name)
    others_item = warframe_export.open_other()
    
    if len(result)>0:
        item = result[0]
        if item["category"] == "Relics":
            return get_relic(unique_name,True)
        else: 
            return item
    else:
        for export_item in others_item:
            if unique_name in export_item["uniqueName"]:
                return export_item
        return None
    

def get_item_name(unique_name):
    """ Get item name from uniqueName

    Args:
        unique_name (str): Item uniqueName

    Returns:
        str: Item name
    """ 

    result = get_item(unique_name)
    if result is not None:
        return result["name"]
    else:
        return ""


def call_market(option):
    """ Call warframe.market API for market inspection.

    Args:
        option (str): Market's item path.

    Returns:
        dict: Item's market data.
    """
    result = warframe_market.get_market_orders(option)['payload']['orders']
    sorted_orders = sorted(result, key=lambda x: x["platinum"])
    return sorted_orders

def get_reward_image(name) -> str:
    """ Get the material image from export API.

    Args:
        name (str): Either name or uniqueName of item

    Returns:
        bytes: ImageBytes
    """
    unique_name = name
    resoureces_json = warframe_export.open_resources()
    recipes_json = warframe_export.open_recipes()
    
    for item in recipes_json:
        if (name.replace(" ","") in item["uniqueName"]):
            unique_name = item["uniqueName"]
            break
    
    for item in resoureces_json:
        if (name in item["name"]):
            unique_name = item["uniqueName"]
            break
    if unique_name:
        img = get_image_url(unique_name)
    else:
        img = get_image_url(unique_name,False)
    
    if img == AppIcons.NO_IMAGE_DATA_URL.value:
        unique_name = warframe_status.item_request(name.replace(" Blueprint", ""),True)
        if len(unique_name)>0:
            img = get_image_url(unique_name[0]["uniqueName"])
        
    return img

def clean_event_data(data):
    """ Cleaning missing data from event API.

    Args:
        data (dict): json data of the event.

    Returns:
        dict: the cleaned data.
    """
    if 'currentScore' in data:
        pass
    else: 
        data['currentScore'] = 0
    
    if 'description' in data:
        pass
    else: 
        data['description'] = "No Description"
    
    if 'node' in data:
        pass
    else: 
        data['node'] = "No Data"
    return data

def get_ongoing_events():
    """ Call warframe status api for event data.

    Returns:
        dict: events data | None
    """
    response = warframe_status.ongoing_event_request()
    events = []
    if len(response)>0:
        for event in response:
            events.append(clean_event_data(event))
            
        sorted_event = sorted(
        [order for order in events ],
        key=lambda x: x["expiry"]
        )
        return sorted_event
    else:
        return None

def get_alerts_data():
    """ Call warframe status api for alert data.

    Returns:
        dict: alerts data | None
    """
    response = warframe_status.alert_request()
    if len(response) >0:
        sorted_alert = sorted(
        [order for order in response ],
        key=lambda x: x["expiry"]
        )
        return sorted_alert
    else:
        return None


def get_alert_reward(data):
    """ Getting alert rewards with their images.

    Args:
        data (dict): alert data.

    Returns:
        list: list of alert rewards.
    """
    reward = []
    if 'mission' in data:
        if 'reward' in data['mission']:
                if 'items' in data['mission']['reward']:
                    if len(data['mission']['reward']['items']) > 0:
                        for item in data['mission']['reward']['items']:
                            reward.append({
                                            "item": item,
                                            "image": item,
                                            "amount": 1
                                        })
                if 'countedItems' in data['mission']['reward']:
                    if len(data['mission']['reward']['countedItems']) > 0:
                        for item in data['mission']['reward']['countedItems']:
                            reward.append({
                                            "item": item['key'],
                                            "image": item['key'],
                                            "amount": item['count']
                                        })
                if 'credits' in data['mission']['reward']:
                    if data['mission']['reward']['credits'] > 0:
                        reward.append({
                                        "item": Warframe.CREDITS.value["name"],
                                        "image": Warframe.CREDITS.value["image"],
                                        "amount": data['mission']['reward']['credits']
                                        })
    return reward

@st.cache_data(ttl="30d",show_spinner=False)
def get_cached_items(item_ids):
    """ Getting all of the items aync by uniqueNames.

    Args:
        item_ids (list): list of uniqueNames.

    Returns:
        list: list of items.
    """
    return asyncio.run(warframe_status.fetch_all_items(item_ids))

def preload_data(data):
    """ Getting all of the baro/varzia items.

    Args:
        data (dict): baro/varzia data for filtering.

    Returns:
        list: list of items.
    """
    items = {
            "types" : [],
            "items" : []
    }
    ids = []
    progress_text = AppMessages.PROGRESS.value
    progress = st.progress(0, text=progress_text)
    with st.spinner(AppMessages.LOAD_DATA.value,show_time=True):
        for i, item in enumerate(data):
            if "M P V" in item["item"]:
                progress.progress((i+1)/len(data), text=f"""{(i+1)}/{len(data)} Items. Removing {item["item"]}""")
                continue
            else:
                ids.append({
                            "uniqueName": item["uniqueName"],
                            "ducats" : item["ducats"] if item["ducats"] is not None else 0,
                            "credits" : item["credits"] if item["credits"] is not None else 0,
                        })
            
                progress.progress((i+1)/len(data), text=f"""{(i+1)}/{len(data)} Items. Indexed: {item["item"]}""")
        
        items["items"] =get_cached_items(ids)

    progress.empty()
    return items

def clear_cached_item_call():
    """ 
        Clear cache for the get_cached_items() function.
    """
    get_cached_items.clear()

def get_all_tradables():
    """ Get all of the market items.

    Returns:
        dict: json response.
    """
    return warframe_market.get_market_items()

def get_item_by_name(name):
    """ Get item by name.

    Args:
        name (string): name of an item.

    Returns:
        dict: json data of the found item | None
    """
    result = warframe_status.item_request(name,search_by_name=True)
    if len(result)>0:
        for item in result:
            if name == item["name"]:
                return item 
        return result[0]
    else:
        return None

def get_news():
    """ API get news data.

    Returns:
        list: list of json data for news.
    """
    world_state=warframe_status.world_state_request()
    news = []
    if 'news' in world_state:
        if len(world_state["news"]) > 0:
            for new in world_state["news"]:
                if new["update"] == False and new["primeAccess"] == False and new["stream"] == False:
                    continue
                else:
                    news.append(new)
            
            news = sorted(
                [new for new in news ],
                key=lambda x: x["date"],reverse=True
                )
            
            return news
        else: return None

def get_cycles():
    """ API get cycles for open worlds.

    Returns:
        list: list of json data for open worlds.
    """
    world_state=warframe_status.world_state_request()
    cycles = [
                {
                    "name":"Cetus",
                    "data": world_state["cetusCycle"],
                    "image": get_image_url("/Lotus/Types/Items/MiscItems/PhotoboothTileEidolonLandscape",True)
                },
                {
                    "name":"Deimos",
                    "data": world_state["cambionCycle"],
                    "image": get_image_url("/Lotus/Types/Items/MiscItems/PhotoboothTileDeimosLandscape",True)
                },
                {
                    "name":"Zariman",
                    "data": world_state["zarimanCycle"],
                    "image": get_image_url("/Lotus/Types/Items/PhotoBooth/Zariman/PhotoboothTileZarAmphitheatre",True)
                },
                {
                    "name":"Fortuna",
                    "data": world_state["vallisCycle"],
                    "image": get_image_url("/Lotus/Types/Items/MiscItems/PhotoboothTileVenusLandscape",True)
                },
                {
                    "name":"Duviri",
                    "data": world_state["duviriCycle"],
                    "image": get_image_url("/Lotus/Types/Items/MiscItems/PhotoboothTileDuviriTeshinsCave",True)
                },
            ]
    return cycles

def get_rivens_settings():
    """ API for riven attribute list and item list

    Returns:
        tuple(list,list): combined data of riven default informations.
    """
    return warframe_market.get_market_riven_items(), warframe_market.get_market_riven_attributes()

def get_rivens(weapon_url_name, 
               buyout_policy=None,
               positive_stats=None,
               negative_stats=None,
               operation=None,
               re_rolls_min=None,
               re_rolls_max=None,
               polarity=None,
               status=None):
    """ API to get all riven auctions.

    Args:
        weapon_url_name (string): weapon url path.
        buyout_policy (string, optional): buyout policy. Defaults to None.
        positive_stats (list, optional): list positive attributes. Defaults to None.
        negative_stats (_type_, optional): list negative attributes. Defaults to None.
        operation (string, optional): not implemented. Defaults to None.
        re_rolls_min (int, optional): min reroll stat. Defaults to None.
        re_rolls_max (int, optional): max reroll stat. Defaults to None.
        polarity (string, optional): polarity of the riven. Defaults to None.

    Returns:
        list: list of riven | None.
    """
    if buyout_policy == "Buyout":
        buyout_policy = "direct"
    elif buyout_policy == "Auction":
        buyout_policy = "with"
    else:
        buyout_policy = None
    rivens = warframe_market.riven_search(weapon_url_name, buyout_policy, positive_stats, negative_stats,operation,re_rolls_min,re_rolls_max,polarity)
    filtered_list =[]
    if status is not None:
        if rivens is not None:
            if len(rivens) >0:
                for item in rivens:
                    if status in item["owner"]["status"]:
                        filtered_list.append(item)
                return filtered_list
    return rivens

def get_weapon_by_name(name):
    """ API for weapon data search by name.

    Args:
        name (string): weapon's name.

    Returns:
        dict: json data of weapon.
    """
    name = name.replace("_", " ")
    return warframe_status.get_weapon_by_name(name)

def get_event_rewards(data):
    """ Get event rewards.

    Args:
        data (dict): event json data.

    Returns:
        list: list of reward names.
    """
    rewards = []
    if "interimSteps" in data and len(data["interimSteps"])>0:
        for step in data["interimSteps"]:
            if "reward" in step:
                if "items" in step["reward"] and len(step["reward"]["items"])>0:
                    for item in step["reward"]["items"]:
                        rewards.append(item)

    if "rewards" in data and len(data["rewards"])>0:
        for reward in data["rewards"]:
            if "items" in reward and len(reward["items"])>0:
                for item in reward["items"]:
                    rewards.append(item)

    return rewards

@st.cache_data(ttl="10d",show_spinner=False)
def get_relics():
    relic_list = []
    relics = warframe_status.relics_request()
    if len(relics) < 1:
        return None
    else:
        for item in relics:
            if item["tradable"] == False or "Intact" not in item["name"]:
                continue
            relic_list.append(item)
        return relic_list

@st.cache_data(ttl="10d",show_spinner=False)
def get_resurgent_relics():
    relic_list = []
    items = get_variza()["inventory"]
    
    if len(items) < 1:
        return None
    else:
        for item in items:
            if "Projections" not in item["uniqueName"]:
                continue
            relic_list.append(item["uniqueName"])
        return relic_list


def filter_relic(data,rewards,types,tags,resurgent_data=None):
    filtered_relics = []
    type_map = tuple(types) if types else ("Axi", "Neo", "Meso", "Lith", "Requiem")

    # Determine if the vaulted filter should be applied
    ignore_vaulted = (tags[0] and tags[1]) or (not tags[0] and not tags[1])
    is_vaulted = None if ignore_vaulted else (True if tags[0] else False)

    for item in data:
        item = extract_relic_rewards(item)
        if item is None:
            continue
        conditions = []

        # Apply vaulted filter if not ignored
        if not ignore_vaulted:
            conditions.append(item.get("vaulted", False) == is_vaulted)

        # Apply resurgent data filter if not ignored
        if resurgent_data is not None:
            unique_name = item["uniqueName"].split("/")[-1]
            conditions.append(any(unique_name in x for x in resurgent_data))

        # If any condition is False, skip this relic
        if not all(conditions):
            continue

        # Filter by type
        if item["name"].startswith(type_map):
            filtered_relics.append(item)

    return filtered_relics