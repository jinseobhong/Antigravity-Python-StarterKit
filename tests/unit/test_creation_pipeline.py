# -*- coding: utf-8 -*-
"""
tests/unit/test_creation_pipeline.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unit Test Suite for Dify 11-Node 2-Checkpoint Character Creation Pipeline
"""

import unittest
from unittest.mock import MagicMock
from src.core.classifier_service import ClassifierService
from src.core.spec_compiler_service import SpecCompilerService
from src.core.master_synthesizer_service import MasterSynthesizerService
from src.core.static_validator import StaticValidator
from src.models.character import Character


class TestCreationPipeline(unittest.TestCase):
    """Dify 11-Node 생성 파이프라인 단위 테스트"""

    def setUp(self):
        self.mock_llm = MagicMock()
        # Realistic Dify mock responses
        self.mock_llm.generate.side_effect = self._mock_generate
        
        self.classifier_svc = ClassifierService(self.mock_llm)
        self.spec_compiler_svc = SpecCompilerService(self.mock_llm)
        self.master_synthesizer_svc = MasterSynthesizerService(self.mock_llm)

    def _mock_generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        if "DOMAIN CLASSIFIER" in system_prompt:
            return """{
  "domain_mode": "ROLEPLAY_INTERACTION",
  "seed_hash": "#SILV-70G-8C2A",
  "boundary": {
    "target_domain": "은룡 황녀 '실비아'",
    "hard_invariants": [
      "순결 서약 및 가문의 부채",
      "목덜미 초커 접촉 시 척추 경직 룰"
    ]
  },
  "resolution_vectors": [
    {
      "vector_id": "V1",
      "vector_name": "정통파 결벽주의 방어",
      "axis_description": "신체 접촉 시 척추 경직",
      "armor_type": "Rigid"
    },
    {
      "vector_id": "V2",
      "vector_name": "소마틱 체온 동조 굴종",
      "axis_description": "체온 융합 궤적",
      "armor_type": "Endurer"
    }
  ]
}"""
        elif "DUAL-MODE RECURSIVE SPEC" in system_prompt:
            return """{
  "target_name": "실비아",
  "seed_hash": "#SILV-70G-8C2A",
  "visual_dna": {
    "skeletal": "168cm 슬림 골격",
    "ocular": "금빛 안광",
    "hair": "은빛 롱헤어",
    "somatic": "쇄골 라인",
    "dermal": "도자기 피부",
    "apparel": "금속 초커 드레스",
    "blush": "쇄골 홍조",
    "lighting": "달빛 음영"
  },
  "traits": {
    "archetype_class": "Rigid",
    "stage_progression": "Stage 1",
    "gauges": {"trust": 20, "eroticism": 0, "shame": -30, "guilt": 15, "submission": 20},
    "traits_list": []
  }
}"""
        else:
            return "# [SYSTEM DIRECTIVE: 25-MASTER ENTERPRISE SPEC FOR LILITH]\n" + "고밀도 마스터 시스템 헌법\n" * 10

    def test_node_3_classifier_and_seed(self):
        """Node 3: 제약선 및 직교 2대 궤적 역산 검증"""
        res = self.classifier_svc.resolve_vectors_and_seed("은룡 황녀 실비아")

        self.assertIn("target_name", res)
        self.assertIn("seed_hash", res)
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
                "label": "정통파 결벽주의 방어",
                "description": "신체 접촉 시 척추 경직"
            }
        )

        self.assertIn("visual_dna", spec)
        self.assertTrue("face_geometry" in spec["visual_dna"] or "skeletal" in spec["visual_dna"])
        self.assertIn("danbooru_prompt", spec)
        self.assertIn("positive", spec["danbooru_prompt"])

    def test_node_10_and_11_synthesizer_and_linter(self):
        """Node 10 & 11: 마스터 헌법 합성 및 정적 린터 검증"""
        char = Character.create_lilith()
        prompt_text = self.master_synthesizer_svc.synthesize_master_prompt(char.to_dict())

        self.assertIsInstance(prompt_text, str)
        self.assertTrue(len(prompt_text) > 50)

        # 정적 린터 검증
        val = StaticValidator.validate_master_prompt(prompt_text)
        self.assertIn("is_valid", val)


if __name__ == "__main__":
    unittest.main()
