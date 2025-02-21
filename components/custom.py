import math
import streamlit as st
from components import dialogs
from config.constants import AppIcons, AppPages
import streamlit_antd_components as sac

def sideNav(current_idx):
    """ Custom Sidebar navigation.

    Args:
        current_idx (int): current page index.
        logo (enum, optional): current page logo. Defaults to Warframe.AYA.value.
    """
    with st.sidebar:
        st.markdown("""<style>.st-emotion-cache-kgpedg {padding: calc(1.375rem) 1.5rem 0rem; margin:-1rem 0 -1rem 0;}</style>""",unsafe_allow_html=True)
        selection = sac.menu([
            sac.MenuItem('Home', icon='house-fill',),
            sac.MenuItem('Vendors', icon='box-fill', children=[
                sac.MenuItem("Baro Ki'ter", icon='arrow-repeat'),
                sac.MenuItem('Varzia', icon='droplet-fill'),
            ]),
            sac.MenuItem('Market', icon='shop-window', children=[
                sac.MenuItem('Orders', icon='cart3'),
                sac.MenuItem('Rivens', icon='dice-6'),
            ]),
            sac.MenuItem('Relics', icon='browser-firefox'),
            sac.MenuItem('News', icon='newspaper'),
            sac.MenuItem('Github', icon='github',description="rqkun/void_pet", href='https://github.com/rqkun/void_pet/')
        ], size='xs',variant='left-bar', return_index=True, open_all=True, index=current_idx)
        
        sac.divider(label='Settings', icon='gear', align='center', color='gray')
        
        if st.button("Clear caches",type="primary",use_container_width=True, help="Force reload data.",icon=AppIcons.SYNC.value):
            dialogs.clear_cache_dialog()
        
    if selection != current_idx:
        if selection == 0:
            st.switch_page(AppPages.HOME.value)
        if selection == 2:
            st.switch_page(AppPages.BARO.value)
        if selection == 3:
            st.switch_page(AppPages.VARZIA.value)
        if selection == 5:
            st.switch_page(AppPages.MARKET.value)
        if selection == 6:
            st.switch_page(AppPages.RIVENS.value)
        if selection == 7:
            st.switch_page(AppPages.RELICS.value)
        if selection == 8:
            st.switch_page(AppPages.NEWS.value)


def paginations(items,num_of_row=2,items_per_row = 5):
    """ Pagination for pages.

    Args:
        items (list): item list.
        num_of_row (int, optional): number of rows per page. Defaults to 2.

    Returns:
        list, int: item list for page, number of item per row.
    """
    items_per_page = items_per_row * num_of_row
    total_items = len(items)

    max_page = math.ceil(total_items / items_per_page)
    page = sac.pagination(total=total_items,page_size=items_per_page,align='center', show_total=True)
    
    page = max(1, min(page, max_page))  

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paged_items = items[start_index:end_index]
    return paged_items, items_per_row


def reject_url_param():
    """ Redirect to 404 page when there's query_params. """
    if len(st.query_params.to_dict())>0:
        st.switch_page(AppPages.NOTFOUND.value)


def empty_result(item):
    """ Render Empty results."""
    sac.result(label='Empty', description=f"""Currently there's no {item}""", status='empty')


def baro_time_alert(message):
    """ Render baro kit'er alert message"""
    sac.alert(label=f"{message}", banner=True,size='xs',variant='outline', color='#4682b4', icon=True, closable=True)


def inject_style(filename):
    """ Inject style from html file."""
    st.html(f"""components/htmls/{filename}.html""")

def auction_style():
    """ Auction page style. """
    inject_style("auction")


def image_style():
    """ Image style. """
    inject_style("image")


def varzia_style():
    """ Varzia page style. """
    inject_style("varzia")


def market_style():
    """ Market page style. """
    inject_style("market")


def world_style():
    """ Home page style. """
    inject_style("world")


def card_style():
    """ Varzia/Baro cards style. """
    inject_style("card")

def app_style():
    """ App style. """
    inject_style("app")

def set_divider():
    """ Render a divider. """
    sac.divider(label='item', icon='diagram-2-fill', align='center', color='gray')