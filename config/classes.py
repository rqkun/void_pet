from typing import Literal


class RivenSearchParams:
    def __init__(self, weapon_url_name, buyout_policy=None, positive_stats=None,
                 negative_stats=None, operation=None, re_rolls_min=None,
                 re_rolls_max=None, polarity=None, type=None):
        self.identifier = weapon_url_name
        self.buyout_policy = buyout_policy
        self.positive_stats = positive_stats or []
        self.negative_stats = negative_stats or []
        self.operation = operation
        self.re_rolls_min = re_rolls_min
        self.type = ""
        self.re_rolls_max = re_rolls_max
        self.polarity = polarity

    def to_query_string(self):
        filters = []
        if self.buyout_policy:
            filters.append(f"buyout_policy={self.buyout_policy}")
        if self.positive_stats:
            positive_query = ",".join(self.positive_stats)
            filters.append(f"positive_stats={positive_query}")
        if self.negative_stats:
            negative_query = ",".join(self.negative_stats)
            filters.append(f"negative_stats={negative_query}")
        if self.operation:
            filters.append(f"operation={self.operation}")
        if self.re_rolls_min is not None:
            filters.append(f"re_rolls_min={self.re_rolls_min}")
        if self.re_rolls_max is not None:
            filters.append(f"re_rolls_max={self.re_rolls_max}")
        if self.polarity:
            filters.append(f"polarity={self.polarity}")
        return "&".join(filters)
class WarframeStatusSearchParams:
    def __init__(self, identifier, by, type=Literal["items","weapons","warframes"],only=None, remove=None):
        self.identifier = identifier
        self.by = by
        self.type = type
        self.only = only or []
        self.remove = remove or []

    def to_query_string(self):
        filters = []
        if self.by:
            filters.append(f"by={self.by}")
        if self.only:
            only_query = ",".join(self.only)
            filters.append(f"only={only_query}")
        if self.remove:
            remove_query = ",".join(self.remove)
            filters.append(f"remove={remove_query}")
        return "&".join(filters)