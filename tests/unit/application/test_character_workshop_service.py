# -*- coding: utf-8 -*-
"""
tests/unit/application/test_character_workshop_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CharacterWorkshopService 4대 로스터 시딩 및 JSON I/O 단위 테스트 (Zero-Dependency unittest)
"""

import gc
import os
import tempfile
import unittest

from src.domain.character import Character, LowenArmor
from src.infrastructure.database.db_manager import DatabaseManager
from src.infrastructure.database.repositories import CharacterRepository
from src.application.character_workshop_service import CharacterWorkshopService, DEFAULT_ROSTER


class TestCharacterWorkshopService(unittest.TestCase):

    def setUp(self):
        """임시 DB 및 서비스 구성"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db_manager = DatabaseManager(db_path=self.temp_db.name)
        self.char_repo = CharacterRepository(self.db_manager)
        self.workshop = CharacterWorkshopService(self.char_repo)

    def tearDown(self):
        del self.workshop
        del self.char_repo
        del self.db_manager
        gc.collect()
        try:
            if os.path.exists(self.temp_db.name):
                os.remove(self.temp_db.name)
        except OSError:
            pass

    def test_default_roster_auto_seeding(self):
        """4대 대표 아키타입 자동 시딩 검증"""
        for item in DEFAULT_ROSTER:
            char = self.char_repo.find_by_seed_hash(item["seed"])
            self.assertIsNotNone(char)
            self.assertEqual(char.name, item["name"])
            self.assertEqual(char.armor_type, item["armor"])

    def test_export_master_prompt(self):
        """마스터 시스템 프롬프트 컴파일 검증"""
        char = self.char_repo.find_by_seed_hash("#LILI-70G-BFFF")
        self.assertIsNotNone(char)

        prompt = self.workshop.export_master_prompt(char)
        self.assertIn("릴리스", prompt)
        self.assertIn("제1황녀", prompt)
        self.assertIn("Rigid (완벽주의 척추 방어)", prompt)
        self.assertIn("외모_특징", prompt)

    def test_export_and_import_json(self):
        """JSON 파일 내보내기 및 가져오기 무결성 검증"""
        char = self.char_repo.find_by_seed_hash("#AIRA-70G-9A4F")
        self.assertIsNotNone(char)

        filename, json_str = self.workshop.export_json(char)
        self.assertIn("에이라", filename)
        self.assertIn("AIRA-70G-9A4F", filename)

        # 역직렬화
        restored = self.workshop.import_json(json_str)
        self.assertEqual(restored.name, "에이라")
        self.assertEqual(restored.seed_hash, "#AIRA-70G-9A4F")
        self.assertEqual(restored.armor_type, LowenArmor.ENDURER)


if __name__ == "__main__":
    unittest.main()
