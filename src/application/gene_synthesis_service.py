# -*- coding: utf-8 -*-
"""
src/application/gene_synthesis_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Application Layer: Dify Node 7 기반 8-Tier Visual DNA & 70단계 유전자 동적 합성 서비스
- 선택된 직교 벡터(V1 or V2)와 제약선으로부터 8중 외모 및 7대 축 인격 유전자 1:1 컴파일
- Illustrious-XL 6-Slot 단부루 태그 연동 및 DB 영속화
"""

from __future__ import annotations
import json
import re
from typing import Dict, Any, Optional

from src.domain.gene_seed import GeneSeed
from src.domain.visual_dna import VisualDNA
from src.domain.personality_gene import PersonalityGene, HardInvariants
from src.domain.character_traits import CharacterTraits, PsychologicalGauges, SomaticMetrics
from src.domain.somatic_ledger import SomaticLedger
from src.domain.spatial_pressure import SpatialPressure
from src.domain.character import Character
from src.infrastructure.database.repositories import CharacterRepository
from src.infrastructure.media.visual_compiler import VisualCompiler
from src.infrastructure.llm.client import MultiLLMClient


class GeneSynthesisService:
    """8-Tier Visual DNA & 유전자 합성기"""

    def __init__(self, char_repo: CharacterRepository, llm_client: MultiLLMClient):
        self.char_repo = char_repo
        self.llm_client = llm_client

    def compile_character(
        self,
        target_name: str,
        title: str,
        seed_hash: str,
        hard_invariants: list,
        selected_vector: Dict[str, Any]
    ) -> Character:
        """선택된 궤적(V1 or V2)과 제약선으로부터 완전한 Character 애그리게이트 생성 및 영속화"""
        
        system_prompt = """[SYSTEM DIRECTIVE: 8-TIER VISUAL DNA & 70-GENE COMPILER]
당신은 승인된 베이스라인과 선택된 궤적(V1/V2)에 맞추어 다음 8-Tier Visual DNA와 7대 축 유전자를 컴파일하는 아키텍트다.
반드시 아래 JSON 스키마를 만족하라:

{
  "visual_dna": {
    "face_geometry": "턱선, 입술, 코선",
    "ocular_optics": "홍채 색상, 동공 림, 속눈썹",
    "hair_physics": "모발 길이, 색상, 결, 잔머리",
    "body_silhouette": "신장(cm), 체형 실루엣, 쇄골/골격 돌출도",
    "dermal_texture": "피부 톤, 표피 질감, 핏줄 가시성",
    "apparel_accents": "메인 의복 스타일, 초커/리본/갑주/장신구",
    "somatic_flush_cue": "수치/체온 상승 시 쇄골·귓바퀴 홍조 경로",
    "lighting_contrast": "기본 광원 대비 및 명암비"
  },
  "personality_gene": {
    "axis_1_physical_reflex": "축 I: 물리적 기질 및 체성 수용체",
    "axis_2_neuro_memory": "축 II: 신경화학 및 소마틱 신체 기억",
    "axis_3_social_deficit": "축 III: 사회적 형성사 및 과거 결핍",
    "axis_4_cognitive_distortion": "축 IV: 인지 왜곡 및 방어기제",
    "axis_5_shadow_ego": "축 V: 그림자 에고 및 피지배 갈망",
    "axis_6_alchemy_submission": "축 VI: 연금술적 각성 및 척수 굴종",
    "axis_7_gesture_ticks": ["제스처 틱 1", "제스처 틱 2", "제스처 틱 3"]
  },
  "traits": {
    "archetype_class": "Rigid / Endurer / Controller / Deprived 중 택1",
    "stage_progression": "Stage 1 (침실 개방 - 포섭된 요새와 결벽)",
    "traits_list": [
      {"category": "외모 & 체형", "details": "요약"},
      {"category": "핵심 결핍 & 트라우마", "details": "요약"},
      {"category": "은밀한 비밀 & 약점", "details": "요약"}
    ]
  }
}
"""
        user_prompt = f"""[캐릭터 정보]
- 이름: {target_name} ({title})
- 시드 해시: {seed_hash}
- 불변 제약선: {json.dumps(hard_invariants, ensure_ascii=False)}
- 선택된 서사 궤적: {json.dumps(selected_vector, ensure_ascii=False)}

위 정보를 바탕으로 완결된 8-Tier Visual DNA, 7대 축 유전자, Traits JSON을 생성하라."""

        v_dna = None
        p_gene = None
        traits = None

        try:
            raw_output = self.llm_client.generate(system_prompt, user_prompt, max_tokens=4096)
            json_match = re.search(r'(\{[\s\S]*\})', raw_output)
            if json_match:
                sanitized = re.sub(r',\s*([\]}])', r'\1', json_match.group(1))
                data = json.loads(sanitized)
                v_dna = VisualDNA.from_dict(data.get("visual_dna", {}))
                
                inv_obj = HardInvariants(
                    primary_boundary=hard_invariants[0] if len(hard_invariants) > 0 else "가문의 명예",
                    ego_collapse_trigger=hard_invariants[1] if len(hard_invariants) > 1 else "초커 강제 시선 고정",
                    somatic_achilles_heel="쇄골 패임의 직접적 체온 접촉"
                )
                p_data = data.get("personality_gene", {})
                p_gene = PersonalityGene.from_dict({**p_data, "hard_invariants": inv_obj.to_dict()})
                traits = CharacterTraits.from_dict(data.get("traits", {}))
        except Exception as e:
            print(f"[GeneSynthesisService] LLM compile failed: {e}. Using deterministic fallback.")

        # 폴백 생성
        if not v_dna:
            v_dna = VisualDNA(
                face_geometry="차가운 오만함을 두른 날렵한 V-line 턱선, 굳게 다문 얇은 입술",
                ocular_optics="서늘한 금빛 홍채와 짙은 호박색 림, 긴 속눈썹",
                hair_physics="허리 아래까지 단정하게 흘러내리는 백은색 직모",
                body_silhouette="168cm의 호리호리한 체형, 꼿꼿한 척추와 깊게 도드라진 쇄골 패임",
                dermal_texture="창백한 백옥 피부, 목덜미의 푸른 핏줄",
                apparel_accents="어깨가 드러난 흑색 실크 오프숄더 드레스, 차가운 은색 금속 초커",
                somatic_flush_cue="극도의 수치 시 쇄골 패임과 귓바퀴로 번지는 붉은 열감",
                lighting_contrast="차가운 달빛과 어두운 밀실의 짙은 명암 대비"
            )
        if not p_gene:
            inv_obj = HardInvariants(
                primary_boundary=hard_invariants[0] if len(hard_invariants) > 0 else "가문의 명예",
                ego_collapse_trigger=hard_invariants[1] if len(hard_invariants) > 1 else "초커 강제 시선 고정",
                somatic_achilles_heel="쇄골 패임의 직접적 체온 접촉"
            )
            p_gene = PersonalityGene(
                hard_invariants=inv_obj,
                axis_1_physical_reflex="목덜미와 초커에 손길이 닿을 때 척추가 경직되며 얕아지는 호흡",
                axis_2_neuro_memory="타락에 대한 공포로 인해 심박이 급격히 상승하며 쇄골이 떨림",
                axis_3_social_deficit="가문의 멸망을 막기 위해 모든 욕망을 거세당한 채 자라난 고립감",
                axis_4_cognitive_distortion="누군가에게 지배당하는 것은 곧 영혼의 파멸이라는 신념",
                axis_5_shadow_ego="자신의 모든 긍지를 산산조각 내어줄 지배자에게 짐을 넘기고 싶은 갈망",
                axis_6_alchemy_submission="체온이 깊게 침투할수록 척수에서부터 무너져 내리는 굴종",
                axis_7_gesture_ticks=["턱을 치켜올려 오만함 유지", "초커 만지작거리기", "시선 내리깔기"]
            )
        if not traits:
            traits = CharacterTraits(
                archetype_title=title or "제국 황녀",
                archetype_class="Rigid (결벽주의 척추 방어)",
                stage_progression="Stage 1 (침실 개방 - 포섭된 요새와 결벽)",
                gauges=PsychologicalGauges(trust=20, eroticism=0, shame=-30, guilt=15, submission=20),
                somatic_metrics=SomaticMetrics(odo="54.2%", taint="7.1%"),
                traits_list=[
                    {"category": "외모 & 체형", "details": f"{v_dna.hair_physics}, {v_dna.ocular_optics}"},
                    {"category": "핵심 결핍 & 트라우마", "details": p_gene.axis_3_social_deficit},
                    {"category": "은밀한 비밀 & 약점", "details": p_gene.hard_invariants.somatic_achilles_heel}
                ]
            )

        # 단부루 태그 컴파일
        pos_prompt, neg_prompt = VisualCompiler.compile_danbooru_prompt(target_name, v_dna)
        v_dna.danbooru_prompt = pos_prompt
        v_dna.negative_prompt = neg_prompt

        seed_obj = GeneSeed.from_input(target_name, seed_hash)
        ledger = SomaticLedger(
            layer_1_reflex="목덜미의 서늘한 금속 초커 사이로 경직된 척추의 영구 방어 기제.",
            layer_2_buffer="귓바퀴와 쇄골로 서서히 번지는 붉은 열감, 헐떡이는 호흡의 미세한 흐트러짐.",
            layer_3_archive="나의 긍지와 위엄은 너의 손길 따위에 흔들리지 않는다는 내적 독백의 균열."
        )
        sp = SpatialPressure.create(1, f"{target_name}의 사적 침실")

        char = Character(
            id=None,
            name=target_name,
            title=title or "미상의 귀족",
            gene_seed=seed_obj,
            visual_dna=v_dna,
            personality_gene=p_gene,
            traits=traits,
            somatic_ledger=ledger,
            spatial_pressure=sp,
            portrait_url="",
            is_active=True
        )

        saved_char = self.char_repo.save(char)
        return saved_char
