# -*- coding: utf-8 -*-
"""
src/application/classifier_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Application Layer: Dify Node 3 기반 Classifier & Vector Resolver
- 사용자 입력 분석 ➔ 고유 시드 발급 (#NAME-70G-XXXX)
- 불변 제약선(Hard Invariants) & NSFW 소마틱 트리거 선행 역산
- 상호 직교하는 2대 해결/서사 궤적 (V1 1안 vs V2 2안) 도출
"""

from __future__ import annotations
import json
import re
from typing import Dict, Any, List

from src.domain.gene_seed import GeneSeed
from src.infrastructure.llm.client import MultiLLMClient


class ClassifierService:
    """도메인 분류 및 직교 2대 궤적 역산 서비스"""

    def __init__(self, llm_client: MultiLLMClient):
        self.llm_client = llm_client

    def resolve_vectors_and_seed(self, user_concept: str) -> Dict[str, Any]:
        """사용자 컨셉 입력으로부터 시드, 제약선, 직교 2대 궤적(V1, V2) 역산"""
        system_prompt = """[SYSTEM DIRECTIVE: DOMAIN CLASSIFIER & ORTHOGONAL VECTOR RESOLVER]
당신은 다크 판타지 서사 엔진의 수석 아키텍트다.
사용자의 캐릭터 컨셉을 분석하여 다음 4가지를 도출하라:
1. 'target_name': 세계관에 맞는 매력적인 여성 캐릭터 이름 및 칭호 (예: 릴리스 (제1황녀 • 제국 황실))
2. 'seed_hash': '#NAME-70G-XXXX' 규격의 고유 시드 해시 (사용자가 입력한 시드가 있다면 100% 계승)
3. 'hard_invariants': 목숨보다 지키려는 도덕적/귀족적 결벽증 및 NSFW 소마틱 트리거 2~3개
4. 'resolution_vectors': 상호 직교하는 2가지 대안 서사 전개 궤적 (V1: 1안, V2: 2안)
   - V1: 1안 전략 (예: 엄격한 방어선과 점진적 신체 이완)
   - V2: 2안 전략 (예: 주도권 역전과 소마틱 체온 동조)

[원초적 어휘 승화 필터]
- 날것의 슬랭을 배제하고 '소마틱 신체 결합', '원초적 피부 밀착', '밀실에서의 절대적 신체 종속' 등 고밀도 문학적 개념어로 정제하라.

[출력 JSON 포맷]
{
  "target_name": "캐릭터 이름",
  "title": "칭호",
  "seed_hash": "#NAME-70G-XXXX",
  "hard_invariants": [
    "불변 제약선 1",
    "NSFW 소마틱 파멸 트리거 2"
  ],
  "resolution_vectors": [
    {
      "vector_id": "V1",
      "vector_name": "1안 서사 궤적 명칭",
      "axis_description": "1안 세부 전개 전략 및 케미",
      "operation": "STRICT_GUARD"
    },
    {
      "vector_id": "V2",
      "vector_name": "2안 서사 궤적 명칭",
      "axis_description": "2안 세부 전개 전략 및 케미",
      "operation": "SOMATIC_REVERSAL"
    }
  ]
}
"""
        user_prompt = f"사용자 캐릭터 컨셉:\n{user_concept}\n\n위 컨셉을 분석하여 시드 해시, 불변 제약선, 직교 2대 궤적(V1, V2) JSON을 생성하라."

        try:
            raw_output = self.llm_client.generate(system_prompt, user_prompt, max_tokens=2048)
            json_match = re.search(r'(\{[\s\S]*\})', raw_output)
            if json_match:
                sanitized = re.sub(r',\s*([\]}])', r'\1', json_match.group(1))
                data = json.loads(sanitized)
                return data
        except Exception as e:
            print(f"[ClassifierService] LLM vector resolution failed: {e}. Using deterministic fallback.")

        # 오프라인/페일오버 결정론적 폴백
        seed_obj = GeneSeed.from_input(user_concept or "릴리스")
        return {
            "target_name": seed_obj.target_name,
            "title": "제국 황녀",
            "seed_hash": seed_obj.seed_hash,
            "hard_invariants": [
                "선조 가문의 막대한 부채와 순결 서약의 도덕적 결벽증",
                "목덜미 초커를 쥔 채 시선을 강제로 고정당하는 순간의 자아 붕괴"
            ],
            "resolution_vectors": [
                {
                    "vector_id": "V1",
                    "vector_name": "[1안] 차가운 귀족적 긍지와 서서히 번지는 균열",
                    "axis_description": "단호한 거부 속에서 점진적으로 이완되는 신체 운동 연쇄",
                    "operation": "STRICT_GUARD"
                },
                {
                    "vector_id": "V2",
                    "vector_name": "[2안] 오만한 주도권 역전과 소마틱 체온 동조",
                    "axis_description": "상대를 시험하다가 역으로 종속되는 격정적 서사 전개",
                    "operation": "SOMATIC_REVERSAL"
                }
            ]
        }
