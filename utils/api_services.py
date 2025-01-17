import lzma
import requests
import streamlit as st

from config.constants import Warframe
import urllib.parse

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


def clean_prime_names(frame_json,weap_json):
    result = []
    for item in frame_json:
        result.append(item["name"])
    for item in weap_json:
        result.append(item["name"])
    return result

@st.cache_data(ttl="10m",show_spinner=False)
def get_all_prime_names():
    """ API request to get all Primes data. """
    request_ref = Warframe.STATUS.value["api"]+"/warframes/search/prime?only=name,category"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    
    weapon_request_ref = Warframe.STATUS.value["api"]+"/weapons/search/prime?only=name,category"
    weapon_request_object = requests.get(weapon_request_ref)
    raise_detailed_error(weapon_request_object)

    return clean_prime_names(request_object.json(),weapon_request_object.json())

def get_item_data(unique_name):
    """ API request to get all matching item data. """
    identifier = unique_name.split("/")
    identifier = "/".join(identifier[len(identifier)-3:])
    encoded_name = urllib.parse.quote_plus(identifier, safe="")
    request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by=uniqueName&remove=abilities,components,patchlogs"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)

    return request_object.json()

@st.cache_data(ttl="1d",show_spinner=False)
def get_manifest():
    """API request to get export manifest."""
    request_ref = "https://origin.warframe.com/PublicExport/index_en.txt.lzma"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    try:
        decompressed_data = lzma.decompress(request_object.content)
        manifest_list = decompressed_data.decode("utf-8")
        for item in manifest_list.split("\r\n"):
            if 'ExportManifest' in item:
                return item
        return "ExportManifest.json!00_N96OiP1NSlFN57WsfBeiPw" # backup
    except lzma.LZMAError as e:
        raise ValueError(f"Failed to decompress the LZMA file: {e}")

@st.cache_data(ttl="1d",show_spinner=False)
def get_public_image_export(file):
    """API request to get export manifest."""
    request_ref = Warframe.PUBLIC_EXPORT.value["api"] + f"/Manifest/{file}"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

def get_abilities(frame_name):
    """API request to get frame's abilities."""
    encoded_name = urllib.parse.quote(frame_name, safe="")
    request_ref = Warframe.STATUS.value["api"]+f"/warframes/search/{encoded_name}?by=name&only=abilities,uniqueName,passiveDescription"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

def raise_detailed_error(request_object):
    """ Get details on http errors. """
    try:
        request_object.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(error, request_object.text)