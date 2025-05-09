from pathlib import Path
import sqlite3


def remove_file(repo_path: Path, file_path: Path):
    """
    Elimina un archivo del área (o tabla) de staging.
    """
    db_path = repo_path / ".pit" / "pit.db"
    if not db_path.exists():
        raise FileNotFoundError("El repositorio no está inicializado.")

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM staging WHERE path = ?
                """,
                (str(file_path),),
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error al eliminar el archivo al área de staging: {e}")
