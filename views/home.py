from datetime import datetime
import streamlit as st
from utils import api_services
from PIL import Image

from utils.icons import AppIcons


def get_baro_json():
    json = api_services.get_baro_data()
    return json

def format_timedelta(delta):
    # Extract hours, minutes, and seconds from the time delta
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(total_seconds, 86400)  # 86400 seconds in a day
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format the time delta
    if days > 0:
        formatted_time_delta = f"{days} days, {hours:02}:{minutes:02}:{seconds:02}"
    else:
        formatted_time_delta = f"{hours:02}:{minutes:02}:{seconds:02}"
    return formatted_time_delta

def check_disable(data):
    return False if data["active"] else True

@st.fragment
def baro_timer():
    baro_card = st.container(border=True)
    with baro_card:
        with st.spinner("Gather Data..."):
            data=get_baro_json()
        
        left,right = st.columns([2,1])
        baro_info = left.container(border=True)
        baro_img = right.container(border=True)
        #_,baro_img_mid,_= baro_img.columns([2,6,1])
        image = Image.open("static/image/baro.png")
        new_image = image.resize((200, 200))
        baro_img.image(new_image,use_container_width=True)

        with baro_info:
            date = datetime.strptime(data["activation"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
            start_date = format_timedelta(date)
            location = data["location"]
            end_date = format_timedelta(datetime.strptime(data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today())
            st.header(data["character"])
            if data["active"]:
                st.write(f"Approximate leaving time: `{end_date}`")
            else:
                st.write(f"Approximate arrival time: `{start_date}`")
            st.write(f"Place: `{location}`")
            if st.button("Reload",use_container_width=True,type="secondary",icon=AppIcons.SYNC.value):
                st.rerun()
        right.button("Browse",use_container_width=True,disabled=check_disable(data),help="This will unlock when he comes back to a relay.")

    

left_col, right_col = st.columns(2)

with left_col:
    baro_timer()
    
    