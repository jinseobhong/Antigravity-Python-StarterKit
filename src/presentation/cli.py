# -*- coding: utf-8 -*-
"""
src/presentation/cli.py
~~~~~~~~~~~~~~~~~~~~~~~
Dify 스타일의 2단계 인간 결재선(HITL Checkpoint 1 & 2)을 완비한 대화형 콘솔 CLI
"""

from __future__ import annotations
import sys
import os

from src.infrastructure.database.db_manager import DatabaseManager
from src.infrastructure.database.repositories import CharacterRepository, TurnLedgerRepository
from src.infrastructure.llm.client import MultiLLMClient
from src.application.classifier_service import ClassifierService
from src.application.gene_synthesis_service import GeneSynthesisService
from src.application.narrative_orchestrator import NarrativeOrchestrator


def run_cli():
    print("=" * 70)
    print("👑 [AbyssEmpire] LLM-Hybrid Somatic Narrative Simulator (HITL Console)")
    print("=" * 70)

    db = DatabaseManager()
    char_repo = CharacterRepository(db)
    turn_repo = TurnLedgerRepository(db)
    llm = MultiLLMClient()
    classifier = ClassifierService(llm)
    synthesis = GeneSynthesisService(char_repo, llm)

    # 1. 캐릭터 선택 or 신규 발현
    chars = char_repo.list_all()
    print("\n[RDB 캐릭터 로스터]:")
    for i, c in enumerate(chars, 1):
        print(f"  {i}. [{c.seed_hash}] {c.name} ({c.title} • {c.faction})")
    print(f"  {len(chars) + 1}. ✨ 새로운 캐릭터 제약선 역산 및 발현 (HITL 파이프라인)")

    choice = input("\n선택 번호를 입력하세요 (기본: 1): ").strip() or "1"
    selected_char = None

    if choice.isdigit() and 1 <= int(choice) <= len(chars):
        selected_char = chars[int(choice) - 1]
    else:
        # 신규 발현 파이프라인 (Dify Node 1 ➔ Checkpoint 1 ➔ Node 2 ➔ Checkpoint 2)
        user_intent = input("\n생성할 캐릭터의 성향/세계를 입력하세요 (예: 차가운 성격의 은발 제1황녀): ").strip()
        print("\n⏳ [1단계] 제약 조건(Hard Invariants) 역산 및 2대 서사 궤적 분석 중...")
        res = classifier.resolve_boundary_and_vectors(user_intent)

        print("\n" + "=" * 50)
        print("🛑 【HUMAN CHECKPOINT 1 : 서사 충돌 궤적 결재】")
        print("=" * 50)
        print(f"* 발급된 GENE SEED : {res['seed_hash']}")
        print(f"* 확정 불변 제약선 : {res['hard_invariants']['primary_boundary']}")
        print(f"* 자아 붕괴 트리거 : {res['hard_invariants']['ego_collapse_trigger']}")
        print(f"* 생체 취약 부위   : {res['hard_invariants']['somatic_achilles_heel']}")
        print("\n[선택 가능한 2대 서사 궤적]:")
        for v in res["resolution_vectors"]:
            print(f"  - [{v['vector_id']}] {v['vector_name']}")
            print(f"      세부 설명: {v['axis_description']}")

        v_choice = input("\n채택할 궤적을 선택하세요 (V1 / V2 / Q:취소, 기본 V1): ").strip().upper() or "V1"
        if v_choice == "Q":
            print("프로세스가 취소되었습니다.")
            return

        selected_v = next((v for v in res["resolution_vectors"] if v["vector_id"] == v_choice), res["resolution_vectors"][0])

        print("\n⏳ [2단계] 8-Tier Visual DNA & 70단계 유전자 마스터 헌법 합성 중...")
        selected_char = synthesis.synthesize_character(
            name=res["target_name"],
            title="고위 귀족",
            faction="독립 세력",
            hard_invariants_dict=res["hard_invariants"],
            selected_vector=selected_v,
            explicit_seed=res["seed_hash"]
        )
        print(f"✨ [{selected_char.name}] 유전자 각인 완료! (Danbooru: {selected_char.visual_dna.danbooru_prompt[:40]}...)")

    # 2. 롤플레이 세션 진입
    orchestrator = NarrativeOrchestrator(selected_char, char_repo, turn_repo, llm)
    print("\n" + "=" * 70)
    print(f"🎭 [{selected_char.name}]와의 1:1 서사 롤플레이가 시작되었습니다.")
    print(f"   [시각 앵커]: {selected_char.visual_dna.compile_literary_anchor()}")
    print("   (명령어: 'undo' 직전 턴 되돌리기, 'quit' 종료)")
    print("=" * 70)

    while True:
        try:
            user_act = input(f"\n[Turn {orchestrator.current_turn} Player Action] > ").strip()
            if not user_act:
                continue
            if user_act.lower() in ["quit", "exit", "q"]:
                print("세션을 종료합니다.")
                break
            if user_act.lower() == "undo":
                if orchestrator.rollback():
                    print("↺ 직전 턴 상태로 성공적으로 롤백되었습니다.")
                else:
                    print("⚠️ 되돌릴 턴이 없습니다.")
                continue

            result = orchestrator.execute_turn(user_act)
            print("\n" + "-" * 60)
            print(f"👑 [{selected_char.name} Response] ({result['pacing_level']})")
            print(f"   [운동 연쇄]: {result['active_kinematic_steps'][0]} ➔ {result['active_kinematic_steps'][1]}")
            print("-" * 60)
            print(result["prose"])
            print("-" * 60)
        except KeyboardInterrupt:
            print("\nCLI Closed.")
            break


if __name__ == "__main__":
    run_cli()
