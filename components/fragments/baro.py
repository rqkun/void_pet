from utils import data_manage
from utils import tools

import streamlit_antd_components as sac
import streamlit as st


from datetime import datetime

@st.fragment(run_every="5m")
def check():
    """ Run check for baro every 5m. """
    full_data=data_manage.get_baro()
    
    if full_data["active"] is True:
        date = datetime.strptime(full_data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
        sac.alert(label=f"Baro Ki'tier is leaving at {tools.format_timedelta(date)}", banner=True,size='xs',variant='outline', color='cyan', icon=True, closable=False)
    else:
        pass
    