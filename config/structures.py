def ware_object(vendor="",data=None):
    """ Return vendor with their inventory data. """
    return {
        "vendor": vendor,
        "data": data
    }

def relic_object(price=1,data=None):
    """ Return relic's prices and data. """
    return {
        "price": price,
        "data": data
    }

def relic_reward_object(chance=0, rarity="", name=""):
    """ Return reward's data. """
    return{
        "name": name,
        "chance": chance,
        "rarity": rarity
    }

def relic_reward_names(name, rewards):
    """ Return relic's name and rewards. """
    return{
        "name": name,
        "rewards": rewards,
    }

# def generic_icon():
#     return{
#         ""
#     }
