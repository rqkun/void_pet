import requests
import streamlit as st
from components import custom
from config.constants import AppIcons, AppPages

st.set_page_config(page_title="Void Pet", page_icon=AppIcons.MAIN_APP.value, layout="centered")

custom.app_style()

home_page = st.Page(AppPages.HOME.value)
baro_page = st.Page(AppPages.BARO.value)
regal_page = st.Page(AppPages.VARZIA.value)
news_page = st.Page(AppPages.NEWS.value)
rivens_page = st.Page(AppPages.RIVENS.value)
relics_page = st.Page(AppPages.RELICS.value)
market_page = st.Page(AppPages.MARKET.value)
error_page = st.Page(AppPages.ERROR.value,url_path="/500")
notfound_page = st.Page(AppPages.NOTFOUND.value,url_path="/404")
authenticated_pages = [home_page,baro_page,regal_page,market_page,news_page,rivens_page,relics_page,error_page,notfound_page]
pg = st.navigation(authenticated_pages,position="hidden")

try:
    pg.run()
except (requests.exceptions.HTTPError,requests.exceptions.Timeout,requests.exceptions.ConnectionError) as error:
    if "rivens" in st.session_state:
        del st.session_state.rivens
    if "orders" in st.session_state:
        del st.session_state.orders
    st.switch_page(AppPages.ERROR.value)