import streamlit as st
from components.markdowns import hide_streamlit_header
from config.constants import AppIcons, AppPages

st.set_page_config(page_title="Void Pet", page_icon=AppIcons.MAIN_APP.value)

hide_streamlit_style = hide_streamlit_header()

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if 'not_baro_time' in st.session_state:
    st.toast(st.session_state.not_baro_time)
    del st.session_state.not_baro_time

home_page = st.Page(AppPages.HOME.value)
varzia_page = st.Page(AppPages.AYA.value)
baro_page = st.Page(AppPages.BARO.value)
regal_page = st.Page(AppPages.VARZIA.value)
error_page = st.Page(AppPages.ERROR.value, url_path="/not_found")
authenticated_pages = [home_page,varzia_page,baro_page,error_page,regal_page]
pg = st.navigation(authenticated_pages,position="hidden")
st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")
pg.run()