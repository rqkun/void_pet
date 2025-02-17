from components import markdowns
from config.constants import AppIcons, AppMessages
from utils import data_manage
from utils.tools import format_timedelta


import streamlit as st


from datetime import datetime, timedelta


@st.fragment(run_every=timedelta(minutes=1))
def show():
    """ Show world state's info card. """
    world_state_card = st.container(border=True)
    with world_state_card:

        top_left,top_right = st.columns([5,1],vertical_alignment="center")
        top_left.markdown(f"""### World""",unsafe_allow_html=True)
        world_state_reload = top_right.button(AppIcons.SYNC.value,use_container_width=True,type="tertiary",key="world_state_reload")
        with st.container(border=True), st.spinner(AppMessages.LOAD_DATA.value):
            data=data_manage.get_world_state()
            data =[
                {
                    "name":"Cetus",
                    "data": data["cetusCycle"],
                    "image": data_manage.get_image_url("/Lotus/Types/Items/MiscItems/PhotoboothTileEidolonLandscape",True)
                },
                {
                    "name":"Deimos",
                    "data": data["cambionCycle"],
                    "image": data_manage.get_image_url("/Lotus/Types/Items/MiscItems/PhotoboothTileDeimosLandscape",True)
                },
                {
                    "name":"Zariman",
                    "data": data["zarimanCycle"],
                    "image": data_manage.get_image_url("/Lotus/Types/Items/PhotoBooth/Zariman/PhotoboothTileZarAmphitheatre",True)
                },
                {
                    "name":"Fortuna",
                    "data": data["vallisCycle"],
                    "image": data_manage.get_image_url("/Lotus/Types/Items/MiscItems/PhotoboothTileVenusLandscape",True)
                },
                {
                    "name":"Duviri",
                    "data": data["duviriCycle"],
                    "image": data_manage.get_image_url("/Lotus/Types/Items/MiscItems/PhotoboothTileDuviriTeshinsCave",True)
                },
            ]
            st.markdown(markdowns.world_clock_md(data),unsafe_allow_html=True)

            if world_state_reload:
                st.rerun(scope="fragment")