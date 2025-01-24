from collections import defaultdict
import streamlit as st
from config import structures
from config.constants import Warframe
from datasources import warframe_export,warframe_market,warframe_status
from utils import tools
from utils.tools import parse_item_string

def get_image(unique_name) -> str:
    """ Return image url from export.

    Args:
        unique_name (str): the identifier of an item.

    Returns:
        str: Item image url.
    """
    if 'image_manifest' not in st.session_state:
        st.session_state.image_manifest = warframe_export.open_manifest()
    identifier = unique_name.split("/")
    identifier = "/".join(identifier[len(identifier)-3:])
    for item in st.session_state.image_manifest:
        if identifier in item["uniqueName"]:
            return Warframe.PUBLIC_EXPORT.value["api"] + item["textureLocation"]
    return "https://static.wikia.nocookie.net/warframe/images/4/46/Void.png"

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
        
    relic = warframe_status.get_relic_by(identifier, is_unique)[0]
    
    relic_export = export_relic(identifier,field)
    for i,item in enumerate(relic["rewards"]):
        item["item"]["uniqueName"] = relic_export["relicRewards"][i]["rewardName"]
        item["item"]["imageName"] = get_image(relic_export["relicRewards"][i]["rewardName"])
    return relic

def get_variza():
    """ Call the warframe status api for varzia data.

    Returns:
        dict: Json data of the api response.
    """
    return warframe_status.get_varzia_data()

def get_baro():
    """ Call the warframe status api for baro data.

    Returns:
        dict: Json data of the api response.
    """
    return warframe_status.get_baro_data()

def get_world_state():
    """ Call the warframe status api for world state data.

    Returns:
        dict: Json data of the api response.
    """
    return warframe_status.get_world_state()

def get_prime_list() -> list:
    """ Call the warframe status api for list of primes.

    Returns:
        list: A clean prime names list.
    """
    p_frame, p_weapon = warframe_status.get_all_prime_names()
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
    for item in piece_list["payload"]["item"]["items_in_set"]:
        if item['en']['item_name'].lower().replace(" ","_") == url_path:
            return item


def get_craftable_info(unique_name):
    """ Get craftable item and it's components.

    Args:
        unique_name (str): Item uniqueName

    Returns:
        dict: Full item and it's images location.
    """
    if "QuestKey" in unique_name:
        unique_name=unique_name.replace("Blueprint","")
    result = warframe_status.get_craftable(unique_name)

    if len(result)==0:
        return {}
    else:
        for component in result[0]["components"]:
            component["imageName"] = get_image(component["uniqueName"])
        return result


def get_frame_abilities_with_image(frame):
    """ Get warframe abilities with the ability images.

    Args:
        frame (str): Frame's name.

    Returns:
        dict: Full frame data and it's ability images location.
    """
    result = warframe_status.get_abilities(frame)

    if len(result) ==0:
        return {}
    else:
        for ability in result[0]["abilities"]:
            ability["imageName"] = get_image(ability["uniqueName"])
        return result

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
    item = warframe_status.get_item(unique_name)[0]
    if item["category"] == "Relics":
        return get_relic(unique_name,True)
    else: 
        return item

def get_item_name(unique_name):
    """ Get item name from uniqueName

    Args:
        unique_name (str): Item uniqueName

    Returns:
        str: Item name
    """ 
    if "QuestKey" in unique_name:
        unique_name = unique_name.split("/")[-1]
        unique_name=unique_name.replace("Blueprint","")
    return warframe_status.get_item(unique_name)[0]["name"]


@st.cache_data(show_spinner=False)
def call_market(option):
    """ Call warframe.market API for market inspection.

    Args:
        option (str): Market's item path.

    Returns:
        dict: Item's market data.
    """
    return warframe_market.get_market_orders(option)['payload']['orders']