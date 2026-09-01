# -*- coding: utf-8 -*-
"""
tests/unit/test_application_services.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unit Tests: 애플리케이션 서비스 계층 (Classifier, GeneSynthesis, NarrativeOrchestrator, UndoManager) 검증
"""

import unittest
import tempfile
from pathlib import Path

from src.infrastructure.database.db_manager import DBManager
from src.infrastructure.database.repositories import CharacterRepository, TurnLedgerRepository
from src.infrastructure.llm.client import MultiLLMClient
from src.application.classifier_service import ClassifierService
from src.application.gene_synthesis_service import GeneSynthesisService
from src.application.narrative_orchestrator import NarrativeOrchestrator
from src.application.undo_manager import UndoManager


class TestApplicationServices(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_dir.name) / "test_app_services.db")
        self.db_manager = DBManager(self.db_path)
        self.char_repo = CharacterRepository(self.db_manager)
        self.turn_repo = TurnLedgerRepository(self.db_manager)
        self.llm_client = MultiLLMClient()

        self.classifier_svc = ClassifierService(self.llm_client)
        self.synthesis_svc = GeneSynthesisService(self.char_repo, self.llm_client)
        self.narrative_orch = NarrativeOrchestrator(self.char_repo, self.turn_repo, self.llm_client)
        self.undo_mgr = UndoManager(self.turn_repo, self.char_repo)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_classifier_and_vector_resolution(self):
        result = self.classifier_svc.resolve_vectors_and_seed("은룡의 황녀 실비아")
        self.assertIn("seed_hash", result)
        self.assertIn("hard_invariants", result)
        self.assertIn("resolution_vectors", result)
        self.assertGreaterEqual(len(result["resolution_vectors"]), 2)

    def test_gene_synthesis_and_character_compilation(self):
        char = self.synthesis_svc.compile_character(
            target_name="릴리스",
            title="제1황녀",
            seed_hash="#LILI-70G-BFFF",
            hard_invariants=["가문의 명예", "초커 접촉"],
            selected_vector={"vector_id": "V1", "vector_name": "1안", "operation": "STRICT_GUARD"}
        )
        self.assertIsNotNone(char.id)
        self.assertEqual(char.name, "릴리스")
        self.assertIn("silver_choker", char.visual_dna.danbooru_prompt)

    def test_narrative_orchestrator_turn_execution_and_undo(self):
        self.char_repo.seed_defaults_if_empty()
        lilith = self.char_repo.get_active()

        # 턴 실행
        res = self.narrative_orch.execute_turn(
            character_id=lilith.id,
            user_action="[릴리스]의 차가운 뺨을 감싸 쥐며 속삭인다.",
            stimulus_type="순애"
        )
        self.assertEqual(res["turn_number"], 1)
        self.assertIn("릴리스", res["narrative_response"])
        self.assertGreaterEqual(res["gauges"]["trust"], 20)

        # Undo 실행
        undone = self.undo_mgr.undo_last_turn(lilith.id)
        self.assertIsNotNone(undone)
        self.assertEqual(len(self.turn_repo.get_history(lilith.id)), 0)


if __name__ == "__main__":
    unittest.main()
