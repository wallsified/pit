import click
from pit.core.commit import create_commit


@click.command()
@click.argument("message")
def commit(message):
    """Guarda los cambios staged en un nuevo commit."""
    try:
        commit_hash = create_commit(message)
        click.echo(f"Commit [{commit_hash[:7]}] creado: {message}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
