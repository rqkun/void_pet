import logging
from statistics import median
from components import custom
from config.constants import AppIcons, Warframe
from utils import data_manage, tools
import streamlit as st
import pandas as pd

custom.sideNav(6)
custom.reject_url_param()

def calculate_price_stats(orders):
    """Calculate min, median, and max prices from a list of orders."""
    if not orders:
        return 0, 0, 0
        
    sorted_orders = tools.get_min_status_plat(orders, None)
    prices = [order["platinum"] for order in orders]
    
    return sorted_orders[0]["platinum"], median(prices), sorted_orders[-1]["platinum"]


def prep_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes data and returns a styled DataFrame in Streamlit, 
    highlighting the row(s) where (Median - Min) is the lowest and non-negative in green,
    and rows where (Median - Min) is negative in red.
    """
    if df.empty:
        logging.warning("No data available to display.")
        return df
    df["Link"] = [f"""[{AppIcons.EXTERNAL.value}]({item}) """ for item in df["Link"]]
    df.set_index("Link", inplace=True)
    df["Diff"] = df["Median"] - df["Min"]
    
    min_diff_value = df[df["Diff"] >= 0]["Diff"].min() if not df[df["Diff"] >= 0].empty else None
    max_diff_value = df[df["Diff"] >= 0]["Diff"].max() if not df[df["Diff"] >= 0].empty else None
    highlight_gold = df[df["Diff"] == max_diff_value].index.tolist() if max_diff_value is not None else []
    highlight_lime = df[df["Diff"] == min_diff_value].index.tolist() if min_diff_value is not None else []
    highlight_red = df[df["Diff"] < 0].index.tolist()

    def highlight_row(row:pd.Series):
        if row.name in highlight_lime:
            return ['color: lime; font-weight: bold;'] * len(row)
        elif row.name in highlight_red:
            return ['color: #FF6961; font-weight: bold;'] * len(row)
        elif row.name in highlight_gold:
            return ['color: #FFD700; font-weight: bold;'] * len(row)
        return [''] * len(row)

    

    df = df.drop(columns=["Diff"])
    
    try:
        styled_df = df.style.apply(highlight_row, axis=1)
    except Exception as e:
        logging.warning(f"Error applying row styling: {e}")
        styled_df = df 

    return styled_df

def process_item_data(items):
    """Process a list of items into a DataFrame-ready format."""
    processed_data = []
    
    for item in items:
        min_plat, median_plat, max_plat = calculate_price_stats(item["orders"])
        processed_data.append({
            "Name": item["url"].replace("_", " ").replace(" set", "").title(),
            "Link": f"{Warframe.MARKET_API.value['url']}{item['url']}",
            "Count": len(item["orders"]),
            "Min": int(min_plat),
            "Median": int(median_plat),
            "Max": int(max_plat),
        })
    
    return processed_data

left,right = st.columns([5,1],vertical_alignment="top")
reload_btn = right.button(AppIcons.SYNC.value,use_container_width=True,type="primary")

with left,st.status("Downloading data..."):
    left,right= st.columns([2,1])
    left.write("Loading Warframes")
    with right,st.spinner("",show_time=True):
        frame_data = data_manage.preload_primeframes_orders()

    left,right= st.columns([2,1])
    left.write("Loading Weapons")
    with right,st.spinner("",show_time=True):
        weapon_data = data_manage.preload_primeweaps_orders()

    left,right= st.columns([2,1])
    left.write("Loading Sentinels")
    with right,st.spinner("",show_time=True):
        sentinels_data = data_manage.preload_primesens_orders()
    left.write(":material/check: Finished Loading")

st.markdown("""<span style="color:lime;">■</span> <b>Should buy</b>: 
            <span style="color:gray;">The lowest differences between lowest price and median price.</span>  
            <span style="color:#FFD700;">■</span> <b>Should sell</b>: 
            <span style="color:gray;">The largest differences between lowest price and median price.</span>  
            <span style="color:#FF6961;">■</span> <b>Overprice</b>: 
            <span style="color:gray;">The there are cheaper sellers but they're currently offline.</span> 
            """,unsafe_allow_html=True)

tab1,tab2,tab3 = st.tabs([
    ":material/person: Warframes",
    ":material/plumbing: Weapons",
    ":material/robot_2: Sentinels"
    ])

with tab1:
    df = pd.DataFrame(process_item_data(frame_data))
    st.table(prep_dataframe(df))

with tab2:
    df = pd.DataFrame(process_item_data(weapon_data))
    st.table(prep_dataframe(df))

with tab3:
    df = pd.DataFrame(process_item_data(sentinels_data))
    st.table(prep_dataframe(df))

if reload_btn:
    data_manage.clear_primecaches()
    st.rerun()