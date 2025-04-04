from datetime import datetime, timezone
from hashlib import sha256
from itertools import chain
import logging
import re
from statistics import median
from typing import Dict, List, Literal, Optional, Tuple, Union

import urllib

from numpy import average
import pandas as pd


from config.classes.parameters import WarframeStatusSearchParams, RivenSearchParams
from config.constants import AppIcons, AppMessages, Warframe
from utils import tools

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
    hours, remainder = divmod(remainder, 3600)
    minutes = divmod(remainder, 60)[0]
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

def sort_open_close(data):
    """
    Filter and find the lowest platinum price for an item.

    Args:
        data (list): List of Warframe.market orders.
        status (str or list): Online status or list of statuses (e.g., "ingame", "online", "offline").

    Returns:
        dict or None: The lowest price order object, or None if no valid orders are found.
    """
    # Ensure status is a list of valid statuses
    df = pd.DataFrame(data)

    # Convert last_seen to datetime
    # df["last_seen"] = pd.to_datetime(df["user"].apply(lambda x: x["last_seen"]),format="%Y-%m-%dT%H:%M:%S.%f%z")
    df["creation_date"] = pd.to_datetime(df["creation_date"],format="%Y-%m-%dT%H:%M:%S.%f%z")
    df["last_update"] = pd.to_datetime(df["last_update"],format="%Y-%m-%dT%H:%M:%S.%f%z")
    
    # Get today's date in UTC
    today = datetime.now(timezone.utc).date()

    # Filter only today's data & status = ingame
    filtered_df = df[((df["creation_date"].dt.date == today) | (df["last_update"].dt.date == today)) & (df["visible"]==True) & (df["order_type"]=="sell")]

    # Sort by last_seen (earliest to latest)
    sorted_df = filtered_df.sort_values(by=["last_update","platinum"], ascending=[True,False])
    
    open = sorted_df.iloc[0]["platinum"] if not sorted_df.empty else None
    # Get last element
    close = sorted_df.iloc[-1]["platinum"] if not sorted_df.empty else None
    
    prices_df = filtered_df.sort_values(by="platinum", ascending=True)

    minp = prices_df.iloc[0]["platinum"]
    maxp = prices_df.iloc[-1]["platinum"]
    
    median_ = median(prices_df["platinum"])
    avg = average(prices_df["platinum"])
    
    return open, close, minp, maxp, median_, avg
    # Status priority for sorting (lower value means higher priority)
    


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
        if 'category' in item:
            if "Warframes" in types and item["category"] == "Warframes":
                condition = True
            if "Archwings" in types and item["category"] == "Archwing":
                condition = True
            if "Weapons" in types and item["category"] in ["Primary", "Secondary", "Melee", "Arch-Gun", "Arch-Melee"]:
                condition = True
            if "Relics" in types and item["category"] == "Relics":
                condition = True
            if "Mods" in types and item["category"] == "Mods":
                condition = True
            if "Cosmetics" in types and item["category"] == "Skins":
                condition = True
            if "Sentinels" in types and item["category"] == "Sentinels":
                condition = True
            if "Others" in types and item["category"] not in ["Sentinels","Skins","Mods","Archwing","Primary", "Secondary", "Melee", "Arch-Gun", "Arch-Melee", "Relics", "Warframes"]:
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

    return urllib.parse.quote(identifier,safe="&")


