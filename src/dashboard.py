import sys
from pathlib import Path

# Add parent directory to path so src modules can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import plotly.express as px
import pandas as pd
from src.db import get_connection, get_all_transactions
from src.ingestor import ingest_csv

DB_PATH = "finance.db"

st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
st.title("Personal Finance Dashboard")

conn = get_connection(DB_PATH)

# --- Sidebar: CSV Upload ---
st.sidebar.header("Import Transactions")
uploaded_file = st.sidebar.file_uploader("Upload bank CSV", type=["csv"])

if uploaded_file:
    tmp_path = Path("data") / uploaded_file.name
    tmp_path.parent.mkdir(exist_ok=True)
    tmp_path.write_bytes(uploaded_file.getvalue())
    count = ingest_csv(conn, tmp_path, source=uploaded_file.name)
    if count > 0:
        st.sidebar.success(f"Imported {count} new transactions.")
    else:
        st.sidebar.info("No new transactions (all already imported).")

# --- Load data ---
df = get_all_transactions(conn)

if df.empty:
    st.info("No transactions yet. Upload a CSV from the sidebar to get started.")
    st.stop()

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)

# --- Filters ---
months = sorted(df["month"].unique(), reverse=True)
selected_month = st.selectbox("Select month", ["All"] + months)

filtered = df if selected_month == "All" else df[df["month"] == selected_month]
expenses = filtered[filtered["amount"] < 0].copy()
expenses["amount_abs"] = expenses["amount"].abs()

# --- KPI Row ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Spent", f"${expenses['amount_abs'].sum():,.2f}")
income = filtered[filtered["amount"] > 0]["amount"].sum()
col2.metric("Total Income", f"${income:,.2f}")
col3.metric("Transactions", len(filtered))

st.divider()

# --- Charts ---
left, right = st.columns(2)

with left:
    st.subheader("Spending by Category")
    cat_summary = expenses.groupby("category")["amount_abs"].sum().reset_index()
    fig_pie = px.pie(cat_summary, values="amount_abs", names="category", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

with right:
    st.subheader("Monthly Spending Trend")
    monthly = df[df["amount"] < 0].copy()
    monthly["amount_abs"] = monthly["amount"].abs()
    monthly_agg = monthly.groupby("month")["amount_abs"].sum().reset_index()
    fig_bar = px.bar(
        monthly_agg,
        x="month",
        y="amount_abs",
        labels={"amount_abs": "Spent ($)", "month": "Month"},
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Transaction Table ---
st.subheader("Transactions")
st.dataframe(
    filtered[["date", "description", "category", "amount"]].sort_values(
        "date", ascending=False
    ),
    use_container_width=True,
)
