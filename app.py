# Creating a Steamlit Visualization for Online Food Delivery Analysis

from pathlib import Path

import pandas as pd  # type: ignore[reportMissingModuleSource]
import streamlit as st  # type: ignore[reportMissingImports]

st.set_page_config(page_title="Food Delivery Analysis", layout="wide")

# Read the original data file in the same folder as app.py
csv_path = Path(__file__).parent / "ONINE_FOOD_DELIVERY_ANALYSIS.csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    df = load_data(csv_path)
except FileNotFoundError:
    st.error(f"Could not find the data file: {csv_path.name}")
    st.stop()

st.title("Online Food Delivery Analysis")
st.caption("Exploring order patterns, delivery times, and cancellations")

# Summary numbers
total_orders = len(df)
delivered = (df["Order_Status"] == "Delivered").sum()
cancelled = (df["Order_Status"] == "Cancelled").sum()
avg_order_value = df["Order_Value"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total orders", f"{total_orders:,}")
c2.metric("Delivered", f"{delivered:,}")
c3.metric("Cancelled", f"{cancelled:,}")
c4.metric("Average order value", f"{avg_order_value:,.0f}" if pd.notna(avg_order_value) else "N/A")

st.subheader("Order value and delivery time")

left, right = st.columns(2)

with left:
    values = df["Order_Value"].dropna()
    if not values.empty:
        bins = pd.cut(values, bins=20).value_counts().sort_index()
        bins.index = bins.index.astype(str)
        st.bar_chart(bins)
        st.caption("Order value distribution (available original values)")

with right:
    times = df["Delivery_Time_Min"].dropna()
    if not times.empty:
        bins = pd.cut(times, bins=20).value_counts().sort_index()
        bins.index = bins.index.astype(str)
        st.bar_chart(bins)
        st.caption("Delivery time distribution (available original values)")

st.subheader("Orders by city and cuisine")

left, right = st.columns(2)

with left:
    st.bar_chart(df["City"].dropna().value_counts().sort_values())
    st.caption("Orders by city")

with right:
    st.bar_chart(df["Cuisine_Type"].dropna().value_counts().sort_values())
    st.caption("Orders by cuisine")

st.subheader("Reasons for cancelled orders")

cancelled_orders = df[df["Order_Status"] == "Cancelled"]
reasons = cancelled_orders["Cancellation_Reason"].fillna("Not recorded").value_counts()

if not reasons.empty:
    st.bar_chart(reasons.sort_values())
else:
    st.info("No cancellation reason data is available.")