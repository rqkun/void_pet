from components import markdowns
from config.constants import AppIcons, AppMessages
from utils import data_manage, tools
from utils.tools import format_timedelta


import streamlit as st


from datetime import datetime, timedelta


@st.fragment(run_every=timedelta(minutes=1))
def show():
    """ Show event's card that update every minute. """
    alert_state_card = st.container(border=True)
    with alert_state_card:

        top_left,top_right = st.columns([5,1],vertical_alignment="center")
        top_left.markdown(f"""### Alerts """,unsafe_allow_html=True)
        alert_state_reload = top_right.button(AppIcons.SYNC.value,use_container_width=True,type="tertiary",key="alert_state_reload")

        alert_info = st.container(border=True)
        with alert_info, st.spinner(AppMessages.LOAD_DATA.value):
            data=data_manage.get_alerts_data()
            if data is not None:
                for alert in data:
                    if alert["active"] == True:

                        percentage_completed = tools.calculate_percentage_time(start=alert["activation"],end=alert["expiry"])
                        if percentage_completed < 1:
                            left,right = alert_info.columns([3,1],vertical_alignment="bottom")
                            with right.popover(AppIcons.INFO.value,use_container_width=True):
                                st.markdown(f"""##### {alert["mission"]["type"]} \
                                    - `{format_timedelta(datetime.strptime(alert["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today(),day=False)}`\
                                        """)
                                st.markdown(f"""<span><i> Reminder, Steelpath rewards might be different.</i></span>""",unsafe_allow_html=True)
                                st.container(border=True).markdown(markdowns.alerts_reward_info_md(data_manage.get_alert_reward(alert)),unsafe_allow_html=True)
                            left.progress(percentage_completed,f"""{alert["mission"]["node"]}""")
            else:
                alert_info.info('There are currently no alerts', icon=AppIcons.INFO.value)
            if alert_state_reload:
                st.rerun(scope="fragment")