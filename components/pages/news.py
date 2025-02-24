import streamlit as st
from components import custom,markdowns
from datetime import datetime
from config.constants import AppIcons, AppMessages
from utils import data_manage
from utils.tools import format_timedelta

custom.sideNav(8)
custom.reject_url_param()
custom.image_style()
_,middle,_ = st.columns([2,3,2],vertical_alignment="center")

with middle,st.spinner(AppMessages.LOAD_DATA.value,show_time=True,_cache=False):
    news = data_manage.get_news()
if len(news) >0:
    for item in news:
        left,right = st.container(border=True).columns([1,2],vertical_alignment="top")
        left.markdown(markdowns.image_md(item["link"],item["message"],item["imageLink"],caption="collapse",size="100%",border=1,animation=False),unsafe_allow_html=True)
        right.markdown(f"""##### {item["message"]}""")
        date = datetime.strptime(item["date"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
        right.markdown(f""" <i>[{format_timedelta(date)}]<i>""",unsafe_allow_html=True)
        right.link_button("Go to link",item["link"],type="secondary",icon=AppIcons.EXTERNAL.value,use_container_width=True)
else:
    with st.container(border=False):
        st.html("<br><br>")
        custom.empty_result(f"""news.""")