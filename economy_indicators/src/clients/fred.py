import requests
from src.core.config import FRED_API_KEY

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


def fetch_series(series_id: str):
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
    }

    res = requests.get(BASE_URL, params=params, timeout=10)
    res.raise_for_status()

    data = res.json()["observations"]

    return [
        {
            "date": item["date"],
            "value": None if item["value"] == "." else item["value"],
        }
        for item in data
    ]