# -*- coding: utf-8 -*-
"""
tests/unit/test_application_services.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unit Test Suite for 4-Tier Application Services
"""

import unittest
import tempfile
from unittest.mock import MagicMock

from src.storage.db_manager import DBManager
from src.storage.repositories import CharacterRepository, TurnLedgerRepository
from src.core.classifier_service import ClassifierService
from src.core.gene_synthesis_service import GeneSynthesisService
from src.core.narrative_orchestrator import NarrativeOrchestrator
from src.core.undo_manager import UndoManager
from src.models.character import Character


class TestApplicationServices(unittest.TestCase):
    """Application Services 단위 테스트"""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = f"{self.temp_dir.name}/test_app_services.db"
        self.db_manager = DBManager(self.db_path)
        self.char_repo = CharacterRepository(self.db_manager)
        self.turn_repo = TurnLedgerRepository(self.db_manager)
        
        self.mock_llm = MagicMock()
        self.mock_llm.generate.side_effect = self._mock_llm_generate
        
        self.classifier_svc = ClassifierService(self.mock_llm)
        self.synthesis_svc = GeneSynthesisService(self.char_repo, self.mock_llm)
        self.narrative_orch = NarrativeOrchestrator(self.char_repo, self.turn_repo, self.mock_llm)
        self.undo_mgr = UndoManager(self.turn_repo, self.char_repo)

    def _mock_llm_generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        if "DOMAIN CLASSIFIER" in system_prompt:
            return """{
  "domain_mode": "ROLEPLAY_INTERACTION",
  "seed_hash": "#LILI-70G-BFFF",
  "boundary": {
    "target_domain": "릴리스 (제1황녀)",
    "hard_invariants": ["가문의 명예", "초커 접촉"]
  },
  "resolution_vectors": [
    {"vector_id": "V1", "vector_name": "1안", "operation": "STRICT_GUARD", "armor_type": "Rigid"},
    {"vector_id": "V2", "vector_name": "2안", "operation": "SOMATIC_DESYNC_TRACK", "armor_type": "Endurer"}
  ]
}"""
        return "릴리스가 당신을 차갑게 응시하며 숨을 삼킵니다."

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_classifier_and_vector_resolution(self):
        res = self.classifier_svc.resolve_vectors_and_seed("제1황녀 릴리스의 결벽증적 척추 방어")
        self.assertIn("target_name", res)
        self.assertIn("seed_hash", res)
        self.assertEqual(len(res["resolution_vectors"]), 2)

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
        lilith = self.char_repo.save(Character.create_lilith())
        self.char_repo.set_active(lilith.id)

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
