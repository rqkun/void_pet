from collections import defaultdict
import re
import streamlit as st
from config import structures
from config.constants import Warframe
from datasources import warframe_export,warframe_market,warframe_status
from utils import api_services, data_tools
from utils.data_tools import parse_item_string

def get_image(uniqueName):
    if 'image_manifest' not in st.session_state:
        st.session_state.image_manifest = warframe_export.open_manifest()
    identifier = uniqueName.split("/")
    identifier = "/".join(identifier[len(identifier)-3:])
    for item in st.session_state.image_manifest:
        if identifier in item["uniqueName"]:
            return Warframe.PUBLIC_EXPORT.value["api"] + item["textureLocation"]
    return "https://static.wikia.nocookie.net/warframe/images/4/46/Void.png"

    # for item in st.session_state.image_manifest:
    #     uniqueName = re.sub(r'\bNeuroptics\b', 'Helmet', uniqueName, flags=re.IGNORECASE)
    #     if uniqueName.replace(" ","") in item["uniqueName"] or transform_string(uniqueName) in item["uniqueName"]:
    #         return Warframe.PUBLIC_EXPORT.value["api"] + item["textureLocation"]
    
    # return "https://static.wikia.nocookie.net/warframe/images/4/46/Void.png"

def export_relic(name,field):
    local_relic_data = warframe_export.open_relic_arcane()
    for item in local_relic_data:
        if name in item[field]:
            return item

def get_relic_reward(relic):
    """ Return relic's rewards dictionary. """
    relic_option={}

    if relic is None:
        return None
    for item in relic["rewards"]:
        value = structures.relic_reward_object(item["chance"],item["rarity"],item["item"]["name"],item["item"]["imageName"])
        if 'Forma Blueprint' not in item["item"]["name"]:
            relic_option[item["item"]["name"]] = value
    return relic_option

def get_relic(name, is_unique):
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
    return warframe_status.get_varzia_data()

def get_world_state():
    return warframe_status.get_world_state()

def get_prime_list():
    p_frame, p_weapon = warframe_status.get_all_prime_names()
    return data_tools.clean_prime_names(p_frame, p_weapon)

def get_prime_resurgent_list(primes,relics_list):
    result = []
    prime = get_prime_list()
    for prime in primes:
        rewards = search_rewards(prime,relics_list)
        if len(rewards)>0:
            result.append(prime)
    return result

def search_rewards(search_key,relics):
    """ Return relic that have search_keys as reward(s). """
    result = {}
    if search_key != "" and len(relics) :
        search_key = "_"+search_key.lower().replace(" ", "_")
        for item in relics:
            if any(search_key in "_"+reward["item"]["name"].lower().replace(" ", "_") for reward in item["rewards"]):
                result[item["name"]] = item["uniqueName"]
               # break  # No need to check further rewards for this key
        
    else:
        for item in relics:
            result[item["name"]] = item["uniqueName"]
    
    return result

def get_sortie_missions(data):
    result = {}
    result_option = []
    for item in data["variants"]:
        result[item["missionType"]] = item
        result_option.append(item["missionType"])
    return result, result_option


def get_invasions_rewards(data):
    result = defaultdict(int)
    for invasion in data:
        if invasion["attacker"]["faction"] != "Infested":
            name, count = parse_item_string(invasion["attacker"]["reward"]["asString"])
            result[name] += count

        
        name, count = parse_item_string(invasion["defender"]["reward"]["asString"])
        result[name] += count

    return result


def get_market_item(url_path):
    piece_list = warframe_market.get_market_item(url_path)
    for item in piece_list["payload"]["item"]["items_in_set"]:
        if item['en']['item_name'].lower().replace(" ","_") == url_path:
            return item


def get_craftable_info(weapon):
    result = api_services.get_craftable(weapon)

    if len(result)==0:
        return {}
    else:
        for component in result[0]["components"]:
            component["imageName"] = get_image(component["uniqueName"])
        return result


def get_frame_abilities_with_image(frame):
    result = api_services.get_abilities(frame)

    if len(result) ==0:
        return {}
    else:
        for ability in result[0]["abilities"]:
            ability["imageName"] = get_image(ability["uniqueName"])
        return result

def get_item(unique_name):
    item = warframe_status.get_item(unique_name)[0]
    if item["category"] == "Relics":
        return get_relic(unique_name,True)
    else: 
        return item

def get_item_name(unique_name):
    return warframe_status.get_item(unique_name)[0]["name"]