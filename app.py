"""
Product Analysis Dashboard
---------------------------
Analyzes product-level sales data to surface:
  1. Best-Selling Categories
  2. Most Profitable Products
  3. Loss-Making Products

Run locally:   streamlit run app.py
Deploy:        push to GitHub -> deploy on Streamlit Community Cloud
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Product Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

REQUIRED_COLUMNS = [
    "Product_Name", "Category", "Units_Sold",
    "Cost_Price", "Selling_Price", "Revenue", "Total_Cost", "Profit",
]


# --------------------------------------------------------------------------
# Data loading
# --------------------------------------------------------------------------
@st.cache_data
def load_default_data() -> pd.DataFrame:
    path = os.path.join("data", "sample_sales_data.csv")
    return pd.read_csv(path)


def validate_and_prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure required columns exist; derive any that are missing but computable."""
    df = df.copy()

    # Try to derive Revenue / Total_Cost / Profit if the user's file lacks them
    if "Revenue" not in df.columns and {"Selling_Price", "Units_Sold"}.issubset(df.columns):
        df["Revenue"] = df["Selling_Price"] * df["Units_Sold"]

    if "Total_Cost" not in df.columns and {"Cost_Price", "Units_Sold"}.issubset(df.columns):
        df["Total_Cost"] = df["Cost_Price"] * df["Units_Sold"]

    if "Profit" not in df.columns and {"Revenue", "Total_Cost"}.issubset(df.columns):
        df["Profit"] = df["Revenue"] - df["Total_Cost"]

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            "Uploaded file is missing required columns (or the data needed to "
            f"derive them): {', '.join(missing)}"
        )

    # Basic numeric coercion
    numeric_cols = ["Units_Sold", "Cost_Price", "Selling_Price", "Revenue", "Total_Cost", "Profit"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_cols)
    df["Profit_Margin_%"] = np.where(
        df["Revenue"] != 0, (df["Profit"] / df["Revenue"]) * 100, 0
    )
    return df


# --------------------------------------------------------------------------
# Sidebar — data source & filters
# --------------------------------------------------------------------------
st.sidebar.title("⚙️ Controls")

data_source = st.sidebar.radio(
    "Data source",
    ["Use sample data", "Upload my own CSV"],
    index=0,
)

if data_source == "Upload my own CSV":
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV",
        type=["csv"],
        help=(
            "Expected columns: Product_Name, Category, Units_Sold, Cost_Price, "
            "Selling_Price. Revenue / Total_Cost / Profit are computed automatically "
            "if not present."
        ),
    )
    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)
    else:
        st.sidebar.info("Upload a file to continue, or switch back to sample data.")
        raw_df = load_default_data()
else:
    raw_df = load_default_data()

try:
    df = validate_and_prepare(raw_df)
except ValueError as e:
    st.error(f"⚠️ {e}")
    st.stop()

# Category filter
all_categories = sorted(df["Category"].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Filter by category", options=all_categories, default=all_categories
)
df = df[df["Category"].isin(selected_categories)]

top_n = st.sidebar.slider("Number of items to show in rankings", 3, 20, 10)

if df.empty:
    st.warning("No data matches the current filters.")
    st.stop()

# --------------------------------------------------------------------------
# Header + KPIs
# --------------------------------------------------------------------------
st.title("📊 Product Analysis Dashboard")
st.caption("Best-selling categories · most profitable products · loss-making products")

total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_units = df["Units_Sold"].sum()
loss_making_count = (df["Profit"] < 0).sum()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
k2.metric("Total Profit", f"₹{total_profit:,.0f}",
          delta=f"{(total_profit / total_revenue * 100):.1f}% margin" if total_revenue else None)
k3.metric("Units Sold", f"{total_units:,.0f}")
k4.metric("Loss-Making Products", f"{loss_making_count}",
          delta=None if loss_making_count == 0 else "needs attention",
          delta_color="inverse")

st.divider()

# --------------------------------------------------------------------------
# 1. Best Selling Categories
# --------------------------------------------------------------------------
st.header("🏆 Best-Selling Categories")

