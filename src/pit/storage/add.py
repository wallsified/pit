import hashlib
import sqlite3
from pathlib import Path


def calculate_hash(content: bytes) -> str:
    """
    Calcula el hash SHA-256 del contenido de un archivo.

    Args:
        content (bytes): Contenido del archivo en formato binario.

    Returns:
        str: Hash SHA-256 del contenido.
    """
    return hashlib.sha256(content).hexdigest()


def pit_add(path: str, content: bytes):
    """
    Añade un archivo al área de staging del repositorio Pit.

    Este método calcula el hash del contenido del archivo y lo guarda en la tabla
    `staging` de la base de datos del repositorio.

    Args:
        path (str): Ruta relativa del archivo dentro del repositorio.
        content (bytes): Contenido del archivo en formato binario.

    Side Effects:
        - Inserta o reemplaza la entrada correspondiente en la tabla `staging`.
        - Guarda los cambios en la base de datos.

    Raises:
        sqlite3.Error: Si ocurre un error al interactuar con la base de datos.
    """
    hash_value = calculate_hash(content)
    repo_path = Path.cwd()  # Asumiendo que el repositorio está en el directorio actual
    try:
        with sqlite3.connect(repo_path / ".pit" / "pit.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                REPLACE INTO staging (path, content, hash) VALUES (?, ?, ?)
            """,
                (path, content, hash_value),
            )
            conn.commit()
        print("Archivos añadidos al área de staging")
    except sqlite3.SQLITE_CORRUPT_INDEX:
        print(
            "Error: La base de datos está corrupta. Intenta repararla o restaurar desde un respaldo."
        )
    # Suponiendo que hagamos un pit rm para eliminar el archivo a posterori
    except sqlite3.IntegrityError:
        print(
            "Error: Ya existe un archivo con la misma ruta en el área de staging. Usa 'pit rm' para eliminarlo antes de añadir uno nuevo."
        )
    except sqlite3.OperationalError:
        print("Error: No se pudo acceder a la base de datos. ¿Aún existe pit.db?")
    except sqlite3.SQLITE_CONSTRAINT_FOREIGNKEY:
        print(
            "Error: Error de restricción de clave foránea. Asegúrate de que la tabla 'staging' esté definida correctamente."
        )
