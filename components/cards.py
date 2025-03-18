import components.markdowns
from config.constants import Warframe
from utils import data_manage


class Card:
    
    def __init__(self, image_url: str, data: dict, metadata=None):
        self.image_url = image_url
        self.data = data
        self.metadata = metadata
        self.type = data.get("category", "Unknown")
        self._hover_md = None
        self._type_data = None
        
        name = data.get("name", "")
        formatted_name = get_formatted_name(name)
        self.wiki_url = Warframe.get_wiki_url(formatted_name, data.get("type", ""))

    @property
    def type_data(self):
        if self._hover_md is None:
            self._load_data()
        return self._hover_md
    
    def _load_data(self):
        self._hover_md = components.markdowns.misc_info_md(self.data)
        
        if 'category' in self.data:
            if self.type == "Warframes" or self.type == "Archwing":
                type_data = data_manage.extract_frame_abilities(self.data)
                if type_data:
                    self._hover_md = components.markdowns.ability_info_md(self.data, type_data)
            # Rest of the conditions...
            elif self.type in ["Primary", "Secondary", "Melee", "Arch-Gun", "Arch-Melee"]:
                type_data = data_manage.extract_craftable_components(self.data)
                if type_data:
                    self._hover_md = components.markdowns.craftable_info_md(type_data)
            elif self.type == "Mods":
                # type_data = market.get (item name url)
                pass
            elif self.type == "Relics":
                type_data = data_manage.extract_relic_rewards(self.data)
                if type_data:
                    self._hover_md = components.markdowns.relic_rewards_info_md(type_data)


    def generate(self):
        image_md = components.markdowns.image_md(self.wiki_url, self.data.get("name", ""), self.image_url, caption="visible", size="50px", border=0.5)
        info_md = components.markdowns.hover_md(image_md, self.type_data)  # This will trigger lazy loading
        ducat_md = components.markdowns.price_overlay_md(self.metadata) if self.metadata is not None else ""
        return components.markdowns.card_md(info_md, ducat_md) + """</div>"""
        
    @classmethod
    def create(cls, data: dict, image_url: str, metadata: dict = None):
        """Factory method to create appropriate card instance"""
        card = cls(image_url, data, metadata)
        
        # Special handling for relics
        if data.get("category") == "Relics":
            card.wiki_url = Warframe.get_wiki_url(
                get_formatted_name(data.get("name", ""),remove_intact=True),
                data.get("type", "")
            )
            
        return card

def match_type(data: dict, image_url: str, metadata: dict) -> Card:
    return Card.create(data, image_url, metadata)

def get_formatted_name(name, remove_intact=False):
    """Helper function to format names consistently"""
    if remove_intact:
        name = name.replace(" Intact", "")
    return name.replace(" ", "_")
