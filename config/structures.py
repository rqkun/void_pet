def ware_object(vendor="",data=None):
    """Return vendor with their inventory data.

    Args:
        vendor (str, optional): Vendor name. Defaults to "".
        data (obj, optional): Vendor inventory. Defaults to None.

    Returns:
        dict: Vendor's data
    """
    return {
        "vendor": vendor,
        "data": data
    }

def relic_object(price=1,data=None):
    """ Return relic's prices and data.

    Args:
        price (int, optional): Relic's Aya price. Defaults to 1.
        data (obj, optional): Relic info. Defaults to None.

    Returns:
        dict: Relic's data
    """
    return {
        "price": price,
        "data": data
    }

def relic_reward_object(chance=0, rarity="", name="", image=""):
    """ Return reward's data.

    Args:
        chance (int, optional): Reward's chance. Defaults to 0.
        rarity (str, optional): Reward's rarity. Defaults to "".
        name (str, optional): Reward's name. Defaults to "".
        image (str, optional): Reward's image url. Defaults to "".
        
    Returns:
        dict: Reward's data
    """
    return{
        "name": name,
        "chance": chance,
        "rarity": rarity,
        "image" : image
    }

