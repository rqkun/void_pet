from statistics import median

def market_filter(data, rep=0, status="All",wtb=""):
    """ Filter data with reputation threshold, online statuses, buy/sell orders. """
    if wtb == "WTB": 
        data =[entry for entry in data if (entry['order_type'] == "buy")]
    else:
        data =[entry for entry in data if (entry['order_type'] == "sell")]
    if status != "All":
        data =[entry for entry in data if (entry['user']['status'] == status.lower())]
    return [entry for entry in data if entry['user']['reputation'] >= rep]
 
def get_average_plat_price(orders):
    """ 
        Return median price of a list of orders.
        By doing it this way, we can avoid large deviation between prices.
    """
    prices = []
    for order in orders:
        prices.append(order["platinum"])
    return median(prices) if len(orders) > 0 else 0

def parse_item_string(item_string):
    parts = item_string.split(" ", 1)  # Split into two parts: count and name
    if parts[0].isdigit():  # Check if the first part is a number
        count = int(parts[0])
        name = parts[1]
    else:  # If no number at the start, default count to 1
        count = 1
        name = item_string
    return name, count

def clean_prime_names(frame_json,weap_json):
    result = []
    for item in frame_json:
        result.append(item["name"])
    for item in weap_json:
        result.append(item["name"])
    return result


    
