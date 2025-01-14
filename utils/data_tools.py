from utils import structures
from statistics import median
import re 

def market_filter(data, rep=0, status="All",wtb=""):
    if wtb == "WTB": 
        data =[entry for entry in data if (entry['order_type'] == "buy")]
    else:
        data =[entry for entry in data if (entry['order_type'] == "sell")]
    if status != "All":
        data =[entry for entry in data if (entry['user']['status'] == status.lower())]
    return [entry for entry in data if entry['user']['reputation'] >= rep]

def get_relic_reward_options(relics,name):
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
    relic_option={}
    for item in relic["data"]["rewards"]:
        if 'Forma Blueprint' not in item["item"]["name"]:
            relic_option[item["item"]["name"].lower().replace(" ", "_")] = item["item"]["name"]
    return relic_option

def get_relic_reward_list(relics):
    relic_option={}
    for item in relics:
        rewards = get_relic_rewards_string(item)
        relic_option[item["data"]["name"]] = structures.relic_reward_names(item["data"]["name"],rewards)
    return relic_option

def get_relic_names(json_data):
    names = []
    for _, obj in enumerate(json_data):
        names.append(obj["data"]["name"])
    return names

def get_correct_piece(piece_list,name):
    for item in piece_list:
        if item['en']['item_name'].lower().replace(" ","_") == name:
            return item
 
def get_average_plat_price(orders):
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
    pattern = r'(\w+\sPrime)'
    match = re.search(pattern, input_string)
    if match:
        return match.group(1)
    else:
        return ""

def get_prime_resurgent(primes,relics_list):
    result = []
    for prime in primes:
        rewards = search_rewards([prime],relics_list)
        if len(rewards)>0:
            result.append(prime)
    return result
    