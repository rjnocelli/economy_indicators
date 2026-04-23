from dataclasses import dataclass
from datetime import date


@dataclass
class EconomicIndicator:
    country: str
    date: date
    indicator: str
    value: float
    unit: str
    source: str