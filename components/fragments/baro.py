from components import cards
from config import structures
from config.constants import AppIcons, AppLabels, AppMessages, AppPages, Warframe
from utils import data_manage
from utils import tools
from utils.tools import check_disable, format_timedelta

import streamlit_antd_components as sac
import streamlit as st


from datetime import datetime, timedelta


@st.fragment(run_every=timedelta(minutes=1))
def show():
    """ Show baro's card that update every minute. """
    baro_card = st.container(border=True)
    with baro_card:

        top_left,top_right = st.columns([5,1],vertical_alignment="center")
        top_left.markdown(f"""### {Warframe.BARO.value["name"]}""",unsafe_allow_html=True)
        baro_reload = top_right.button(AppIcons.SYNC.value,use_container_width=True,type="tertiary",key="baro_reload")
        baro_info_card = st.container(border=True)
        with baro_info_card, st.spinner(AppMessages.LOAD_DATA.value):
            left,right = baro_info_card.columns([2,1])
            baro_info = left.container(border=False)
            baro_img = right.container(border=True)
            with baro_img:
                cards.prep_image(Warframe.BARO)


            with baro_info:
                data=data_manage.get_baro()
                date = datetime.strptime(data["activation"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
                start_date = format_timedelta(date)
                end_date = format_timedelta(datetime.strptime(data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today())

                if data["active"]:
                    st.write(AppMessages.end_time_message(end_date))
                else:
                    st.write(AppMessages.start_time_message(start_date))

                if baro_reload:
                    if 'baro_wares' in st.session_state:
                        del st.session_state["baro_wares"]
                    if 'baro_wares_detail' in st.session_state:
                        del st.session_state["baro_wares_detail"]
                    st.rerun(scope="fragment")
        if baro_info.button(AppLabels.BROWSE.value,use_container_width=True,disabled=check_disable(data),help=AppMessages.BARO_LOCKED.value,key="baro_browse",type="primary"):
            st.session_state["baro_wares"] = structures.ware_object("baro",data["inventory"])
            st.switch_page(AppPages.BARO.value)
@st.fragment(run_every="5m")
def check():
    full_data=data_manage.get_baro()
    
    if full_data["active"] is True:
        date = datetime.strptime(full_data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
        sac.alert(label=f"Baro Ki'tier is leaving at {tools.format_timedelta(date)}", banner=True,size='xs',variant='outline', color='cyan', icon=True, closable=False)
    else:
        pass
    