from components import markdowns
from config.constants import AppIcons, AppMessages
from utils import data_manage


import streamlit as st


from datetime import timedelta


@st.fragment(run_every=timedelta(minutes=1))
def show():
    """Show world state's info card. """
    world_state_card = st.container(border=True)
    with world_state_card:
        st.subheader("""World""")
        with st.container(border=True), st.spinner(AppMessages.LOAD_DATA.value):
            try:
                data=data_manage.get_cycles()
                st.markdown(markdowns.world_clock_md(data),unsafe_allow_html=True)
            except:
                st.warning(f"Error occured",icon=AppIcons.ERROR.value)