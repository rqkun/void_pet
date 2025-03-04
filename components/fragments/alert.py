from components import markdowns
from config.constants import AppIcons, AppMessages
from utils import data_manage, tools
from utils.tools import format_timedelta


import streamlit as st


from datetime import datetime, timedelta


@st.fragment(run_every=timedelta(minutes=1))
def show():
    """Show alert's card that update every minute. """
    alert_state_card = st.container(border=False)
    with alert_state_card:

        
        st.subheader("""Alerts """)

        alert_info = st.container(border=True)
        with alert_info, st.spinner(AppMessages.LOAD_DATA.value):
            data=data_manage.get_alerts_data()
            
            if data is None:
                alert_info.info('There are currently no alerts', icon=AppIcons.INFO.value)
            else:   
                count = 0
                for alert in data:
                    try:
                        if alert["active"] == True:
                            percentage_completed = tools.calculate_percentage_time(start=alert["activation"],end=alert["expiry"])
                            if percentage_completed < 1:
                                count += 1
                                left,right = alert_info.columns([3,1],vertical_alignment="bottom")
                                with right.popover(AppIcons.INFO.value,use_container_width=True):
                                    time = format_timedelta(datetime.strptime(alert["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today(),day=True)
                                    info_md = markdowns.alerts_reward_info_md(data_manage.get_alert_reward(alert))
                                    st.markdown(markdowns.event_alert_card_md(alert["mission"]["type"],time,info_md),unsafe_allow_html=True)
                                left.progress(percentage_completed,f"""{alert["mission"]["node"]}""")
                    except:
                        st.warning(f"Error occured",icon=AppIcons.ERROR.value)
                if count <1:
                    alert_info.info('There are currently no alerts', icon=AppIcons.INFO.value)