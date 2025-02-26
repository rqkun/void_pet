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