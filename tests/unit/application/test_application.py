# -*- coding: utf-8 -*-
"""
tests/unit/application/test_application.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Application Layer 단위 테스트
- ClassifierService, GeneSynthesisService, UndoManager, NarrativeOrchestrator
"""

import os
import unittest
from src.infrastructure.database.db_manager import DatabaseManager
from src.infrastructure.database.repositories import CharacterRepository, TurnLedgerRepository
from src.infrastructure.llm.client import MultiLLMClient
from src.application.classifier_service import ClassifierService
from src.application.gene_synthesis_service import GeneSynthesisService
from src.application.undo_manager import UndoManager
from src.application.narrative_orchestrator import NarrativeOrchestrator


class TestApplication(unittest.TestCase):

    def setUp(self):
        self.test_db_path = "test_app_spec.db"
        self.db = DatabaseManager(self.test_db_path)
        self.char_repo = CharacterRepository(self.db)
        self.turn_repo = TurnLedgerRepository(self.db)
        self.llm = MultiLLMClient()
        self.classifier = ClassifierService(self.llm)
        self.synthesis = GeneSynthesisService(self.char_repo, self.llm)

    def tearDown(self):
        if hasattr(self.db._local, "conn") and self.db._local.conn:
            self.db._local.conn.close()
            self.db._local.conn = None
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_classifier_service_boundary_resolution(self):
        """ClassifierService 제약선 및 V1/V2 궤적 도출 검증"""
        res = self.classifier.resolve_boundary_and_vectors("차가운 은발의 황녀 릴리스")
        self.assertTrue(res["seed_hash"].startswith("#LILI-70G-"))
        self.assertIn("hard_invariants", res)
        self.assertEqual(len(res["resolution_vectors"]), 2)

    def test_gene_synthesis_service_creation(self):
        """GeneSynthesisService 8-Tier Visual DNA & 유전자 합성 검증"""
        char = self.synthesis.synthesize_character(
            name="실비아",
            title="몰락 귀족 영애",
            faction="구 제국 귀족",
            hard_invariants_dict={"primary_boundary": "유기 불안 방어"},
            selected_vector={"vector_id": "V1", "vector_name": "방어선 고수"}
        )
        self.assertIsNotNone(char)
        self.assertEqual(char.name, "실비아")
        self.assertTrue(char.visual_dna.danbooru_prompt.startswith("1girl"))

    def test_undo_manager_push_pop(self):
        """UndoManager 스냅샷 푸시/팝 검증"""
        chars = self.char_repo.list_all()
        char = chars[0]
        undo = UndoManager()
        undo.push(1, char, "행동", "대사")
        self.assertEqual(undo.depth, 1)

        snap = undo.pop()
        self.assertIsNotNone(snap)
        self.assertEqual(snap.turn_number, 1)
        self.assertEqual(undo.depth, 0)

    def test_narrative_orchestrator_execute_turn(self):
        """NarrativeOrchestrator 1턴 실행 및 3-Tier 원장 동기화 검증"""
        chars = self.char_repo.list_all()
        char = chars[0]
        orch = NarrativeOrchestrator(char, self.char_repo, self.turn_repo, self.llm)

        res = orch.execute_turn("그녀의 손끝을 잡았다.")
        self.assertEqual(res["turn"], 1)
        self.assertIn("prose", res)
        self.assertEqual(len(orch.history), 1)

        # Undo 롤백 테스트
        rolled_back = orch.rollback()
        self.assertTrue(rolled_back)
        self.assertEqual(orch.current_turn, 1)
        self.assertEqual(len(orch.history), 0)


if __name__ == "__main__":
    unittest.main()
