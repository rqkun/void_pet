from enum import Enum
import json
import logging
import lzma
import re
import requests
import streamlit as st
import urllib

from supabase import Client, create_client

from config.constants import Warframe
from utils.api_services import raise_detailed_error

@st.cache_data(ttl="30d", show_spinner=False)
def export_open(item:Enum):
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
    try:
        manifest_files = get_index_file()
        for file in manifest_files:
            if item["path"] in file:
                file = file.replace(" ", "")
                logging.info(f"Processing file: {file}")
                encoded_name = urllib.parse.quote(file, safe="")
                url = f"""{Warframe.PUBLIC_EXPORT_API.value["api"]}/Manifest/{encoded_name}"""

                response = requests.get(url)
                raise_detailed_error(response)

                cleaned_json = re.sub(r'[\x00-\x1f\x7f]', '', response.text)
                data = json.loads(cleaned_json)
                # json_data = json.dumps(data, indent=4)

                return data[item["object_name"]]

    except requests.exceptions.RequestException as origin_error:  # This is the correct syntax
        logging.warning(f"""Failed request object {item["path"]} in Origin System({origin_error.args[0]}). Trying to read from s3.""")
        try:
            request_object = requests.get(f"""{st.secrets["supabase"]["SUPABASE_BUCKET_URL"]}{item["path"]}""")
            raise_detailed_error(request_object)
            return request_object.json()[item["object_name"]]
        except requests.exceptions.RequestException as s3_error:
            logging.warning(f"""Failed request object {item["path"]} in Origin System({s3_error.args[0]}). Trying to read from local backup.""")
            try:
                with open(f"""static/exports/{item["path"]}""", "r", encoding="utf-8") as file:
                    return json.load(file)[item["object_name"]]
            except Exception as e:
                logging.error(f"""Failed to read object {item["path"]}. Error: {s3_error.args[0]}""")
                return None

@st.cache_data(ttl="30d", show_spinner=False)
def get_index_file():
    """Fetch and decompress the manifest file."""
    logging.info("Fetching manifest file.")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    request_ref = Warframe.PUBLIC_EXPORT_API.value["index"]
    
    response = requests.get(request_ref,headers=headers)
    response.raise_for_status()

    logging.info("Decompressing manifest file.")
    buf = bytearray(response.content)
    buf[5:13] = b'\xff\xff\xff\xff\xff\xff\xff\xff'
    decompressed_data = lzma.decompress(buf, format=lzma.FORMAT_ALONE)
    
    return decompressed_data.decode("utf-8", errors='ignore').split("\r\n")


@st.cache_resource(ttl="30d",show_spinner=False)
def get_supabase_client():
    SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase


def update_exports():
    """Fetch and upload JSON files to Supabase."""
    logging.info("Processing manifest files.")
    manifest_files = get_index_file()
    supabase = get_supabase_client()
    BUCKET_NAME = "json-files"
    for file in manifest_files:
        file = file.replace(" ", "")
        logging.info(f"Processing file: {file}")
        encoded_name = urllib.parse.quote(file, safe="")
        url = f"""{Warframe.PUBLIC_EXPORT_API.value["api"]}/Manifest/{encoded_name}"""

        response = requests.get(url)
        response.raise_for_status()

        cleaned_json = re.sub(r'[\x00-\x1f\x7f]', '', response.text)
        data = json.loads(cleaned_json)
        json_data = json.dumps(data, indent=4)
        file_name = file.split(".json")[0] + ".json"

        supabase.storage.from_(BUCKET_NAME).upload(file_name, json_data.encode('utf-8'), {"content-type": "application/json","upsert":"true"})
        logging.info(f"File '{file_name}' uploaded successfully to bucket '{BUCKET_NAME}'.")
    logging.info(f"All files successfully updated.")
        
        
