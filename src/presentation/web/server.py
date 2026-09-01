# -*- coding: utf-8 -*-
"""
src/presentation/web/server.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Clean 4-Tier 전용 로컬 웹 스튜디오 서버 (Python 표준 http.server 기반, 의존성 제로)
- 8-Tier Visual DNA & 70-Step Personality Genes 연동
- Dify 스타일 2단계 인간 결재선(HITL Checkpoint 1 & 2) REST API 완비
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

from src.domain.character import Character
from src.infrastructure.database.db_manager import DatabaseManager
from src.infrastructure.database.repositories import CharacterRepository, TurnLedgerRepository
from src.infrastructure.llm.client import MultiLLMClient
from src.infrastructure.llm.prompt_synthesizer import PromptSynthesizer
from src.infrastructure.media.visual_compiler import VisualCompiler
from src.application.classifier_service import ClassifierService
from src.application.gene_synthesis_service import GeneSynthesisService
from src.application.narrative_orchestrator import NarrativeOrchestrator


class WebStudioApp:
    """웹 스튜디오 4계층 백엔드 매니저"""

    def __init__(self, db_path: str = "abyss_engine.db"):
        self.db_manager = DatabaseManager(db_path=db_path)
        self.char_repo = CharacterRepository(self.db_manager)
        self.turn_repo = TurnLedgerRepository(self.db_manager)
        self.llm_client = MultiLLMClient()
        self.classifier = ClassifierService(self.llm_client)
        self.synthesis = GeneSynthesisService(self.char_repo, self.llm_client)

        chars = self.char_repo.list_all()
        self.active_character = chars[0] if chars else None

        self.orchestrator = NarrativeOrchestrator(
            character=self.active_character,
            char_repo=self.char_repo,
            turn_repo=self.turn_repo,
            llm_client=self.llm_client
        ) if self.active_character else None

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
        if not self.orchestrator or not self.active_character:
            return {"character": None, "step": 1, "chat_history": []}

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
            "chat_history": chat_history,
        }


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

        # 3. REST API (/api/...)
        elif parsed.path == "/api/state":
            self._send_json(STUDIO_APP.get_state_payload())

        elif parsed.path == "/api/characters":
            chars = [c.to_dict() for c in STUDIO_APP.char_repo.list_all()]
            self._send_json(chars)

        elif parsed.path == "/api/export_prompt":
            if STUDIO_APP.active_character:
                prompt = PromptSynthesizer.build_master_system_instruction(STUDIO_APP.active_character)
            else:
                prompt = "활성 캐릭터가 없습니다."
            self._send_json({"prompt": prompt})

        elif parsed.path == "/api/llm_status":
            has_gemini = bool(STUDIO_APP.llm_client.gemini_key)
            has_claude = bool(STUDIO_APP.llm_client.claude_key)
            masked_gemini = (STUDIO_APP.llm_client.gemini_key[:6] + "..." + STUDIO_APP.llm_client.gemini_key[-4:]) if has_gemini else "미등록"
            masked_claude = (STUDIO_APP.llm_client.claude_key[:6] + "..." + STUDIO_APP.llm_client.claude_key[-4:]) if has_claude else "미등록"
            self._send_json({
                "has_key": has_gemini or has_claude,
                "has_gemini": has_gemini,
                "has_claude": has_claude,
                "masked_gemini": masked_gemini,
                "masked_claude": masked_claude,
                "active_provider": STUDIO_APP.llm_client.active_provider,
                "active_model": STUDIO_APP.llm_client.model
            })

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        data = json.loads(body) if body else {}

        if parsed.path == "/api/config_llm":
            g_key = data.get("gemini_key", "").strip()
            c_key = data.get("claude_key", "").strip()
            provider = data.get("provider", "GEMINI").strip()
            STUDIO_APP.llm_client.set_keys_and_provider(gemini_key=g_key, claude_key=c_key, provider=provider)
            self._send_json({"status": "SUCCESS", "active_provider": STUDIO_APP.llm_client.active_provider})

        elif parsed.path == "/api/select_character":
            seed = data.get("seed_hash", "")
            STUDIO_APP.select_character(seed)
            self._send_json(STUDIO_APP.get_state_payload())

        elif parsed.path == "/api/classify_and_propose":
            query = data.get("query", "")
            result = STUDIO_APP.classifier.resolve_boundary_and_vectors(query)
            self._send_json(result)

        elif parsed.path == "/api/synthesize_character":
            char = STUDIO_APP.synthesis.synthesize_character(
                name=data.get("name", "새 캐릭터"),
                title=data.get("title", "고위 귀족"),
                faction=data.get("faction", "독립 세력"),
                hard_invariants_dict=data.get("hard_invariants", {}),
                selected_vector=data.get("selected_vector", {}),
                explicit_seed=data.get("seed_hash", "")
            )
            STUDIO_APP.select_character(char.seed_hash)
            self._send_json(STUDIO_APP.get_state_payload())

        elif parsed.path == "/api/action":
            action_text = data.get("action_text", "")
            if STUDIO_APP.orchestrator:
                STUDIO_APP.orchestrator.execute_turn(raw_action=action_text)
            self._send_json(STUDIO_APP.get_state_payload())

        elif parsed.path == "/api/undo":
            if STUDIO_APP.orchestrator:
                STUDIO_APP.orchestrator.rollback()
            self._send_json(STUDIO_APP.get_state_payload())

        elif parsed.path == "/api/reset":
            if STUDIO_APP.orchestrator:
                STUDIO_APP.orchestrator.current_turn = 1
                STUDIO_APP.orchestrator.history.clear()
                STUDIO_APP.orchestrator.undo_manager.clear()
            self._send_json(STUDIO_APP.get_state_payload())

        elif parsed.path == "/api/generate_danbooru":
            if STUDIO_APP.active_character:
                pos, neg = VisualCompiler.compile_danbooru_pair(STUDIO_APP.active_character)
            else:
                pos, neg = "", ""
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
