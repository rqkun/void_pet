import asyncio
import random
import httpx
import requests
from config.classes.parameters import RivenSearchParams
from config.constants import Warframe
from utils.api_services import raise_detailed_error
import streamlit as st

from utils.tools import hash_func

@st.cache_data(ttl="1m",show_spinner=False)
def items(url_path=None,order=False)-> dict:
    """API request to get item's orders.

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
    base_url = Warframe.MARKET_API.value["api"]
    request_url = f"{base_url}/items{path}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url,headers=headers)
    raise_detailed_error(response)
    return response.json()


@st.cache_data(ttl="7d",show_spinner=False)
def rivens_info(key:str):
    """API request to get riven items data.

    Returns:
        dict: All riven items data
    """
    if key not in ["items","attributes"]:
        raise ValueError("Riven API - Implemented key. (items, attributes)")
    base_url = Warframe.MARKET_API.value["api"]
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
    base_url = Warframe.MARKET_API.value["api"]
    query_string = params.to_query_string()
    request_url = f"{base_url}/auctions/search?{query_string}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url, headers=headers)
    raise_detailed_error(response)
    data = response.json()
    obj = data.get("payload", {}).get("auctions", [])
    return obj if obj else None

async def items_async(item_ids):
    """Fetch multiple items concurrently with error handling."""
    
    async def fetch_item(client, item_id:str, retries=3, SEMAPHORE=None):
        """Fetch item asynchronously with retries and concurrency limit."""
        async with SEMAPHORE:
            for attempt in range(retries):
                try:
                    path = f"""{Warframe.MARKET_API.value["api"]}/items/{item_id.replace("&", "and")}/orders?include=item"""
                    headers = {"accept": "application/json",'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                    if "excalibur" in item_id:
                        continue
                    response = await client.get(path, headers=headers,follow_redirects=True)
                    if response.status_code == 200:
                        list_included:list = []
                        img_link = ""
                        if "include" in response.json():
                            if "item" in response.json()["include"]:
                                list_included:list = response.json()["include"]["item"].get("items_in_set",[])
                                for item in list_included:
                                    if item.get("set_root",False):
                                        img_link = item["en"].get("icon","")
                                        break
                                        
                        
                        return{
                            "url": item_id,
                            "img_link": img_link,
                            "orders": response.json()["payload"]["orders"]
                        }
                
                except (httpx.HTTPStatusError, httpx.ReadTimeout, httpx.PoolTimeout) as e:
                    wait_time = 2 ** attempt + random.uniform(0, 1)
                    await asyncio.sleep(wait_time)

        return None # Return None if all retries fail
    
    SEMAPHORE = asyncio.Semaphore(3)  # Reduce concurrency to ease API load
    async with httpx.AsyncClient(timeout=10) as client:  # Set a timeout
        tasks = [fetch_item(client, item_id, SEMAPHORE=SEMAPHORE) for item_id in item_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)  # Continue on failure
        return [res for res in results if res is not None] # Remove failed requests