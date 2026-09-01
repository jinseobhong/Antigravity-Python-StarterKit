# -*- coding: utf-8 -*-
"""
src/domain/pressure_stage.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
신경생리학적 4단계 압력 궤적 상태 머신 (PressureStage)
- STAGE_1_ELASTIC: 탄성 저항 (꼿꼿한 오만과 반발)
- STAGE_2_OVERLOAD: 감각 과부하 (호흡 잠김과 동요)
- STAGE_3_PLASTIC: 소성 항복 (가드 크러시 & 무릎 꺾임)
- STAGE_4_SUCTION: 역전 흡착 (자발적 안식 & 쾌락 굴종)
"""

from __future__ import annotations
from enum import Enum


class PressureStage(str, Enum):
    """신경생리학적 4단계 압력 궤적 열거형"""
    STAGE_1_ELASTIC = "Stage 1 (탄성 저항: 꼿꼿한 오만과 반발)"
    STAGE_2_OVERLOAD = "Stage 2 (감각 과부하: 호흡 잠김과 동요)"
    STAGE_3_PLASTIC = "Stage 3 (소성 항복: 가드 크러시 & 무릎 꺾임)"
    STAGE_4_SUCTION = "Stage 4 (역전 흡착: 자발적 안식 & 쾌락 굴종)"

    @classmethod
    def from_neural_taint(cls, taint: float) -> PressureStage:
        """신경 오염도(0.0 ~ 100.0)에 따른 결정론적 압력 단계 전이"""
        if taint < 25.0:
            return cls.STAGE_1_ELASTIC
        elif taint < 55.0:
            return cls.STAGE_2_OVERLOAD
        elif taint < 85.0:
            return cls.STAGE_3_PLASTIC
        else:
            return cls.STAGE_4_SUCTION

    @property
    def level(self) -> int:
        """단계별 정수 레벨 (1 ~ 4)"""
        if self == self.STAGE_1_ELASTIC:
            return 1
        elif self == self.STAGE_2_OVERLOAD:
            return 2
        elif self == self.STAGE_3_PLASTIC:
            return 3
        else:
            return 4
