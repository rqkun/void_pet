import streamlit as st
from utils.icons import AppIcons

st.set_page_config(page_title="GTOME", page_icon=AppIcons.MAIN_APP.value,layout="wide")
home_page = st.Page("views/home.py", title="Home")

authenticated_pages = [home_page]
pg = st.navigation(authenticated_pages,position="hidden")
pg.run()