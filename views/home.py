from datetime import datetime, timedelta
import streamlit as st
from utils import api_services
from PIL import Image

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

@st.dialog("Browse Wares",width="large")
def browse_ware(item_list):
    with st.container(height=400):
        st.write(item_list)
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
                st.rerun()
        if right.button("Browse",use_container_width=True,disabled=check_disable(data),help="This will unlock when he comes back to a relay.",key="baro_browse"):
            browse_ware(data["inventory"])

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
                st.write(f"Leaving: \n`{end_date}`")
            else:
                st.write(f"Arrival: \n`{start_date}`")
            st.write(f"Place: `{location}`")
            if st.button("Reload",use_container_width=True,type="secondary",icon=AppIcons.SYNC.value,key="variza_reload"):
                st.rerun()
        if right.button("Browse",use_container_width=True,disabled=check_disable(data),help="Click to browse wares",key="variza_browse"):
            browse_ware(data["inventory"])

        

left_col,_,right_col = st.columns([20,1,20])

with left_col:
    baro_timer()
    
with right_col:
    varzia_timer()