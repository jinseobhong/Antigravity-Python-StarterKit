# -*- coding: utf-8 -*-
"""
src/domain/somatic_ledger.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
3계층 신경·메모리 원장 (3-Tier Somatic Ledger) 도메인 모델
- Layer 1: Primitive Reflex Matrix (무조건/조건 반사)
- Layer 2: Short-Term Somatic Buffer (이력현상, 감각 잔향, 정서 충격)
- Layer 3: Long-Term Somatic & Semantic Archive (영구 신체 각인, 정서적 부채 원장, 공유된 비밀)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class SomaticLedger:
    """3계층 신경·메모리 원장 엔티티"""
    # Layer 1: 원초 반사계 (즉각적 물리 반사)
    layer_1_reflex: Dict[str, str] = field(default_factory=lambda: {
        "pupil_dilation": "미세하게 수축된 동공",
        "spine_rigidity": "꼿꼿하게 긴장된 척추",
        "swallowing_reflex": "목구멍의 침 삼킴 반사 억제"
    })

    # Layer 2: 단기 소마틱 버퍼 (직전 턴의 감각 잔향 & 열역학적 계면 마찰)
    layer_2_short_term: Dict[str, str] = field(default_factory=lambda: {
        "sensory_hysteresis": "목덜미에 남아있는 서늘한 초커의 감촉",
        "respiratory_flutter": "미세하게 가라앉은 얕은 호흡",
        "dermal_heat_flux": "쇄골 부근의 안정된 체온"
    })

    # Layer 3: 장기 소마틱 & 의미론적 아카이브 (영구 각인, 감정 부채, 서사적 전복도)
    layer_3_long_term: Dict[str, Any] = field(default_factory=lambda: {
        "permanent_somatic_imprints": [],
        "emotional_debt_balance": "완벽주의적 도덕적 우위 고수",
        "shared_vulnerability_secrets": [],
        "relationship_inversion_rate": "0% (경계 및 대치 상태)"
    })

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SomaticLedger:
        return cls(
            layer_1_reflex=data.get("layer_1_reflex", {}),
            layer_2_short_term=data.get("layer_2_short_term", {}),
            layer_3_long_term=data.get("layer_3_long_term", {})
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "layer_1_reflex": self.layer_1_reflex,
            "layer_2_short_term": self.layer_2_short_term,
            "layer_3_long_term": self.layer_3_long_term
        }

    def format_meta_header(self, step: int, seed_hash: str, pacing_level: str = "Level 1") -> str:
        """턴별 상단 [STATUS META] 마스터 헤더 포맷팅"""
        return (
            f"[STATUS META]\n"
            f"[SEED HASH] {seed_hash}\n"
            f"[STEP] STEP {step} | [서사 호흡] {pacing_level}\n"
            f"[Layer 1 (반사계)] {self.layer_1_reflex.get('spine_rigidity', '척추 긴장')}\n"
            f"[Layer 2 (단기버퍼)] {self.layer_2_short_term.get('sensory_hysteresis', '잔향 안정')}\n"
            f"[Layer 3 (장기기억)] 전복도: {self.layer_3_long_term.get('relationship_inversion_rate', '0%')}"
        )
