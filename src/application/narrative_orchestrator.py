# -*- coding: utf-8 -*-
"""
src/application/narrative_orchestrator.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
턴 라이프사이클 관리, 도메인 생체 연산, 멀티 LLM 생성 및 Undo 스택 총괄 오케스트레이터
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple

from src.domain.character import Character
from src.domain.action_frame import ActionFrame
from src.infrastructure.database.repositories import CharacterRepository, TurnHistoryRepository
from src.infrastructure.llm.client import UniversalLLMClient
from src.infrastructure.llm.prompt_builder import PromptBuilder
from .action_parser_service import ActionParserService
from .undo_manager import UndoManager, TurnSnapshot


@dataclass
class TurnResult:
    """한 턴의 실행 결과 응답 객체"""
    turn_number: int
    user_action: str
    action_frame: ActionFrame
    narrative_prose: str
    somatic_events: List[str]
    character: Character


class NarrativeOrchestrator:
    """실시간 서사 롤플레이 오케스트레이터"""

    def __init__(
        self,
        character: Character,
        char_repo: CharacterRepository,
        turn_repo: TurnHistoryRepository,
        llm_client: Optional[UniversalLLMClient] = None,
    ):
        self.character = character
        self.char_repo = char_repo
        self.turn_repo = turn_repo
        self.llm_client = llm_client or UniversalLLMClient()
        self.parser = ActionParserService()
        self.undo_manager = UndoManager()
        self.current_turn = 1
        self.history: List[Dict[str, Any]] = []

    def execute_turn(self, raw_action: str) -> TurnResult:
        """
        1. 턴 스냅샷 저장 (Undo 보장)
        2. 사용자 행동 파싱 ➔ ActionFrame
        3. 도메인 17대 텐서 외력 및 Kinematic Chain 연산 (Pure Python)
        4. 자아 내구도 / 신경 오염도 인과율 갱신 (Pure Python)
        5. LLM 서사 집필 호출
        6. DB 원장 기록 및 영속화
        """
        # 1. 롤백을 위한 스냅샷 푸시
        self.undo_manager.push_snapshot(
            turn_number=self.current_turn,
            character=self.character,
            user_action=raw_action,
            narrative_prose="",
        )

        # 2. 자연어 파싱
        frame = self.parser.parse_input(raw_action)

        # 3. 17대 텐서 및 신체 운동 연쇄 전이 연산 (0토큰, 결정론적)
        somatic_events = self.character.tensors.apply_stimulus(
            primary_tensor=frame.primary_tensor,
            intensity=frame.intensity * 0.1
        )

        # 4. 생체 수치 갱신 (강도에 따른 자아 데미지 및 오염도 가산)
        ego_damage = frame.intensity * 2.5
        taint_gain = frame.intensity * 3.0
        self.character.apply_damage_and_taint(ego_damage=ego_damage, taint_gain=taint_gain)

        # 5. LLM 서사 생성
        sys_prompt, user_prompt = PromptBuilder.build_narrative_prompts(
            character=self.character,
            action_frame=frame,
            turn_number=self.current_turn,
            recent_chat_history=self.history
        )
        raw_prose = self.llm_client.generate(sys_prompt, user_prompt)
        if not raw_prose:
            # LLM API 미제공 또는 오프라인 환경을 위한 기본 폴백 서사
            raw_prose = f'{self.character.name}는 숨을 들이쉬며 당신의 행동을 응시했다.\n\n"무슨 생각을 하는 거지?"\n\n그녀의 등줄기에 차가운 긴장감이 스쳐 지나갔다.'

        # 6. DB 영속화
        char_id = self.char_repo.save(self.character)
        self.turn_repo.record_turn(
            character_id=char_id,
            turn_number=self.current_turn,
            user_action=raw_action,
            vector_type=frame.dominant_vector.name,
            narrative_prose=raw_prose,
            ego_durability=self.character.ego_durability,
            neural_taint=self.character.neural_taint,
            pressure_stage=self.character.pressure_stage.value,
        )

        result = TurnResult(
            turn_number=self.current_turn,
            user_action=raw_action,
            action_frame=frame,
            narrative_prose=raw_prose,
            somatic_events=somatic_events,
            character=self.character,
        )

        self.history.append({
            "turn": self.current_turn,
            "action": raw_action,
            "prose": raw_prose,
        })
        self.current_turn += 1
        return result

    def rollback(self) -> Optional[Character]:
        """직전 턴으로 완벽 롤백"""
        snapshot = self.undo_manager.pop_snapshot()
        if not snapshot:
            return None

        self.character = self.undo_manager.restore_character(snapshot)
        self.current_turn = snapshot.turn_number
        self.char_repo.save(self.character)
        if self.history:
            self.history.pop()
        return self.character
