# -*- coding: utf-8 -*-
"""
tests/e2e/test_web_api_e2e.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Contract-Driven E2E Tracer Bullet Integration Test Suite for AbyssEngine Web Studio
- E2E HTTP Endpoints Verification (No Mocking)
"""

import unittest
import threading
import time
import urllib.request
import json
import tempfile
from pathlib import Path

from src.infrastructure.database.db_manager import DBManager
from src.presentation.web.server import ThreadedHTTPServer, StudioHandler


class TestWebAPIEndToEnd(unittest.TestCase):
    """실제 HTTP 서버 구동 기반 E2E 통합 테스트"""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.db_path = f"{cls.temp_dir.name}/test_e2e.db"
        
        # 서비스 싱글톤 초기화
        StudioHandler.initialize_services(cls.db_path)

        # 빈 포트 할당하여 서버 기동
        cls.server = ThreadedHTTPServer(("127.0.0.1", 0), StudioHandler)
        cls.port = cls.server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{cls.port}"

        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.temp_dir.cleanup()

    def _http_get(self, path: str) -> dict | list:
        url = f"{self.base_url}{path}"
        req = urllib.request.Request(url, headers={"User-Agent": "E2ETest"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            self.assertEqual(resp.status, 200)
            data = resp.read().decode("utf-8")
            return json.loads(data)

    def _http_post(self, path: str, payload: dict) -> dict:
        url = f"{self.base_url}{path}"
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            self.assertEqual(resp.status, 200)
            data = resp.read().decode("utf-8")
            return json.loads(data)

    def test_01_get_initial_state_and_characters(self):
        """1. 초기 상태 및 기본 캐릭터 목록 조회 검증"""
        state = self._http_get("/api/state")
        self.assertIn("character", state)
        self.assertIn("chat_history", state)

        chars = self._http_get("/api/characters")
        self.assertIsInstance(chars, list)

    def test_02_full_character_creation_and_apply_flow(self):
        """2. Dify 11-Node 캐릭터 생성 풀 파이프라인 (컨셉 ➔ V1/V2 ➔ 스펙 ➔ 영구 저장) 검증"""
        # Step 1: 컨셉 역산 (Node 3)
        classify_res = self._http_post("/api/characters/classify", {
            "concept": "차가운 은룡 황녀 실비아, 가문의 부채를 갚기 위해 은색 초커를 착용"
        })
        self.assertIn("target_name", classify_res)
        self.assertIn("seed_hash", classify_res)
        self.assertIn("resolution_vectors", classify_res)
        self.assertGreaterEqual(len(classify_res["resolution_vectors"]), 2)

        target_name = classify_res["target_name"]
        seed_hash = classify_res["seed_hash"]
        selected_vector = classify_res["resolution_vectors"][0]

        # Step 2: 8-Tier DNA & 70-Gene 스펙 컴파일 (Node 7)
        compile_res = self._http_post("/api/characters/compile-spec", {
            "target_name": target_name,
            "title": classify_res.get("title", "은룡의 후예"),
            "seed_hash": seed_hash,
            "hard_invariants": classify_res.get("hard_invariants", []),
            "selected_vector": selected_vector
        })
        self.assertTrue(compile_res.get("success"))
        self.assertIn("spec", compile_res)
        self.assertIn("danbooru_prompt", compile_res["spec"])

        # Step 3: RDB 영구 저장 및 활성화 (Node 11 & DB)
        create_res = self._http_post("/api/create_character", {
            "target_name": target_name,
            "title": classify_res.get("title", "은룡의 후예"),
            "seed_hash": seed_hash,
            "hard_invariants": classify_res.get("hard_invariants", []),
            "selected_vector": selected_vector
        })
        self.assertIn("character", create_res)
        self.assertEqual(create_res["character"]["seed_hash"], seed_hash)

        # Step 4: DB에서 실제로 조회가 되는지 확인
        state_after = self._http_get("/api/state")
        self.assertEqual(state_after["character"]["seed_hash"], seed_hash)

    def test_03_roleplay_turn_execution_undo_and_reset(self):
        """3. 1:1 서사 턴 전송 ➔ 턴 원장 누적 ➔ Undo 롤백 ➔ Reset 검증"""
        # 턴 1 전송
        action_res_1 = self._http_post("/api/action", {
            "action_text": "떨리는 은색 초커 부근을 조용히 응시하며 굳게 닫힌 입술을 손끝으로 가리킨다.",
            "vector_type": "SUBJUGATION",
            "choice_id": "2"
        })
        self.assertIn("character", action_res_1)
        self.assertEqual(action_res_1["step"], 2)
        self.assertEqual(len(action_res_1["chat_history"]), 1)

        # 턴 2 전송
        action_res_2 = self._http_post("/api/action", {
            "action_text": "외투를 벗어 황녀의 어깨에 걸쳐주며 체온을 전달한다.",
            "vector_type": "DEVOTION_COMFORT",
            "choice_id": "1"
        })
        self.assertEqual(action_res_2["step"], 3)
        self.assertEqual(len(action_res_2["chat_history"]), 2)

        # Undo 실행 (턴 2 롤백)
        undo_res = self._http_post("/api/undo", {})
        self.assertTrue(undo_res.get("success"))
        self.assertEqual(undo_res["step"], 2)
        self.assertEqual(len(undo_res["chat_history"]), 1)

        # Reset 실행 (전체 초기화)
        reset_res = self._http_post("/api/reset", {})
        self.assertTrue(reset_res.get("success"))
        self.assertEqual(len(reset_res["chat_history"]), 0)

    def test_04_select_and_delete_character(self):
        """4. 상주 캐릭터 교체 및 삭제 검증"""
        # 캐릭터 1 생성
        self._http_post("/api/create_character", {
            "target_name": "벨리아",
            "title": "홍염의 죄수",
            "seed_hash": "#VELI-70G-E2E1",
            "hard_invariants": ["역린 방어"],
            "selected_vector": {"vector_id": "V1", "armor_type": "Rigid"}
        })
        # 캐릭터 2 생성
        self._http_post("/api/create_character", {
            "target_name": "카밀라",
            "title": "성기사단장",
            "seed_hash": "#CAMI-70G-E2E2",
            "hard_invariants": ["성약 서약"],
            "selected_vector": {"vector_id": "V2", "armor_type": "Endurer"}
        })

        chars = self._http_get("/api/characters")
        self.assertGreaterEqual(len(chars), 2)
        char_a = chars[0]
        char_b = chars[1]

        # char_b로 상주 캐릭터 전환
        select_res = self._http_post("/api/select_character", {
            "seed_hash": char_b["seed_hash"]
        })
        self.assertEqual(select_res["character"]["seed_hash"], char_b["seed_hash"])

        # char_a 삭제
        del_res = self._http_post("/api/delete_character", {
            "seed_hash": char_a["seed_hash"]
        })
        self.assertTrue(del_res.get("success"))


if __name__ == "__main__":
    unittest.main()
