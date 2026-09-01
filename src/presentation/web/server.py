# -*- coding: utf-8 -*-
"""
src/presentation/web/server.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Presentation Layer: ThreadedHTTPServer 기반 REST API 및 웹 스튜디오 서빙 서버
- 완전한 비동기 멀티스레드 서빙으로 UI 프리징 0%
- SQLite WAL DB 및 Application Services와 100% 동적 바인딩
"""

from __future__ import annotations
import os
import json
import socketserver
import urllib.parse
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any

from src.infrastructure.database.db_manager import DBManager
from src.infrastructure.database.repositories import CharacterRepository, TurnLedgerRepository
from src.infrastructure.media.visual_compiler import VisualCompiler
from src.infrastructure.llm.client import MultiLLMClient
from src.infrastructure.llm.prompt_synthesizer import PromptSynthesizer
from src.application.classifier_service import ClassifierService
from src.application.gene_synthesis_service import GeneSynthesisService
from src.application.spec_compiler_service import SpecCompilerService
from src.application.master_synthesizer_service import MasterSynthesizerService
from src.application.static_validator import StaticValidator
from src.application.narrative_orchestrator import NarrativeOrchestrator
from src.application.undo_manager import UndoManager
from src.domain.character import Character


class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """멀티스레드 비동기 HTTP 서버"""
    allow_reuse_address = True
    daemon_threads = True


