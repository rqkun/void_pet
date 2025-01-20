import streamlit as st

from components import dialogs
import components.markdowns
from config.constants import AppIcons, AppMessages, Warframe
from utils.data_tools import get_frame_abilities_with_image, get_item_image_single

def relic_reward_card(option,item, icon):
    relic_name_cleaned = option["name"].lower().replace(" ","_")
    infor_container = st.container(border=True)
    market_url = Warframe.MARKET.value["url"]
    static_url = Warframe.MARKET.value["static"]
    left,right = infor_container.columns([2,1],vertical_alignment="top")
    with left:
        st.markdown(f"""##### {item["en"]["item_name"]}""")
        st.markdown(components.markdowns.prime_component_info_md(item,option["rarity"],option["chance"]),unsafe_allow_html=True)
        
    with right.container(border=True):
        wiki_url = f"{market_url}/{relic_name_cleaned}"
        st.markdown(f"""
                    <a href="{wiki_url}"><img alt="duca" style="display: block;margin-left: auto;margin-right: auto;" src="{get_item_image_single(option["name"])}"/>""",unsafe_allow_html=True)
    

def item_card(item, image):
    infor_container = st.container(border=True)
    left,right = infor_container.columns([2,1],vertical_alignment="top")
    with left:
        st.markdown(f"""##### {item["name"]}""")
        
        if item["type"] == "Warframe" or item["type"] == "Archwing":
            st.markdown(components.markdowns.warframe_info_md(item["name"]),unsafe_allow_html=True)
        elif "Weapon" in item["uniqueName"] or "Sentinels" in item["category"]:
            st.markdown(components.markdowns.weapon_info_md(item["name"]),unsafe_allow_html=True)
        elif "Relic" in item["type"]:
            st.markdown(components.markdowns.relic_info_md(item["uniqueName"]),unsafe_allow_html=True)
        else: 
            st.markdown(f"""
                    <i>{item["description"]}</i> <br/>
                    """,unsafe_allow_html=True)
        
    with right.container(border=True):
        wiki_url = item["wikiaUrl"] if 'wikiaUrl' in item else Warframe.get_wiki_url("")
        st.markdown(f"""
                    <a href="{wiki_url}"><img alt="ducat" style="display: block;margin-left: auto;margin-right: auto;" src="{image}"/></a>""",unsafe_allow_html=True)
    if "Relic" in item["type"]:
        if right.button("Market",use_container_width=True):
            dialogs.market_check(item)
