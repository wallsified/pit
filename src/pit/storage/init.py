import sqlite3
from pathlib import Path


def init_db(repo_path: Path):
    pit_dir = repo_path / ".pit"
    pit_dir.mkdir(exist_ok=True)
    db_path = pit_dir / "pit.db"

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.executescript("""
            -- Tabla de commits
            CREATE TABLE IF NOT EXISTS commits (
                id TEXT PRIMARY KEY,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                author TEXT NOT NULL,
                parent_id TEXT,
                FOREIGN KEY (parent_id) REFERENCES commits(id)
            );

            -- Tabla de archivos versionados
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                commit_id TEXT NOT NULL,
                path TEXT NOT NULL,
                content BLOB NOT NULL,
                hash TEXT NOT NULL,
                FOREIGN KEY (commit_id) REFERENCES commits(id),
                UNIQUE(commit_id, path)
            );

            -- Área de staging
            CREATE TABLE IF NOT EXISTS staging (
                path TEXT PRIMARY KEY,
                content BLOB NOT NULL,
                hash TEXT NOT NULL
            );

            -- Referencias (punteros simbólicos)
            CREATE TABLE IF NOT EXISTS refs (
                name TEXT PRIMARY KEY,
                commit_id TEXT,
                FOREIGN KEY (commit_id) REFERENCES commits(id)
            );

            -- Líneas base (ramas)
            CREATE TABLE IF NOT EXISTS baselines (
                name TEXT PRIMARY KEY,
                commit_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (commit_id) REFERENCES commits(id)
            );

            -- Diffs generados
            CREATE TABLE IF NOT EXISTS diffs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_commit TEXT NOT NULL,
                to_commit TEXT NOT NULL,
                diff TEXT NOT NULL,
                generated_at TEXT NOT NULL,
                FOREIGN KEY (from_commit) REFERENCES commits(id),
                FOREIGN KEY (to_commit) REFERENCES commits(id)
            );

            -- HEAD simbólico
            CREATE TABLE IF NOT EXISTS head (
                ref_name TEXT PRIMARY KEY
            );

            -- Reajustar refs y HEAD
            DELETE FROM refs;
            DELETE FROM head;
            """)
    except sqlite3.SQLITE_CANTOPEN_ISDIR:
        print(
            f"Error: No se puede abrir la base de datos en {db_path}. Asegúrate de que no sea un directorio."
        )
    except sqlite3.SQLITE_CANTOPEN_FULLPATH:
        print(
            f"Error: No se puede abrir la base de datos en {db_path}. Asegúrate de que la ruta sea correcta."
        )
    except sqlite3.SQLITE_CANTOPEN:
        print(
            f"Error: No se puede crear la base de datos en {db_path}. Asegúrate de que la ruta tenga permisos de escritura."
        )


def add_main_head_refs(repo_path: Path):
    """
    Agrega las referencias HEAD y main al repositorio.
    """
    try:
        with sqlite3.connect(repo_path / ".pit" / "pit.db") as conn:
            cursor = conn.cursor()
            cursor.executescript(
                """
                INSERT OR IGNORE INTO refs (name, commit_id) VALUES ('main', NULL);
                INSERT OR IGNORE INTO head (ref_name) VALUES ('main');
                """
            )
            conn.commit()
    except sqlite3.SQLITE_NOTFOUND:
        print(
            "Error: No se encontró la tabla de referencias. Asegúrate de que la base de datos esté inicializada correctamente."
        )
    except sqlite3.IntegrityError:
        print("Error: Ya existen referencias HEAD y main en la base de datos.")
    except sqlite3.OperationalError:
        print(
            "Error: No se pudo acceder a la base de datos. Asegúrate de que la ruta sea correcta."
        )
    except sqlite3.ProgrammingError:
        print(
            "Error: Error de programación al acceder a la base de datos. Asegúrate de que la tabla de referencias esté definida correctamente."
        )


def init_repo(repo_path: Path):
    """
    Inicializa un nuevo repositorio de Pit.
    """
    init_db(repo_path)
    add_main_head_refs(repo_path)
    print(f"Repositorio de Pit inicializado en: {repo_path}")
