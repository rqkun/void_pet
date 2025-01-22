import streamlit as st
from components import cards, headers
from config import structures
from utils import data_manage

from config.constants import AppIcons, AppLabels, AppMessages, AppPages, Warframe

def store_varzia(data):
    if 'varzia_wares_detail' not in st.session_state:
        relic_list = []
        progress_text = AppMessages.PROGRESS.value
        progress = st.progress(0, text=progress_text)
        for i, item in enumerate(data):
            relic_unique_name = item["item"].replace(" ","")
            tmp = data_manage.get_relic(relic_unique_name,True)
            item_name = tmp["name"].replace('Intact', '')
            relic_list.append(tmp)
            progress.progress((i+1)/len(data), text=AppMessages.index_relic_message(item_name))
        st.session_state.varzia_wares_detail = relic_list
        progress.empty()
        return relic_list
    else:
        return st.session_state.varzia_wares_detail
    
    
query_params = st.query_params.to_dict()

if len(query_params)>0:
    st.switch_page(AppPages.ERROR.value)

_, mid,_ = st.columns([1,4,1])
with mid:
    headers.basic(logo=Warframe.AYA.value)

if 'varzia_wares' not in st.session_state:
    full_data=data_manage.get_variza()
    filtered_data = [item for item in full_data["inventory"] if item['credits'] is not None]
    st.session_state["varzia_wares"] = structures.ware_object("varzia",filtered_data)

data = st.session_state.varzia_wares["data"]
with mid:
    relics = store_varzia(data)
    with st.spinner(AppMessages.LOAD_DATA.value):
        all_prime=  data_manage.get_prime_list()
        prime_frame_options = data_manage.get_prime_resurgent_list(all_prime,relics)
        
    bot_left, bot_right =st.columns([4,1],vertical_alignment="bottom")
    prime = bot_left.selectbox(
        AppLabels.PRIME_SELECT.value,
        prime_frame_options
    )
    
    bot_right.link_button(AppLabels.WIKI.value,url=Warframe.get_wiki_url(prime),use_container_width=True,icon=AppIcons.WIKI.value,help=AppMessages.GOTO_WIKI.value)
    names = data_manage.search_rewards(prime,relics)
    
    relic_index = st.selectbox(AppLabels.RELIC_SELECT.value,
                options=names,
                )
    with st.spinner(AppMessages.LOAD_DATA.value):
        item = data_manage.get_relic(names[relic_index],True)
        image_url = data_manage.get_image(item["uniqueName"])
        cards.generic(item,image_url)
