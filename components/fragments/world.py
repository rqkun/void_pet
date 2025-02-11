from config.constants import AppIcons, AppMessages
from utils import data_manage
from utils.tools import format_timedelta


import streamlit as st


from datetime import datetime, timedelta


@st.fragment(run_every=timedelta(minutes=1))
def show():
    """ Show Sortie's info card. """
    world_state_card = st.container(border=True)
    with world_state_card:

        top_left,top_right = st.columns([5,1],vertical_alignment="center")
        top_left.markdown(f"""### World""",unsafe_allow_html=True)
        world_state_reload = top_right.button(AppIcons.SYNC.value,use_container_width=True,type="tertiary",key="world_state_reload")
        with st.container(border=True), st.spinner(AppMessages.LOAD_DATA.value):
            data=data_manage.get_world_state()
            data ={
                "Cetus": data["cetusCycle"],
                "Deimos": data["cambionCycle"],
                "Zariman": data["zarimanCycle"],
                "Fortuna": data["vallisCycle"],
                "Duviri": data["duviriCycle"]
            }
            cycle_info,cycle_time = st.columns([1,1])
            cycle_info.markdown(f"""
                                Cetus: `{data["Cetus"]["state"].upper()}`<br>
                                Deimos: `{data["Deimos"]["state"].upper()}`<br>
                                Fortuna: `{data["Fortuna"]["state"].upper()}`<br>
                                Zariman: `{data["Zariman"]["state"].upper()}`<br>
                                Duviri: `{data["Duviri"]["state"].upper()}`<br>
                                """,unsafe_allow_html=True)
            cycle_time.markdown(f"""
                                Time: `{format_timedelta(datetime.strptime(data["Cetus"]["expiry"]
                                ,"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today(),day=False)}`<br>
                                Time: `{format_timedelta(datetime.strptime(data["Deimos"]["expiry"]
                                ,"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today(),day=False)}`<br>
                                Time: `{format_timedelta(datetime.strptime(data["Fortuna"]["expiry"]
                                ,"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today(),day=False)}`<br>
                                Time: `{format_timedelta(datetime.strptime(data["Zariman"]["expiry"]
                                ,"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today(),day=False)}`<br>
                                Time: `{format_timedelta(datetime.strptime(data["Duviri"]["expiry"]
                                ,"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today(),day=False)}`<br>
                                """,unsafe_allow_html=True)

            if world_state_reload:
                st.rerun(scope="fragment")