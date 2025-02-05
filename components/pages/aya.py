import streamlit as st
from components import cards, headers
from config import structures
from utils import data_manage

from config.constants import AppIcons, AppLabels, AppMessages, AppPages, Warframe

def store_aya(data):
    """ Loading data from session state. """
    if 'aya_wares_detail' not in st.session_state:
        relic_list = []
        progress_text = AppMessages.PROGRESS.value
        progress = st.progress(0, text=progress_text)
        for i, item in enumerate(data):
            relic_unique_name = item["item"].replace(" ","")
            tmp = data_manage.get_relic(relic_unique_name,True)
            item_name = tmp["name"].replace('Intact', '')
            relic_list.append(tmp)
            progress.progress((i+1)/len(data), text=AppMessages.index_relic_message(item_name))
        st.session_state.aya_wares_detail = relic_list
        progress.empty()
        return relic_list
    else:
        return st.session_state.aya_wares_detail
    
    
query_params = st.query_params.to_dict()

if len(query_params)>0:
    st.switch_page(AppPages.ERROR.value)


headers.basic(logo=Warframe.AYA)

if 'aya_wares' not in st.session_state:
    full_data=data_manage.get_variza()
    filtered_data = [item for item in full_data["inventory"] if item['credits'] is not None]
    st.session_state["aya_wares"] = structures.ware_object("aya",filtered_data)

data = st.session_state.aya_wares["data"]

relics = store_aya(data)
with st.spinner(AppMessages.LOAD_DATA.value):
    all_prime=  data_manage.get_prime_list()
    prime_frame_options = data_manage.get_prime_resurgent_list(all_prime,relics)
prime_select,relic_select, refresh =st.columns([7,2,1],vertical_alignment="bottom")
prime = prime_select.multiselect(
    AppLabels.PRIME_SELECT.value,
    prime_frame_options,
    format_func = lambda option: option.replace(" Prime", ""),
    max_selections=4,
    placeholder=AppLabels.PRIME_SELECT.value,
    label_visibility="collapsed"
)

names = data_manage.search_rewards(prime,relics)


relic_index = relic_select.selectbox(AppLabels.RELIC_SELECT.value,
            options=names,
            format_func=lambda option: option.replace(" Intact", ""),
            placeholder=AppLabels.RELIC_SELECT.value,
            label_visibility="collapsed"
            )

if refresh.button(AppIcons.SYNC.value,use_container_width=True):
    if 'aya_wares' in st.session_state:
        del st.session_state["aya_wares"]
    if 'aya_wares_detail' in st.session_state:
        del st.session_state["aya_wares_detail"]
    st.cache_data.clear()
    st.rerun()

with st.spinner(AppMessages.LOAD_DATA.value):
    item = data_manage.get_relic(names[relic_index],True)
    image_url = data_manage.get_image_url(item["uniqueName"])
    cards.generic(item,image_url)
