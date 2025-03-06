import asyncio
from collections import defaultdict
from enum import Enum
import json
import logging
import lzma
import re
from PIL import Image
import requests
import streamlit as st
from config.classes.parameters import RivenSearchParams, WarframeStatusSearchParams
from config.constants import AppExports, AppIcons, AppMessages, Warframe
from datasources import warframe_export,warframe_market,warframe_status
from utils import api_services, data_manage, tools
import utils.api_services as api_services
from utils.tools import parse_item_string

def get_image_url(unique_name,is_full =True) -> str:
    """Return image url from export.

    Args:
        unique_name (str): the identifier of an item.

    Returns:
        str: Item image url.
    """
    if 'image_manifest' not in st.session_state:
        st.session_state.image_manifest = query_exports(AppExports.MANIFEST.value)
    if is_full:
        identifier = unique_name.split("/")
        identifier = "/".join(identifier[len(identifier)-3:])
    else:
        identifier = unique_name
    for item in st.session_state.image_manifest:
        if identifier in item["uniqueName"]:
            return Warframe.PUBLIC_EXPORT_API.value["api"] + item["textureLocation"]

    return AppIcons.NO_IMAGE_DATA_URL.value


def export_relic(name,field):
    """Return the relic from the public export file.

    Args:
        name (str): uniqueName or name of the item.
        field (string): uniqueName / name

    Returns:
        dict: The json of found relic item.
    """
    local_relic_data = query_exports(AppExports.RELIC_ARCANE.value)
    for item in local_relic_data:
        if name in item[field]:
            return item
    return None


def extract_relic_rewards(relic):
    """
    Extract and update relic reward information.

    Args:
        relic (dict): Relic data containing rewards and unique identifier.

    Returns:
        dict or None: Updated relic with extracted reward details, or None if export fails.
    """
    relic_export = export_relic(relic["uniqueName"], "uniqueName")
    if not relic_export:
        return None
    
    rewards = relic.get("rewards", [])
    for i, item in enumerate(rewards):
        reward_data = relic_export["relicRewards"][i]
        item["item"].update({
            "uniqueName": reward_data["rewardName"],
            "imageName": get_image_url(reward_data["rewardName"])
        })
        
    return relic


def get_variza():
    """Call the warframe status api for varzia data.

    Returns:
        dict: Json data of the api response.
    """
    return warframe_status.world("vaultTrader")


def get_baro():
    """Call the warframe status api for baro data.

    Returns:
        dict: Json data of the api response.
    """
    return warframe_status.world("voidTrader")

@st.cache_data(ttl="1m",show_spinner=False)
def get_world_state():
    """Call the warframe status api for world state data.

    Returns:
        dict: Json data of the api response.
    """
    return warframe_status.world()


def get_prime_list() -> list:
    """Call the warframe status api for list of primes.

    Returns:
        list: A clean prime names list.
    """
    p_frame = warframe_status.items(WarframeStatusSearchParams("prime","name",type="warframes",only=["name","category"]))
    p_weapon = warframe_status.items(WarframeStatusSearchParams("prime","name",type="weapons",only=["name","category"]))
    
    return tools.clean_prime_names(p_frame, p_weapon)


def get_invasion()->dict:
    return warframe_status.world("invasions")


def get_invasions_rewards(data) -> dict:
    """Get Invasion's rewards info

    Args:
        data (dict): World state data of Invasions


    Returns:
        dict: Dictionary of rewards
    """
    result = defaultdict(int)
    for invasion in data:
        if invasion["attacker"]["faction"] != "Infested":
            name, count = parse_item_string(invasion["attacker"]["reward"]["asString"])
            result[name] += count

        
        name, count = parse_item_string(invasion["defender"]["reward"]["asString"])
        result[name] += count

    return dict(result)


def get_market_item(url_path):
    """Get warframe.market API data for item.

    Args:
        url_path (str): Item path.

    Returns:
        dict: Json of the Item found.
    """
    piece_list = warframe_market.items(url_path,False)
    if len(piece_list["payload"]["item"]["items_in_set"]) >1:
        for item in piece_list["payload"]["item"]["items_in_set"]:
            if item['en']['item_name'].lower().replace("(Key)","").replace(" ","_").replace("-","_") == url_path:
                return item
    return piece_list["payload"]["item"]["items_in_set"][0]


