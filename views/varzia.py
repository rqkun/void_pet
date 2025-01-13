import streamlit as st
from utils import api_services, data_tools, headers, structures
from PIL import Image
import requests
from io import BytesIO

from utils.icons import AppIcons

@st.cache_data(show_spinner=False)
def call_market(option):
    with st.spinner("Loading market values..."):
        return api_services.get_market_orders(option)['payload']['orders']

@st.dialog("Details")
def relic_reward_check(option):
    relic_name_cleaned = option["name"].lower().replace(" ","_")
    with st.spinner("Loading data..."):
        single_item =api_services.get_market_item(relic_name_cleaned)
        item = data_tools.get_correct_piece(single_item["payload"]["item"]["items_in_set"],name=relic_name_cleaned)   
        icon = item["sub_icon"]
    
    infor_container = st.container(border=True)
    infor_container.markdown(f"""## {item["en"]["item_name"]}""")
    left_top,right_top = infor_container.columns([2,1],vertical_alignment="top")
    with left_top.container(border=False):
        
        st.markdown(f"""
                    Rarity: <font color="#FF4B4B">{option["rarity"]}</font> | Base chances: <font color="#FF4B4B">{option["chance"]}</font> %<br />
                    Ducats: <font color="#FF4B4B">{item["ducats"]}</font> <img alt="ducat" style="width:20px;height:20px;" src="{AppIcons.DUCAT.value}"/> <br/>
                    MR: <font color="#FF4B4B">{item["mastery_level"]}</font> <br />
                    Description: {item["en"]["description"]} <br />
                    """,unsafe_allow_html=True)

    right_top.container().markdown(f"""
                    <img alt="ducat" style="display: block;margin-left: auto;margin-right: auto;" src="{st.secrets.market_api.static}/{icon}"/>""",unsafe_allow_html=True)
    right_top.container().write("")
    
    #market check
    left_top,right_top = st.columns([2,1],vertical_alignment="bottom")
    wtb = st.toggle("Are you finding someone to buy ?")
    offline = st.toggle("Include offline orders ?")
    rep = left_top.number_input("Reputation threshold: ",0,step=1)
    limit = right_top.number_input("Number of Trades: ",1,step=1)
    left_bot,right_bot = st.columns([5,1],vertical_alignment="bottom")
    bottom_contain_r = st.container(border=True)
    right_bot.link_button(AppIcons.EXTERNAL.value,f"{st.secrets.market_api.web}/{relic_name_cleaned}",type="secondary",use_container_width=True,help="Go to warframe.market.")
        
    if left_bot.button("Inspect",use_container_width=True,icon=AppIcons.INSPECT.value,type="primary"):
        market_data =data_tools.market_filter(call_market(relic_name_cleaned),rep=rep, offline=offline,wtb=wtb)[:limit]
        avg_plat = data_tools.get_average_plat_price(market_data)
        bottom_contain_r.markdown(f"""<div> Average: <font color="#FF4B4B">{avg_plat:.2f} <img alt="plat" style="width:20px;height:20px;" src="{AppIcons.PLATINUM.value}"/> </font> Platinum(s) from <font color="#FF4B4B">{len(market_data)}</font> offer(s). </a> <br>""",unsafe_allow_html=True)
        bottom_contain_r.write("")

def store_varzia(data):
    if 'varzia_wares_detail' not in st.session_state:
        relic_list = []
        progress_text = "Operation in progress. Please wait."
        progress = st.progress(0, text=progress_text)
        for i, item in enumerate(data):
            relic_unique_name = item["item"].replace(" ","")
            tmp = api_services.get_relic_data(relic_unique_name)
            item_name = tmp["name"].replace('Intact', '')
            relic_list.append(structures.relic_object(price=item["credits"],data=tmp))
            progress.progress((i+1)/len(data), text=f"Indexed: {item_name}")
        st.session_state.varzia_wares_detail = relic_list
        progress.empty()
        return relic_list
    else:
        return st.session_state.varzia_wares_detail
    
    
query_params = st.query_params.to_dict()

if len(query_params)>0:
    st.switch_page("views/error.py")
    
_, mid,_ = st.columns([1,4,1])

if 'varzia_wares' not in st.session_state:
    full_data=api_services.get_varzia_data()
    filtered_data = [item for item in full_data["inventory"] if item['credits'] is not None]
    st.session_state["varzia_wares"] = structures.ware_object("varzia",filtered_data)
    
data = st.session_state.varzia_wares["data"]
with mid:
    headers.basic(logo=AppIcons.AYA.value)
    with st.spinner("Loading relics..."):
        relics = store_varzia(data)

        prime_frame_options=  api_services.get_all_prime_names()
        primes = st.multiselect(
            "Which Primes",
            prime_frame_options,
            placeholder="Leave empty if check all of the relics currently available."
            
        )
        
        names = data_tools.search_rewards(primes,relics)
    if len(names)>0:
        relic_index = st.selectbox("Choose a relic to inspect it's rewards: ",
                    options=names,
                    )
        option_map = data_tools.get_relic_reward_options(relics,relic_index)
        reward_option = st.radio(
            "Choose a reward to inspect: ",
            options=option_map.keys(),
        )
        
        bot_right, bot_left=st.columns([5,1])
        if bot_right.button("Market",disabled=("Forma Blueprint" in reward_option),use_container_width=True,icon=AppIcons.MARKET.value,type="primary"):
            relic_reward_check(option_map[reward_option])
        wiki_url = data_tools.extract_prime_substring(reward_option).replace(" ","/")
        bot_left.link_button(AppIcons.DETAILS.value,url=f"https://warframe.fandom.com/wiki/{wiki_url}",use_container_width=True)
    else:
        st.warning("Currently not on rotation.")

