import streamlit as st

from utils import headers

_, mid,_ = st.columns([1,4,1])

with mid:
    headers.basic()
    st.error("Unimplemented Function")