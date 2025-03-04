from components import markdowns
from config.constants import AppIcons, AppMessages
from utils import data_manage
from utils.tools import format_timedelta


import streamlit as st


from datetime import datetime, timedelta

@st.fragment(run_every=timedelta(days=1))
def show():
    """Show Invasion rewards card. """
    event_state_card = st.container(border=True)
    with event_state_card:
        st.markdown(f"""### News {AppIcons.NEWS.value}""")
        with st.expander("Expands",expanded=True),st.spinner(AppMessages.LOAD_DATA.value,show_time=True,_cache=False):
            news = data_manage.get_news()
            if len(news)>0:
                for item in news:
                    left,right = st.container(border=True).columns([1,2],vertical_alignment="top")
                    left.markdown(markdowns.image_md(item["link"],item["message"],item["imageLink"],caption="collapse",size="100%",border=1,animation=False),unsafe_allow_html=True)
                    right.markdown(f"""##### {item["message"]}""")
                    date = datetime.strptime(item["date"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
                    right.markdown(f"""<i>[{format_timedelta(date)}]<i>""",unsafe_allow_html=True)
                    right.link_button("Go to link",item["link"],type="secondary",icon=AppIcons.EXTERNAL.value,use_container_width=True)
            else:
                st.info('There are currently no news', icon=AppIcons.INFO.value)