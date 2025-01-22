import streamlit as st
from components import cards
from config.constants import AppIcons, AppLabels, AppMessages
from datasources import warframe_status
from utils import data_manage, data_tools
from utils.data_manage import call_market


@st.dialog(AppLabels.DETAIL_MARKET.value)
def baro_item_check(uniqueName):
    """ Show item details with market lookup options. """
    with st.spinner(AppMessages.LOAD_DATA.value):
        item = warframe_status.get_item_data(uniqueName)
        image_url = data_tools.get_item_image(uniqueName)
    cards.item_card(item[0],image_url)

@st.dialog(AppLabels.DETAIL_MARKET.value)
def market_check(item):
    """ Market inspection dialog. """
    option_map = item["rewards"]
    reward_form = st.form("reward_inspect_form",clear_on_submit=False,border=False)
    reward_option = reward_form.selectbox(
        AppLabels.REWARD_SELECT.value,
        options=option_map,
        format_func= lambda option: option["item"]["name"],
    )
    left_number,right_number = reward_form.columns([1,1],vertical_alignment="top")
    left_select,right_select = reward_form.columns([2,1],vertical_alignment="top")
    status = left_select.segmented_control(AppLabels.STATUS.value,options=AppLabels.status_options(),default=AppLabels.DEFAULT_STATUS.value,help=AppMessages.OFFER_STATUS_TOOLTIP.value)
    wtb = right_select.segmented_control(AppLabels.TYPE.value,options=AppLabels.type_options(), default=AppLabels.DEFAULT_TYPE.value,help=AppMessages.OFFER_TYPE_TOOLTIP.value)
    rep = left_number.number_input(AppLabels.REPUTATION.value,0,step=1)
    limit = right_number.number_input(AppLabels.NUMBER_OF_TRADES.value,min_value=1,step=1,value=10)
    bottom_contain_r = reward_form.container(border=False)
    submit = reward_form.form_submit_button(AppLabels.INSPECT.value,use_container_width=True,icon=AppIcons.INSPECT.value,type="secondary")
    
    if submit:
        with bottom_contain_r,st.spinner(AppMessages.LOAD_DATA.value):
            relic_name_cleaned = reward_option["item"]["name"].lower().replace(" ","_")
            item = data_manage.get_market_item(relic_name_cleaned)  
            market_data = data_tools.market_filter(call_market(relic_name_cleaned),rep=rep, status=status,wtb=wtb)[:limit]
            avg_plat = data_tools.get_average_plat_price(market_data)
            cards.component(reward_option,item,reward_option["item"]["imageName"],avg_plat,len(market_data))
        