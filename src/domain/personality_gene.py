# -*- coding: utf-8 -*-
"""
src/domain/personality_gene.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
7대 절대 차원축 70단계 인격 유전자 & 제약 조건(Hard Invariants) 도메인 모델
- 축 I: 물리적 기질 및 체성 수용체
- 축 II: 신경화학 및 소마틱 신체 기억
- 축 III: 사회적 형성사 및 심층 결핍
- 축 IV: 와일랜드 서사 핵 및 인지 왜곡
- 축 V: 에고 역학 및 그림자 원형
- 축 VI: 연금술적 각성 및 서사적 척수 굴종
- 축 VII: 6대 화법 및 미세 제스처 틱
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class HardInvariants:
    """불변 제약선 엔티티 (캐릭터가 목숨보다 지키려는 방어선)"""
    primary_boundary: str         # 핵심 방어선 (예: 가문의 마지막 명예와 순결 서약)
    ego_collapse_trigger: str     # 자아 붕괴 트리거 (예: 목덜미 초커를 쥐고 강제로 시선을 맞출 때)
    somatic_achilles_heel: str    # 생체 취약 부위 (예: 쇄골 패임의 직접적 체온 접촉)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HardInvariants:
        return cls(
            primary_boundary=data.get("primary_boundary", "도덕적 자존감과 귀족적 결벽증"),
            ego_collapse_trigger=data.get("ego_collapse_trigger", "통제권의 강제 박탈"),
            somatic_achilles_heel=data.get("somatic_achilles_heel", "목덜미 및 쇄골 접촉")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_boundary": self.primary_boundary,
            "ego_collapse_trigger": self.ego_collapse_trigger,
            "somatic_achilles_heel": self.somatic_achilles_heel
        }


@dataclass
class PersonalityGene:
    """7대 차원축 70단계 인격 유전자 엔티티"""
    hard_invariants: HardInvariants
    axis_1_physical_reflex: str          # 축 I: 물리 반사 (체성 감각, 피부 역치)
    axis_2_neuro_memory: str             # 축 II: 신체 기억 (과거 억압된 호흡 흔적)
    axis_3_social_deficit: str           # 축 III: 사회적 결핍 (가문 부채, 애착 결핍)
    axis_4_cognitive_distortion: str     # 축 IV: 인지 왜곡 ("완벽하지 않으면 파멸한다")
    axis_5_shadow_ego: str               # 축 V: 그림자 에고 (숨겨진 피지배/복종 갈망)
    axis_6_alchemy_submission: str       # 축 VI: 척수 굴종 (한계 자극 시의 무조건 굴복)
    axis_7_gesture_ticks: List[str]      # 축 VII: 미세 제스처 틱 (초커 만지기, 시선 내리깔기 등)
    full_70_steps: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PersonalityGene:
        invariants_data = data.get("hard_invariants", {})
        invariants = HardInvariants.from_dict(invariants_data) if isinstance(invariants_data, dict) else HardInvariants(
            primary_boundary="도덕적 결벽증",
            ego_collapse_trigger="통제권 상실",
            somatic_achilles_heel="목덜미"
        )
        return cls(
            hard_invariants=invariants,
            axis_1_physical_reflex=data.get("axis_1_physical_reflex", "목덜미 접촉 시 척추 경직"),
            axis_2_neuro_memory=data.get("axis_2_neuro_memory", "호흡을 억누르는 흉곽 경련"),
            axis_3_social_deficit=data.get("axis_3_social_deficit", "가문의 부채로 인한 강박"),
            axis_4_cognitive_distortion=data.get("axis_4_cognitive_distortion", "취약성을 보이면 파멸한다는 신념"),
            axis_5_shadow_ego=data.get("axis_5_shadow_ego", "통제받고 의지하고 싶은 무의식"),
            axis_6_alchemy_submission=data.get("axis_6_alchemy_submission", "체온 밀착 시 무너지는 방어선"),
            axis_7_gesture_ticks=data.get("axis_7_gesture_ticks", ["시선 회피", "초커 만지기"]),
            full_70_steps=data.get("full_70_steps", {})
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hard_invariants": self.hard_invariants.to_dict(),
            "axis_1_physical_reflex": self.axis_1_physical_reflex,
            "axis_2_neuro_memory": self.axis_2_neuro_memory,
            "axis_3_social_deficit": self.axis_3_social_deficit,
            "axis_4_cognitive_distortion": self.axis_4_cognitive_distortion,
            "axis_5_shadow_ego": self.axis_5_shadow_ego,
            "axis_6_alchemy_submission": self.axis_6_alchemy_submission,
            "axis_7_gesture_ticks": self.axis_7_gesture_ticks,
            "full_70_steps": self.full_70_steps
        }
