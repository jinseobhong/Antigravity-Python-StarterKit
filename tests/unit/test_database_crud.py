# -*- coding: utf-8 -*-
"""
tests/unit/test_database_crud.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unit Tests: SQLite WAL 데이터베이스 및 Character/TurnLedger 리포지토리 실물 CRUD 검증
"""

import os
import unittest
import tempfile
from pathlib import Path

from src.infrastructure.database.db_manager import DBManager
from src.infrastructure.database.repositories import CharacterRepository, TurnLedgerRepository
from src.domain.character import Character


class TestDatabaseCRUD(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_dir.name) / "test_abyss.db")
        self.db_manager = DBManager(self.db_path)
        self.char_repo = CharacterRepository(self.db_manager)
        self.turn_repo = TurnLedgerRepository(self.db_manager)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_seed_and_retrieve_characters(self):
        # 1. 4대 기본 캐릭터 시딩
        self.char_repo.seed_defaults_if_empty()
        all_chars = self.char_repo.list_all()
        self.assertEqual(len(all_chars), 4)

        # 2. 활성 캐릭터(릴리스) 확인
        active = self.char_repo.get_active()
        self.assertIsNotNone(active)
        self.assertEqual(active.name, "릴리스")
        self.assertEqual(active.gene_seed.seed_hash, "#LILI-70G-BFFF")

        # 3. 캐릭터 스위칭(에이라 활성화)
        aira = next(c for c in all_chars if c.name == "에이라")
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
        self.char_repo.seed_defaults_if_empty()
        lilith = self.char_repo.get_active()

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

        # 턴 삭제 (Undo)
        removed = self.turn_repo.remove_last_turn(lilith.id)
        self.assertIsNotNone(removed)
        self.assertEqual(len(self.turn_repo.get_history(lilith.id)), 0)


if __name__ == "__main__":
    unittest.main()
