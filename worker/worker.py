import os
import psycopg2
from datetime import datetime, timezone

# Load DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

def test_supabase_connection():
    print("🐱 Testing connection to Supabase at:", DATABASE_URL)
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Insert a test alert row
        cur.execute("""
            INSERT INTO alerts (type, message, metadata, importance, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            "startup-test",
            f"worker-startup-test — {datetime.now(timezone.utc).isoformat()}",
            '{}',
            'low',
            datetime.now(timezone.utc)
        ))

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Supabase test insert successful!")

    except Exception as e:
        print("❌ Database test failed:", e)

def main():
    print("Worker starting...", datetime.now(timezone.utc).isoformat())
    test_supabase_connection()

if __name__ == "__main__":
    main()
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
