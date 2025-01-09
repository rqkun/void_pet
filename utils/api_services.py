import requests
import streamlit as st

def get_baro_data():
    request_ref = "https://api.warframestat.us/pc/voidTrader"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    return request_object.json()


def raise_detailed_error(request_object):
    """ Get details on http errors. """
    try:
        request_object.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(error, request_object.text)