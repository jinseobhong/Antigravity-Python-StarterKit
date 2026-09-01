# -*- coding: utf-8 -*-
"""
src/domain/visual_dna.py
~~~~~~~~~~~~~~~~~~~~~~~~
Domain Layer: 8-Tier 해부학적 외모 규격 모델 (Visual DNA Matrix)
- 안면 골격, 동공 광학, 모발 물리, 체형 실루엣, 표피 질감, 의복/초커, 생체 홍조, 조명 대비
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class VisualDNA:
    """8-Tier 해부학적 외모 규격"""
    face_geometry: str       # Tier 1: 턱선, 입술, 코선
    ocular_optics: str       # Tier 2: 홍채 색상, 동공 림, 속눈썹
    hair_physics: str        # Tier 3: 모발 길이, 색상, 결, 잔머리 물리
    body_silhouette: str     # Tier 4: 신장(cm), 체형 실루엣, 쇄골/골격 돌출도
    dermal_texture: str      # Tier 5: 피부 톤, 표피 질감, 핏줄 가시성
    apparel_accents: str     # Tier 6: 메인 의복 스타일, 초커/리본/갑주/장신구
    somatic_flush_cue: str   # Tier 7: 수치/체온 상승 시 쇄골·귓바퀴 홍조 경로
    lighting_contrast: str   # Tier 8: 기본 광원 대비 및 명암비
    danbooru_prompt: str = ""
    negative_prompt: str = ""

    def compile_literary_anchor(self) -> str:
        """서사용 문학 앵커 요약문 추출"""
        return (
            f"[외모 규격] {self.hair_physics}, {self.ocular_optics}, "
            f"{self.face_geometry}, {self.body_silhouette}, {self.apparel_accents}"
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
            "negative_prompt": self.negative_prompt,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> VisualDNA:
        return cls(
            face_geometry=data.get("face_geometry", "서늘하고 날렵한 턱선, 굳게 다문 얇은 입술"),
            ocular_optics=data.get("ocular_optics", "차가운 금빛 홍채와 짙은 속눈썹"),
            hair_physics=data.get("hair_physics", "허리까지 내려오는 백은색 직모"),
            body_silhouette=data.get("body_silhouette", "168cm 호리호리한 체형, 도드라진 쇄골"),
            dermal_texture=data.get("dermal_texture", "창백한 백옥 피부, 목덜미의 푸른 핏줄"),
            apparel_accents=data.get("apparel_accents", "검은 실크 오프숄더 드레스, 서늘한 은색 초커"),
            somatic_flush_cue=data.get("somatic_flush_cue", "수치 시 귓바퀴와 쇄골로 번지는 붉은 열감"),
            lighting_contrast=data.get("lighting_contrast", "차가운 달빛과 어둠 속의 극적인 명암 대비"),
            danbooru_prompt=data.get("danbooru_prompt", ""),
            negative_prompt=data.get("negative_prompt", "")
        )
