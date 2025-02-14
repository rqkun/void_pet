from datetime import datetime, timezone
import re
from statistics import median

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
 
 
def get_average_plat_price(orders) -> float:
    """ Return median price of a list of orders. 
        By doing it this way, we can avoid large deviation between prices.

    Args:
        orders (list): list of orders.

    Returns:
        float: the median price of input orders.
    """
    prices = []
    for order in orders:
        prices.append(order["platinum"])
    return median(prices) if len(orders) > 0 else 0


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
        return AppMessages.delta_datetime_message(days,hours,minutes)
    else:
        return AppMessages.delta_time_message(hours,minutes)


def check_disable(data):
    """ Check the button should be disable or not

    Args:
        data (obj): Button's condition

    Returns:
        bool: Button's disable state
    """
    return False if data["active"] else True


def get_min_status_plat(data,status):
    """ Filter and find the lowest plat price for an item.

    Args:
        data (object): Warframe.market Data
        status (str): Online status, usually Ingame.

    Returns:
        object: The lowest price order object.
    """
    filtered_sorted_orders = sorted(
    [order for order in data if (order["user"]["status"] == status and order['order_type'] == "sell") ],
    key=lambda x: x["platinum"]
    )
    return filtered_sorted_orders[0]


def remove_wf_color_codes(string):
    return re.sub(r"<.*?>", "", string)


def deforma_rewards(option_map):
    for item in option_map:
        if "Forma Blueprint" in item["item"]["name"]:
            option_map.remove(item)
    return option_map

def calculate_percentage_time(start,end):
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