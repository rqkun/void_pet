from datetime import datetime, timedelta
import streamlit as st
from utils import api_services, structures
from PIL import Image
import pandas as pd
from utils.icons import AppIcons

def prep_image(route):
    image = Image.open(route)
    return image.resize((200, 200))

def format_timedelta(delta):
    # Extract hours, minutes, and seconds from the time delta
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(total_seconds, 86400)  # 86400 seconds in a day
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    # Format the time delta
    formatted_time_delta = f"{days} days, {hours} hours, {minutes} minutes"
    return formatted_time_delta

def check_disable(data):
    return False if data["active"] else True
        
@st.fragment(run_every=timedelta(minutes=1))
def baro_timer():
    baro_card = st.container(border=True)
    with baro_card:
        with st.spinner("Gather Data..."):
            data=api_services.get_baro_data()
        
        left,right = st.columns([2,1])
        baro_info = left.container(border=True)
        baro_img = right.container(border=True)
        
        baro_img.image(prep_image("static/image/baro.png"),use_container_width=True)

        with baro_info:
            date = datetime.strptime(data["activation"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
            start_date = format_timedelta(date)
            location = data["location"]
            end_date = format_timedelta(datetime.strptime(data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today())
            st.header(data["character"])
            if data["active"]:
                st.write(f"Leaving: `{end_date}`")
            else:
                st.write(f"Arrival: `{start_date}`")
            st.write(f"Place: `{location}`")
            if st.button("Reload",use_container_width=True,type="secondary",icon=AppIcons.SYNC.value,key="baro_reload"):
                if 'baro_wares' in st.session_state:
                    del st.session_state["baro_wares"]
                if 'baro_wares_detail' in st.session_state:
                    del st.session_state["baro_wares_detail"]
                st.cache_data.clear()
                st.rerun()
        if right.button("Browse",use_container_width=True,disabled=check_disable(data),help="This will unlock when he comes back to a relay.",key="baro_browse",type="primary"):
            st.switch_page("views/error.py")
            pass

@st.fragment(run_every=timedelta(minutes=1))
def varzia_timer():
    varzia_card = st.container(border=True)
    with varzia_card:
        with st.spinner("Gather Data..."):
            data=api_services.get_varzia_data()
        
        left,right = st.columns([2,1])
        varzia_info = left.container(border=True)
        varzia_img = right.container(border=True)
        varzia_img.image(prep_image("static/image/varzia.png"),use_container_width=True)

        with varzia_info:
            date = datetime.strptime(data["activation"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
            start_date = format_timedelta(date)
            location = data["location"]
            end_date = format_timedelta(datetime.strptime(data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today())
            st.header("Varzia")
            if data["active"]:
                st.write(f"Leaving: `{end_date}`")
            else:
                st.write(f"Arrival: `{start_date}`")
            st.write(f"Place: `{location}`")
            if st.button("Reload",use_container_width=True,type="secondary",icon=AppIcons.SYNC.value,key="variza_reload"):
                if 'varzia_wares' in st.session_state:
                    del st.session_state["varzia_wares"]
                if 'varzia_wares_detail' in st.session_state:
                    del st.session_state["varzia_wares_detail"]
                st.cache_data.clear()
                st.rerun()
        if right.button("Browse",use_container_width=True,disabled=check_disable(data),help="Click to browse wares.",key="variza_browse",type="primary"):
            #Aya Only!
            filtered_data = [item for item in data["inventory"] if item['credits'] is not None]
            st.session_state["varzia_wares"] = structures.ware_object("varzia",filtered_data)
            st.switch_page("views/varzia.py")


left_col,_,right_col = st.columns([20,1,20])
with left_col:
        baro_timer()
    
with right_col:
    varzia_timer()