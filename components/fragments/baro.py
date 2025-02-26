from components import custom
from config.classes.vendors import VoidTraider
from config.constants import AppMessages

import streamlit as st



@st.fragment(run_every="5m")
def check():
    """Run check for baro every 5m. """
    _,middle,_ = st.columns([2,3,2],vertical_alignment="center")
    with middle,st.spinner(AppMessages.LOAD_DATA.value,show_time=True,_cache=False):
        full_data=VoidTraider()
    
    if full_data.is_active():
        custom.baro_time_alert(f"Baro Ki'tier is leaving at {full_data.leave_time()}")
    else:
        pass
    