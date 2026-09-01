# -*- coding: utf-8 -*-
"""
tests/unit/application/test_undo_manager.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
UndoManager 및 TurnSnapshot 롤백 무결성 단위 테스트 (Zero-Dependency unittest)
"""

import unittest

from src.domain.character import Character, LowenArmor
from src.application.undo_manager import UndoManager


class TestUndoManager(unittest.TestCase):

    def test_undo_stack_push_pop_and_restoration(self):
        """TurnSnapshot 푸시, 팝 및 캐릭터 엔티티 복원 검증"""
        manager = UndoManager()
        self.assertFalse(manager.can_undo)
        self.assertEqual(manager.history_depth, 0)

        # 1. 초기 캐릭터 상태
        char = Character(
            name="엘레나",
            title="성기사",
            faction="제국",
            armor_type=LowenArmor.RIGID,
        )

        # 턴 1 상태 스냅샷 저장
        manager.push_snapshot(
            turn_number=1,
            character=char,
            user_action="인사한다",
            narrative_prose="그녀가 바라본다.",
        )
        self.assertTrue(manager.can_undo)
        self.assertEqual(manager.history_depth, 1)

        # 2. 턴 2로 상태 변형 (자아 80, 오염 30)
        char.apply_damage_and_taint(ego_damage=20.0, taint_gain=30.0)
        self.assertEqual(char.ego_durability, 80.0)
        self.assertEqual(char.neural_taint, 30.0)

        # 3. 롤백 수행
        snapshot = manager.pop_snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(snapshot.turn_number, 1)

        restored_char = manager.restore_character(snapshot)
        self.assertEqual(restored_char.name, "엘레나")
        self.assertEqual(restored_char.ego_durability, 100.0)
        self.assertEqual(restored_char.neural_taint, 0.0)
        self.assertFalse(manager.can_undo)


if __name__ == "__main__":
    unittest.main()
