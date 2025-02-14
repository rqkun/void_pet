import streamlit as st
from components import custom
from components.fragments import alert,event,invasion,world 

custom.sideNav(0)

left_col,right_col = st.columns(2)
with left_col:
    world.show()
    invasion.show()   
        
with right_col:
    alert.show()
    event.show()
    