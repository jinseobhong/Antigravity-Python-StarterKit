# -*- coding: utf-8 -*-
"""
src/application/gene_synthesis_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[Dify Node 17881238650450: CONCRETE IMPLEMENTATION & GENE SYNTHESIZER]
- 승인된 제약선과 서사 궤적으로부터 8-Tier Visual DNA & 70-Step Personality Genes 동적 합성
- 4대 대표 아키타입(릴리스, 에이라, 세라피나, 실비아) 기본 템플릿 내장
"""

from __future__ import annotations
import json
import re
from typing import Dict, Any, Optional

from src.domain.character import Character
from src.domain.gene_seed import GeneSeed
from src.domain.visual_dna import VisualDNA
from src.domain.personality_gene import PersonalityGene, HardInvariants
from src.infrastructure.llm.client import MultiLLMClient
from src.infrastructure.media.visual_compiler import VisualCompiler
from src.infrastructure.database.repositories import CharacterRepository


class GeneSynthesisService:
    """8-Tier Visual DNA & 70단계 유전자 동적 합성 서비스"""

    def __init__(self, char_repo: CharacterRepository, llm_client: MultiLLMClient):
        self.char_repo = char_repo
        self.llm = llm_client
        self._seed_default_archetypes()

    def synthesize_character(self, name: str, title: str, faction: str, hard_invariants_dict: dict, selected_vector: dict, explicit_seed: str = "") -> Character:
        """LLM을 통해 제약선으로부터 8중 외모와 70단계 유전자를 1:1 인과 사슬로 합성"""
        seed = GeneSeed.from_input(name, explicit_seed=explicit_seed)

        system_instruction = """[SYSTEM DIRECTIVE: 8-TIER VISUAL DNA & 70-STEP GENE COMPILER]
당신은 확정된 제약선(Hard Invariants)과 서사 궤적으로부터 캐릭터의 [8-Tier Visual DNA]와 [7-Axis Personality DNA]를 완벽히 인과적으로 역산하는 수석 아키텍트다.
제약선(트라우마/결벽증)이 왜 이 외모(초커, 쇄골, 눈빛)와 신체 반응으로 발현되는지 1:1로 엮어라.

반드시 다음 JSON 포맷으로만 응답하라:
{
  "visual_dna": {
    "face_geometry": "서늘하고 날렵한 턱선, 굳게 다문 얇고 창백한 입술",
    "ocular_optics": "금빛 홍채 주변에 짙은 호박색 림, 길고 촘촘한 은빛 속눈썹",
    "hair_physics": "허리까지 내려오는 백은색 직모, 뺨을 타고 흐르는 단정한 옆머리",
    "body_silhouette": "168cm 호리호리한 체형, 도드라진 쇄골 패임과 꼿꼿한 척추",
    "dermal_texture": "창백한 백옥 피부, 목덜미에 비치는 미세한 푸른 핏줄",
    "apparel_accents": "어깨가 드러난 검은 실크 오프숄더 드레스, 차가운 은색 금속 초커",
    "somatic_flush_cue": "수치/당황 시 귓바퀴와 쇄골을 타고 번지는 붉은 열감",
    "lighting_contrast": "차가운 달빛 아래 반투명한 피부와 짙은 그림자"
  },
  "personality_dna": {
    "axis_1_physical_reflex": "목덜미 접촉 시 척추가 경직되는 방어 반사",
    "axis_2_neuro_memory": "호흡을 억누르는 흉곽 경련과 얕은 호흡",
    "axis_3_social_deficit": "가문의 부채로 인한 강박적 순결 의무감",
    "axis_4_cognitive_distortion": "자신의 취약성을 드러내는 것은 곧 파멸이라는 신념",
    "axis_5_shadow_ego": "타인에게 완전히 통제받고 짐을 내려놓고 싶은 무의식적 갈망",
    "axis_6_alchemy_submission": "체온 밀착 시 무너지는 방어선",
    "axis_7_gesture_ticks": ["눈을 가늘게 뜨며 시선 회피", "당황 시 초커 가장자리를 손끝으로 쓸어내림"]
  }
}"""
        user_prompt = f"""[대상 캐릭터]: {name} ({title} • {faction})
[불변 제약선]: {json.dumps(hard_invariants_dict, ensure_ascii=False)}
[선택된 서사 궤적]: {json.dumps(selected_vector, ensure_ascii=False)}

위 정보를 바탕으로, 인과관계가 완벽히 결합된 8-Tier Visual DNA 및 7-Axis Personality DNA JSON을 합성하라."""

        resp = self.llm.generate_text(system_instruction, user_prompt)
        try:
            m = re.search(r'\{[\s\S]*\}', resp)
            data = json.loads(m.group(0)) if m else {}
        except Exception:
            data = {}

        v_data = data.get("visual_dna", {})
        p_data = data.get("personality_dna", {})
        p_data["hard_invariants"] = hard_invariants_dict

        v_dna = VisualDNA.from_dict(v_data)
        p_gene = PersonalityGene.from_dict(p_data)

        char = Character(
            gene_seed=seed,
            name=name,
            title=title,
            faction=faction,
            visual_dna=v_dna,
            personality_gene=p_gene
        )
        pos_tag, neg_tag = VisualCompiler.compile_danbooru_pair(char)
        char.visual_dna.danbooru_prompt = pos_tag
        char.visual_dna.negative_prompt = neg_tag

        self.char_repo.save(char)
        return char

    def _seed_default_archetypes(self) -> None:
        """4대 대표 아키타입(릴리스, 에이라, 세라피나, 실비아) 자동 시딩"""
        existing = self.char_repo.list_all()
        if existing:
            return

        # 1. 릴리스 (제1황녀)
        char_1 = Character.create_archetype(
            name="릴리스",
            title="제1황녀",
            faction="제국 황실",
            explicit_seed="#LILI-70G-BFFF",
            visual_dict={
                "face_geometry": "서늘하고 날렵한 v-line 턱선, 굳게 다문 얇고 창백한 입술",
                "ocular_optics": "금빛 홍채 주변에 짙은 호박색 림, 길고 촘촘한 은빛 속눈썹",
                "hair_physics": "허리까지 내려오는 백은색 직모, 뺨을 타고 흐르는 단정한 옆머리",
                "body_silhouette": "168cm 호리호리한 체형, 도드라진 쇄골 패임과 꼿꼿한 척추",
                "dermal_texture": "창백한 백옥 피부, 목덜미에 비치는 미세한 푸른 핏줄",
                "apparel_accents": "어깨가 드러난 검은 실크 오프숄더 드레스, 차가운 은색 금속 초커",
                "somatic_flush_cue": "수치/당황 시 귓바퀴와 쇄골을 타고 번지는 붉은 열감",
                "lighting_contrast": "차가운 달빛 아래 반투명한 피부와 짙은 그림자"
            },
            gene_dict={
                "hard_invariants": {
                    "primary_boundary": "선조 가문의 막대한 부채와 순결 서약의 도덕적 결벽증",
                    "ego_collapse_trigger": "목덜미 초커를 쥐고 강제로 시선을 맞출 때",
                    "somatic_achilles_heel": "쇄골 패임의 직접적 체온 접촉"
                },
                "axis_1_physical_reflex": "목덜미 접촉 시 척추가 경직되는 방어 반사",
                "axis_2_neuro_memory": "호흡을 억누르는 흉곽 경련과 얕은 호흡",
                "axis_3_social_deficit": "가문의 부채로 인한 강박적 순결 의무감",
                "axis_4_cognitive_distortion": "자신의 취약성을 드러내는 것은 곧 파멸이라는 신념",
                "axis_5_shadow_ego": "타인에게 완전히 통제받고 짐을 내려놓고 싶은 무의식적 갈망",
                "axis_6_alchemy_submission": "체온 밀착 시 무너지는 방어선",
                "axis_7_gesture_ticks": ["눈을 가늘게 뜨며 시선 회피", "당황 시 초커 가장자리를 손끝으로 쓸어내림"]
            }
        )
        pos, neg = VisualCompiler.compile_danbooru_pair(char_1)
        char_1.visual_dna.danbooru_prompt = pos
        char_1.visual_dna.negative_prompt = neg
        self.char_repo.save(char_1)

        # 2. 에이라 (성기사단장)
        char_2 = Character.create_archetype(
            name="에이라",
            title="백은의 성기사단장",
            faction="성교단",
            explicit_seed="#AIRA-70G-9A4F",
            visual_dict={
                "face_geometry": "단아하고 결의에 찬 턱선, 결벽적으로 정돈된 입술",
                "ocular_optics": "청명하고 시린 청안, 흔들리지 않는 굳건한 시선",
                "hair_physics": "단정하게 땋아 올린 백금발, 땀에 젖어 이마에 붙은 잔머리",
                "body_silhouette": "172cm 탄탄하고 우아한 기사의 신체, 백은의 흉갑",
                "dermal_texture": "햇빛에 가볍게 그을린 건강한 피부, 훈련으로 단련된 손끝",
                "apparel_accents": "백은의 정밀 흉갑, 목을 보호하는 가죽 고지트",
                "somatic_flush_cue": "갑주가 벗겨질 때 쇄골과 목덜미에 차오르는 극심한 수치심과 열감",
                "lighting_contrast": "성스러운 대성당 스테인드글라스 빛과 갑주의 금속 반사"
            },
            gene_dict={
                "hard_invariants": {
                    "primary_boundary": "성교단에 바친 절대적 정결과 인내의 서약",
                    "ego_collapse_trigger": "흉갑이 해체되고 맨살의 온기가 맞닿을 때",
                    "somatic_achilles_heel": "흉곽 중심부와 등골 라인"
                },
                "axis_1_physical_reflex": "신체 접촉 시 방어 본능으로 흉근 수축",
                "axis_2_neuro_memory": "금욕 훈련으로 인한 감각 억압의 잔향",
                "axis_3_social_deficit": "기사단장이라는 무거운 책임감과 접촉 갈망",
                "axis_4_cognitive_distortion": "쾌락이나 안식을 바라는 것은 죄악이라는 강박",
                "axis_5_shadow_ego": "어떤 방어도 할 수 없는 무력한 상태로 안기고 싶은 갈망",
                "axis_6_alchemy_submission": "갑주 해체 후 온기 전달 시 척수 전면 이완",
                "axis_7_gesture_ticks": ["입술을 깨물며 신음 억제", "주먹을 꽉 쥐며 떨림 방어"]
            }
        )
        pos2, neg2 = VisualCompiler.compile_danbooru_pair(char_2)
        char_2.visual_dna.danbooru_prompt = pos2
        char_2.visual_dna.negative_prompt = neg2
        self.char_repo.save(char_2)

        # 3. 세라피나 (심연의 대마도사)
        char_3 = Character.create_archetype(
            name="세라피나",
            title="심연의 대마도사",
            faction="비전 마탑",
            explicit_seed="#SERA-70G-3C2D",
            visual_dict={
                "face_geometry": "매혹적이고 요염한 갸름한 턱선, 오만한 미소를 머금은 입술",
                "ocular_optics": "자줏빛 마력으로 빛나는 신비로운 눈동자, 짙은 속눈썹",
                "hair_physics": "풍성한 자줏빛 웨이브 머리, 어깨를 감싸는 탐스러운 컬",
                "body_silhouette": "165cm 굴곡진 관능적 체형, 깊게 파인 벨벳 로브",
                "dermal_texture": "부드럽고 촉촉한 피부, 마법 문양이 미세하게 박힌 목덜미",
                "apparel_accents": "심연의 흑자색 벨벳 로브, 마력 억제 보석 초커",
                "somatic_flush_cue": "마력 과열 시 전신 피부에 번지는 붉은 마력 회로와 헐떡임",
                "lighting_contrast": "보랏빛 마력 불꽃과 어둠 속의 극적인 명암"
            },
            gene_dict={
                "hard_invariants": {
                    "primary_boundary": "타인을 완벽히 통제하고 지배해야 한다는 절대적 우월감",
                    "ego_collapse_trigger": "자신의 마력 회로가 역류하여 신체 통제권을 잃을 때",
                    "somatic_achilles_heel": "목덜미 마력 코어 룬 각인 부위"
                },
                "axis_1_physical_reflex": "마력 자극 시 신경망 전신 진동",
                "axis_2_neuro_memory": "마탑에서의 실험으로 과민해진 신경 감각",
                "axis_3_social_deficit": "아무도 믿지 못하는 고립감과 배신에 대한 공포",
                "axis_4_cognitive_distortion": "지배하지 못하면 지배당해 이용당한다는 불신",
                "axis_5_shadow_ego": "모든 통제를 빼앗기고 완벽히 굴복당하고 싶은 피학적 충동",
                "axis_6_alchemy_submission": "마력 코어 압박 시 무조건적 복종 모드 전이",
                "axis_7_gesture_ticks": ["오만하게 손가락 튕기기", "마력 불안정 시 관자놀이 짚기"]
            }
        )
        pos3, neg3 = VisualCompiler.compile_danbooru_pair(char_3)
        char_3.visual_dna.danbooru_prompt = pos3
        char_3.visual_dna.negative_prompt = neg3
        self.char_repo.save(char_3)

        # 4. 실비아 (몰락 귀족 영애)
        char_4 = Character.create_archetype(
            name="실비아",
            title="몰락 귀족 영애",
            faction="구 제국 귀족",
            explicit_seed="#SILV-70G-77E2",
            visual_dict={
                "face_geometry": "가련하고 앳된 달걀형 얼굴, 촉촉하게 젖은 도톰한 입술",
                "ocular_optics": "버림받을까 두려워하는 큰 흑요석 눈망울, 촉촉한 눈가",
                "hair_physics": "어깨를 살짝 덮는 부드러운 흑발 단발, 바람에 흩날리는 잔머리",
                "body_silhouette": "158cm 왜소하고 가냘픈 체형, 부서질 듯 연약한 쇄골",
                "dermal_texture": "부드럽고 얇은 피부, 체온에 민감하게 반응하는 살결",
                "apparel_accents": "약간 낡았지만 단정한 프릴 레이스 드레스, 낡은 리본 초커",
                "somatic_flush_cue": "작은 손길에도 뺨 전체와 목덜미가 새빨갛게 물드는 극도의 체온 반응",
                "lighting_contrast": "희미한 촛불 아래 드러나는 가녀린 실루엣"
            },
            gene_dict={
                "hard_invariants": {
                    "primary_boundary": "버림받지 않기 위해 필사적으로 순종하고 매달리는 애착 방어",
                    "ego_collapse_trigger": "부드럽게 뺨을 감싸며 절대 버리지 않는다고 속삭일 때",
                    "somatic_achilles_heel": "손끝과 목덜미 리본 부위"
                },
                "axis_1_physical_reflex": "작은 온기에도 자석처럼 끌려가는 신체 반사",
                "axis_2_neuro_memory": "차가운 감옥에 방치되었던 추위의 신체 기억",
                "axis_3_social_deficit": "가문 몰락 후 겪은 유기 불안과 절대적 결핍",
                "axis_4_cognitive_distortion": "자신은 온기를 구걸해야만 살아남을 수 있다는 절박함",
                "axis_5_shadow_ego": "온전히 상대방의 소유물이 되어 구속되고 싶은 의존 갈망",
                "axis_6_alchemy_submission": "포옹 및 체온 전달 시 눈물 흘리며 전면 굴복",
                "axis_7_gesture_ticks": ["상대방의 옷자락을 꼭 쥐는 틱", "시선을 위로 올려다보는 버릇"]
            }
        )
        pos4, neg4 = VisualCompiler.compile_danbooru_pair(char_4)
        char_4.visual_dna.danbooru_prompt = pos4
        char_4.visual_dna.negative_prompt = neg4
        self.char_repo.save(char_4)
