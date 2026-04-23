import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

DB_PATH = Path("data/macro.db")


def load_features():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT date, country, regime, real_rate, inflation, fx
        FROM macro_features
        """,
        conn,
    )

    conn.close()
    df["date"] = pd.to_datetime(df["date"])
    return df


st.title("🌍 Macro Regime Dashboard")

df = load_features()

st.subheader("Latest Regime per Country")

latest = df.sort_values("date").groupby("country").tail(1)

st.dataframe(latest)


st.subheader("Regime Timeline")

selected_country = st.selectbox("Country", df["country"].unique())

filtered = df[df["country"] == selected_country]

st.line_chart(
    filtered.set_index("date")["real_rate"]
)

st.write("Current regime:")
st.write(filtered.iloc[-1]["regime"])