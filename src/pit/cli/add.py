import sqlite3
import click
from pathlib import Path
from ..storage.database import init_db, DB_PATH


@click.command()
@click.argument("path", type=click.Path(exists=True))
def add(path):
    """Añade un archivo al staging area."""
    init_db()
    file_path = Path(path).resolve()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO tracked_files (path, last_modified) VALUES (?, ?)",
            (str(file_path), file_path.stat().st_mtime),
        )
    click.echo(f"{file_path} añadido al staging area")
