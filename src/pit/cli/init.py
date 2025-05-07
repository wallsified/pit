import click

from ..storage.add import add_file
from ..storage.init import init_repo
from pathlib import Path

from ..storage.remove import remove_file


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


# El nombre de los argumentos debe ser el mismo que el nombre del argumento
# en la función, de lo contrario no se pasará el argumento a la función.
@cli.command()
@click.argument("file", required=True)
def add(file):
    """
    Agrega un archivo al area de staging de Pit.
    """
    if file:
        file_path = Path(file)
        if file_path.exists():
            repo_path = Path.cwd()
            add_file(repo_path, file_path)
            click.echo(f"Archivo {file} agregado al repositorio.\n")
        else:
            click.echo(f"El archivo {file} no existe.\n")
    else:
        click.echo("Por favor, proporciona la ruta del archivo a agregar.")


@cli.command()
@click.argument("file", required=True)
def remove(file):
    """
    Borra un archivo del area de staging de Pit.
    """
    if file:
        file_path = Path(file)
        if file_path.exists():
            repo_path = Path.cwd()
            remove_file(repo_path, file_path)
            click.echo(f"Archivo {file} eliminado del repositorio.\n")
        else:
            click.echo(f"El archivo {file} no existe.")
    else:
        click.echo("Por favor, proporciona la ruta del archivo a eliminar.\n")
