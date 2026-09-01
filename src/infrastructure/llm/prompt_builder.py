# -*- coding: utf-8 -*-
"""
src/infrastructure/llm/prompt_builder.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
17대 텐서 수치 및 70대 신체 헌법 노드를 서사 생성 프롬프트로 합성하는 빌더
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any

from src.domain.character import Character
from src.domain.action_frame import ActionFrame
from src.domain.tensor_matrix import TENSOR_REGISTRY


class PromptBuilder:
    """고밀도 문학 서사 생성용 프롬프트 합성기"""

    @staticmethod
    def build_narrative_prompts(
        character: Character,
        action_frame: ActionFrame,
        turn_number: int,
        recent_chat_history: List[Dict[str, Any]]
    ) -> Tuple[str, str]:
        """시스템 지시문 및 유저 프롬프트 생성"""
        system_prompt = f"""
당신은 최고급 몰입형 인터랙티브 서사 롤플레이 작가입니다.
[캐릭터 정보]
- 이름: {character.name} ({character.title})
- 소속/진영: {character.faction}
- 신체 갑주 유형: {character.armor_type.value}
- 현재 압력 상태: {character.pressure_stage.value}
- 자아 내구도: {character.ego_durability:.1f}% / 신경 오염도: {character.neural_taint:.1f}%

[핵심 서사 집필 규칙]
1. 플레이어의 행동에 대해 캐릭터의 내면적 심리 갈등과 미세한 신체 생체 반응을 고밀도로 묘사하십시오.
2. 대사는 반드시 큰따옴표(\"...\")로 묶고 독립된 줄로 분리하십시오.
3. [SOM_...], [STATUS] 등의 기계적인 스탯 태그나 수치 텍스트를 절대 출력하지 마십시오.
"""

        spotlights = [TENSOR_REGISTRY.get(t, t) for t in character.tensors.active_spotlights]
        user_prompt = f"""
[현재 턴 {turn_number}]
- 플레이어 행동: {action_frame.raw_text}
- 주요 발화 화행: {action_frame.speech_act.value}
- 감각 집중 부위: {', '.join(spotlights) if spotlights else '경추/호흡'}
- 관계역학 벡터: {action_frame.dominant_vector.value}

위 상황에 이어지는 캐릭터의 심리적 저항과 신체적 반응을 문학적 서사로 집필하십시오.
"""
        return system_prompt.strip(), user_prompt.strip()
