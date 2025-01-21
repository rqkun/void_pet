import json
import streamlit as st

from config.constants import AppExports
@st.cache_data(ttl="1d", show_spinner=False)
def open_cosmetics():
    with open(AppExports.COSMETICS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportCustoms"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_drones():
    with open(AppExports.DRONES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportDrones"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_flavours():
    with open(AppExports.FLAVOURS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportFlavour"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_bundles():
    with open(AppExports.BUNDLES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportFusionBundles"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_gears():
    with open(AppExports.GEARS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportGear"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_keys():
    with open(AppExports.KEYS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportKeys"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_manifest():
    with open(AppExports.MANIFEST.value, "r", encoding="utf-8") as file:
        return json.load(file)["Manifest"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_recipes():
    with open(AppExports.RECIPES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportRecipes"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_regions():
    with open(AppExports.REGIONS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportRegions"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_relic_arcane():
    with open(AppExports.RELIC_ARCANE.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportRelicArcane"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_resources():
    with open(AppExports.RESOURCES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportResources"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_sentiels():
    with open(AppExports.SENTIELS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportSentinels"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_sorties():
    with open(AppExports.SORTIES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportSortieRewards"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_upgrades():
    with open(AppExports.UPGRADES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportUpgrades"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_warframes():
    with open(AppExports.WARFRAMES.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportWarframes"]

@st.cache_data(ttl="1d", show_spinner=False)
def open_weapons():
    with open(AppExports.WEAPONS.value, "r", encoding="utf-8") as file:
        return json.load(file)["ExportWeapons"]