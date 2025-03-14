import components.markdowns
from config.constants import Warframe
from utils import data_manage


class Card:
    
    def __init__(self,image_url: str,data:dict,metadata=None):
        self.image_url = image_url
        self.data = data
        self.metadata = metadata
        self.type = data.get("category","Unknown")
        self.type_data = ""
        self.wiki_url = Warframe.get_wiki_url(data.get("name","").replace(" ","_"),data.get("type",""))

    def _preload(self):
        hover_md = components.markdowns.misc_info_md(self.data)
        if 'category' in self.data:
            if self.type == "Warframes" or self.type == "Archwing":
                type_data = data_manage.extract_frame_abilities(self.data)
                if type_data:
                    hover_md = components.markdowns.ability_info_md(self.data,type_data)
            elif self.type in ["Primary", "Secondary", "Melee", "Arch-Gun", "Arch-Melee"]:
                type_data = data_manage.extract_craftable_components(self.data)
                if type_data:
                    hover_md = components.markdowns.craftable_info_md(type_data)
            elif self.type == "Mods":
                # type_data = market.get (item name url)
                pass
            elif self.type == "Relics":
                type_data = data_manage.extract_relic_rewards(self.data)
                if type_data:
                    hover_md = components.markdowns.relic_rewards_info_md(type_data)

        self.type_data = hover_md

    def generate(self):
        self._preload()
        image_md = components.markdowns.image_md(self.wiki_url,self.data.get("name",""),self.image_url,caption="visible",size="50px",border=0.5)
        info_md = components.markdowns.hover_md(image_md,self.type_data)
        ducat_md = components.markdowns.price_overlay_md(self.metadata) if self.metadata is not None else ""
        return components.markdowns.card_md(info_md,ducat_md)+ """</div>"""


class WeaponCard(Card):
    def __init__(self,image_url: str,data:dict,metadata=None):
        super().__init__(image_url, data, metadata)


class WarframeCard(Card):
    def __init__(self,image_url: str,data:dict,metadata=None):
        super().__init__(image_url, data, metadata)


class ArchwingCard(Card):
    def __init__(self,image_url: str,data:dict,metadata=None):
        super().__init__(image_url, data, metadata)


class SentinelCard(Card):
    def __init__(self,image_url: str,data:dict,metadata=None):
        super().__init__(image_url, data, metadata)

class ModCard(Card):
    def __init__(self,image_url: str,data:dict,metadata=None):
        super().__init__(image_url, data, metadata)


class RelicCard(Card):
    def __init__(self,image_url: str,data:dict,metadata=None):
        super().__init__(image_url, data, metadata)
        self.wiki_url = Warframe.get_wiki_url(data.get("name","").replace(" Intact", "").replace(" ","_"),data.get("type",""))


def match_type(data:dict,image_url:str,metadata:dict) -> Card:
    type = data.get("category","Unknown")
    if type == "Warframes":
        return WarframeCard(image_url,data=data,metadata=metadata)
    elif type == "Archwing":
        return ArchwingCard(image_url,data=data,metadata=metadata)
    elif type == "Sentinels":
        return SentinelCard(image_url,data=data,metadata=metadata)
    elif type == "Mods":
        return ModCard(image_url,data=data,metadata=metadata)
    elif type == "Relics":
        return RelicCard(image_url,data=data,metadata=metadata)
    elif type in ["Primary", "Secondary", "Melee", "Arch-Gun", "Arch-Melee"]:
        return WeaponCard(image_url,data=data,metadata=metadata)
    else:
        return Card(image_url,data=data,metadata=metadata)

