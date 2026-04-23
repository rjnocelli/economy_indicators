import sqlite3
import pandas as pd


def load_raw_data(db_path="data/macro.db"):
    conn = sqlite3.connect(db_path)

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


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    pivot = df.pivot_table(
        index=["date", "country"],
        columns="indicator",
        values="value"
    ).reset_index()

    features = []

    for _, row in pivot.iterrows():

        try:
            inflation = row.get("inflation")
            rate = row.get("interest_rate")
            fx = row.get("fx_eurusd")

            if pd.isna(inflation) or pd.isna(rate):
                continue

            real_rate = rate - inflation

            # -------------------------
            # REGIME RULES
            # -------------------------
            if inflation > 3 and real_rate < 0:
                regime = "inflationary pressure"

            elif inflation > 3 and real_rate > 1:
                regime = "tightening cycle"

            elif inflation < 3 and real_rate > 1:
                regime = "disinflation"

            elif inflation < 3 and real_rate < 0:
                regime = "liquidity expansion"

            else:
                regime = "neutral"

            features.append({
                "date": str(row["date"].date()),
                "country": row["country"],
                "regime": regime,
                "real_rate": real_rate,
                "inflation": inflation,
                "fx": fx,
            })

        except Exception:
            continue

    return pd.DataFrame(features)


def save_features(df: pd.DataFrame, db_path="data/macro.db"):
    conn = sqlite3.connect(db_path)

    conn.executemany(
        """
        INSERT OR REPLACE INTO macro_features
        (date, country, regime, real_rate, inflation, fx)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        df.values.tolist(),
    )

    conn.commit()
    conn.close()


def run_feature_pipeline():
    raw = load_raw_data()
    features = build_features(raw)
    save_features(features)

    print(f"✔ Stored {len(features)} macro features")