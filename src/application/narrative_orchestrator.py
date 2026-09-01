# -*- coding: utf-8 -*-
"""
src/application/narrative_orchestrator.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Application Layer: Dify Node 10 기반 소마틱 서사 오케스트레이터
- 완급 조절(Level 1~3), 3-Layer 공간 압력, 신체 운동 연쇄 전이
- 3-Tier 신경·메모리 원장 실시간 갱신 & 5대 심리 게이지 동적 변화
- SQLite WAL DB에 실시간 트랜잭션 영속화
"""

from __future__ import annotations
import re
from typing import Dict, Any, Tuple

from src.domain.character import Character
from src.domain.kinematic_chain import KinematicChain
from src.domain.somatic_ledger import SomaticLedger
from src.infrastructure.database.repositories import CharacterRepository, TurnLedgerRepository
from src.infrastructure.llm.client import MultiLLMClient
from src.infrastructure.llm.prompt_synthesizer import PromptSynthesizer


class NarrativeOrchestrator:
    """실시간 소마틱 롤플레이 서사 오케스트레이터"""

    def __init__(
        self,
        char_repo: CharacterRepository,
        turn_repo: TurnLedgerRepository,
        llm_client: MultiLLMClient
    ):
        self.char_repo = char_repo
        self.turn_repo = turn_repo
        self.llm_client = llm_client

    def execute_turn(
        self,
        character_id: int,
        user_action: str,
        stimulus_type: str = "DEFAULT"
    ) -> Dict[str, Any]:
        """플레이어의 턴 행동을 받아 LLM 서사 생성 및 3-Tier 원장 / 5대 게이지 영속 갱신"""
        char = self.char_repo.get_by_id(character_id)
        if not char:
            raise ValueError(f"Character ID {character_id} not found.")

        history = self.turn_repo.get_history(character_id)
        turn_number = len(history) + 1

        # 1. 시스템 프롬프트 및 턴 프롬프트 조립
        system_prompt = PromptSynthesizer.synthesize_master_system_prompt(char)
        turn_prompt = PromptSynthesizer.synthesize_turn_prompt(
            char, turn_number, user_action, history, stimulus_type
        )

        # 2. LLM 서사 생성
        try:
            raw_response = self.llm_client.generate(system_prompt, turn_prompt, max_tokens=4096)
        except Exception as e:
            print(f"[NarrativeOrchestrator] LLM turn generation failed: {e}. Generating offline response.")
            raw_response = self._generate_fallback_response(char, turn_number, user_action, stimulus_type)

        # 3. 응답 파싱 (Meta, Narrative, Ledger)
        meta_status, narrative_prose, ledger_obj = self._parse_llm_turn_output(raw_response, char, turn_number)

        # 4. 5대 심리 게이지 동적 변화 계산 (자극 유형 및 턴에 따라 반영)
        self._update_gauges_by_stimulus(char, stimulus_type)

        # 5. 캐릭터 상태 갱신 및 저장
        char.somatic_ledger = ledger_obj
        self.char_repo.save(char)

        # 6. 턴 히스토리 영속화
        self.turn_repo.record_turn(
            character_id=character_id,
            turn_number=turn_number,
            user_action=user_action,
            narrative_response=narrative_prose,
            meta_status=meta_status,
            somatic_ledger=ledger_obj.to_dict(),
            gauges=char.traits.gauges.to_dict()
        )

        return {
            "turn_number": turn_number,
            "character_id": character_id,
            "character_name": char.name,
            "user_action": user_action,
            "narrative_response": narrative_prose,
            "meta_status": meta_status,
            "somatic_ledger": ledger_obj.to_dict(),
            "gauges": char.traits.gauges.to_dict(),
            "raw_output": raw_response
        }

    def _update_gauges_by_stimulus(self, char: Character, stimulus_type: str) -> None:
        """자극 유형에 따른 5대 심리 게이지 변화"""
        g = char.traits.gauges
        if stimulus_type in ("순애", "AFFECTION", "COMFORT"):
            g.trust += 5
            g.eroticism += 2
            g.shame -= 5
            g.submission += 2
        elif stimulus_type in ("압박", "PRESSURE", "CONQUEST"):
            g.trust -= 2
            g.eroticism += 5
            g.shame += 10
            g.submission += 8
        elif stimulus_type in ("유혹", "SEDUCTION", "STIMULATION"):
            g.eroticism += 8
            g.shame += 5
            g.submission += 5
        elif stimulus_type in ("제압", "SUBJUGATION", "RELAX"):
            g.trust += 2
            g.shame += 2
            g.submission += 6
        elif stimulus_type in ("탐색", "EXPLORE", "SYNC"):
            g.trust += 4
            g.eroticism += 3
        else:
            g.trust += 1
            g.eroticism += 1
            g.submission += 1
        g.clamp()

    def _parse_llm_turn_output(
        self,
        raw_output: str,
        char: Character,
        turn_number: int
    ) -> Tuple[Dict[str, Any], str, SomaticLedger]:
        """LLM 출력에서 [STATUS META], [NARRATIVE], [CUMULATIVE NEURAL & MEMORY LEDGER] 파싱"""
        meta_dict = {
            "seed_hash": char.gene_seed.seed_hash,
            "turn_number": turn_number,
            "pacing_level": f"Level {min(3, max(1, (turn_number + 1) // 2))}",
            "spatial_layer": f"Layer {char.spatial_pressure.layer_level} ({char.spatial_pressure.location_name})",
            "spotlights": KinematicChain.get_spotlight_tensors(turn_number)
        }

        narrative_part = raw_output
        l1 = "목덜미 초커 부근으로 경직된 척추와 방어적 호흡."
        l2 = "귓바퀴와 쇄골로 서서히 번지는 붉은 열감."
        l3 = "자신의 긍지가 흔들리는 것에 대한 내적 혼란."

        # NARRATIVE 섹션 추출
        narrative_match = re.search(r'\[NARRATIVE\]([\s\S]*?)(?=\[CUMULATIVE|\Z)', raw_output, re.IGNORECASE)
        if narrative_match:
            narrative_part = narrative_match.group(1).strip()

        # LEDGER 섹션 추출
        l1_match = re.search(r'Layer 1[^\n:]*:\s*([^\n]+)', raw_output)
        if l1_match:
            l1 = l1_match.group(1).strip()
        l2_match = re.search(r'Layer 2[^\n:]*:\s*([^\n]+)', raw_output)
        if l2_match:
            l2 = l2_match.group(1).strip()
        l3_match = re.search(r'Layer 3[^\n:]*:\s*([^\n]+)', raw_output)
        if l3_match:
            l3 = l3_match.group(1).strip()

        return meta_dict, narrative_part, SomaticLedger(l1, l2, l3)

    def _generate_fallback_response(
        self,
        char: Character,
        turn_number: int,
        user_action: str,
        stimulus_type: str
    ) -> str:
        """오프라인 또는 오류 시 결정론적 문학적 폴백 서사"""
        return f"""[STATUS META]
• [SEED HASH] {char.gene_seed.seed_hash}
• [서사 호흡] Level 2 | [공간 압력] Layer {char.spatial_pressure.layer_level} ({char.spatial_pressure.location_name})
• [활성화 유전자] 축 I (물리적 기질 반사), 축 IV (인지 왜곡 방어기제)
• [활성화 텐서] 02_ocular_and_gaze, 06_apparel_tension_and_seam

[NARRATIVE]
차가운 침실 안, 서늘한 공기 속에서 {char.name}는 서서히 다가오는 당신의 그림자를 차갑게 응시하고 있었다.
은빛 머리칼은 달빛을 받아 서늘하게 부서졌고, 목을 옥죄고 있는 금속 초커 사이로 그녀의 가느다란 목덜미가 미세하게 진동했다.

"……선을 넘지 마라. 무례한 자여. 나의 긍지와 순결은 네 손길 따위에 흔들리지 않는다."

{char.name}는 턱을 치켜올리며 오만한 눈빛을 유지하려 애썼으나, 목덜미를 스치는 서늘한 체온 앞에서 그녀의 귓바퀴와 쇄골에는 이미 숨길 수 없는 붉은 열감이 서서히 번져가고 있었다.

[CUMULATIVE NEURAL & MEMORY LEDGER]
• Layer 1 (Primitive Reflex Matrix): 서늘한 초커 틈새로 경직된 척추와 불규칙해진 나노 호흡.
• Layer 2 (Short-Term Somatic Buffer): 귓바퀴와 쇄골 패임으로 걷잡을 수 없이 번져가는 붉은 열감.
• Layer 3 (Long-Term Somatic & Semantic Archive): 이 침입자 앞에서 자신의 오만한 방어선이 서서히 침식당하고 있다는 전율."""
