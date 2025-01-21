import streamlit as st

from components import dialogs
import components.markdowns
from config.constants import AppIcons, AppLabels, AppMessages, Warframe


def info_module(item):
    if item["type"] == "Warframe" or item["type"] == "Archwing":
        st.markdown(components.markdowns.warframe_info_md(item["name"]),unsafe_allow_html=True)
    elif "Weapon" in item["uniqueName"] or "Sentinels" in item["category"]:
        st.markdown(components.markdowns.weapon_info_md(item["name"]),unsafe_allow_html=True)
    elif "Relic" in item["type"]:
        st.markdown(components.markdowns.relic_info_md(item),unsafe_allow_html=True)
    else: 
        st.markdown(f"""
                <i>{item["description"]}</i> <br/>
                """,unsafe_allow_html=True)

def component(item,market_item, image_url: str, price : int, offers: str):
    relic_name_cleaned = item["item"]["name"].lower().replace(" ","_")
    market_url = Warframe.MARKET.value["url"]
    generic_container = st.container(border=True)
    left,right = generic_container.columns([2,1],vertical_alignment="top")
    with left:
        st.markdown(f"""##### {market_item["en"]["item_name"]}""")
        st.markdown(components.markdowns.prime_component_info_md(market_item,item["rarity"],item["chance"],price,offers),unsafe_allow_html=True)
    with right.container(border=True):
        wiki_url = f"{market_url}/{relic_name_cleaned}"
        st.markdown(f"""
                    <a href="{wiki_url}"><img alt="duca" style="display: block;margin-left: auto;margin-right: auto;" src="{image_url}"/>""",unsafe_allow_html=True)
    right.link_button(AppLabels.MARKET.value,url=wiki_url,use_container_width=True,icon=AppIcons.EXTERNAL.value,type="primary",help=AppMessages.MARKET_TOOL_TIP.value)
    

def generic(item, image_url: str):
    generic_container = st.container(border=True)
    left,right = generic_container.columns([2,1],vertical_alignment="top")
    with left:
        st.markdown(f"""##### {item["name"]}""")
        info_module(item)
    with right.container(border=True):
        wiki_url = item["wikiaUrl"] if 'wikiaUrl' in item else Warframe.get_wiki_url("")
        st.markdown(f"""<a href="{wiki_url}">
                        <img alt="ducat" style="display: block;
                                            margin-left: auto;
                                            margin-right: auto;" 
                            src="{image_url}"/></a>""",unsafe_allow_html=True)
    if "Relic" in item["type"]:
        if right.button(AppLabels.MARKET.value,use_container_width=True,icon=AppIcons.MARKET.value,type="primary"):
            dialogs.market_check(item)
