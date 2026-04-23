CREATE TABLE IF NOT EXISTS economic_indicators (
    country TEXT NOT NULL,
    date TEXT NOT NULL,
    indicator TEXT NOT NULL,
    value REAL,
    unit TEXT,
    source TEXT,
    PRIMARY KEY (country, date, indicator)
);