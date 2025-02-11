import streamlit as st
from components import cards, markdowns
from config.constants import AppIcons, AppLabels, AppMessages, Warframe
from datasources import warframe_status
from utils import data_manage, tools
from utils.data_manage import call_market

@st.dialog(AppLabels.DETAIL_MARKET.value)
def baro_item_check(uniqueName):
    """ Show item details with market lookup options. """
    with st.spinner(AppMessages.LOAD_DATA.value):
        item = warframe_status.get_item_data(uniqueName)
        image_url = tools.get_item_image(uniqueName)
    cards.item_card(item[0],image_url)

@st.dialog(AppLabels.DETAIL_MARKET.value)
def market_check(item):
    """ Market inspection dialog. """
    with st.container(border=True), st.spinner(AppMessages.LOAD_DATA.value):
        
        left,right = st.columns([5,1],vertical_alignment="bottom")
        
        with right.popover(":material/settings:",use_container_width=True):
            status = st.segmented_control(AppLabels.STATUS.value,options=AppLabels.status_options(),default=AppLabels.DEFAULT_STATUS.value,help=AppMessages.OFFER_STATUS_TOOLTIP.value)
            wtb = st.segmented_control(AppLabels.TYPE.value,options=AppLabels.type_options(), default=AppLabels.DEFAULT_TYPE.value,help=AppMessages.OFFER_TYPE_TOOLTIP.value)
            rep = st.number_input(AppLabels.REPUTATION.value,0,step=1)
            limit = st.number_input(AppLabels.NUMBER_OF_TRADES.value,min_value=1,step=1,value=10)
        
        option_map = tools.deforma_rewards(item["rewards"])
    
        reward_option = left.selectbox(
            AppLabels.REWARD_SELECT.value,
            options=option_map,
            format_func= lambda option: option["item"]["name"],
        )

        relic_name_cleaned = reward_option["item"]["name"].lower().replace(" ","_")
        market_url = f"""{Warframe.MARKET.value["url"]}/{relic_name_cleaned}"""
        
        
        item = data_manage.get_market_item(relic_name_cleaned) 
        market_data = call_market(relic_name_cleaned)
        filtered_data = tools.market_filter(market_data,rep=rep, status=status,wtb=wtb)[:limit]
        order = tools.get_min_status_plat(market_data,"ingame")
        whisper = f"""/w {order["user"]["ingame_name"]} Hi! I want to buy: "{item["en"]["item_name"]}" for {order["platinum"]} platinum. (warframe.market)"""
        avg_plat = tools.get_average_plat_price(filtered_data)


        left,right = st.columns([2,1],vertical_alignment="center")
        with left:
            st.markdown(markdowns.prime_component_info_md(item,reward_option["rarity"],reward_option["chance"],avg_plat,len(filtered_data),order["platinum"]),unsafe_allow_html=True)
        right.container(border=True).image(reward_option["item"]["imageName"]) 

    
    st.code(whisper,language="md",wrap_lines=True)
    st.link_button(AppLabels.MARKET.value,url=market_url,use_container_width=True,type="primary",icon=AppIcons.EXTERNAL.value,help=AppMessages.MARKET_TOOL_TIP.value)

        