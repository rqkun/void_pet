import streamlit as st

from utils.icons import AppIcons
def basic(logo=None):
    """ Add header function. """
    with st.header(""):
        left, _,mid,_, right = st.columns([2,2,1,2,2],vertical_alignment="bottom")
        with left:
            if st.button("Home",use_container_width=True,icon=AppIcons.HOME.value):
                st.switch_page("views/home.py")
        with right:
            with st.popover("Menu",use_container_width=True, icon=AppIcons.MENU.value):
                
                st.page_link("views/varzia.py",
                             label="Varzia",
                             icon=AppIcons.MENU.value,
                             use_container_width=True)
        with mid:
            if logo is not None:
                cont = st.container(border=False)
                cont.html(f"""<img alt="logo" style="width:100%;" src="{logo}"/>""")