def extract_craftable_components(json_data):
    """Getting components of a craftable items.

    Args:
        json_data (dict): main item data.

    Returns:
        dict: item data with components data attach to it.
    """
    if 'components' in json_data:
        for component in json_data["components"]:
            component["imageName"] = get_image_url(component["uniqueName"])
    return json_data


def extract_frame_abilities(json_data):
    """Get warframe abilities with the ability images.

    Args:
        json_data (dict): frame's data.

    Returns:
        dict: abilities data.
    """
    for ability in json_data["abilities"]:
        ability["imageName"] = get_image_url(ability["uniqueName"])
    return {
        "passive": json_data["passiveDescription"] if "passiveDescription" in json_data else "",
        "abilities": json_data["abilities"]
        }


def call_market(option):
    """Call warframe.market API for market inspection.

    Args:
        option (str): Market's item path.

    Returns:
        dict: Item's market data.
    """
    result = warframe_market.items(url_path=option,order=True)['payload']['orders']
    sorted_orders = sorted(result, key=lambda x: x["platinum"])
    return sorted_orders


def get_reward_image(name) -> str:
    """ Get the material image from export API.

    Args:
        name (str): Either name or uniqueName of item

    Returns:
        bytes: ImageBytes
    """
    unique_name = name
    resoureces_json = query_exports(AppExports.RESOURCES.value)
    recipes_json = query_exports(AppExports.RECIPES.value)
    
    for item in recipes_json:
        if (name.replace(" ","") in item["uniqueName"]):
            unique_name = item["uniqueName"]
            break
    
    for item in resoureces_json:
        if (name in item["name"]):
            unique_name = item["uniqueName"]
            break
    if unique_name:
        img = get_image_url(unique_name)
    else:
        img = get_image_url(unique_name,False)
    
    if img == AppIcons.NO_IMAGE_DATA_URL.value:
        unique_name = warframe_status.items(WarframeStatusSearchParams(name.replace(" Blueprint", ""),by="name",type="items",only=["uniqueName"]))
        if len(unique_name)>0:
            img = get_image_url(unique_name[0]["uniqueName"])
        
    return img


def clean_event_data(data):
    """Cleaning missing data from event API.

    Args:
        data (dict): json data of the event.

    Returns:
        dict: the cleaned data.
    """
    if 'currentScore' in data:
        pass
    else: 
        data['currentScore'] = 0
    
    if 'description' in data:
        pass
    else: 
        data['description'] = "No Description"
    
    if 'node' in data:
        pass
    else: 
        data['node'] = "No Data"
    return data


def get_ongoing_events():
    """Call warframe status api for event data.

    Returns:
        dict: events data | None
    """
    response = warframe_status.world("events")
    events = []
    if len(response)>0:
        for event in response:
            events.append(clean_event_data(event))
            
        sorted_event = sorted(
        [order for order in events ],
        key=lambda x: x["expiry"]
        )
        return sorted_event
    else:
        return None


def get_alerts_data():
    """Call warframe status api for alert data.

    Returns:
        dict: alerts data | None
    """
    response = warframe_status.world("alerts")
    if len(response) >0:
        sorted_alert = sorted(
        [order for order in response ],
        key=lambda x: x["expiry"]
        )
        return sorted_alert
    else:
        return None


