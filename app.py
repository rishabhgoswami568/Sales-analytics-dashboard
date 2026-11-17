import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📊", layout="wide")
DATA_PATH = Path(__file__).parent / "data" / "sales_data.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["profit"] = df["revenue"] - (df["quantity"] * df["unit_cost"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df

df = load_data()
st.title("📊 Sales Analytics & Business Intelligence")
st.caption("An interactive retail sales dashboard built with Python, pandas, Streamlit, and Plotly.")

with st.sidebar:
    st.header("Filters")
    min_date, max_date = df["order_date"].min().date(), df["order_date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    regions = st.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
    categories = st.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    else:
        start_date, end_date = pd.Timestamp(min_date), pd.Timestamp(max_date)

filtered = df[
    df["order_date"].between(start_date, end_date + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))
    & df["region"].isin(regions)
    & df["category"].isin(categories)
].copy()

if filtered.empty:
    st.warning("No rows match the selected filters. Change the filters to see results.")
    st.stop()

revenue = filtered["revenue"].sum()
profit = filtered["profit"].sum()
orders = filtered["order_id"].nunique()
units = filtered["quantity"].sum()
margin = (profit / revenue * 100) if revenue else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Revenue", f"${revenue:,.0f}")
c2.metric("Profit", f"${profit:,.0f}")
c3.metric("Orders", f"{orders:,}")
c4.metric("Units Sold", f"{units:,}")
c5.metric("Profit Margin", f"{margin:.1f}%")

left, right = st.columns(2)
monthly = filtered.groupby("month", as_index=False).agg(Revenue=("revenue", "sum"), Profit=("profit", "sum"))
with left:
    st.subheader("Monthly Revenue & Profit")
    long_monthly = monthly.melt(id_vars="month", var_name="Metric", value_name="Amount")
    fig = px.line(long_monthly, x="month", y="Amount", color="Metric", markers=True,
                  labels={"month": "Month", "Amount": "Amount (USD)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Revenue by Category")
    category_sales = filtered.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig = px.bar(category_sales, x="category", y="revenue", color="category",
                 labels={"category": "Category", "revenue": "Revenue (USD)"})
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Revenue by Region")
    region_sales = filtered.groupby("region", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig = px.bar(region_sales, x="region", y="revenue", labels={"region": "Region", "revenue": "Revenue (USD)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Top 10 Products")
    products = filtered.groupby("product", as_index=False).agg(Revenue=("revenue", "sum"), Profit=("profit", "sum"))
    products = products.sort_values("Revenue", ascending=False).head(10)
    fig = px.bar(products, x="Revenue", y="product", orientation="h", color="Profit",
                 labels={"Revenue": "Revenue (USD)", "product": "Product", "Profit": "Profit (USD)"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Business Insights")
best_category = category_sales.iloc[0]["category"] if not category_sales.empty else "N/A"
best_region = region_sales.iloc[0]["region"] if not region_sales.empty else "N/A"
best_product = products.iloc[0]["product"] if not products.empty else "N/A"
st.markdown(
    f"- **Top category by revenue:** {best_category}\n"
    f"- **Top region by revenue:** {best_region}\n"
    f"- **Top product by revenue:** {best_product}\n"
    f"- **Overall profit margin:** {margin:.1f}%"
)

st.subheader("Filtered Order Data")
st.dataframe(filtered.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)
st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_sales_data.csv", mime="text/csv")
