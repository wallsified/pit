import sqlite3
import click
from ..storage.database import DB_PATH


@click.command()
def history():
    """Muestra el historial de commits."""
    with sqlite3.connect(DB_PATH) as conn:
        commits = conn.execute(
            "SELECT hash, message, timestamp FROM commits ORDER BY timestamp DESC"
        ).fetchall()

    for idx, (hash_, message, timestamp) in enumerate(commits, 1):
        click.echo(f"{idx}. [{hash_[:7]}] {message} ({timestamp})")
