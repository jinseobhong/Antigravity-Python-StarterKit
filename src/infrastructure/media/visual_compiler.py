# -*- coding: utf-8 -*-
"""
src/infrastructure/media/visual_compiler.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
이중 파이프라인 정밀 외모 컴파일러 (Dual-Pipeline Visual Compiler)
- 파이프라인 A: LLM 서사 집필용 압축 문학적 시각 앵커문
- 파이프라인 B: Illustrious-XL / SD 전용 6-Slot 단부루 태그 세트
"""

from __future__ import annotations
from typing import Tuple, Dict, Any
from src.domain.character import Character
from src.domain.visual_dna import VisualDNA


class VisualCompiler:
    """외모 DNA를 문학 서사 앵커와 이미지 태그로 컴파일하는 어댑터"""

    @staticmethod
    def compile_danbooru_pair(character: Character) -> Tuple[str, str]:
        """Illustrious-XL 전용 6-Slot 긍정/부정 프롬프트 컴파일"""
        v = character.visual_dna
        name_clean = character.name.lower().replace(" ", "_")

        # Slot 1: 품질/스타일
        slot_1 = "1girl, solo, masterpiece, best quality, highly detailed, expressive eyes, dynamic lighting"
        
        # Slot 2: 캐릭터 고유 앵커
        slot_2 = f"{name_clean}, elegant posture, looking at viewer"

        # Slot 3: 모발 및 눈동자
        hair_tags = "silver_hair, long_hair, straight_hair" if "은" in v.hair_physics or "백" in v.hair_physics else "dark_hair, long_hair"
        eye_tags = "golden_eyes, glowing_eyes" if "금" in v.ocular_optics else "blue_eyes"
        slot_3 = f"{hair_tags}, {eye_tags}"

        # Slot 4: 의복 및 초커/액세서리
        apparel_tags = "black_dress, off_shoulder_dress, choker, silver_choker, jewelry"
        slot_4 = apparel_tags

        # Slot 5: 신체 해부학 및 생체 홍조
        body_tags = "collarbone, pale_skin, slender, delicate_features"
        if "홍조" in v.somatic_flush_cue or "열감" in v.somatic_flush_cue:
            body_tags += ", slight_blush"
        slot_5 = body_tags

        # Slot 6: 배경 및 분위기
        slot_6 = "dark_fantasy, opulent_room, candle_light, moonlight, rim_lighting"

        positive_prompt = f"{slot_1}, {slot_2}, {slot_3}, {slot_4}, {slot_5}, {slot_6}"
        negative_prompt = (
            "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, "
            "cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, "
            "username, blurry, deformed face"
        )

        return positive_prompt, negative_prompt

    @staticmethod
    def compile_literary_anchor(character: Character) -> str:
        """LLM 서사 집필용 외모 주입구"""
        return character.visual_dna.compile_literary_anchor()
