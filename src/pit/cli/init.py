import click
from ..storage.init import init_repo
from pathlib import Path


@click.group()
def cli():
    """CLI para Pit."""
    pass


@cli.command()
def init():
    """Inicializa un nuevo repositorio de Pit."""
    repo_path = Path.cwd()
    init_repo(repo_path)
