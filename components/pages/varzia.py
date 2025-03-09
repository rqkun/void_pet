import streamlit as st
from components import custom
from config.classes.vendors import VaultTraider
from utils import data_manage
from config.constants import AppIcons, AppMessages, AppPages, Warframe


def store_regal():
    """Loading data. """
    _,middle,_ = st.columns([2,3,2],vertical_alignment="center")
    with middle,st.spinner(AppMessages.LOAD_DATA.value,show_time=True,_cache=False):
        data=VaultTraider()
    data.preload()
    return data

custom.sideNav(2)
custom.reject_url_param()
custom.image_style()
custom.card_style()

data = store_regal()

left,mid,right =st.columns([1,7,1],vertical_alignment="center")

with left.popover(AppIcons.FILTER.value,use_container_width=True):
    categories = Warframe.FILTER.value
    selected_categories= st.pills("Pick the desired item type.",categories,selection_mode="multi")
    data.filter(selected_categories)

with mid:
    start_idx, end_idx, items_per_row = custom.paginations(length=len(data.filtered_inventory),num_of_row=3)

if right.button(AppIcons.SYNC.value,type="primary",use_container_width=True, help="Force reload data."):
    data_manage.clear_cached_item_call()
    del data
    st.switch_page(AppPages.VARZIA.value)

_,middle,_ = st.columns([3,2,3],vertical_alignment="center")

with middle,st.spinner("",show_time=True,_cache=False):
    view_data = data.parse_items(start_idx, end_idx)

list_col = st.columns(items_per_row)
start_idx = 0
custom.varzia_style()
for idx, item in enumerate(iterable=view_data[start_idx:]):
    with list_col[idx%items_per_row]:
        if item is not None:
            st.markdown(item["html"],unsafe_allow_html=True)