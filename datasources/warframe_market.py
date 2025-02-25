import requests
from config.classes import RivenSearchParams
from config.constants import Warframe
from utils.api_services import raise_detailed_error
import streamlit as st

from utils.tools import hash_func

@st.cache_data(ttl="1m",show_spinner=False)
def items(url_path=None,order=False)-> dict:
    """ API request to get item's orders.

    Args:
        url_path (str): warframe.market Item path.

    Returns:
        dict: Orders data
    """
    if url_path is not None:
        order_req = "/orders" if order else ""
        path = f"/{url_path}{order_req}"
    else:
        path =""
    base_url = Warframe.MARKET.value["api"]
    request_url = f"{base_url}/items{path}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url,headers=headers)
    raise_detailed_error(response)
    return response.json()


@st.cache_data(ttl="7d",show_spinner=False)
def rivens_info(key:str):
    """ API request to get riven items data.

    Returns:
        dict: All riven items data
    """
    if key not in ["items","attributes"]:
        raise ValueError("Riven API - Implemented key. (items, attributes)")
    base_url = Warframe.MARKET.value["api"]
    request_url = f"{base_url}/riven/{key}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url,headers=headers)
    raise_detailed_error(response)
    data = response.json()
    obj = data.get("payload", {}).get(key, [])
    return obj if obj else None


@st.cache_data(hash_funcs={RivenSearchParams: hash_func},ttl="1m",show_spinner=False)
def rivens_auction(params:RivenSearchParams):
    """
    API request to get riven attribute data.

    Args:
        params (RivenSearchParams): The search parameters.

    Returns:
        list or None: List of auctions if found, otherwise None.
    """
    base_url = Warframe.MARKET.value["api"]
    query_string = params.to_query_string()
    request_url = f"{base_url}/auctions/search?{query_string}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url, headers=headers)
    raise_detailed_error(response)
    data = response.json()
    obj = data.get("payload", {}).get("auctions", [])
    return obj if obj else None
