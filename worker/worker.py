import os
import psycopg2
from datetime import datetime, timezone

DATABASE_URL = os.getenv("DATABASE_URL")

def test_supabase_connection():
    print("🐱 Testing connection to Supabase at:", DATABASE_URL)
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        msg = f"worker-startup-test — {datetime.now(timezone.utc).isoformat()}"
        cur.execute("""
            INSERT INTO alerts (type, message, metadata, importance, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            "startup-test",
            msg,
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
