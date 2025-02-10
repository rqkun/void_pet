import streamlit as st
from PIL import Image
from components import dialogs
import components.markdowns
from config.constants import AppIcons, AppLabels, Warframe
from utils import api_services
from utils import data_manage


def info_module(item, baro_info = None):
    """ Categorized item markdown. """
    
    left,right = st.columns([2,5],vertical_alignment="center")
    
    right.markdown(f"""##### {item["name"]}""")
    
    if baro_info is not None:
        st.markdown(components.markdowns.baro_ware_md(item,baro_info),unsafe_allow_html=True)
    
    if 'description' in item:
            st.markdown(f"""
                <i>{item["description"]}</i> <br/>
                """,unsafe_allow_html=True)
    pop_info = left.popover(AppIcons.INFO.value, use_container_width=True)
    if 'type' in item and 'category' in item:
        if item["type"] == "Warframe" or item["type"] == "Archwing":
            pop_info.container(border=True).markdown(components.markdowns.warframe_info_md(item["name"]),unsafe_allow_html=True)
        elif ("Weapons" in item["uniqueName"] or "Sentinels" in item["category"]) and item["category"] != "Skins":
            pop_info.container(border=True).markdown(components.markdowns.weapon_info_md(item["name"]),unsafe_allow_html=True)
        elif "Relic" in item["type"]:
            pop_info.container(border=True).markdown(components.markdowns.relic_info_md(item),unsafe_allow_html=True)
            if st.button(AppLabels.MARKET.value,use_container_width=True,icon=AppIcons.MARKET.value,type="primary"):
                dialogs.market_check(item)

# def component(item,market_item, image_url: str, lowest_online_plat: int, filtered_data: object):
#     """ Prime component info card. """
#     avg_plat = tools.get_average_plat_price(filtered_data)
#     relic_name_cleaned = item["item"]["name"].lower().replace(" ","_")
#     market_url = Warframe.MARKET.value["url"]
#     generic_container = st.container(border=True)
#     left,right = generic_container.columns([2,1],vertical_alignment="bottom")
#     with left:
#         st.subheader(f"""{market_item["en"]["item_name"]}""",divider="red")
#         st.markdown(components.markdowns.prime_component_info_md(market_item,item["rarity"],item["chance"],avg_plat,len(filtered_data),lowest_online_plat),unsafe_allow_html=True)
#     with right.container(border=True):
#         url = f"{market_url}/{relic_name_cleaned}"
#         st.image(data_manage.get_image_bytes(image_url))
#     right.link_button(AppLabels.MARKET.value,url=url,use_container_width=True,icon=AppIcons.EXTERNAL.value,type="primary",help=AppMessages.MARKET_TOOL_TIP.value)
    
def generic(item, image_url: str):
    """ Generic info card. """
    generic_container = st.container(border=True)
    left,right = generic_container.columns([2,1],vertical_alignment="top")
    with left:
        if item is not None:
            info_module(item) 
        
    with right.container(border=True):
        if 'wikiaUrl' in item:
            wiki_url = item["wikiaUrl"]
        else:
            wiki_url = Warframe.get_wiki_url(item["name"].replace(" Intact", "").replace(" ","_"))
        if 'category' in item and item["category"] == "Mods":
            image_url = item["wikiaThumbnail"].split(".png")[0] + ".png"
        st.markdown(components.markdowns.image_md(wiki_url,item["name"],image_url),unsafe_allow_html=True)
        st.write(" ")

def baro(item,baro_info, image_url: str):
    """ Generic info card. """
    generic_container = st.container(border=True)
    
    left,right = generic_container.columns([2,1],vertical_alignment="top")
    
    with left:
        if item is not None:
            info_module(item,baro_info) 

    with right.container(border=True):
        if item is not None:
            if 'wikiaUrl' in item:
                wiki_url = item["wikiaUrl"]
            else:
                wiki_url = Warframe.get_wiki_url(item["name"].replace(" Intact", "").replace(" ","_"))
            if 'category' in item and item["category"] == "Mods":
                image_url = item["wikiaThumbnail"].split(".png")[0] + ".png"
        else:
            wiki_url = Warframe.get_wiki_url(baro_info["name"].replace("StoreItem", "").replace(" ","_"))
        st.markdown(components.markdowns.image_md(wiki_url,baro_info["name"],image_url),unsafe_allow_html=True)
        st.write(" ")
def prep_image(enum):
    """ Image card of Baro/Varzia."""
    img_location = data_manage.get_image_url(enum.value["uniqueName"])
    img_bytes = api_services.get_image(img_location)
    if img_bytes is not None:
        image = Image.open(img_bytes)
        st.image(img_bytes,use_container_width=True)
    else:
        image = Image.open(enum.value["image"])
        st.image(image.resize((200, 200)),use_container_width=True)
    