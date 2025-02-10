
import requests
import urllib
from config.constants import Warframe
from utils.api_services import raise_detailed_error
import streamlit as st


@st.cache_data(ttl="1m",show_spinner=False)
def get_world_state():
    """ API request to get current world state data.

    Returns:
        dict: World state data
    """
    request_ref = Warframe.STATUS.value["api"]+"/pc"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


@st.cache_data(ttl="1m",show_spinner=False)
def get_baro_data():
    """ API request to get current baro's data.

    Returns:
        dict: Baro's data
    """
    request_ref = Warframe.STATUS.value["api"]+"/pc/voidTrader"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


@st.cache_data(ttl="1d",show_spinner=False)
def get_varzia_data():
    """ API request to get current varzia's data.

    Returns:
        dict: Varzia's data
    """
    request_ref = Warframe.STATUS.value["api"]+"/pc/vaultTrader"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

@st.cache_data(ttl="1d",show_spinner=False)
def get_all_prime_names():
    """ API request to get all primes data.

    Returns:
        dict: Prime Warframes data,
        dict: Prime weapons data.
    """
    request_ref = Warframe.STATUS.value["api"]+"/warframes/search/prime?only=name,category"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    
    weapon_request_ref = Warframe.STATUS.value["api"]+"/weapons/search/prime?only=name,category"
    weapon_request_object = requests.get(weapon_request_ref)
    raise_detailed_error(weapon_request_object)

    return request_object.json(), weapon_request_object.json()

def get_relic_by(name, is_unique):
    """ API request to get a relic's data.
    Args:
        name (str): relic uniqueName or name.
        is_unique (bool): is name arg uniqueName.

    Returns:
        dict: Relic's data.
    """
    encoded_name = urllib.parse.quote(name, safe="")
    field = "name"
    if is_unique:
        field = "uniqueName"
    request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by={field}&only=type,category,rewards,name,uniqueName,description,vaulted"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

def get_item(unique_name, search_by_name=False):
    """ API request to get all matching item data.

    Args:
        unique_name (str): Item's uniqueName

    Returns:
        dict: Item's data.
    """
    if search_by_name:
        encoded_name = urllib.parse.quote_plus(unique_name, safe="")
        request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by=name&remove=abilities,components,patchlogs"
    else:
        identifier = unique_name.split("/")
        identifier = "/".join(identifier[len(identifier)-3:])
        encoded_name = urllib.parse.quote_plus(identifier, safe="")
        request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by=uniqueName&remove=abilities,components,patchlogs"
        
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


def get_abilities(frame_name):
    """ API request to get frame's abilities.

    Args:
        frame_name (str): Frame's name

    Returns:
        dict: Frame's data.
    """
    encoded_name = urllib.parse.quote(frame_name, safe="")
    request_ref = Warframe.STATUS.value["api"]+f"/warframes/search/{encoded_name}?by=name&only=abilities,uniqueName,passiveDescription"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


def get_craftable(item_name):
    """ API request to get craftable's component.

    Args:
        item_name (str): item's name

    Returns:
        dict: Item's data.
    """

    encoded_name = urllib.parse.quote(item_name, safe="")
    request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by=name&only=name,uniqueName,description,category,type,masteryReq,components"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()