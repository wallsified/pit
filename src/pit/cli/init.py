import click
from ..storage.init import init_repo
from pathlib import Path


@click.group()
def cli():
    """
    Pit significa "Python Information Tracker".
    Git-alike, pero creado en Python.
    """
    pass


@cli.command()
def init():
    """
    Inicializa un nuevo repositorio de Pit.
    Por defecto, se inicializa en el directorio actual de trabajo.
    """
    repo_path = Path.cwd()
    init_repo(repo_path)


# WIP
@cli.command()
@click.option("--file", help="Ruta del archivo a agregar")
def add(file):
    """
    Agrega un archivo al repositorio de Pit.
    """
    if file:
        file_path = Path(file)
        if file_path.exists():
            # Aquí iría la lógica para agregar el archivo al repositorio
            click.echo(f"Archivo {file} agregado al repositorio.")
        else:
            click.echo(f"El archivo {file} no existe.")
    else:
        click.echo("Por favor, proporciona la ruta del archivo a agregar.")
