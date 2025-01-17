import streamlit as st

from utils.data_tools import get_frame_abilities_with_image

def warframe_abilities(name):
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

