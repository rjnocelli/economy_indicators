CREATE TABLE IF NOT EXISTS economic_indicators (
    country TEXT NOT NULL,
    date DATE NOT NULL,
    indicator TEXT NOT NULL,
    value DOUBLE PRECISION,
    unit TEXT,
    source TEXT,
    PRIMARY KEY (country, date, indicator)
);