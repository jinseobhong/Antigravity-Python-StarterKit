# -*- coding: utf-8 -*-
"""
tests/unit/domain/test_pressure_stage.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
4단계 압력 궤적 상태 머신 단위 테스트 (Zero-Dependency unittest)
"""

import unittest
from src.domain.pressure_stage import PressureStage


class TestPressureStage(unittest.TestCase):

    def test_pressure_stage_transitions(self):
        """신경 오염도 구간별 정확한 단계 전이 검증"""
        self.assertEqual(PressureStage.from_neural_taint(0.0), PressureStage.STAGE_1_ELASTIC)
        self.assertEqual(PressureStage.from_neural_taint(24.9), PressureStage.STAGE_1_ELASTIC)

        self.assertEqual(PressureStage.from_neural_taint(25.0), PressureStage.STAGE_2_OVERLOAD)
        self.assertEqual(PressureStage.from_neural_taint(54.9), PressureStage.STAGE_2_OVERLOAD)

        self.assertEqual(PressureStage.from_neural_taint(55.0), PressureStage.STAGE_3_PLASTIC)
        self.assertEqual(PressureStage.from_neural_taint(84.9), PressureStage.STAGE_3_PLASTIC)

        self.assertEqual(PressureStage.from_neural_taint(85.0), PressureStage.STAGE_4_SUCTION)
        self.assertEqual(PressureStage.from_neural_taint(100.0), PressureStage.STAGE_4_SUCTION)

    def test_pressure_stage_levels(self):
        """레벨 정수 속성 검증"""
        self.assertEqual(PressureStage.STAGE_1_ELASTIC.level, 1)
        self.assertEqual(PressureStage.STAGE_2_OVERLOAD.level, 2)
        self.assertEqual(PressureStage.STAGE_3_PLASTIC.level, 3)
        self.assertEqual(PressureStage.STAGE_4_SUCTION.level, 4)


if __name__ == "__main__":
    unittest.main()
