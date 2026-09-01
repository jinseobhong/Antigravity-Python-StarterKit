# -*- coding: utf-8 -*-
"""
src/domain/character_traits.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Domain Layer: 16대 RDB Traits & 5대 심리 게이지 (신뢰, 성애, 수치심, 죄책감, 굴종) 및 생체 수치 모델
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class PsychologicalGauges:
    """5대 심리 게이지 (Play Room 상단 상태 바 1:1 연동)"""
    trust: int = 20         # 신뢰 (%)
    eroticism: int = 0      # 성애 (%)
    shame: int = -30        # 수치심 (음수: 도도한 방어 ~ 양수: 극도의 수치 굴복)
    guilt: int = 15         # 죄책감 (%)
    submission: int = 20    # 굴종 (%)

    def clamp(self) -> None:
        self.trust = max(0, min(100, self.trust))
        self.eroticism = max(0, min(100, self.eroticism))
        self.shame = max(-100, min(100, self.shame))
        self.guilt = max(0, min(100, self.guilt))
        self.submission = max(0, min(100, self.submission))

    def to_dict(self) -> Dict[str, int]:
        return {
            "trust": self.trust,
            "eroticism": self.eroticism,
            "shame": self.shame,
            "guilt": self.guilt,
            "submission": self.submission
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PsychologicalGauges:
        return cls(
            trust=int(data.get("trust", 20)),
            eroticism=int(data.get("eroticism", 0)),
            shame=int(data.get("shame", -30)),
            guilt=int(data.get("guilt", 15)),
            submission=int(data.get("submission", 20))
        )


@dataclass
class SomaticMetrics:
    """생체 수치 (ODO / TAINT)"""
    odo: str = "54.2%"      # 신체 순도 및 마력 침투도
    taint: str = "7.1%"     # 심연 침식 및 타락도

    def to_dict(self) -> Dict[str, str]:
        return {"odo": self.odo, "taint": self.taint}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SomaticMetrics:
        return cls(
            odo=str(data.get("odo", "54.2%")),
            taint=str(data.get("taint", "7.1%"))
        )


@dataclass
class CharacterTraits:
    """16대 RDB 상세 고유 속성 (Character Studio 하단 인스펙터 패널)"""
    archetype_title: str             # 예: 제1황녀 • 제국 황실
    archetype_class: str             # 예: Rigid (결벽주의 척추 방어)
    stage_progression: str           # 예: Stage 1 (침실 개방 - 포섭된 요새와 결벽)
    gauges: PsychologicalGauges = field(default_factory=PsychologicalGauges)
    somatic_metrics: SomaticMetrics = field(default_factory=SomaticMetrics)
    traits_list: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "archetype_title": self.archetype_title,
            "archetype_class": self.archetype_class,
            "stage_progression": self.stage_progression,
            "gauges": self.gauges.to_dict(),
            "somatic_metrics": self.somatic_metrics.to_dict(),
            "traits_list": self.traits_list
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CharacterTraits:
        return cls(
            archetype_title=data.get("archetype_title", "제국 황녀"),
            archetype_class=data.get("archetype_class", "Rigid (결벽주의 척추 방어)"),
            stage_progression=data.get("stage_progression", "Stage 1 (침실 개방 - 포섭된 요새와 결벽)"),
            gauges=PsychologicalGauges.from_dict(data.get("gauges", {})),
            somatic_metrics=SomaticMetrics.from_dict(data.get("somatic_metrics", {})),
            traits_list=data.get("traits_list", [])
        )