def prep_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes data and returns a styled DataFrame in Streamlit, 
    highlighting the row(s) where (Median - Min) is the lowest and non-negative in green,
    and rows where (Median - Min) is negative in red.
    """
    if df.empty:
        logging.warning("No data available to display.")
        return df
    
    base_url = Warframe.MARKET_API.value["url"]
    icon = AppIcons.EXTERNAL.value
    # df = df.drop(columns=["Open","Close"])
    formatted_names = df["Name"].str.replace(" ", "_").str.lower() + "_set"
    df["Link"] = f"{base_url}" + formatted_names
    df.set_index("Link", inplace=True)
    # df.set_index("Name", inplace=True)
    df["Diff"] = df["Median"] - df["Min"]

    min_diff_value = df[df["Diff"] >= 0]["Diff"].min() if not df[df["Diff"] >= 0].empty else None
    max_diff_value = df[df["Diff"] >= 0]["Diff"].max() if not df[df["Diff"] >= 0].empty else None
    highlight_gold = df[df["Diff"] == max_diff_value].index.tolist() if max_diff_value is not None else []
    highlight_lime = df[df["Diff"] == min_diff_value].index.tolist() if min_diff_value is not None else []
    highlight_red = df[df["Diff"] < 0].index.tolist()

    def highlight_row(row:pd.Series):
        if row.name in highlight_lime:
            return ['color: lime; font-weight: bold;'] * len(row)
        elif row.name in highlight_red:
            return ['color: #FF6961; font-weight: bold;'] * len(row)
        elif row.name in highlight_gold:
            return ['color: #FFD700; font-weight: bold;'] * len(row)
        return [''] * len(row)



    df = df.drop(columns=["Diff"])

    try:
        styled_df = df.style.apply(highlight_row, axis=1)
    except Exception as e:
        logging.warning(f"Error applying row styling: {e}")
        styled_df = df

    return styled_df


def calculate_price_stats(orders):
    """Calculate min, median, and max prices from a list of orders."""
    if not orders:
        return 0, 0, 0, 0, 0, 0

    return sort_open_close(orders)


def process_item_data(items:list)->list:
    """Process a list of items into a DataFrame-ready format."""
    processed_data = []

    for item in items:
        open_price,close_price,min_plat, max_plat, median_plat, avg_plat = calculate_price_stats(item["orders"])
        processed_data.append({
            "Image": f"""{Warframe.MARKET_API.value["static"]}{item["img_link"]}""",
            "Name": item["url"].replace("_", " ").replace(" set", "").title(),
            "Count": len(item["orders"]),
            "Average": int(avg_plat),
            "Median": int(median_plat),
            "Min": int(min_plat),
            "Max": int(max_plat),
            "Open": int(open_price),
            "Close": int(close_price),
        })

    return processed_data


def convert_index(name: str):
    """Generate an index using Name and current GMT date."""
    name = f"""{name.replace(" ", "-")}-{datetime.now(timezone.utc).strftime("%d-%m-%Y-UTC")}"""
    return name


def insert(df: pd.DataFrame, sheet: pd.DataFrame):
    """Insert or update data in the sheet, ensuring timestamps are in GMT."""
    if len(sheet) ==0 or list(sheet.columns) != Warframe.COLUMN_DEF.value:
        sheet= pd.DataFrame(columns=Warframe.COLUMN_DEF.value)
    sheet.set_index("Id", inplace=True)

    current_time = datetime.now(timezone.utc).strftime("%d/%m/%Y - %H:%M:%S UTC")
    for _, item in df.iterrows():
        index_name = convert_index(item["Name"])

        sheet.loc[index_name] = [
            item["Name"],
            int(item["Count"]),
            int(item["Average"]),
            int(item["Median"]),
            int(item["Min"]),
            int(item["Max"]),
            sheet.at[index_name, "Open"] if index_name in sheet.index else int(item["Open"]),
            int(item["Close"]),
            current_time
        ]

    return sheet


def format_time_difference(td, original_time):
    """
    Format a timedelta into days, hours, minutes format
    If more than a week has passed, return the original UTC time
    """
    # Check if more than a week (7 days) has passed
    if td.days > 7:
        # Return the original UTC time formatted nicely
        return f"{original_time}"
    
    # Extract days
    days = td.days
    
    # Extract hours and minutes from seconds
    seconds = td.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    # Build the formatted string
    if days > 0:
        return f"{days} days, {hours} hours, {minutes} minutes ago"
    elif hours > 0:
        return f"{hours} hours, {minutes} minutes ago"
    else:
        return f"{minutes} minutes ago"


def extract_item_name(url:str) -> str:
    return url.split("/")[-1].replace("_", " ").title()