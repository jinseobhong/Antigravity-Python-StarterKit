# -*- coding: utf-8 -*-
"""
tests/unit/domain/test_character.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Character 엔티티 및 로웬 신체 갑주 단위 테스트 (Zero-Dependency unittest)
"""

import unittest
from src.domain.character import Character, LowenArmor
from src.domain.pressure_stage import PressureStage


class TestCharacter(unittest.TestCase):

    def test_character_initialization_and_seed_hash(self):
        """캐릭터 생성 시 고유 seed_hash 결정론적 생성 검증"""
        char = Character(
            name="엘레나",
            title="제국 성기사단장",
            faction="신성 제국",
            armor_type=LowenArmor.RIGID,
        )

        self.assertEqual(char.name, "엘레나")
        self.assertEqual(char.armor_type, LowenArmor.RIGID)
        self.assertEqual(char.ego_durability, 100.0)
        self.assertEqual(char.neural_taint, 0.0)
        self.assertEqual(char.pressure_stage, PressureStage.STAGE_1_ELASTIC)
        self.assertEqual(len(char.seed_hash), 16)

    def test_character_damage_and_pressure_transition(self):
        """자아 내구도 감소 및 오염도 증가에 따른 압력 단계 전이 검증"""
        char = Character(
            name="엘레나",
            title="성기사단장",
            faction="신성 제국",
            armor_type=LowenArmor.RIGID,
        )

        # Stage 1 -> Stage 2 (Taint 30)
        char.apply_damage_and_taint(ego_damage=20.0, taint_gain=30.0)
        self.assertEqual(char.ego_durability, 80.0)
        self.assertEqual(char.neural_taint, 30.0)
        self.assertEqual(char.pressure_stage, PressureStage.STAGE_2_OVERLOAD)

        # Stage 2 -> Stage 3 (Taint 60)
        char.apply_damage_and_taint(ego_damage=30.0, taint_gain=30.0)
        self.assertEqual(char.ego_durability, 50.0)
        self.assertEqual(char.neural_taint, 60.0)
        self.assertEqual(char.pressure_stage, PressureStage.STAGE_3_PLASTIC)

        # Stage 3 -> Stage 4 (Taint 90)
        char.apply_damage_and_taint(ego_damage=40.0, taint_gain=30.0)
        self.assertEqual(char.ego_durability, 10.0)
        self.assertEqual(char.neural_taint, 90.0)
        self.assertEqual(char.pressure_stage, PressureStage.STAGE_4_SUCTION)

    def test_character_serialization_roundtrip(self):
        """직렬화 및 역직렬화 무결성 검증"""
        char1 = Character(
            name="세라",
            title="대마법사",
            faction="학술원",
            armor_type=LowenArmor.DETACHED,
            traits={"결핍": "정서적 고립", "트라우마": "화재"},
        )
        char1.apply_damage_and_taint(15.0, 40.0)

        char_dict = char1.to_dict()
        char2 = Character.from_dict(char_dict)

        self.assertEqual(char2.name, char1.name)
        self.assertEqual(char2.armor_type, LowenArmor.DETACHED)
        self.assertEqual(char2.ego_durability, char1.ego_durability)
        self.assertEqual(char2.neural_taint, char1.neural_taint)
        self.assertEqual(char2.traits, char1.traits)
        self.assertEqual(char2.pressure_stage, char1.pressure_stage)


if __name__ == "__main__":
    unittest.main()
