# -*- coding: utf-8 -*-
"""
tests/unit/infrastructure/test_llm_config.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LLMConfig 및 PromptBuilder 단위 테스트 (Zero-Dependency unittest)
"""

import os
import tempfile
import unittest

from src.domain.character import Character, LowenArmor
from src.domain.action_frame import ActionFrame, ObservableEvent, SpeechAct, Segment
from src.domain.relational_vector import RelationalVector
from src.infrastructure.llm.config import LLMConfig, GEMINI_MODEL_CASCADE, CLAUDE_MODEL_CASCADE
from src.infrastructure.llm.prompt_builder import PromptBuilder


class TestLLMInfrastructure(unittest.TestCase):

    def test_llm_config_cascade_lists(self):
        """캐스케이드 모델 목록 유효성 검증"""
        self.assertGreater(len(GEMINI_MODEL_CASCADE), 0)
        self.assertGreater(len(CLAUDE_MODEL_CASCADE), 0)
        self.assertIn("gemini-3.6-flash", GEMINI_MODEL_CASCADE)

    def test_llm_config_load_from_file(self):
        """임시 .env 파일로부터 API 키 및 설정 로드 검증"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False, encoding="utf-8") as f:
            f.write("GEMINI_API_KEY=test_gemini_key_123\n")
            f.write("ANTHROPIC_API_KEY=test_claude_key_456\n")
            f.write("LLM_PROVIDER=claude\n")
            env_file = f.name

        try:
            cfg = LLMConfig.load_from_env(env_path=env_file)
            self.assertEqual(cfg.gemini_api_key, "test_gemini_key_123")
            self.assertEqual(cfg.claude_api_key, "test_claude_key_456")
            self.assertEqual(cfg.provider, "claude")
        finally:
            if os.path.exists(env_file):
                os.remove(env_file)

    def test_prompt_builder_synthesis(self):
        """PromptBuilder 서사 프롬프트 조립 무결성 검증"""
        char = Character(
            name="아이리스",
            title="마법사",
            faction="성역",
            armor_type=LowenArmor.RIGID,
        )
        char.tensors.apply_stimulus("04_cervical", intensity=0.5)

        event = ObservableEvent(actor="player", target="character", contact=True)
        frame = ActionFrame(
            raw_text="손을 뻗어 어깨를 감싼다.",
            segments=[Segment(type="action", text="손을 뻗어 어깨를 감싼다.")],
            event=event,
            primary_tensor="04_cervical",
            dominant_vector=RelationalVector.DEVOTION_COMFORT,
            speech_act=SpeechAct.CONSOLATION,
            intensity=2.0,
        )

        sys_prompt, user_prompt = PromptBuilder.build_narrative_prompts(
            character=char,
            action_frame=frame,
            turn_number=1,
            recent_chat_history=[]
        )

        self.assertIn("아이리스", sys_prompt)
        self.assertIn("Rigid (완벽주의 척추 방어)", sys_prompt)
        self.assertIn("손을 뻗어 어깨를 감싼다.", user_prompt)
        self.assertIn("🌸 순애 및 정서적 위로 벡터", user_prompt)


if __name__ == "__main__":
    unittest.main()
