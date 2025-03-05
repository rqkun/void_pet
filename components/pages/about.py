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


if st.button("Run"):
    logging.info("Starting JSON upload process.")
    try:
        st.write(get_manifest())
        logging.info("All files uploaded successfully.")
    except Exception as e:
        logging.error(f"Error during upload process: {e}")