from components import custom
from config.constants import AppMessages
from utils import data_manage
from utils import tools

import streamlit_antd_components as sac
import streamlit as st


from datetime import datetime

@st.fragment(run_every="5m")
def check():
    """ Run check for baro every 5m. """
    _,middle,_ = st.columns([2,3,2],vertical_alignment="center")
    with middle,st.spinner(AppMessages.LOAD_DATA.value,show_time=True,_cache=False):
        full_data=data_manage.get_baro()
    
    if full_data["active"] is True:
        date = datetime.strptime(full_data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
        custom.baro_time_alert(f"Baro Ki'tier is leaving at {tools.format_timedelta(date)}")
    else:
        pass
    