# -*- coding: utf-8 -*-
"""
src/domain/kinematic_chain.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Domain Layer: 7단계 신체 운동 연쇄 파동 전이 엔진 (Kinematic Chain)
- 시선 ➔ 성대/호흡 ➔ 흉곽/심박 ➔ 부속기관 ➔ 의복 장력 ➔ 손끝 악력 ➔ 족부 접지력
- 2~3개 활성 텐서 On/Off 스포트라이트 선별
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class KinematicChain:
    """신체 운동 연쇄 파동 및 스포트라이트 텐서 관리자"""
    
    TENSORS: List[str] = (
        "01_cranial_and_headwear",
        "02_ocular_and_gaze",
        "03_vocal_and_respiratory",
        "04_thoracic_and_heartbeat",
        "05_appendage_and_wings_horns",
        "06_apparel_tension_and_seam",
        "07_digital_and_grip_strength",
        "08_pedal_and_ground_contact"
    )

    @classmethod
    def get_spotlight_tensors(cls, turn_count: int, stimulus_type: str = "DEFAULT") -> List[str]:
        """턴 수와 자극 유형에 따라 직전 텐서 쿨다운 및 새로운 2~3개 텐서 점등"""
        step = turn_count % 4
        if stimulus_type in ("PRESSURE", "CONQUEST", "압박"):
            return ["02_ocular_and_gaze", "06_apparel_tension_and_seam", "07_digital_and_grip_strength"]
        elif stimulus_type in ("AFFECTION", "COMFORT", "순애"):
            return ["03_vocal_and_respiratory", "04_thoracic_and_heartbeat", "07_digital_and_grip_strength"]
        elif stimulus_type in ("SEDUCTION", "STIMULATION", "유혹"):
            return ["01_cranial_and_headwear", "03_vocal_and_respiratory", "06_apparel_tension_and_seam"]
        
        # 순환 스포트라이트
        if step == 0:
            return ["02_ocular_and_gaze", "03_vocal_and_respiratory"]
        elif step == 1:
            return ["04_thoracic_and_heartbeat", "06_apparel_tension_and_seam"]
        elif step == 2:
            return ["07_digital_and_grip_strength", "08_pedal_and_ground_contact"]
        else:
            return ["01_cranial_and_headwear", "03_vocal_and_respiratory", "04_thoracic_and_heartbeat"]
