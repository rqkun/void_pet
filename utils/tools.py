from datetime import datetime, timezone
import re
from typing import Union

from config.classes import WarframeStatusSearchParams, RivenSearchParams
from config.constants import AppMessages

def market_filter(data, rep=0, status="All",wtb=""):
    """ Filter data with reputation threshold, online statuses, buy/sell orders.

    Args:
        data (json): a json / dictionary object of market's orders.
        rep (int, optional): reputation threshold for filter. Defaults to 0.
        status (str, optional): online status of the order owner for filter. Defaults to "All".
        wtb (str, optional): wtb/wts status. Defaults to "".

    Returns:
        List: orders that have been filtered out.
    """
    if wtb == "WTB": 
        data =[entry for entry in data if (entry['order_type'] == "buy")]
    else:
        data =[entry for entry in data if (entry['order_type'] == "sell")]
    if status != "All" and status is not None:
        data =[entry for entry in data if (entry['user']['status'] == status.lower())]
    return [entry for entry in data if entry['user']['reputation'] >= rep]


def parse_item_string(item_string):
    """ Return name and count of the reward string.

    Args:
        item_string (str): The reward string to be processed.

    Returns:
        str: Name of the reward.
        int: Amount of the reward.
    """
    parts = item_string.split(" ", 1)
    if parts[0].isdigit(): 
        count = int(parts[0])
        name = parts[1]
    else:
        count = 1
        name = item_string
    return name, count


def clean_prime_names(frame_json,weap_json):
    """ Group and clean the prime list.

    Args:
        frame_json (list): Prime Frame list.
        weap_json (list): Prime Weapon list .

    Returns:
        list: Full list of Primes.
    """
    result = []
    for item in frame_json:
        result.append(item["name"])
    for item in weap_json:
        result.append(item["name"])
    return result


def format_timedelta(delta,day=True):
    """ Extract hours, minutes, and seconds from the time delta.

    Args:
        delta (timedelta): Iime period.
        day (bool, optional): Whether if should the function return days or not. Defaults to True.

    Returns:
        str: Formatted time message.
    """
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)
    if day:
        message = AppMessages.delta_datetime_message(days,hours,minutes)
    else:
        message = AppMessages.delta_time_message(hours,minutes)
    if total_seconds < 0:
        return message.replace("-","") + " ago"
    else: return message


def get_min_status_plat(data,status):
    """ Filter and find the lowest plat price for an item.

    Args:
        data (object): Warframe.market Data
        status (str): Online status, usually Ingame.

    Returns:
        object: The lowest price order object.
    """
    if status is None or status == "":
        status = ["offline","ingame","online"]
    status_priority = {"ingame": 0, "online": 1, "offline": 2}
    
    filtered_sorted_orders = sorted(
        [order for order in data if ((order["user"]["status"] in status) and order['order_type'] == "sell")],
        key=lambda x: (status_priority.get(x["user"]["status"], 3), x["platinum"])
    )
    return filtered_sorted_orders


def remove_wf_color_codes(string):
    """ Remove Warframe color codes in strings.

    Args:
        string (string): target string.

    Returns:
        string: removed color string.
    """
    return re.sub(r"<.*?>", "", string)


def deforma_rewards(option_map):
    """ Remove Forma Blueprint rewards for market checking.

    Args:
        option_map (list): list of rewards.

    Returns:
        list: non-forma list of rewards
    """
    for item in option_map:
        if "Forma Blueprint" in item["item"]["name"]:
            option_map.remove(item)
    return option_map

def calculate_percentage_time(start,end) -> float:
    """ Calculate time percentage base on start, end time.

    Args:
        start (string): Start timestamp string.
        end (string): End timestamp string.

    Returns:
        float: calculated percentage completed.
    """
    target_time = datetime.fromisoformat(end.replace("Z", "+00:00"))
    # Current time in UTC
    current_time = datetime.now(timezone.utc)
    # Calculate percentage
    start_time = datetime.fromisoformat(start.replace("Z", "+00:00"))  # Arbitrary start point
    elapsed_time = (current_time - start_time).total_seconds()
    total_time = (target_time - start_time).total_seconds()
    percentage_completed = (elapsed_time / total_time)
    return percentage_completed


def filter_data(items, types):
    """ Filter for baro/varzia

    Args:
        items (list): list of items need filtered.
        types (list): filter types.

    Returns:
        list: list of filtered items.
    """
    filtered = []

    # If types is None or empty, set condition to True to keep all items
    if types is None or len(types) == 0:
        return items

    for item in items:
        condition = False

        # If 'Weapon' is selected, include weapon items
        if "Weapon" in types and item["category"] in ["Primary", "Secondary", "Melee", "Arch-Gun", "Arch-Melee"]:
            condition = True

        # If 'Relic' is selected, include relic items
        if "Relic" in types and item["type"] == "Relic":
            condition = True

        # If 'Warframe' is selected, include warframe items
        if "Warframe" in types and item["type"] == "Warframe":
            condition = True

        # If 'Others' is selected, include items that are not Weapon, Relic, or Warframe
        if "Others" in types and item["category"] not in ["Primary", "Secondary", "Melee", "Arch-Gun", "Arch-Melee", "Relic", "Warframe"] and item["type"] not in ["Primary", "Secondary", "Melee", "Arch-Gun", "Arch-Melee", "Relic", "Warframe"]:
            condition = True

        # Append the item if it matches any of the selected conditions
        if condition:
            filtered.append(item)
    return filtered


def check_pattern_prime_set(s):
    """ Check for item with name 'x Prime Set/Blueprint'.

    Args:
        s (string): item name.

    Returns:
        boolean: whether if the item match or not.
    """
    pattern = r"^(.+)_prime_(set|blueprint)$"
    return bool(re.match(pattern, s))


def check_pattern_set(s):
    """ Check for item with name 'x Set'.

    Args:
        s (string): item name.

    Returns:
        boolean: whether if the item match or not.
    """
    pattern = r"^(.+)_(set)$"
    return bool(re.match(pattern, s))


def hash_func(obj: Union[RivenSearchParams , WarframeStatusSearchParams]) -> str:
    query_string = obj.to_query_string()
    return f"{obj.type}&{obj.identifier}&{query_string}"