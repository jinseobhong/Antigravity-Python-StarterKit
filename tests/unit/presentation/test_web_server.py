# -*- coding: utf-8 -*-
"""
tests/unit/presentation/test_web_server.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Clean 4-Tier 웹 스튜디오 서버 및 API 핸들러 단위 테스트 (Zero-Dependency unittest)
"""

import os
import unittest
from src.presentation.web.server import STUDIO_APP, TEMPLATES_DIR, STATIC_DIR


class TestWebStudioServer(unittest.TestCase):

    def test_templates_and_static_files_exist(self):
        """모듈화된 템플릿 및 정적 에셋 파일 존재성 검증"""
        index_html = os.path.join(TEMPLATES_DIR, "index.html")
        self.assertTrue(os.path.exists(index_html), "index.html 템플릿이 존재해야 합니다.")

        with open(index_html, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("AbyssEmpire Web Studio", content)
        self.assertIn("Play Room", content)
        self.assertIn("캐릭터 보관소", content)
        self.assertIn("단부루 태그", content)

        # CSS 및 JS 모듈 존재 검증
        style_css = os.path.join(STATIC_DIR, "css", "style.css")
        api_js = os.path.join(STATIC_DIR, "js", "api.js")
        app_js = os.path.join(STATIC_DIR, "js", "app.js")
        self.assertTrue(os.path.exists(style_css))
        self.assertTrue(os.path.exists(api_js))
        self.assertTrue(os.path.exists(app_js))

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
        selected = STUDIO_APP.select_character("#SERA-70G-3C2D")
        self.assertIsNotNone(selected)
        self.assertEqual(selected.name, "세라피나")

        payload = STUDIO_APP.get_state_payload()
        self.assertEqual(payload["character"]["name"], "세라피나")


if __name__ == "__main__":
    unittest.main()
