import streamlit as st
from utils.icons import AppIcons

st.set_page_config(page_title="Void Pet", page_icon=AppIcons.MAIN_APP.value,layout="wide")
home_page = st.Page("views/home.py", title="Home",icon=AppIcons.HOME.value)
ware_page = st.Page("views/varzia.py", title="Browse Varzia Wares",icon=AppIcons.VARZIA.value)
error_page = st.Page("views/error.py", title="Not Found",url_path="/404")
authenticated_pages = [home_page,ware_page,error_page]
pg = st.navigation(authenticated_pages,position="hidden")
pg.run()