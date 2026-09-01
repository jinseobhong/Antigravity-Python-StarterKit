# -*- coding: utf-8 -*-
"""
tests/unit/presentation/test_prose_sanitizer.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ProseSanitizer 시스템 태그 박멸 및 대사 서식화 단위 테스트 (Zero-Dependency unittest)
"""

import unittest
from src.presentation.prose_sanitizer import ProseSanitizer


class TestProseSanitizer(unittest.TestCase):

    def test_sanitize_removes_system_tags(self):
        """[SOM_...], [STATUS] 등 기계적 시스템 태그 완벽 소멸 검증"""
        raw_llm_out = (
            "[NARRATIVE] [SOM_04_CERVICAL] 엘레나의 경추가 굳어졌다. "
            "[STATUS: Taint +10%] Step 1에서 전이된 자극은 흉곽을 압박했다. "
            '"어째서 그런 눈으로 보는 거죠?" 그녀는 떨리는 목소리로 물었다.'
        )

        clean = ProseSanitizer.sanitize(raw_llm_out)

        self.assertNotIn("[SOM_", clean)
        self.assertNotIn("[STATUS", clean)
        self.assertNotIn("[NARRATIVE]", clean)
        self.assertNotIn("Step 1에서", clean)
        self.assertIn('"어째서 그런 눈으로 보는 거죠?"', clean)

    def test_sanitize_dialogue_paragraph_separation(self):
        """대사(\"...\")가 독립된 줄로 분리되는지 검증"""
        raw = '그녀는 고개를 저었다. "절대 굴복하지 않아." 그리고 눈을 감았다.'
        clean = ProseSanitizer.sanitize(raw)

        self.assertIn('\n\n"절대 굴복하지 않아."\n\n', clean)


if __name__ == "__main__":
    unittest.main()
