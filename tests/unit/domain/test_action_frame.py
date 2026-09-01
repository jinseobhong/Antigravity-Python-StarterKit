# -*- coding: utf-8 -*-
"""
tests/unit/domain/test_action_frame.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ActionFrame 및 자연어 사건 모델 단위 테스트 (Zero-Dependency unittest)
"""

import unittest
from src.domain.action_frame import ActionFrame, ObservableEvent, SpeechAct, Segment
from src.domain.relational_vector import RelationalVector


class TestActionFrame(unittest.TestCase):

    def test_action_frame_creation_and_serialization(self):
        """ActionFrame 객체 생성 및 딕셔너리 직렬화 검증"""
        event = ObservableEvent(
            actor="player",
            target="character",
            action_verb="whisper_and_touch",
            body_targets=["04_cervical"],
            contact=True,
            distance_change="closer",
            force="low",
        )

        frame = ActionFrame(
            raw_text='손목을 잡으며 "포기해"라고 속삭인다.',
            segments=[
                Segment(type="action", text="손목을 잡으며"),
                Segment(type="dialogue", text="포기해"),
                Segment(type="action", text="라고 속삭인다."),
            ],
            event=event,
            primary_tensor="04_cervical",
            dominant_vector=RelationalVector.SUBJUGATION,
            speech_act=SpeechAct.INTIMIDATION,
            intensity=3.5,
            predicted_deltas={"dominance": 0.4, "vulnerability": 0.3},
        )

        self.assertEqual(frame.intensity, 3.5)
        self.assertEqual(frame.dominant_vector, RelationalVector.SUBJUGATION)
        self.assertEqual(frame.speech_act, SpeechAct.INTIMIDATION)
        self.assertTrue(frame.event.contact)

        data = frame.to_dict()
        self.assertEqual(data["primary_tensor"], "04_cervical")
        self.assertEqual(len(data["segments"]), 3)
        self.assertEqual(data["event"]["distance_change"], "closer")


if __name__ == "__main__":
    unittest.main()
