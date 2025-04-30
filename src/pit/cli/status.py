import sqlite3

import click

from ..storage.database import init_db, DB_PATH


@click.command()
def status():
    """Muestra archivos trackeados y cambios pendientes."""
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        files = conn.execute("SELECT path, is_staged FROM tracked_files").fetchall()

    if not files:
        click.echo("No hay archivos trackeados.")
        return

    for path, is_staged in files:
        new_status = "STAGED" if is_staged else "UNSTAGED"
        click.echo(f"{new_status}: {path}")
