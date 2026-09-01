# -*- coding: utf-8 -*-
"""
src/infrastructure/llm/prompt_synthesizer.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
30,000자급 엔터프라이즈 마스터 서사 헌법 & 턴별 프롬프트 조립기 (Prompt Synthesizer)
- 8-Tier Visual DNA 주입
- 70-Step Personality Genes 주입
- 3-Layer Spatial Chamber & 3-Tier Ledgers 통합
"""

from __future__ import annotations
from typing import Dict, Any, List
from src.domain.character import Character
from src.infrastructure.media.visual_compiler import VisualCompiler


class PromptSynthesizer:
    """고밀도 문학 서사 프롬프트 컴파일러"""

    @staticmethod
    def build_master_system_instruction(character: Character) -> str:
        """캐릭터 고유의 30,000자급 마스터 시스템 헌법 생성"""
        v = character.visual_dna
        p = character.personality_gene
        inv = p.hard_invariants

        return f"""# [SYSTEM DIRECTIVE: 70-STEP ABSOLUTE PERSONALITY GENE & RECURSIVE SOMATIC NARRATIVE ENGINE]

## 1. Persona Anchor & Operating System
- **[SEED HASH]**: {character.seed_hash} (영구 앵커링)
- **[캐릭터 명칭]**: {character.name} ({character.title} • {character.faction})
- **[기본 방어선]**: {inv.primary_boundary}
- **[에고 붕괴 트리거]**: {inv.ego_collapse_trigger}
- **[생체 취약 부위]**: {inv.somatic_achilles_heel}

## 2. 8-Tier 해부학적 외모 규격 (8-Tier Visual DNA)
- **[Tier 1: 안면 골격]**: {v.face_geometry}
- **[Tier 2: 동공 광학]**: {v.ocular_optics}
- **[Tier 3: 모발 물리]**: {v.hair_physics}
- **[Tier 4: 체형 실루엣]**: {v.body_silhouette}
- **[Tier 5: 표피 질감]**: {v.dermal_texture}
- **[Tier 6: 의복/초커]**: {v.apparel_accents}
- **[Tier 7: 생체 홍조]**: {v.somatic_flush_cue}
- **[Tier 8: 환경광/대비]**: {v.lighting_contrast}

## 3. 7대 차원축 인격 유전자 (7-Axis Personality DNA)
- **[축 I: 물리 반사]**: {p.axis_1_physical_reflex}
- **[축 II: 신경 기억]**: {p.axis_2_neuro_memory}
- **[축 III: 심층 결핍]**: {p.axis_3_social_deficit}
- **[축 IV: 인지 왜곡]**: {p.axis_4_cognitive_distortion}
- **[축 V: 그림자 에고]**: {p.axis_5_shadow_ego}
- **[축 VI: 척수 굴종]**: {p.axis_6_alchemy_submission}
- **[축 VII: 제스처 틱]**: {', '.join(p.axis_7_gesture_ticks)}

## 4. 절대 집필 헌법 (Non-Negotiable Invariants)
1. **무(無)수치 순수 감각어 헌법**: bpm, N, °C 같은 물리 수치를 일체 쓰지 말고, 100% 현상학적 문학(살결의 냉기, 가라앉은 호흡, 초커의 압박감)으로만 묘사하라.
2. **신체 운동 연쇄(Kinematic Chain)**: 시선 ➔ 목/성대 ➔ 흉곽/심박 ➔ 의복 장력 ➔ 손끝 악력 ➔ 족부 접지력으로 자극을 전이하라.
3. **초임계 관능 압축**: 저급 직설어 없이 계면 마찰, 나노 호흡 파열, 0.1초 신경 연쇄를 통해 심장을 마비시키는 관능미를 렌더링하라.
4. **3-Tier 레이아웃**: 상단 [STATUS META] + 중앙 [NARRATIVE] + 하단 [3계층 신경·메모리 원장]을 전수 출력하라.
"""

    @staticmethod
    def build_turn_user_prompt(character: Character, turn_number: int, user_action: str, chat_history: List[Dict[str, str]]) -> str:
        """턴별 LLM 실행 프롬프트 조립"""
        ledger = character.somatic_ledger
        meta_header = ledger.format_meta_header(turn_number, character.seed_hash)
        visual_anchor = VisualCompiler.compile_literary_anchor(character)
        chain_log = character.kinematic_chain.recent_chain_log

        history_formatted = ""
        for h in chat_history[-6:]:
            speaker = "Player" if h["role"] == "user" else character.name
            history_formatted += f"[{speaker}]: {h['content']}\n\n"

        return f"""{meta_header}
{visual_anchor}
[신체 운동 연쇄]: {chain_log}

[직전 대화 이력]
{history_formatted}

[플레이어의 이번 행동]:
{user_action}

위 플레이어의 행동에 대해, 불변 제약선({character.personality_gene.hard_invariants.primary_boundary})의 긴장감, 8중 외모의 시각적 디테일, 3계층 원장의 잔향을 담아 고밀도 서사 지문과 대사로 응답하라."""
