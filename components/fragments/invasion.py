from components import markdowns
from config.constants import AppIcons, AppMessages
from utils import data_manage
from utils.data_manage import get_invasions_rewards


import streamlit as st


from datetime import timedelta


@st.fragment(run_every=timedelta(minutes=5))
def show():
    """ Show Invasion rewards card. """
    event_state_card = st.container(border=True)
    with event_state_card:
        st.subheader("""Invasions """)
        with st.expander("Rewards",expanded=True),st.spinner(AppMessages.LOAD_DATA.value):
            try:
                data=get_invasions_rewards(data_manage.get_world_state()["invasions"])
                if data is not None:
                    st.markdown(markdowns.invasions_reward_info_md(data),unsafe_allow_html=True)
                else:
                    st.info('There are currently no invasion', icon=AppIcons.INFO.value)
            except:
                st.warning(f"Error occured",icon=AppIcons.ERROR.value)