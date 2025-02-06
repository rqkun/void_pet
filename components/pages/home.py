from datetime import datetime, timedelta
import streamlit as st
from PIL import Image
from components import cards, headers
from config import structures
import datasources.warframe_status
from config.constants import AppIcons, AppLabels, AppMessages, AppPages, Warframe
from utils import data_manage
from utils.data_manage import get_sortie_missions,get_invasions_rewards
from utils.tools import check_disable,format_timedelta

@st.fragment(run_every=timedelta(minutes=1))
def baro_timer():
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

@st.fragment(run_every=timedelta(minutes=1))
def varzia_timer():
    """ Show varzia's card that update every minute. """
    varzia_card = st.container(border=True)
    with varzia_card:
        
        top_left,top_right = st.columns([5,1],vertical_alignment="center")
        top_left.markdown(f"""### {Warframe.VARZIA.value["name"]}""",unsafe_allow_html=True)
        varzia_reload = top_right.button(AppIcons.SYNC.value,use_container_width=True,type="tertiary",key="varzia_reload2")
        
        varzia_info_card = st.container(border=True)
        with varzia_info_card, st.spinner(AppMessages.LOAD_DATA.value):
            left,right = varzia_info_card.columns([2,1])
            varzia_info = left.container(border=False)
            varzia_img = right.container(border=True)
            with varzia_img:
                cards.prep_image(Warframe.VARZIA)
            with varzia_info:
                data=datasources.warframe_status.get_varzia_data()
                date = datetime.strptime(data["activation"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
                start_date = format_timedelta(date)
                end_date = format_timedelta(datetime.strptime(data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today())
                
                if data["active"]:
                    st.write(AppMessages.end_time_message(end_date))
                else:
                    st.write(AppMessages.start_time_message(start_date))

                if varzia_reload:
                    if 'varzia_wares' in st.session_state:
                        del st.session_state["varzia_wares"]
                    if 'varzia_wares_detail' in st.session_state:
                        del st.session_state["varzia_wares_detail"]
                    st.rerun(scope="fragment")
            if varzia_info.button(AppLabels.BROWSE.value,use_container_width=True,disabled=check_disable(data),help=AppMessages.VARZIA_BROWSE.value,key="varzia_browse",type="primary"):
                st.switch_page(AppPages.VARZIA.value)

@st.fragment(run_every=timedelta(minutes=1))
def event_state_timer():
    """ Show event's card that update every minute. """
    event_state_card = st.container(border=True)
    with event_state_card:
        
        top_left,top_right = st.columns([5,1],vertical_alignment="center")
        top_left.markdown(f"""### Events """,unsafe_allow_html=True)
        event_state_reload = top_right.button(AppIcons.SYNC.value,use_container_width=True,type="tertiary",key="event_state_reload")
        
        events_info = st.container(border=True)
        with events_info, st.spinner(AppMessages.LOAD_DATA.value):
            data=data_manage.get_world_state()
            if len(data["events"])>0:
                for event in data["events"]:
                    try:
                        left,right = events_info.columns([8,1],vertical_alignment="top")
                        right.link_button(AppIcons.EXTERNAL.value,url=Warframe.get_wiki_url(event["description"]),use_container_width=True,type="tertiary")
                        left.progress(event["currentScore"],f"""{event["description"]} | {event["node"]}""")
                    except:
                        pass
            else:
                events_info.info('There are currently no events', icon=AppIcons.INFO.value)
            if event_state_reload:
                st.rerun(scope="fragment")

@st.fragment(run_every=timedelta(minutes=1))
def world_state_timer():
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

@st.fragment()
def sortie_state_timer():
    """ Show Sortie's info card. """
    event_state_card = st.container(border=True)
    with event_state_card:
        top_left,top_right = st.columns([5,1],vertical_alignment="center")
        top_left.markdown(f"""### Sortie""",unsafe_allow_html=True)
        sortie_state_reload = top_right.button(AppIcons.SYNC.value,use_container_width=True,type="tertiary",key="sortie_state_reload")
        with st.container(border=True),st.spinner(AppMessages.LOAD_DATA.value):
            data=data_manage.get_world_state()["sortie"]
            sortie_steps, sortie_step_names = get_sortie_missions(data)
            tablist = st.tabs(sortie_step_names)
            for i,tab in enumerate(tablist):
                with tab:
                    sortie_node = sortie_steps[sortie_step_names[i]]
                    st.markdown(f"""Boss: `{data["boss"]}` - `{data["faction"]}` <br>
                                {AppMessages.location_message(sortie_node["node"])}<br>
                                Modifier: `{sortie_node["modifier"]}`
                                """,unsafe_allow_html=True)
            if sortie_state_reload:
                st.rerun(scope="fragment")
           

@st.fragment(run_every=timedelta(minutes=5))
def invasion_state_timer():
    """ Show Invasion rewards card. """
    event_state_card = st.container(border=True)
    with event_state_card:
        
        top_left,top_right = st.columns([5,1],vertical_alignment="center")
        top_left.markdown(f"""### Invasion Rewards""",unsafe_allow_html=True)
        invasion_state_reload = top_right.button(AppIcons.SYNC.value,use_container_width=True,type="tertiary",key="invasion_state_reload")
        
        
        with st.container(border=True),st.spinner(AppMessages.LOAD_DATA.value):
            data=get_invasions_rewards(data_manage.get_world_state()["invasions"])
            for item,amount in data.items():
                left,right = st.columns([1,6],vertical_alignment="top")
                right.write(f"{item}: `{amount}`")
                image = Image.open(data_manage.get_invasion_reward_image(item))
                left.image(image)

            if invasion_state_reload:
                st.rerun(scope="fragment")

headers.basic(None)

left_col,right_col = st.columns(2)
with left_col:
    baro_timer()
    varzia_timer()
    world_state_timer()
    
with right_col:
    event_state_timer()
    invasion_state_timer()
    #sortie_state_timer()
    
    