import streamlit as st
from PIL import Image
from config.constants import AppIcons, AppLabels, AppPages, Warframe
from utils import data_manage
def basic(logo=None):
    """ Add header function. """
    with st.header("",anchor=False):
        left, _,mid,_, right = st.columns([1,3,1,3,1],vertical_alignment="bottom")
        with left:
            if st.button(AppIcons.HOME.value, type="secondary",use_container_width=True):
                st.switch_page(AppPages.HOME.value)
        with right:
            with st.popover(AppIcons.MENU.value,use_container_width=True):
                
                st.page_link(AppPages.AYA.value,
                             label=f"""{AppIcons.AYA.value} {Warframe.AYA.value["name"]}""",
                             use_container_width=True)
                st.page_link(AppPages.BARO.value,
                             label=f"""{AppIcons.BARO.value} {Warframe.BARO.value["name"]}""",
                             use_container_width=True)
                st.page_link(AppPages.VARZIA.value,
                             label="Varzia",
                             icon=AppIcons.VARZIA.value,
                             use_container_width=True)
                st.page_link(AppPages.ISSUE.value,
                             label=AppLabels.REPORT.value,
                             icon=AppIcons.ISSUES.value,
                             use_container_width=True)
                
        with mid:
            if logo is not None:
                cont = st.container(border=False)
                image = Image.open(data_manage.get_image_bytes(logo.value["image"]))
                cont.image(image)
                #cont.html(image_md(url="#",alt=logo.value["name"],source=logo.value["image"],size="50%"))