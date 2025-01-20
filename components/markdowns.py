import streamlit as st

from config import structures
from config.constants import Warframe
from utils.data_tools import get_frame_abilities_with_image, get_craftable_info, get_relic_info

def warframe_info_md(name):
    result = get_frame_abilities_with_image(name)
    abilities = result[0]["abilities"]
    return f"""
            <b>Passive</b>: <i>{result[0]["passiveDescription"]}</i> <br/>
            <div class="row" style="display: flex;">
            <div class="column">
            <img alt="ducat" src="{abilities[0]["imageName"]}" title="{abilities[0]["description"]}"/></div>
            <div class="column">
            <img alt="ducat" src="{abilities[1]["imageName"]}" title="{abilities[1]["description"]}"/></div>
            <div class="column">
            <img alt="ducat" src="{abilities[2]["imageName"]}" title="{abilities[2]["description"]}"/></div>
            <div class="column">
            <img alt="ducat" src="{abilities[3]["imageName"]}" title="{abilities[3]["description"]}"/></div>
            </div><br>"""

def weapon_info_md(name):
    result = get_craftable_info(name)
    weapon = result[0]
    md = f"""
            <b>Description</b>: <i>{weapon["description"]}</i> <br/>
            <div class="row" style="display: flex;">
            """
    for component in weapon["components"]:
        md = md + f"""
            <div class="column">
            <img alt="ducat" src="{component["imageName"]}" title="{component["name"]} x{component["itemCount"]}"/>
            </div>"""
    return md + """</div><br>"""

def relic_info_md(name):
    result = get_relic_info(name)
    md = f""" """
    for reward in result["rewards"]:
        md = md + f"""
            <img alt="ducat" style="width:50px;height:50px;" src="{reward["imageName"]}" title="{reward["rarity"]}: {reward["chance"]}%"/>
            {reward["item"]["name"]} <br/>"""
    return md + """<br>"""

def prime_component_info_md(item,rarity,chances):
    return f"""
    Rarity: <font color="#FF4B4B">{rarity}</font><br/>
    Base chances: <font color="#FF4B4B">{chances}</font> %<br />
    Ducats: <font color="#FF4B4B">{item["ducats"]}</font> <img alt="ducat" style="width:20px;height:20px;" src="{Warframe.DUCAT.value}"/> <br/>
    MR: <font color="#FF4B4B">{item["mastery_level"]}</font> <br />
    """