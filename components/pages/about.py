import lzma
import re
import requests
import os
import json
import urllib
import logging
from supabase import create_client, Client
import streamlit as st

from datasources import warframe_export

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if st.button("Run"):
    logging.info("Starting JSON upload process.")
    try:
        warframe_export.process_manifest()
        logging.info("All files uploaded successfully.")
    except Exception as e:
        logging.error(f"Error during upload process: {e}")