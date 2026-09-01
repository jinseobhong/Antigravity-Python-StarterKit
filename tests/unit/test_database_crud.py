# -*- coding: utf-8 -*-
"""
tests/unit/test_database_crud.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unit Test Suite for Database CRUD Operations
"""

import unittest
import tempfile
from src.infrastructure.database.db_manager import DBManager
from src.infrastructure.database.repositories import CharacterRepository, TurnLedgerRepository
from src.domain.character import Character


class TestDatabaseCRUD(unittest.TestCase):
    """Database CRUD 단위 테스트"""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = f"{self.temp_dir.name}/test_crud.db"
        self.db_manager = DBManager(self.db_path)
        self.char_repo = CharacterRepository(self.db_manager)
        self.turn_repo = TurnLedgerRepository(self.db_manager)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_seed_and_retrieve_characters(self):
        # 1. 캐릭터 저장
        lilith = self.char_repo.save(Character.create_lilith())
        aira = self.char_repo.save(Character.create_aira())
        self.char_repo.set_active(lilith.id)

        all_chars = self.char_repo.list_all()
        self.assertEqual(len(all_chars), 2)

        # 2. 활성 캐릭터(릴리스) 확인
        active = self.char_repo.get_active()
        self.assertIsNotNone(active)
        self.assertEqual(active.name, "릴리스")
        self.assertEqual(active.gene_seed.seed_hash, "#LILI-70G-BFFF")

        # 3. 캐릭터 스위칭(에이라 활성화)
        self.char_repo.set_active(aira.id)
        new_active = self.char_repo.get_active()
        self.assertEqual(new_active.name, "에이라")

    def test_save_and_update_character(self):
        custom = Character.create_sylvia()
        custom.name = "실비아_수정본"
        saved = self.char_repo.save(custom)
        self.assertIsNotNone(saved.id)

        fetched = self.char_repo.get_by_id(saved.id)
        self.assertEqual(fetched.name, "실비아_수정본")
        self.assertEqual(fetched.traits.archetype_class, "Deprived (가련한 유기 불안)")

        # 업데이트
        fetched.traits.gauges.trust = 85
        self.char_repo.save(fetched)
        updated = self.char_repo.get_by_id(saved.id)
        self.assertEqual(updated.traits.gauges.trust, 85)

    def test_turn_ledger_recording_and_history(self):
        lilith = self.char_repo.save(Character.create_lilith())

        # 1턴 기록
        self.turn_repo.record_turn(
            character_id=lilith.id,
            turn_number=1,
            user_action="릴리스의 손을 감싸 쥔다.",
            narrative_response="릴리스가 놀라며 손을 뺀다.",
            meta_status={"turn": 1},
            somatic_ledger={"l1": "경직", "l2": "열감", "l3": "동요"},
            gauges={"trust": 25, "submission": 22}
        )

        history = self.turn_repo.get_history(lilith.id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["user_action"], "릴리스의 손을 감싸 쥔다.")


if __name__ == "__main__":
    unittest.main()
