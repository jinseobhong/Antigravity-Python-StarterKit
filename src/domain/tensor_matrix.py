# -*- coding: utf-8 -*-
"""
src/domain/tensor_matrix.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~
17대 생체·물리·의복 텐서 및 신체 운동 연쇄(Kinematic Chain) 전이 엔진
- 100% 순수 파이썬 결정론적 인과율 (0토큰, 0ms, 무오차)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


# 17대 완전 범용 생체·물리·의복 텐서 마스터 레지스트리
TENSOR_REGISTRY: Dict[str, str] = {
    "01_cranial": "두상/관자놀이 텐서",
    "02_ocular": "동공 산대/시선 회피 텐서",
    "03_vocal": "성대 쇳소리/호흡 파열 텐서",
    "04_cervical": "경추 굳음/초커 조임 텐서",
    "05_clavicular": "쇄골 승강/피부 붉어짐 텐서",
    "06_thoracic": "흉곽 팽창/심박 가속 텐서",
    "07_appendage": "고유 부속기관(귀/말초) 텐서",
    "08_dorsal": "등줄기/기립근 전율 텐서",
    "09_sartorial": "의복 솔기/단추 장력 텐서",
    "10_manual": "손가락 악력/손끝 땀 텐서",
    "11_abdominal": "복부 코어/횡격막 수축 텐서",
    "12_pelvic": "골반 경사/요추 과신전 텐서",
    "13_femoral": "대퇴부/무릎 관절 경직 텐서",
    "14_pedal": "족부 접지력 상실 텐서",
    "15_integumentary": "피부 광택/계면 마찰열 텐서",
    "16_tactile": "피부 접촉면 열전도율 텐서",
    "17_aura": "밀실 공간 압력/체적 텐서",
}

# 7단계 표준 신체 운동 연쇄 전이 경로
KINEMATIC_CHAIN_FLOW: List[str] = [
    "02_ocular",
    "03_vocal",
    "04_cervical",
    "06_thoracic",
    "09_sartorial",
    "10_manual",
    "14_pedal",
]


@dataclass
class TensorMatrix:
    """17대 텐서 레벨 관리 및 운동 연쇄 전이 계산기"""
    levels: Dict[str, float] = field(default_factory=lambda: {k: 0.0 for k in TENSOR_REGISTRY})
    active_spotlights: List[str] = field(default_factory=list)
    recent_chain_history: List[str] = field(default_factory=list)

    def get_level(self, tensor_key: str) -> float:
        """특정 텐서 레벨 조회 (0.0 ~ 1.0)"""
        return self.levels.get(tensor_key, 0.0)

    def apply_stimulus(self, primary_tensor: str, intensity: float = 0.4) -> List[str]:
        """
        특정 텐서에 1차 외력을 가하고 신체 운동 연쇄(Kinematic Chain)를 따라 파동을 전이.
        반환값: 발생한 자극 및 연쇄 이벤트 로그 리스트
        """
        if primary_tensor not in self.levels:
            primary_tensor = "04_cervical"

        # 직전 스포트라이트 리셋 및 1차 자극 가산
        self.active_spotlights = [primary_tensor]
        self.levels[primary_tensor] = min(1.0, max(0.0, self.levels[primary_tensor] + intensity))

        tensor_name = TENSOR_REGISTRY.get(primary_tensor, primary_tensor)
        events = [f"주 자극: {tensor_name} (+{intensity*100:.0f}%)"]

        # 운동 연쇄 전이 계산 (감쇠율 60% 적용)
        if primary_tensor in KINEMATIC_CHAIN_FLOW:
            idx = KINEMATIC_CHAIN_FLOW.index(primary_tensor)
            if idx + 1 < len(KINEMATIC_CHAIN_FLOW):
                next_tensor = KINEMATIC_CHAIN_FLOW[idx + 1]
                decayed_intensity = intensity * 0.6
                self.levels[next_tensor] = min(1.0, max(0.0, self.levels[next_tensor] + decayed_intensity))
                self.active_spotlights.append(next_tensor)
                
                next_name = TENSOR_REGISTRY.get(next_tensor, next_tensor)
                event_str = f"파동 전이: {tensor_name} ➔ {next_name} (+{decayed_intensity*100:.0f}%)"
                events.append(event_str)
                self.recent_chain_history.append(event_str)

        return events

    def to_dict(self) -> Dict[str, Any]:
        """직렬화용 딕셔너리 변환"""
        return {
            "levels": dict(self.levels),
            "active_spotlights": list(self.active_spotlights),
            "recent_chain_history": list(self.recent_chain_history),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TensorMatrix:
        """역직렬화 생성"""
        matrix = cls()
        if "levels" in data:
            matrix.levels.update(data["levels"])
        if "active_spotlights" in data:
            matrix.active_spotlights = list(data["active_spotlights"])
        if "recent_chain_history" in data:
            matrix.recent_chain_history = list(data["recent_chain_history"])
        return matrix
