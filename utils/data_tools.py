from utils import structures
def market_filter(data, rep=0, offline=False,wtb=False):
    if wtb is False:
        data =[entry for entry in data if (entry['order_type'] == "sell")]
    else: 
        data =[entry for entry in data if (entry['order_type'] == "buy")]
    if offline is False:
        data =[entry for entry in data if (entry['user']['status'] == "online" or entry['user']['status'] == "ingame")]
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
                    if any(search_key.lower().replace(" ", "_") in key.lower() for search_key in search_keys):
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
    for index, obj in enumerate(json_data):
        names.append(obj["data"]["name"])
    return names

def get_correct_piece(piece_list,name):
    for item in piece_list:
        if item['en']['item_name'].lower().replace(" ","_") == name:
            return item
 
def get_average_plat_price(orders):
    avg_plat = 0
    for order in orders:
        avg_plat += order["platinum"]
    return avg_plat/len(orders) if len(orders) > 0 else 0

def clean_prime_names(frame_json,weap_json):
    result = []
    for item in frame_json:
        result.append(item["name"]) 
    for item in weap_json:
        result.append(item["name"]) 
    return result