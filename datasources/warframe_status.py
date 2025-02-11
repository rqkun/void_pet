
import requests
import urllib
from config.constants import Warframe
from utils.api_services import raise_detailed_error
import streamlit as st


@st.cache_data(ttl="1m",show_spinner=False)
def world_state_request():
    """ API request to get current world state data.

    Returns:
        dict: World state data
    """
    request_ref = Warframe.STATUS.value["api"]+"/pc"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


@st.cache_data(ttl="1m",show_spinner=False)
def void_traider_request():
    """ API request to get current baro's data.

    Returns:
        dict: Baro's data
    """
    request_ref = Warframe.STATUS.value["api"]+"/pc/voidTrader"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


@st.cache_data(ttl="1d",show_spinner=False)
def vault_traider_request():
    """ API request to get current varzia's data.

    Returns:
        dict: Varzia's data
    """
    request_ref = Warframe.STATUS.value["api"]+"/pc/vaultTrader"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

@st.cache_data(ttl="1d",show_spinner=False)
def prime_warframes_request():
    """ API request to get all prime warframes data.

    Returns:
        dict: Prime Warframes data,
    """
    request_ref = Warframe.STATUS.value["api"]+"/warframes/search/prime?only=name,category"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    
    return request_object.json()

@st.cache_data(ttl="1d",show_spinner=False)
def prime_weapons_request():
    """ API request to get all prime weapons data.

    Returns:
        dict: Prime Weapons data,
    """
    request_ref = Warframe.STATUS.value["api"]+"/weapons/search/prime?only=name,category"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    
    return request_object.json()

def relic_request(name, is_unique):
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

def item_request(unique_name, search_by_name=False):
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


def abilities_request(frame_name):
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


def craftable_request(item_name):
    """ API request to get craftable's component.

    Args:
        item_name (str): item's name

    Returns:
        dict: Item's data.
    """

    encoded_name = urllib.parse.quote(item_name, safe="")
    request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by=name"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


@st.cache_data(ttl="1h",show_spinner=False)
def ongoing_event_request():
    """ API request to get current events data.

    Returns:
        dict: Event state data
    """
    request_ref = Warframe.STATUS.value["api"]+"/pc/events"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

@st.cache_data(ttl="5m",show_spinner=False)
def alert_request():
    """ API request to get current alerts data.

    Returns:
        dict: Alert state data
    """
    request_ref = Warframe.STATUS.value["api"]+"/pc/alerts"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()