def get_alert_reward(data):
    """Getting alert rewards with their images.

    Args:
        data (dict): alert data.

    Returns:
        list: list of alert rewards.
    """
    reward = []
    if 'mission' in data:
        if 'reward' in data['mission']:
                if 'items' in data['mission']['reward']:
                    if len(data['mission']['reward']['items']) > 0:
                        for item in data['mission']['reward']['items']:
                            reward.append({
                                            "item": item,
                                            "image": item,
                                            "amount": 1
                                        })
                if 'countedItems' in data['mission']['reward']:
                    if len(data['mission']['reward']['countedItems']) > 0:
                        for item in data['mission']['reward']['countedItems']:
                            reward.append({
                                            "item": item['key'],
                                            "image": item['key'],
                                            "amount": item['count']
                                        })
                if 'credits' in data['mission']['reward']:
                    if data['mission']['reward']['credits'] > 0:
                        reward.append({
                                        "item": Warframe.CREDITS.value["name"],
                                        "image": Warframe.CREDITS.value["image"],
                                        "amount": data['mission']['reward']['credits']
                                        })
    return reward


@st.cache_data(ttl="30d",show_spinner=False)
def get_cached_items(item_ids):
    """Getting all of the items aync by uniqueNames.

    Args:
        item_ids (list): list of uniqueNames.

    Returns:
        list: list of items.
    """
    return asyncio.run(warframe_status.items_async(item_ids))


def preload_data(data):
    """Getting all of the baro/varzia items.

    Args:
        data (dict): baro/varzia data for filtering.

    Returns:
        list: list of items.
    """
    items = {
            "types" : [],
            "items" : []
    }
    ids = []
    progress_text = AppMessages.PROGRESS.value
    progress = st.progress(0, text=progress_text)
    with st.spinner(AppMessages.LOAD_DATA.value,show_time=True):
        for i, item in enumerate(data):
            if "M P V" in item["item"]:
                progress.progress((i+1)/len(data), text=f"""{(i+1)}/{len(data)} Items. Removing {item["item"]}""")
                continue
            else:
                ids.append({
                            "uniqueName": item["uniqueName"],
                            "metadata":{
                                "ducats" : item["ducats"] if item["ducats"] is not None else 0,
                                "credits" : item["credits"] if item["credits"] is not None else 0,
                            }
                            
                        })
            
                progress.progress((i+1)/len(data), text=f"""{(i+1)}/{len(data)} Items. Indexed: {item["item"]}""")
        
        items["items"] =get_cached_items(ids)

    progress.empty()
    return items


def clear_cached_item_call():
    """
        Clear cache for the get_cached_items() function.
    """
    get_cached_items.clear()


def get_all_tradables():
    """Get all of the market items.

    Returns:
        dict: json response.
    """
    return warframe_market.items()


def get_item_by_name(name):
    """Get item by name.

    Args:
        name (string): name of an item.

    Returns:
        dict: json data of the found item | None
    """
    result = warframe_status.items(WarframeStatusSearchParams(identifier=name.replace(" Blueprint", ""),by="name",type="items"))
    if len(result)>0:
        for item in result:
            if name == item["name"]:
                return item 
        return result[0]
    else:
        return None


def get_news():
    """API get news data.

    Returns:
        list: list of json data for news.
    """
    world_state=warframe_status.world()
    news = []
    if 'news' in world_state:
        if len(world_state["news"]) > 0:
            for new in world_state["news"]:
                if new["update"] == False and new["primeAccess"] == False and new["stream"] == False:
                    continue
                else:
                    news.append(new)
            
            news = sorted(
                [new for new in news ],
                key=lambda x: x["date"],reverse=True
                )
            
            return news
        else: return None


def get_cycles():
    """API get cycles for open worlds.

    Returns:
        list: list of json data for open worlds.
    """
    world_state=warframe_status.world()
    cycles = [
                {
                    "name":"Cetus",
                    "data": world_state["cetusCycle"],
                    "image": get_image_url("/Lotus/Types/Items/MiscItems/PhotoboothTileEidolonLandscape",True)
                },
                {
                    "name":"Deimos",
                    "data": world_state["cambionCycle"],
                    "image": get_image_url("/Lotus/Types/Items/MiscItems/PhotoboothTileDeimosLandscape",True)
                },
                {
                    "name":"Zariman",
                    "data": world_state["zarimanCycle"],
                    "image": get_image_url("/Lotus/Types/Items/PhotoBooth/Zariman/PhotoboothTileZarAmphitheatre",True)
                },
                {
                    "name":"Fortuna",
                    "data": world_state["vallisCycle"],
                    "image": get_image_url("/Lotus/Types/Items/MiscItems/PhotoboothTileVenusLandscape",True)
                },
                {
                    "name":"Duviri",
                    "data": world_state["duviriCycle"],
                    "image": get_image_url("/Lotus/Types/Items/MiscItems/PhotoboothTileDuviriTeshinsCave",True)
                },
            ]
    return cycles