class StudioHandler(SimpleHTTPRequestHandler):
    """Web Studio REST API 및 정적 파일 핸들러"""

    # 서버 인스턴스 싱글톤 참조
    db_manager: DBManager = None
    char_repo: CharacterRepository = None
    turn_repo: TurnLedgerRepository = None
    llm_client: MultiLLMClient = None
    classifier_svc: ClassifierService = None
    synthesis_svc: GeneSynthesisService = None
    spec_compiler_svc: SpecCompilerService = None
    master_synthesizer_svc: MasterSynthesizerService = None
    narrative_orch: NarrativeOrchestrator = None
    undo_mgr: UndoManager = None

    @classmethod
    def initialize_services(cls, db_path: str = None) -> None:
        cls.db_manager = DBManager(db_path)
        cls.char_repo = CharacterRepository(cls.db_manager)
        cls.turn_repo = TurnLedgerRepository(cls.db_manager)
        cls.llm_client = MultiLLMClient()
        cls.classifier_svc = ClassifierService(cls.llm_client)
        cls.synthesis_svc = GeneSynthesisService(cls.char_repo, cls.llm_client)
        cls.spec_compiler_svc = SpecCompilerService(cls.llm_client)
        cls.master_synthesizer_svc = MasterSynthesizerService(cls.llm_client)
        cls.narrative_orch = NarrativeOrchestrator(cls.char_repo, cls.turn_repo, cls.llm_client)
        cls.undo_mgr = UndoManager(cls.turn_repo, cls.char_repo)
        
        # 4대 대표 캐릭터 시딩
        cls.char_repo.seed_defaults_if_empty()

    def do_GET(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        # 1. API Endpoints
        if path == "/api/characters":
            chars = self.char_repo.list_all()
            self._send_json([c.to_dict() for c in chars])
            return

        elif path == "/api/characters/active":
            active = self.char_repo.get_active()
            self._send_json(active.to_dict() if active else {})
            return

        elif path == "/api/turns":
            char_id = query.get("character_id", [None])[0]
            if char_id:
                history = self.turn_repo.get_history(int(char_id))
                self._send_json(history)
            else:
                active = self.char_repo.get_active()
                if active and active.id:
                    history = self.turn_repo.get_history(active.id)
                    self._send_json(history)
                else:
                    self._send_json([])
            return

        elif path == "/api/config":
            self._send_json({
                "llm_provider": self.llm_client.primary_provider,
                "gemini_model": self.llm_client.gemini_model,
                "anthropic_model": self.llm_client.anthropic_model,
                "has_gemini_key": bool(self.llm_client.gemini_key),
                "has_anthropic_key": bool(self.llm_client.anthropic_key)
            })
            return

        # 2. Static / HTML Serving
        web_root = Path(__file__).resolve().parent
        if path in ("/", "/index.html"):
            index_path = web_root / "templates" / "index.html"
            self._serve_file(index_path, "text/html; charset=utf-8")
            return

        if path.startswith("/static/"):
            rel_path = path[len("/static/"):]
            file_path = web_root / "static" / rel_path
            if file_path.exists() and file_path.is_file():
                content_type = self._guess_content_type(file_path)
                self._serve_file(file_path, content_type)
                return

        self.send_error(404, "File Not Found")

    def do_POST(self) -> None:
        path = self.path
        body_data = self._read_json_body()

        if path == "/api/characters/active":
            char_id = body_data.get("character_id")
            if char_id:
                success = self.char_repo.set_active(int(char_id))
                active = self.char_repo.get_active()
                self._send_json({"success": success, "active": active.to_dict() if active else {}})
            else:
                self._send_json({"error": "character_id required"}, status=400)
            return

        elif path == "/api/characters/classify":
            concept = body_data.get("concept", "")
            result = self.classifier_svc.resolve_vectors_and_seed(concept)
            self._send_json(result)
            return

        elif path == "/api/characters/compile-spec":
            target_name = body_data.get("target_name", "미상의 귀족")
            title = body_data.get("title", "귀족")
            seed_hash = body_data.get("seed_hash", "#GENE-70G-INIT")
            hard_invariants = body_data.get("hard_invariants", [])
            selected_vector = body_data.get("selected_vector", {})

            spec_data = self.spec_compiler_svc.compile_spec(
                target_name=target_name,
                title=title,
                seed_hash=seed_hash,
                hard_invariants=hard_invariants,
                selected_vector=selected_vector
            )
            self._send_json({"success": True, "spec": spec_data})
            return

        elif path == "/api/characters/synthesize-master":
            char_data = body_data.get("character_data", {})
            result = self.master_synthesizer_svc.synthesize_master_prompt(char_data)
            self._send_json(result)
            return

        elif path == "/api/characters/compile":
            target_name = body_data.get("target_name", "미상")
            title = body_data.get("title", "귀족")
            seed_hash = body_data.get("seed_hash", "")
            hard_invariants = body_data.get("hard_invariants", [])
            selected_vector = body_data.get("selected_vector", {})

            compiled_char = self.synthesis_svc.compile_character(
                target_name=target_name,
                title=title,
                seed_hash=seed_hash,
                hard_invariants=hard_invariants,
                selected_vector=selected_vector
            )
            self._send_json({"success": True, "character": compiled_char.to_dict()})
            return

        elif path == "/api/characters/delete":
            char_id = body_data.get("character_id")
            if char_id:
                success = self.char_repo.delete(int(char_id))
                self._send_json({"success": success})
            else:
                self._send_json({"error": "character_id required"}, status=400)
            return

        elif path == "/api/turns":
            char_id = body_data.get("character_id")
            action = body_data.get("user_action", "")
            stimulus = body_data.get("stimulus_type", "DEFAULT")

            if not char_id:
                active = self.char_repo.get_active()
                char_id = active.id if active else None

            if char_id and action:
                turn_result = self.narrative_orch.execute_turn(
                    character_id=int(char_id),
                    user_action=action,
                    stimulus_type=stimulus
                )
                self._send_json(turn_result)
            else:
                self._send_json({"error": "character_id and user_action required"}, status=400)
            return

        elif path == "/api/turns/undo":
            char_id = body_data.get("character_id")
            if not char_id:
                active = self.char_repo.get_active()
                char_id = active.id if active else None

            if char_id:
                undone = self.undo_mgr.undo_last_turn(int(char_id))
                active = self.char_repo.get_by_id(int(char_id))
                self._send_json({
                    "success": bool(undone),
                    "undone_turn": undone,
                    "active_gauges": active.traits.gauges.to_dict() if active else {}
                })
            else:
                self._send_json({"error": "character_id required"}, status=400)
            return

        elif path == "/api/turns/reset":
            char_id = body_data.get("character_id")
            if not char_id:
                active = self.char_repo.get_active()
                char_id = active.id if active else None

            if char_id:
                self.turn_repo.clear_history(int(char_id))
                self._send_json({"success": True})
            else:
                self._send_json({"error": "character_id required"}, status=400)
            return

        elif path == "/api/characters/danbooru":
            char_id = body_data.get("character_id")
            char = self.char_repo.get_by_id(int(char_id)) if char_id else self.char_repo.get_active()
            if char:
                pos, neg = VisualCompiler.compile_danbooru_prompt(char.name, char.visual_dna)
                self._send_json({"positive_prompt": pos, "negative_prompt": neg})
            else:
                self._send_json({"error": "character not found"}, status=404)
            return

        elif path == "/api/characters/prompt":
            char_id = body_data.get("character_id")
            char = self.char_repo.get_by_id(int(char_id)) if char_id else self.char_repo.get_active()
            if char:
                prompt_text = PromptSynthesizer.synthesize_master_system_prompt(char)
                self._send_json({"master_prompt": prompt_text})
            else:
                self._send_json({"error": "character not found"}, status=404)
            return

        elif path == "/api/import":
            json_str = body_data.get("character_json", "")
            try:
                char_data = json.loads(json_str) if isinstance(json_str, str) else json_str
                imported = Character.from_dict(char_data)
                imported.id = None  # 새 ID 발급
                saved = self.char_repo.save(imported)
                self._send_json({"success": True, "character": saved.to_dict()})
            except Exception as e:
                self._send_json({"error": f"Import failed: {str(e)}"}, status=400)
            return

        self.send_error(404, "Endpoint Not Found")

    def _read_json_body(self) -> Dict[str, Any]:
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 0:
                raw = self.rfile.read(content_length).decode("utf-8")
                return json.loads(raw)
        except Exception:
            pass
        return {}

    def _send_json(self, data: Any, status: int = 200) -> None:
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def _serve_file(self, file_path: Path, content_type: str) -> None:
        try:
            content = file_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")

    @staticmethod
    def _guess_content_type(path: Path) -> str:
        suffix = path.suffix.lower()
        mapping = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml"
        }
        return mapping.get(suffix, "application/octet-stream")


def run_server(port: int = 8000, db_path: str = None) -> None:
    """Web Studio 서버 구동 함수"""
    StudioHandler.initialize_services(db_path)
    server_address = ("0.0.0.0", port)
    httpd = ThreadedHTTPServer(server_address, StudioHandler)
    print(f"======================================================================")
    print(f"[AbyssEngine Studio Server] Running on http://127.0.0.1:{port}")
    print(f"  - Database: SQLite WAL (abyss_engine.db)")
    print(f"  - Concurrency: ThreadedHTTPServer (Zero-Freeze AJAX)")
    print(f"======================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()
        httpd.server_close()


if __name__ == "__main__":
    run_server()
