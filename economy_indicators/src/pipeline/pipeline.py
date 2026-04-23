from src.core.config import INDICATORS
from src.clients import fred, ecb
from src.core.normalize import normalize
from src.db.db import insert_data


def run_pipeline():
    all_rows = []

    for country, cfg in INDICATORS.items():
        source = cfg["source"]

        for indicator, series_id in cfg["series"].items():
            try:
                if source == "fred":
                    raw = fred.fetch_series(series_id)
                elif source == "ecb":
                    raw = ecb.fetch_series(series_id)
                else:
                    continue

                normalized = normalize(
                    raw,
                    country=country,
                    indicator=indicator,
                    source=source,
                )

                all_rows.extend(normalized)

                print(f"✔ {country} - {indicator}")

            except Exception as e:
                print(f"✖ Error {country} {indicator}: {e}")

    insert_data(all_rows)