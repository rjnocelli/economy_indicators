import time
import random
from datetime import date
from typing import Optional
import request
from src.core.config import INDICATORS
from src.clients import fred, ecb
from src.core.normalize import normalize
from src.db.db import insert_data


def run_pipeline(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """
    Main ingestion pipeline.

    Args:
        start_date (str): optional ISO date (YYYY-MM-DD)
        end_date (str): optional ISO date (YYYY-MM-DD)
    """

    if end_date is None:
        end_date = date.today().isoformat()

    all_rows = []

    session = request.Session()
    session.headers.update(
        {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
        }
    )
    for country, cfg in INDICATORS.items():
        source = cfg["source"]

        for indicator, series_config in cfg["series"].items():
            try:
                # ----------------------
                # FRED
                # ----------------------
                if source == "fred":
                    raw = fred.fetch_series(
                        series_id=series_config,
                        start_date=start_date,
                        end_date=end_date,
                    )

                # ----------------------
                # ECB
                # ----------------------
                elif source == "ecb":
                    raw = ecb.fetch_series(
                        dataset=series_config["dataset"],
                        key=series_config["key"],
                        start_date=start_date,
                        end_date=end_date,
                    )
                    time.sleep(random.uniform(3, 6))
                else:
                    print(f"⚠ Unknown source: {source}")
                    continue

                # ----------------------
                # Normalize
                # ----------------------
                normalized = normalize(
                    raw,
                    country=country,
                    indicator=indicator,
                    source=source,
                )
                if not normalized:
                    print(f"⚠ EMPTY RESULT {country} - {indicator}")

                all_rows.extend(normalized)

                print(f"✔ {country} - {indicator} ({len(normalized)} rows)")

            except Exception as e:
                print(f"✖ Error {country} {indicator}: {e}")

    # ----------------------
    # Load into DB
    # ----------------------
    insert_data(all_rows)

    print(f"\n✅ Pipeline completed. Inserted {len(all_rows)} rows.")


# ----------------------
# CLI entry (optional)
# ----------------------
if __name__ == "__main__":
    # Example: full backfill from 2018
    run_pipeline(start_date="2018-01-01")