def get_rivens_settings():
    """API for riven attribute list and item list

    Returns:
        tuple(list,list): combined data of riven default informations.
    """
    return warframe_market.rivens_info("items"), warframe_market.rivens_info("attributes")


def get_rivens(weapon_url_name, buyout_policy=None, positive_stats=None, negative_stats=None,
               operation=None, re_rolls_min=None, re_rolls_max=None, polarity=None, status=None):
    """
    Fetch and filter Riven auctions from Warframe Market.

    Args:
        weapon_url_name (str): Weapon URL path.
        buyout_policy (str, optional): Buyout type ("Buyout", "Auction", or None).
        positive_stats (list, optional): List of positive attributes.
        negative_stats (list, optional): List of negative attributes.
        operation (str, optional): Not implemented (reserved for future use).
        re_rolls_min (int, optional): Minimum reroll count.
        re_rolls_max (int, optional): Maximum reroll count.
        polarity (str, optional): Riven polarity.
        status (str, optional): Desired owner status (e.g., "ingame", "online", "offline").

    Returns:
        list: Filtered list of Riven auctions or None if no results.
    """
    buyout_map = {"Buyout": "direct", "Auction": "with"}
    buyout_policy = buyout_map.get(buyout_policy, None)

    # Fetch rivens from the market API
    rivens = warframe_market.rivens_auction(
        RivenSearchParams(weapon_url_name, buyout_policy, positive_stats,
                          negative_stats, operation, re_rolls_min, re_rolls_max, polarity)
    )

    if not rivens or status is None:
        return rivens

    # Filter by owner status
    return [riven for riven in rivens if status == riven["owner"]["status"]]


def get_weapon_by_name(name):
    """API for weapon data search by name.

    Args:
        name (string): weapon's name.

    Returns:
        dict: json data of weapon.
    """
    name = name.replace("_", " ")
    response = warframe_status.items(WarframeStatusSearchParams(name,"name",type="weapons",remove=["patchlogs"]))
    if len(response) < 1:
        return None
    else:
        for item in response:
            if item["name"].lower() == name.lower():
                return item
        return response[0]


def get_event_rewards(data):
    """Get event rewards.

    Args:
        data (dict): event json data.

    Returns:
        list: list of reward names.
    """
    rewards = []
    if "interimSteps" in data and len(data["interimSteps"])>0:
        for step in data["interimSteps"]:
            if "reward" in step:
                if "items" in step["reward"] and len(step["reward"]["items"])>0:
                    for item in step["reward"]["items"]:
                        rewards.append(item)

    if "rewards" in data and len(data["rewards"])>0:
        for reward in data["rewards"]:
            if "items" in reward and len(reward["items"])>0:
                for item in reward["items"]:
                    rewards.append(item)

    return rewards


@st.cache_data(ttl="10d",show_spinner=False)
def get_relics():
    """Return all relics.

    Returns:
        list: relic list.
    """
    relic_list = []
    relics = warframe_status.items(WarframeStatusSearchParams("Relic",by="type",type="items",remove=["patchlogs"]))

    if len(relics) < 1:
        return None
    else:
        
        for item in relics:
            if item["tradable"] == False or "Intact" not in item["name"]:
                continue
            if len(item["rewards"])>0:
                item = extract_relic_rewards(item)
            else: 
                continue
            if item is None:
                continue
            relic_list.append(item)
        return relic_list


@st.cache_data(ttl="10d",show_spinner=False)
def get_resurgent_relics():
    """Return list of resurgent relic.

    Returns:
        list: list of resurgent relic.
    """
    relic_list = []
    items = get_variza()["inventory"]
    
    if len(items) < 1:
        return None
    else:
        for item in items:
            if "Projections" not in item["uniqueName"]:
                continue
            relic_list.append(item["uniqueName"])
        return relic_list



