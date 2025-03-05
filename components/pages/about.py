import logging
import streamlit as st
import utils.local_manifest_update as update

if st.button("Run"):
    logging.info("Starting JSON upload process.")
    try:
        update()
        logging.info("All files uploaded successfully.")
    except Exception as e:
        logging.error(f"Error during upload process: {e}")