import json
import streamlit as st

from config.constants import AppExports, Warframe
@st.cache_data(ttl="1d", show_spinner=False)
def open_cosmetics():
    """ Read Cosmetic's Json info.

    Returns:
        dict: Json of Cosmetics info.
    """
    with open(AppExports.COSMETICS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportCustoms"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_drones():
    """ Read Drone's Json info.

    Returns:
        dict: Json of Drones info.
    """
    with open(AppExports.DRONES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportDrones"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_flavours():
    """ Read Flavour's Json info.

    Returns:
        dict: Json of Flavours info.
    """
    with open(AppExports.FLAVOURS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportFlavour"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_bundles():
    """ Read Bundle's Json info.

    Returns:
        dict: Json of Bundles info.
    """
    with open(AppExports.BUNDLES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportFusionBundles"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_gears():
    """ Read Gear's Json info.

    Returns:
        dict: Json of Gears info.
    """
    with open(AppExports.GEARS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportGear"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_keys():
    """ Read Key's Json info.

    Returns:
        dict: Json of Quest Keys info.
    """
    with open(AppExports.KEYS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportKeys"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_manifest():
    """ Read Manifest's Json info.

    Returns:
        dict: Json of Image Manifest info.
    """
    with open(AppExports.MANIFEST.value, "r", encoding="utf-8") as file:
        return json.load(file)["Manifest"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_recipes():
    """ Read Recipe's Json info.

    Returns:
        dict: Json of Recipes info.
    """
    with open(AppExports.RECIPES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportRecipes"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_regions():
    """ Read Region's Json info.

    Returns:
        dict: Json of Regions info.
    """
    with open(AppExports.REGIONS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportRegions"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_relic_arcane():
    """ Read Relic & Arcane Json info.

    Returns:
        dict: Json of Relics and Arcanes info.
    """
    with open(AppExports.RELIC_ARCANE.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportRelicArcane"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_resources():
    """ Read Resource's Json info.

    Returns:
        dict: Json of Resources info.
    """
    with open(AppExports.RESOURCES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportResources"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_sentiels():
    """ Read Sentiel's Json info.

    Returns:
        dict: Json of Sentinels info.
    """
    with open(AppExports.SENTIELS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportSentinels"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_sorties():
    """ Read Sorties Reward's Json info.

    Returns:
        dict: Json of Sortie Rewards info.
    """
    with open(AppExports.SORTIES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportSortieRewards"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_upgrades():
    """ Read Upgrade's Json info.

    Returns:
        dict: Json of Mods and Upgrades info.
    """
    with open(AppExports.UPGRADES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportUpgrades"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_warframes():
    """ Read Frame's Json info.

    Returns:
        dict: Json of Warframes info.
    """
    with open(AppExports.WARFRAMES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportWarframes"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_weapons():
    """ Read Weapon's Json info.

    Returns:
        dict: Json of Weapons info.
    """
    with open(AppExports.WEAPONS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportWeapons"]

