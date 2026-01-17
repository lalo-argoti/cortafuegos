import sqlite3

DB_PATH = "/data/login_attempts.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open("models.sql") as f:
        conn.executescript(f.read())
    conn.close()
