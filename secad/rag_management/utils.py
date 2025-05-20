import psycopg2
import hashlib
import os
from dotenv import load_dotenv
load_dotenv()


def file_exists_in_catalog(db_config, file_hash, collection):
    catalog_table = os.getenv("CATALOG_TABLE")
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 1 FROM {catalog_table} WHERE file_hash = %s AND collection = %s
    """, (file_hash, collection))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def update_catalog(db_config, details: dict):
    catalog_table = os.getenv("CATALOG_TABLE")
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {catalog_table} (file_hash, metadata, collection)
        VALUES (%s, %s, %s)
    """, (details["file_hash"], details["metadata"], details["collection"]))
    conn.commit()
    cursor.close()
    conn.close()

def get_file_hash(uploaded_file):
    """Generate a SHA256 hash for the uploaded file."""
    hasher = hashlib.new("sha256")
    content = uploaded_file.getvalue()
    hasher.update(content)
    return hasher.hexdigest()



    