def filter_relic(data,rewards,types,tags,resurgent_data=None):
    """Relic filter function.

    Args:
        data (list): relic list.
        rewards (list): reward keywords.
        types (list): relic eras.
        tags (list): relic vault tags.
        resurgent_data (list, optional): list of resurgent relics. Defaults to None.

    Returns:
        list: list of filtered relic.
    """
    filtered_relics = []
    type_map = tuple(types) if types else ("Axi", "Neo", "Meso", "Lith", "Requiem")
    # Determine if the vaulted filter should be applied
    ignore_vaulted = (tags[0] and tags[1]) or (not tags[0] and not tags[1])
    is_vaulted = None if ignore_vaulted else (True if tags[0] else False)

    for item in data:
        conditions = []

        # Apply vaulted filter if not ignored
        if not ignore_vaulted:
            conditions.append(item.get("vaulted", False) == is_vaulted)

        # Apply resurgent data filter if not ignored
        if resurgent_data is not None:
            unique_name = item["uniqueName"].split("/")[-1]
            conditions.append(any(unique_name in x for x in resurgent_data))

        if rewards:
            reward_names = [reward["item"]["name"] for reward in item.get("rewards", [])]

            # Check if any keyword exists as a whole word in any reward name
            reward_match = any(
                any(re.search(rf"\b{re.escape(keyword)}\b", name, re.IGNORECASE) for keyword in rewards)
                for name in reward_names
            )
            conditions.append(reward_match)

        # If any condition is False, skip this relic
        if not all(conditions):
            continue

        # Filter by type
        if item["name"].startswith(type_map):
            filtered_relics.append(item)

    return filtered_relics


def get_relic_rewards():
    """Relic list of relic rewards, requiems included.

    Returns:
        list: list of rewards.
    """
    requiems = warframe_status.items(WarframeStatusSearchParams("Requiem",by="name",type="items",remove=["patchlogs"]))
    requiems_rewards =[]
    if len(requiems)> 0:
        for item in requiems:
            if "rewards" in item and len(item["rewards"])>0:
                requiems_rewards.extend(item["rewards"])
    requiems_rewards = list({reward["item"]["name"] for reward in requiems_rewards})
    rewards = get_prime_list()
    rewards.extend(requiems_rewards)
    return rewards


def prep_image(enum):
    """Image card of Baro/Varzia."""
    img_location = data_manage.get_image_url(enum.value["uniqueName"])
    img_bytes = api_services.get_image(img_location)
    if img_bytes is not None:
        image = Image.open(img_bytes)
        st.image(img_bytes,use_container_width=True)
    else:
        image = Image.open(enum.value["image"])
        st.image(image.resize((200, 200)),use_container_width=True)


def query_exports(item:Enum):
    try:
        return warframe_export.export_open(item)
    except Exception as err:
        logging.warning(f"""Failed request object {item["path"]} in S3. Trying local json instead.""")
        try:
            return warframe_export.export_open(item)
        except Exception as sub_err:
            logging.error(f"""Failed read object {item["path"]}. Error: {sub_err}""")
            return None


def update_exports(password: str) -> None:
    try:
        if password == st.secrets.app.key:
            warframe_export.update_exports()
            error = None
        else:
            raise ValueError("Wrong passkey.")
        
    except (requests.RequestException, lzma.LZMAError) as e:
        logging.error(f"Error fetching or decompressing manifest: {e}")
        error = e
    except (requests.RequestException, json.JSONDecodeError) as e:
        logging.error(f"Error processing: {e}")
        error = e
    except ValueError as e:
        error = e
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        error = e
        
    if error:
        raise error


def clear_cache():
    warframe_market.items.clear()
    warframe_market.rivens_auction.clear()
    warframe_market.rivens_info.clear()
    
    warframe_status.items.clear()
    
    get_world_state.clear()
    get_cached_items.clear()
    get_relics.clear()
    get_resurgent_relics.clear()
    