
import asyncio
import random
import re
import requests
import urllib
from config.classes import WarframeStatusSearchParams
from config.constants import Warframe
from utils.api_services import raise_detailed_error
import streamlit as st
import httpx

from utils.tools import hash_func

@st.cache_data(ttl="1m",show_spinner=False)
def world(path=None):
    """ API request to get current world state data.
    Args:
        path(str):
            "events": "Current events",
            "alerts": "Active alerts",
            "news": "Active news",
            "voidTrader": "Baro Ki'Teer's inventory",
            "vaultTrader": "Varzia's prime vault",
            "invasions": "Ongoing invasions",
            "sortie": "Daily sortie mission",
            "cetusCycle": "Cetus day/night cycle",
            "vallisCycle": "Orb Vallis warm/cold cycle",
            "cambionCycle": "Cambion Drift Fass/Vome cycle",
            "zarimanCycle": "Zariman Grineer/Corpus cycle",
            "duviriCycle": "Duviri Joy/Anger/Envy/Sorrow/Fear cycle"
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
    if " and " in params.identifier:
        params.identifier = params.identifier.replace(" and ", " & ")
    name = re.sub(r'\s*\(.*?\)', '', params.identifier)
    encoded_key = urllib.parse.quote_plus(name, safe="")
    base_url = Warframe.STATUS.value["api"]
    query_string = params.to_query_string()
    request_url = f"{base_url}/{params.type}/search/{encoded_key}?{query_string}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url, headers=headers)
    raise_detailed_error(response)
    return response.json()


async def items_async(client, item_id, retries=3, SEMAPHORE=None):
    """Fetch item asynchronously with retries and concurrency limit."""
    async with SEMAPHORE:
        for attempt in range(retries):
            try:
                identifier = item_id["uniqueName"].split("/")[-1]
                encoded_name = urllib.parse.quote_plus(identifier, safe="")
                url = Warframe.STATUS.value["api"] + f"/items/search/{encoded_name}?by=uniqueName&remove=introduced,patchlogs"
                
                response = await client.get(url, follow_redirects=True)
                
                if response.status_code == 200:
                    json_data = response.json()
                    if json_data:
                        result = json_data[0]
                        result["ducats"] = item_id["ducats"]
                        result["credits"] = item_id["credits"]
                        return result
            
            except (httpx.HTTPStatusError, httpx.ReadTimeout, httpx.PoolTimeout) as e:
                wait_time = 2 ** attempt + random.uniform(0, 1)
                await asyncio.sleep(wait_time)

    return None # Return None if all retries fail

async def fetch_all_items(item_ids):
    """Fetch multiple items concurrently with error handling."""
    SEMAPHORE = asyncio.Semaphore(3)  # Reduce concurrency to ease API load
    async with httpx.AsyncClient(timeout=10) as client:  # Set a timeout
        tasks = [items_async(client, item_id, SEMAPHORE=SEMAPHORE) for item_id in item_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)  # Continue on failure
        return [res for res in results if res is not None] # Remove failed requests