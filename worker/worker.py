# worker/worker.py
import os
import time
from datetime import datetime
import traceback

# Optional DB test import
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")

def test_db_insert_once():
    """Try a single-safe insert into alerts to verify DB connection."""
    if not DATABASE_URL:
        print("🔴 DATABASE_URL not set in env. Skipping DB test.")
        return

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # Use a unique message so we can find it easily in Supabase
        msg = f"worker-startup-test — {datetime.utcnow().isoformat()}"
        cur.execute(
            "INSERT INTO alerts (type, message, timestamp) VALUES (%s, %s, %s)",
            ("startup-test", msg, datetime.utcnow())
        )
        conn.commit()
        cur.close()
        conn.close()
        print("🟢 DB test insert succeeded:", msg)
    except Exception as e:
        print("🔴 DB test insert FAILED:")
        traceback.print_exc()

def main_loop():
    while True:
        print(f"🐱 CryptoCat Worker heartbeat {datetime.utcnow().isoformat()}")
        time.sleep(60)

if __name__ == "__main__":
    print("Worker starting...", datetime.utcnow().isoformat())
    # Run DB test once at startup
    test_db_insert_once()
    # Then continue normal loop
    main_loop()
