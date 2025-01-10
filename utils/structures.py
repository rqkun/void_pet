def ware_object(vendor="",data=None):
    return {
        "vendor": vendor,
        "data": data
    }

def relic_object(price=1,data=None):
    return {
        "price": price,
        "data": data
    }

def relic_reward_object(chance=0, rarity="", name=""):
    return{
        "name": name,
        "chance": chance,
        "rarity": rarity
    }
