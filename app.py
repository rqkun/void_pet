import streamlit as st
from config.constants import AppIcons, AppMessages, AppPages
from utils import data_tools

if 'image_manifest' not in st.session_state:
    with st.spinner(AppMessages.LOAD_DATA.value):
        st.session_state.image_manifest = data_tools.get_public_image_export()["Manifest"]
    st.rerun()
else:
    st.set_page_config(page_title="Void Pet", page_icon=AppIcons.MAIN_APP.value,layout="wide")
    home_page = st.Page(AppPages.HOME.value, icon=AppIcons.HOME.value)
    varzia_page = st.Page(AppPages.VARZIA.value, icon=AppIcons.VARZIA.value)
    baro_page = st.Page(AppPages.BARO.value, icon=AppIcons.BARO.value)
    error_page = st.Page(AppPages.ERROR.value, icon=AppIcons.ERROR.value,url_path="/not_found")
    authenticated_pages = [home_page,varzia_page,baro_page,error_page]
    pg = st.navigation(authenticated_pages,position="hidden")
    pg.run()