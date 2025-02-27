import base64
from datetime import datetime

from millify import millify
from config.constants import Warframe
from utils import tools
from utils import data_manage
from typing import Literal

def ability_info_md(item,abilities):
    """Abilities markdown custom web element. """
    md = f"""<span class="item-image-drop-down-content"> <b>{item["name"]} &middot; {item["type"]} </b><br>"""
    if 'passiveDescription' in abilities:
        md = md + f"""<b>Passive</b>: <i>{abilities["passiveDescription"]}</i><br/>"""
    for ability in abilities["abilities"]:
        md = md + f"""
            <img alt="{ability["name"]}" style="width:30px;height:30px;" src="{ability["imageName"]}" title="{ability["name"]}"/>
            <b>{ability["name"]}</b> : <i>{ability["description"]}</i><br/>"""
    return md + """</span>"""


def craftable_info_md(item):
    """Craftable markdown custom web element. """
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
    """Relic rewards markdown custom web element. """
    md = f"""<span class="item-image-drop-down-content"> <b>{item["name"]} &middot; {item["type"]}<br>"""
    for reward in item["rewards"]:
        md = md + f"""
            <img alt="{reward["item"]["name"]}" style="width:30px;height:30px;" src="{reward["item"]["imageName"]}" title="{reward["rarity"]}: {reward["chance"]}%"/>
            {reward["item"]["name"]} <br/>"""
    return md + """</span>"""


def misc_info_md(item):
    """Misc information markdown custom web element. """
    md = f"""<span class="item-image-drop-down-content"> <b>{item["name"]} &middot; {item["type"]}</b><br>"""

    if 'damage' in item:
        md = md + f"""<i>Status Chance: {item["procChance"]*100:.2f} % &middot; Firerate/Attack Speed: {item["fireRate"]:.2f}</i> <br>"""
        md = md + f"""<i>Crit Chance: {item["criticalChance"]*100:.2f} % &middot; Crit Multiplier: {item["criticalMultiplier"]:.2f}x</i> <br>"""
        
    if 'description' in item:
        md = md + f"""<i>{item["description"]}</i>"""
    return md + """</span>"""


def hover_md(image_md, info_md):
    """Return hover dialog markdown custom web element. """
    md = f"""<div class="item-image-drop-down">"""
    md = md + image_md
    md = md + info_md
    md = md + """</div>"""
    return md


def price_overlay_md(price_info):
    """Prices markdown custom web element. """
    return f"""
        <div class="price-tag" >{price_info["amount"]}<img class="price-img" alt="{price_info["type"]["name"]}" src="{price_info["type"]["image"]}"/></div>
        """


def image_md(url,alt,source,caption:Literal["hidden", "collapse", "visible"],animation=True, size="65%",border=1):
    """Return image markdown custom web element. """
    if animation:
        img_class = "item-image"
    else:
        img_class = "item-image-fake"
    md = f"""<a href="{url}" target="_blank" class="tooltip-wrap">
                <img alt="{alt}" class ="{img_class}" style="border-radius: {border}rem;" src="{source}" title="{alt}"/></a>"""
    if caption == "hidden" or caption == "visible":
        md = md + f"""<p class="image-caption" style="visibility: {caption};">{alt}</p>"""
    return md


def card_md(image_md,price_md):
    """Return card markdown custom web element. """
    md = f"""<div class="item-flex-content">"""
    md = md + image_md
    md = md + price_md 
    md = md + """</div>"""
    return md


def mod_info_md(item):
    """Mods markdown custom web element. """
    md = f""""""
    
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
    
    sub_md = f""""""
    if 'drops' in item:
        sub_md = sub_md + """<b>Drop Locations:</b><br><div style="padding-left: 20px;">"""
        for drop in item["drops"]:
            sub_md = sub_md + f"""Rates: <font color="#FF4B4B"><i>{drop["chance"]}</i></font> - {drop["location"]}<br> """
        sub_md = sub_md + """</div>"""
    else: 
        sub_md = sub_md + """<b>Drop Locations:</b> <br><div style="padding-left: 20px;"><i>None</i></div>"""
    return md,sub_md


def alerts_reward_info_md(data):
    """Alert rewards markdown custom web element. """
    md = f"""<div><span><b>Reward:<b/> <i style="color:#a3a3a3;"> Reminder, Steelpath rewards might be different.</i></span><br>"""
    for reward in data:
        if reward["item"] != "Credits":
            reward["image"] = data_manage.get_reward_image(reward["image"])
        md = md + f"""
            <img alt="{reward["item"]}" style="width:30px;height:30px;" src="{reward["image"]}" title="{reward["item"]}"/>
            <span>{reward["amount"]:,} {reward["item"]}</span><br/> """
    return md +"</div>"


