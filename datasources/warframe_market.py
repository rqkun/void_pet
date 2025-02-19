import requests
from config.constants import Warframe
from utils.api_services import raise_detailed_error
import streamlit as st

def get_market_orders(url_path):
    """ API request to get item's orders.

    Args:
        url_path (str): warframe.market Item path.

    Returns:
        dict: Orders data
    """
    request_ref = Warframe.MARKET.value["api"]+f"/items/{url_path}/orders"
    headers = {"accept": "application/json","Platform": "pc"}
    request_object = requests.get(request_ref,headers=headers)
    raise_detailed_error(request_object)
    return request_object.json()

@st.cache_data(ttl="1d",show_spinner=False)
def get_market_item(url_path):
    """ API request to get item's data.

    Args:
        url_path (str): warframe.market Item path.

    Returns:
        dict: Item's data
    """
    request_ref = Warframe.MARKET.value["api"]+f"/items/{url_path}"
    headers = {"accept": "application/json","Platform": "pc"}
    request_object = requests.get(request_ref,headers=headers)
    raise_detailed_error(request_object)
    return request_object.json()

@st.cache_data(ttl="1d",show_spinner=False)
def get_market_items():
    """ API request to get item's data.

    Returns:
        dict: All tradable items data
    """
    request_ref = Warframe.MARKET.value["api"]+f"/items"
    headers = {"accept": "application/json"}
    request_object = requests.get(request_ref,headers=headers)
    raise_detailed_error(request_object)
    return request_object.json()

@st.cache_data(ttl="7d",show_spinner=False)
def get_market_riven_items():
    """ API request to get riven items data.

    Returns:
        dict: All riven items data
    """
    request_ref = Warframe.MARKET.value["api"]+f"/riven/items"
    headers = {"accept": "application/json"}
    request_object = requests.get(request_ref,headers=headers)
    raise_detailed_error(request_object)
    if "payload" in request_object.json():
        if "items" in request_object.json()["payload"]:
            return request_object.json()["payload"]["items"]
    return None

@st.cache_data(ttl="7d",show_spinner=False)
def get_market_riven_attributes():
    """ API request to get riven attribute data.

    Returns:
        dict: All riven attributes data
    """
    request_ref = Warframe.MARKET.value["api"]+f"/riven/attributes"
    headers = {"accept": "application/json"}
    request_object = requests.get(request_ref,headers=headers)
    raise_detailed_error(request_object)
    if "payload" in request_object.json():
        if "attributes" in request_object.json()["payload"]:
            return request_object.json()["payload"]["attributes"]
    return None

def riven_search(weapon_url_name, buyout_policy=None, positive_stats=None, negative_stats=None,operation=None,re_rolls_min=None,re_rolls_max=None,polarity=None):
    """ API request to get riven attribute data.

    Returns:
        dict: All riven attributes data
    """
    filters = ""
    if buyout_policy is not None:
        filters = filters + f"&buyout_policy={buyout_policy}"
    if positive_stats is not None:
        if len(positive_stats) >0:
            if len(positive_stats)>1:
                positive_query = ",".join(positive_stats)
            elif len(positive_stats)==1:
                positive_query = positive_stats[0]
            filters = filters + f"&positive_stats={positive_query}"
    if negative_stats is not None:
        if len(negative_stats) >0:
            if len(negative_stats) >1:
                negative_query = ",".join(negative_stats)
            elif len(negative_stats)== 1:
                negative_query = negative_stats[0]
            filters = filters + f"&negative_stats={negative_query}"
    if operation is not None:
        filters = filters + f"&operation={operation}"
    if re_rolls_min is not None:
        filters = filters + f"&re_rolls_min={re_rolls_min}"
    if re_rolls_max is not None:
        filters = filters + f"&re_rolls_max={re_rolls_max}"
    if polarity is not None:
        filters = filters + f"&polarity={polarity}"

    request_ref = Warframe.MARKET.value["api"]+f"/auctions/search?type=riven&weapon_url_name={weapon_url_name}{filters}&sort_by=price_asc"
    headers = {"accept": "application/json"}
    request_object = requests.get(request_ref,headers=headers)
    raise_detailed_error(request_object)
    if "payload" in request_object.json():
        if "auctions" in request_object.json()["payload"]:
            if len(request_object.json()["payload"]["auctions"]) >0:
                return request_object.json()["payload"]["auctions"]
    return None