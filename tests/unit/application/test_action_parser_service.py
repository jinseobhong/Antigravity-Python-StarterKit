# -*- coding: utf-8 -*-
"""
tests/unit/application/test_action_parser_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ActionParserService 대사/지문 분할 및 화행/텐서 분류 단위 테스트 (Zero-Dependency unittest)
"""

import unittest

from src.domain.action_frame import SpeechAct
from src.domain.relational_vector import RelationalVector
from src.application.action_parser_service import ActionParserService


class TestActionParserService(unittest.TestCase):

    def test_parse_input_with_dialogue_and_action(self):
        """지문과 대사가 혼합된 자연어 입력 파싱 검증"""
        raw_text = '손을 뻗어 목을 잡으며 "포기해라"라고 강압적으로 명령한다.'
        frame = ActionParserService.parse_input(raw_text)

        self.assertEqual(frame.primary_tensor, "04_cervical")
        self.assertEqual(frame.speech_act, SpeechAct.INTIMIDATION)
        self.assertEqual(frame.dominant_vector, RelationalVector.SUBJUGATION)
        self.assertEqual(frame.intensity, 4.0)
        self.assertTrue(frame.event.contact)

        # 지문/대사 세그먼트 분할 확인
        dialogue_segments = [s for s in frame.segments if s.type == "dialogue"]
        action_segments = [s for s in frame.segments if s.type == "action"]
        self.assertEqual(len(dialogue_segments), 1)
        self.assertEqual(dialogue_segments[0].text, "포기해라")
        self.assertGreater(len(action_segments), 0)

    def test_parse_comfort_action(self):
        """위로 및 순애 벡터 파싱 검증"""
        raw_text = '조심스럽게 다가가서 눈을 바라보며 "괜찮아, 내가 곁에 있어"라고 위로한다.'
        frame = ActionParserService.parse_input(raw_text)

        self.assertEqual(frame.primary_tensor, "02_ocular")
        self.assertEqual(frame.speech_act, SpeechAct.CONSOLATION)
        self.assertEqual(frame.dominant_vector, RelationalVector.DEVOTION_COMFORT)
        self.assertEqual(frame.event.distance_change, "closer")


if __name__ == "__main__":
    unittest.main()
