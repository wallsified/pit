import hashlib
import sqlite3
from datetime import datetime

from pit.storage.database import DB_PATH


def generate_hash(content: str) -> str:
    return hashlib.sha1(content.encode()).hexdigest()[:8]  # Short hash como Git


def create_commit(message: str):
    with sqlite3.connect(DB_PATH) as conn:
        # 1. Obtener archivos staged
        files = conn.execute("SELECT path FROM tracked_files WHERE is_staged=TRUE").fetchall()
        if not files:
            raise ValueError("No hay archivos staged para commit.")

        # 2. Generar hash único (simplificado)
        commit_hash = generate_hash(message + str(datetime.now()))

        # 3. Guardar commit
        conn.execute("INSERT INTO commits (hash, message) VALUES (?, ?)", (commit_hash, message))
        conn.execute("UPDATE tracked_files SET is_staged=FALSE")
    return commit_hash
