# -*- coding: utf-8 -*-
"""
src/presentation/web/server.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Clean 4-Tier 전용 로컬 웹 스튜디오 서버 (Python 표준 http.server 기반, 의존성 제로)
- TailwindCSS & Glassmorphism 실시간 인터랙티브 대시보드
- 4대 대표 아키타입(릴리스, 에이라, 세라피나, 실비아) 즉시 롤플레이
- 17대 생체 텐서 실시간 게이지 및 불변 Undo 롤백 완비
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


# 전역 인스턴스
STUDIO_APP = WebStudioApp()


HTML_PAGE = r"""<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>👑 AbyssEmpire &bull; Somatic Narrative Web Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        body { font-family: 'Pretendard', sans-serif; background: #07080d; color: #f1f5f9; }
        .glass-panel { background: rgba(15, 17, 26, 0.88); backdrop-filter: blur(16px); border: 1px solid #1e2235; }
        .neon-glow:hover { box-shadow: 0 0 20px rgba(168, 85, 247, 0.35); }
        .prose-box p { margin-bottom: 0.85rem; line-height: 1.8; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #07080d; }
        ::-webkit-scrollbar-thumb { background: #1e2235; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #a855f7; }
    </style>
</head>
<body class="h-screen flex flex-col justify-between overflow-hidden">

    <!-- Header Navbar -->
    <header class="h-16 border-b border-gray-800/80 px-6 flex items-center justify-between glass-panel z-20">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 via-pink-500 to-amber-400 flex items-center justify-center shadow-lg">
                <i class="fa-solid fa-crown text-white"></i>
            </div>
            <div>
                <h1 class="text-lg font-black tracking-wide bg-gradient-to-r from-purple-400 via-pink-300 to-amber-300 bg-clip-text text-transparent">
                    AbyssEmpire Web Studio
                </h1>
                <p class="text-[11px] text-gray-400 font-medium">Clean 4-Tier Somatic Engine &bull; Gemini / Claude Cascade</p>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="flex items-center gap-2">
            <button onclick="switchTab('play')" id="tabPlay" class="px-4 py-2 rounded-xl text-xs font-bold bg-purple-600 text-white shadow transition flex items-center gap-1.5">
                <i class="fa-solid fa-masks-theater text-xs"></i> Play Room
            </button>
            <button onclick="switchTab('roster')" id="tabRoster" class="px-4 py-2 rounded-xl text-xs font-bold bg-gray-800/80 text-gray-300 hover:text-white hover:bg-gray-700 transition flex items-center gap-1.5">
                <i class="fa-solid fa-users text-xs"></i> 캐릭터 로스터
            </button>
            <button onclick="openPromptModal()" class="px-3 py-2 rounded-xl text-xs font-bold bg-gray-900 border border-purple-800/50 text-purple-300 hover:bg-purple-950/80 transition flex items-center gap-1.5">
                <i class="fa-solid fa-file-code text-xs"></i> 마스터 프롬프트
            </button>
        </div>
    </header>

    <!-- Main Container -->
    <main class="flex-1 flex overflow-hidden p-4 gap-4 max-w-7xl mx-auto w-full">

        <!-- Left: Active Character Card & Somatic Gauges (320px) -->
        <aside class="w-80 glass-panel rounded-2xl p-4 flex flex-col justify-between shrink-0 overflow-y-auto space-y-4">
            <div>
                <div class="flex items-center justify-between mb-3">
                    <span class="text-[11px] font-extrabold text-purple-400 uppercase tracking-wider flex items-center gap-1">
                        <i class="fa-solid fa-anchor"></i> Active Persona
                    </span>
                    <span id="charSeed" class="text-[10px] font-mono text-amber-400 bg-amber-950/40 px-2 py-0.5 rounded border border-amber-500/30">#SEED</span>
                </div>

                <!-- Persona Banner -->
                <div class="p-4 rounded-xl bg-gradient-to-br from-purple-950/50 to-pink-950/20 border border-purple-800/40 mb-3 text-center">
                    <div class="w-14 h-14 mx-auto rounded-2xl bg-gradient-to-tr from-purple-600 to-pink-500 flex items-center justify-center text-white text-xl font-black shadow-lg mb-2" id="charAvatar">
                        릴
                    </div>
                    <h2 class="text-base font-black text-white" id="charName">릴리스</h2>
                    <p class="text-xs text-purple-300" id="charTitle">제1황녀 &bull; 제국 황실</p>
                    <div class="mt-2 inline-block px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-purple-900/60 text-purple-200 border border-purple-500/40" id="charArmor">
                        Rigid (완벽주의 척추)
                    </div>
                </div>

                <!-- 17대 생체 텐서 & 압력 궤적 -->
                <div class="space-y-2.5">
                    <div class="flex items-center justify-between text-xs">
                        <span class="text-gray-400 font-bold">압력 궤적 단계</span>
                        <span id="pressureStage" class="text-pink-400 font-extrabold">STAGE 1: 정렬 방어</span>
                    </div>
                    <div class="w-full bg-gray-900 rounded-full h-2 overflow-hidden border border-gray-800">
                        <div id="egoBar" class="bg-gradient-to-r from-emerald-500 to-purple-500 h-2 rounded-full transition-all duration-300" style="width: 100%"></div>
                    </div>

                    <div class="pt-2 border-t border-gray-800">
                        <span class="text-[11px] font-extrabold text-gray-400 uppercase">⚡ 운동 연쇄 (Kinematic Chain)</span>
                        <p id="chainEvent" class="text-xs text-amber-300 mt-1 font-medium bg-amber-950/30 p-2 rounded-lg border border-amber-800/30">
                            신체 운동 연쇄 안정
                        </p>
                    </div>

                    <!-- 단부루 프롬프트 뷰어 버튼 -->
                    <button onclick="openDanbooruModal()" class="w-full mt-2 py-2 bg-pink-950/40 hover:bg-pink-900/60 border border-pink-700/40 text-pink-300 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 shadow">
                        <i class="fa-solid fa-wand-magic-sparkles text-xs"></i> 단부루 6-Slot 태그 생성
                    </button>
                </div>
            </div>

            <div class="pt-3 border-t border-gray-800/80 flex gap-2">
                <button onclick="triggerUndo()" class="flex-1 py-2 bg-gray-800 hover:bg-gray-700 text-gray-200 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1">
                    <i class="fa-solid fa-rotate-left text-xs"></i> 턴 되돌리기
                </button>
                <button onclick="triggerReset()" class="px-3 py-2 bg-red-950/40 hover:bg-red-900/60 border border-red-800/50 text-red-300 rounded-xl text-xs font-bold transition flex items-center gap-1">
                    <i class="fa-solid fa-trash text-xs"></i> 리셋
                </button>
            </div>
        </aside>

        <!-- Right View 1: Play Room (Chat Session) -->
        <section id="viewPlay" class="flex-1 glass-panel rounded-2xl p-5 flex flex-col justify-between overflow-hidden">
            
            <!-- Chat Log Box -->
            <div id="chatBox" class="flex-1 overflow-y-auto space-y-4 pr-2 mb-4">
                <div class="p-4 rounded-2xl bg-purple-950/30 border border-purple-900/40 text-sm leading-relaxed prose-box">
                    <p class="font-bold text-purple-300 mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-sparkles text-amber-400"></i> 세션이 시작되었습니다.
                    </p>
                    <p class="text-gray-300" id="introProse">
                        서늘한 대리석 기둥 사이로 차가운 바람이 스며듭니다. 상대방을 마주하고 첫 행동을 취하십시오.
                    </p>
                </div>
            </div>

            <!-- Tactical Choices Chips -->
            <div class="space-y-2 mb-3">
                <span class="text-[11px] font-bold text-gray-400 uppercase">🎯 전술 선택지 (Tactical Actions)</span>
                <div id="choicesBox" class="flex flex-wrap gap-2">
                    <button onclick="sendQuickChoice('DEVOTION_COMFORT', '가까이 다가가 차가운 뺨을 부드럽게 감싸 쥔다.')" class="px-3 py-1.5 bg-purple-950/60 hover:bg-purple-900 border border-purple-700/50 text-purple-200 rounded-xl text-xs font-bold transition">
                        💖 [헌신/위로] 뺨 감싸기
                    </button>
                    <button onclick="sendQuickChoice('SUBJUGATION', '차가운 시선으로 턱을 치켜들며 복종을 요구한다.')" class="px-3 py-1.5 bg-pink-950/60 hover:bg-pink-900 border border-pink-700/50 text-pink-200 rounded-xl text-xs font-bold transition">
                        ⚡ [정복/압박] 턱 치켜들기
                    </button>
                    <button onclick="sendQuickChoice('SOMATIC_SYNC', '나란히 앉아 서로의 은밀한 체온과 호흡을 맞춘다.')" class="px-3 py-1.5 bg-cyan-950/60 hover:bg-cyan-900 border border-cyan-700/50 text-cyan-200 rounded-xl text-xs font-bold transition">
                        🌊 [체온/동조] 호흡 맞추기
                    </button>
                </div>
            </div>

            <!-- Input Bar -->
            <form onsubmit="handleSend(event)" class="flex gap-2">
                <input type="text" id="actionInput" placeholder="행동이나 대사를 자연어로 입력하세요 (예: 그녀의 손끝을 잡으며 부드럽게 속삭였다.)" class="flex-1 bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-purple-500 transition">
                <button type="submit" class="px-5 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white rounded-xl text-xs font-extrabold shadow transition flex items-center gap-1.5 shrink-0">
                    <i class="fa-solid fa-paper-plane text-xs"></i> 턴 실행
                </button>
            </form>
        </section>

        <!-- Right View 2: Character Roster & Creation -->
        <section id="viewRoster" class="hidden flex-1 glass-panel rounded-2xl p-5 flex flex-col justify-between overflow-y-auto space-y-4">
            <div>
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h3 class="text-base font-black text-white">🎭 캐릭터 보관소 (Character Roster)</h3>
                        <p class="text-xs text-gray-400">플레이할 인격을 선택하거나 신규 캐릭터를 생성합니다.</p>
                    </div>
                    <button onclick="openCreateModal()" class="px-3.5 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl text-xs font-bold shadow flex items-center gap-1.5">
                        <i class="fa-solid fa-plus text-xs"></i> 신규 캐릭터 생성
                    </button>
                </div>

                <div id="rosterGrid" class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <!-- Dynamic Roster Cards -->
                </div>
            </div>
        </section>

    </main>

    <!-- Master Prompt Modal -->
    <div id="promptModal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="glass-panel rounded-2xl p-6 max-w-2xl w-full max-h-[85vh] flex flex-col justify-between">
            <div class="flex items-center justify-between pb-3 border-b border-gray-800 mb-3">
                <h4 class="text-sm font-black text-purple-300 flex items-center gap-2">
                    <i class="fa-solid fa-file-code"></i> 마스터 시스템 프롬프트 (25,000자급)
                </h4>
                <button onclick="closePromptModal()" class="text-gray-400 hover:text-white"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <textarea id="promptText" readonly class="flex-1 w-full bg-gray-950 p-4 rounded-xl text-xs font-mono text-gray-300 border border-gray-800 resize-none h-96"></textarea>
            <div class="mt-4 flex justify-end gap-2">
                <button onclick="copyMasterPrompt()" class="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-xl text-xs font-bold transition">
                    프롬프트 복사
                </button>
                <button onclick="closePromptModal()" class="px-4 py-2 bg-gray-800 text-gray-300 rounded-xl text-xs font-bold">
                    닫기
                </button>
            </div>
        </div>
    </div>

    <!-- Danbooru Tags Modal -->
    <div id="danbooruModal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="glass-panel rounded-2xl p-6 max-w-xl w-full flex flex-col justify-between">
            <div class="flex items-center justify-between pb-3 border-b border-gray-800 mb-3">
                <h4 class="text-sm font-black text-pink-300 flex items-center gap-2">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> Illustrious-XL 6-Slot 단부루 태그
                </h4>
                <button onclick="closeDanbooruModal()" class="text-gray-400 hover:text-white"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="space-y-3">
                <div>
                    <label class="text-[11px] font-bold text-gray-400 uppercase">Positive Prompt</label>
                    <textarea id="danbooruPos" readonly class="w-full bg-gray-950 p-3 rounded-xl text-xs font-mono text-pink-300 border border-gray-800 resize-none h-24 mt-1"></textarea>
                </div>
                <div>
                    <label class="text-[11px] font-bold text-gray-400 uppercase">Negative Prompt</label>
                    <textarea id="danbooruNeg" readonly class="w-full bg-gray-950 p-3 rounded-xl text-xs font-mono text-gray-400 border border-gray-800 resize-none h-20 mt-1"></textarea>
                </div>
            </div>
            <div class="mt-4 flex justify-end">
                <button onclick="closeDanbooruModal()" class="px-4 py-2 bg-gray-800 text-gray-300 rounded-xl text-xs font-bold">
                    닫기
                </button>
            </div>
        </div>
    </div>

    <script>
        let currentCharacter = null;

        async function fetchState() {
            try {
                const res = await fetch('/api/state');
                const data = await res.json();
                renderState(data);
            } catch (err) {
                console.error('fetchState error:', err);
            }
        }

        async function fetchRoster() {
            try {
                const res = await fetch('/api/characters');
                const list = await res.json();
                renderRoster(list);
            } catch (err) {
                console.error('fetchRoster error:', err);
            }
        }

        function renderState(data) {
            if (!data || !data.character) return;
            const c = data.character;
            currentCharacter = c;

            document.getElementById('charSeed').innerText = c.seed_hash || '#SEED';
            document.getElementById('charAvatar').innerText = c.name ? c.name.charAt(0) : '👑';
            document.getElementById('charName').innerText = c.name;
            document.getElementById('charTitle').innerText = `${c.title} • ${c.faction}`;
            document.getElementById('charArmor').innerText = c.armor_type;

            const ego = c.ego_durability !== undefined ? c.ego_durability : 100;
            document.getElementById('egoBar').style.width = `${Math.max(0, Math.min(100, ego))}%`;

            document.getElementById('pressureStage').innerText = `STAGE: ${c.pressure_stage}`;
            document.getElementById('chainEvent').innerText = data.recent_chain || '신체 운동 연쇄 안정';

            // 채팅 이력 렌더링
            const box = document.getElementById('chatBox');
            if (data.chat_history && data.chat_history.length > 0) {
                box.innerHTML = data.chat_history.map(msg => {
                    if (msg.role === 'user') {
                        return `
                            <div class="flex justify-end mb-3">
                                <div class="bg-purple-900/60 border border-purple-700/40 text-purple-100 rounded-2xl rounded-tr-none px-4 py-2.5 max-w-xl text-xs shadow">
                                    ${msg.content}
                                </div>
                            </div>
                        `;
                    } else {
                        return `
                            <div class="flex justify-start mb-3">
                                <div class="bg-gray-900/90 border border-gray-800 text-gray-200 rounded-2xl rounded-tl-none px-4 py-3 max-w-xl text-xs shadow prose-box leading-relaxed">
                                    <div class="font-bold text-pink-400 mb-1 flex items-center gap-1.5">
                                        <i class="fa-solid fa-crown text-[10px]"></i> ${c.name}
                                    </div>
                                    ${marked.parse(msg.content)}
                                </div>
                            </div>
                        `;
                    }
                }).join('');
                box.scrollTop = box.scrollHeight;
            }
        }

        function renderRoster(list) {
            const grid = document.getElementById('rosterGrid');
            if (!grid || !list) return;
            grid.innerHTML = list.map(item => `
                <div class="p-4 rounded-xl bg-gray-900/70 border border-gray-800 hover:border-purple-600/50 transition flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-xl bg-purple-600/30 border border-purple-500/40 flex items-center justify-center text-purple-300 font-bold">
                            ${item.name.charAt(0)}
                        </div>
                        <div>
                            <h4 class="text-xs font-black text-white">${item.name}</h4>
                            <p class="text-[11px] text-gray-400">${item.title} • ${item.armor_type}</p>
                        </div>
                    </div>
                    <button onclick="selectCharacter('${item.seed_hash}')" class="px-3 py-1.5 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-bold transition">
                        선택
                    </button>
                </div>
            `).join('');
        }

        async function selectCharacter(seedHash) {
            try {
                const res = await fetch('/api/select_character', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({seed_hash: seedHash})
                });
                const data = await res.json();
                renderState(data);
                switchTab('play');
            } catch (err) {
                console.error('selectCharacter error:', err);
            }
        }

        async function handleSend(e) {
            e.preventDefault();
            const input = document.getElementById('actionInput');
            const text = input.value.trim();
            if (!text) return;
            input.value = '';

            const res = await fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action_text: text, vector_type: 'SUBJUGATION'})
            });
            const data = await res.json();
            renderState(data);
        }

        async function sendQuickChoice(vectorType, text) {
            const res = await fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action_text: text, vector_type: vectorType})
            });
            const data = await res.json();
            renderState(data);
        }

        async function triggerUndo() {
            const res = await fetch('/api/undo', {method: 'POST'});
            const data = await res.json();
            renderState(data);
        }

        async function triggerReset() {
            if (!confirm('세션을 1턴으로 초기화하시겠습니까?')) return;
            const res = await fetch('/api/reset', {method: 'POST'});
            const data = await res.json();
            renderState(data);
        }

        async function openPromptModal() {
            const res = await fetch('/api/export_prompt');
            const data = await res.json();
            document.getElementById('promptText').value = data.prompt || '';
            document.getElementById('promptModal').classList.remove('hidden');
        }

        function closePromptModal() {
            document.getElementById('promptModal').classList.add('hidden');
        }

        function copyMasterPrompt() {
            const txt = document.getElementById('promptText');
            txt.select();
            document.execCommand('copy');
            alert('마스터 프롬프트가 클립보드에 복사되었습니다.');
        }

        async function openDanbooruModal() {
            const res = await fetch('/api/generate_danbooru', {method: 'POST'});
            const data = await res.json();
            document.getElementById('danbooruPos').value = data.positive || '';
            document.getElementById('danbooruNeg').value = data.negative || '';
            document.getElementById('danbooruModal').classList.remove('hidden');
        }

        function closeDanbooruModal() {
            document.getElementById('danbooruModal').classList.add('hidden');
        }

        function switchTab(tab) {
            if (tab === 'play') {
                document.getElementById('viewPlay').classList.remove('hidden');
                document.getElementById('viewRoster').classList.add('hidden');
                document.getElementById('tabPlay').className = 'px-4 py-2 rounded-xl text-xs font-bold bg-purple-600 text-white shadow transition flex items-center gap-1.5';
                document.getElementById('tabRoster').className = 'px-4 py-2 rounded-xl text-xs font-bold bg-gray-800/80 text-gray-300 hover:text-white hover:bg-gray-700 transition flex items-center gap-1.5';
            } else {
                document.getElementById('viewPlay').classList.add('hidden');
                document.getElementById('viewRoster').classList.remove('hidden');
                document.getElementById('tabPlay').className = 'px-4 py-2 rounded-xl text-xs font-bold bg-gray-800/80 text-gray-300 hover:text-white hover:bg-gray-700 transition flex items-center gap-1.5';
                document.getElementById('tabRoster').className = 'px-4 py-2 rounded-xl text-xs font-bold bg-purple-600 text-white shadow transition flex items-center gap-1.5';
                fetchRoster();
            }
        }

        // 초기 구동
        fetchState();
    </script>
</body>
</html>
"""


class WebStudioHandler(BaseHTTPRequestHandler):
    """Clean 4-Tier 웹 스튜디오 HTTP 요청 핸들러"""

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self._send_html(HTML_PAGE)
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
            char = STUDIO_APP.select_character(seed)
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
