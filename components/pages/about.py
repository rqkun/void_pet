from components import custom
import streamlit_antd_components as sac
import streamlit as st

from config.constants import AppIcons, AppMessages
from utils import data_manage


custom.sideNav(6)
custom.reject_url_param()

st.subheader(f"""{AppIcons.INFO.value} About the Page""")
st.markdown("""<font style="color:gray">A Python-based Streamlit application that utilizes the Warframe Stat API\
    and the Warframe.market API to provide up-to-date information on in-game events,\
        vendor inventories, and market pricing.</font>"""
        ,unsafe_allow_html=True)
expander = st.expander("Admin")
with expander:
    left,right = st.columns([4,1])
    text = left.text_input("text_input",type='password',placeholder='Enter passkey...',label_visibility="collapsed")
    submit = right.button("Update",type="primary",use_container_width=True,icon=AppIcons.SYNC.value)
st.subheader(":material/functions: Features")
st.markdown("""<font style="color:gray">
        &middot; In-Game Event Tracking <br>
        &middot; Vendor Inventory Lookup <br>
        &middot; Market Price Checkup <br>
        &middot; News Updates <br>
        &middot; Riven mods Auction Checkup <br>
        &middot; Discord Bot Integration</font>
        """,unsafe_allow_html=True)
st.subheader(":material/link: Links")
sac.buttons([
    sac.ButtonsItem(label="warframe.market/docs", icon=sac.AntIcon(name='ApiOutlined'), href="https://warframe.market/api_docs"),
    sac.ButtonsItem(label="warframestat.us/docs", icon=sac.AntIcon(name='ApiOutlined'), href="https://docs.warframestat.us/"),
    sac.ButtonsItem(label='Github',color="gray", icon='github', href="https://github.com/rqkun/void_pet"),
    sac.ButtonsItem(label='Invite Me!',color="cyan", icon='discord', href="https://discord.com/oauth2/authorize?client_id=1047432559388282900"),
],index=None, align='left',size="sm", color='#4682b4', variant='filled', gap='lg',use_container_width=True)

if submit:
    with expander, st.spinner(AppMessages.LOAD_DATA.value,show_time=True):
        try:
            data_manage.update_exports(text)
        except Exception as e:
            expander.error(e.args[0],icon=AppIcons.ERROR.value)