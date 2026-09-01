# -*- coding: utf-8 -*-
"""
src/presentation/web/server.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Clean 4-Tier 전용 로컬 웹 스튜디오 서버 (Python 표준 http.server 기반, 의존성 제로)
- 모듈화된 프론트엔드 (static/css, static/js, templates/index.html) 정적 서빙
- 4대 대표 아키타입(릴리스, 에이라, 세라피나, 실비아) 서사 롤플레이 & 17대 텐서 API 완비
"""

from __future__ import annotations
import os
import sys
import json
import webbrowser
import threading
from typing import Optional, Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Windows 콘솔 UTF-8 인코딩 안전 보장
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.domain.character import Character, LowenArmor
from src.domain.relational_vector import RelationalVector
from src.infrastructure.database.db_manager import DatabaseManager
from src.infrastructure.database.repositories import CharacterRepository, TurnHistoryRepository
from src.infrastructure.llm.client import UniversalLLMClient
from src.infrastructure.media.danbooru_prompt_builder import DanbooruPromptBuilder
from src.application.character_workshop_service import CharacterWorkshopService
from src.application.narrative_orchestrator import NarrativeOrchestrator


class WebStudioApp:
    """웹 스튜디오 4계층 백엔드 매니저"""

    def __init__(self, db_path: str = "abyss_engine.db"):
        self.db_manager = DatabaseManager(db_path=db_path)
        self.char_repo = CharacterRepository(self.db_manager)
        self.turn_repo = TurnHistoryRepository(self.db_manager)
        self.workshop = CharacterWorkshopService(self.char_repo)
        self.llm_client = UniversalLLMClient()

        # 활성 캐릭터 복원 (기본: 릴리스)
        chars = self.char_repo.list_all()
        if chars:
            self.active_character = chars[0]
        else:
            self.active_character = self.workshop.import_json({
                "name": "릴리스",
                "title": "제1황녀",
                "faction": "제국 황실",
                "armor_type": "Rigid",
                "traits": {"외모_특징": "차가운 은발과 서늘한 금빛 동공"}
            })

        self.orchestrator = NarrativeOrchestrator(
            character=self.active_character,
            char_repo=self.char_repo,
            turn_repo=self.turn_repo,
            llm_client=self.llm_client
        )

    def select_character(self, seed_hash: str) -> Optional[Character]:
        char = self.char_repo.find_by_seed_hash(seed_hash)
        if char:
            self.active_character = char
            self.orchestrator = NarrativeOrchestrator(
                character=self.active_character,
                char_repo=self.char_repo,
                turn_repo=self.turn_repo,
                llm_client=self.llm_client
            )
            return char
        return None

    def get_state_payload(self) -> Dict[str, Any]:
        c = self.orchestrator.character
        chat_history = []
        for h in self.orchestrator.history:
            chat_history.append({"role": "user", "content": h["action"]})
            chat_history.append({"role": "assistant", "content": h["prose"]})

        last_action = self.orchestrator.history[-1]["action"] if self.orchestrator.history else ""
        last_narrative = self.orchestrator.history[-1]["prose"] if self.orchestrator.history else ""

        return {
            "character": c.to_dict(),
            "step": self.orchestrator.current_turn,
            "last_action": last_action,
            "last_narrative": last_narrative,
            "active_tensors": c.tensors.active_spotlights,
            "recent_chain": c.tensors.recent_chain_history[-1] if c.tensors.recent_chain_history else "신체 운동 연쇄 안정",
            "chat_history": chat_history,
        }


# 전역 백엔드 인스턴스
STUDIO_APP = WebStudioApp()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")


class WebStudioHandler(BaseHTTPRequestHandler):
    """Clean 4-Tier 웹 스튜디오 HTTP 요청 핸들러"""

    def do_GET(self):
        parsed = urlparse(self.path)

        # 1. 메인 HTML 서빙
        if parsed.path in ["/", "/index.html"]:
            template_path = os.path.join(TEMPLATES_DIR, "index.html")
            if os.path.exists(template_path):
                with open(template_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                self._send_html(html_content)
            else:
                self.send_error(404, "Template not found")

        # 2. 정적 에셋 서빙 (/static/...)
        elif parsed.path.startswith("/static/"):
            rel_path = parsed.path[len("/static/"):]
            file_path = os.path.join(STATIC_DIR, rel_path)
            self._serve_file(file_path)

        # 3. 초상화 정적 서빙 (/portraits/...)
        elif parsed.path.startswith("/portraits/"):
            rel_path = parsed.path[len("/portraits/"):]
            file_path = os.path.join(BASE_DIR, "portraits", rel_path)
            self._serve_file(file_path)

        # 4. REST API (/api/...)
        elif parsed.path == "/api/state":
            self._send_json(STUDIO_APP.get_state_payload())

        elif parsed.path == "/api/characters":
            chars = [c.to_dict() for c in STUDIO_APP.char_repo.list_all()]
            self._send_json(chars)

        elif parsed.path == "/api/export_prompt":
            prompt = STUDIO_APP.workshop.export_master_prompt(STUDIO_APP.active_character)
            self._send_json({"prompt": prompt})

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        data = json.loads(body) if body else {}

        if parsed.path == "/api/select_character":
            seed = data.get("seed_hash", "")
            STUDIO_APP.select_character(seed)
            self._send_json(STUDIO_APP.get_state_payload())

        elif parsed.path == "/api/action":
            action_text = data.get("action_text", "")
            STUDIO_APP.orchestrator.execute_turn(raw_action=action_text)
            self._send_json(STUDIO_APP.get_state_payload())

        elif parsed.path == "/api/undo":
            STUDIO_APP.orchestrator.rollback()
            self._send_json(STUDIO_APP.get_state_payload())

        elif parsed.path == "/api/reset":
            STUDIO_APP.orchestrator.current_turn = 1
            STUDIO_APP.orchestrator.history.clear()
            STUDIO_APP.orchestrator.undo_manager.clear()
            self._send_json(STUDIO_APP.get_state_payload())

        elif parsed.path == "/api/generate_danbooru":
            pos, neg = DanbooruPromptBuilder.compile_prompt_pair(STUDIO_APP.active_character)
            self._send_json({"positive": pos, "negative": neg})

        else:
            self.send_response(404)
            self.end_headers()

    def _serve_file(self, file_path: str):
        if os.path.exists(file_path) and os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            mime_map = {
                ".css": "text/css; charset=utf-8",
                ".js": "application/javascript; charset=utf-8",
                ".json": "application/json; charset=utf-8",
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".webp": "image/webp",
                ".svg": "image/svg+xml",
                ".html": "text/html; charset=utf-8",
            }
            content_type = mime_map.get(ext, "application/octet-stream")
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "public, max-age=3600")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()

    def _send_html(self, html_str: str):
        data = html_str.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, obj: Any, status_code: int = 200):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        # 무소음 콘솔
        return


def launch_web_studio(port: int = 8877, open_browser: bool = True):
    server = None
    target_port = port
    while target_port < port + 20:
        try:
            HTTPServer.allow_reuse_address = True
            server = HTTPServer(("127.0.0.1", target_port), WebStudioHandler)
            break
        except OSError:
            target_port += 1

    if not server:
        print("❌ 사용 가능한 포트를 찾을 수 없습니다.")
        return

    url = f"http://127.0.0.1:{target_port}"
    print(f"\n✨ [Clean 4-Tier Abyss Web Studio 가동 성공!] URL: {url}")
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("\nWeb Studio Closed.")


if __name__ == "__main__":
    launch_web_studio()
