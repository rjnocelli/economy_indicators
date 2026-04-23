import pandas as pd
from db import get_engine


def load_data():
    engine = get_engine()

    query = """
    SELECT country, date, indicator, value
    FROM economic_indicators
    ORDER BY date
    """

    df = pd.read_sql(query, engine)

    df["date"] = pd.to_datetime(df["date"])

    return df


def pivot_data(df):
    return df.pivot_table(
        index="date",
        columns=["country", "indicator"],
        values="value"
    )