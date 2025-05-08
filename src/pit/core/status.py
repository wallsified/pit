from pathlib import Path
import sqlite3


def get_status(repo_path: Path):
    """
    Obtiene el estado del repositorio.
    """
    db_path = repo_path / ".pit" / "pit.db"
    if not db_path.exists():
        raise FileNotFoundError("El repositorio no está inicializado.")

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT path FROM staging
                """
            )
            rows = cursor.fetchall()
            print("Archivos en el área de staging:\n")
            for path in rows:
                print(f"- {path[0]}")
            print("Recuerda hacer un commit para confirmar tus cambios.")

    except sqlite3.Error as e:
        print(
            f"Error al obtener el estado del repositorio: {e}. ¿El repositorio está inicializado?."
        )
