from datetime import datetime, timezone
from hashlib import sha256
from itertools import chain
import re
from typing import Dict, List, Literal, Optional, Tuple, Union

import urllib


from config.classes.parameters import WarframeStatusSearchParams, RivenSearchParams
from config.constants import AppMessages, Warframe

def market_filter(
        data,
        rep: int = 0,
        status: Optional[Literal["ingame", "online", "offline"]] = None,
        wtb: Optional[Literal["sell", "buy"]] = "sell"
    ) -> List[Dict]:
    """
    Filter market orders based on reputation threshold, user status, and order type.

    Args:
        data (List[Dict]): List of market order dictionaries.
        rep (int, optional): Minimum reputation threshold. Defaults to 0.
        status (str, optional): User's online status to filter by. Defaults to None.
        wtb (str, optional): Order type to filter by ('sell' or 'buy'). Defaults to None.

    Returns:
        List[Dict]: Filtered list of market orders.
    """
    if wtb:
        data = [entry for entry in data if entry['order_type'] == wtb]
    if status:
        data = [entry for entry in data if entry['user']['status'] == status]
    return [entry for entry in data if entry['user']['reputation'] >= rep]


def parse_item_string(item_string: str) -> Tuple[str, int]:
    """
    Extract the item name and count from a given string.

    Args:
        item_string (str): The input string containing the item and its count.

    Returns:
        Tuple[str, int]: A tuple containing the item name and its count.

    Examples:
        >>> parse_item_string("3 Apple")
        ('Apple', 3)
        >>> parse_item_string("Banana")
        ('Banana', 1)
    """
    if not item_string.strip():
        raise ValueError("The input string is empty or only contains whitespace.")

    parts = item_string.split(maxsplit=1)
    if parts[0].isdigit():
        count = int(parts[0])
        name = parts[1] if len(parts) > 1 else ""
    else:
        count = 1
        name = item_string

    if not name:
        raise ValueError("The item name is missing in the input string.")

    return name, count


def clean_prime_names(frame_json, weap_json):
    """Group and clean the prime list.

    Args:
        frame_json (list): Prime Frame list.
        weap_json (list): Prime Weapon list.

    Returns:
        list: Combined list of Prime names.
    """
    return [item["name"] for item in chain(frame_json, weap_json)]


def format_timedelta(delta, day=True):
    """
    Extract hours, minutes, and optionally days from a timedelta object.

    Args:
        delta (timedelta): Time period.
        day (bool, optional): Whether to include days in the output. Defaults to True.

    Returns:
        str: Formatted time message.
    """
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(abs(total_seconds), 86400)
    hours, minutes = divmod(remainder, 3600)[0], divmod(remainder, 60)[0]

    message = (
        AppMessages.delta_datetime_message(days, hours, minutes)
        if day else
        AppMessages.delta_time_message(hours, minutes)
    )

    return message + " ago" if total_seconds < 0 else message


def get_min_status_plat(data, status):
    """
    Filter and find the lowest platinum price for an item.

    Args:
        data (list): List of Warframe.market orders.
        status (str or list): Online status or list of statuses (e.g., "ingame", "online", "offline").

    Returns:
        dict or None: The lowest price order object, or None if no valid orders are found.
    """
    # Ensure status is a list of valid statuses
    status = Warframe.ONLINE_STATUS.value["list"] if not status else [status] if isinstance(status, str) else status
    
    # Status priority for sorting (lower value means higher priority)
    status_priority = Warframe.ONLINE_STATUS.value["priority"]

    # Filter and sort the orders
    filtered_sorted_orders = sorted(
        (order for order in data if order["user"]["status"] in status and order['order_type'] == "sell"),
        key=lambda x: (status_priority.get(x["user"]["status"], 3), x["platinum"])
    )

    return filtered_sorted_orders if filtered_sorted_orders else None



def remove_wf_color_codes(string) -> str:
    """Remove Warframe color codes in strings.

    Args:
        string (string): target string.

    Returns:
        string: removed color string.
    """
    return re.sub(r"<.*?>", "", string)


def calculate_percentage_time(start,end) -> float:
    """Calculate time percentage base on start, end time.

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
    """Filter for baro/varzia

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
        if "Relic" in types and item["category"] == "Relics":
            condition = True

        # If 'Warframe' is selected, include warframe items
        if "Warframe" in types and item["category"] == "Warframes":
            condition = True

        # If 'Others' is selected, include items that are not Weapon, Relic, or Warframe
        if "Others" in types and item["category"] not in ["Primary", "Secondary", "Melee", "Arch-Gun", "Arch-Melee", "Relics", "Warframes"]:
            condition = True

        # Append the item if it matches any of the selected conditions
        if condition:
            filtered.append(item)
    return filtered


def check_pattern_prime_set(s):
    """Check for item with name 'x Prime Set/Blueprint'.

    Args:
        s (string): item name.

    Returns:
        boolean: whether if the item match or not.
    """
    pattern = r"^(.+)_prime_(set|blueprint)$"
    return bool(re.match(pattern, s))


def check_pattern_normal_set(s):
    """Check for item with name 'x Set'.

    Args:
        s (string): item name.

    Returns:
        boolean: whether if the item match or not.
    """
    pattern = r"^(.+)_(set)$"
    return bool(re.match(pattern, s))


def hash_func(obj: Union[RivenSearchParams, WarframeStatusSearchParams]) -> str:
    """
    Generate a unique hash for a given search parameter object.

    Args:
        obj (Union[RivenSearchParams, WarframeStatusSearchParams]): Object containing search parameters.

    Returns:
        str: A unique hash string representing the object.
    """
    query_string = obj.to_query_string()
    raw_string = f"{obj.type}&{obj.identifier}&{query_string}"
    
    # Generate a secure hash to ensure uniqueness
    return sha256(raw_string.encode('utf-8')).hexdigest()


def encode_identifier(identifier, is_unique=False):
    """
    Encode an identifier for use in URLs.

    Args:
        identifier (str): The identifier to be encoded.
        is_unique (bool, optional): Whether to use a unique identifier format. Defaults to False.

    Returns:
        str: The encoded identifier.
    """
    if is_unique:
        parts = identifier.split("/")
        identifier = "/".join(parts[-3:]) if len(parts) >= 3 else parts[-1]
    else:
        identifier = identifier.replace(" and ", " & ")
        identifier = re.sub(r'\s*\(.*?\)', '', identifier)

    return urllib.parse.quote_plus(identifier, safe="")
