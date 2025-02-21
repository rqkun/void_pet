import streamlit as st

@st.dialog("Clear caches")
def clear_cache_dialog():
    """Clear cache confirm dialog."""
    left,right = st.columns([4,1],vertical_alignment="center")
    left.write("Confirm clear caches? This will affect other users.")
    if right.button("Confirm",type="primary",use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun(scope="app")