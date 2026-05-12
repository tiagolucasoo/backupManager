import sqlite3
from config.theme import DB_FILE

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perfis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE,
            host TEXT,
            usuario TEXT,
            senha BLOB,
            bancos TEXT DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()