import unittest
import sqlite3
from pathlib import Path
from src.pit.storage.add import add_file
from src.pit.storage.remove import remove_file
from src.pit.storage.init import init_repo
from shutil import rmtree


class TestPitRemove(unittest.TestCase):
    def setUp(self):
        """Configura un repositorio temporal para las pruebas."""
        self.repo_path = Path("remove_test")
        self.repo_path.mkdir(exist_ok=True)
        init_repo(self.repo_path)

        self.test_file = self.repo_path / "test_file.txt"
        with self.test_file.open("w") as f:
            f.write("probando 'pit remove'")

    def test_add_file(self):
        """Prueba que un archivo se agregue correctamente al área de staging."""
        add_file(self.repo_path, self.test_file)

        db_path = self.repo_path / ".pit" / "pit.db"
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT path FROM staging WHERE path = ?", (str(self.test_file),))
            result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], str(self.test_file))

    def test_remove_file(self):
        """Prueba que un archivo se elimine correctamente del área de staging."""
        # Agregar el archivo primero
        add_file(self.repo_path, self.test_file)

        # Luego eliminarlo
        remove_file(self.repo_path, self.test_file)

        db_path = self.repo_path / ".pit" / "pit.db"
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT path FROM staging WHERE path = ?", (str(self.test_file),))
            result = cursor.fetchone()

        self.assertIsNone(result)

    def tearDown(self):
        """Limpia el repositorio temporal después de las pruebas."""
        rmtree(self.repo_path, ignore_errors=True)


# Ejecución de las pruebas unitarias
suite = unittest.TestLoader().loadTestsFromTestCase(TestPitRemove)
unittest.TextTestRunner(verbosity=2).run(suite)
