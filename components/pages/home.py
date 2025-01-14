from datetime import datetime, timedelta
import streamlit as st
from utils import api_services, structures
from PIL import Image
from config.constants import AppIcons, AppLabels, AppMessages, AppPages, Warframe

def prep_image(route):
    """ Crop images. """
    image = Image.open(route)
    return image.resize((200, 200))

def format_timedelta(delta):
    """ Extract hours, minutes, and seconds from the time delta. """
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)
    return AppMessages.delta_time_message(days,hours,minutes)

def check_disable(data):
    """ Revert active variable. """
    return False if data["active"] else True
        
@st.fragment(run_every=timedelta(minutes=1))
def baro_timer():
    """ Show baro's cards that update every minute. """
    baro_card = st.container(border=True)
    with baro_card:
        with st.spinner(AppMessages.LOAD_DATA.value):
            data=api_services.get_baro_data()
        
        left,right = st.columns([2,1])
        baro_info = left.container(border=True)
        baro_img = right.container(border=True)
        
        baro_img.image(prep_image(Warframe.BARO.value["image"]),use_container_width=True)

        with baro_info:
            date = datetime.strptime(data["activation"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
            start_date = format_timedelta(date)
            location = data["location"]
            end_date = format_timedelta(datetime.strptime(data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today())
            st.markdown(f"""### {Warframe.BARO.value["name"]} <br> """,unsafe_allow_html=True)
            if data["active"]:
                st.write(AppMessages.end_time_message(end_date))
            else:
                st.write(AppMessages.start_time_message(start_date))
            st.write(AppMessages.start_time_message(location))
            if st.button(AppLabels.RELOAD.value,use_container_width=True,type="secondary",icon=AppIcons.SYNC.value,key="baro_reload"):
                if 'baro_wares' in st.session_state:
                    del st.session_state["baro_wares"]
                if 'baro_wares_detail' in st.session_state:
                    del st.session_state["baro_wares_detail"]
                st.cache_data.clear()
                st.rerun()
        if right.button(AppLabels.BROWSE.value,use_container_width=True,disabled=check_disable(data),help=AppMessages.BARO_LOCKED.value,key="baro_browse",type="primary"):
            st.switch_page(AppPages.ERROR.value)
            pass

@st.fragment(run_every=timedelta(minutes=1))
def varzia_timer():
    """ Show varzia's cards that update every minute. """
    varzia_card = st.container(border=True)
    with varzia_card:
        with st.spinner(AppMessages.LOAD_DATA.value):
            data=api_services.get_varzia_data()
        
        left,right = st.columns([2,1])
        varzia_info = left.container(border=True)
        varzia_img = right.container(border=True)
        varzia_img.image(prep_image(Warframe.VARZIA.value["image"]),use_container_width=True)

        with varzia_info:
            date = datetime.strptime(data["activation"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
            start_date = format_timedelta(date)
            location = data["location"]
            end_date = format_timedelta(datetime.strptime(data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today())
            st.markdown(f"""### {Warframe.VARZIA.value["name"]} <br> """,unsafe_allow_html=True)
            if data["active"]:
                st.write(AppMessages.end_time_message(end_date))
            else:
                st.write(AppMessages.start_time_message(start_date))
            st.write(AppMessages.start_time_message(location))
            if st.button(AppLabels.RELOAD.value,use_container_width=True,type="secondary",icon=AppIcons.SYNC.value,key="variza_reload"):
                if 'varzia_wares' in st.session_state:
                    del st.session_state["varzia_wares"]
                if 'varzia_wares_detail' in st.session_state:
                    del st.session_state["varzia_wares_detail"]
                st.cache_data.clear()
                st.rerun()
        if right.button(AppLabels.BROWSE.value,use_container_width=True,disabled=check_disable(data),help=AppMessages.VARZIA_BROWSE.value,key="variza_browse",type="primary"):
            #Aya Only!
            filtered_data = [item for item in data["inventory"] if item['credits'] is not None]
            st.session_state["varzia_wares"] = structures.ware_object("varzia",filtered_data)
            st.switch_page(AppPages.VARZIA.value)


left_col,_,right_col = st.columns([20,1,20])
with left_col:
    baro_timer()
    
with right_col:
    varzia_timer()