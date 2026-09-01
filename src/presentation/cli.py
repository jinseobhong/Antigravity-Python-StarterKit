# -*- coding: utf-8 -*-
"""
src/presentation/cli.py
~~~~~~~~~~~~~~~~~~~~~~~
AbyssEngine 터미널 대화형 인터랙티브 롤플레이 CLI 런처
"""

from __future__ import annotations
import sys
from typing import Optional

from src.domain.character import Character, LowenArmor
from src.infrastructure.database.db_manager import DatabaseManager
from src.infrastructure.database.repositories import CharacterRepository, TurnHistoryRepository
from src.application.narrative_orchestrator import NarrativeOrchestrator
from .prose_sanitizer import ProseSanitizer


def run_cli_session():
    """터미널 기반 인터랙티브 서사 롤플레이 세션 시작"""
    print("=" * 70)
    print("  [AbyssEngine] 인터랙티브 서사 시뮬레이터 (CLI Edition)")
    print("=" * 70)

    db_manager = DatabaseManager()
    char_repo = CharacterRepository(db_manager)
    turn_repo = TurnHistoryRepository(db_manager)

    # 기본 캐릭터 생성/로드
    char = Character(
        name="엘레나",
        title="제국 성기사단장",
        faction="신성 제국",
        armor_type=LowenArmor.RIGID,
        traits={"결핍": "완벽주의에 대한 강박", "트라우마": "원정 실패"},
    )
    char_repo.save(char)

    orchestrator = NarrativeOrchestrator(
        character=char,
        char_repo=char_repo,
        turn_repo=turn_repo,
    )

    print(f"\n[대상 캐릭터]: {char.name} ({char.title})")
    print(f"[로웬 갑주]: {char.armor_type.value}")
    print(f"[현재 상태]: 자아 내구도 {char.ego_durability:.1f}% | 신경 오염도 {char.neural_taint:.1f}%\n")
    print("명령어: 'undo' (직전 턴 되돌리기), 'exit' (종료)\n" + "-" * 70)

    while True:
        try:
            user_input = input("\n[Player] > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("\n[세션을 종료합니다.]")
                break
            if user_input.lower() == "undo":
                restored = orchestrator.rollback()
                if restored:
                    print(f"\n[UNDO 롤백 완료] {restored.name}의 상태가 턴 {orchestrator.current_turn}으로 복원되었습니다.")
                    print(f"자아 내구도: {restored.ego_durability:.1f}% | 신경 오염도: {restored.neural_taint:.1f}%")
                else:
                    print("\n[알림] 더 이상 되돌릴 이전 턴이 없습니다.")
                continue

            result = orchestrator.execute_turn(user_input)
            clean_prose = ProseSanitizer.sanitize(result.narrative_prose)

            print(f"\n[Turn {result.turn_number} 서사]")
            print(clean_prose)
            print("\n" + "." * 70)
            print(f"⚡ [생체 역학 연산]: {', '.join(result.somatic_events)}")
            print(f"📊 [수치 갱신]: 자아 내구도 {result.character.ego_durability:.1f}% | 신경 오염도 {result.character.neural_taint:.1f}% | {result.character.pressure_stage.value}")
            print("." * 70)

        except (KeyboardInterrupt, EOFError):
            print("\n[세션을 종료합니다.]")
            break


if __name__ == "__main__":
    run_cli_session()
