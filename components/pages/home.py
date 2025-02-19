import streamlit as st
from components import custom
from components.fragments import alert,event,invasion,world,baro

custom.sideNav(0)

baro.check()
custom.hover_effect()

world.show()
left,right = st.container(border=True).columns(2)
with left: event.show()
with right: alert.show()
invasion.show()
