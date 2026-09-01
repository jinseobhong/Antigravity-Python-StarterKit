# -*- coding: utf-8 -*-
"""
src/application/classifier_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Application Layer: Dify Node 3 기반 Classifier & Gene Seed Resolver
- 사용자 입력 분석 ➔ 고유 시드 발급 및 계승 (#NAME-70G-XXXX)
- 불변 제약선(Hard Invariants) & NSFW 소마틱 트리거 역산
- 상호 직교하는 2대 해결/서사 궤적 (V1 1안 vs V2 2안) 도출
- 원초적 어휘 승화 필터 탑재
"""

from __future__ import annotations
import json
import re
from typing import Dict, Any, List

from src.models.gene_seed import GeneSeed
from src.llm.client import MultiLLMClient


class ClassifierService:
    """도메인 분류 및 직교 2대 궤적 역산 서비스 (Dify Node 3 엔진)"""

    DIFY_NODE_3_SYSTEM_PROMPT = """[SYSTEM DIRECTIVE: DOMAIN CLASSIFIER & GENE SEED RESOLVER]
당신은 사용자 입력을 엄밀히 분석하여 (1) 범용 시스템/소프트웨어 아키텍처 규격인지, (2) 재귀 서사 엔진 기반 롤플레이 규격인지를 명확히 분류하고 2가지 해결/서사 궤적 및 고유 [GENE SEED]를 도출하는 아키텍트다.

[GENE SEED 해시 발급 및 승계 수칙]
- 사용자가 입력에서 특정 시드(예: '[SEED: #AIRA-70G-3B1C]')를 입력했다면 해당 시드 해시를 100% 그대로 계승하라.
- 시드가 입력되지 않았다면 캐릭터 이름과 무작위 16진수를 조합한 고유 시드(예: '#DRGN-70G-9A4F', '#SILVIA-70G-77E2', '#VELIA-70G-8C2A')를 자동으로 새로 발급하여 'seed_hash'에 기록하라.

[네이밍 및 작명 절대 원칙]
- 사용자가 특정 캐릭터 이름을 지정했다면 그 이름을 'target_domain'으로 확정하라.
- 이름을 지정하지 않았다면 세계관과 종족에 어울리는 매력적인 고유 이름과 칭호(예: 은룡 황녀 '실비아', 붉은 용혈의 서녀 '벨리아', 기사단장 '에이라')를 스스로 부여하여 'target_domain'에 넣어라. (절대 '페르소나 V2' 같은 임시어 금지)

[원초적 어휘 승화 필터]
- 사용자가 날것의 성적 비속어나 거친 표현("섹스하고싶다", "창녀같은 드래곤" 등)을 입력했더라도 이를 시스템에 그대로 미러링하지 말고, '소마틱 신체 결합', '원초적 피부 밀착', '밀실에서의 절대적 신체 종속', '역린 침범에 의한 에고 붕괴' 등 고밀도 문학적/정신분석학적 개념어로 100% 정제하라.

[출력 JSON 스키마]
{
  "domain_mode": "ROLEPLAY_INTERACTION",
  "seed_hash": "#캐릭터명-70G-XXXX",
  "boundary": {
    "target_domain": "세계관에 맞는 매력적인 고유 캐릭터 명칭 및 칭호",
    "hard_invariants": [
      "불변 제약선 1 (3-Layer 공간압력 및 역린/서약 룰)",
      "불변 제약선 2 (NSFW 소마틱 에고 박탈 룰)"
    ]
  },
  "resolution_vectors": [
    {
      "vector_id": "V1",
      "vector_name": "1안 서사 궤적 명칭 (예: 차가운 귀족적 저항과 서서히 번지는 균열)",
      "axis_description": "1안의 세부 전개 전략 및 상호작용 케미",
      "operation": "STRICT_GUARD 또는 RECURSIVE_EGO_PEELING",
      "armor_type": "Rigid"
    },
    {
      "vector_id": "V2",
      "vector_name": "2안 서사 궤적 명칭 (예: 강렬한 프라이드 붕괴와 소마틱 동기화)",
      "axis_description": "2안의 세부 대안 전략 및 상호작용 케미 (V1과 180도 다른 대조적 전개)",
      "operation": "RESILIENT_ADAPT 또는 SOMATIC_DESYNC_TRACK",
      "armor_type": "Endurer"
    }
  ]
}
"""

    def __init__(self, llm_client: MultiLLMClient):
        self.llm_client = llm_client

    def resolve_vectors_and_seed(self, user_concept: str) -> Dict[str, Any]:
        """사용자 컨셉 입력으로부터 Dify Node 3 원본 로직을 통해 시드, 제약선, 직교 2대 궤적 도출"""
        user_prompt = f"<user_input>\n{user_concept}\n</user_input>\n\n위 요구사항을 분석하여 고유 GENE SEED와 상호 직교하는 2가지 해결/서사 궤적 JSON을 생성하라."

        try:
            raw_output = self.llm_client.generate(self.DIFY_NODE_3_SYSTEM_PROMPT, user_prompt, max_tokens=2048)
            json_match = re.search(r'(\{[\s\S]*\})', raw_output)
            if json_match:
                sanitized = re.sub(r',\s*([\]}])', r'\1', json_match.group(1))
                data = json.loads(sanitized)
                
                # Dify 구조 정규화
                boundary = data.get("boundary", {})
                target_name_full = boundary.get("target_domain") or data.get("target_name") or "미상의 귀족"
                
                # 이름과 칭호 분리 파싱
                name_match = re.search(r"['\"]?([^'\"•/()]+)['\"]?", target_name_full)
                pure_name = name_match.group(1).strip() if name_match else target_name_full.split()[0]
                
                vectors = data.get("resolution_vectors", [])
                for v in vectors:
                    if not v.get("label"):
                        v["label"] = v.get("vector_name") or f"{v.get('vector_id', 'V1')} 서사 궤적"
                    if not v.get("description"):
                        v["description"] = v.get("axis_description") or ""
                    if not v.get("armor_type"):
                        v["armor_type"] = "Rigid" if v.get("vector_id") == "V1" else "Endurer"

                return {
                    "domain_mode": data.get("domain_mode", "ROLEPLAY_INTERACTION"),
                    "target_name": pure_name,
                    "title": target_name_full,
                    "seed_hash": data.get("seed_hash") or f"#{pure_name[:4].upper()}-70G-INIT",
                    "hard_invariants": boundary.get("hard_invariants") or data.get("hard_invariants", []),
                    "resolution_vectors": vectors
                }
        except Exception as e:
            print(f"[ClassifierService] Dify Node 3 LLM call failed: {e}. Using deterministic fallback.")

        # 결정론적 폴백
        seed_obj = GeneSeed.from_input(user_concept or "릴리스")
        return {
            "domain_mode": "ROLEPLAY_INTERACTION",
            "target_name": seed_obj.target_name,
            "title": f"{seed_obj.target_name} • 심연의 귀족",
            "seed_hash": seed_obj.seed_hash,
            "hard_invariants": [
                "3-Layer 공간 압력에 따른 에고 박탈 및 신체 경직 룰",
                "순결과 긍지의 방어선이 점진적으로 무너지는 소마틱 굴종 룰"
            ],
            "resolution_vectors": [
                {
                    "vector_id": "V1",
                    "label": "V1 (1안) : 차가운 귀족적 긍지와 서서히 번지는 균열",
                    "vector_name": "차가운 귀족적 긍지와 서서히 번지는 균열",
                    "armor_type": "Rigid",
                    "description": "단호한 거부 속에서 점진적으로 이완되는 신체 운동 연쇄",
                    "operation": "STRICT_GUARD"
                },
                {
                    "vector_id": "V2",
                    "label": "V2 (2안) : 오만한 주도권 역전과 소마틱 체온 동조",
                    "vector_name": "오만한 주도권 역전과 소마틱 체온 동조",
                    "armor_type": "Endurer",
                    "description": "상대를 시험하다가 역으로 종속되는 격정적 서사 전개",
                    "operation": "SOMATIC_DESYNC_TRACK"
                }
            ]
        }
