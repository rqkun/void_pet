
import requests
import urllib
from config.constants import Warframe
from utils.api_services import raise_detailed_error
import streamlit as st


@st.cache_data(ttl="1m",show_spinner=False)
def get_world_state():
    """ API request to get current world state data. """
    request_ref = Warframe.STATUS.value["api"]+"/pc"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


@st.cache_data(ttl="1m",show_spinner=False)
def get_baro_data():
    """ API request to get Baro's data. """
    request_ref = Warframe.STATUS.value["api"]+"/pc/voidTrader"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


@st.cache_data(ttl="1m",show_spinner=False)
def get_varzia_data():
    """ API request to get Varzia's data. """
    request_ref = Warframe.STATUS.value["api"]+"/pc/vaultTrader"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

@st.cache_data(ttl="1d",show_spinner=False)
def get_all_prime_names():
    """ API request to get all Primes data. """
    request_ref = Warframe.STATUS.value["api"]+"/warframes/search/prime?only=name,category"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    
    weapon_request_ref = Warframe.STATUS.value["api"]+"/weapons/search/prime?only=name,category"
    weapon_request_object = requests.get(weapon_request_ref)
    raise_detailed_error(weapon_request_object)

    return request_object.json(), weapon_request_object.json()

def get_relic_by(name, is_unique):
    """API request to get craftable's component."""
    encoded_name = urllib.parse.quote(name, safe="")
    field = "name"
    if is_unique:
        field = "uniqueName"
    request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by={field}&only=type,category,rewards,name,uniqueName,description,vaulted"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

def get_item(unique_name):
    """ API request to get all matching item data. """
    identifier = unique_name.split("/")
    identifier = "/".join(identifier[len(identifier)-3:])
    encoded_name = urllib.parse.quote_plus(identifier, safe="")
    request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by=uniqueName&remove=abilities,components,patchlogs"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()