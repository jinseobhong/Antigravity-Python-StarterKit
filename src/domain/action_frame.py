# -*- coding: utf-8 -*-
"""
src/domain/action_frame.py
~~~~~~~~~~~~~~~~~~~~~~~~~~
자연어 행동 지문/대사 파싱 결과 및 5D 정서 델타 사건 모델 (ActionFrame)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any

from .relational_vector import RelationalVector


class SpeechAct(str, Enum):
    """7대 발화 화행 의도 (Pragmatics)"""
    CONSOLATION = "CONSOLATION"          # 위로·안식
    INTIMIDATION = "INTIMIDATION"        # 위협·강압
    ADORATION = "ADORATION"              # 찬미·경배·헌신
    PROVOCATION = "PROVOCATION"          # 도발·조롱
    ENTREATY = "ENTREATY"                # 애원·간청
    SEDUCTION = "SEDUCTION"              # 유혹·암시
    COLD_SILENCE = "COLD_SILENCE"        # 냉담·무응답


@dataclass
class Segment:
    """대사("...") 또는 행동 지문 분할 세그먼트"""
    type: str  # "dialogue" | "action"
    text: str


@dataclass
class ObservableEvent:
    """물리적으로 관측 가능한 사건 단위"""
    actor: str = "player"
    target: str = "character"
    action_verb: str = "interact"
    body_targets: List[str] = field(default_factory=list)
    contact: bool = False
    distance_change: str = "none"  # "closer" | "further" | "none"
    force: str = "low"            # "none" | "low" | "medium" | "high" | "extreme"


@dataclass
class ActionFrame:
    """파싱된 완전한 상호작용 사건 프레임"""
    raw_text: str
    segments: List[Segment]
    event: ObservableEvent
    primary_tensor: str
    dominant_vector: RelationalVector
    speech_act: SpeechAct
    intensity: float = 1.0  # 1.0 ~ 5.0
    predicted_deltas: Dict[str, float] = field(default_factory=lambda: {
        "trust": 0.0,
        "erotic": 0.0,
        "dominance": 0.0,
        "taboo": 0.0,
        "vulnerability": 0.0
    })

    def to_dict(self) -> Dict[str, Any]:
        """직렬화"""
        return {
            "raw_text": self.raw_text,
            "segments": [{"type": s.type, "text": s.text} for s in self.segments],
            "event": {
                "actor": self.event.actor,
                "target": self.event.target,
                "action_verb": self.event.action_verb,
                "body_targets": list(self.event.body_targets),
                "contact": self.event.contact,
                "distance_change": self.event.distance_change,
                "force": self.event.force,
            },
            "primary_tensor": self.primary_tensor,
            "dominant_vector": self.dominant_vector.value,
            "speech_act": self.speech_act.value,
            "intensity": self.intensity,
            "predicted_deltas": dict(self.predicted_deltas),
        }
