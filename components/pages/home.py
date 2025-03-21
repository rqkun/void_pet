import streamlit as st
from components import custom
from components.fragments import alert,event,invasion, news,world,baro

custom.sideNav(0)
custom.reject_url_param()
custom.world_style()
baro.check()
world.show()
left,right = st.container(border=True).columns(2)
with left: event.show()
with right: alert.show()
invasion.show()
news.show()