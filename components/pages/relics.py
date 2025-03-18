import streamlit as st
from components import custom
from components.cards import Card
from config.constants import AppIcons, AppMessages
from utils import data_manage

def store_resurgent():
    return data_manage.get_resurgent_relics()

def store_relics():
    return data_manage.get_relics()

def store_primes():
    rewards = data_manage.get_relic_rewards()
    return rewards

custom.sideNav(5)
custom.reject_url_param()
custom.image_style()
custom.card_style()

_,middle,_ = st.columns([2,3,2],vertical_alignment="center")
with middle,st.spinner(AppMessages.LOAD_DATA.value,show_time=True,_cache=False):
    primes = store_primes()
    relics = store_relics()
    resurgents = store_resurgent()

status_placeholder = st.empty()
search_form = st.expander("Search",expanded=True,icon=AppIcons.INSPECT.value).form("relic_search_form",clear_on_submit=False,border=False)

left_top,right_top=search_form.columns([7,1],vertical_alignment="bottom")

rewards = left_top.multiselect(
    "Select",
    options= primes,
    label_visibility="collapsed",
    placeholder="Select up to 3 reward(s)",
    max_selections=3,
    format_func= lambda x: x.replace(" Prime",""),
)

left,right=search_form.columns([4,1],vertical_alignment="bottom")

submit = right.form_submit_button("Search",use_container_width=True,icon=AppIcons.INSPECT.value,type="primary")
types = left.segmented_control("Type",
                                ["Axi","Neo","Meso","Lith","Requiem"],
                                selection_mode="multi",
                                default=None,
                                format_func= lambda x: x.title())
adv_setting = right_top.popover(AppIcons.SETTING.value,use_container_width=True)
with adv_setting:
    vaulted = st.checkbox("Vaulted")
    non_vault = st.checkbox("Non-Vaulted")
    resurgent = st.checkbox("Resurgent")

container = search_form.container(border=False)
result_container = st.container(border=False)

if submit:
    with container, st.spinner("",show_time=True):
        tags = [vaulted,non_vault]
        if "relics" in st.session_state:
            del st.session_state.relics
        st.session_state.relics = data_manage.filter_relic(relics,rewards,types,tags,resurgent_data=(resurgents if resurgent else None))

if "relics" in st.session_state:
    if st.session_state.relics is None or len(st.session_state.relics) ==0:
        st.write(" ")
        custom.empty_result(f"""relics with current filters.""")
    else:
        current_relics = st.session_state.relics
        start_idx, end_idx, items_per_row = custom.paginations(len(current_relics),3,items_per_row=6)
        view_relics = current_relics[start_idx:end_idx]
        _,middle,_ = st.columns([3,2,3],vertical_alignment="center")

        with middle,st.spinner("",show_time=True,_cache=False):
            for item in view_relics:
                item["image"] = data_manage.get_image_url(item["uniqueName"])
                item["html"] = Card(data=item, image_url=item["image"]).generate()
        list_col = st.columns(items_per_row)
        start_idx = 0
        custom.varzia_style()
        for idx, item in enumerate(iterable=view_relics[start_idx:]):
            with list_col[idx%items_per_row]:
                if item is not None:
                    st.markdown(item["html"],unsafe_allow_html=True)
