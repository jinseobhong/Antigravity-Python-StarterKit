# -*- coding: utf-8 -*-
"""
tests/unit/presentation/test_web_server.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Clean 4-Tier 웹 스튜디오 서버 및 API 핸들러 단위 테스트 (Zero-Dependency unittest)
"""

import unittest
from src.presentation.web.server import STUDIO_APP, HTML_PAGE


class TestWebStudioServer(unittest.TestCase):

    def test_html_page_contains_required_sections(self):
        """웹 대시보드 필수 컴포넌트 렌더링 검증"""
        self.assertIn("AbyssEmpire Web Studio", HTML_PAGE)
        self.assertIn("Play Room", HTML_PAGE)
        self.assertIn("캐릭터 보관소", HTML_PAGE)
        self.assertIn("단부루 6-Slot 태그 생성", HTML_PAGE)

    def test_studio_app_state_payload(self):
        """백엔드 상태 페이로드 무결성 검증"""
        payload = STUDIO_APP.get_state_payload()
        self.assertIn("character", payload)
        self.assertIn("step", payload)
        self.assertIn("chat_history", payload)
        self.assertIn("active_tensors", payload)
        self.assertEqual(payload["step"], 1)

    def test_studio_app_character_selection(self):
        """캐릭터 선택 및 오케스트레이터 재초기화 검증"""
        # 세라피나 선택
        selected = STUDIO_APP.select_character("#SERA-70G-3C2D")
        self.assertIsNotNone(selected)
        self.assertEqual(selected.name, "세라피나")

        payload = STUDIO_APP.get_state_payload()
        self.assertEqual(payload["character"]["name"], "세라피나")


if __name__ == "__main__":
    unittest.main()
