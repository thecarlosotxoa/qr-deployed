# backend/utils/db.py

import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def get_db_connection():
    """Function to establish a database connection."""
    conn = psycopg2.connect(Config.DATABASE_URL, cursor_factory=RealDictCursor)
    return conn
