import math
import streamlit as st
from config.classes.exceptions import ResetBotFlag
from config.constants import AppIcons, AppPages
import streamlit_antd_components as sac
from streamlit_option_menu import option_menu

def sideNav(current_idx):
    """Custom Sidebar navigation.

    Args:
        current_idx (int): current page index.
        logo (enum, optional): current page logo. Defaults to Warframe.AYA.value.
    """
    option_maping = ["Home", "Void", "Vault", 'Market', 'Rivens','Relics','Statistics','About']
    with st.sidebar:
        st.markdown("""<style>.st-emotion-cache-kgpedg {padding: calc(1.375rem) 1.5rem 0rem; margin:-1rem 0 -1rem 0;}</style>""",unsafe_allow_html=True)
        selection = option_menu(None, option_maping,
                        icons=['house', 'arrow-repeat', "droplet-fill", 'cart3','dice-6','browser-firefox','bar-chart-fill','discord'], 
                        menu_icon=None, default_index=current_idx, orientation="vertical",
                        styles={
                            "container": {"padding": "0!important", "background-color": "#262730","display":"flex",},
                            "icon": {"color": "white", "font-size": "20px"},

                            "nav-item":{
                                "min-height":"2.5rem",
                                "display":" flex",
                                "-webkit-box-align":" center",
                                "align-items":" center",
                                "-webkit-box-pack":" center",
                                "justify-content":" center",
                                "font-weight":" 400",
                                "border-radius":" 0.5rem",
                                "min-height":" 2.5rem",
                                "margin":" 0px",
                                "line-height":" 1.6",
                                "text-transform":" none",
                                "font-size":" inherit",
                                "font-family":" inherit",
                                "width":" 100%",
                                "font-family": '"Source Sans Pro", sans-serif',
                                "margin-bottom":"5px",
                                "max-height":"40px",
                                "font-size": "14px"
                            },
                            "nav-link": {
                                "font-family":" inherit",
                                "width":" 100%",
                                "font-size":" inherit",
                                "display":"flex",
                                "text-align": "left",
                                "margin":"0px",
                                "--hover-border": "#232323",
                                "align-items":" center",
                                "justify-content":" flex-start",
                                "max-height":"40px",
                            },
                            "nav-link-selected": {
                                "background-color":"rgb(255, 75, 75, 100)",
                                "font-family":"inherit",
                                "width":"100%",
                                "font-size":"inherit",
                                "display":"flex",
                                "align-items":"center",
                                "justify-content":"flex-start",
                                "font-weight":"normal",
                            },
                        }
                    )
                        
        sac.divider(label='Settings', icon='gear', align='center', color='gray')
        
        if st.button("Clear caches",type="secondary",use_container_width=True, help="Force reload data.",icon=AppIcons.SYNC.value):
            raise ResetBotFlag("True")
    
    selected_idx = option_maping.index(selection)
    
    if selected_idx != current_idx:
        if selected_idx == 0:
            st.switch_page(AppPages.HOME.value)
        if selected_idx == 1:
            st.switch_page(AppPages.BARO.value)
        if selected_idx == 2:
            st.switch_page(AppPages.VARZIA.value)
        if selected_idx == 3:
            st.switch_page(AppPages.MARKET.value)
        if selected_idx == 4:
            st.switch_page(AppPages.RIVENS.value)
        if selected_idx == 5:
            st.switch_page(AppPages.RELICS.value)
        if selected_idx == 6:
            st.switch_page(AppPages.STATISTICS.value)
        if selected_idx == 7:
            st.switch_page(AppPages.ABOUT.value)


def paginations(length,num_of_row=2,items_per_row = 5):
    """Pagination for pages.

    Args:
        items (list): item list.
        num_of_row (int, optional): number of rows per page. Defaults to 2.

    Returns:
        list, int: item list for page, number of item per row.
    """
    items_per_page = items_per_row * num_of_row

    max_page = math.ceil(length / items_per_page)
    page = sac.pagination(total=length,page_size=items_per_page,align='center', show_total=True)
    
    page = max(1, min(page, max_page))  

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    
    return start_index, end_index, items_per_row


def reject_url_param():
    """Redirect to 404 page when there's query_params. """
    if len(st.query_params.to_dict())>0:
        st.switch_page(AppPages.NOTFOUND.value)


def empty_result(item):
    """Render Empty results."""
    sac.result(label='Empty', description=f"""Currently there's no {item}""", status='empty')


def baro_time_alert(message):
    """Render baro kit'er alert message"""
    sac.alert(label=f"{message}", banner=True,size='xs',variant='outline', color='#4682b4', icon=True, closable=True)


def inject_style(filename):
    """Inject style from html file."""
    st.html(f"""components/htmls/{filename}.html""")

def auction_style():
    """Auction page style. """
    inject_style("auction")


def image_style():
    """Image style. """
    inject_style("image")


def varzia_style():
    """Varzia page style. """
    inject_style("varzia")


def market_style():
    """Market page style. """
    inject_style("market")


def world_style():
    """Home page style. """
    inject_style("world")


def card_style():
    """Varzia/Baro cards style. """
    inject_style("card")

def app_style():
    """App style. """
    inject_style("app")

def set_divider():
    """Render a divider. """
    sac.divider(label='item', icon='diagram-2-fill', align='center', color='gray')