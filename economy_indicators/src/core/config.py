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
            "interest_rate": "ESTR",
            "inflation": "ICP.M.U2.N.000000.4.ANR",
            "unemployment": "LFSA.M.U2.Z.Z.Z.Z.Z.Z.Z.UR",
            "fx_eurusd": "EXR.D.USD.EUR.SP00.A",
            "money_supply": "BSI.M.U2.Y.V.M30.X.1.U2.2300.Z01.E",
        },
    },
}