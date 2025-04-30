import click
from ..storage.database import init_db


@click.group()
def cli():
    """CLI para Pit."""
    pass


@cli.command()
def init():
    """Inicializa un nuevo repositorio de Pit."""
    init_db()
    click.echo("Repositorio de Pit inicializado")
