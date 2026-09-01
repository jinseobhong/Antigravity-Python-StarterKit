# -*- coding: utf-8 -*-
"""
src/domain/spatial_pressure.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Domain Layer: 3-Layer 공간 압력 챔버 모델
- Layer 0: 공적 공간 (사회적 가면과 형식적 예의)
- Layer 1: 경계 공간 (시선 집중과 신체적 긴장)
- Layer 2: 사적 밀실 (에고 붕괴와 유저 주도 NSFW 소마틱 본능 해금)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SpatialPressure:
    layer_level: int       # 0, 1, 2
    location_name: str     # 예: 집무실, 복도, 사적 침실
    atmosphere: str        # 분위기 및 공간 압력 묘사
    nsfw_unlocked: bool    # Layer 2 밀실 진입 시 True

    @classmethod
    def create(cls, layer: int = 1, location: str = "황녀의 침실") -> SpatialPressure:
        clamped = max(0, min(2, layer))
        unlocked = (clamped == 2)
        atmospheres = {
            0: "공식적인 집무실의 차가운 대리석과 격식 있는 거리감",
            1: "단둘만 남겨진 서재, 촛불 아래 좁혀지는 시선과 서늘한 공기",
            2: "문이 굳게 닫힌 침실, 밀폐된 공기 속 서로의 거친 호흡과 은밀한 체온"
        }
        return cls(
            layer_level=clamped,
            location_name=location,
            atmosphere=atmospheres.get(clamped, atmospheres[1]),
            nsfw_unlocked=unlocked
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "layer_level": self.layer_level,
            "location_name": self.location_name,
            "atmosphere": self.atmosphere,
            "nsfw_unlocked": self.nsfw_unlocked
        }
