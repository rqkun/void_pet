import streamlit as st

from components import custom, markdowns
from config.constants import AppIcons, AppLabels, AppMessages, Warframe
from utils import data_manage, tools

from utils.tools import check_pattern_prime_set
from utils.tools import check_pattern_set

custom.sideNav(4)
custom.reject_url_param()
custom.hover_style()

_,middle,_ = st.columns([2,3,2],vertical_alignment="center")

with middle,st.spinner(AppMessages.LOAD_DATA.value,show_time=True,_cache=False):
    options = data_manage.get_all_tradables()["payload"]["items"]

status_placeholder = st.empty()
search_form = st.expander("Search",expanded=True,icon=AppIcons.INSPECT.value).form("market_search_form",clear_on_submit=False,border=False)
left_top,right_top = search_form.columns([5,1],vertical_alignment="center")
option = left_top.multiselect("Search_box",options,
               format_func= lambda option: option["item_name"],
               max_selections=1,
               placeholder="Search up a name",
               label_visibility="collapsed")

left,right=search_form.columns([4,1],vertical_alignment="bottom")

submit = right.form_submit_button("Search",use_container_width=True,icon=AppIcons.INSPECT.value,type="primary")

status = left.segmented_control("Status",
                                ["ingame","offline","online"],
                                selection_mode="single",
                                default="ingame",
                                format_func= lambda x: x.title())

adv_setting = right_top.popover(":material/settings:",use_container_width=True)
rep = adv_setting.number_input(AppLabels.REPUTATION.value,min_value=0,value="min",step=1)
limit = adv_setting.number_input(AppLabels.NUMBER_OF_TRADES.value,min_value=5,value=10,max_value=20,step=1)

container = search_form.container(border=False)
result_container = st.container(border=False)


if submit:
    if option != None and len(option)>0:
        with container, st.spinner("",show_time=True):
            status_placeholder.empty()
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
            market_data = tools.market_filter(data_manage.call_market(option[0]["url_name"]),rep,status=status)
            filtered_data = tools.get_min_status_plat(market_data,status)
            if "orders" in st.session_state:
                del st.session_state.orders
            if filtered_data is not None:
                st.session_state.orders = {
                    "orders": filtered_data,
                    "name": option[0]["item_name"],
                    "image": image,
                    "url_name":option[0]["url_name"],
                    "market_data": item_market
                    }
    else: 
        status_placeholder.warning("Please select an item.",icon=AppIcons.WARNING.value)
            

        
if 'orders' in st.session_state:
    orders = st.session_state.orders
    with search_form: 
        custom.set_divider()
        left,right = search_form.columns([1,4],vertical_alignment="center")
        left.markdown(markdowns.image_md(Warframe.MARKET.value["url"]+orders["url_name"],orders["name"],orders["image"],"hidden"),unsafe_allow_html=True)
        with right:
            st.markdown(markdowns.market_item_desc(orders["market_data"]),unsafe_allow_html=True)
            st.pills("Tags",orders["market_data"]["tags"],disabled=True,label_visibility="collapsed")
    with result_container:
        if len(orders["orders"]) ==0:
            st.write(" ")
            custom.empty_result(f"""{option[0]["item_name"]} with current filters.""")
        else:
            custom.market_style()
            paged_items, items_per_row = custom.paginations(orders["orders"],items_per_row=1,num_of_row=limit)
            for order in paged_items:
                st.markdown(markdowns.market_order_md(order,orders["market_data"]),unsafe_allow_html=True)
                whisper = f"""/w {order["user"]["ingame_name"]} Hi! I want to buy: "{orders["name"]}" for {order["platinum"]} platinum. (warframe.market)"""
                st.code(whisper,language="md",wrap_lines=False)
                st.write(" ")