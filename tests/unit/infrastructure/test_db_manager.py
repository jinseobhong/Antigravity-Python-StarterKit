# -*- coding: utf-8 -*-
"""
tests/unit/infrastructure/test_db_manager.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SQLite DatabaseManager 및 Repositories CRUD 단위 테스트 (Zero-Dependency unittest)
"""

import gc
import os
import tempfile
import unittest

from src.domain.character import Character, LowenArmor
from src.infrastructure.database.db_manager import DatabaseManager
from src.infrastructure.database.repositories import CharacterRepository, TurnHistoryRepository


class TestDatabaseInfrastructure(unittest.TestCase):

    def setUp(self):
        """격리된 임시 SQLite 데이터베이스 생성"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db_manager = DatabaseManager(db_path=self.temp_db.name)
        self.char_repo = CharacterRepository(self.db_manager)
        self.turn_repo = TurnHistoryRepository(self.db_manager)

    def tearDown(self):
        """임시 파일 정리 (Windows 파일 락 안전 해제)"""
        del self.char_repo
        del self.turn_repo
        del self.db_manager
        gc.collect()
        try:
            if os.path.exists(self.temp_db.name):
                os.remove(self.temp_db.name)
        except OSError:
            pass

    def test_schema_and_master_somatic_seeding(self):
        """테이블 스키마 생성 및 마스터 텐서 시딩 검증"""
        with self.db_manager.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM tensor_definitions;")
            count = cur.fetchone()[0]
            self.assertGreater(count, 0)

    def test_character_repository_save_and_find(self):
        """Character 엔티티 저장 및 seed_hash 기준 복원 검증"""
        char = Character(
            name="실비아",
            title="제국 근위대장",
            faction="황실",
            armor_type=LowenArmor.CONTROLLER,
            traits={"욕망": "완전한 통제", "결핍": "취약성 공포"},
        )
        char.apply_damage_and_taint(ego_damage=10.0, taint_gain=40.0)

        char_id = self.char_repo.save(char)
        self.assertGreater(char_id, 0)

        restored = self.char_repo.find_by_seed_hash(char.seed_hash)
        self.assertIsNotNone(restored)
        self.assertEqual(restored.name, "실비아")
        self.assertEqual(restored.armor_type, LowenArmor.CONTROLLER)
        self.assertEqual(restored.ego_durability, 90.0)
        self.assertEqual(restored.neural_taint, 40.0)
        self.assertEqual(restored.traits["욕망"], "완전한 통제")

    def test_turn_history_repository(self):
        """턴 히스토리 원장 기록 및 조회 검증"""
        char = Character(
            name="루나",
            title="마법사",
            faction="학회",
            armor_type=LowenArmor.DEPRIVED,
        )
        char_id = self.char_repo.save(char)

        turn_id = self.turn_repo.record_turn(
            character_id=char_id,
            turn_number=1,
            user_action="다가가서 말을 건넨다",
            vector_type="DEVOTION_COMFORT",
            narrative_prose="그녀는 조심스럽게 고개를 들었다.",
            ego_durability=100.0,
            neural_taint=0.0,
            pressure_stage="Stage 1",
        )
        self.assertGreater(turn_id, 0)

        history = self.turn_repo.get_history(char_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["user_action"], "다가가서 말을 건넨다")


if __name__ == "__main__":
    unittest.main()
