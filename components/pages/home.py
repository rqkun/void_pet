import streamlit as st
from components import custom
from components.fragments import alert,event,invasion,world,baro
from config.constants import AppMessages, AppPages

custom.sideNav(0)
custom.reject_url_param()
custom.hover_effect()

baro.check()
world.show()
left,right = st.container(border=True).columns(2)
with left: event.show()
with right: alert.show()
invasion.show()
_,middle,_ = st.columns([2,3,2],vertical_alignment="center")
if middle.button("Go back",use_container_width=True,type='primary'):
    st.switch_page(AppPages.NOTFOUND.value)
