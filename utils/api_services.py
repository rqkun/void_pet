import requests
import streamlit as st

from config.constants import Warframe
import urllib.parse

def get_relic_data(unique_name):
    """ API request to get data by uniqueName. """
    request_ref = Warframe.STATUS.value["api"]+f"/items/{unique_name}?by=uniqueName&only=rewards,name"
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

def get_craftable(weapon_name):
    """API request to get craftable's component."""
    encoded_name = urllib.parse.quote(weapon_name, safe="")
    request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by=name&only=name,uniqueName,description,category,type,masteryReq,components"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

def get_relic_by_unique_name(unique_name):
    """API request to get craftable's component."""
    encoded_name = urllib.parse.quote(unique_name, safe="")
    request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by=uniqueName&only=rewards,name,description,vaulted"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

def get_relic_by_name(name):
    """API request to get craftable's component."""
    encoded_name = urllib.parse.quote(name, safe="")
    request_ref = Warframe.STATUS.value["api"]+f"/items/search/{encoded_name}?by=name&remove=abilities,components,patchlogs"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


def raise_detailed_error(request_object):
    """ Get details on http errors. """
    try:
        request_object.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(error, request_object.text)