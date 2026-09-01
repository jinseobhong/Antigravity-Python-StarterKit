# -*- coding: utf-8 -*-
"""
tests/unit/test_creation_pipeline.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unit Test Suite for Dify 11-Node 25-Master Character Creation Algorithm
- Node 3: Classifier & Orthogonal Vectors Resolver
- Node 7: 8-Tier DNA, 17-Tensor & 70-Gene Spec Compiler
- Node 10: 30,000-char Master Synthesizer with 5 Core Mandates
- Node 11: Static Linter & SQLite DB Persistence
"""

import unittest
from src.infrastructure.database.db_manager import DBManager
from src.infrastructure.database.repositories import CharacterRepository
from src.application.classifier_service import ClassifierService
from src.application.spec_compiler_service import SpecCompilerService
from src.application.master_synthesizer_service import MasterSynthesizerService
from src.application.static_validator import StaticValidator
from src.domain.character import Character


class TestCreationPipeline(unittest.TestCase):
    """캐릭터 생성 풀 파이프라인 검증 테스트"""

    def setUp(self):
        from src.infrastructure.llm.client import MultiLLMClient
        self.db_manager = DBManager(":memory:")
        self.char_repo = CharacterRepository(self.db_manager)
        self.llm_client = MultiLLMClient()
        self.classifier_svc = ClassifierService(self.llm_client)
        self.spec_compiler_svc = SpecCompilerService(self.llm_client)
        self.master_synthesizer_svc = MasterSynthesizerService(self.llm_client)

    def test_node_3_classifier_and_seed(self):
        """Node 3: 제약선 및 직교 2대 궤적 역산 검증"""
        concept = "제국의 은룡 황녀 실비아, 가문의 명예와 순결 서약을 지키기 위해 금속 초커를 차고 있다."
        res = self.classifier_svc.resolve_vectors_and_seed(concept)

        self.assertTrue(len(res["target_name"]) > 0)
        self.assertTrue(res["seed_hash"].startswith("#"))
        self.assertTrue(len(res["hard_invariants"]) > 0)
        self.assertEqual(len(res["resolution_vectors"]), 2)
        self.assertEqual(res["resolution_vectors"][0]["vector_id"], "V1")
        self.assertEqual(res["resolution_vectors"][1]["vector_id"], "V2")

    def test_node_7_spec_compiler(self):
        """Node 7: 8-Tier DNA, 17대 텐서, 70단계 유전자 컴파일 검증"""
        spec = self.spec_compiler_svc.compile_spec(
            target_name="실비아",
            title="은룡 황녀",
            seed_hash="#SILV-70G-TEST",
            hard_invariants=["가문의 명예", "순결 서약"],
            selected_vector={
                "vector_id": "V1",
                "vector_name": "정통파 결벽주의 방어",
                "axis_description": "신체 접촉 시 척추 경직"
            }
        )

        self.assertIn("visual_dna", spec)
        self.assertIn("skeletal", spec["visual_dna"])
        self.assertIn("danbooru_prompt", spec)
        self.assertIn("positive", spec["danbooru_prompt"])
        self.assertIn("genes_70", spec)

    def test_node_10_and_11_synthesizer_and_linter(self):
        """Node 10 & 11: 마스터 헌법 합성 및 정적 린터 검증"""
        char = Character.create_lilith()
        res = self.master_synthesizer_svc.synthesize_master_prompt(char.to_dict())

        self.assertTrue(res["is_valid"])
        self.assertTrue(len(res["master_prompt"]) >= 1000)

        # 정적 린터 검증
        val = StaticValidator.validate_master_prompt(res["master_prompt"])
        self.assertTrue(val["is_valid"])


if __name__ == "__main__":
    unittest.main()
