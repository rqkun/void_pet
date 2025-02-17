from datetime import datetime
from config.constants import Warframe
from utils import tools
from utils import data_manage
from typing import Literal

def ability_info_md(item,abilities):
    """ Abilities markdown custom web element. """
    md = f"""<span class="item-image-drop-down-content"> <b>{item["name"]} &middot; {item["type"]} </b><br>"""
    if 'passiveDescription' in abilities:
        md = md + f"""<b>Passive</b>: <i>{abilities["passiveDescription"]}</i><br/>"""
    for ability in abilities["abilities"]:
        md = md + f"""
            <img alt="{ability["name"]}" style="width:30px;height:30px;" src="{ability["imageName"]}" title="{ability["name"]}"/>
            <b>{ability["name"]}</b> : <i>{ability["description"]}</i><br/>"""
    return md + """</span>"""


def craftable_info_md(item):
    """ Craftable markdown custom web element. """
    md = f"""<span class="item-image-drop-down-content"> <b>{item["name"]} &middot; {item["type"]} &middot; MR: {item["masteryReq"] if 'masteryReq' in item else 0}</b><br>"""

    if 'damage' in item:
        md = md + f"""<i>Status Chance: {item["procChance"]*100:.2f} % &middot; Firerate/Attack Speed: {item["fireRate"]:.2f}</i> <br>"""
        md = md + f"""<i>Crit Chance: {item["criticalChance"]*100:.2f} % &middot; Crit Multiplier: {item["criticalMultiplier"]:.2f}x</i> <br>"""
        
    if 'components' in item:
        md = md + f"""<b>Components</b>:<br>"""
        for component in item["components"]:
            md = md + f"""
                <img alt="{component["name"]}" style="width:30px;height:30px;" src="{component["imageName"]}" title="{component["name"]}"/>
                <i>x {component["itemCount"]} {component["name"]} <br></i>"""
    return md + """</span>"""


def relic_rewards_info_md(item):
    """ Relic rewards markdown custom web element. """
    md = f"""<span class="item-image-drop-down-content"> <b>{item["name"]} &middot; {item["type"]}<br>"""
    for reward in item["rewards"]:
        md = md + f"""
            <img alt="{reward["item"]["name"]}" style="width:30px;height:30px;" src="{reward["item"]["imageName"]}" title="{reward["rarity"]}: {reward["chance"]}%"/>
            {reward["item"]["name"]} <br/>"""
    return md + """</span>"""


def misc_info_md(item):
    """ Misc information markdown custom web element. """
    md = f"""<span class="item-image-drop-down-content"> <b>{item["name"]} &middot; {item["type"]}</b><br>"""

    if 'damage' in item:
        md = md + f"""<i>Status Chance: {item["procChance"]*100:.2f} % &middot; Firerate/Attack Speed: {item["fireRate"]:.2f}</i> <br>"""
        md = md + f"""<i>Crit Chance: {item["criticalChance"]*100:.2f} % &middot; Crit Multiplier: {item["criticalMultiplier"]:.2f}x</i> <br>"""
        
    if 'description' in item:
        md = md + f"""<i>{item["description"]}</i>"""
    return md + """</span>"""


def hover_md(image_md, info_md):
    """Return hover dialog markdown custom web element. """
    md = f""" <div class="item-image-drop-down">"""
    md = md + image_md
    md = md + info_md
    md = md + """</div>"""
    return md

def price_overlay_md(price_info):
    """ Prices markdown custom web element. """
    return f"""
        <p style="position: absolute;
            bottom: 10px;
            left: calc(60px + 0.5vw);
            align-self: flex-end;
            display: flex;
            z-index: 10;
            background-color: rgba(0, 0, 0, 0.5);
            padding-left: 10px;
            padding-right: 10px;
            padding-top: 3px;
            padding-bottom: 3px;
            border-radius: 10px;
            background-opacity: 10%;
            font-size: calc(12px + 0.5vw);
            flex-direction: row;
            align-items: center;
            flex-wrap: nowrap;
            ">{price_info["amount"]}<img alt="{price_info["type"]["name"]}" style="width:calc(20px + 0.5vw);height:auto;" src="{price_info["type"]["image"]}"/></p>
        """
def image_md(url,alt,source,caption:Literal["hidden", "collapse", "visible"],animation=True, size="65%"):
    """Return image markdown custom web element. """
    if animation:
        img_class = "item-image"
    else:
        img_class = "fake"
    md = f"""<a href="{url}" target="_blank" style="" class="tooltip-wrap">
                <img alt="{alt}" class ="{img_class}" 
                    style="
                            position: relative;
                            display: block;
                            align-items: center;
                            margin-left: auto;
                            margin-right: auto;
                            height: auto;
                            width: {size};
                            border-radius: 10px;
                            zoom: 150%;"
                    src="{source}" title="{alt}"/></a>"""
    if caption == "hidden" or caption == "visible":
        md = md + f"""<p style="text-overflow: ellipsis;
                                text-align: center;
                                padding-top: 10px;
                                font-size: 75%;
                                white-space: nowrap;
                                overflow: hidden;
                                visibility: {caption};">{alt}</p>"""
    return md

