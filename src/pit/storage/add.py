import hashlib
from pathlib import Path
import sqlite3


def add_file(repo_path: Path, file_path: Path):
    """
    Agrega un archivo al área (o tabla) de staging.
    """
    db_path = repo_path / ".pit" / "pit.db"
    if not db_path.exists():
        raise FileNotFoundError("El repositorio no está inicializado.")

    # Leer el contenido del archivo
    with file_path.open("rb") as f:
        content = f.read()

    # Calcular el hash del contenido
    file_hash = hashlib.sha256(content).hexdigest()

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO staging (path, content, hash)
                VALUES (?, ?, ?)
                """,
                (str(file_path), content, file_hash),
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error al agregar el archivo al área de staging: {e}")
