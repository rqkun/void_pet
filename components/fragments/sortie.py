from config.constants import AppIcons, AppMessages
from utils import data_manage
from utils.data_manage import get_sortie_missions


import streamlit as st


@st.fragment()
def show():
    """ Show Sortie's info card. """
    event_state_card = st.container(border=True)
    with event_state_card:
        top_left,top_right = st.columns([5,1],vertical_alignment="center")
        top_left.markdown(f"""### Sortie""",unsafe_allow_html=True)
        sortie_state_reload = top_right.button(AppIcons.SYNC.value,use_container_width=True,type="tertiary",key="sortie_state_reload")
        with st.container(border=True),st.spinner(AppMessages.LOAD_DATA.value):
            data=data_manage.get_world_state()["sortie"]
            sortie_steps, sortie_step_names = get_sortie_missions(data)
            tablist = st.tabs(sortie_step_names)
            for i,tab in enumerate(tablist):
                with tab:
                    sortie_node = sortie_steps[sortie_step_names[i]]
                    st.markdown(f"""Boss: `{data["boss"]}` - `{data["faction"]}` <br>
                                {AppMessages.location_message(sortie_node["node"])}<br>
                                Modifier: `{sortie_node["modifier"]}`
                                """,unsafe_allow_html=True)
            if sortie_state_reload:
                st.rerun(scope="fragment")