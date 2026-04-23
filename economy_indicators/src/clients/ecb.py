import requests
import time
import random

BASE_URL = "https://data-api.ecb.europa.eu/service/data"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36",
}


def fetch_series(
    dataset: str, key: str, start_date=None, end_date=None, session=None, max_retries=5
):
    url = f"{BASE_URL}/{dataset}/{key}"

    params = {}
    if start_date:
        params["startPeriod"] = start_date
    if end_date:
        params["endPeriod"] = end_date

    session = session or requests.Session()
    session.headers.update(HEADERS)

    for attempt in range(max_retries):
        try:
            res = session.get(url, params=params, headers=HEADERS, timeout=15)

            if res.status_code == 503:
                raise Exception("Blocked (503)")

            res.raise_for_status()
            data = res.json()

            series = list(data["dataSets"][0]["series"].values())[0]
            observations = series["observations"]
            dates = data["structure"]["dimensions"]["observation"][0]["values"]

            output = []
            for idx, obs in observations.items():
                value = obs[0]
                date = dates[int(idx)]["id"]

                output.append(
                    {
                        "date": date,
                        "value": value,
                    }
                )

            return output

        except Exception as e:
            wait = (2**attempt) + random.uniform(0, 1)
            print(f"⚠ ECB retry {attempt + 1}/{max_retries} in {wait:.2f}s: {e}")
            time.sleep(wait)

    print(f"✖ Failed after {max_retries} retries: {dataset}/{key}")
    return []
