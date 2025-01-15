from datetime import datetime, timedelta
import streamlit as st
from utils import api_services, structures
from PIL import Image
from config.constants import AppIcons, AppLabels, AppMessages, AppPages, Warframe
from utils.data_tools import get_invasions_rewards, get_sortie_missions

def prep_image(route):
    """ Crop images. """
    image = Image.open(route)
    return image.resize((150, 150))

def format_timedelta(delta,day=True):
    """ Extract hours, minutes, and seconds from the time delta. """
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)
    if day:
        return AppMessages.delta_datetime_message(days,hours,minutes)
    else:
        return AppMessages.delta_time_message(hours,minutes)

def check_disable(data):
    """ Revert active variable. """
    return False if data["active"] else True
        
@st.fragment(run_every=timedelta(minutes=1))
def baro_timer():
    """ Show baro's card that update every minute. """
    baro_card = st.container(border=True)
    with baro_card:
        with st.spinner(AppMessages.LOAD_DATA.value):
            data=api_services.get_baro_data()
        st.markdown(f"""### {Warframe.BARO.value["name"]}""",unsafe_allow_html=True)
        baro_info_card = st.container(border=True)
        left,right = baro_info_card.columns([2,1])
        
        baro_info = left.container(border=False)
        baro_img = right.container(border=True)
        
        baro_img.image(prep_image(Warframe.BARO.value["image"]),use_container_width=True)

        with baro_info:
            date = datetime.strptime(data["activation"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
            start_date = format_timedelta(date)
            end_date = format_timedelta(datetime.strptime(data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today())
            
            if data["active"]:
                st.write(AppMessages.end_time_message(end_date))
            else:
                st.write(AppMessages.start_time_message(start_date))
            if st.button(AppLabels.RELOAD.value,use_container_width=True,type="secondary",icon=AppIcons.SYNC.value,key="baro_reload"):
                if 'baro_wares' in st.session_state:
                    del st.session_state["baro_wares"]
                if 'baro_wares_detail' in st.session_state:
                    del st.session_state["baro_wares_detail"]
                st.rerun(scope="fragment")
        if baro_info.button(AppLabels.BROWSE.value,use_container_width=True,disabled=check_disable(data),help=AppMessages.BARO_LOCKED.value,key="baro_browse",type="primary"):
            st.switch_page(AppPages.ERROR.value)
            pass

@st.fragment(run_every=timedelta(minutes=1))
def varzia_timer():
    """ Show varzia's card that update every minute. """
    varzia_card = st.container(border=True)
    with varzia_card:
        with st.spinner(AppMessages.LOAD_DATA.value):
            data=api_services.get_varzia_data()
        st.markdown(f"""### {Warframe.VARZIA.value["name"]}""",unsafe_allow_html=True)
        varzia_info_card = st.container(border=True)
        left,right = varzia_info_card.columns([2,1])
        varzia_info = left.container(border=False)
        varzia_img = right.container(border=True)
        varzia_img.image(prep_image(Warframe.VARZIA.value["image"]),use_container_width=True)

        with varzia_info:
            date = datetime.strptime(data["activation"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
            start_date = format_timedelta(date)
            end_date = format_timedelta(datetime.strptime(data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today())
            
            if data["active"]:
                st.write(AppMessages.end_time_message(end_date))
            else:
                st.write(AppMessages.start_time_message(start_date))
            st.write("")
            if st.button(AppLabels.RELOAD.value,use_container_width=True,type="secondary",icon=AppIcons.SYNC.value,key="variza_reload"):
                if 'varzia_wares' in st.session_state:
                    del st.session_state["varzia_wares"]
                if 'varzia_wares_detail' in st.session_state:
                    del st.session_state["varzia_wares_detail"]
                st.cache_data.clear()
                st.rerun(scope="fragment")
        if varzia_info.button(AppLabels.BROWSE.value,use_container_width=True,disabled=check_disable(data),help=AppMessages.VARZIA_BROWSE.value,key="variza_browse",type="primary"):
            #Aya Only!
            filtered_data = [item for item in data["inventory"] if item['credits'] is not None]
            st.session_state["varzia_wares"] = structures.ware_object("varzia",filtered_data)
            st.switch_page(AppPages.VARZIA.value)

@st.fragment(run_every=timedelta(minutes=1))
def event_state_timer():
    """ Show event's card that update every minute. """
    event_state_card = st.container(border=True)
    with event_state_card:
        with st.spinner(AppMessages.LOAD_DATA.value):
            data=api_services.get_world_state()
        st.markdown(f"""### Events """,unsafe_allow_html=True)
        events_info = st.container(border=True)
        # events_wiki = right.container(border=True)
        if len(data["events"])>0:
            for event in data["events"]:
                left,right = events_info.columns([8,1],vertical_alignment="top")
                right.link_button(AppIcons.EXTERNAL.value,url=Warframe.get_wiki_url(event["description"]),use_container_width=True,type="tertiary")
                left.progress(event["currentScore"],f"""{event["description"]} | {event["node"]}""")
        else:
            events_info.info('There are currently no events', icon=AppIcons.INFO.value)
        if events_info.button(AppLabels.RELOAD.value,use_container_width=True,type="secondary",icon=AppIcons.SYNC.value,key="event_state_reload"):
            st.rerun(scope="fragment")

@st.fragment(run_every=timedelta(minutes=1))
def world_state_timer():
    """ Show Sortie's info card. """
    world_state_card = st.container(border=True)
    with world_state_card:
        with st.spinner(AppMessages.LOAD_DATA.value):
            data=api_services.get_world_state()
            data ={
                "Cetus": data["cetusCycle"],
                "Deimos": data["cambionCycle"],
                "Zariman": data["zarimanCycle"],
                "Fortuna": data["vallisCycle"],
                "Duviri": data["duviriCycle"]
            }
            
        st.markdown(f"""### World""",unsafe_allow_html=True)
        with st.container(border=True):
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

            if st.button(AppLabels.RELOAD.value,use_container_width=True,type="secondary",icon=AppIcons.SYNC.value,key="world_state_reload"):
                st.rerun(scope="fragment")

@st.fragment()
def sortie_state_timer():
    """ Show Sortie's info card. """
    event_state_card = st.container(border=True)
    with event_state_card:
        with st.spinner(AppMessages.LOAD_DATA.value):
            data=api_services.get_world_state()["sortie"]
        st.markdown(f"""### Sortie""",unsafe_allow_html=True)
        
        
        with st.container(border=True),st.spinner(AppMessages.LOAD_DATA.value):
            sortie_steps, sortie_step_names = get_sortie_missions(data)
            tablist = st.tabs(sortie_step_names)
            for i,tab in enumerate(tablist):
                with tab:
                    sortie_node = sortie_steps[sortie_step_names[i]]
                    st.markdown(f"""Boss: `{data["boss"]}` - `{data["faction"]}` <br>
                                {AppMessages.location_message(sortie_node["node"])}<br>
                                Modifier: `{sortie_node["modifier"]}`
                                """,unsafe_allow_html=True)
            if st.button(AppLabels.RELOAD.value,use_container_width=True,type="secondary",icon=AppIcons.SYNC.value,key="sortie_state_reload"):
                st.rerun(scope="fragment")
           

@st.fragment(run_every=timedelta(minutes=5))
def invasion_state_timer():
    """ Show Invasion rewards card. """
    event_state_card = st.container(border=True)
    with event_state_card:
        with st.spinner(AppMessages.LOAD_DATA.value):
            data=get_invasions_rewards(api_services.get_world_state()["invasions"])
        st.markdown(f"""### Invasion Rewards""",unsafe_allow_html=True)
        
        
        with st.container(border=True),st.spinner(AppMessages.LOAD_DATA.value):
            st.json(data)
            
            if st.button(AppLabels.RELOAD.value,use_container_width=True,type="secondary",icon=AppIcons.SYNC.value,key="invasion_state_reload"):
                st.rerun(scope="fragment")

left_col,right_col = st.columns(2)
with left_col:
    baro_timer()
    varzia_timer()
    invasion_state_timer()
with right_col:
    event_state_timer()
    sortie_state_timer()
    world_state_timer()
    