def invasions_reward_info_md(data):
    """Invasion rewards markdown custom web element. """
    md = f""""""
    for item,amount in data.items():
        image = data_manage.get_reward_image(item)
        md = md + f"""
            <img alt="{item}" style="width:30px;height:30px;" src="{image}" title="{item}"/>
            <span>{amount:,} {item}</span><br/> """
    return md


def market_order_md(data,item):
    """Market order custom web element. """
    img = "https://warframe.market/static/assets/user/default-avatar.png"

    if "mod_rank" in data:
        if "mod_max_rank" in item:
            rank = f"""of {item["mod_max_rank"]}"""
        mod_rank = f"""<span class="rank-amount flex-font">  Rank {data["mod_rank"]} {rank}</span>"""
    else: mod_rank = ""
    if data["user"]["avatar"] is not None:
        img = Warframe.MARKET_API.value["static"]+data["user"]["avatar"]
    md =f"""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"><div class="row"> """
    md = md+ f"""
    <div class="listing-container">
        <div class="listing-content">
            <div class="tag-section">
                <span class="status-tag {data["user"]["status"]}-tag">{data["user"]["status"].title()}</span>
            </div>
            <div class="profile-section">
                <a class="profile-link" style="text-decoration: none;" href="{Warframe.MARKET_API.value["base"]}profile/{data["user"]["ingame_name"]}">
                    <img class="profile-image" alt="{data["user"]["ingame_name"]}" src="{img}">
                    <span class="profile-name flex-font"><b>{data["user"]["ingame_name"]}</b></span>
                </a>
            </div>
            <div class="rank-section">{mod_rank}</div>
            <div class="reputation-section">
                <span class="reputation-score flex-font">{data["user"]["reputation"]} <i class="fa fa-smile-o"></i></span>
            </div>
            <div class="quantity-section">
                <span class="quantity-amount flex-font">{data["quantity"]} <i class="fa fa-cubes"></i></span>
            </div>
            <div class="price-section">
                <span class="price-amount flex-font">{data["platinum"]} <img alt="{Warframe.PLATINUM.value["name"]}" style="width:20px;height:20px;" src="{Warframe.PLATINUM.value["image"]}"/></span>
            </div>
        </div>
    </div>
    <br>
    """
    return md


def market_item_desc(data):
    """Market item description custom web element."""
    md = f"""<span> <b>{data["en"]["item_name"]} &middot;</b> {data["trading_tax"]:,} <img alt="{Warframe.CREDITS.value["name"]}" style="width:20px;height:20px;" src="{Warframe.CREDITS.value["image"]}"/><br>"""
    
    md = md + f"""
        <i>{data["en"]["description"]}</i>"""
    return md + """</span><br>"""


