# -*- coding: utf-8 -*-
"""
tests/unit/infrastructure/test_danbooru_prompt_builder.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Illustrious-XL 6-Slot 단부루 태그 컴파일러 단위 테스트 (Zero-Dependency unittest)
"""

import unittest

from src.domain.character import Character, LowenArmor
from src.infrastructure.media.danbooru_prompt_builder import DanbooruPromptBuilder


class TestDanbooruPromptBuilder(unittest.TestCase):

    def test_compile_prompt_pair_for_rigid_armor(self):
        """Rigid 갑주 캐릭터 단부루 6-Slot 태그 컴파일 검증"""
        char = Character(
            name="릴리스",
            title="제1황녀",
            faction="황실",
            armor_type=LowenArmor.RIGID,
            traits={"외모": "은발과 금안, 금속 초커"}
        )

        pos, neg = DanbooruPromptBuilder.compile_prompt_pair(char)

        # Slot 1: 고정 품질
        self.assertIn("masterpiece, newest, aesthetic", pos)
        # Slot 2: 구도
        self.assertIn("1girl, solo, cowboy shot", pos)
        # Slot 3: 유전자
        self.assertIn("silver hair", pos)
        self.assertIn("golden eyes", pos)
        # Slot 4: 로웬 갑주 의복
        self.assertIn("choker", pos)
        # 부정 프롬프트
        self.assertIn("bad anatomy", neg)
        self.assertIn("bad hands", neg)

    def test_compile_prompt_pair_for_controller_armor(self):
        """Controller 갑주 캐릭터 단부루 태그 검증"""
        char = Character(
            name="세라피나",
            title="대마도사",
            faction="마탑",
            armor_type=LowenArmor.CONTROLLER,
            traits={"외모": "자발과 자안"}
        )

        pos, _ = DanbooruPromptBuilder.compile_prompt_pair(char)
        self.assertIn("purple hair", pos)
        self.assertIn("violet eyes", pos)
        self.assertIn("seductive smirk", pos)


if __name__ == "__main__":
    unittest.main()
