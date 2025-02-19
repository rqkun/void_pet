from config.constants import AppIcons, AppMessages, Warframe
from utils import data_manage, tools


import streamlit as st


from datetime import timedelta


@st.fragment(run_every=timedelta(minutes=1))
def show():
    """ Show event's card that update every minute. """
    event_state_card = st.container(border=False)
    with event_state_card:

        st.subheader("""Events """)
        events_info = st.container(border=True)
        with events_info, st.spinner(AppMessages.LOAD_DATA.value):
            data=data_manage.get_ongoing_events()
            if data is not None:
                for event in data:
                    left,right = events_info.columns([8,1],vertical_alignment="bottom")
                    right.link_button(AppIcons.EXTERNAL.value,url=Warframe.get_wiki_url(event["description"]),use_container_width=True,type="tertiary")
                    node = event["victimNode"] if "victimNode" in event else event["node"]
                    percentage = tools.calculate_percentage_time(event["activation"],event["expiry"])
                    left.progress(percentage,f"""{event["description"]} | {node}""")
                        
            else:
                events_info.info('There are currently no events', icon=AppIcons.INFO.value)