from datetime import datetime
import streamlit as st
from components import cards, headers
from config import structures
from utils import data_manage

from config.constants import AppIcons, AppMessages, AppPages, Warframe
from utils.tools import format_timedelta

@st.cache_data(ttl="1d",show_spinner=False)
def store_baro(data):
    """ Loading data from session state. """
    if 'baro_wares_detail' not in st.session_state:
        items = {}
        progress_text = AppMessages.PROGRESS.value
        progress = st.progress(0, text=progress_text)
        
        for i, item in enumerate(data):
            if "M P V" in item["item"]:
                pass
            else:
                name = data_manage.get_item_name(item["uniqueName"])
                items[item["uniqueName"]] = {
                    "name": name if name != "" else item["item"],
                    "ducats" : item["ducats"],
                    "credits" : item["credits"],
                }
                progress.progress((i+1)/len(data), text=AppMessages.index_relic_message(items[item["uniqueName"]]["name"]))
        
        progress.empty()
        st.session_state.baro_wares_detail = items
        return items
    else:
        return st.session_state.baro_wares_detail
    
query_params = st.query_params.to_dict()

if len(query_params)>0:
    st.switch_page(AppPages.ERROR.value)
    

headers.basic(logo=Warframe.DUCAT)
    
if 'baro_wares' not in st.session_state:
    full_data=data_manage.get_baro()
    if full_data["active"] is False:
        date = datetime.strptime(full_data["activation"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
        st.session_state.not_baro_time = AppMessages.baro_time_message(format_timedelta(date))
        st.switch_page(AppPages.HOME.value)
    st.session_state["baro_wares"] = structures.ware_object("baro",full_data["inventory"])

data = st.session_state.baro_wares["data"]

items = store_baro(data)

left, right =st.columns([6,1],vertical_alignment="bottom")

uniqueName = left.selectbox("item",
                            options=items.keys(),
                            format_func= lambda option: items[option]["name"],
                            )

if right.button(AppIcons.SYNC.value,use_container_width=True):
    if 'baro_wares' in st.session_state:
        del st.session_state["baro_wares"]
    if 'baro_wares_detail' in st.session_state:
        del st.session_state["baro_wares_detail"]
    st.cache_data.clear()

with st.spinner(AppMessages.LOAD_DATA.value):
    item = data_manage.get_item(uniqueName)
    image_url = data_manage.get_image(uniqueName)
    cards.baro(item,items[uniqueName],image_url)