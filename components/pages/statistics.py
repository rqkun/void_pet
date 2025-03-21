import math
from components import custom
from datetime import datetime, timezone
import pandas as pd
import streamlit as st
from config.constants import Warframe
from datasources import google_sheet
from utils import data_manage
from utils import tools
from utils.tools import prep_dataframe,insert,process_item_data
from streamlit import session_state as SESSIONS
custom.sideNav(6)
custom.reject_url_param()

@st.cache_data(ttl="1d",show_spinner=False)
def process_history(_gsread_client:google_sheet.GoogleSheetConnection,sheet_name:str)-> pd.DataFrame:
    worksheet = pd.DataFrame(_gsread_client.open(sheet_name,f"{datetime.today().year}"))
    return worksheet


@st.dialog("Details")
def history_diag(data):
    pass


client = google_sheet.get_instance()

to_year = datetime.today().year


col1,col2,col3 = st.columns([4,1,1],vertical_alignment="center")
sync_btn = col2.button("Sync",icon=":material/cloud: ",use_container_width=True,type="primary")
reload_btn = col3.button("Reload",icon=":material/refresh:",use_container_width=True,type="secondary")
status_bar = col1.empty()
if 'statistic_data' not in SESSIONS:
    SESSIONS.statistic_data = {
        "frame_data":{},
        "weapon_data":{},
        "sentinel_data":{},
    }
    
with status_bar,st.spinner("Fetching warframe orders...",show_time=True):
    frame_orders_list = data_manage.preload_primeframes_orders()
    frame_orders_df= pd.DataFrame(process_item_data(frame_orders_list))

with status_bar,st.spinner("Gathering warframe history...",show_time=True):
    frames_worksheet = process_history(client,"prime_frames")
    SESSIONS.statistic_data["frame_data"] = {
        "name": "prime_frames",
        "dataframe": frame_orders_df,
        "latest_sync": frames_worksheet["Changed"].iloc[-1],
        "formated": prep_dataframe(frame_orders_df),
        "history": insert(df=frame_orders_df,sheet=frames_worksheet),
        
    }

with status_bar, st.spinner("Fetching weapon orders...",show_time=True):
    weapon_orders_list = data_manage.preload_primeweaps_orders()
    weapon_orders_df= pd.DataFrame(process_item_data(weapon_orders_list))
with status_bar,st.spinner("Gathering weapon history...",show_time=True):
    weapons_worksheet = process_history(client,"prime_weapons")
    SESSIONS.statistic_data["weapon_data"] = {
        "name": "prime_weapons",
        "dataframe": weapon_orders_df,
        "latest_sync": weapons_worksheet["Changed"].iloc[-1],
        "formated": prep_dataframe(weapon_orders_df),
        "history": insert(df=weapon_orders_df,sheet=weapons_worksheet)
    }

with status_bar,st.spinner("Fetching sentinel orders...",show_time=True):
    sentinel_orders_list = data_manage.preload_primesens_orders()
    sentinel_orders_df= pd.DataFrame(process_item_data(sentinel_orders_list))

with status_bar,st.spinner("Gathering sentinel history...",show_time=True):
    sentinels_worksheet = process_history(client,"prime_sentinels")
    SESSIONS.statistic_data["sentinel_data"] = {
        "name": "prime_sentinels",
        "dataframe": sentinel_orders_df,
        "latest_sync": sentinels_worksheet["Changed"].iloc[-1],
        "formated": prep_dataframe(sentinel_orders_df),
        "history": insert(df=sentinel_orders_df,sheet=sentinels_worksheet)
    }

with status_bar,st.spinner("Combining histories",show_time=True):
    SESSIONS.statistic_data["total_history"]=pd.concat([
        SESSIONS.statistic_data["frame_data"].get("history",pd.DataFrame(columns=Warframe.COLUMN_DEF.value)),
        SESSIONS.statistic_data["weapon_data"].get("history",pd.DataFrame(columns=Warframe.COLUMN_DEF.value)),
        SESSIONS.statistic_data["sentinel_data"].get("history",pd.DataFrame(columns=Warframe.COLUMN_DEF.value))
    ], axis=0)

with status_bar:
    if "statistic_data" in SESSIONS:
        time_data = SESSIONS.statistic_data["frame_data"].get("latest_sync")
        parsed_time = datetime.strptime(time_data + " +0000", "%d/%m/%Y - %H:%M:%S UTC %z")
        time_diff = datetime.now(timezone.utc) - parsed_time
        formatted_time_diff = tools.format_time_difference(time_diff, time_data)
    st.markdown(f""":material/check_circle: **Last Sync:** *:gray[{formatted_time_diff}]*.""")

st.markdown(f"""<span style="color:lime;">■</span> <b>Stable</b>: 
            <span style="color:gray;">The lowest differences between lowest price and median price.</span>  
            <span style="color:#FFD700;">■</span> <b>Underprice</b>: 
            <span style="color:gray;">The largest differences between lowest price and median price.</span>  
            <span style="color:#FF6961;">■</span> <b>Overprice</b>: 
            <span style="color:gray;">The there are cheaper sellers but they're currently offline.</span>  
            """,unsafe_allow_html=True)

tab1,tab2,tab3 = st.tabs([
    ":material/person: Warframes",
    ":material/plumbing: Weapons",
    ":material/robot_2: Sentinels",
    # ":material/monitoring: Metrics"
    ])

