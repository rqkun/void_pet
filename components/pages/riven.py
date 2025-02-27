
import streamlit as st
from components import custom, markdowns
from config.constants import AppIcons, AppMessages, Warframe
from utils import data_manage


custom.sideNav(6)
custom.reject_url_param()
custom.image_style()


_,middle,_ = st.columns([2,3,2],vertical_alignment="center")

with middle,st.spinner(AppMessages.LOAD_DATA.value,show_time=True,_cache=False):
    riven_items, riven_attributes = data_manage.get_rivens_settings()
status_placeholder = st.empty()
search_form = st.expander("Search",expanded=True,icon=AppIcons.INSPECT.value).form("riven_search_form",clear_on_submit=False,border=False)
left,right=search_form.columns([1,1],vertical_alignment="top")
weapon = left.multiselect(
    "Select a weapon",
    options= riven_items,
    format_func= lambda x: x["item_name"],
    max_selections=1
)
neg_atr = right.multiselect(
    "Select a negative attribute",
    options= riven_attributes,
    format_func= lambda x: x["effect"],
    max_selections=1
)
left_top,right_top=search_form.columns([7,1],vertical_alignment="bottom")

pos_atr = left_top.multiselect(
    "Select positive attributes",
    options= riven_attributes,
    format_func= lambda x: x["effect"],
    max_selections=3,
    placeholder="Choose up to 3 attributes"
)

left,right=search_form.columns([4,1],vertical_alignment="bottom")

submit = right.form_submit_button("Search",use_container_width=True,icon=AppIcons.INSPECT.value,type="primary")
status = left.segmented_control("Status",
                                Warframe.ONLINE_STATUS.value["list"],
                                selection_mode="single",
                                default="ingame",
                                format_func= lambda x: x.title())
adv_setting = right_top.popover(AppIcons.SETTING.value,use_container_width=True)

left,right=adv_setting.columns([1,1],vertical_alignment="top")
polarity = adv_setting.pills("Polarity",
                ["madurai","vazarin","naramon","zenurik"],
                format_func= lambda x: x.title(),selection_mode="single")
left,right=adv_setting.columns([1,1],vertical_alignment="center")
reroll_min = left.number_input("Reroll min",min_value=0,value="min",step=1)
reroll_max = right.number_input("Reroll max",min_value=0,step=1,value=100)

container = search_form.container(border=False)
result_container = st.container(border=False)


if submit:
    if len(weapon) ==0:
        status_placeholder.warning("Please select a weapon.",icon=AppIcons.WARNING.value)
    else:
        with container, st.spinner("",show_time=True):
            status_placeholder.empty()
            positive_stats=[]
            negative_stats=[]
            for item in pos_atr:
                positive_stats.append(item["url_name"])
            for item in neg_atr:
                negative_stats.append(item["url_name"])
        
            if "rivens" in st.session_state:
                del st.session_state.rivens
            item = data_manage.get_weapon_by_name(weapon[0]['item_name'])
            image = data_manage.get_image_url(item["uniqueName"],True)
            rivens = data_manage.get_rivens(weapon[0]["url_name"],
                                                buyout_policy=None,
                                                positive_stats=positive_stats, 
                                                negative_stats=negative_stats,
                                                operation=None,
                                                re_rolls_min=reroll_min,
                                                re_rolls_max=reroll_max,
                                                polarity=polarity,status=status)

            st.session_state.rivens = {
                "auctions": rivens,
                "item": item,
                "image": image,
                }

if 'rivens' in st.session_state:
    if st.session_state.rivens['auctions'] is None or len(st.session_state.rivens['auctions']) ==0:
        st.write(" ")
        custom.empty_result(f"""Riven with current filters.""")
    else:
        current_rivens = st.session_state.rivens['auctions']
        custom.auction_style()
        start_idx, end_idx, items_per_row = custom.paginations(len(current_rivens),10,items_per_row=1)
        view_rivens = current_rivens[start_idx:end_idx]
        for idx, auction in enumerate(iterable=view_rivens):
            if auction is not None:
                st.markdown(markdowns.riven_auction_md(auction,st.session_state['rivens']['image']),unsafe_allow_html=True)
                name = f"""{st.session_state['rivens']['item']["name"]} {auction["item"]["name"].replace("-"," ").title().replace(" ","-")}"""
                whisper = f"""/w {auction["owner"]["ingame_name"]} Hi! I want to buy: "{name}" riven. """
                st.code(whisper,language="md",wrap_lines=True)




