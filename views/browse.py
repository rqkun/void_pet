import streamlit as st
from utils import api_services, data_tools, structures
from PIL import Image
import requests
from io import BytesIO

@st.cache_data(show_spinner=False)
def call_market(option):
    with st.spinner("Loading market values..."):
        return api_services.get_market_orders(option)['payload']['orders']

@st.dialog("Relic")
def relic_reward_check(option):
    relic_name_cleaned = option["name"].lower().replace(" ","_")
    left_top,right_top = st.columns(2,vertical_alignment="bottom")
    wtb = st.toggle("Are you finding someone to buy ?")
    offline = st.toggle("Include offline orders ?")
    rep = left_top.number_input("Reputation threshold: ",0,step=1)
    limit = right_top.number_input("Number of Trades: ",1,step=1)
    left_bot,right_bot = st.columns([2,3],vertical_alignment="center")
    bottom_contain_r = right_bot.container(border=True)
    if left_bot.button("GO",use_container_width=True):
        market_data =data_tools.market_filter(call_market(relic_name_cleaned),rep=rep, offline=offline,wtb=wtb)[:limit]
        avg_plat = data_tools.get_average_plat_price(market_data)
        bottom_contain_r.markdown(f"""Average: <font color="#FF4B4B">**{avg_plat:.2f}** <img alt="plat" style="width:20px;height:20px;" src="https://static.wikia.nocookie.net/warframe/images/e/e7/PlatinumLarge.png"/> </font> Platinum(s)""",unsafe_allow_html=True)

@st.dialog("Details")
def relic_reward_detail(option):
    with st.spinner("Retrieving data..."):
        relic_name_cleaned = option["name"].lower().replace(" ","_")
        single_item =api_services.get_market_item(relic_name_cleaned)
        left_top,right_top = st.columns([2,1])
        item = data_tools.get_correct_piece(single_item["payload"]["item"]["items_in_set"],name=relic_name_cleaned)                          
        icon = item["sub_icon"]
        with left_top.container(border=False):
            st.markdown(f"""## {item["en"]["item_name"]}""")
            st.markdown(f"""Ducats: {item["ducats"]} <img alt="ducat" style="width:20px;height:20px;" src="https://static.wikia.nocookie.net/warframe/images/d/d5/OrokinDucats.png"/> <br/>
                        Rarity: `{option["rarity"]}` Base chances: `{option["chance"]}`<br />
                        MR: {item["mastery_level"]} <br />
                        Wiki: [here]({item["en"]["wiki_link"]}) <br />
                        """,unsafe_allow_html=True)
        response = requests.get(f"{st.secrets.market_api.static}/{icon}")
        img = Image.open(BytesIO(response.content)).resize((200, 200))
        right_top.container(border=True).image(img)
    
    


def store_varzia(data):
    if 'browse_wares_detail' not in st.session_state:
        relic_list = []
        progress_text = "Operation in progress. Please wait."
        progress = st.progress(0, text=progress_text)
        for i, item in enumerate(data):
            relic_unique_name = item["item"].replace(" ","")
            tmp = api_services.get_relic_data(relic_unique_name)
            item_name = tmp["name"].replace('Intact', '')
            relic_list.append(structures.relic_object(price=item["credits"],data=tmp))
            progress.progress((i+1)/len(data), text=f"Indexed: {item_name}")
        st.session_state.browse_wares_detail = relic_list
        progress.empty()
        return relic_list
    else:
        return st.session_state.browse_wares_detail
    
_, mid,_ = st.columns([1,4,1])

if 'browse_wares' not in st.session_state:
    st.switch_page("views/home.py")
else:
    if st.session_state.browse_wares["vendor"] =="varzia":
        
        data = st.session_state.browse_wares["data"]
        with mid:
            relics = store_varzia(data)

            prime_frame_options=  api_services.get_all_prime_names()
            primes = st.multiselect(
                "Which Primes",
                prime_frame_options,
                placeholder="Leave empty if check all of the relic currently available."
                
            )
            
            
            names = data_tools.search_rewards(primes,relics)
            if len(names)>0:
                relic_index = st.selectbox("Choose reward from: ",
                            options=names,
                            )
                option_map = data_tools.get_relic_reward_options(relics,relic_index)
                option = st.radio(
                    "Choose reward: ",
                    options=option_map.keys(),
                )
                
                bot_right, bot_left=st.columns(2)
                if bot_right.button("Market",disabled=("Forma Blueprint" in option),use_container_width=True):
                    relic_reward_check(option_map[option])
                if bot_left.button("Detail",use_container_width=True):
                    relic_reward_detail(option_map[option])
            else:
                st.warning("Currently not on rotation.")

