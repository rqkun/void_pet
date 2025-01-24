from config.constants import Warframe
from utils.data_manage import get_craftable_info,get_frame_abilities_with_image
def warframe_info_md(name):
    """ Warframe markdown custom web element. """
    result = get_frame_abilities_with_image(name)
    abilities = result[0]["abilities"]
    return f"""
            <b>Passive</b>: <i>{result[0]["passiveDescription"]}</i> <br/>
            <div class="row" style="display: flex;">
            <div class="column">
            <img alt="{abilities[0]["name"]}" src="{abilities[0]["imageName"]}" title="{abilities[0]["description"]}"/></div>
            <div class="column">
            <img alt="{abilities[1]["name"]}" src="{abilities[1]["imageName"]}" title="{abilities[1]["description"]}"/></div>
            <div class="column">
            <img alt="{abilities[2]["name"]}" src="{abilities[2]["imageName"]}" title="{abilities[2]["description"]}"/></div>
            <div class="column">
            <img alt="{abilities[3]["name"]}" src="{abilities[3]["imageName"]}" title="{abilities[3]["description"]}"/></div>
            </div><br>"""

def weapon_info_md(name):
    """ Weapon markdown custom web element. """
    result = get_craftable_info(name)
    weapon = result[0]
    md = f"""
            <b>Description</b>: <i>{weapon["description"]}</i> <br/>
            <div class="row" style="display: flex;">
            """
    for component in weapon["components"]:
        md = md + f"""
            <div class="column">
            <img alt="{component["name"]}" src="{component["imageName"]}" title="{component["name"]} x{component["itemCount"]}"/>
            </div>"""
    return md + """</div><br>"""

def relic_info_md(item):
    """ Relic markdown custom web element. """
    md = f""" """
    for reward in item["rewards"]:
        md = md + f"""
            <img alt="{reward["item"]["name"]}" style="width:30px;height:30px;" src="{reward["item"]["imageName"]}" title="{reward["rarity"]}: {reward["chance"]}%"/>
            {reward["item"]["name"]} <br/>"""
    return md + """<br>"""

def prime_component_info_md(item,rarity,chances,price,offers):
    """ Prime component markdown custom web element. """
    return f"""
    <div> Average: 
    <font color="#FF4B4B">{price:.2f}
        <img alt="{Warframe.PLATINUM.value["name"]}" style="width:20px;height:20px;" src="{Warframe.PLATINUM.value["image"]}"/> 
    </font> from <font color="#FF4B4B">{offers}</font> offer(s).<br>
    Rarity: <font color="#FF4B4B">{rarity}</font><br/>
    Base chances: <font color="#FF4B4B">{chances}</font> %<br/>
    Ducats: <font color="#FF4B4B">{item["ducats"]}</font>
        <img alt="{Warframe.DUCAT.value["name"]}" style="width:20px;height:20px;" src="{Warframe.DUCAT.value["image"]}"/> <br/>
    MR: <font color="#FF4B4B">{item["mastery_level"]}</font>
    <br/><br/>
    """

def baro_ware_md(item,baro_info):
    """ Baro wares markdown custom web element. """
    return f"""
    Ducats: <font color="#FF4B4B">{baro_info["ducats"]}</font>
        <img alt="{Warframe.DUCAT.value["name"]}" style="width:20px;height:20px;" src="{Warframe.DUCAT.value["image"]}"/> |
    Credits: <font color="#FF4B4B">{baro_info["credits"]}</font>
        <img alt="{Warframe.CREDITS.value["name"]}" style="width:20px;height:20px;" src="{Warframe.CREDITS.value["image"]}"/> |
    Type: <font color="#FF4B4B">{item["type"].replace(" Mod", "")}</font>
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