# -*- coding: utf-8 -*-
"""
src/application/undo_manager.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Application Layer: 불변 턴 스냅샷 기반 Undo / Rollback 관리자
- 직전 턴의 상태 및 원장 데이터를 안전하게 롤백
"""

from __future__ import annotations
from typing import Optional, Dict, Any
from src.storage.repositories import TurnLedgerRepository, CharacterRepository
from src.models.somatic_ledger import SomaticLedger
from src.models.character_traits import PsychologicalGauges


class UndoManager:
    """불변 Undo / Rollback 매니저"""

    def __init__(self, turn_repo: TurnLedgerRepository, char_repo: CharacterRepository):
        self.turn_repo = turn_repo
        self.char_repo = char_repo

    def undo_last_turn(self, character_id: int) -> Optional[Dict[str, Any]]:
        """직전 턴을 삭제하고 캐릭터의 3-Tier 원장 및 심리 게이지를 그 이전 턴으로 롤백"""
        removed = self.turn_repo.remove_last_turn(character_id)
        if not removed:
            return None

        # 남은 히스토리 중 가장 최근 턴 조회
        history = self.turn_repo.get_history(character_id)
        char = self.char_repo.get_by_id(character_id)
        if char:
            if history:
                last_turn = history[-1]
                char.somatic_ledger = SomaticLedger.from_dict(last_turn["somatic_ledger"])
                char.traits.gauges = PsychologicalGauges.from_dict(last_turn["gauges"])
            else:
                # 턴 기록이 없으면 초기 상태 복원
                char.traits.gauges = PsychologicalGauges(trust=20, eroticism=0, shame=-30, guilt=15, submission=20)
            self.char_repo.save(char)

        return removed
