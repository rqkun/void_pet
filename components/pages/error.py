import streamlit as st

from components import headers

_, mid,_ = st.columns([1,4,1])

with mid:
    headers.basic()
    st.error("Unimplemented Function")