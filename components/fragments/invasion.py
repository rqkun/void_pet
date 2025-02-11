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

        top_left,top_right = st.columns([5,1],vertical_alignment="center")
        top_left.markdown(f"""### Invasion Rewards""",unsafe_allow_html=True)
        invasion_state_reload = top_right.button(AppIcons.SYNC.value,use_container_width=True,type="tertiary",key="invasion_state_reload")

        with st.container(border=True),st.spinner(AppMessages.LOAD_DATA.value):
            data=get_invasions_rewards(data_manage.get_world_state()["invasions"])
            st.markdown(markdowns.invasions_reward_info_md(data),unsafe_allow_html=True)
            if invasion_state_reload:
                st.rerun(scope="fragment")