column_config ={
    "Link":st.column_config.LinkColumn(
            "Link",
            help="Link to warframe.market",
            validate=r"^https://warframe\.market/items/[a-z0-9_]+$",
            display_text="🌐 Open",
            pinned=True
        ),
    "Image":st.column_config.ImageColumn(
            "Image",
            help="The image of the prime set",
            pinned=True,
            width="small"
        ),
    "Name":st.column_config.TextColumn(
            "Item",
            help="The name of the prime set",
            pinned=True
        ),
    "Count":st.column_config.NumberColumn(
            "Volume",
            help="The number of order (All time)",
            format="compact",
        ),
    "Average":st.column_config.NumberColumn(
            "Average",
            help="The average price of the set (Today)",
            format="compact",
        ),
    "Median":st.column_config.NumberColumn(
            "Median",
            help="The median price of the set (Today)",
            format="compact",
        ),
    "Min":st.column_config.NumberColumn(
            "Low",
            help="The lowest price of the set (Today)",
            format="compact",
        ),
    "Max":st.column_config.NumberColumn(
            "High",
            help="The highest price of the set (Today)",
            format="compact",
        ),
    "Open":st.column_config.NumberColumn(
            "Open",
            help="The first price of the set (Today)",
            format="compact",
        ),
    "Close":st.column_config.NumberColumn(
            "Close",
            help="The last price of the set (Today)",
            format="compact",
        ),
}

tab1.dataframe(SESSIONS.statistic_data["frame_data"].get("formated",pd.DataFrame(columns=Warframe.COLUMN_DEF.value)),
               use_container_width=True,
               column_order=["Image","Name", "Count", "Median", "Average", "Min", "Max"],
               height= max(35 * len(SESSIONS.statistic_data["frame_data"].get("dataframe",pd.DataFrame(columns=Warframe.COLUMN_DEF.value))) + math.ceil(35*1.05), 35*3),
               column_config=column_config
               )

tab2.dataframe(SESSIONS.statistic_data["weapon_data"].get("formated",pd.DataFrame(columns=Warframe.COLUMN_DEF.value)),
               use_container_width=True,
               column_order=["Image","Name", "Count", "Median", "Average", "Min", "Max"],
               height= max(35 * len(SESSIONS.statistic_data["weapon_data"].get("dataframe",pd.DataFrame(columns=Warframe.COLUMN_DEF.value))) + math.ceil(35*1.05), 35*3),
               column_config=column_config
               )

tab3.dataframe(SESSIONS.statistic_data["sentinel_data"].get("formated",pd.DataFrame(columns=Warframe.COLUMN_DEF.value)),
               use_container_width=True,
               column_order=["Image","Name", "Count", "Median", "Average", "Min", "Max"],
               height= max(35 * len(SESSIONS.statistic_data["sentinel_data"].get("dataframe",pd.DataFrame(columns=Warframe.COLUMN_DEF.value))) + math.ceil(35*1.05), 35*3),
               column_config=column_config
               )

#               //////////////////////////
#               /   Under construction   /
#               //////////////////////////
#
# if "total_history" in SESSIONS.statistic_data:
#     with tab4:
#         with st.form("qform",enter_to_submit=True):
#             weapon_names = SESSIONS.statistic_data["total_history"]["Name"].unique().tolist()
#             selected_names = st.multiselect(
#                 label="Choose Weapons",
#                 options=weapon_names
#             )
            
#             submitted = st.form_submit_button("Submit")
#             if submitted and selected_names:
#                 selected_weapons_df = SESSIONS.statistic_data["total_history"][SESSIONS.statistic_data["total_history"]["Name"].isin(selected_names)]
#                 st.table(selected_weapons_df)
#                 fig = go.Figure(data=[go.Candlestick(x=selected_weapons_df['Changed'],
#                                 open=selected_weapons_df['Open'],
#                                 high=selected_weapons_df['Max'],
#                                 low=selected_weapons_df['Min'],
#                                 close=selected_weapons_df['Close'])])
#                 st.plotly_chart(fig, theme="streamlit")


if reload_btn:
    with st.spinner("",show_time=True):
        if 'statistic_data' in SESSIONS:
            del SESSIONS.statistic_data
        data_manage.clear_primecaches()
    st.rerun()
if sync_btn:
    with st.spinner("",show_time=True):
        if 'statistic_data' in SESSIONS:
            with status_bar, st.spinner("Synchronizing warframe data...",show_time=True):
                client.update(SESSIONS.statistic_data["frame_data"].get("name","prime_frames"),
                            SESSIONS.statistic_data["frame_data"].get("history",
                                                                        pd.DataFrame(columns=Warframe.COLUMN_DEF.value)
                                                                    ).reset_index()
                            ,f"{to_year}")

            with status_bar, st.spinner("Synchronizing weapons data...",show_time=True):
                client.update(SESSIONS.statistic_data["weapon_data"].get("name","prime_weapons"),
                        SESSIONS.statistic_data["weapon_data"].get("history",
                                                                    pd.DataFrame(columns=Warframe.COLUMN_DEF.value)
                                                                ).reset_index()
                        ,f"{to_year}")

            with status_bar, st.spinner("Synchronizing sentinels data...",show_time=True):
                client.update(SESSIONS.statistic_data["sentinel_data"].get("name","prime_sentinels"),
                        SESSIONS.statistic_data["sentinel_data"].get("history",
                                                                    pd.DataFrame(columns=Warframe.COLUMN_DEF.value)
                                                                    ).reset_index(),
                        f"{to_year}")

            del SESSIONS.statistic_data
            process_history.clear()
    st.rerun()