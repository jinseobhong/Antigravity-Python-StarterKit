# -*- coding: utf-8 -*-
"""
src/infrastructure/media/danbooru_prompt_builder.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Illustrious-XL 전용 6-Slot 단부루(Danbooru) 태그 컴파일러
[Slot 1: Quality] -> [Slot 2: Framing] -> [Slot 3: Genetics & NSFW] -> [Slot 4: Armor & Pose] -> [Slot 5: Shader] -> [Slot 6: Atmosphere]
"""

from __future__ import annotations
from typing import Tuple, Dict, Any, Optional

from src.domain.character import Character, LowenArmor


class DanbooruPromptBuilder:
    """Illustrious-XL 전용 6-Slot 태그 컴파일러"""

    @classmethod
    def compile_prompt_pair(
        cls,
        character: Character,
        custom_request: str = ""
    ) -> Tuple[str, str]:
        """결정론적 6-Slot 단부루 긍정/부정 프롬프트 생성"""
        # Slot 1: 고정 품질 코어
        slot1_quality = "masterpiece, newest, aesthetic, sensitive, high resolution, 8k"

        # Slot 2: 구도 및 피사체
        slot2_framing = "1girl, solo, cowboy shot, upper body, looking at viewer"

        # 캐릭터 텍스트 분석
        traits_text = " ".join([str(v) for v in (character.traits or {}).values() if isinstance(v, str)])
        combined = f"{character.name} {character.title} {character.faction} {traits_text} {custom_request}".lower()

        # Slot 3: 헤어 및 안구 유전자
        hair_tags = []
        if any(w in combined for w in ["은발", "백발", "silver", "white hair"]):
            hair_tags.append("silver hair, white hair")
        elif any(w in combined for w in ["백금발", "금발", "platinum", "blonde"]):
            hair_tags.append("platinum blonde hair, blonde hair")
        elif any(w in combined for w in ["자발", "보라", "자줏빛", "purple", "violet hair"]):
            hair_tags.append("purple hair, violet hair")
        elif any(w in combined for w in ["흑발", "검은", "black hair"]):
            hair_tags.append("black hair")
        else:
            hair_tags.append("silver hair")

        eye_tags = []
        if any(w in combined for w in ["금안", "노란", "gold", "yellow eyes"]):
            eye_tags.append("golden eyes, yellow eyes")
        elif any(w in combined for w in ["적안", "붉은", "red", "crimson eyes"]):
            eye_tags.append("crimson eyes, red eyes")
        elif any(w in combined for w in ["청안", "벽안", "blue eyes", "sapphire eyes"]):
            eye_tags.append("sapphire eyes, blue eyes")
        elif any(w in combined for w in ["자안", "보라", "purple eyes", "violet eyes"]):
            eye_tags.append("violet eyes, purple eyes")
        else:
            eye_tags.append("glowing eyes")

        # Slot 4: 로웬 신체 갑주 및 의복
        if character.armor_type == LowenArmor.RIGID:
            expr = "haughty expression, blushing, sharp gaze"
            armor = "ornate military uniform, metal choker, black choker, plunging neckline, deep cleavage, bare collarbone"
        elif character.armor_type == LowenArmor.CONTROLLER:
            expr = "seductive smirk, bedroom eyes, parted lips"
            armor = "open plunging velvet robe, translucent silk lingerie, exposed cleavage, bare shoulders"
        elif character.armor_type == LowenArmor.ENDURER:
            expr = "breathless, vulnerable expression, blushing, biting lip"
            armor = "silver plate armor corset, engraved pauldrons, metal collar, form-fitting armor, exposed collarbone"
        elif character.armor_type == LowenArmor.DEPRIVED:
            expr = "melancholic, teary eyes, moist lips, vulnerable"
            armor = "antique black lace dress, gothic lace choker, plunging sheer neckline, bare collarbone, deep cleavage"
        else:
            expr = "blushing, parted lips, vulnerable expression"
            armor = "silver plate armor corset, metal choker, plunging neckline, exposed collarbone"

        slot3_genetics = f"nsfw, cleavage, bare shoulders, exposed skin, {', '.join(hair_tags)}, {', '.join(eye_tags)}, {expr}"
        slot4_armor = armor
        slot5_shader = "detailed eyes, glowing eyes, intricate eyes, clean lines, detailed lineart, anime coloring, dramatic lighting, strong rim light, reflective, metallic sheen, lustrous"

        # 배경 및 분위기
        if any(w in combined for w in ["성당", "교단", "신성", "endurer"]):
            bg = "ornate cathedral background"
        elif any(w in combined for w in ["마탑", "마법", "controller"]):
            bg = "ornate magical library background"
        elif any(w in combined for w in ["귀족", "영애", "deprived"]):
            bg = "ornate dark room background"
        else:
            bg = "ornate imperial throne room background"

        slot6_atmosphere = f"sparkles, floating glowing particles, glint, depth of field, {bg}, suggestive"

        positive_prompt = f"{slot1_quality}, {slot2_framing}, {slot3_genetics}, {slot4_armor}, {slot5_shader}, {slot6_atmosphere}"
        negative_prompt = (
            "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, "
            "cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, "
            "username, blurry, artist name, simple background, flat lighting, bad eyes, (crossed eyes, strabismus, asymmetric eyes, mismatched pupils:1.3), deformed iris, deformed pupils"
        )

        return positive_prompt, negative_prompt