metric_choice = st.radio(
    "Rank categories by", ["Units Sold", "Revenue"], horizontal=True, key="cat_metric"
)
metric_col = "Units_Sold" if metric_choice == "Units Sold" else "Revenue"

cat_summary = (
    df.groupby("Category", as_index=False)
    .agg(Units_Sold=("Units_Sold", "sum"), Revenue=("Revenue", "sum"), Profit=("Profit", "sum"))
    .sort_values(metric_col, ascending=False)
)

col1, col2 = st.columns([2, 1])
with col1:
    fig_cat = px.bar(
        cat_summary,
        x="Category",
        y=metric_col,
        color="Category",
        text_auto=".2s",
        title=f"Categories Ranked by {metric_choice}",
    )
    fig_cat.update_layout(showlegend=False, xaxis_title="", yaxis_title=metric_choice)
    st.plotly_chart(fig_cat, use_container_width=True)
with col2:
    fig_pie = px.pie(cat_summary, names="Category", values=metric_col, hole=0.45,
                      title="Share of Total")
    st.plotly_chart(fig_pie, use_container_width=True)

st.dataframe(cat_summary.style.format({
    "Units_Sold": "{:,.0f}", "Revenue": "₹{:,.0f}", "Profit": "₹{:,.0f}"
}), use_container_width=True)

st.divider()

# --------------------------------------------------------------------------
# 2. Most Profitable Products
# --------------------------------------------------------------------------
st.header("💰 Most Profitable Products")

top_profitable = df.sort_values("Profit", ascending=False).head(top_n)

fig_profit = px.bar(
    top_profitable.sort_values("Profit"),
    x="Profit",
    y="Product_Name",
    color="Category",
    orientation="h",
    text_auto=".2s",
    title=f"Top {top_n} Products by Profit",
)
fig_profit.update_layout(yaxis_title="", xaxis_title="Profit (₹)")
st.plotly_chart(fig_profit, use_container_width=True)

st.dataframe(
    top_profitable[["Product_Name", "Category", "Units_Sold", "Revenue", "Profit", "Profit_Margin_%"]]
    .style.format({
        "Units_Sold": "{:,.0f}", "Revenue": "₹{:,.0f}",
        "Profit": "₹{:,.0f}", "Profit_Margin_%": "{:.1f}%"
    }),
    use_container_width=True,
)

st.divider()

# --------------------------------------------------------------------------
# 3. Loss-Making Products
# --------------------------------------------------------------------------
st.header("📉 Loss-Making Products")

loss_making = df[df["Profit"] < 0].sort_values("Profit")

if loss_making.empty:
    st.success("No loss-making products in the current selection. 🎉")
else:
    fig_loss = px.bar(
        loss_making.head(top_n).sort_values("Profit", ascending=False),
        x="Profit",
        y="Product_Name",
        color="Category",
        orientation="h",
        text_auto=".2s",
        title=f"Top {min(top_n, len(loss_making))} Loss-Making Products",
        color_discrete_sequence=px.colors.sequential.Reds_r,
    )
    fig_loss.update_layout(yaxis_title="", xaxis_title="Profit (₹, negative = loss)")
    st.plotly_chart(fig_loss, use_container_width=True)

    st.dataframe(
        loss_making[["Product_Name", "Category", "Units_Sold", "Revenue", "Cost_Price", "Selling_Price", "Profit", "Profit_Margin_%"]]
        .style.format({
            "Units_Sold": "{:,.0f}", "Revenue": "₹{:,.0f}", "Cost_Price": "₹{:,.2f}",
            "Selling_Price": "₹{:,.2f}", "Profit": "₹{:,.0f}", "Profit_Margin_%": "{:.1f}%"
        }),
        use_container_width=True,
    )

    st.warning(
        f"⚠️ {len(loss_making)} product(s) are currently sold at a loss. "
        "Consider revisiting pricing or sourcing cost for these items."
    )

st.divider()
st.caption("Built with Streamlit · Data is sample/demo data unless a CSV is uploaded.")
