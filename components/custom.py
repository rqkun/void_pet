import math
import streamlit as st
import components.markdowns
from config.constants import AppIcons, AppPages, Warframe
import streamlit_antd_components as sac
import components

def sideNav(current_idx,logo=Warframe.AYA.value):
    with st.sidebar:
        
        st.markdown(components.markdowns.image_md("https://github.com/rqkun/void_pet/","Void Pet",source=logo["image"],caption="visible",size="30%"),unsafe_allow_html=True)
        
        selection = sac.menu([
            sac.MenuItem('Home', icon='house-fill'),
            sac.MenuItem('Vendors', icon='box-fill', children=[
                sac.MenuItem("Baro Ki'ter", icon='arrow-repeat'),
                sac.MenuItem('Varzia', icon='droplet-fill'),
            ]),
            sac.MenuItem('Market', icon='shop-window'),
            sac.MenuItem('rqkun', icon='github', href='https://github.com/rqkun/void_pet/')
        ], size='sm',variant='left-bar', return_index=True, open_all=True, index=current_idx)
        
        sac.divider(label='Settings', icon='gear', align='center', color='gray')
        
        if st.button("Clear caches",type="secondary",use_container_width=True, help="Force reload data.",icon=AppIcons.SYNC.value):
            st.cache_data.clear()
            st.rerun()
        
    if selection != current_idx:
        if selection == 0:
            st.switch_page(AppPages.HOME.value)
        if selection == 2:
            st.switch_page(AppPages.BARO.value)
        if selection == 3:
            st.switch_page(AppPages.VARZIA.value)
        if selection == 4:
            st.switch_page(AppPages.MARKET.value)
        
        
def paginations(items,num_of_row=2):
    
    items_per_row = 5
    items_per_page = items_per_row * num_of_row
    total_items = len(items)

    max_page = math.ceil(total_items / items_per_page)
    page = sac.pagination(total=total_items,page_size=items_per_page,align='center', show_total=True)
    
    page = max(1, min(page, max_page))  

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paged_items = items[start_index:end_index]
    return paged_items, items_per_row

def hover_effect():
    st.html("components/htmls/hover.html")

def hover_dialog():
    st.html("components/htmls/hover_dialog.html")
    
def market_item_style():
    st.html("components/htmls/market.html")