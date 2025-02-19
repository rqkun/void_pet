from components import markdowns
from config.constants import AppIcons, AppMessages, Warframe
from utils import data_manage, tools


import streamlit as st


from datetime import datetime, timedelta


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
                    try:
                        left,right = events_info.columns([3,1],vertical_alignment="bottom")
                        # right.link_button(AppIcons.EXTERNAL.value,url=Warframe.get_wiki_url(event["description"]),use_container_width=True,type="tertiary")
                        node = event["victimNode"] if "victimNode" in event else event["node"]
                        percentage = tools.calculate_percentage_time(event["activation"],event["expiry"])
                        time = tools.format_timedelta(datetime.strptime(event["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today(),day=True)
                        # info_md = markdowns.alerts_reward_info_md(data_manage.get_alert_reward(alert))
                        rewards = data_manage.get_event_rewards(event)
                        event["description"] = event["description"].replace("Operation: ", "")
                        left.progress(percentage,f"""{event["description"]}""")
                        pop = right.popover(AppIcons.INFO.value,use_container_width=True)
                        pop.markdown(markdowns.stats_info_md(node,time,markdowns.event_info_md(event,rewards)),unsafe_allow_html=True)
                    except:
                        st.warning(f"Error occured",icon=AppIcons.ERROR.value)
            else:
                events_info.info('There are currently no events', icon=AppIcons.INFO.value)