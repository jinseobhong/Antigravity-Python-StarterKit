# -*- coding: utf-8 -*-
"""
src/application/undo_manager.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
불변 스냅샷 기반 롤백(Undo) 스택 관리자 (UndoManager & TurnSnapshot)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from src.domain.character import Character


@dataclass(frozen=True)
class TurnSnapshot:
    """턴별 불변 상태 스냅샷 (Rollback Anchor)"""
    turn_number: int
    character_dict: Dict[str, Any]
    user_action: str
    narrative_prose: str
    delta_logs: Dict[str, Any]


class UndoManager:
    """롤백 스택 관리자"""

    def __init__(self):
        self._stack: List[TurnSnapshot] = []

    @property
    def can_undo(self) -> bool:
        """롤백 가능 여부 (최소 1개 이상의 스냅샷 존재 시)"""
        return len(self._stack) > 0

    @property
    def history_depth(self) -> int:
        """현재 스택 깊이"""
        return len(self._stack)

    def push_snapshot(
        self,
        turn_number: int,
        character: Character,
        user_action: str,
        narrative_prose: str,
        delta_logs: Optional[Dict[str, Any]] = None
    ) -> None:
        """현재 턴 스냅샷을 스택에 푸시"""
        snapshot = TurnSnapshot(
            turn_number=turn_number,
            character_dict=character.to_dict(),
            user_action=user_action,
            narrative_prose=narrative_prose,
            delta_logs=dict(delta_logs or {}),
        )
        self._stack.append(snapshot)

    def pop_snapshot(self) -> Optional[TurnSnapshot]:
        """직전 턴 스냅샷 팝 (스택에서 제거 후 반환)"""
        if not self.can_undo:
            return None
        return self._stack.pop()

    def restore_character(self, snapshot: TurnSnapshot) -> Character:
        """스냅샷으로부터 캐릭터 도메인 엔티티 100% 오차 없이 복원"""
        return Character.from_dict(snapshot.character_dict)
