import streamlit as st

import components.markdowns
from config.constants import AppIcons, AppMessages, Warframe
from utils.data_tools import get_frame_abilities_with_image

def relic_reward_card(option,item, icon):
    relic_name_cleaned = option["name"].lower().replace(" ","_")
    infor_container = st.container(border=True)
    market_url = Warframe.MARKET.value["url"]
    static_url = Warframe.MARKET.value["static"]
    left,right = infor_container.columns([2,1],vertical_alignment="top")
    with left:
        st.markdown(f"""##### {item["en"]["item_name"]}""")
        st.markdown(f"""
                    Rarity: <font color="#FF4B4B">{option["rarity"]}</font> | Base chances: <font color="#FF4B4B">{option["chance"]}</font> %<br />
                    Ducats: <font color="#FF4B4B">{item["ducats"]}</font> <img alt="ducat" style="width:20px;height:20px;" src="{Warframe.DUCAT.value}"/> <br/>
                    MR: <font color="#FF4B4B">{item["mastery_level"]}</font> <br />
                    """,unsafe_allow_html=True)
        
    with right.container(border=True):
        wiki_url = f"{market_url}/{relic_name_cleaned}"
        st.markdown(f"""
                    <a href="{wiki_url}"><img alt="ducat" style="display: block;margin-left: auto;margin-right: auto;" src="{static_url}/{icon}"/>""",unsafe_allow_html=True)
    

def info_card(item, image):
    infor_container = st.container(border=True)
    
    left,right = infor_container.columns([2,1],vertical_alignment="top")

    with left:
        st.markdown(f"""##### {item["name"]}""")
        
        if item["type"] == "Warframe":
            
            st.markdown(components.markdowns.warframe_abilities(item["name"]),unsafe_allow_html=True)
        else: 
            st.markdown(f"""
                    <i>{item["description"]}</i> <br/>
                    """,unsafe_allow_html=True)
    with right.container(border=True):
        wiki_url = item["wikiaUrl"] if 'wikiaUrl' in item else Warframe.get_wiki_url("")
        st.markdown(f"""
                    <a href="{wiki_url}"><img alt="ducat" style="display: block;margin-left: auto;margin-right: auto;" src="{image}"/></a>""",unsafe_allow_html=True)

    
        
    