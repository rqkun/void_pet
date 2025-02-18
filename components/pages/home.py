import streamlit as st
from components import custom
from components.fragments import alert,event,invasion,world,baro

custom.sideNav(0)

baro.check()
custom.hover_effect()
left_col,right_col = st.columns(2)
with left_col:
    alert.show()
    world.show()

with right_col:
    event.show()
    invasion.show()