
import asyncio
import random
import requests
import urllib
from config.classes.parameters import WarframeStatusSearchParams
from config.constants import Warframe
from utils.api_services import raise_detailed_error
import streamlit as st
import httpx

from utils.tools import hash_func
from utils.tools import encode_identifier

@st.cache_data(ttl="1m",show_spinner=False)
def world(path=None):
    """ API request to get current world state data.
    Args:
        path(str):
            "events": "Current events",\n
            "alerts": "Active alerts",\n
            "news": "Active news",\n
            "voidTrader": "Baro Ki'Teer's inventory",\n
            "vaultTrader": "Varzia's prime vault",\n
            "invasions": "Ongoing invasions",\n
            "sortie": "Daily sortie mission",\n
            "cetusCycle": "Cetus day/night cycle",\n
            "vallisCycle": "Orb Vallis warm/cold cycle",\n
            "cambionCycle": "Cambion Drift Fass/Vome cycle",\n
            "zarimanCycle": "Zariman Grineer/Corpus cycle",\n
            "duviriCycle": "Duviri Joy/Anger/Envy/Sorrow/Fear cycle"\n
    Returns:
        dict: World state data
    """
    base_url = Warframe.STATUS.value["api"]
    route = f"/{path}" if path is not None else ""
    request_url = f"{base_url}/pc{route}?language=en"
    headers = {"accept": "application/json"}
    response = requests.get(request_url,headers=headers)
    raise_detailed_error(response)
    return response.json()

@st.cache_data(hash_funcs={WarframeStatusSearchParams: hash_func},ttl="1d",show_spinner=False)
def items(params:WarframeStatusSearchParams):
    """ API request to get item searchable data.

    Args:
        params (WarframeStatusSearchParams): The search parameters.

    Returns:
        list: List of items if found, otherwise empty.
    """
    encoded_key = encode_identifier(params.identifier)
    base_url = Warframe.STATUS.value["api"]
    query_string = params.to_query_string()
    request_url = f"{base_url}/{params.type}/search/{encoded_key}?{query_string}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url, headers=headers)
    raise_detailed_error(response)
    return response.json()


async def fetch_item(client, item_id, retries=3, SEMAPHORE=None):
    """Fetch item asynchronously with retries and concurrency limit."""
    async with SEMAPHORE:
        for attempt in range(retries):
            try:
                identifier = encode_identifier(item_id["uniqueName"],True)
                url = f"""{Warframe.STATUS.value["api"]}/items/search/{identifier}?by=uniqueName&remove=introduced,patchlogs"""
                
                response = await client.get(url, follow_redirects=True)
                
                if response.status_code == 200:
                    json_data = response.json()
                    if json_data:
                        result = json_data[0]
                        if "metadata" in item_id:
                            if "ducats" in item_id["metadata"]:
                                result["ducats"] = item_id["metadata"]["ducats"]
                            if "credits" in item_id["metadata"]:
                                result["credits"] = item_id["metadata"]["credits"]
                        return result
            
            except (httpx.HTTPStatusError, httpx.ReadTimeout, httpx.PoolTimeout) as e:
                wait_time = 2 ** attempt + random.uniform(0, 1)
                await asyncio.sleep(wait_time)

    return None # Return None if all retries fail

async def items_async(item_ids):
    """Fetch multiple items concurrently with error handling."""
    SEMAPHORE = asyncio.Semaphore(3)  # Reduce concurrency to ease API load
    async with httpx.AsyncClient(timeout=10) as client:  # Set a timeout
        tasks = [fetch_item(client, item_id, SEMAPHORE=SEMAPHORE) for item_id in item_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)  # Continue on failure
        return [res for res in results if res is not None] # Remove failed requests