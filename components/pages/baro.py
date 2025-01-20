import streamlit as st
from components import cards, headers
from utils import api_services, data_tools

from config.constants import AppMessages, AppPages, Warframe

@st.cache_data(ttl="1d",show_spinner=False)
def store_baro(data):
    if 'baro_wares_detail' not in st.session_state:
        items = {}
        progress_text = AppMessages.PROGRESS.value
        progress = st.progress(0, text=progress_text)
        for i, item in enumerate(data):
            if "M P V" in item["item"]:
                pass
            else:
                name = data_tools.get_item_name(item["uniqueName"])
                items[item["uniqueName"]] = name if name != "" else item["item"]
                progress.progress((i+1)/len(data), text=AppMessages.index_relic_message(items[item["uniqueName"]]))
        
        progress.empty()
        st.session_state.baro_wares_detail = items
        return items
    else:
        return st.session_state.baro_wares_detail
    
query_params = st.query_params.to_dict()

if len(query_params)>0:
    st.switch_page(AppPages.ERROR.value)
    
_, mid,_ = st.columns([1,4,1])
with mid:
    headers.basic(logo=Warframe.DUCAT.value)
    
if 'baro_wares' not in st.session_state:
    st.switch_page(AppPages.HOME.value)

data = st.session_state.baro_wares["data"]
with mid:
    items = store_baro(data)
    uniqueName = st.selectbox("item",
                              options=items.keys(),
                              format_func= lambda option: items[option],
                              )
    with st.spinner(AppMessages.LOAD_DATA.value):
        item = api_services.get_item_data(uniqueName)
        image_url = data_tools.get_item_image(uniqueName)
        cards.item_card(item[0],image_url)