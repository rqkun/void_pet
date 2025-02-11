import datasources.warframe_status
from components import cards
from config.constants import AppIcons, AppLabels, AppMessages, AppPages, Warframe
from utils.tools import check_disable, format_timedelta


import streamlit as st


from datetime import datetime, timedelta


@st.fragment(run_every=timedelta(minutes=1))
def show():
    """ Show varzia's card that update every minute. """
    varzia_card = st.container(border=True)
    with varzia_card:

        top_left,top_right = st.columns([5,1],vertical_alignment="center")
        top_left.markdown(f"""### {Warframe.VARZIA.value["name"]}""",unsafe_allow_html=True)
        varzia_reload = top_right.button(AppIcons.SYNC.value,use_container_width=True,type="tertiary",key="varzia_reload2")

        varzia_info_card = st.container(border=True)
        with varzia_info_card, st.spinner(AppMessages.LOAD_DATA.value):
            left,right = varzia_info_card.columns([2,1])
            varzia_info = left.container(border=False)
            varzia_img = right.container(border=True)
            with varzia_img:
                cards.prep_image(Warframe.VARZIA)
            with varzia_info:
                data=datasources.warframe_status.vault_traider_request()
                date = datetime.strptime(data["activation"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
                start_date = format_timedelta(date)
                end_date = format_timedelta(datetime.strptime(data["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today())

                if data["active"]:
                    st.write(AppMessages.end_time_message(end_date))
                else:
                    st.write(AppMessages.start_time_message(start_date))

                if varzia_reload:
                    if 'varzia_wares' in st.session_state:
                        del st.session_state["varzia_wares"]
                    if 'varzia_wares_detail' in st.session_state:
                        del st.session_state["varzia_wares_detail"]
                    st.rerun(scope="fragment")
            if varzia_info.button(AppLabels.BROWSE.value,use_container_width=True,disabled=check_disable(data),help=AppMessages.VARZIA_BROWSE.value,key="varzia_browse",type="primary"):
                st.switch_page(AppPages.VARZIA.value)