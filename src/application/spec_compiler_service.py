# -*- coding: utf-8 -*-
"""
src/application/spec_compiler_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Application Layer: Dify Node 7 기반 듀얼 모드 스펙 컴파일러 (Dual-Mode Spec Compiler)
- 8-Tier 해부학적 Visual DNA Matrix 컴파일
- Track 1: 17대 범용 생체·의복 텐서 매트릭스 ([01_cranial] ~ [17_aura])
- Track 2: 7대 차원축 70단계 인격 유전자 (Axis I ~ Axis VII)
- Kinematic Chain 7단계 신체 운동 연쇄 파동 전이 및 스포트라이트
- Illustrious-XL 6-Slot Danbooru 프롬프트 자동 조립
"""

from __future__ import annotations
import json
import re
from typing import Dict, Any, List

from src.infrastructure.llm.client import MultiLLMClient
from src.domain.visual_dna import VisualDNA
from src.domain.personality_gene import PersonalityGene, HardInvariants
from src.domain.character_traits import CharacterTraits
from src.infrastructure.media.visual_compiler import VisualCompiler


class SpecCompilerService:
    """Dify Node 7 스펙 컴파일러 서비스"""

    COMPILER_SYSTEM_PROMPT = """You are the Dual-Mode Specification Compiler (Node 7) of AbyssEngine.
Given a baseline character entity (Target Name, Title, Seed Hash, Hard Invariants, Selected Orthogonal Vector),
compile the full high-precision specification conforming strictly to the 25-Master standards:

1. 8-Tier Visual DNA:
   - skeletal: Frame & bone structure (e.g. "슬림하고 단련된 황실 골격, 168cm")
   - ocular: Pupil/Iris depth & gaze (e.g. "서늘한 백금빛 금안, 좁혀진 동공")
   - hair: Hair texture, length, style (e.g. "허리까지 내려오는 은발 스트레이트")
   - somatic: Somatic shape & proportions (e.g. "유려한 쇄골 라인과 섬세한 가슴선")
   - dermal: Skin texture & moisture (e.g. "서늘하고 창백한 도자기 피부")
   - apparel: Hard apparel & choker constraints (e.g. "금속 초커와 오프숄더 제복 드레스")
   - blush: Thermal flush & reaction pattern (e.g. "당황 시 뺨에서 쇄골로 번지는 홍조")
   - lighting: Contrast & ambient illumination (e.g. "차갑고 날카로운 달빛 음영")

2. 17 Universal Somatic & Apparel Tensors (17대 생체·의복 텐서):
   - Provide concrete descriptive specifications for at least:
     01_cranial, 02_ocular, 03_oral, 04_cervical_and_choker, 05_clavicle, 06_thoracic, 07_respiratory,
     08_lumbar, 09_pelvic, 10_digital_extremities, 11_pedal, 12_dermal_texture, 13_thermal_flush,
     14_apparel_tension, 15_olfactory, 16_visceral, 17_aura.

3. 70 Universal Personality Genes (7대 차원축 70단계 유전자):
   - Axis I (1-10): Ego & Power Drive (에고 및 지배욕)
   - Axis II (11-20): Somatic Vulnerability & Defense (신체 방어선)
   - Axis III (21-30): Erotic Receptivity (성애 수용도)
   - Axis IV (31-40): Moral & Ethical Friction (도덕적 마찰/죄책감)
   - Axis V (41-50): Spatial Intimacy Threshold (공간 친밀도 역치)
   - Axis VI (51-60): Verbal Reticence & Subversion (언어적 저항/복종)
   - Axis VII (61-70): Submission Equilibrium (최종 굴종 평형점)

4. 16 RDB Traits & Gauges:
   - gauges: trust (0-100), eroticism (0-100), shame (-100-100), guilt (0-100), submission (0-100)
   - traits_list: 3-5 key structured traits (category, details)

Return ONLY valid JSON matching this structure:
{
  "visual_dna": { ... 8 tiers ... },
  "tensors_17": { ... 17 tensor strings ... },
  "genes_70": { "gene_01": "...", ... "gene_70": "..." },
  "traits": {
    "archetype_class": "...",
    "stage_progression": "Stage 1",
    "gauges": { "trust": 20, "eroticism": 0, "shame": -30, "guilt": 15, "submission": 20 },
    "traits_list": [
      { "category": "신체/의복", "details": "..." },
      { "category": "결핍/서약", "details": "..." },
      { "category": "감각/반사", "details": "..." }
    ]
  }
}"""

    def __init__(self, llm_client: MultiLLMClient | None = None):
        self.llm = llm_client or MultiLLMClient()

    def compile_spec(self, target_name: str, title: str, seed_hash: str, hard_invariants: List[str], selected_vector: Dict[str, Any]) -> Dict[str, Any]:
        """Dify Node 7: 8-Tier DNA, 17대 텐서, 70단계 유전자 종합 컴파일"""
        user_prompt = f"""Target Name: {target_name}
Title: {title}
Seed Hash: {seed_hash}
Hard Invariants: {json.dumps(hard_invariants, ensure_ascii=False)}
Selected Orthogonal Vector: {json.dumps(selected_vector, ensure_ascii=False)}

Compile the complete 8-Tier Visual DNA, 17 Somatic Tensors, 70 Personality Genes, and Structured Traits now."""

        try:
            response_text = self.llm.generate(
                system_prompt=self.COMPILER_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                max_tokens=4096
            )
            clean = response_text.strip()
            if clean.startswith("```"):
                clean = re.sub(r"^```[a-zA-Z0-9_-]*\n?", "", clean)
                clean = re.sub(r"\n?```$", "", clean).strip()
            data = json.loads(clean)
        except Exception as e:
            print(f"[SpecCompilerService] LLM compile failed: {e}. Using deterministic fallback.")
            data = self._fallback_compilation(target_name, title, seed_hash, hard_invariants, selected_vector)

        # 6-Slot Danbooru 태그 자동 조립
        v_dna_dict = data.get("visual_dna", {})
        visual_dna = VisualDNA.from_dict(v_dna_dict)
        pos_tag, neg_tag = VisualCompiler.compile_danbooru_prompt(target_name, visual_dna)
        data["danbooru_prompt"] = {
            "positive": pos_tag,
            "negative": neg_tag
        }

        return data

    def _fallback_compilation(self, target_name: str, title: str, seed_hash: str, hard_invariants: List[str], selected_vector: Dict[str, Any]) -> Dict[str, Any]:
        """LLM 오프라인 시 결정론적 기본 컴파일"""
        v_dna = {
            "skeletal": f"슬림하고 우아한 골격, 167cm, {selected_vector.get('vector_name', '정통파')}",
            "ocular": "서늘한 백금빛 금안, 좁혀진 동공",
            "hair": "허리까지 단정히 내려오는 은발 스트레이트",
            "somatic": "선명한 쇄골 라인과 균형 잡힌 신체 비율",
            "dermal": "서늘하고 창백한 도자기 피부",
            "apparel": "단단한 은제 초커와 오프숄더 제복 드레스",
            "blush": "동요 시 뺨과 쇄골에 스며드는 은은한 홍조",
            "lighting": "차가운 달빛과 짙은 음영의 대비"
        }

        genes = {f"gene_{i:02d}": f"차원축 70단계 유전자 {i}번 발현 상태" for i in range(1, 71)}
        tensors = {f"tensor_{i:02d}": f"17대 생체·의복 텐서 {i}번 매핑" for i in range(1, 18)}

        traits = {
            "archetype_class": f"Rigid ({target_name})",
            "stage_progression": "Stage 1 (초기 경계)",
            "gauges": {"trust": 20, "eroticism": 0, "shame": -30, "guilt": 15, "submission": 20},
            "traits_list": [
                {"category": "신체/의복", "details": v_dna["apparel"]},
                {"category": "결핍/서약", "details": hard_invariants[0] if hard_invariants else "불변의 가문 명예"},
                {"category": "감각/반사", "details": "접촉 시 신체 긴장 및 척추 경직"}
            ]
        }

        return {
            "visual_dna": v_dna,
            "tensors_17": tensors,
            "genes_70": genes,
            "traits": traits
        }
