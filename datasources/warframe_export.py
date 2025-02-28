from enum import Enum
import json
import streamlit as st


@st.cache_data(ttl="7d", show_spinner=False)
def export_request(item:Enum):
    """_summary_

    Args:
        item (Enum): Included path and object key.\n
            "DRONES": "Drones",\n
            "COSMETICS": "Cosmetics",\n
            "FLAVOURS": "Colors",\n
            "BUNDLES": "Bundles",\n
            "GEARS": "Gears",\n
            "KEYS": "Quest Keys",\n
            "MANIFEST": "Image paths",\n
            "RECIPES": "Recipes",\n
            "REGIONS": "Regions",\n
            "RELIC_ARCANE": "Relics & Arcanes",\n
            "RESOURCES": "Materials",\n
            "SENTINELS": "Sentinels",\n
            "SORTIES": "Sortie rewards",\n
            "NIGHTWAVE": "Nightwaves",\n
            "RAILJACK": "Railjack",\n
            "INTRINSICS": "Intrinsics",\n
            "UPGRADES": "Mods",\n
            "MOD_SET": "Mod sets",\n
            "AVIONICS": "Avionics",\n
            "FOCUS_UPGRADES": "Operator/Drifter Focus",\n
            "WARFRAMES": "Warframes",\n
            "ABILITIES": "Abilities",\n
            "WEAPONS": "Weapons",\n
            "RAILJACK_WEAPONS": "Railjack weapons",\n
            "OTHER": "Other"\n

    Returns:
        dict: Raw json data of the export.
    """
    # request_object = requests.get(f"""{st.secrets.host.url}/app/{item["path"]}""")
    # raise_detailed_error(request_object)
    # return request_object.json()[item["object_name"]]
    with open(item["path"], "r", encoding="utf-8") as file:
        return json.load(file)[item["object_name"]]