import pytest
from src.pit.core.status import get_status
from src.pit.storage.init import init_repo
from src.pit.storage.add import add_file


@pytest.fixture
def temp_repo(tmp_path):
    """Crea un repositorio temporal para las pruebas."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    init_repo(repo_path)
    return repo_path


def test_get_status(temp_repo, caps):
    """Prueba que get_status liste correctamente los archivos en el área de staging."""
    # Crear un archivo de prueba
    test_file = temp_repo / "test_file.txt"
    with test_file.open("w") as f:
        f.write("Contenido de prueba")

    # Agregar el archivo al área de staging
    add_file(temp_repo, test_file)

    # Ejecutar get_status y capturar la salida
    get_status(temp_repo)
    captured = caps.readouterr()

    # Verificar que el archivo aparece en la salida
    assert "Archivos en el área de staging:" in captured.out
    assert str(test_file) in captured.out
    assert "Recuerda hacer un commit para confirmar tus cambios." in captured.out
