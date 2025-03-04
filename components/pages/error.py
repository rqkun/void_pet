import streamlit_antd_components as sac
import streamlit as st
from components import custom
from config.constants import AppIcons, AppPages

custom.sideNav(0)

sac.result(label='505', description='Internal Server Error', status=500)
_,middle,_ = st.columns([2,3,2],vertical_alignment="center")
reload_btn = middle.button("Reload",use_container_width=True,type='primary')
    
if 'app_error' in st.session_state:
    st.toast(st.session_state.app_error,icon=AppIcons.ERROR.value)
if reload_btn:
    if 'app_error' in st.session_state:
        del st.session_state.app_error
    st.switch_page(AppPages.HOME.value)