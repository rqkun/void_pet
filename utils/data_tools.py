from collections import defaultdict
from utils import structures
from statistics import median
import re 

def market_filter(data, rep=0, status="All",wtb=""):
    """ Filter data with reputation threshold, online statuses, buy/sell orders. """
    if wtb == "WTB": 
        data =[entry for entry in data if (entry['order_type'] == "buy")]
    else:
        data =[entry for entry in data if (entry['order_type'] == "sell")]
    if status != "All":
        data =[entry for entry in data if (entry['user']['status'] == status.lower())]
    return [entry for entry in data if entry['user']['reputation'] >= rep]

def get_relic_reward_options(relics,name):
    """ Return relic's rewards dictionary. """
    relic = None
    relic_option={}
    for item in relics:
        if item["data"]["name"] == name:
            relic = item["data"]
            break
    if relic is None:
        return None
    for item in relic["rewards"]:
        value = structures.relic_reward_object(item["chance"],item["rarity"],item["item"]["name"])
        if 'Forma Blueprint' not in item["item"]["name"]:
            relic_option[item["item"]["name"]] = value
    return relic_option

def search_rewards(search_keys,data):
    """ Return relic that have search_keys as reward(s). """
    relics = get_relic_reward_list(data)
    if len(search_keys) > 0 and len(relics) :
        result = []
        for dict_key, outer_dict in relics.items():
            if 'rewards' in outer_dict:
                for key in outer_dict['rewards'].keys():
                    if any("_"+search_key.lower().replace(" ", "_") in "_"+key.lower() for search_key in search_keys):
                        result.append(dict_key)
                        break  # No need to check further rewards for this outer key
        return result
    return get_relic_names(data)

def get_relic_rewards_string(relic):
    """ Return dictionary with reward names with some formatting. """
    relic_option={}
    for item in relic["data"]["rewards"]:
        if 'Forma Blueprint' not in item["item"]["name"]:
            relic_option[item["item"]["name"].lower().replace(" ", "_")] = item["item"]["name"]
    return relic_option

def get_relic_reward_list(relics):
    """ Return dictionary options for the select relic widget. """
    relic_option={}
    for item in relics:
        rewards = get_relic_rewards_string(item)
        relic_option[item["data"]["name"]] = structures.relic_reward_names(item["data"]["name"],rewards)
    return relic_option

def get_relic_names(json_data):
    """ Return list of relic names from input. """
    names = []
    for _, obj in enumerate(json_data):
        names.append(obj["data"]["name"])
    return names

def get_correct_piece(piece_list,name):
    """ Return the correct Prime component from a set. """
    for item in piece_list:
        if item['en']['item_name'].lower().replace(" ","_") == name:
            return item
 
def get_average_plat_price(orders):
    """ 
        Return median price of a list of orders.
        By doing it this way, we can avoid large deviation between prices.
    """
    prices = []
    for order in orders:
        prices.append(order["platinum"])
    return median(prices) if len(orders) > 0 else 0

def clean_prime_names(frame_json,weap_json):
    result = []
    for item in frame_json:
        result.append(item["name"]) 
    for item in weap_json:
        result.append(item["name"]) 
    return result

def extract_prime_substring(input_string):
    """ Return the Prime set name from a Prime component. """
    pattern = r'(\w+\sPrime)'
    match = re.search(pattern, input_string)
    if match:
        return match.group(1)
    else:
        return ""

def get_prime_resurgent(primes,relics_list):
    """ Return the list of prime resurgent that are in rotation. """
    result = []
    for prime in primes:
        rewards = search_rewards([prime],relics_list)
        if len(rewards)>0:
            result.append(prime)
    return result

def get_sortie_missions(data):
    result = {}
    result_option = []
    for item in data["variants"]:
        result[item["missionType"]] = item
        result_option.append(item["missionType"])
    return result, result_option

def parse_item_string(item_string):
    parts = item_string.split(" ", 1)  # Split into two parts: count and name
    if parts[0].isdigit():  # Check if the first part is a number
        count = int(parts[0])
        name = parts[1]
    else:  # If no number at the start, default count to 1
        count = 1
        name = item_string
    return name, count

def get_invasions_rewards(data):
    result = defaultdict(int)
    for invasion in data:
        if invasion["attacker"]["faction"] != "Infested":
            name, count = parse_item_string(invasion["attacker"]["reward"]["asString"]) 
            result[name] += count

        
        name, count = parse_item_string(invasion["defender"]["reward"]["asString"]) 
        result[name] += count
    
    return result