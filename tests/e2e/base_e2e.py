"""
tests/e2e/base_e2e.py — 종단간(E2E) 테스트 베이스 프레임워크
모든 E2E 테스트는 독립된 임시 SQLite WAL 데이터베이스 환경에서 실행됩니다.
"""

import unittest
import tempfile
from pathlib import Path
from src.infrastructure.database.connection import DatabaseManager


class BaseE2ETestCase(unittest.TestCase):
    """격리된 런타임 환경과 DB 매니저를 제공하는 E2E 베이스 테스트 클래스"""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "e2e_test.db"
        self.db = DatabaseManager(self.db_path)
        self.db.init_schema()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()
