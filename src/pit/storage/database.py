import sqlite3
from pathlib import Path

# Ruta absoluta a ~/.pit/pit.db
DB_DIR = Path.home() / ".pit"
DB_PATH = DB_DIR / "pit.db"


def init_db():
    # Crear directorio si no existe
    DB_DIR.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tracked_files (
                path TEXT PRIMARY KEY,
                last_modified REAL,
                is_staged BOOLEAN DEFAULT FALSE
            )""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS commits (
                hash TEXT PRIMARY KEY,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")
