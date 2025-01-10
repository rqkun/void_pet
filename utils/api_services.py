import requests
import streamlit as st



def get_baro_data():
    request_ref = f"{st.secrets.warframe_api.gateway}/pc/voidTrader"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

def get_varzia_data():
    request_ref = f"{st.secrets.warframe_api.gateway}/pc/vaultTrader"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

def get_relic_data(unique_name):
    request_ref = f"{st.secrets.warframe_api.gateway}/items/{unique_name}?by=uniqueName&only=rewards,name"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()

def get_market_orders(url_path):
    request_ref = f"{st.secrets.market_api.gateway}/items/{url_path}/orders"
    headers = {"accept": "application/json","Platform": "pc"}
    request_object = requests.get(request_ref,headers=headers)
    raise_detailed_error(request_object)
    return request_object.json()

def get_market_item(url_path):
    request_ref = f"{st.secrets.market_api.gateway}/items/{url_path}"
    headers = {"accept": "application/json","Platform": "pc"}
    request_object = requests.get(request_ref,headers=headers)
    raise_detailed_error(request_object)
    return request_object.json()

def raise_detailed_error(request_object):
    """ Get details on http errors. """
    try:
        request_object.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(error, request_object.text)