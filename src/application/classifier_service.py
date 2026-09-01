# -*- coding: utf-8 -*-
"""
src/application/classifier_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[Dify Node 1788098588498: CLASSIFIER & VECTOR RESOLVER]
- 사용자 입력 분석 및 고유 GENE SEED 발급
- 불변 제약선(Hard Invariants) 역산
- 2대 서사 충돌 궤적(V1 저항 vs V2 붕괴) 도출
"""

from __future__ import annotations
import json
import re
from typing import Dict, Any, List

from src.domain.gene_seed import GeneSeed
from src.infrastructure.llm.client import MultiLLMClient


class ClassifierService:
    """제약 조건 역산 및 V1/V2 서사 궤적 분류기"""

    def __init__(self, llm_client: MultiLLMClient):
        self.llm = llm_client

    def resolve_boundary_and_vectors(self, user_query: str, explicit_seed: str = "") -> Dict[str, Any]:
        """사용자 입력으로부터 제약선 및 2대 서사 궤적 도출 (Human Checkpoint 1용)"""
        # 1. 고유 시드 발급
        # 기본 캐릭터 이름 추출 (예: '릴리스', '에이라', '세라피나', '실비아' 등)
        target_name = "릴리스"
        for name in ["릴리스", "에이라", "세라피나", "실비아"]:
            if name in user_query:
                target_name = name
                break
        else:
            match = re.search(r'([가-힣A-Za-z]{2,8})', user_query)
            if match:
                target_name = match.group(1)

        gene_seed = GeneSeed.from_input(target_name, explicit_seed=explicit_seed)

        system_instruction = """[SYSTEM DIRECTIVE: DOMAIN CLASSIFIER & CONSTRAINT RESOLVER]
당신은 사용자 입력을 분석하여 (1) 캐릭터의 절대 불변 제약선(Hard Invariants), (2) 2가지 해결/서사 충돌 궤적(V1 vs V2)을 도출하는 수석 아키텍트다.
원초적 비속어나 거친 표현은 '소마틱 신체 결합', '원초적 피부 밀착', '밀실에서의 절대적 신체 종속' 등 고밀도 문학 개념어로 승화하라.

반드시 다음 JSON 포맷으로만 응답하라:
{
  "target_domain": "캐릭터 고유 이름 및 칭호",
  "hard_invariants": {
    "primary_boundary": "목숨보다 지키려는 도덕적/귀족적 결벽증 및 제약선",
    "ego_collapse_trigger": "자아 붕괴 트리거",
    "somatic_achilles_heel": "생체 취약 부위"
  },
  "resolution_vectors": [
    {
      "vector_id": "V1",
      "vector_name": "1안: 차가운 귀족적 저항과 서서히 번지는 균열",
      "axis_description": "차가운 방어선을 고수하며 미세한 신체적 동요만을 드러내는 궤적",
      "operation": "STRICT_GUARD"
    },
    {
      "vector_id": "V2",
      "vector_name": "2안: 강렬한 프라이드 붕괴와 소마틱 체온 동조",
      "axis_description": "제약선이 한계까지 몰려 파열되며 급격한 신체적 밀착과 굴종으로 전이되는 궤적",
      "operation": "RECURSIVE_EGO_PEELING"
    }
  ]
}"""
        response_text = self.llm.generate_text(system_instruction, user_query)
        try:
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                parsed = json.loads(json_match.group(0))
            else:
                parsed = {}
        except Exception:
            parsed = {}

        hard_invariants = parsed.get("hard_invariants", {
            "primary_boundary": "선조 가문의 부채와 순결 서약의 도덕적 결벽증",
            "ego_collapse_trigger": "목덜미 초커를 쥐고 강제로 시선을 맞출 때",
            "somatic_achilles_heel": "쇄골 패임의 직접적 체온 접촉"
        })

        vectors = parsed.get("resolution_vectors", [
            {
                "vector_id": "V1",
                "vector_name": "1안: 차가운 귀족적 저항과 방어선 고수",
                "axis_description": "차가운 시선과 날카로운 언어로 방어선을 유지하는 궤적",
                "operation": "STRICT_GUARD"
            },
            {
                "vector_id": "V2",
                "vector_name": "2안: 프라이드 붕괴와 소마틱 동조",
                "axis_description": "제약선이 무너지며 호흡과 체온이 급격히 일치되는 궤적",
                "operation": "RECURSIVE_EGO_PEELING"
            }
        ])

        return {
            "seed_hash": gene_seed.seed_hash,
            "target_name": target_name,
            "hard_invariants": hard_invariants,
            "resolution_vectors": vectors,
            "raw_query": user_query
        }
