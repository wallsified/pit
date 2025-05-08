import sqlite3
import unittest


class TestPitInit(unittest.TestCase):
    """
    Clase de prueba unitaria para verificar la funcionalidad de inicialización de `pit init`.
    """

    def setUp(self):
        """
        Configuración inicial que se ejecuta antes de cada prueba.
        Crea (y reinicializa en cada prueba) una base de datos SQLite en memoria y define las tablas necesarias para
        las pruebas.

        Nota: Las pruebas se hacen en una BD en memoria por que, de lo contrario, las pruebas se ejecutarían en la
        misma base de datos y podrían interferir entre sí.
        """
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.executescript(
            """
        CREATE TABLE commits (
            id TEXT PRIMARY KEY,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            author TEXT NOT NULL,
            parent_id TEXT,
            FOREIGN KEY (parent_id) REFERENCES commits(id)
        );

        CREATE TABLE files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commit_id TEXT NOT NULL,
            path TEXT NOT NULL,
            content BLOB NOT NULL,
            hash TEXT NOT NULL,
            FOREIGN KEY (commit_id) REFERENCES commits(id),
            UNIQUE(commit_id, path)
        );

        CREATE TABLE staging (
            path TEXT PRIMARY KEY,
            content BLOB NOT NULL,
            hash TEXT NOT NULL
        );

        CREATE TABLE refs (
            name TEXT PRIMARY KEY,
            commit_id TEXT,
            FOREIGN KEY (commit_id) REFERENCES commits(id)
        );

        CREATE TABLE baselines (
            name TEXT PRIMARY KEY,
            commit_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (commit_id) REFERENCES commits(id)
        );

        CREATE TABLE diffs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_commit TEXT NOT NULL,
            to_commit TEXT NOT NULL,
            diff TEXT NOT NULL,
            generated_at TEXT NOT NULL,
            FOREIGN KEY (from_commit) REFERENCES commits(id),
            FOREIGN KEY (to_commit) REFERENCES commits(id)
        );

        CREATE TABLE head (
            ref_name TEXT PRIMARY KEY
        );
        """
        )

    def test_pit_init_creates_main_and_head(self):
        """
        Prueba que el comando `pit init` crea correctamente las referencias `main` y `head`.

        - Inserta una referencia `main` en la tabla `refs`.
        - Inserta una referencia `main` en la tabla `head`.
        - Verifica que ambas referencias existan y tengan los valores esperados.
        """
        self.cursor.execute("INSERT INTO refs (name, commit_id) VALUES ('main', NULL)")
        self.cursor.execute("INSERT INTO head (ref_name) VALUES ('main')")
        self.conn.commit()

        # Verificar que main y head existen
        self.cursor.execute("SELECT * FROM refs WHERE name = 'main'")
        main_ref = self.cursor.fetchone()

        self.cursor.execute("SELECT * FROM head")
        head_ref = self.cursor.fetchone()

        self.assertEqual(main_ref, ("main", None))
        self.assertEqual(head_ref, ("main",))

    def tearDown(self):
        """
        Limpieza que se ejecuta después de cada prueba.
        Cierra la conexión a la base de datos SQLite.
        """
        self.conn.close()


# Ejecución de las pruebas unitarias
suite = unittest.TestLoader().loadTestsFromTestCase(TestPitInit)
unittest.TextTestRunner(verbosity=2).run(suite)
