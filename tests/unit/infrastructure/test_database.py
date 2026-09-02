"""
tests/unit/infrastructure/test_database.py — SQLite 데이터베이스 매니저 단위 테스트
AAA 패턴 (Arrange - Act - Assert) 준수
"""

import unittest
import tempfile
from pathlib import Path
from src.infrastructure.database.connection import DatabaseManager

class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / 'test_app.db'
        self.db = DatabaseManager(self.db_path)
        self.db.init_schema()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_database_connection_and_wal_mode(self):
        # Arrange & Act
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode;")
            mode = cursor.fetchone()[0]
            cursor.execute("PRAGMA foreign_keys;")
            fk = cursor.fetchone()[0]
        finally:
            conn.close()

        # Assert
        self.assertEqual(mode.lower(), 'wal')
        self.assertEqual(fk, 1)

    def test_transaction_rollback_on_error(self):
        # Arrange
        with self.db.transaction() as conn:
            conn.execute("CREATE TABLE sample (id TEXT PRIMARY KEY, val TEXT);")

        try:
            with self.db.transaction() as conn:
                conn.execute("INSERT INTO sample (id, val) VALUES ('1', 'Alpha');")
                raise RuntimeError("Simulated failure inside transaction")
        except RuntimeError:
            pass

        # Act & Assert
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sample WHERE id = '1'")
            row = cursor.fetchone()
            self.assertIsNone(row)  # Rollback succeeded

if __name__ == '__main__':
    unittest.main()
