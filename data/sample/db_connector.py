import sqlite3

def connect_db(path="app.db"):
    """Connect to a SQLite database."""
    conn = sqlite3.connect(path)
    return conn

def create_table(conn):
    """Create a demo table for logs."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY, message TEXT)"
    )
    conn.commit()
