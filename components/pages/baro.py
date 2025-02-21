from datetime import datetime
from millify import millify
import streamlit as st
from components import cards, custom
from utils import data_manage

from config.constants import AppIcons, AppMessages, AppPages, Warframe
from utils.tools import filter_data, format_timedelta

def store_baro():
    """ Loading data. """
    _,middle,_ = st.columns([2,3,2],vertical_alignment="center")
    with middle,st.spinner(AppMessages.LOAD_DATA.value,show_time=True,_cache=False):
        full_data=data_manage.get_baro()
    if full_data["active"] is False:
        date = datetime.strptime(full_data["activation"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
        items= None
        alert_message = AppMessages.baro_time_message(format_timedelta(date))
    else:
        items = data_manage.preload_data(full_data["inventory"])
        date = datetime.strptime(full_data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
        alert_message = f"""Baro will leave in {format_timedelta(date)}"""

    st.session_state.baro_alert = {
        "active" : full_data["active"],
        "message" : alert_message
    }
    
    return items

custom.sideNav(2)
custom.reject_url_param()
custom.image_style()
custom.card_style()
items = store_baro()
if 'baro_alert' in st.session_state:
    custom.baro_time_alert(st.session_state.baro_alert["message"])

if items is not None:
    left,mid,right =st.columns([1,7,1],vertical_alignment="center")
    with left.popover(":material/filter_list:",use_container_width=True):
        categories = ["Warframe", "Weapon", "Relic", "Others"]
        selected_categories= st.pills("Pick the desired item type.",categories,selection_mode="multi")
        filtered_data = filter_data(items["items"],selected_categories)

    with mid:
        paged_items, items_per_row = custom.paginations(filtered_data,3)

    if right.button(AppIcons.SYNC.value,type="primary",use_container_width=True, help="Force reload data."):
        data_manage.clear_cached_item_call()
        st.switch_page(AppPages.BARO.value)

    _,middle,_ = st.columns([3,2,3],vertical_alignment="center")

    with middle,st.spinner("",show_time=True,_cache=False):
        for item in paged_items:
            item["image"] = data_manage.get_image_url(item["uniqueName"])
            type = Warframe.DUCAT.value
            amount = item["ducats"]
            item["html"] = cards.generic(package=item, image_url=item["image"], price_info=
                    {
                        "type": type,
                        "amount": millify(amount,precision=2)
                    })

    list_col = st.columns(items_per_row)
    start_idx = 0
    custom.varzia_style()
    for idx, item in enumerate(iterable=paged_items[start_idx:]):
        with list_col[idx%items_per_row]:
            if item is not None:
                st.markdown(item["html"],unsafe_allow_html=True)
else:
    with st.container(border=False):
        st.html("<br><br>")
        custom.empty_result(f"""items.""")