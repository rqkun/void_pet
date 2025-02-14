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
