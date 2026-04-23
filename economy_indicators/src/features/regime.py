import pandas as pd


def classify_regime(df: pd.DataFrame) -> pd.DataFrame:
    """
    Very simple rule-based macro regime classifier.
    """

    pivot = df.pivot_table(
        index="date",
        columns=["country", "indicator"],
        values="value"
    )

    regimes = []

    for date in pivot.index:

        try:
            inflation = pivot.loc[date, ("US", "inflation")]
            rate = pivot.loc[date, ("US", "interest_rate")]
            fx = pivot.loc[date, ("US", "fx_eurusd")]

            real_rate = rate - inflation

            # -----------------------------
            # RULES (simple but powerful)
            # -----------------------------

            if inflation > 3 and real_rate < 0:
                regime = "🟥 inflationary pressure"

            elif inflation > 3 and real_rate > 1:
                regime = "🟧 tightening cycle"

            elif inflation < 3 and real_rate > 1:
                regime = "🟨 disinflation / restrictive"

            elif inflation < 3 and real_rate < 0:
                regime = "🟩 liquidity expansion"

            else:
                regime = "⚪ neutral"

            regimes.append({
                "date": date,
                "regime": regime,
                "real_rate": real_rate,
                "inflation": inflation,
                "fx": fx,
            })

        except Exception:
            continue

    return pd.DataFrame(regimes)