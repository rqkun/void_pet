import requests
import streamlit as st
from components import custom
from components.integrations.discord import bots
from config.classes.exceptions import ResetBotFlag
from config.constants import AppIcons, AppPages, Warframe
import logging

from utils import api_services
def clear_session():
    if "rivens" in st.session_state:
        del st.session_state.rivens
    if "orders" in st.session_state:
        del st.session_state.orders
    if "relics" in st.session_state:
        del st.session_state.relics

st.set_page_config(page_title="Void Pet", page_icon=api_services.get_image(Warframe.AYA.value["image"]), layout="centered")
logging.basicConfig(level=logging.INFO)
custom.app_style()

home_page = st.Page(AppPages.HOME.value)
baro_page = st.Page(AppPages.BARO.value,url_path="/void")
regal_page = st.Page(AppPages.VARZIA.value,url_path="/vault")
news_page = st.Page(AppPages.NEWS.value)
rivens_page = st.Page(AppPages.RIVENS.value)
relics_page = st.Page(AppPages.RELICS.value)
market_page = st.Page(AppPages.MARKET.value)
error_page = st.Page(AppPages.ERROR.value,url_path="/500")
notfound_page = st.Page(AppPages.NOTFOUND.value,url_path="/404")
authenticated_pages = [home_page,baro_page,regal_page,market_page,news_page,rivens_page,relics_page,error_page,notfound_page]
pg = st.navigation(authenticated_pages,position="hidden")

#bot = bots.get_discord()

try:
    pg.run()
except (requests.exceptions.HTTPError,requests.exceptions.Timeout,requests.exceptions.ConnectionError) as error:
    clear_session()
    logging.error("; ".join(error.args))
    st.switch_page(AppPages.ERROR.value)
except ResetBotFlag:
    #bot.stop()
    clear_session()
    st.cache_data.clear()
    st.cache_resource.clear()
    logging.info("Reset caches, sessions and bot.")
    st.rerun(scope="app")