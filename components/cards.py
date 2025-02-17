import streamlit as st
from PIL import Image
from components import custom
import components.markdowns
from config.constants import Warframe
from utils import api_services
from utils import data_manage

def info(item):
    """ The info module for a card. """
    hover_md = ""
    if 'type' in item and 'category' in item:
        if item["type"] == "Warframe" or item["type"] == "Archwing":
            type_data = data_manage.extract_frame_abilities(item)
            hover_md = components.markdowns.ability_info_md(item,type_data)
        elif ("Weapons" in item["uniqueName"] or "Sentinels" in item["category"]) and item["category"] != "Skins":
            type_data = data_manage.extract_craftable_components(item)
            hover_md =components.markdowns.craftable_info_md(type_data)
        elif ("Mods" in item["category"]):
            # type_data = market.get (item name url)
            pass
        elif "Relic" in item["type"]:
            type_data = data_manage.extract_relic_rewards(item)
            hover_md = components.markdowns.relic_rewards_info_md(type_data)
        else:
            hover_md = components.markdowns.misc_info_md(item)

    return hover_md

def generic(image_url: str,package=None,price_info=None):
    """ Generic info card. """
    item = package
    generic_container = st.container(border=False)
    with generic_container:
        if item is not None:
            if 'wikiaUrl' in item:
                wiki_url = item["wikiaUrl"]
            else:
                wiki_url = Warframe.get_wiki_url(item["name"].replace(" Intact", "").replace(" ","_"))
            if 'category' in item and item["category"] == "Mods":
                image_url = item["wikiaThumbnail"].split(".png")[0] + ".png"
        elif price_info is not None:
             wiki_url = Warframe.get_wiki_url(price_info["name"].replace("StoreItem", "").replace(" ","_"))
        
        hover_md = info(item)
                
        image_md = components.markdowns.image_md(wiki_url,item["name"],image_url,caption="visible")
        info_md = components.markdowns.hover_md(image_md,hover_md)
        ducat_md = components.markdowns.price_overlay_md(price_info) if price_info is not None else ""
        md = components.markdowns.card_md(info_md,ducat_md)

        return md + """</div>"""

            
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