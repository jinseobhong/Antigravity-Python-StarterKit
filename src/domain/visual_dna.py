# -*- coding: utf-8 -*-
"""
src/domain/visual_dna.py
~~~~~~~~~~~~~~~~~~~~~~~~
8중 해부학적 외모 규격 (8-Tier Visual DNA Matrix) 도메인 모델
- 안면 골격, 동공 광학, 모발 물리, 체형 실루엣, 표피 질감, 의복/초커, 생체 홍조, 조명 대비
- 서사 묘사용 문학 앵커와 이미지 생성용(Danbooru) 태그를 1:1로 결합
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class VisualDNA:
    """8중 해부학적 외모 규격 엔티티"""
    face_geometry: str          # Tier 1: 턱선, 콧날, 입술 형상 (예: 서늘하고 날렵한 v-line, 굳게 다문 얇은 입술)
    ocular_optics: str          # Tier 2: 홍채 색, 림, 속눈썹, 시선 (예: 차가운 금빛 홍채, 짙은 호박색 림)
    hair_physics: str           # Tier 3: 기장, 질감, 옆머리 (예: 허리까지 오는 백은색 직모, 단정한 옆머리)
    body_silhouette: str        # Tier 4: 체형, 쇄골, 목선 (예: 168cm 호리호리한 체형, 도드라진 쇄골)
    dermal_texture: str         # Tier 5: 피부 톤, 표피 표식 (예: 창백한 백옥 피부, 목덜미의 푸른 핏줄)
    apparel_accents: str        # Tier 6: 의복, 초커, 코르셋 (예: 검은 실크 오프숄더 드레스, 차가운 은색 금속 초커)
    somatic_flush_cue: str      # Tier 7: 생체 홍조, 땀, 입술 떨림 (예: 쇄골과 귓바퀴를 타고 번지는 붉은 열감)
    lighting_contrast: str      # Tier 8: 환경광, 그림자 (예: 차가운 달빛 아래 반투명한 피부와 짙은 그림자)
    danbooru_prompt: str = ""   # Illustrious-XL 6-Slot 단부루 태그
    negative_prompt: str = ""   # 부정 태그

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> VisualDNA:
        return cls(
            face_geometry=data.get("face_geometry", "단정한 안면 골격"),
            ocular_optics=data.get("ocular_optics", "서늘한 눈동자"),
            hair_physics=data.get("hair_physics", "자연스럽게 흘러내린 머릿결"),
            body_silhouette=data.get("body_silhouette", "우아한 신체 실루엣"),
            dermal_texture=data.get("dermal_texture", "부드러운 피부결"),
            apparel_accents=data.get("apparel_accents", "몸에 맞춘 단정한 의복"),
            somatic_flush_cue=data.get("somatic_flush_cue", "긴장 시 쇄골에 번지는 미세한 열감"),
            lighting_contrast=data.get("lighting_contrast", "은은한 명암 대비"),
            danbooru_prompt=data.get("danbooru_prompt", "1girl, solo, masterpiece, highly detailed face"),
            negative_prompt=data.get("negative_prompt", "lowres, bad anatomy, worst quality, blurry")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "face_geometry": self.face_geometry,
            "ocular_optics": self.ocular_optics,
            "hair_physics": self.hair_physics,
            "body_silhouette": self.body_silhouette,
            "dermal_texture": self.dermal_texture,
            "apparel_accents": self.apparel_accents,
            "somatic_flush_cue": self.somatic_flush_cue,
            "lighting_contrast": self.lighting_contrast,
            "danbooru_prompt": self.danbooru_prompt,
            "negative_prompt": self.negative_prompt
        }

    def compile_literary_anchor(self) -> str:
        """LLM 서사 집필용 압축 문학적 앵커 반환"""
        return (
            f"[시각적 외모 앵커]: {self.hair_physics}, {self.ocular_optics}. "
            f"{self.face_geometry}, {self.dermal_texture}. "
            f"{self.apparel_accents}, {self.body_silhouette}."
        )
