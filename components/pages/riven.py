
import streamlit as st
from components import custom, markdowns
from config.constants import AppIcons
from utils import data_manage
import streamlit_antd_components as sac


custom.sideNav(6)
custom.hover_effect()

_,middle,_ = st.columns([3,2,3],vertical_alignment="center")

with middle,st.spinner("",show_time=True,_cache=False):
    riven_items, riven_attributes = data_manage.get_rivens_settings()
status_placeholder = st.empty()
search_form = st.form("riven_search_form",clear_on_submit=False)
container = st.container(border=False)
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

left,right=search_form.columns([4,1],vertical_alignment="center")

submit = right.form_submit_button("Search",use_container_width=True,icon=AppIcons.INSPECT.value,type="primary")
adv_setting = right_top.popover(":material/settings:",use_container_width=True)

left,right=adv_setting.columns([1,1],vertical_alignment="top")
polarity = adv_setting.pills("Polarity",
                ["madurai","vazarin","naramon","zenurik"],
                format_func= lambda x: x.title(),selection_mode="single")
left,right=adv_setting.columns([1,1],vertical_alignment="center")
reroll_min = left.number_input("Reroll min",min_value=0,value="min",step=1)
reroll_max = right.number_input("Reroll max",min_value=0,step=1,value=100)





if submit:
    st.json(weapon)
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
            rivens = data_manage.get_rivens(weapon[0]["url_name"],
                                                buyout_policy=None,
                                                positive_stats=positive_stats, 
                                                negative_stats=negative_stats,
                                                operation=None,
                                                re_rolls_min=reroll_min,
                                                re_rolls_max=reroll_max,
                                                polarity=polarity)
            if rivens is not None:
                st.session_state.rivens = {
                    "auctions": rivens,
                    "item_name": weapon[0]["item_name"],
                    }
            else:
                status_placeholder.warning("No Rivens found.",icon=AppIcons.WARNING.value)

if 'rivens' in st.session_state:
    st.html("components/htmls/auction.html")
    paged_items, items_per_row = custom.paginations(st.session_state.rivens['auctions'],10,items_per_row=1)
    # st.json(paged_items)
    with container, st.spinner("",show_time=True):
        if 'item_name' in st.session_state['rivens']:
            item = data_manage.get_weapon_by_name(st.session_state['rivens']['item_name'])
            image = data_manage.get_image_url(item["uniqueName"],True)
    for idx, auction in enumerate(iterable=paged_items):
        if auction is not None:
            st.markdown(markdowns.riven_auction_md(auction,image),unsafe_allow_html=True)




