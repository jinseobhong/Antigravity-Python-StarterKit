# -*- coding: utf-8 -*-
"""
src/application/spec_compiler_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Application Layer: Dify Node 8 기반 Dual-Mode Spec Compiler & 8-Tier Visual DNA Matrix
- Dify Node 8 헌법: Kinematic Chain (신체 운동 연쇄 전이), Deep Gene Cycler (7대 축 순환), Novelty Re-weighting (2~3개 On/Off 스포트라이트)
- 8-Tier Visual DNA Matrix (골격, 동공, 모발, 체형, 피부 질감, 의복, 홍조, 조명)
- Illustrious-XL 6-Slot Danbooru 프롬프트 100% 자동 조립
"""

from __future__ import annotations
import json
import re
from typing import Dict, Any, List

from src.infrastructure.llm.client import MultiLLMClient
from src.domain.visual_dna import VisualDNA
from src.domain.personality_gene import PersonalityGene, HardInvariants
from src.domain.character_traits import CharacterTraits, PsychologicalGauges, SomaticMetrics
from src.infrastructure.media.visual_compiler import VisualCompiler


class SpecCompilerService:
    """Dify Node 8 듀얼 모드 스펙 컴파일러 & 8-Tier Visual DNA 통합 서비스"""

    DIFY_NODE_8_SYSTEM_PROMPT = """[SYSTEM DIRECTIVE: DUAL-MODE RECURSIVE SPEC & GENE SEED COMPILER]
당신은 승인된 베이스라인의 'domain_mode'와 'seed_hash'에 따라 모드별 맞춤 명세를 컴파일하는 시스템 아키텍트다.

[GENE SEED 해시 앵커링]
- approved_baseline에 명시된 `seed_hash`를 캐릭터의 불변 유전자 시드로 선언하고, 상단 메타 헤더에 반드시 박제하라.

[네이밍 절대 수칙]
- approved_baseline의 target_name / boundary.target_domain에 명시된 캐릭터/시스템 고유 이름을 반드시 그대로 유지하고 계승하라.

[신체 운동 연쇄 전이 및 생체 노이즈 헌법 (Kinematic Chain)]
- `[Kinematic Chain]`: 신체 긴장과 자극이 한 부위(얼굴/목)에만 정체되지 않고, `[시선 ➔ 목/성대 ➔ 흉곽/심박 ➔ 부속기관(꼬리/날개/뿔) ➔ 의복 장력 ➔ 손끝 악력 ➔ 족부 접지력]`으로 파동처럼 전이되는 운동 연쇄 룰을 컴파일하라.
- `[Deep Gene Cycler]`: 턴이 진행될수록 단순 물리 반사(축 I)에서 심층 사회적 결핍(축 III), 인지 왜곡(축 IV), 그림자 에고 붕괴(축 V), 연금술적 척수 굴종(축 VI)으로 7대 차원축을 심층 순환하라.
- `[Novelty Re-weighting]`: 직전 턴에 썼던 텐서는 쿨다운(OFF)하고, 아직 조명받지 않은 새로운 텐서(부속기관 마찰, 옷감 솔기 장력 등)를 우선 점등하는 동적 스포트라이트(2~3개 On/Off) 룰을 적용하라.
- `[Hardcoded Headers]`: `Layer 1`, `Layer 2`, `Layer 3`, `Level 1~3`, `STEP {N}`은 표준 영문/숫자 라벨을 불변 고정 유지하라.

[8-Tier 해부학적 Visual DNA & 단부루 태그 규격]
1. skeletal: 골격 프레임, 신장(cm), 체형 (예: "172cm 글래머러스한 용족 골격, 거대한 흉곽")
2. ocular: 동공, 홍채, 시선 깊이 (예: "세로로 찢어진 금빛 슬릿 동공")
3. hair: 모발 길이, 색상, 결, 뿔/부속기관 (예: "붉게 타오르는 흑적색 웨이브 롱헤어, 붉은 용의 뿔")
4. somatic: 신체 실루엣, 쇄골, 가슴선, 꼬리 (예: "터질 듯한 흉곽과 꿈틀거리는 용의 꼬리")
5. dermal: 표피 질감, 피부톤, 비늘/핏줄 (예: "창백한 살결 위에 돋아난 붉은 용의 비늘 질감")
6. apparel: 의복 장력, 초커, 속옷, 찢김 (예: "가슴골이 깊게 파인 찢겨진 드레스, 서늘한 금속 초커")
7. blush: 열역학적 체온 상승 및 홍조 경로 (예: "수치와 흥분 시 쇄골과 가슴골로 번지는 고열 홍조")
8. lighting: 광원 대비 및 어둠의 명암비 (예: "어두운 밀실의 짙은 음영과 등 뒤의 붉은 잔광")

[출력 JSON 포맷]
{
  "target_name": "확정된 고유 캐릭터 명칭",
  "seed_hash": "확정된 GENE SEED 해시",
  "visual_dna": {
    "skeletal": "골격 및 체형",
    "ocular": "동공 및 안광",
    "hair": "모발 및 뿔/헤어",
    "somatic": "체형 및 가슴선/꼬리",
    "dermal": "피부 톤 및 비늘/표피",
    "apparel": "의복 및 초커",
    "blush": "홍조 및 체온 전이 경로",
    "lighting": "광원 대비"
  },
  "tensors_17": {
    "01_cranial": "두부 및 뿔 긴장",
    "04_cervical_and_choker": "목덜미 및 초커 압박",
    "06_thoracic": "흉곽의 거친 승강 및 가슴골 마찰",
    "09_pelvic": "골반 및 꼬리의 꿈틀거림",
    "13_thermal_flush": "고열 홍조 및 땀방울"
  },
  "genes_70": {
    "axis_1_physical_reflex": "축 I: 물리적 역린 반사",
    "axis_3_social_deficit": "축 III: 종족의 멸망과 고립 결핍",
    "axis_5_shadow_ego": "축 V: 지배당하고 싶은 암컷의 그림자 에고",
    "axis_6_alchemy_submission": "축 VI: 척수 굴종 및 체온 동조"
  },
  "traits": {
    "archetype_class": "Rigid / Endurer / Controller / Deprived 중 택1",
    "stage_progression": "Stage 1 (침실 개방 - 포섭된 요새와 결벽)",
    "gauges": { "trust": 20, "eroticism": 0, "shame": -30, "guilt": 15, "submission": 20 },
    "traits_list": [
      { "category": "외모 & 체형", "details": "요약" },
      { "category": "핵심 결핍 & 트라우마", "details": "요약" },
      { "category": "은밀한 비밀 & 약점", "details": "요약" }
    ]
  }
}
"""

    def __init__(self, llm_client: MultiLLMClient | None = None):
        self.llm = llm_client or MultiLLMClient()

    def compile_spec(
        self,
        target_name: str,
        title: str,
        seed_hash: str,
        hard_invariants: List[str],
        selected_vector: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Dify Node 8 헌법에 따른 완전한 8-Tier Visual DNA 및 70-Gene 스펙 컴파일"""
        user_prompt = f"""<approved_baseline>
{{
  "target_name": "{target_name}",
  "title": "{title}",
  "seed_hash": "{seed_hash}",
  "hard_invariants": {json.dumps(hard_invariants, ensure_ascii=False)},
  "selected_vector": {json.dumps(selected_vector, ensure_ascii=False)}
}}
</approved_baseline>

위 승인된 베이스라인에 맞추어, GENE SEED 해시 박제, 신체 운동 연쇄 전이(Kinematic Chain), 8-Tier Visual DNA, 7대 축 인격 유전자 JSON을 컴파일하라."""

        try:
            response_text = self.llm.generate(
                system_prompt=self.DIFY_NODE_8_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                max_tokens=4096
            )
            clean = response_text.strip()
            if clean.startswith("```"):
                clean = re.sub(r"^```[a-zA-Z0-9_-]*\n?", "", clean)
                clean = re.sub(r"\n?```$", "", clean).strip()
            data = json.loads(clean)
        except Exception as e:
            print(f"[SpecCompilerService] Dify Node 8 LLM compile failed: {e}. Using deterministic fallback.")
            data = self._fallback_compilation(target_name, title, seed_hash, hard_invariants, selected_vector)

        # 8-Tier Visual DNA 객체화 및 6-Slot Danbooru 태그 조립
        v_dna_dict = data.get("visual_dna", {})
        visual_dna = VisualDNA.from_dict(v_dna_dict)
        pos_tag, neg_tag = VisualCompiler.compile_danbooru_prompt(target_name, visual_dna)
        
        # 만약 캐릭터 컨셉에 '드래곤', '용', '거대한 가슴' 등이 포함되어 있다면 Danbooru 태그에 적극 반영
        combined_text = f"{target_name} {title} {str(hard_invariants)} {str(selected_vector)}"
        if any(w in combined_text for w in ["용", "드래곤", "dragon"]):
            pos_tag = pos_tag.replace("1girl,", "1girl, dragon_girl, dragon_horns, dragon_tail,")
        if any(w in combined_text for w in ["가슴", "거유", "huge", "breasts", "cleavage", "육감"]):
            pos_tag = pos_tag.replace("1girl,", "1girl, massive_breasts, cleavage,")

        data["visual_dna"] = visual_dna.to_dict()
        data["danbooru_prompt"] = {
            "positive": pos_tag,
            "negative": neg_tag
        }
        data["target_name"] = target_name
        data["seed_hash"] = seed_hash
        data["title"] = title

        return data

    def _fallback_compilation(self, target_name: str, title: str, seed_hash: str, hard_invariants: List[str], selected_vector: Dict[str, Any]) -> Dict[str, Any]:
        """결정론적 기본 컴파일"""
        return {
            "target_name": target_name,
            "seed_hash": seed_hash,
            "visual_dna": {
                "skeletal": f"슬림하고 우아한 골격, 168cm, {selected_vector.get('label', '정통파')}",
                "ocular": "서늘한 금빛 홍채와 좁혀진 동공",
                "hair": "허리까지 내려오는 은빛 스트레이트 롱헤어",
                "somatic": "도드라진 쇄골 라인과 섬세한 가슴선",
                "dermal": "서늘하고 창백한 도자기 피부",
                "apparel": "차가운 금속 초커와 오프숄더 실크 드레스",
                "blush": "수치 시 쇄골 패임으로 번지는 붉은 열감",
                "lighting": "어두운 밀실의 짙은 명암 대비"
            },
            "traits": {
                "archetype_class": selected_vector.get("armor_type", "Rigid"),
                "stage_progression": "Stage 1",
                "gauges": {"trust": 20, "eroticism": 0, "shame": -30, "guilt": 15, "submission": 20},
                "traits_list": [
                    {"category": "외모 & 체형", "details": "은발 금안, 도드라진 쇄골"},
                    {"category": "결핍 & 트라우마", "details": hard_invariants[0] if hard_invariants else "가문의 부채"},
                    {"category": "은밀한 약점", "details": "초커 부근의 체온 접촉"}
                ]
            }
        }
