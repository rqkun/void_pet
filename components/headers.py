import streamlit as st

from config.constants import AppIcons, AppLabels, AppPages, Warframe
def basic(logo=None):
    """ Add header function. """
    with st.header(""):
        left, _,mid,_, right = st.columns([1,2,1,2,1],vertical_alignment="bottom")
        with left:
            if st.button(AppIcons.HOME.value,use_container_width=True):
                st.switch_page(AppPages.HOME.value)
        with right:
            with st.popover(AppIcons.MENU.value,use_container_width=True,):
                
                st.page_link(AppPages.VARZIA.value,
                             label=Warframe.VARZIA.value["name"],
                             icon=AppIcons.VARZIA.value,
                             use_container_width=True)
                st.page_link(AppPages.ISSUE.value,
                             label=AppLabels.REPORT.value,
                             icon=AppIcons.ISSUES.value,
                             use_container_width=True)
        with mid:
            if logo is not None:
                cont = st.container(border=False)
                cont.html(f"""<img alt="logo" style="width:50%;display: block;margin-left: auto;margin-right: auto;width: 50px;" src="{logo}"/>""")