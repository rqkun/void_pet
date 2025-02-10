import streamlit as st
from components import cards, headers
from config import structures
from utils import data_manage

from config.constants import AppIcons, AppLabels, AppMessages, AppPages, Warframe

@st.cache_data(ttl="7d",show_spinner=False)
def store_regal(data):
    """ Loading data from session state. """
    if 'varzia_wares_detail' not in st.session_state:
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
        st.session_state.varzia_wares_detail = items
        return items
    else:
        return st.session_state.varzia_wares_detail
    
query_params = st.query_params.to_dict()

if len(query_params)>0:
    st.switch_page(AppPages.ERROR.value)

headers.basic(logo=Warframe.REGAL_AYA)
    
if 'varzia_wares' not in st.session_state:
    full_data=data_manage.get_variza()
    st.session_state["varzia_wares"] = structures.ware_object("regal",full_data["inventory"])

data = st.session_state.varzia_wares["data"]
    
items = store_regal(data)
left, right =st.columns([6,1],vertical_alignment="bottom")
uniqueName = left.selectbox(AppLabels.INSPECT.value,
                            options=items.keys(),
                            format_func= lambda option: items[option],
                            )
if right.button(AppIcons.SYNC.value,use_container_width=True):
    if 'varzia_wares' in st.session_state:
        del st.session_state["varzia_wares"]
    if 'varzia_wares_detail' in st.session_state:
        del st.session_state["varzia_wares_detail"]
    st.cache_data.clear()

with st.spinner(AppMessages.LOAD_DATA.value):
    item = data_manage.get_item(uniqueName)
    if item is not None:
        image_url = data_manage.get_image_url(uniqueName)
        cards.generic(item=item,image_url=image_url)