import streamlit as st
from components import custom,markdowns
from datetime import datetime
from config.constants import AppIcons
from utils import data_manage
from utils.tools import format_timedelta

custom.sideNav(5)
custom.hover_effect()

news = data_manage.get_news()

for item in news:
    left,right = st.container(border=True).columns([1,2],vertical_alignment="top")
    
    left.markdown(markdowns.image_md(item["link"],item["message"],item["imageLink"],caption="hidden",size="100%",animation=False),unsafe_allow_html=True)
    right.markdown(f"""##### {item["message"]}""")
    date = datetime.strptime(item["date"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
    right.markdown(f""" <i>[{format_timedelta(date)}]<i>""",unsafe_allow_html=True)
    right.link_button("Go to link",item["link"],type="secondary",icon=AppIcons.EXTERNAL.value,use_container_width=True)