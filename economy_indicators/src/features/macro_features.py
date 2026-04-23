import pandas as pd


def compute_real_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    real rate = interest rate - inflation
    """

    pivot = df.pivot_table(
        index="date",
        columns=["country", "indicator"],
        values="value"
    )

    if ("US", "interest_rate") not in pivot or ("US", "inflation") not in pivot:
        return pd.DataFrame()

    pivot["US_real_rate"] = (
        pivot[("US", "interest_rate")] -
        pivot[("US", "inflation")]
    )

    return pivot[["US_real_rate"]].reset_index()


def compute_inflation_trend(df: pd.DataFrame) -> pd.DataFrame:
    pivot = df[df["indicator"] == "inflation"].copy()

    pivot = pivot.sort_values("date")
    pivot["inflation_trend"] = pivot.groupby("country")["value"].diff(3)

    return pivot[["date", "country", "inflation_trend"]]


def compute_fx_trend(df: pd.DataFrame) -> pd.DataFrame:
    fx = df[df["indicator"] == "fx_eurusd"].copy()
    fx = fx.sort_values("date")

    fx["fx_trend"] = fx.groupby("country")["value"].transform(
        lambda x: x.rolling(3).mean().diff()
    )

    return fx[["date", "country", "fx_trend"]]