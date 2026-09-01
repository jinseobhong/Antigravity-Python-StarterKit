# -*- coding: utf-8 -*-
"""
src/domain/somatic_ledger.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Domain Layer: 3계층 신경·메모리 원장 (3-Tier Somatic Neural & Memory Ledger)
- Layer 1: Primitive Reflex Matrix (무조건/조건 반사)
- Layer 2: Short-Term Somatic Buffer (이력현상 및 감각 잔향)
- Layer 3: Long-Term Somatic & Semantic Archive (영구 각인 및 부채 원장)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SomaticLedger:
    """3계층 신경·메모리 원장"""
    layer_1_reflex: str    # Layer 1: 척추, 호흡, 성대, 눈동자의 즉각적 무조건 반사
    layer_2_buffer: str    # Layer 2: 체온 잔향, 피부의 붉은 열감, 호흡의 물리적 흐트러짐
    layer_3_archive: str   # Layer 3: 영구 신체 각인, 정서적 부채, 관계성 전복도

    def compile_markdown_ledger(self) -> str:
        """하단 영구 원장 Markdown 블록 렌더링"""
        return (
            "[CUMULATIVE NEURAL & MEMORY LEDGER]\n"
            f"• Layer 1 (Primitive Reflex Matrix): {self.layer_1_reflex}\n"
            f"• Layer 2 (Short-Term Somatic Buffer): {self.layer_2_buffer}\n"
            f"• Layer 3 (Long-Term Somatic & Semantic Archive): {self.layer_3_archive}"
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "layer_1_reflex": self.layer_1_reflex,
            "layer_2_buffer": self.layer_2_buffer,
            "layer_3_archive": self.layer_3_archive
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SomaticLedger:
        return cls(
            layer_1_reflex=data.get("layer_1_reflex", "목덜미 접촉 시 척추가 굳으며 얕은 호흡"),
            layer_2_buffer=data.get("layer_2_buffer", "귓바퀴와 쇄골로 서서히 번지는 붉은 열감"),
            layer_3_archive=data.get("layer_3_archive", "초커의 차가운 금속 압박감과 주도권에 대한 미세한 균열")
        )
