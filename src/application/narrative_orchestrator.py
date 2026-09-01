# -*- coding: utf-8 -*-
"""
src/application/narrative_orchestrator.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[Dify Node 3: RECURSIVE SOMATIC NARRATIVE ENGINE]
- 실시간 1:1 서사 롤플레이 턴 오케스트레이션
- 7단계 신체 운동 연쇄 파동 전이 & 2~3 스포트라이트 점등
- 동적 완급 조절 (Level 1~3 Pacing)
- 3계층 신경·메모리 원장 (Layer 1, 2, 3) 갱신 및 DB 동기화
"""

from __future__ import annotations
import copy
from typing import Dict, Any, List, Optional

from src.domain.character import Character
from src.domain.spatial_pressure import SpatialLayer
from src.infrastructure.llm.client import MultiLLMClient
from src.infrastructure.llm.prompt_synthesizer import PromptSynthesizer
from src.infrastructure.database.repositories import CharacterRepository, TurnLedgerRepository
from src.application.undo_manager import UndoManager


class NarrativeOrchestrator:
    """하이브리드 서사 롤플레이 총괄 오케스트레이터"""

    def __init__(
        self,
        character: Character,
        char_repo: CharacterRepository,
        turn_repo: TurnLedgerRepository,
        llm_client: MultiLLMClient
    ):
        self.character = character
        self.char_repo = char_repo
        self.turn_repo = turn_repo
        self.llm = llm_client
        self.undo_manager = UndoManager()
        self.current_turn = 1
        self.history: List[Dict[str, str]] = []

    def execute_turn(self, raw_action: str) -> Dict[str, Any]:
        """플레이어 행동에 따라 1턴 서사 진행 (비결정론적 LLM 추론 & 3-Tier 원장 동기화)"""
        # 1. 롤백을 위한 스냅샷 푸시
        last_action_text = self.history[-1]["action"] if self.history else ""
        last_prose_text = self.history[-1]["prose"] if self.history else ""
        self.undo_manager.push(self.current_turn, self.character, last_action_text, last_prose_text)

        # 2. 신체 운동 연쇄 파동 전이 (Kinematic Chain 2~3 스포트라이트)
        active_steps = self.character.kinematic_chain.advance_wave()

        # 3. 완급 조절 레벨 결정
        if self.current_turn <= 2:
            pacing_level = "Level 1 (경량 2~4문단)"
        elif self.current_turn <= 6:
            pacing_level = "Level 2 (서사 고조 5~8문단)"
            if self.character.spatial_pressure.current_layer == SpatialLayer.LAYER_0_PUBLIC:
                self.character.spatial_pressure.transition_to(SpatialLayer.LAYER_1_THRESHOLD)
        else:
            pacing_level = "Level 3 (대하 클라이맥스 10~15문단)"
            self.character.spatial_pressure.transition_to(SpatialLayer.LAYER_2_INTIMATE)

        # 4. LLM 프롬프트 조립 & 서사 생성
        system_instruction = PromptSynthesizer.build_master_system_instruction(self.character)
        chat_hist = []
        for h in self.history:
            chat_hist.append({"role": "user", "content": h["action"]})
            chat_hist.append({"role": "assistant", "content": h["prose"]})

        user_prompt = PromptSynthesizer.build_turn_user_prompt(
            self.character,
            self.current_turn,
            raw_action,
            chat_hist
        )

        generated_prose = self.llm.generate_text(system_instruction, user_prompt, temperature=0.85)

        # 5. 3계층 원장 동적 갱신
        self._update_somatic_ledger(raw_action, active_steps)

        # 6. 이력 및 DB 기록
        self.history.append({
            "action": raw_action,
            "prose": generated_prose
        })

        self.turn_repo.record_turn(
            seed_hash=self.character.seed_hash,
            turn_num=self.current_turn,
            action=raw_action,
            prose=generated_prose,
            ledger_snap=self.character.somatic_ledger.to_dict()
        )
        self.char_repo.save(self.character)
        self.current_turn += 1

        return {
            "turn": self.current_turn - 1,
            "action": raw_action,
            "prose": generated_prose,
            "pacing_level": pacing_level,
            "active_kinematic_steps": active_steps,
            "ledger": self.character.somatic_ledger.to_dict()
        }

    def rollback(self) -> bool:
        """이전 턴 상태로 불변 롤백 (Undo)"""
        snap = self.undo_manager.pop()
        if not snap:
            return False

        self.current_turn = snap.turn_number
        self.character = snap.character_snapshot
        if self.history:
            self.history.pop()

        self.char_repo.save(self.character)
        return True

    def _update_somatic_ledger(self, action: str, active_steps: List[str]) -> None:
        """행동에 따라 3계층 원장 상태 갱신"""
        ledger = self.character.somatic_ledger
        # Layer 1: 반사계 갱신
        ledger.layer_1_reflex["spine_rigidity"] = f"{active_steps[0]}에 따른 긴장성 경직"
        # Layer 2: 단기버퍼 갱신
        ledger.layer_2_short_term["sensory_hysteresis"] = f"{active_steps[1]}에 머문 잔향과 체온 교환"
        # Layer 3: 장기기억 갱신
        inversion = min(100, (self.current_turn * 12))
        ledger.layer_3_long_term["relationship_inversion_rate"] = f"{inversion}% (심리적 틈새와 의존 심화)"
