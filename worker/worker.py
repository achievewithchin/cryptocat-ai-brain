# worker/worker.py
import os
import socket
import traceback
import psycopg2
from datetime import datetime, timezone

DATABASE_URL = os.getenv("DATABASE_URL")

def try_connect_dsn(dsn):
    try:
        conn = psycopg2.connect(dsn, connect_timeout=10, sslmode="require")
        return conn
    except Exception:
        traceback.print_exc()
        return None

def try_connect_ip(host_ip, user, password, dbname="postgres", port=5432):
    try:
        conn = psycopg2.connect(host=host_ip, port=port, user=user, password=password, dbname=dbname, connect_timeout=10, sslmode="require")
        return conn
    except Exception:
        traceback.print_exc()
        return None

def parse_dsn(dsn):
    # crude parse: postgresql://user:pass@host:port/dbname?params
    import re
    m = re.match(r'postgres(?:ql)?://([^:]+):([^@]+)@([^:/?]+)(?::(\d+))?/(.*?)($|\?)', dsn)
    if not m:
        return None
    user, password, host, port, dbname = m.group(1), m.group(2), m.group(3), m.group(4) or "5432", m.group(5)
    return {"user": user, "password": password, "host": host, "port": int(port), "dbname": dbname}

def resolve_ipv4(hostname):
    try:
        return [ai[4][0] for ai in socket.getaddrinfo(hostname, None) if ai[0] == socket.AF_INET]
    except Exception:
        return []

def test_supabase_connection():
    print("Testing DSN:", "SET" if DATABASE_URL else "NOT SET")
    if not DATABASE_URL:
        print("DATABASE_URL missing in env")
        return False

    # 1) try DSN as-is (forces sslmode require via connect)
    print("Trying DSN connect...")
    conn = try_connect_dsn(DATABASE_URL)
    if conn:
        print("Connected via DSN")
        conn.close()
        return True

    # 2) try IPv4 fallback
    info = parse_dsn(DATABASE_URL)
    if not info:
        print("Failed to parse DSN for fallback")
        return False

    print("Resolving IPv4 for host:", info["host"])
    ipv4s = resolve_ipv4(info["host"])
    print("IPv4 addresses:", ipv4s)
    for ip in ipv4s:
        print("Attempting connect to IPv4:", ip)
        conn = try_connect_ip(ip, info["user"], info["password"], dbname=info["dbname"], port=info["port"])
        if conn:
            print("Connected via IPv4", ip)
            conn.close()
            return True

    print("All connection attempts failed")
    return False

def main():
    print("Worker starting...", datetime.now(timezone.utc).isoformat())
    ok = test_supabase_connection()
    if ok:
        print("✅ Supabase reachable")
    else:
        print("❌ Supabase NOT reachable")

if __name__ == "__main__":
    main()
