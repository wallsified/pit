import sqlite3
import unittest
from pathlib import Path

from src.pit.storage.init import init_repo
from src.pit.storage.add import add_file

repo_path = Path("status_test")
repo_path.mkdir(parents=True, exist_ok=True)


class TestPitStatus(unittest.TestCase):
    def setUp(self) -> None:
        """
        Configura un repositorio temporal en memoria
        para realizar pruebas a pit status.
        """
        init_repo(repo_path)
        self.test_file = repo_path / "test_file.txt"
        with self.test_file.open("w") as f:
            f.write("probando 'pit status'")
        add_file(repo_path, self.test_file)

    def test_status(self) -> None:
        """
        Prueba que el estado del repositorio se obtenga correctamente.
        """
        db_path = repo_path / ".pit" / "pit.db"
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT path FROM staging")
            result = cursor.fetchall()

        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result), 1)

    def tearDown(self) -> None:
        """
        Limpia el repositorio creado temporalmente tras las pruebas.
        """
        db_path = repo_path / ".pit" / "pit.db"
        if db_path.exists():
            try:
                with sqlite3.connect(db_path) as conn:
                    conn.close()
            except sqlite3.Error as e:
                print(f"Error al cerrar la base de datos {e}")


suite = unittest.TestLoader().loadTestsFromTestCase(TestPitStatus)
unittest.TextTestRunner(verbosity=2).run(suite)
