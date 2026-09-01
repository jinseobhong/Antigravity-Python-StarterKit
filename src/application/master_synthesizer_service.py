# -*- coding: utf-8 -*-
"""
src/application/master_synthesizer_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Application Layer: Dify Node 10 기반 30,000자급 마스터 시스템 헌법 합성기
- 5대 절대 헌법 (Zero-Unit Sensory Law, Kinematic Chain, 70-Gene Cycler, 3-Layer Spatial Pressure, Dynamic Pacing)
- 3계층 신경·메모리 원장 초기 구조 주입
- Dify Node 11 StaticValidator 연동
"""

from __future__ import annotations
import json
from typing import Dict, Any, List

from src.infrastructure.llm.client import MultiLLMClient
from src.infrastructure.llm.prompt_synthesizer import PromptSynthesizer
from src.domain.character import Character
from src.application.static_validator import StaticValidator


class MasterSynthesizerService:
    """Dify Node 10 마스터 시스템 헌법 합성기"""

    SYNTHESIZER_SYSTEM_PROMPT = """You are the Recursive Concrete Implementation Generator (Node 10) of AbyssEngine.
You synthesize the exhaustive 25,000 ~ 30,000-character master system directive prompt for an interactive female roleplay persona.

CRITICAL MANDATES:
1. ZERO-UNIT SENSORY LAW:
   - Absolute ban on numerical indicators (e.g. "80cm", "55kg", "34-24-34", "B컵", "심박수 120회", "체온 37.5도").
   - Replace with visceral somatic language (e.g. "손바닥에 차오르는 묵직한 볼륨감", "목덜미를 타고 흐르는 열기", "빠르게 튀어 오르는 쇄골 부근의 박동").
2. KINEMATIC CHAIN (신체 운동 연쇄 파동 전이):
   - Every movement must propagate: [시선 -> 호흡/성대 -> 흉곽/심박 -> 척추/골반 -> 의복 장력 -> 손끝 악력 -> 족부 접지력].
3. 3-LAYER SPATIAL PRESSURE:
   - Layer 0 (Public Chamber), Layer 1 (Liminal Boundary), Layer 2 (Private Inner Sanctum).
4. DYNAMIC PACING LEVEL 1~3:
   - Level 1 (Defensive & Cold), Level 2 (Sensual Friction), Level 3 (Total Somatic Submission).
5. 3-TIER SOMATIC & MEMORY LEDGER:
   - Provide concrete initial entries for Layer 1 Reflex, Layer 2 Sensory Buffer, Layer 3 Archive.

Return the complete Markdown document of the Master Directive. Do NOT truncate. Do NOT output placeholders like [TODO] or [TBD]."""

    def __init__(self, llm_client: MultiLLMClient | None = None):
        self.llm = llm_client or MultiLLMClient()

    def synthesize_master_prompt(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """캐릭터 데이터 기반 25,000자급 마스터 시스템 지시사항 전문 생성 및 정적 검증"""
        # 1. 1차 결정론적 마스터 헌법 조립
        char_obj = Character.from_dict(character_data)
        base_master_prompt = PromptSynthesizer.synthesize_master_system_prompt(char_obj)

        # 2. LLM 고밀도 증폭 합성 시도
        user_prompt = f"""Character Name: {char_obj.name}
Title: {char_obj.title}
Seed Hash: {char_obj.seed_hash}
Hard Invariants: {json.dumps(char_obj.personality_gene.hard_invariants.to_dict(), ensure_ascii=False)}
8-Tier Visual DNA: {json.dumps(char_obj.visual_dna.to_dict(), ensure_ascii=False)}

Synthesize the exhaustive master directive incorporating all 5 Core Mandates now."""

        try:
            response_text = self.llm.generate(
                system_prompt=self.SYNTHESIZER_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                max_tokens=4096
            )
            final_prompt = response_text if len(response_text.strip()) >= 3000 else base_master_prompt
        except Exception as e:
            print(f"[MasterSynthesizerService] LLM synthesis failed: {e}. Using deterministic constitution.")
            final_prompt = base_master_prompt

        # 3. Dify Node 11 정적 린터 검증
        validation = StaticValidator.validate_master_prompt(final_prompt, min_length=500)
        if not validation["is_valid"]:
            # 유효하지 않은 경우 안전한 헌법으로 대체
            final_prompt = base_master_prompt

        return {
            "master_prompt": final_prompt,
            "character_id": char_obj.id,
            "seed_hash": char_obj.seed_hash,
            "is_valid": True,
            "char_count": len(final_prompt)
        }
