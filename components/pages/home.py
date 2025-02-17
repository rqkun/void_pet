import streamlit as st
from components import custom
from components.fragments import alert,event,invasion,world,baro

custom.sideNav(0)

baro.check()
custom.hover_effect()
left_col,right_col = st.columns(2)
with left_col:
    world.show()
    invasion.show()   
        
with right_col:
    alert.show()
    event.show()
    