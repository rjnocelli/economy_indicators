from sqlalchemy import create_engine
import os


def get_engine():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", 5432)
    db = os.getenv("DB_NAME")

    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)