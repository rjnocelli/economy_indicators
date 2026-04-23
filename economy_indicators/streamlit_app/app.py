import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from pathlib import Path

DB_PATH = Path("data/macro.db")


# ----------------------------
# DB loader (SQLite only)
# ----------------------------
def load_data():
    if not DB_PATH.exists():
        st.error("Database not found. Run pipeline first.")
        st.stop()

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT country, date, indicator, value
        FROM economic_indicators
        """,
        conn,
    )

    conn.close()

    df["date"] = pd.to_datetime(df["date"])
    return df


# ----------------------------
# App config
# ----------------------------
st.set_page_config(layout="wide")
st.title("🌍 Macro Economic Dashboard (SQLite)")


# ----------------------------
# Load data
# ----------------------------
@st.cache_data(ttl=60)
def get_data():
    return load_data()


df = get_data()

if df.empty:
    st.warning("No data available. Run pipeline first.")
    st.stop()


# ----------------------------
# Sidebar filters
# ----------------------------
st.sidebar.header("Filters")

countries = sorted(df["country"].unique())
indicators = sorted(df["indicator"].unique())

selected_countries = st.sidebar.multiselect(
    "Countries",
    options=countries,
    default=["US", "EU"] if "US" in countries else countries[:1],
)

selected_indicators = st.sidebar.multiselect(
    "Indicators",
    options=indicators,
    default=["interest_rate", "inflation"] if "interest_rate" in indicators else indicators[:1],
)


# ----------------------------
# Filter dataset
# ----------------------------
filtered = df[
    (df["country"].isin(selected_countries)) &
    (df["indicator"].isin(selected_indicators))
]


# ----------------------------
# Time series chart
# ----------------------------
st.subheader("Time Series")

fig = px.line(
    filtered,
    x="date",
    y="value",
    color="indicator",
    line_dash="country",
    markers=False,
)

st.plotly_chart(fig, use_container_width=True)


# ----------------------------
# Latest values table
# ----------------------------
st.subheader("Latest Values")

latest = (
    filtered.sort_values("date")
    .groupby(["country", "indicator"])
    .tail(1)
    .sort_values(["country", "indicator"])
)

st.dataframe(latest, use_container_width=True)


# ----------------------------
# Quick stats
# ----------------------------
st.subheader("Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Countries", len(selected_countries))
col2.metric("Indicators", len(selected_indicators))
col3.metric("Rows", len(filtered))