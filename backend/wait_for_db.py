#!/usr/bin/env python3
"""Wait for PostgreSQL to be ready before starting the application."""
import sys
import time
from urllib.parse import urlparse

import psycopg2
from app.config import settings


def wait_for_db(max_retries: int = 30, retry_interval: int = 2) -> None:
    db_url = settings.database_url
    parsed = urlparse(db_url)
    user = parsed.username or "postgres"
    password = parsed.password or ""
    host = parsed.hostname or "localhost"
    port = parsed.port or 5432
    dbname = (parsed.path or "/postgres").lstrip("/")

    print(f"Waiting for database at {host}:{port}...")
    for attempt in range(1, max_retries + 1):
        try:
            conn = psycopg2.connect(
                host=host,
                port=int(port),
                user=user,
                password=password,
                dbname=dbname,
            )
            conn.close()
            print(f"Database is ready after {attempt} attempt(s).")
            return
        except psycopg2.OperationalError as e:
            print(f"Attempt {attempt}/{max_retries}: Database not ready yet ({e})")
            time.sleep(retry_interval)

    print("Database did not become ready in time. Exiting.")
    sys.exit(1)


if __name__ == "__main__":
    wait_for_db()
