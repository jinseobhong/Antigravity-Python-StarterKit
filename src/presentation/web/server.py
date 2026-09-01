# -*- coding: utf-8 -*-
"""
src/presentation/web/server.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Presentation Layer: ThreadedHTTPServer 기반 고반응형 REST API 및 웹 스튜디오 서빙 서버
- 완전한 비동기 멀티스레드 서빙으로 UI 프리징 0%
- 토스트 알림, 로딩 스피너, 타이프라이터 스트림, 10대 모달과 100% 동적 바인딩
- SQLite WAL DB 및 Clean 4-Tier Application Services와 완벽 연동
"""

from __future__ import annotations
import os
import json
import socketserver
import urllib.parse
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any, List

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
from src.domain.gene_seed import GeneSeed


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

        # 1. State 조회 (단일 진실 공급원)
        if path == "/api/state":
            active = self.char_repo.get_active()
            if not active:
                chars = self.char_repo.list_all()
                if chars:
                    active = chars[0]
                    self.char_repo.set_active(active.id)
            
            if active:
                history = self.turn_repo.get_history(active.id)
                last_turn = history[-1] if history else {}
                state_data = {
                    "character": self._char_to_view_dict(active),
                    "chat_history": [
                        {
                            "step": h.get("turn_number", 1),
                            "user_action": h.get("user_action", ""),
                            "narrative_prose": h.get("narrative_response", ""),
                            "pressure_stage": active.traits.stage_progression
                        }
                        for h in history
                    ],
                    "step": len(history) + 1,
                    "last_action": last_turn.get("user_action", ""),
                    "last_narrative": last_turn.get("narrative_response", "차가운 공기 속에서 그녀가 당신을 응시하고 있습니다."),
                    "active_tensors": ["04_cervical_and_choker", "05_clavicle", "14_apparel_tension"],
                    "choices": [
                        {"type": "DEVOTION_COMFORT", "text": "떨리는 어깨에 조용히 외투를 걸쳐주며 더 이상 홀로 짊어질 필요 없다고 위로한다."},
                        {"type": "SUBJUGATION", "text": "치켜든 턱을 거세게 쥐어 올리며 가문의 위선과 오만한 긍지를 짓누른다."},
                        {"type": "SUBMISSION_FAWN", "text": "황녀의 구두 앞에 정중히 한쪽 무릎을 꿇고 손등을 들어 올려 입을 맞춘다."},
                        {"type": "SOMATIC_SYNC", "text": "경직된 목덜미와 쇄골 부근을 서늘한 손끝으로 쓸어내리며 체온 변화를 유도한다."},
                        {"type": "SUSPENSION", "text": "차갑게 뒤돌아서서 침묵으로 일관하며 오만한 시선을 고립시킨다."}
                    ]
                }
                self._send_json(state_data)
            else:
                self._send_json({
                    "character": None,
                    "chat_history": [],
                    "step": 1,
                    "last_action": "",
                    "last_narrative": "",
                    "active_tensors": [],
                    "choices": []
                })
            return

        # 2. 전체 캐릭터 목록 조회
        elif path == "/api/characters":
            chars = self.char_repo.list_all()
            self._send_json([self._char_to_view_dict(c) for c in chars])
            return

        elif path == "/api/characters/active":
            active = self.char_repo.get_active()
            self._send_json(self._char_to_view_dict(active) if active else {})
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

        elif path == "/api/export_json":
            seed_hash = query.get("seed_hash", [""])[0]
            char = self.char_repo.get_by_seed(seed_hash) if seed_hash else self.char_repo.get_active()
            if char:
                json_str = json.dumps(char.to_dict(), ensure_ascii=False, indent=2)
                self._send_json({
                    "filename": f"{char.name}_{char.seed_hash}.json",
                    "json_str": json_str
                })
            else:
                self._send_json({"error": "Character not found"}, status=404)
            return

        elif path == "/api/llm_config" or path == "/api/config":
            self._send_json({
                "success": True,
                "provider": self.llm_client.primary_provider,
                "gemini_model": self.llm_client.gemini_model,
                "anthropic_model": self.llm_client.anthropic_model,
                "has_gemini_key": bool(self.llm_client.gemini_key),
                "has_anthropic_key": bool(self.llm_client.anthropic_key),
                "anthropic_workspace_id": self.llm_client.anthropic_workspace_id
            })
            return

        # Static / HTML Serving
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

        # 1. 캐릭터 선택 (Select Active Character)
        if path in ("/api/select_character", "/api/characters/active"):
            seed_hash = body_data.get("seed_hash")
            char_id = body_data.get("character_id")
            
            char = None
            if seed_hash:
                char = self.char_repo.get_by_seed(seed_hash)
            elif char_id:
                char = self.char_repo.get_by_id(int(char_id))
            
            if char and char.id:
                self.char_repo.set_active(char.id)
                self._send_state_response(char)
            else:
                self._send_json({"error": "Character not found"}, status=404)
            return

        # 2. 턴 행동 실행 (Execute Turn / Action)
        elif path in ("/api/action", "/api/turns"):
            action_text = body_data.get("action_text") or body_data.get("user_action") or body_data.get("custom_text") or ""
            stimulus = body_data.get("vector_type") or body_data.get("stimulus_type") or "DEFAULT"
            char_id = body_data.get("character_id")

            active = self.char_repo.get_by_id(int(char_id)) if char_id else self.char_repo.get_active()
            if not active or not active.id:
                active = self.char_repo.list_all()[0]
                self.char_repo.set_active(active.id)

            if active and action_text:
                turn_result = self.narrative_orch.execute_turn(
                    character_id=active.id,
                    user_action=action_text,
                    stimulus_type=stimulus
                )
                self._send_state_response(active)
            else:
                self._send_json({"error": "action_text required"}, status=400)
            return

        # 3. Undo 실행
        elif path in ("/api/undo", "/api/turns/undo"):
            active = self.char_repo.get_active()
            if active and active.id:
                undone = self.undo_mgr.undo_last_turn(active.id)
                if undone:
                    self._send_state_response(active, extra={"success": True, "undone": undone})
                else:
                    self._send_json({"success": False, "error": "No more turns to undo"})
            else:
                self._send_json({"error": "No active character"}, status=400)
            return

        # 4. Reset 실행
        elif path in ("/api/reset", "/api/turns/reset"):
            active = self.char_repo.get_active()
            if active and active.id:
                self.turn_repo.clear_history(active.id)
                self._send_state_response(active, extra={"success": True})
            else:
                self._send_json({"error": "No active character"}, status=400)
            return

        # 5. Dify Node 3: 제약선 및 직교 2대 궤적 역산
        elif path == "/api/characters/classify":
            concept = body_data.get("concept", "")
            result = self.classifier_svc.resolve_vectors_and_seed(concept)
            self._send_json(result)
            return

        # 6. Dify Node 7: 8-Tier DNA & 70-Gene 스펙 컴파일
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

        # 7. Dify Node 10: 30,000자급 마스터 시스템 헌법 합성
        elif path == "/api/characters/synthesize-master":
            char_data = body_data.get("character_data", {})
            result = self.master_synthesizer_svc.synthesize_master_prompt(char_data)
            self._send_json(result)
            return

        # 8. 캐릭터 생성 & 컴파일 (Create Character)
        elif path in ("/api/create_character", "/api/characters/compile"):
            target_name = body_data.get("name") or body_data.get("target_name", "미상의 귀족")
            title = body_data.get("title", "귀족")
            seed_hash = body_data.get("seed_hash", "")
            raw_text = body_data.get("raw_text", "")
            hard_invariants = body_data.get("hard_invariants", [])
            selected_vector = body_data.get("selected_vector", {})
            traits_input = body_data.get("traits", {})

            if raw_text and not hard_invariants:
                res = self.classifier_svc.resolve_vectors_and_seed(raw_text)
                target_name = res.get("target_name") or target_name
                title = res.get("title") or title
                seed_hash = res.get("seed_hash") or seed_hash
                hard_invariants = res.get("hard_invariants", [])
                selected_vector = res.get("resolution_vectors", [{}])[0]

            compiled_char = self.synthesis_svc.compile_character(
                target_name=target_name,
                title=title,
                seed_hash=seed_hash,
                hard_invariants=hard_invariants,
                selected_vector=selected_vector
            )
            self._send_state_response(compiled_char, extra={"success": True})
            return

        # 9. 캐릭터 수정 (Update Character)
        elif path == "/api/update_character":
            seed_hash = body_data.get("seed_hash")
            char = self.char_repo.get_by_seed(seed_hash) if seed_hash else None
            if char:
                char.name = body_data.get("name", char.name)
                char.title = body_data.get("title", char.title)
                if "image_url" in body_data and body_data["image_url"]:
                    char.portrait_url = body_data["image_url"]
                
                # Traits 업데이트
                traits_in = body_data.get("traits", {})
                if traits_in:
                    char.traits.traits_list = [
                        {"category": k, "details": v}
                        for k, v in traits_in.items()
                    ]
                self.char_repo.save(char)
                self._send_state_response(char, extra={"success": True})
            else:
                self._send_json({"error": "Character not found"}, status=404)
            return

        # 10. 캐릭터 삭제 (Delete Character)
        elif path in ("/api/delete_character", "/api/characters/delete"):
            seed_hash = body_data.get("seed_hash")
            char_id = body_data.get("character_id")
            char = self.char_repo.get_by_seed(seed_hash) if seed_hash else self.char_repo.get_by_id(int(char_id))
            if char and char.id:
                self.char_repo.delete(char.id)
                remaining = self.char_repo.list_all()
                active = remaining[0] if remaining else None
                if active and active.id:
                    self.char_repo.set_active(active.id)
                    self._send_state_response(active, extra={"success": True})
                else:
                    self._send_json({"success": True, "state": None})
            else:
                self._send_json({"error": "Character not found"}, status=404)
            return

        # 11. LLM 설정 저장
        elif path == "/api/save_llm_config":
            provider = body_data.get("provider", "claude")
            anthropic_model = body_data.get("anthropic_model", "")
            gemini_model = body_data.get("gemini_model", "")
            if anthropic_model:
                self.llm_client.anthropic_model = anthropic_model
            if gemini_model:
                self.llm_client.gemini_model = gemini_model
            self.llm_client.primary_provider = provider
            self._send_json({"success": True, "provider": provider})
            return

        self.send_error(404, "Endpoint Not Found")

    # -------------------------------------------------------------
    # Helper Serialization & Response Methods
    # -------------------------------------------------------------
    def _char_to_view_dict(self, char: Character) -> Dict[str, Any]:
        """프론트엔드 전용 뷰 딕셔너리 변환"""
        traits_dict = {}
        for t in char.traits.traits_list:
            traits_dict[t.get("category", "특성")] = t.get("details", "")

        return {
            "id": char.id,
            "name": char.name,
            "title": char.title,
            "faction": char.traits.archetype_title.split("•")[-1].strip() if "•" in char.traits.archetype_title else "제국 진영",
            "seed_hash": char.seed_hash,
            "armor_type": char.traits.archetype_class,
            "pressure_stage": char.traits.stage_progression,
            "ego_durability": 100 - (char.traits.gauges.submission if hasattr(char.traits.gauges, "submission") else 0),
            "neural_taint": float(char.traits.somatic_metrics.taint.replace("%", "")) if hasattr(char.traits.somatic_metrics, "taint") else 7.1,
            "image_url": char.portrait_url or "",
            "traits": traits_dict,
            "trust": char.traits.gauges.trust,
            "erotic": char.traits.gauges.eroticism,
            "dominance": char.traits.gauges.shame,
            "taboo": char.traits.gauges.guilt,
            "vulnerability": char.traits.gauges.submission
        }

    def _send_state_response(self, char: Character, extra: Dict[str, Any] = None) -> None:
        """단일 진실 공급원 state 동기 응답"""
        history = self.turn_repo.get_history(char.id) if char.id else []
        last_turn = history[-1] if history else {}
        resp = {
            "success": True,
            "character": self._char_to_view_dict(char),
            "chat_history": [
                {
                    "step": h.get("turn_number", 1),
                    "user_action": h.get("user_action", ""),
                    "narrative_prose": h.get("narrative_response", ""),
                    "pressure_stage": char.traits.stage_progression
                }
                for h in history
            ],
            "step": len(history) + 1,
            "last_action": last_turn.get("user_action", ""),
            "last_narrative": last_turn.get("narrative_response", "차가운 공기 속에서 그녀가 당신을 응시하고 있습니다."),
            "active_tensors": ["04_cervical_and_choker", "05_clavicle", "14_apparel_tension"],
            "choices": [
                {"type": "DEVOTION_COMFORT", "text": "떨리는 어깨에 조용히 외투를 걸쳐주며 더 이상 홀로 짊어질 필요 없다고 위로한다."},
                {"type": "SUBJUGATION", "text": "치켜든 턱을 거세게 쥐어 올리며 가문의 위선과 오만한 긍지를 짓누른다."},
                {"type": "SUBMISSION_FAWN", "text": "황녀의 구두 앞에 정중히 한쪽 무릎을 꿇고 손등을 들어 올려 입을 맞춘다."},
                {"type": "SOMATIC_SYNC", "text": "경직된 목덜미와 쇄골 부근을 서늘한 손끝으로 쓸어내리며 체온 변화를 유도한다."},
                {"type": "SUSPENSION", "text": "차갑게 뒤돌아서서 침묵으로 일관하며 오만한 시선을 고립시킨다."}
            ]
        }
        if extra:
            resp.update(extra)
        self._send_json(resp)

    def _send_json(self, data: Any, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, file_path: Path, content_type: str) -> None:
        try:
            content = file_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception:
            self.send_error(500, "Internal Server Error")

    def _read_json_body(self) -> Dict[str, Any]:
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 0:
                raw = self.rfile.read(content_length).decode("utf-8")
                return json.loads(raw)
        except Exception:
            pass
        return {}

    def _guess_content_type(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        mapping = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
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
    print(f"  - Concurrency: ThreadedHTTPServer (Zero-Freeze AJAX & Toasts)")
    print(f"======================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()
        httpd.server_close()


if __name__ == "__main__":
    run_server()
