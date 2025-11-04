import os
import psycopg2

# connect to Supabase (Postgres)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)
