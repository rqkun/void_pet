import lzma
import re
import requests
import os
import json
import urllib
import logging
from supabase import create_client, Client
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Initialize Supabase client
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "json-files"

def get_manifest():
    """Fetch and decompress the manifest file."""
    try:
        logging.info("Fetching manifest file.")
        request_ref = "https://origin.warframe.com/PublicExport/index_en.txt.lzma"
        
        response = requests.get(request_ref)
        response.raise_for_status()

        logging.info("Decompressing manifest file.")
        decompressed_data = lzma.decompress(response.content)
        return decompressed_data.decode("utf-8", errors='ignore').split("\r\n")
    except (requests.RequestException, lzma.LZMAError) as e:
        logging.error(f"Error fetching or decompressing manifest: {e}")
        raise ValueError(f"Error fetching or decompressing manifest: {e}")


def process_manifest():
    """Fetch and upload JSON files to Supabase."""
    logging.info("Processing manifest files.")
    manifest_files = get_manifest()

    for file in manifest_files:

        try:
            file = file.replace(" ", "")
            logging.info(f"Processing file: {file}")
            encoded_name = urllib.parse.quote(file, safe="")
            url = f"http://content.warframe.com/PublicExport/Manifest/{encoded_name}"

            response = requests.get(url)
            response.raise_for_status()

            # Clean and parse JSON
            cleaned_json = re.sub(r'[\x00-\x1f\x7f]', '', response.text)

            # Parse the JSON data
            data = json.loads(cleaned_json)
            json_data = json.dumps(data, indent=4)
            # Ensure proper filename
            file_name = file.split(".json")[0] + ".json"

            # Upload to Supabase
            try:
                supabase.storage.from_(BUCKET_NAME).upload(file_name, json_data.encode('utf-8'), {"content-type": "application/json","upsert":"true"})
                logging.info(f"File '{file_name}' uploaded successfully to bucket '{BUCKET_NAME}'.")
            except Exception as e:
                logging.error(e.args)


        except (requests.RequestException, json.JSONDecodeError) as e:
            logging.error(f"Error processing {file}: {e}")



if __name__ == "__main__":
    logging.info("Starting JSON upload process.")
    try:
        process_manifest()
        logging.info("All files uploaded successfully.")
    except Exception as e:
        logging.error(f"Error during upload process: {e}")