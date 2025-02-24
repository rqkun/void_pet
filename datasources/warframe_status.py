
import asyncio
import random
import re
import requests
import urllib
from config.constants import Warframe
from utils.api_services import raise_detailed_error
import streamlit as st
import httpx

@st.cache_data(ttl="1m",show_spinner=False)
def world_state_request():
    """ API request to get current world state data.

    Returns:
        dict: World state data
    """
    request_ref = Warframe.STATUS.value["api"]+"/pc?language=en"
    request_object = requests.get(request_ref,timeout=5)
    raise_detailed_error(request_object)
    return request_object.json()


@st.cache_data(ttl="1m",show_spinner=False)
def void_traider_request():
    """ API request to get current baro's data.

    Returns:
        dict: Baro's data
    """
    request_ref = Warframe.STATUS.value["api"]+"/pc/voidTrader?language=en"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


@st.cache_data(ttl="1d",show_spinner=False)
def vault_traider_request():
    """ API request to get current varzia's data.

    Returns:
        dict: Varzia's data
    """
    request_ref = Warframe.STATUS.value["api"]+"/pc/vaultTrader?language=en"
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
        encoded_name = urllib.parse.quote(unique_name)
        request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by=name&remove=patchlogs"
    else:
        identifier = unique_name.split("/")
        identifier = "/".join(identifier[len(identifier)-3:])
        encoded_name = urllib.parse.quote_plus(identifier, safe="")
        request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by=uniqueName&remove=patchlogs"
        
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
    request_ref = Warframe.STATUS.value["api"]+"/pc/events?language=en"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

@st.cache_data(ttl="5m",show_spinner=False)
def alert_request():
    """ API request to get current alerts data.

    Returns:
        dict: Alert state data
    """
    request_ref = Warframe.STATUS.value["api"]+"/pc/alerts?language=en"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


async def fetch_item(client, item_id, retries=3, SEMAPHORE=None):
    """Fetch item asynchronously with retries and concurrency limit."""
    async with SEMAPHORE:
        for attempt in range(retries):
            try:
                identifier = item_id["uniqueName"].split("/")
                identifier = "/".join(identifier[-3:])
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
        tasks = [fetch_item(client, item_id, SEMAPHORE=SEMAPHORE) for item_id in item_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)  # Continue on failure
        return [res for res in results if res is not None] # Remove failed requests

def get_weapon_by_name(name):
    """ Search weapon by name """
    if " and " in name:
        name = name.replace(" and ", " & ")
    name = re.sub(r'\s*\(.*?\)', '', name)
    encoded_name = urllib.parse.quote(name)
    request_ref = Warframe.STATUS.value["api"]+f"/weapons/search/{encoded_name}?by=name&remove=patchlogs"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    if len(request_object.json()) < 1:
        return None
    else:
        for item in request_object.json():
            if item["name"].lower() == name:
                return item
        return request_object.json()[0]

def relics_request():
    """ Search weapon by name """
    request_ref = Warframe.STATUS.value["api"]+"/items/search/Relic?by=type&remove=patchlogs"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

def requiem_request():
    """ Search requiem relics. """
    request_ref = Warframe.STATUS.value["api"]+"/items/search/Requiem?by=name&remove=patchlogs"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()