import requests
import streamlit as st
from components import custom
from components.integrations.discord import bots
from config.classes.exceptions import ResetBotFlag
from config.constants import AppIcons, AppPages
import logging
from PIL import Image

from utils import data_manage

def clear_session():
    if "rivens" in st.session_state:
        del st.session_state.rivens
    if "orders" in st.session_state:
        del st.session_state.orders
    if "relics" in st.session_state:
        del st.session_state.relics
    data_manage.clear_cache()

st.set_page_config(page_title="Void-Pet", page_icon=Image.open(AppIcons.MAIN_APP.value), layout="centered")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
custom.app_style()

home_page = st.Page(AppPages.HOME.value)
baro_page = st.Page(AppPages.BARO.value,url_path="/void")
regal_page = st.Page(AppPages.VARZIA.value,url_path="/vault")
rivens_page = st.Page(AppPages.RIVENS.value)
relics_page = st.Page(AppPages.RELICS.value)
market_page = st.Page(AppPages.MARKET.value)
error_page = st.Page(AppPages.ERROR.value,url_path="/500")
notfound_page = st.Page(AppPages.NOTFOUND.value,url_path="/404")
authenticated_pages = [home_page,baro_page,regal_page,market_page,rivens_page,relics_page,error_page,notfound_page]
pg = st.navigation(authenticated_pages,position="hidden")

# bot = bots.start_bot()

try:
    pg.run()
except ResetBotFlag:
    # bot.stop()
    clear_session()
    bots.start_bot.clear()
    logging.info("Reset caches, sessions and bot.")
    st.rerun(scope="app")
except (requests.exceptions.HTTPError,requests.exceptions.Timeout,requests.exceptions.ConnectionError) as error:
    clear_session()
    error_message = "; ".join(error.args)
    logging.error(error_message)
    st.session_state.app_error = error_message
    st.switch_page(AppPages.ERROR.value)