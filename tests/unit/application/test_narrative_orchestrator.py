# -*- coding: utf-8 -*-
"""
tests/unit/application/test_narrative_orchestrator.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NarrativeOrchestrator 턴 오케스트레이션 및 롤백 통합 단위 테스트 (Zero-Dependency unittest)
"""

import gc
import os
import tempfile
import unittest

from src.domain.character import Character, LowenArmor
from src.infrastructure.database.db_manager import DatabaseManager
from src.infrastructure.database.repositories import CharacterRepository, TurnHistoryRepository
from src.application.narrative_orchestrator import NarrativeOrchestrator


class TestNarrativeOrchestrator(unittest.TestCase):

    def setUp(self):
        """격리된 임시 DB 및 오케스트레이터 구성"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db_manager = DatabaseManager(db_path=self.temp_db.name)
        self.char_repo = CharacterRepository(self.db_manager)
        self.turn_repo = TurnHistoryRepository(self.db_manager)

        self.character = Character(
            name="카타리나",
            title="마법학회장",
            faction="학술원",
            armor_type=LowenArmor.RIGID,
        )
        self.char_repo.save(self.character)

        self.orchestrator = NarrativeOrchestrator(
            character=self.character,
            char_repo=self.char_repo,
            turn_repo=self.turn_repo,
        )

    def tearDown(self):
        del self.orchestrator
        del self.char_repo
        del self.turn_repo
        del self.db_manager
        gc.collect()
        try:
            if os.path.exists(self.temp_db.name):
                os.remove(self.temp_db.name)
        except OSError:
            pass

    def test_execute_turn_and_state_updates(self):
        """1턴 진행 시 텐서 및 생체 수치 갱신 검증"""
        result = self.orchestrator.execute_turn('목을 잡으며 "순순히 항복해"라고 압박한다.')

        self.assertEqual(result.turn_number, 1)
        self.assertEqual(result.action_frame.primary_tensor, "04_cervical")
        self.assertLess(result.character.ego_durability, 100.0)
        self.assertGreater(result.character.neural_taint, 0.0)
        self.assertIn("04_cervical", result.character.tensors.active_spotlights)
        self.assertGreater(len(result.somatic_events), 0)

    def test_rollback_after_turn(self):
        """턴 실행 후 Undo 롤백 수행 시 이전 상태로 복귀 검증"""
        initial_ego = self.character.ego_durability
        initial_taint = self.character.neural_taint

        # 턴 1 실행
        self.orchestrator.execute_turn("위협한다.")
        self.assertNotEqual(self.character.ego_durability, initial_ego)

        # 롤백 수행
        restored = self.orchestrator.rollback()
        self.assertIsNotNone(restored)
        self.assertEqual(restored.ego_durability, initial_ego)
        self.assertEqual(restored.neural_taint, initial_taint)
        self.assertEqual(self.orchestrator.current_turn, 1)


if __name__ == "__main__":
    unittest.main()
