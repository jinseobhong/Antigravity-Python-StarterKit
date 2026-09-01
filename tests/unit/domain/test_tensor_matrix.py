# -*- coding: utf-8 -*-
"""
tests/unit/domain/test_tensor_matrix.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
17대 생체 텐서 및 Kinematic Chain 운동 연쇄 전이 단위 테스트 (Zero-Dependency unittest)
"""

import unittest
from src.domain.tensor_matrix import TensorMatrix, TENSOR_REGISTRY


class TestTensorMatrix(unittest.TestCase):

    def test_tensor_matrix_default_state(self):
        """17대 텐서 기본 초기화 검증"""
        matrix = TensorMatrix()
        self.assertEqual(len(matrix.levels), 17)
        for key in TENSOR_REGISTRY:
            self.assertEqual(matrix.get_level(key), 0.0)

    def test_tensor_matrix_stimulus_and_chain_propagation(self):
        """외력 가산 및 신체 운동 연쇄 파동 전이(시선 -> 성대 -> 경추) 검증"""
        matrix = TensorMatrix()

        # 1차 자극: 02_ocular (시선) 에 0.5 가산
        events = matrix.apply_stimulus("02_ocular", intensity=0.5)

        # 02_ocular는 0.5로 상승
        self.assertEqual(matrix.get_level("02_ocular"), 0.5)
        # 다음 연쇄 노드인 03_vocal (성대)로 60% 감쇠 전이 (0.5 * 0.6 = 0.3)
        self.assertAlmostEqual(matrix.get_level("03_vocal"), 0.3, places=5)
        # 스포트라이트에 두 노드가 활성화되어야 함
        self.assertIn("02_ocular", matrix.active_spotlights)
        self.assertIn("03_vocal", matrix.active_spotlights)
        self.assertEqual(len(events), 2)

    def test_tensor_matrix_saturation_limit(self):
        """텐서 상한선(1.0) 초과 방지 클램핑 검증"""
        matrix = TensorMatrix()
        matrix.apply_stimulus("04_cervical", intensity=0.8)
        matrix.apply_stimulus("04_cervical", intensity=0.8)

        self.assertEqual(matrix.get_level("04_cervical"), 1.0)

    def test_tensor_matrix_serialization(self):
        """직렬화 및 역직렬화 검증"""
        matrix1 = TensorMatrix()
        matrix1.apply_stimulus("06_thoracic", intensity=0.4)

        data = matrix1.to_dict()
        matrix2 = TensorMatrix.from_dict(data)

        self.assertEqual(matrix2.get_level("06_thoracic"), matrix1.get_level("06_thoracic"))
        self.assertEqual(matrix2.active_spotlights, matrix1.active_spotlights)
        self.assertEqual(matrix2.recent_chain_history, matrix1.recent_chain_history)


if __name__ == "__main__":
    unittest.main()