def card_md(image_md,price_md):
    """Return card markdown custom web element. """
    md = f""" <div class="item-flex-content" style="display:flex;justify-content: space-between;flex-direction: column; ">"""
    md = md + image_md
    md = md + price_md 
    md = md + """</div>"""
    return md

def hide_streamlit_header():
    """Hide the Streamlit header. """
    return """
            <style>
                /* Hide the Streamlit header and menu */
                header {visibility: hidden;}
                div.block-container {padding-top:1rem;}
                
            </style>
        """


def mod_info_md(item):
    """ Mods markdown custom web element. """
    md = f""" """
    
    if 'polarity' in item:
        md = md + f"""
                <b> Polarity: </b><i>{item["polarity"]}</i><br>
                """
                
    if 'compatName' in item:
        md = md + f"""
                <b> Slot: </b> <i>{item["compatName"]}</i><br>
                """

    if 'levelStats' in item:
        
        for idx, level in enumerate(item["levelStats"]):
            md = md + f"""
                <b> Level {idx}:</b>
                """
            for stat in level["stats"]:  
                md = md + f"""<i>{ tools.remove_wf_color_codes(stat)} </i><br>"""
    
    sub_md = f""" """
    if 'drops' in item:
        sub_md = sub_md + """<b>Drop Locations:</b><br><div style="padding-left: 20px;">"""
        for drop in item["drops"]:
            sub_md = sub_md + f"""Rates: <font color="#FF4B4B"><i>{drop["chance"]}</i></font> - {drop["location"]}<br> """
        sub_md = sub_md + """</div>"""
    else: 
        sub_md = sub_md + """<b>Drop Locations:</b> <br><div style="padding-left: 20px;"><i>None</i></div>"""
    return md,sub_md

def alerts_reward_info_md(data):
    """ Alert rewards markdown custom web element. """
    md = f""" """
    for reward in data:
        if reward["item"] != "Credits":
            reward["image"] = data_manage.get_reward_image(reward["image"])
        md = md + f"""
            {reward["amount"]:,}
            <img alt="{reward["item"]}" style="width:30px;height:30px;" src="{reward["image"]}" title="{reward["item"]}"/>
            <span>{reward["item"]}</span><br/> """
    return md

def invasions_reward_info_md(data):
    """ Invasion rewards markdown custom web element. """
    md = f""" """
    for item,amount in data.items():
        image = data_manage.get_reward_image(item)
        md = md + f"""
            {amount:,}
            <img alt="{item}" style="width:30px;height:30px;" src="{image}" title="{item}"/>
            <span>{item}</span><br/> """
    return md

def market_order_md(data):
    """ Market order custom web element. """
    img = "https://warframe.market/static/assets/user/default-avatar.png"
    if data["user"]["avatar"] is not None:
        img = Warframe.MARKET.value["static"]+data["user"]["avatar"]
    md =f"""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"><div class="row"> """
    md = md+ f"""
    <div class="listing-container">
        <div class="listing-content">
            <div class="tag-section">
                <span class="wts-tag">wts</span>
            </div>
            <div class="profile-section">
                <a class="profile-link" style="text-decoration: none;" href="{Warframe.MARKET.value["base"]}profile/{data["user"]["ingame_name"]}">
                    <img class="profile-image" style="text-decoration: none;" alt="{data["user"]["ingame_name"]}" src="{img}">
                    <span class="profile-name" style="text-decoration: none;" >{data["user"]["ingame_name"]}</span>
                </a>
            </div>
            <div class="reputation-section">
                <span class="reputation-score">{data["user"]["reputation"]} <i class="fa fa-heart-o"></i></span>
            </div>
            <div class="reputation-section">
                <span class="reputation-score">{data["quantity"]} <i class="fa fa-inbox"></i></span>
            </div>
            <div class="price-section">
                <span class="price-amount">{data["platinum"]} <img alt="{Warframe.PLATINUM.value["name"]}" style="width:20px;height:20px;" src="{Warframe.PLATINUM.value["image"]}"/></span>
            </div>
        </div>
    </div>
    <br>
    """
    return md

def market_item_desc(data):
    md = f"""<span> <b>{data["en"]["item_name"]} &middot;</b> {data["trading_tax"]:,} <img alt="{Warframe.CREDITS.value["name"]}" style="width:20px;height:20px;" src="{Warframe.CREDITS.value["image"]}"/><br>"""
    
    md = md + f"""
        <i>{data["en"]["description"]}</i>"""
    return md + """</span><br>"""

def world_clock_md(data):
    md = f"""<div> """
    # &middot; <i>{tools.format_timedelta(datetime.strptime(item["data"]["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today(),day=False)}</i>
    for item in data:
        md = md + f"""<div style="display:flex;flex-direction:row;gap:5px;justify-content:space-between;align-items:center;"><img alt="{item["name"]}" style="width:50px;height:50px;border-radius:10px;padding:5px;" src="{item["image"]}"/><b>{item["name"]} &middot; </b> {item["data"]["state"].upper()}<br></div>"""
    return md + """<br> </div>"""