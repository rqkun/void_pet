import requests
import streamlit as st

from config.constants import Warframe
from utils import data_tools

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

def get_relic_data(unique_name):
    """ API request to get data by uniqueName. """
    request_ref = Warframe.STATUS.value["api"]+f"/items/{unique_name}?by=uniqueName&only=rewards,name"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

def get_market_orders(url_path):
    """ API request to get item's orders. """
    request_ref = Warframe.MARKET.value["api"]+f"/items/{url_path}/orders"
    headers = {"accept": "application/json","Platform": "pc"}
    request_object = requests.get(request_ref,headers=headers)
    raise_detailed_error(request_object)
    return request_object.json()

def get_market_item(url_path):
    """ API request to get market item's data. """
    request_ref = Warframe.MARKET.value["api"]+f"/items/{url_path}"
    headers = {"accept": "application/json","Platform": "pc"}
    request_object = requests.get(request_ref,headers=headers)
    raise_detailed_error(request_object)
    return request_object.json()

@st.cache_data(ttl="10m",show_spinner=False)
def get_all_prime_names():
    """ API request to get all Primes data. """
    request_ref = Warframe.STATUS.value["api"]+"/warframes/search/prime?only=name,category"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    
    weapon_request_ref = Warframe.STATUS.value["api"]+"/weapons/search/prime?only=name,category"
    weapon_request_object = requests.get(weapon_request_ref)
    raise_detailed_error(weapon_request_object)

    return data_tools.clean_prime_names(request_object.json(),weapon_request_object.json())
    
    
def raise_detailed_error(request_object):
    """ Get details on http errors. """
    try:
        request_object.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(error, request_object.text)