# -*- coding: utf-8 -*-
"""
tests/unit/infrastructure/test_infra.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Infrastructure Layer 단위 테스트
- VisualCompiler, PromptSynthesizer, MultiLLMClient, DatabaseManager, Repositories
"""

import os
import unittest
from src.domain.character import Character
from src.infrastructure.media.visual_compiler import VisualCompiler
from src.infrastructure.llm.client import MultiLLMClient
from src.infrastructure.llm.prompt_synthesizer import PromptSynthesizer
from src.infrastructure.database.db_manager import DatabaseManager
from src.infrastructure.database.repositories import CharacterRepository, TurnLedgerRepository


class TestInfrastructure(unittest.TestCase):

    def setUp(self):
        self.test_db_path = "test_infra_spec.db"
        self.db = DatabaseManager(self.test_db_path)
        self.char_repo = CharacterRepository(self.db)
        self.turn_repo = TurnLedgerRepository(self.db)

        self.char = Character.create_archetype(
            name="릴리스",
            title="제1황녀",
            faction="제국 황실",
            explicit_seed="#LILI-70G-BFFF",
            visual_dict={
                "face_geometry": "서늘한 턱선",
                "hair_physics": "백은색 직모",
                "ocular_optics": "금빛 눈동자"
            },
            gene_dict={"axis_1_physical_reflex": "척추 경직"}
        )

    def tearDown(self):
        if hasattr(self.db._local, "conn") and self.db._local.conn:
            self.db._local.conn.close()
            self.db._local.conn = None
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_visual_compiler_danbooru_prompt(self):
        """VisualCompiler 6-Slot 단부루 태그 컴파일 검증"""
        pos, neg = VisualCompiler.compile_danbooru_pair(self.char)
        self.assertIn("1girl", pos)
        self.assertIn("silver_hair", pos)
        self.assertIn("golden_eyes", pos)
        self.assertIn("lowres", neg)

    def test_prompt_synthesizer_master_directive(self):
        """PromptSynthesizer 마스터 헌법 조립 검증"""
        instruction = PromptSynthesizer.build_master_system_instruction(self.char)
        self.assertIn("#LILI-70G-BFFF", instruction)
        self.assertIn("8-Tier 해부학적 외모 규격", instruction)
        self.assertIn("무(無)수치 순수 감각어 헌법", instruction)

    def test_character_repository_save_and_find(self):
        """CharacterRepository 저장 및 복원 검증"""
        self.char_repo.save(self.char)
        found = self.char_repo.find_by_seed_hash("#LILI-70G-BFFF")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "릴리스")
        self.assertEqual(found.seed_hash, "#LILI-70G-BFFF")

    def test_turn_ledger_repository(self):
        """TurnLedgerRepository 턴 기록 및 조회 검증"""
        self.char_repo.save(self.char)
        self.turn_repo.record_turn(
            seed_hash="#LILI-70G-BFFF",
            turn_num=1,
            action="손끝을 잡았다",
            prose="그녀의 손끝이 파르르 떨렸다.",
            ledger_snap={"layer_1": "경직"}
        )
        hist = self.turn_repo.get_history("#LILI-70G-BFFF")
        self.assertEqual(len(hist), 1)
        self.assertEqual(hist[0]["action"], "손끝을 잡았다")


if __name__ == "__main__":
    unittest.main()
