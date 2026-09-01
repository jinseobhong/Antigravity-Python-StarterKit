# -*- coding: utf-8 -*-
"""
src/domain/spatial_pressure.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
3-Layer 공간 압력 챔버 (Spatial Pressure Chamber) 도메인 모델
- Layer 0: 공적 공간 (Public Domain) — 차가운 사회적 가면 및 철벽 방어
- Layer 1: 경계 공간 (Threshold Domain) — 1:1 대치 및 미세한 신체적 동조/긴장
- Layer 2: 사적 밀실 (Intimate Chamber) — 제약선의 균열, 에고 박탈 및 유저 주도 스킨십 해금
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass


class SpatialLayer(str, Enum):
    LAYER_0_PUBLIC = "Layer 0 (공적 공간)"
    LAYER_1_THRESHOLD = "Layer 1 (경계 공간)"
    LAYER_2_INTIMATE = "Layer 2 (사적 밀실)"


@dataclass
class SpatialPressureChamber:
    """공간 압력 챔버 상태 머신"""
    current_layer: SpatialLayer = SpatialLayer.LAYER_1_THRESHOLD
    touch_unlocked: bool = False
    intimacy_stage: int = 1

    def transition_to(self, layer: SpatialLayer) -> None:
        self.current_layer = layer
        if layer == SpatialLayer.LAYER_2_INTIMATE:
            self.touch_unlocked = True
            self.intimacy_stage = 3
        elif layer == SpatialLayer.LAYER_1_THRESHOLD:
            self.touch_unlocked = True
            self.intimacy_stage = 2
        else:
            self.touch_unlocked = False
            self.intimacy_stage = 1

    def to_dict(self) -> dict:
        return {
            "current_layer": self.current_layer.value,
            "touch_unlocked": self.touch_unlocked,
            "intimacy_stage": self.intimacy_stage
        }
