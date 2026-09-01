# -*- coding: utf-8 -*-
"""
src/infrastructure/media/visual_compiler.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Infrastructure Layer: Illustrious-XL 6-Slot Danbooru Tag Compiler
- 8-Tier Visual DNA로부터 고화질 단부루 태그(Positive & Negative) 1:1 컴파일
- Web UI의 'AI 일러스트 생성' 원클릭 연동 지원
"""

from __future__ import annotations
import re
from typing import Dict, Tuple
from src.models.visual_dna import VisualDNA


class VisualCompiler:
    """Illustrious-XL 6-Slot 단부루 태그 컴파일러"""

    MASTER_QUALITY_TAGS = "masterpiece, best quality, ultra-detailed, highres, absurdres"
    DEFAULT_NEGATIVE_TAGS = (
        "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, "
        "fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, "
        "signature, watermark, username, blurry, artist name, mutated hands, poorly drawn face"
    )

    @classmethod
    def compile_danbooru_prompt(cls, char_name: str, dna: VisualDNA) -> Tuple[str, str]:
        """8-Tier Visual DNA로부터 6-Slot 단부루 프롬프트 및 네거티브 프롬프트 생성"""
        
        # Slot 1: Master Quality
        slot_1 = cls.MASTER_QUALITY_TAGS

        # Slot 2: Character Name & Base Pose
        name_tag = re.sub(r'[^a-zA-Z0-9_]', '', char_name.lower()) or "girl"
        slot_2 = f"{name_tag}, 1girl, solo, dark_fantasy"

        # Slot 3: Hair & Eyes
        hair_tag = cls._extract_hair_tags(dna.hair_physics)
        eyes_tag = cls._extract_eye_tags(dna.ocular_optics)
        slot_3 = f"{hair_tag}, {eyes_tag}"

        # Slot 4: Apparel & Choker
        apparel_tag = cls._extract_apparel_tags(dna.apparel_accents)
        slot_4 = apparel_tag

        # Slot 5: Somatic & Sensorial Cues
        somatic_tag = cls._extract_somatic_tags(dna.somatic_flush_cue, dna.body_silhouette, dna.dermal_texture)
        slot_5 = somatic_tag

        # Slot 6: Lighting & Atmosphere
        lighting_tag = cls._extract_lighting_tags(dna.lighting_contrast)
        slot_6 = lighting_tag

        full_positive = f"{slot_1}, {slot_2}, {slot_3}, {slot_4}, {slot_5}, {slot_6}"
        # 중복 콤마 정리
        clean_positive = re.sub(r'\s*,\s*', ', ', full_positive).strip(', ')
        return clean_positive, cls.DEFAULT_NEGATIVE_TAGS

    @staticmethod
    def _extract_hair_tags(desc: str) -> str:
        tags = []
        if "은발" in desc or "백은" in desc or "silver" in desc.lower():
            tags.append("silver_hair")
        elif "백금발" in desc or "platinum" in desc.lower():
            tags.append("platinum_blonde_hair")
        elif "흑" in desc or "black" in desc.lower() or "자색" in desc:
            tags.append("purple_hair, dark_purple_hair")
        elif "핑크" in desc or "pink" in desc.lower():
            tags.append("pink_hair")
        else:
            tags.append("silver_hair")

        if "직모" in desc or "스트레이트" in desc or "straight" in desc.lower():
            tags.append("straight_hair")
        elif "단발" in desc or "short" in desc.lower():
            tags.append("short_hair")
        elif "웨이브" in desc or "wavy" in desc.lower():
            tags.append("wavy_hair")

        if "긴" in desc or "허리" in desc or "long" in desc.lower():
            tags.append("very_long_hair")
        return ", ".join(tags)

    @staticmethod
    def _extract_eye_tags(desc: str) -> str:
        tags = []
        if "금빛" in desc or "호박" in desc or "gold" in desc.lower():
            tags.append("golden_eyes, amber_eyes")
        elif "벽안" in desc or "푸른" in desc or "blue" in desc.lower():
            tags.append("blue_eyes")
        elif "자수정" in desc or "자안" in desc or "purple" in desc.lower():
            tags.append("purple_eyes")
        elif "루비" in desc or "적안" in desc or "red" in desc.lower():
            tags.append("red_eyes")
        else:
            tags.append("amber_eyes")
        tags.append("detailed_eyes")
        return ", ".join(tags)

    @staticmethod
    def _extract_apparel_tags(desc: str) -> str:
        tags = []
        if "오프숄더" in desc or "드레스" in desc or "dress" in desc.lower():
            tags.append("black_dress, off-shoulder_dress")
        elif "갑주" in desc or "흉갑" in desc or "armor" in desc.lower():
            tags.append("silver_armor, breastplate, gauntlets")
        elif "로브" in desc or "코르셋" in desc or "corset" in desc.lower():
            tags.append("corset, velvet_robe, cleavage")
        elif "레이스" in desc or "frill" in desc.lower():
            tags.append("frills_dress, worn_dress")

        if "초커" in desc or "choker" in desc.lower():
            tags.append("silver_choker, collar")
        return ", ".join(tags)

    @staticmethod
    def _extract_somatic_tags(flush: str, body: str, skin: str) -> str:
        tags = []
        if "쇄골" in body or "collarbone" in body.lower():
            tags.append("collarbone")
        if "백옥" in skin or "창백" in skin or "pale" in skin.lower():
            tags.append("pale_skin")
        if "홍조" in flush or "열감" in flush or "blush" in flush.lower():
            tags.append("blushing, heavy_blush")
        tags.append("trembling, skin_texture")
        return ", ".join(tags)

    @staticmethod
    def _extract_lighting_tags(desc: str) -> str:
        return "dramatic_shadow, cinematic_lighting, moonlight, deep_darkness"
