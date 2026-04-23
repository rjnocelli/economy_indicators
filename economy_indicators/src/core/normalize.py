from datetime import datetime


def normalize(series, country, indicator, source, unit="%"):
    output = []

    for row in series:
        value = row["value"]
        if value is None:
            continue

        try:
            parsed_date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        except Exception:
            continue

        output.append({
            "country": country,
            "date": parsed_date,
            "indicator": indicator,
            "value": float(value),
            "unit": unit,
            "source": source,
        })

    return output