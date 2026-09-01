# -*- coding: utf-8 -*-
"""
src/domain/personality_gene.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Domain Layer: 7대 차원축 70단계 마스터 인격 유전자 & 불변 제약선(Hard Invariants) 모델
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class HardInvariants:
    """불변 제약선 모델 (Constraint-First Core)"""
    primary_boundary: str      # 목숨보다 지키려는 도덕적/귀족적 결벽증 및 제약선
    ego_collapse_trigger: str  # NSFW 소마틱 자아 붕괴 트리거
    somatic_achilles_heel: str # 생체적/감각적 절대 취약 부위

    def to_dict(self) -> Dict[str, str]:
        return {
            "primary_boundary": self.primary_boundary,
            "ego_collapse_trigger": self.ego_collapse_trigger,
            "somatic_achilles_heel": self.somatic_achilles_heel
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HardInvariants:
        return cls(
            primary_boundary=data.get("primary_boundary", "가문의 명예와 순결 서약"),
            ego_collapse_trigger=data.get("ego_collapse_trigger", "목덜미 초커를 쥔 채 시선 강제 고정"),
            somatic_achilles_heel=data.get("somatic_achilles_heel", "쇄골 패임의 직접적 체온 접촉")
        )


@dataclass
class PersonalityGene:
    """7대 절대 차원축 70단계 인격 유전자"""
    hard_invariants: HardInvariants
    axis_1_physical_reflex: str        # 축 I: 물리적 기질 및 체성 수용체
    axis_2_neuro_memory: str           # 축 II: 신경화학 및 소마틱 신체 기억
    axis_3_social_deficit: str         # 축 III: 사회적 형성사 및 과거 결핍
    axis_4_cognitive_distortion: str   # 축 IV: 인지 왜곡 및 방어기제
    axis_5_shadow_ego: str             # 축 V: 그림자 에고 및 피지배 갈망
    axis_6_alchemy_submission: str     # 축 VI: 연금술적 각성 및 척수 굴종
    axis_7_gesture_ticks: List[str] = field(default_factory=list) # 축 VII: 미세 제스처 틱

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hard_invariants": self.hard_invariants.to_dict(),
            "axis_1_physical_reflex": self.axis_1_physical_reflex,
            "axis_2_neuro_memory": self.axis_2_neuro_memory,
            "axis_3_social_deficit": self.axis_3_social_deficit,
            "axis_4_cognitive_distortion": self.axis_4_cognitive_distortion,
            "axis_5_shadow_ego": self.axis_5_shadow_ego,
            "axis_6_alchemy_submission": self.axis_6_alchemy_submission,
            "axis_7_gesture_ticks": self.axis_7_gesture_ticks
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PersonalityGene:
        inv_data = data.get("hard_invariants", {})
        inv = HardInvariants.from_dict(inv_data) if isinstance(inv_data, dict) else HardInvariants(
            primary_boundary="가문의 명예",
            ego_collapse_trigger="초커 접촉",
            somatic_achilles_heel="쇄골 패임"
        )
        return cls(
            hard_invariants=inv,
            axis_1_physical_reflex=data.get("axis_1_physical_reflex", "목덜미 접촉 시 척추 경직"),
            axis_2_neuro_memory=data.get("axis_2_neuro_memory", "얕은 호흡과 흉곽 경련"),
            axis_3_social_deficit=data.get("axis_3_social_deficit", "가문의 막대한 부채와 순결 의무"),
            axis_4_cognitive_distortion=data.get("axis_4_cognitive_distortion", "취약성을 드러내는 것은 파멸"),
            axis_5_shadow_ego=data.get("axis_5_shadow_ego", "완전히 지배당하고 짐을 내려놓고 싶은 갈망"),
            axis_6_alchemy_submission=data.get("axis_6_alchemy_submission", "체온 밀착 시 무너지는 방어선"),
            axis_7_gesture_ticks=data.get("axis_7_gesture_ticks", ["눈을 가늘게 뜨며 시선 회피", "초커 만지작거리기"])
        )
