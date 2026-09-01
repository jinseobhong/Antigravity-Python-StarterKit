# -*- coding: utf-8 -*-
"""
src/domain/kinematic_chain.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
7단계 신체 운동 연쇄 파동 전이 (Kinematic Chain Engine)
- [시선 ➔ 목/성대 ➔ 흉곽/심박 ➔ 부속기관(꼬리/날개/뿔) ➔ 의복 장력 ➔ 손끝 악력 ➔ 족부 접지력]
- 자극이 특정 부위에 정체되지 않고 전신으로 파동처럼 전이되도록 2~3개 활성 스포트라이트를 동적으로 순환
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any


KINEMATIC_STEPS = [
    "시선 (Ocular Alignment)",
    "목/성대/호흡 (Vocal & Laryngeal Reflex)",
    "흉곽/심박 (Thoracic Heartbeat)",
    "부속기관/특수신체 (Appendage & Horns/Wings/Tail)",
    "의복/초커 장력 (Choker & Fabric Tension)",
    "손끝/악력 (Distal Grip & Tremor)",
    "족부 접지력 (Grounding Stability)"
]


@dataclass
class KinematicChainState:
    """신체 운동 연쇄 전이 상태 관리자"""
    current_focus_indices: List[int] = field(default_factory=lambda: [0, 1])
    recent_chain_log: str = "시선 ➔ 목덜미 긴장으로의 초기 파동 전이"

    def advance_wave(self, stimulus_type: str = "TOUCH") -> List[str]:
        """자극에 따라 다음 운동 연쇄 포인트로 2~3개 스포트라이트 점등"""
        # 다음 단계로 순환
        next_indices = [(i + 2) % len(KINEMATIC_STEPS) for i in self.current_focus_indices]
        self.current_focus_indices = next_indices
        active_labels = [KINEMATIC_STEPS[idx] for idx in next_indices]
        self.recent_chain_log = f"{active_labels[0]} ➔ {active_labels[1]} 파동 전이"
        return active_labels

    def to_dict(self) -> Dict[str, Any]:
        return {
            "active_steps": [KINEMATIC_STEPS[i] for i in self.current_focus_indices],
            "recent_chain_log": self.recent_chain_log
        }
