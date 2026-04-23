import psycopg2
import os


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5432),
    )


def insert_data(rows):
    if not rows:
        return

    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO economic_indicators (country, date, indicator, value, unit, source)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (country, date, indicator) DO NOTHING;
    """

    data = [
        (
            r["country"],
            r["date"],
            r["indicator"],
            r["value"],
            r["unit"],
            r["source"],
        )
        for r in rows
    ]

    cur.executemany(query, data)
    conn.commit()

    cur.close()
    conn.close()