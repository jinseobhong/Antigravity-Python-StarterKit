# -*- coding: utf-8 -*-
"""
src/application/undo_manager.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TurnSnapshot 기반 불변 롤백 스택 관리자 (Undo Manager)
"""

from __future__ import annotations
import copy
from dataclasses import dataclass
from typing import List, Optional
from src.domain.character import Character


@dataclass
class TurnSnapshot:
    """턴 상태 불변 스냅샷"""
    turn_number: int
    character_snapshot: Character
    last_action: str
    last_prose: str


class UndoManager:
    """단일 세션 롤백 스택 관리자"""

    def __init__(self):
        self._stack: List[TurnSnapshot] = []

    def push(self, turn_number: int, character: Character, action: str, prose: str) -> None:
        snap = TurnSnapshot(
            turn_number=turn_number,
            character_snapshot=copy.deepcopy(character),
            last_action=action,
            last_prose=prose
        )
        self._stack.append(snap)

    def pop(self) -> Optional[TurnSnapshot]:
        if not self._stack:
            return None
        return self._stack.pop()

    def clear(self) -> None:
        self._stack.clear()

    @property
    def depth(self) -> int:
        return len(self._stack)
