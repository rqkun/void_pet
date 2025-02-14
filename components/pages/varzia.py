import streamlit as st
from components import cards, custom
from config import structures
from utils import data_manage
from millify import millify
from config.constants import AppIcons, Warframe

from utils.tools import filter_data


def store_regal():
    """ Loading data from session state. """
    data=data_manage.get_variza()
    # if data is not None: 
    
    items = data_manage.preload_data(data["inventory"])
    return items

custom.sideNav(3,Warframe.REGAL_AYA.value)

items = store_regal()

_,left,right =st.columns([1,7,1],vertical_alignment="center")

with right.popover(":material/filter_list:",use_container_width=True):
    categories = ["Warframe", "Weapon", "Relic", "Others"]
    selected_categories= st.pills("Pick the desired item type.",categories,selection_mode="multi")
    filtered_data = filter_data(items["items"],selected_categories)

with left:
    paged_items, page, items_per_row, num_of_row = custom.paginations(filtered_data,3)

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