from config.constants import Warframe
from utils import tools
from utils import data_manage
from utils.data_manage import get_craftable_info,get_frame_abilities_with_image
def warframe_info_md(name):
    """ Warframe markdown custom web element. """
    result = get_frame_abilities_with_image(name)
    if result is not None:
        abilities = result[0]["abilities"]
        if 'passiveDescription' in result[0]:
            md = f"""<b>Passive</b>: <i>{result[0]["passiveDescription"]}</i> <br/>"""
        else:
            md = f""" """
        for ability in abilities:
            md = md + f"""
                <img alt="{ability["name"]}" style="width:30px;height:30px;" src="{ability["imageName"]}" title="{ability["name"]}"/>
                <b>{ability["name"]}</b> : <i>{ability["description"]}</i><br/>"""
        return md + """<br>"""
    else:
        return f"""
                Undefined Data.
                """

def craftable_info_md(name):
    """ Craftable markdown custom web element. """
    result = get_craftable_info(name)
    md = f""" """
    if result is not None:
        craftable = result[0]
        
        if 'masteryReq' in craftable:
            md = md + f"""
                    <b>MR</b>: <i>{craftable["masteryReq"]}</i> <br/>
                """
        
        if 'damage' in craftable:
            md = md + f"""<b>Stats</b>: <br/><p style="padding-left: 20px;">"""
            md = md + f"""<i>Status Chance: {craftable["procChance"]*100:.2f} %</i><br>"""
            md = md + f"""<i>Crit Chance: {craftable["criticalChance"]*100:.2f} %</i><br>"""
            md = md + f"""<i>Crit Multiplier: {craftable["criticalMultiplier"]:.2f}x</i><br>"""
            md = md + f"""<i>Firerate/Attack Speed: {craftable["fireRate"]:.2f}</i><br>"""
            md = md + "</p>"        

        sub_md = f""" """

        if 'components' in craftable:
            sub_md = sub_md + f"""<b>Components</b>:<span>"""
            for component in craftable["components"]:
                sub_md = sub_md + f"""
                    <img alt="{component["name"]}" style="width:30px;height:30px;" src="{component["imageName"]}" title="{component["name"]}"/>
                    <i>x {component["itemCount"]} {component["name"]},</i>"""
        
        return md,sub_md+"""</span>"""
    else:
        return f"""
                Undefined Data.
                """

def relic_info_md(item):
    """ Relic markdown custom web element. """
    md = f""" """
    for reward in item["rewards"]:
        md = md + f"""
            <img alt="{reward["item"]["name"]}" style="width:30px;height:30px;" src="{reward["item"]["imageName"]}" title="{reward["rarity"]}: {reward["chance"]}%"/>
            {reward["item"]["name"]} <br/>"""
    return md + """<br>"""

def prime_component_info_md(item,rarity,chances,price,offers,lowest_ingame):
    """ Prime component markdown custom web element. """
    return f"""
    <div> Average: 
    <font color="#FF4B4B">{price:,.2f}
        <img alt="{Warframe.PLATINUM.value["name"]}" style="width:20px;height:20px;" src="{Warframe.PLATINUM.value["image"]}"/> 
    </font> from <font color="#FF4B4B">{offers}</font> offer(s).<br>
    <div> Lowest: 
    <font color="#FF4B4B">{lowest_ingame:,}</font>
        <img alt="{Warframe.PLATINUM.value["name"]}" style="width:20px;height:20px;" src="{Warframe.PLATINUM.value["image"]}"/><br>
    Rarity: <font color="#FF4B4B">{rarity}</font> | <font color="#FF4B4B">{chances}</font> %<br/>
    Ducats: <font color="#FF4B4B">{item["ducats"]:,}</font>
        <img alt="{Warframe.DUCAT.value["name"]}" style="width:20px;height:20px;" src="{Warframe.DUCAT.value["image"]}"/> | MR: <font color="#FF4B4B">{item["mastery_level"]}</font>
    <br/><br/>
    """

def baro_ware_md(item,baro_info):
    """ Baro wares markdown custom web element. """
    if item is not None:
        return f"""
        Ducats: <font color="#FF4B4B">{baro_info["ducats"]:,}</font>
            <img alt="{Warframe.DUCAT.value["name"]}" style="width:20px;height:20px;" src="{Warframe.DUCAT.value["image"]}"/> |
        Credits: <font color="#FF4B4B">{baro_info["credits"]:,}</font>
            <img alt="{Warframe.CREDITS.value["name"]}" style="width:20px;height:20px;" src="{Warframe.CREDITS.value["image"]}"/>
        """
    else:
        return f"""
        Ducats: <font color="#FF4B4B">{baro_info["ducats"]:,}</font>
            <img alt="{Warframe.DUCAT.value["name"]}" style="width:20px;height:20px;" src="{Warframe.DUCAT.value["image"]}"/> |
        Credits: <font color="#FF4B4B">{baro_info["credits"]:,}</font>
            <img alt="{Warframe.CREDITS.value["name"]}" style="width:20px;height:20px;" src="{Warframe.CREDITS.value["image"]}"/>
        """

def image_md(url,alt,source, size="100%"):
    """Return image markdown custom web element. """
    return f"""<a href="{url}">
                <img alt="{alt}" 
                    style="display: block;
                            margin-left: auto;
                            margin-right: auto;
                            height: auto;
                            width: {size};"
                    src="{source}"/></a>"""

def hide_streamlit_header():
    """Hide the Streamlit header. """
    return """
            <style>
                /* Hide the Streamlit header and menu */
                header {visibility: hidden;}
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
    """ Relic markdown custom web element. """
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
    """ Relic markdown custom web element. """
    md = f""" """
    for item,amount in data.items():
        image = data_manage.get_reward_image(item)
        md = md + f"""
            {amount:,}
            <img alt="{item}" style="width:30px;height:30px;" src="{image}" title="{item}"/>
            <span>{item}</span><br/> """
    return md