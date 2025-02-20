import streamlit_antd_components as sac
import streamlit as st
from components import custom
from config.constants import AppPages

custom.sideNav(0)
sac.result(label='505', description='Internal Server Error', status=500)
_,middle,_ = st.columns([2,3,2],vertical_alignment="center")
if middle.button("Reload",use_container_width=True,type='primary'):
    st.switch_page(AppPages.HOME.value)