import streamlit as st
from components import headers
from components.fragments import alert,baro,event,invasion,varzia,world 

headers.basic(None)

left_col,right_col = st.columns(2)

with left_col:
    baro.show()
with right_col:
    varzia.show()

left_col,right_col = st.columns(2)

with left_col:
    alert.show()
    event.show()
    
with right_col:
    world.show()
    invasion.show()
    
    