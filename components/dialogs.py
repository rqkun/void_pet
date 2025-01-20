import streamlit as st
from components import cards
from config.constants import AppIcons, AppLabels, AppMessages, Warframe
from utils import api_services, data_tools


@st.cache_data(show_spinner=False)
def call_market(option):
    """ All the market API. """
    with st.spinner(AppMessages.LOAD_DATA.value):
        return api_services.get_market_orders(option)['payload']['orders']

@st.dialog(AppLabels.DETAIL_MARKET.value)
def relic_reward_check(option):
    """ Show item details with market lookup options. """
    relic_name_cleaned = option["name"].lower().replace(" ","_")
    with st.spinner(AppMessages.LOAD_DATA.value):
        single_item =api_services.get_market_item(relic_name_cleaned)
        item = data_tools.get_correct_piece(single_item["payload"]["item"]["items_in_set"],name=relic_name_cleaned)   
        icon = item["sub_icon"]

    cards.relic_reward_card(option,item,icon)
    
    #market check
    inspect_form = st.form("market_inspection_form",border=False)
    left_number,right_number = inspect_form.columns([1,1],vertical_alignment="top")
    left_select,right_select = inspect_form.columns([2,1],vertical_alignment="top")
    status = left_select.segmented_control(AppLabels.STATUS.value,options=AppLabels.status_options(),default=AppLabels.DEFAULT_STATUS.value,help=AppMessages.OFFER_STATUS_TOOLTIP.value)
    wtb = right_select.segmented_control(AppLabels.TYPE.value,options=AppLabels.type_options(), default=AppLabels.DEFAULT_TYPE.value,help=AppMessages.OFFER_TYPE_TOOLTIP.value)
    rep = left_number.number_input(AppLabels.REPUTATION.value,0,step=1)
    limit = right_number.number_input(AppLabels.NUMBER_OF_TRADES.value,min_value=1,step=1,value=10)
    submit = inspect_form.form_submit_button(AppLabels.INSPECT.value,use_container_width=True,icon=AppIcons.INSPECT.value,type="primary")
    bottom_contain_r = inspect_form.container(border=True)
        
    if submit:
        market_data = data_tools.market_filter(call_market(relic_name_cleaned),rep=rep, status=status,wtb=wtb)[:limit]
        avg_plat = data_tools.get_average_plat_price(market_data)
        bottom_contain_r.markdown(f"""<div> Average: <font color="#FF4B4B">{avg_plat:.2f} <img alt="plat" style="width:20px;height:20px;" src="{Warframe.PLATINUM.value}"/> </font> Platinum(s) from <font color="#FF4B4B">{len(market_data)}</font> offer(s). </a> <br>""",unsafe_allow_html=True)
        bottom_contain_r.write("")



@st.dialog(AppLabels.DETAIL_MARKET.value)
def baro_item_check(uniqueName):
    """ Show item details with market lookup options. """
    with st.spinner(AppMessages.LOAD_DATA.value):
        item = api_services.get_item_data(uniqueName)
        image_url = data_tools.get_item_image(uniqueName)
    cards.item_card(item[0],image_url)

@st.dialog(AppLabels.DETAIL_MARKET.value,width="large")
def market_check(item):
    option_map = data_tools.get_relic_reward(item)
    reward_form = st.form("reward_inspect_form",clear_on_submit=False,border=False)
    reward_option = reward_form.selectbox(
        AppLabels.REWARD_SELECT.value,
        options=option_map.keys(),
    )
    
    
    
    st.write(reward_option)

    if reward_form.form_submit_button(AppLabels.MARKET.value,use_container_width=True,icon=AppIcons.MARKET.value,type="primary"):
        with st.spinner(AppMessages.LOAD_DATA.value):
            relic_name_cleaned = option_map[reward_option]["name"].lower().replace(" ","_")
            single_item =api_services.get_market_item(relic_name_cleaned)
            item = data_tools.get_correct_piece(single_item["payload"]["item"]["items_in_set"],name=relic_name_cleaned)   
            icon = item["sub_icon"]

            cards.relic_reward_card(option_map[reward_option],item,icon)
        