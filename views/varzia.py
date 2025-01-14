import streamlit as st
from utils import api_services, data_tools, headers, structures

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
    left_top,right_top = infor_container.columns([5,1],vertical_alignment="top")
    left_top.markdown(f"""## {item["en"]["item_name"]}""")
    right_top.link_button(AppIcons.EXTERNAL.value,f"{st.secrets.market_api.web}/{relic_name_cleaned}",type="tertiary",use_container_width=True,help="Go to warframe.market.")
    
    left_bot,right_bot = infor_container.columns([2,1],vertical_alignment="top")
    with left_bot.container(border=True):
        
        st.markdown(f"""
                    Rarity: <font color="#FF4B4B">{option["rarity"]}</font> | Base chances: <font color="#FF4B4B">{option["chance"]}</font> %<br />
                    Ducats: <font color="#FF4B4B">{item["ducats"]}</font> <img alt="ducat" style="width:20px;height:20px;" src="{AppIcons.DUCAT.value}"/> <br/>
                    MR: <font color="#FF4B4B">{item["mastery_level"]}</font> <br />
                    """,unsafe_allow_html=True)

    right_bot.container().markdown(f"""
                    <img alt="ducat" style="display: block;margin-left: auto;margin-right: auto;" src="{st.secrets.market_api.static}/{icon}"/>""",unsafe_allow_html=True)
    right_bot.container().write("")
    
    #market check
    inspect_form = st.form("market_inspection_form",border=False)
    left_number,right_number = inspect_form.columns([1,1],vertical_alignment="top")
    left_select,right_select = inspect_form.columns([2,1],vertical_alignment="top")
    options = ["All", "Online", "Offline", "Ingame"]
    status = left_select.segmented_control("Status",options,default="All",help="Include all trades when empty.")
    wtb = right_select.segmented_control("Type",options=["WTS","WTB"],help="WTS: sell offers, WTB: buy offers. Default to WTS if empty.", default="WTS")

    
    rep = left_number.number_input("Reputation threshold: ",0,step=1)
    limit = right_number.number_input("Number of Trades: ",min_value=1,step=1,value=10)
    submit = inspect_form.form_submit_button("Inspect",use_container_width=True,icon=AppIcons.INSPECT.value,type="primary")
    bottom_contain_r = inspect_form.container(border=True)
        
    if submit:
        market_data = data_tools.market_filter(call_market(relic_name_cleaned),rep=rep, status=status,wtb=wtb)[:limit]
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
with mid:
    headers.basic(logo=AppIcons.AYA.value)
    

if 'varzia_wares' not in st.session_state:
    full_data=api_services.get_varzia_data()
    filtered_data = [item for item in full_data["inventory"] if item['credits'] is not None]
    st.session_state["varzia_wares"] = structures.ware_object("varzia",filtered_data)

data = st.session_state.varzia_wares["data"]
with mid:
    relics = store_varzia(data)
    with st.spinner("Loading relics..."):
        all_prime=  api_services.get_all_prime_names()
        prime_frame_options = data_tools.get_prime_resurgent(all_prime,relics)
        bot_left, bot_right =st.columns([4,1],vertical_alignment="bottom")
        prime = bot_left.selectbox(
            "Choose a Prime.",
            prime_frame_options
        )
        
        wiki_url = prime.replace(" ","_")
        bot_right.link_button("Wiki",url=f"https://warframe.fandom.com/wiki/{wiki_url}",use_container_width=True,icon=AppIcons.WIKI.value,help=f"Go to {prime} Wiki.")
        names = data_tools.search_rewards([prime],relics)
    
    relic_index = st.selectbox("Choose a relic to inspect it's rewards: ",
                options=names,
                )
    
    option_map = data_tools.get_relic_reward_options(relics,relic_index)
    reward_form = st.form("reward_inspect_form",clear_on_submit=False,border=False)
    reward_option = reward_form.radio(
        "Choose a reward to inspect: ",
        options=option_map.keys(),
    )
    
    #
    if reward_form.form_submit_button("Market",disabled=("Forma Blueprint" in reward_option),use_container_width=True,icon=AppIcons.MARKET.value,type="primary"):
        relic_reward_check(option_map[reward_option])
    # 
