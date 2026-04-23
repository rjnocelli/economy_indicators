import os
import sqlite3
from contextlib import closing

DB_PATH = "data/macro.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS economic_indicators (
    country TEXT NOT NULL,
    date TEXT NOT NULL,
    indicator TEXT NOT NULL,
    value REAL,
    unit TEXT,
    source TEXT,
    PRIMARY KEY (country, date, indicator)
);
"""

FEATURES_SCHEMA = """
CREATE TABLE IF NOT EXISTS macro_features (
    date TEXT NOT NULL,
    country TEXT NOT NULL,
    regime TEXT,
    real_rate REAL,
    inflation REAL,
    fx REAL,
    PRIMARY KEY (date, country)
);
"""

def ensure_db_path():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def get_connection():
    ensure_db_path()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    conn.execute(FEATURES_SCHEMA)
    return conn


def insert_data(rows):
    if not rows:
        return

    with closing(get_connection()) as conn:
        with conn:
            conn.executemany(
                """
                INSERT OR IGNORE INTO economic_indicators
                (country, date, indicator, value, unit, source)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        r["country"],
                        str(r["date"]),  # store as ISO string
                        r["indicator"],
                        r["value"],
                        r["unit"],
                        r["source"],
                    )
                    for r in rows
                ],
            )
