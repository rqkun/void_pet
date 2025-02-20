import streamlit as st
from components import cards, custom
from utils import data_manage
from millify import millify
from config.constants import AppIcons, AppMessages, AppPages, Warframe

from utils.tools import filter_data


def store_regal():
    """ Loading data. """
    _,middle,_ = st.columns([2,3,2],vertical_alignment="center")
    with middle,st.spinner(AppMessages.LOAD_DATA.value,show_time=True,_cache=False):
        data=data_manage.get_variza()
    if data is not None: 
        return data_manage.preload_data(data["inventory"])
    else: return None

custom.sideNav(3)
custom.reject_url_param()
custom.hover_effect()
items = store_regal()

left,mid,right =st.columns([1,7,1],vertical_alignment="center")

with left.popover(":material/filter_list:",use_container_width=True):
    categories = ["Warframe", "Weapon", "Relic", "Others"]
    selected_categories= st.pills("Pick the desired item type.",categories,selection_mode="multi")
    filtered_data = filter_data(items["items"],selected_categories)

with mid:
    paged_items, items_per_row = custom.paginations(filtered_data,3)

if right.button(AppIcons.SYNC.value,type="primary",use_container_width=True, help="Force reload data."):
    data_manage.clear_cached_item_call()
    st.switch_page(AppPages.VARZIA.value)

_,middle,_ = st.columns([3,2,3],vertical_alignment="center")

with middle,st.spinner("",show_time=True,_cache=False):
    for item in paged_items:
        item["image"] = data_manage.get_image_url(item["uniqueName"])
        type = Warframe.REGAL_AYA.value if item["ducats"]>0 else Warframe.AYA.value
        amount = item["ducats"] if item["ducats"]>0 else item["credits"]
        item["html"] = cards.generic(package=item, image_url=item["image"], price_info=
                {
                    "type": type,
                    "amount": millify(amount,precision=2)
                })

list_col = st.columns(items_per_row)
start_idx = 0
custom.hover_dialog()
for idx, item in enumerate(iterable=paged_items[start_idx:]):
    with list_col[idx%items_per_row]:
        if item is not None:
            st.markdown(item["html"],unsafe_allow_html=True)