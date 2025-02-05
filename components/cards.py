import streamlit as st
from PIL import Image
from components import dialogs
import components.markdowns
from config.constants import AppIcons, AppLabels, AppMessages, Warframe
from utils import api_services
from utils import data_manage


def info_module(item):
    """ Categorized item markdown. """
    if item["type"] == "Warframe" or item["type"] == "Archwing":
        st.markdown(components.markdowns.warframe_info_md(item["name"]),unsafe_allow_html=True)
    elif ("Weapons" in item["uniqueName"] or "Sentinels" in item["category"]) and item["category"] != "Skins":
        st.markdown(components.markdowns.weapon_info_md(item["name"]),unsafe_allow_html=True)
    elif "Relic" in item["type"]:
        st.markdown(components.markdowns.relic_info_md(item),unsafe_allow_html=True)
    else: 
        st.markdown(f"""
                <i>{item["description"]}</i> <br/>
                """,unsafe_allow_html=True)

def component(item,market_item, image_url: str, price : int, offers: str):
    """ Prime component info card. """
    relic_name_cleaned = item["item"]["name"].lower().replace(" ","_")
    market_url = Warframe.MARKET.value["url"]
    generic_container = st.container(border=True)
    left,right = generic_container.columns([2,1],vertical_alignment="bottom")
    with left:
        st.markdown(f"""##### {market_item["en"]["item_name"]}""")
        st.markdown(components.markdowns.prime_component_info_md(market_item,item["rarity"],item["chance"],price,offers),unsafe_allow_html=True)
    with right.container(border=True):
        url = f"{market_url}/{relic_name_cleaned}"
        st.markdown(components.markdowns.image_md(url,item["item"]["name"],image_url),unsafe_allow_html=True)
    right.link_button(AppLabels.MARKET.value,url=url,use_container_width=True,icon=AppIcons.EXTERNAL.value,type="primary",help=AppMessages.MARKET_TOOL_TIP.value)
    

def generic(item, image_url: str):
    """ Generic info card. """
    generic_container = st.container(border=True)
    left,right = generic_container.columns([2,1],vertical_alignment="top")
    with left:
        st.markdown(f"""##### {item["name"]}""")
        info_module(item)
    with right.container(border=True):
        wiki_url = item["wikiaUrl"] if 'wikiaUrl' in item else Warframe.get_wiki_url(item["name"].replace(" Intact", "").replace(" ","_"))
        if item["category"] == "Mods":
            image_url = item["wikiaThumbnail"].split(".png")[0] + ".png"
        st.markdown(components.markdowns.image_md(wiki_url,item["name"],image_url),unsafe_allow_html=True)
        st.write(" ")
    if "Relic" in item["type"]:
        if right.button(AppLabels.MARKET.value,use_container_width=True,icon=AppIcons.MARKET.value,type="primary"):
            dialogs.market_check(item)

def baro(item,baro_info, image_url: str):
    """ Generic info card. """
    generic_container = st.container(border=True)
    left,right = generic_container.columns([2,1],vertical_alignment="top")
    with left:
        st.markdown(f"""##### {item["name"]}""")
        if  item["category"] != "Mods" and "Relic" not in item["type"]:
            st.markdown(f"""
                    <i>{item["description"]}</i> <br/>
                    """,unsafe_allow_html=True)
        st.markdown(components.markdowns.baro_ware_md(item,baro_info),unsafe_allow_html=True)
        if "Relic"  in item["type"]:
            st.markdown(components.markdowns.relic_info_md(item),unsafe_allow_html=True)

    with right.container(border=True):
        wiki_url = item["wikiaUrl"] if 'wikiaUrl' in item else Warframe.get_wiki_url(item["name"].replace(" Intact", "").replace(" ","_"))
        if item["category"] == "Mods":
            image_url = item["wikiaThumbnail"].split(".png")[0] + ".png"
        st.markdown(components.markdowns.image_md(wiki_url,item["name"],image_url),unsafe_allow_html=True)
        st.write(" ")
    if "Relic" in item["type"]:
        if right.button(AppLabels.MARKET.value,use_container_width=True,icon=AppIcons.MARKET.value,type="primary"):
            dialogs.market_check(item)

def prep_image(enum):
    """ Image card of Baro/Varzia."""
    img_location = data_manage.get_image_url(enum.value["uniqueName"])
    img_bytes = api_services.get_image(img_location)
    if img_bytes is not None:
        image = Image.open(img_bytes)
        st.image(image,use_container_width=True)
    else:
        image = Image.open(enum.value["image"])
        st.image(image.resize((200, 200)),use_container_width=True)
    