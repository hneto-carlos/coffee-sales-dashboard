import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Coffee Sales Dashboard", layout="wide")

st.title("☕ Coffee Shop Sales Dashboard")
st.markdown("Business insights for daily operations")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/coffee_sales_clean.csv")
    
    # Ensure datetime
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    
    return df

df = load_data()

st.sidebar.header("Filters")

store = st.sidebar.multiselect(
    "Select Store",
    options=df["store_location"].unique(),
    default=df["store_location"].unique()
)

product = st.sidebar.multiselect(
    "Select Product",
    options=df["product_type"].unique(),
    default=df["product_type"].unique()
)

df = df[
    (df["store_location"].isin(store)) &
    (df["product_type"].isin(product))
]


# -------------------------
# KPI METRICS
# -------------------------
total_revenue = df["revenue"].sum()
total_orders = df.shape[0]
avg_order = total_revenue / total_orders
top_product = df.groupby("product_type")["revenue"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Orders", total_orders)
col3.metric("Avg Order Value", f"${avg_order:.2f}")
col4.metric("Top Product", top_product)

# -------------------------
# PREPARE DATA FOR CHARTS
# -------------------------

# Sales by Hour
hourly_sales = df.groupby("hour")["revenue"].sum().reset_index()
fig_hour = px.line(hourly_sales, x="hour", y="revenue", markers=True)

# Weekday vs Weekend
df["day_type"] = df["day"].apply(
    lambda x: "Weekend" if x in ["Saturday", "Sunday"] else "Weekday"
)

day_type_sales = df.groupby("day_type")["revenue"].sum().reset_index()
fig_daytype = px.bar(day_type_sales, x="day_type", y="revenue")

# -------------------------
# SALES OVERVIEW
# -------------------------
st.subheader("⏰ Sales Overview")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Sales by Hour**")
    st.plotly_chart(fig_hour, use_container_width=True)

with col2:
    st.markdown("**Weekday vs Weekend**")
    st.plotly_chart(fig_daytype, use_container_width=True)

# -------------------------
# TOP PRODUCTS
# -------------------------
st.subheader("🥐 Top Products")

top_products = (
    df.groupby("product_type")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(top_products, x="product_type", y="revenue")
st.plotly_chart(fig_products, use_container_width=True)

# -------------------------
# REVENUE TREND
# -------------------------
st.subheader("📅 Revenue Trend")

daily_sales = df.groupby("transaction_date")["revenue"].sum().reset_index()
fig_trend = px.line(daily_sales, x="transaction_date", y="revenue")

st.plotly_chart(fig_trend, use_container_width=True)


# -------------------------
# STORE PERFORMANCE (BONUS 🔥)
# -------------------------
st.subheader("🏪 Store Location Performance")

store_sales = df.groupby("store_location")["revenue"].sum().reset_index()
fig_store = px.bar(store_sales, x="store_location", y="revenue")

st.plotly_chart(fig_store, use_container_width=True)

# -------------------------
# INSIGHTS
# -------------------------

peak_hour = hourly_sales.loc[hourly_sales["revenue"].idxmax(), "hour"]
peak_revenue = hourly_sales["revenue"].max()

best_product = top_products.iloc[0]["product_type"]
best_product_rev = top_products.iloc[0]["revenue"]

st.subheader("📌 Key Insights")

st.markdown(f"""
- Peak sales occur at **{peak_hour}:00**, generating **${peak_revenue:,.0f}**.
- Top product is **{best_product}**, contributing **${best_product_rev:,.0f}**.
- Revenue concentration suggests opportunity to promote lower-performing products.
- Consider boosting afternoon sales with targeted promotions.
""")
