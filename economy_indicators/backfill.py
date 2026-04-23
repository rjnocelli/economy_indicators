from datetime import date

from src.core.config import INDICATORS
from src.clients import fred, ecb
from src.core.normalize import normalize
from src.db.db import insert_data

START_DATE = "2018-01-01"
END_DATE = date.today().isoformat()


def run_backfill():
    all_rows = []

    for country, cfg in INDICATORS.items():
        source = cfg["source"]

        for indicator, series_config in cfg["series"].items():
            try:
                if source == "fred":
                    raw = fred.fetch_series(
                        series_config, start_date=START_DATE, end_date=END_DATE
                    )

                elif source == "ecb":
                    raw = ecb.fetch_series(
                        dataset=series_config["dataset"],
                        key=series_config["key"],
                        start_date=START_DATE,
                        end_date=END_DATE,
                    )

                else:
                    continue

                normalized = normalize(
                    raw,
                    country=country,
                    indicator=indicator,
                    source=source,
                )

                all_rows.extend(normalized)

                print(f"✔ Backfilled {country} - {indicator}")

            except Exception as e:
                print(f"✖ Error {country} {indicator}: {e}")

    insert_data(all_rows)


if __name__ == "__main__":
    run_backfill()
