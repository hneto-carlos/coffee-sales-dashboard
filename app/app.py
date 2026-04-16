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
# SALES BY HOUR
# -------------------------
st.subheader("⏰ Sales by Hour")

hourly_sales = df.groupby("hour")["revenue"].sum().reset_index()
fig_hour = px.line(hourly_sales, x="hour", y="revenue", markers=True)

st.plotly_chart(fig_hour, use_container_width=True)

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
# WEEKDAY VS WEEKEND
# -------------------------
st.subheader("📆 Weekday vs Weekend")

df["day_type"] = df["day"].apply(
    lambda x: "Weekend" if x in ["Saturday", "Sunday"] else "Weekday"
)

day_type_sales = df.groupby("day_type")["revenue"].sum().reset_index()
fig_daytype = px.bar(day_type_sales, x="day_type", y="revenue")

st.plotly_chart(fig_daytype, use_container_width=True)

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
st.subheader("📌 Key Insights")

st.markdown("""
- Peak hours highlight when staffing should be optimized.
- A few product types drive most of the revenue (focus on best sellers).
- Weekend vs weekday differences can guide promotions.
- Store-level performance helps identify high and low-performing locations.
""")