# utils/db_utils.py
import psycopg2
from config.settings import DB_CONFIG

def get_db_connection():
    """Create and return a database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"❌ Database connection error: {e}")
        return None

def insert_page_data(url, status, response_body, headers, data):
    """Insert scraped data into the database."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO pages (url, response_status, response_body, response_headers, data)
                VALUES (%s, %s, %s, %s, %s) RETURNING uuid;
            """, (url, status, response_body, headers, data))
            
            page_id = cur.fetchone()[0]
            conn.commit()
            print(f"✅ Data inserted successfully with ID: {page_id}")
    except psycopg2.Error as e:
        print(f"❌ Error inserting data: {e}")
    finally:
        conn.close()
