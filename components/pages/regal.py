import streamlit as st
from components import cards, headers
from utils import data_manage

from config.constants import AppMessages, AppPages, Warframe

@st.cache_data(ttl="1d",show_spinner=False)
def store_regal(data):
    if 'regal_wares_detail' not in st.session_state:
        items = {}
        progress_text = AppMessages.PROGRESS.value
        progress = st.progress(0, text=progress_text)
        
        for i, item in enumerate(data):
            if "M P V" in item["item"]:
                pass
            else:
                name = data_manage.get_item_name(item["uniqueName"])
                items[item["uniqueName"]] = name if name != "" else item["item"]
                progress.progress((i+1)/len(data), text=AppMessages.index_relic_message(items[item["uniqueName"]]))
        
        progress.empty()
        st.session_state.regal_wares_detail = items
        return items
    else:
        return st.session_state.regal_wares_detail
    
query_params = st.query_params.to_dict()

if len(query_params)>0:
    st.switch_page(AppPages.ERROR.value)
    
_, mid,_ = st.columns([1,4,1])
with mid:
    headers.basic(logo=Warframe.REGAL_AYA.value)
    
if 'regal_wares' not in st.session_state:
    st.switch_page(AppPages.HOME.value)

data = st.session_state.regal_wares["data"]
with mid:
    items = store_regal(data)
    pass
    uniqueName = st.selectbox("item",
                              options=items.keys(),
                              format_func= lambda option: items[option],
                              )
    with st.spinner(AppMessages.LOAD_DATA.value):
        item = data_manage.get_item(uniqueName)
        image_url = data_manage.get_image(uniqueName)
        cards.generic(item,image_url)