from utils import structures
def market_filter(data, rep=0, offline=False,wtb=False):
    if wtb is False:
        data =[entry for entry in data if (entry['order_type'] == "sell")]
    else: 
        data =[entry for entry in data if (entry['order_type'] == "buy")]
    if offline is False:
        data =[entry for entry in data if (entry['user']['status'] == "online" or entry['user']['status'] == "ingame")]
    return [entry for entry in data if entry['user']['reputation'] >= rep]

def get_relic_reward_options(relic):
    relic_option={}
    for item in relic["rewards"]:
        value = structures.relic_reward_object(item["chance"],item["rarity"],item["item"]["name"])
        if 'Forma Blueprint' not in item["item"]["name"]:
            relic_option[item["item"]["name"]] = value
    return relic_option

def get_relic_names(json_data):
    name_index_dict = {}
    for index, obj in enumerate(json_data):
        name = obj["data"]["name"]
        name_index_dict[name] = index
    return name_index_dict


 
def get_average_plat_price(orders):
    avg_plat = 0
    for order in orders:
        avg_plat += order["platinum"]
    return avg_plat/len(orders) if len(orders) > 0 else 0