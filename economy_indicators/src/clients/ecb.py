import requests

BASE_URL = "https://data-api.ecb.europa.eu/service/data"


def fetch_series(series_id: str):
    url = f"{BASE_URL}/{series_id}"

    res = requests.get(url, headers={"Accept": "application/json"}, timeout=10)
    res.raise_for_status()

    data = res.json()

    try:
        observations = data["dataSets"][0]["series"]["0:0:0:0:0"]["observations"]
        dates = data["structure"]["dimensions"]["observation"][0]["values"]
    except Exception:
        return []

    output = []

    for idx, obs in observations.items():
        value = obs[0]
        date = dates[int(idx)]["id"]

        output.append({
            "date": date,
            "value": value,
        })

    return output