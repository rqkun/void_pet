import streamlit as st

from components import custom, markdowns
from config.constants import AppIcons, AppLabels, AppMessages, Warframe
from utils import data_manage, tools

from utils.tools import check_pattern_prime_set
from utils.tools import check_pattern_set

custom.sideNav(4)
custom.reject_url_param()
custom.hover_effect()
_,middle,_ = st.columns([2,3,2],vertical_alignment="center")

with middle,st.spinner(AppMessages.LOAD_DATA.value,show_time=True,_cache=False):
    options = data_manage.get_all_tradables()["payload"]["items"]
left,mid,right = st.columns([1,5,1],vertical_alignment="center")
with left.popover(":material/settings:",use_container_width=True):
    rep = st.number_input(AppLabels.REPUTATION.value,0,step=1)
    limit = st.number_input(AppLabels.NUMBER_OF_TRADES.value,min_value=1,step=1,value=10,max_value=10,help="Max 10 trades.")
        
option = mid.multiselect("Search_box",options,
               format_func= lambda option: option["item_name"],
               max_selections=1,
               placeholder="Search up a name",
               label_visibility="collapsed")

if right.button(AppIcons.SYNC.value,use_container_width=True,type="primary"):
    st.rerun()

left,right = st.columns([1,4],vertical_alignment="center")
if option != None and len(option)>0:
    custom.market_item_style()
    with st.spinner(AppMessages.LOAD_DATA.value,show_time=True):
        item_market = data_manage.get_market_item(option[0]["url_name"])
        if check_pattern_prime_set(option[0]["url_name"]):
            name = option[0]["item_name"].replace(" Set","").replace(" Blueprint","")
            item = data_manage.get_item_by_name(name)
            image = data_manage.get_image_url(item["uniqueName"])
        elif check_pattern_set(option[0]["url_name"]):
            name = option[0]["item_name"].replace(" Set","")
            item = data_manage.get_item_by_name(name)
            image = data_manage.get_image_url(item["uniqueName"])
        else:
            image = Warframe.MARKET.value["static"] + item_market["icon"]

        left.markdown(markdowns.image_md(Warframe.MARKET.value["url"]+option[0]["url_name"],option[0]["item_name"],image,"hidden"),unsafe_allow_html=True)
        with right:
            st.markdown(markdowns.market_item_desc(item_market),unsafe_allow_html=True)
            st.pills("Tags",item_market["tags"],disabled=True,label_visibility="collapsed")
        market_data = tools.market_filter(data_manage.call_market(option[0]["url_name"]),rep,status="ingame")
        filtered_data = tools.get_min_status_plat(market_data,"ingame")[:limit]

    if len(filtered_data) >0:
        for order in filtered_data:
            left,right = st.columns([4,1],vertical_alignment="center")
            left.markdown(markdowns.market_order_md(order),unsafe_allow_html=True)
            with right.popover("Copy",use_container_width=True,icon=":material/content_copy:"):
                whisper = f"""/w {order["user"]["ingame_name"]} Hi! I want to buy: "{option[0]["item_name"]}" for {order["platinum"]} platinum. (warframe.market)"""
                st.code(whisper,language="md",wrap_lines=True)
    else:
        with st.container(border=False):
            st.html("<br>")
            custom.empty_result(f"""{option[0]["item_name"]} with current filters.""")
            

        


