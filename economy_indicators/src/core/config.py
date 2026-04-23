import os
from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")

INDICATORS = {
    "US": {
        "source": "fred",
        "series": {
            "interest_rate": "FEDFUNDS",
            "inflation": "CPIAUCSL",
            "unemployment": "UNRATE",
            "gdp_growth": "A191RL1Q225SBEA",
            "exports": "EXPGS",
            "imports": "IMPGS",
            "fx_eurusd": "DEXUSEU",
            "money_supply": "M2SL",
        },
    },
    "EU": {
        "source": "ecb",
        "series": {
            "interest_rate": {
                "dataset": "EST",
                "key": "B.EU000A2X2A25.WT",  # €STR
            },
            "fx_eurusd": {"dataset": "EXR", "key": "D.USD.EUR.SP00.A"},
            "money_supply": {"dataset": "BSI", "key": "M.U2.Y.V.M30.X.1.U2.2300.Z01.E"},
        },
    },
}