def world_clock_md(data):
    """Open world clocks custom web element."""
    md = f"""<div class ="world-clock-container"> """
    for item in data:
        span = datetime.strptime(item["data"]["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
        if span.total_seconds() >0:
            time = tools.format_timedelta(span,day=False)
        else: time = tools.format_timedelta(datetime.today()-datetime.today(),day=False)
        md = md + f"""<div class= "world-clock-content">
                            <img class = "world-clock-img" alt="{item["name"]}" src="{item["image"]}"/>
                            <div class = "world-clock-txt">
                                <span><b>{item["name"]}:</b></span>
                                <span>{item["data"]["state"].title()} &middot; <i style="color: gray;">{time}</i></span>
                            </div>
                       </div>
                    """
    return md + """<br></div>"""


def render_svg(svg,size):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = f"""<img style="filter:invert(100%);" width={size} height={size} """
    part2 = r'src="data:image/svg+xml;base64,%s"/>' % b64
    html = html + part2
    return html


def riven_auction_md(data,image):
    """Market riven auctions custom web element. """
    if "_and_" in data["item"]["weapon_url_name"]:
        data["item"]["weapon_url_name"] = data["item"]["weapon_url_name"].replace("_and_", "_&_")
    plat_icon = f"""<img alt="{Warframe.PLATINUM.value["name"]}" style="width:20px;height:20px;" src="{Warframe.PLATINUM.value["image"]}"/>"""
    name = data["item"]["weapon_url_name"].replace("_"," ").title()
    attribute = ""
    polarity = render_svg(open(f"""components/svgs/{data["item"]["polarity"]}.svg""").read(),20)
    if data["owner"]["status"] == "offline":
        status = """style="color: #e44a36;" """
    elif data["owner"]["status"] == "online":
        status = """style="color: #62e579;" """
    else:
        status = """style="color: #b387d9;" """
        
    data["item"]["attributes"] = sorted(data["item"]["attributes"],key=lambda x: (x['positive'] == False, len(x['url_name'])))
        
    for item in data["item"]["attributes"]:
        if item["positive"]:
            sign = "+"
            class_c = "pos"
        else: 
            sign = "-"
            class_c = "neg"
        if "Damage Vs" in item["url_name"].replace("_"," ").title():
            value = f"""{abs(item["value"]) }x"""
        else:
            value = f"""{sign}{abs(item["value"]) }%"""
        
        attribute = attribute + f"""<div class="stat-{class_c} flex-font stat-card">{value} {item["url_name"].replace("_"," ").title()}</div>"""
    avatar_img = "https://warframe.market/static/assets/user/default-avatar.png"
    
    if not data["is_direct_sell"]:
        direct_auction = "Auction"
    else: direct_auction = "Buyout"
    price = ""
    if data["buyout_price"] is not None:
        price = price + f"""<div class="price flex-font"> Buyout Price: <span class="price-amount-text">{data["buyout_price"]} {plat_icon}</span></div>"""
    if data["is_direct_sell"] == False:
        price = price + f"""<div class="price flex-font"> Starting Price:<span class="price-amount-text">{data["starting_price"]} {plat_icon}</span></div>"""
    if data["top_bid"] is not None: 
        price = price + f"""<div class="price flex-font"> Top Bid:<span class="price-amount-text">{data["top_bid"]} {plat_icon}</span></div>"""
    
    if data["owner"]["avatar"] is not None:
        avatar_img = Warframe.MARKET_API.value["static"]+data["owner"]["avatar"]

    md = f"""
        <div class="card" >
            <img class="aunction-item-img" src="{image}" alt="{name}">
            <a class="title" href="{Warframe.MARKET_API.value["base"]}auction/{data["id"]}">{name} {data["item"]["name"].replace("-"," ").title().replace(" ","-")}</a>
            <hr class="solid" style="margin-top:5px;margin-bottom:5px;">
            <div class="price-details">
                <div class="stat-details">
                    <div class="stats">{attribute}</div>
                    <div class="details flex-font">
                        MR:<span class="price-amount-text">{data["item"]["mastery_level"]}</span> &nbsp; 
                        Ranks:<span class="price-amount-text">{data["item"]["mod_rank"]}</span> &nbsp; 
                        Re-rolls:<span class="price-amount-text">{data["item"]["re_rolls"]}</span> &nbsp; 
                        Polarity: {polarity} {data["item"]["polarity"].title()}
                    </div>
                </div>
                <div class="price-container">{price}</div>
            </div>
            <hr class="solid" style="margin-top:10px;margin-bottom:10px;">
            <div class="seller">
                <div class="tag-section">
                    <span class="auction-tag">{direct_auction}</span>
                </div>
                <img src="{avatar_img}" alt="{data["owner"]["ingame_name"]}">
                <span class="seller-name flex-font">{data["owner"]["ingame_name"]}</span>
                <span class="status flex-font" {status}>{data["owner"]["status"].title()} <b>&middot; {data["owner"]["region"].upper()}</b></span>
            </div>
        </div>
    """

    return md


def event_alert_card_md(name, time,info_md):
    """Events and Alerts container custom web element."""
    md = f"""<div class="event-alert-card">
                <div class="event-alert-name-time-container">
                    <h4>{name} &middot;</h4>
                    <span><i style="color:#a3a3a3;">&nbsp; {time}</i></span>
                </div>
                <div class="event-alert-info">{info_md}</div></div>"""
    return md


def event_info_md(data,step_rewards):
    """Event info custom element. """
    jobs = """<div class="event-info-popup">"""
    if data["jobs"] is not None and len(data["jobs"]) > 0:
        for item in data["jobs"]:
            jobs = jobs + f"""<div class="event-bounty-info">"""
            rewards = ", ".join(item["rewardPool"])
            jobs = jobs + f"""<details><summary>{item["type"]} &middot; Enemies: {item["enemyLevels"][0]} - {item["enemyLevels"][1]}</summary><b>Rewards: </b><font style="color:#a3a3a3;">{rewards}</font></details></div>"""
    jobs = jobs + "</div>"
    if step_rewards is not None and len(step_rewards)>0:
        step_rewards_md = f"""<details><summary><b>Rewards</b></summary><font style="color:#a3a3a3;">{"<br>".join(step_rewards)}</font></details>"""
    else:
        step_rewards_md =""
    md = f"""<div>
                <div style="display:flex;"><i style="color:#a3a3a3;max-width:300px;">{data["tooltip"]}</i></div>{jobs}{step_rewards_md}
        </div>
    """
    return md
