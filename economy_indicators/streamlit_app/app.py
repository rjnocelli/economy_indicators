import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data

st.set_page_config(layout="wide")

st.title("🌍 Macro Economic Dashboard")

@st.cache_data
def get_data():
    return load_data()


df = get_data()

# Sidebar filters
st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(df["country"].unique()),
    default=["US", "EU"]
)

indicators = st.sidebar.multiselect(
    "Select Indicators",
    options=sorted(df["indicator"].unique()),
    default=["interest_rate", "inflation"]
)

# Filter data
filtered = df[
    (df["country"].isin(countries)) &
    (df["indicator"].isin(indicators))
]

if filtered.empty:
    st.warning("No data for selected filters")
    st.stop()

# Line chart
fig = px.line(
    filtered,
    x="date",
    y="value",
    color="indicator",
    line_dash="country",
)

st.plotly_chart(fig, use_container_width=True)

# Latest values table
st.subheader("Latest Values")

latest = (
    filtered.sort_values("date")
    .groupby(["country", "indicator"])
    .tail(1)
    .sort_values(["country", "indicator"])
)

st.dataframe(latest, use_container_width=True)