"""
tests/e2e/test_smoke_e2e.py — E2E 인프라 스모크 및 라이프사이클 관통 테스트
"""

import unittest
from tests.e2e.base_e2e import BaseE2ETestCase


class TestE2ESmoke(BaseE2ETestCase):
    """E2E 격리 환경 및 트랜잭션 수명주기 스모크 검증"""

    def test_e2e_isolated_database_lifecycle(self):
        # 1. Arrange & Act: 테이블 생성 및 데이터 삽입
        with self.db.transaction() as conn:
            conn.execute("CREATE TABLE e2e_session (session_id TEXT PRIMARY KEY, status TEXT);")
            conn.execute("INSERT INTO e2e_session (session_id, status) VALUES ('SESS_01', 'ACTIVE');")

        # 2. Assert: 데이터 영구 보존 확인
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM e2e_session WHERE session_id = 'SESS_01';")
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row["status"], "ACTIVE")


if __name__ == "__main__":
    unittest.main()
