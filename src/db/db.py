import psycopg2
import os

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")



def get_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,  
        user=DB_USER,       
        password=DB_PASSWORD,  
        host=DB_HOST,
        port=DB_PORT
    )
    return conn


def test_db_connection():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        conn.close()
        return f"Connected successfully! PostgreSQL version: {version[0]}"
    except Exception as e:
        return f"Connection failed: {e}"