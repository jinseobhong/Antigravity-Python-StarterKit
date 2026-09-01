# -*- coding: utf-8 -*-
"""
src/domain/character.py
~~~~~~~~~~~~~~~~~~~~~~~
Domain Layer: Character 애그리게이트 루트 모델
- GeneSeed, VisualDNA, PersonalityGene, CharacterTraits, SomaticLedger, SpatialPressure 완전 결합
- 4대 대표 아키타입(릴리스, 에이라, 세라피나, 실비아) 실물 팩토리 수록
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from src.models.gene_seed import GeneSeed
from src.models.visual_dna import VisualDNA
from src.models.personality_gene import PersonalityGene, HardInvariants
from src.models.character_traits import CharacterTraits, PsychologicalGauges, SomaticMetrics
from src.models.somatic_ledger import SomaticLedger
from src.models.spatial_pressure import SpatialPressure


@dataclass
class Character:
    """Character 애그리게이트 루트"""
    id: Optional[int]
    name: str
    title: str
    gene_seed: GeneSeed
    visual_dna: VisualDNA
    personality_gene: PersonalityGene
    traits: CharacterTraits
    somatic_ledger: SomaticLedger
    spatial_pressure: SpatialPressure
    portrait_url: str = ""
    is_active: bool = False

    @property
    def seed_hash(self) -> str:
        return self.gene_seed.seed_hash

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "seed_hash": self.gene_seed.seed_hash,
            "visual_dna": self.visual_dna.to_dict(),
            "personality_gene": self.personality_gene.to_dict(),
            "traits": self.traits.to_dict(),
            "somatic_ledger": self.somatic_ledger.to_dict(),
            "spatial_pressure": self.spatial_pressure.to_dict(),
            "portrait_url": self.portrait_url,
            "is_active": self.is_active
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Character:
        seed_obj = GeneSeed.from_input(data.get("name", "무명"), data.get("seed_hash", ""))
        v_dna = VisualDNA.from_dict(data.get("visual_dna", {}))
        p_gene = PersonalityGene.from_dict(data.get("personality_gene", {}))
        traits_obj = CharacterTraits.from_dict(data.get("traits", {}))
        ledger_obj = SomaticLedger.from_dict(data.get("somatic_ledger", {}))
        
        sp_data = data.get("spatial_pressure", {})
        sp_obj = SpatialPressure.create(
            layer=sp_data.get("layer_level", 1),
            location=sp_data.get("location_name", "침실")
        )

        return cls(
            id=data.get("id"),
            name=data.get("name", "릴리스"),
            title=data.get("title", "제1황녀"),
            gene_seed=seed_obj,
            visual_dna=v_dna,
            personality_gene=p_gene,
            traits=traits_obj,
            somatic_ledger=ledger_obj,
            spatial_pressure=sp_obj,
            portrait_url=data.get("portrait_url", ""),
            is_active=bool(data.get("is_active", False))
        )

    # -------------------------------------------------------------
    # 4대 대표 실물 아키타입 팩토리
    # -------------------------------------------------------------
    @classmethod
    def create_lilith(cls) -> Character:
        """[Rigid] 릴리스 — 제1황녀 • 제국 황실 (#LILI-70G-BFFF)"""
        seed = GeneSeed.from_input("릴리스", "#LILI-70G-BFFF")
        v_dna = VisualDNA(
            face_geometry="차가운 오만함을 두른 날렵한 V-line 턱선, 굳게 다문 얇고 창백한 입술",
            ocular_optics="깊이를 알 수 없는 서늘한 금빛 홍채와 짙은 호박색 림, 긴 속눈썹",
            hair_physics="허리 아래까지 단정하게 흘러내리는 백은색 스트레이트 직모, 뺨을 스치는 옆머리",
            body_silhouette="168cm의 호리호리하고 유려한 실루엣, 꼿꼿한 척추와 깊게 도드라진 쇄골 패임",
            dermal_texture="햇빛을 거의 보지 않은 투명할 정도로 창백한 백옥 피부, 목덜미의 푸른 핏줄",
            apparel_accents="어깨와 쇄골이 드러난 흑색 실크 오프숄더 드레스, 목을 빈틈없이 감싼 차가운 은색 금속 초커",
            somatic_flush_cue="극도의 수치와 긴장 시 쇄골 패임과 귓바퀴를 타고 붉게 타오르는 홍조",
            lighting_contrast="차가운 달빛과 어두운 밀실의 짙은 명암 대비",
            danbooru_prompt="lilith, masterpiece, best quality, 1girl, solo, silver_hair, very_long_hair, straight_hair, golden_eyes, amber_eyes, black_dress, off-shoulder, collarbone, silver_choker, pale_skin, blushing, dramatic_lighting, dark_fantasy",
            negative_prompt="lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry"
        )
        inv = HardInvariants(
            primary_boundary="선조 가문의 막대한 부채와 순결 서약의 도덕적 결벽증",
            ego_collapse_trigger="목에 채워진 금속 초커를 쥔 채 시선을 강제로 고정당하는 순간",
            somatic_achilles_heel="도드라진 쇄골 패임에 닿는 타인의 묵직하고 뜨거운 체온"
        )
        p_gene = PersonalityGene(
            hard_invariants=inv,
            axis_1_physical_reflex="목덜미와 초커에 손길이 닿을 때 척추가 반사적으로 굳어지며 얕아지는 호흡",
            axis_2_neuro_memory="타락과 쾌락에 대한 공포로 인해 심박이 급격히 상승하며 쇄골이 미세하게 떨림",
            axis_3_social_deficit="가문의 멸망을 막기 위해 모든 인간적 욕망을 거세당한 채 자라난 깊은 고립감",
            axis_4_cognitive_distortion="누군가에게 무조건적인 호의를 받거나 지배당하는 것은 곧 영혼의 파멸이라는 신념",
            axis_5_shadow_ego="자신의 모든 긍지와 제약선을 산산조각 내어줄 절대적 지배자에게 짐을 넘기고 복종하고 싶은 갈망",
            axis_6_alchemy_submission="체온이 깊게 침투할수록 오만하던 눈빛이 풀리며 척수에서부터 무너져 내리는 굴종",
            axis_7_gesture_ticks=["동요를 숨기려 턱을 치켜올리기", "무의식중에 초커 가장자리를 만지작거리기", "시선을 차갑게 내리깔기"]
        )
        traits = CharacterTraits(
            archetype_title="제1황녀 • 제국 황실",
            archetype_class="Rigid (결벽주의 척추 방어)",
            stage_progression="Stage 1 (침실 개방 - 포섭된 요새와 결벽)",
            gauges=PsychologicalGauges(trust=20, eroticism=0, shame=-30, guilt=15, submission=20),
            somatic_metrics=SomaticMetrics(odo="54.2%", taint="7.1%"),
            traits_list=[
                {"category": "외모 & 체형", "details": "차가운 은발과 서늘한 금빛 동공, 목에 채워진 서늘한 금속 초커"},
                {"category": "핵심 결핍 & 트라우마", "details": "선조 가문의 막대한 부채와 순결 서약의 도덕적 결벽증"},
                {"category": "은밀한 비밀 & 약점", "details": "가문의 비밀 금고 열쇠를 소유하고 있으며 체온에 극도로 취약함"}
            ]
        )
        ledger = SomaticLedger(
            layer_1_reflex="목덜미의 서늘한 금속 초커 사이로 경직된 척추의 영구 방어 기제가 역력함.",
            layer_2_buffer="귓바퀴와 쇄골로 서서히 번지는 붉은 열감, 헐떡이는 호흡의 미세한 흐트러짐.",
            layer_3_archive="나의 긍지와 위엄은 너의 손길 따위에 흔들리지 않는다는 내적 독백의 균열."
        )
        sp = SpatialPressure.create(1, "황녀의 사적 집무실")
        return cls(
            id=None,
            name="릴리스",
            title="제1황녀",
            gene_seed=seed,
            visual_dna=v_dna,
            personality_gene=p_gene,
            traits=traits,
            somatic_ledger=ledger,
            spatial_pressure=sp,
            portrait_url="",
            is_active=True
        )

    @classmethod
    def create_aira(cls) -> Character:
        """[Endurer] 에이라 — 백은의 성기사단장 (#AIRA-70G-9A4F)"""
        seed = GeneSeed.from_input("에이라", "#AIRA-70G-9A4F")
        v_dna = VisualDNA(
            face_geometry="단호하고 금욕적인 턱선, 결의에 찬 굳건한 입매",
            ocular_optics="푸른 바다처럼 투명하고 흔들림 없는 벽안",
            hair_physics="어깨선에 닿는 깔끔한 백금발 단발머리",
            body_silhouette="172cm의 탄탄하게 단련된 기사 체형, 굳은 등근육과 기립근",
            dermal_texture="전투의 잔상인 미세한 흉터와 단단한 살결",
            apparel_accents="은빛 흉갑과 검은 가죽 갑주, 목을 감싼 성스러운 결속 인장",
            somatic_flush_cue="갑주 해제 시 목덜미에서 등줄기로 이어지는 깊은 열기",
            lighting_contrast="성스러운 은빛 광원과 그림자의 대비",
            danbooru_prompt="aira, masterpiece, best quality, 1girl, solo, short_hair, platinum_blonde_hair, blue_eyes, armor, breastplate, muscular_female, athletic, dark_fantasy",
            negative_prompt="lowres, bad anatomy, bad hands, text, blurry"
        )
        inv = HardInvariants(
            primary_boundary="교단에 바친 평생의 금욕과 기사도 서약",
            ego_collapse_trigger="갑주가 하나씩 해제되며 맨살이 공기에 노출되는 순간",
            somatic_achilles_heel="견갑골 사이 척추 라인에 닿는 손길"
        )
        p_gene = PersonalityGene(
            hard_invariants=inv,
            axis_1_physical_reflex="갑주를 벗길 때 이빨을 깨물며 신체 경직",
            axis_2_neuro_memory="절대 굴복하지 않겠다는 결의와 이에 반하는 신체적 고조",
            axis_3_social_deficit="평생 훈련과 규율 외에는 타인의 애정을 받아보지 못한 결핍",
            axis_4_cognitive_distortion="쾌락을 느끼는 것은 신에 대한 배신이라는 죄책감",
            axis_5_shadow_ego="강한 전사가 아닌 한 명의 암컷으로서 완전히 꺾이고 싶은 충동",
            axis_6_alchemy_submission="기사도의 한계를 넘어서는 소마틱 종속",
            axis_7_gesture_ticks=["검자루를 꽉 쥐기", "턱을 당겨 시선 정면 고정", "거친 숨 몰아쉬기"]
        )
        traits = CharacterTraits(
            archetype_title="백은의 성기사단장",
            archetype_class="Endurer (성직자형 금욕 인내)",
            stage_progression="Stage 1 (성소 대치 - 단련된 갑주와 계율)",
            gauges=PsychologicalGauges(trust=15, eroticism=0, shame=-40, guilt=30, submission=10),
            somatic_metrics=SomaticMetrics(odo="68.0%", taint="3.2%"),
            traits_list=[
                {"category": "외모 & 체형", "details": "백금발 단발, 투명한 벽안, 은빛 흉갑과 단련된 기립근"},
                {"category": "핵심 결핍 & 트라우마", "details": "교단의 엄격한 계율과 금욕 서약에 갇힌 영혼"},
                {"category": "은밀한 비밀 & 약점", "details": "갑주가 해제되었을 때 맨살의 감각에 극도로 취약함"}
            ]
        )
        ledger = SomaticLedger(
            layer_1_reflex="흉갑 아래로 거칠게 들썩이는 늑골과 굳게 다문 입술.",
            layer_2_buffer="갑주 틈새로 새어나오는 뜨거운 체온과 목덜미의 식은땀.",
            layer_3_archive="기사로서의 맹세가 침입자의 손길 앞에서 흔들리고 있다는 죄책감."
        )
        sp = SpatialPressure.create(1, "기사단장 개인 기도실")
        return cls(
            id=None,
            name="에이라",
            title="성기사단장",
            gene_seed=seed,
            visual_dna=v_dna,
            personality_gene=p_gene,
            traits=traits,
            somatic_ledger=ledger,
            spatial_pressure=sp,
            portrait_url="",
            is_active=False
        )

    @classmethod
    def create_seraphina(cls) -> Character:
        """[Controller] 세라피나 — 심연의 대마도사 (#SERA-70G-1C3D)"""
        seed = GeneSeed.from_input("세라피나", "#SERA-70G-1C3D")
        v_dna = VisualDNA(
            face_geometry="요염하고 매혹적인 입꼬리, 오만한 눈매",
            ocular_optics="마력으로 은은하게 빛나는 자수정빛 자안",
            hair_physics="물결치듯 흐르는 흑자색의 긴 웨이브 헤어",
            body_silhouette="165cm의 굴곡진 관능적 바디라인, 가느다란 허리",
            dermal_texture="부드러운 실크 같은 살결, 손목의 마법 각인",
            apparel_accents="반투명한 벨벳 로브, 가슴골을 드러낸 코르셋 드레스",
            somatic_flush_cue="마력 공명 시 피부 표면에 떠오르는 보랏빛 문양",
            lighting_contrast="신비로운 보랏빛 마력광과 짙은 어둠",
            danbooru_prompt="seraphina, masterpiece, best quality, 1girl, solo, long_hair, wavy_hair, purple_hair, purple_eyes, corset, velvet_robe, cleavage, dark_fantasy",
            negative_prompt="lowres, bad anatomy, bad hands, text, blurry"
        )
        inv = HardInvariants(
            primary_boundary="모든 상황을 지배하고 통제해야 한다는 지적 오만함",
            ego_collapse_trigger="자신의 마법이나 계략이 완전히 무력화되고 역으로 구속당할 때",
            somatic_achilles_heel="허리 양옆의 얇은 늑골선과 골반 라인"
        )
        p_gene = PersonalityGene(
            hard_invariants=inv,
            axis_1_physical_reflex="역으로 제압당할 때 혀를 차며 발버둥치는 예민한 반응",
            axis_2_neuro_memory="상대를 조롱하다가도 숨결이 닿으면 급격히 흐트러지는 호흡",
            axis_3_social_deficit="타인을 도구로만 대하며 진정한 유대를 맺어보지 못한 고독",
            axis_4_cognitive_distortion="지배하지 못하면 지배당한다는 극단적 권력관",
            axis_5_shadow_ego="자신의 모든 마법과 오만을 꺾어줄 압도적인 포식자 앞에서의 전율",
            axis_6_alchemy_submission="지배자에서 피지배자로 뒤바뀌는 쾌감의 역전",
            axis_7_gesture_ticks=["부채로 입술 가리기", "상대를 위아래로 훑어보기", "도발적인 콧웃음"]
        )
        traits = CharacterTraits(
            archetype_title="심연의 대마도사",
            archetype_class="Controller (오만한 지배/역전)",
            stage_progression="Stage 1 (탑의 밀실 - 보랏빛 결계와 도발)",
            gauges=PsychologicalGauges(trust=10, eroticism=20, shame=-20, guilt=5, submission=5),
            somatic_metrics=SomaticMetrics(odo="42.5%", taint="18.9%"),
            traits_list=[
                {"category": "외모 & 체형", "details": "흑자색 웨이브 헤어, 자수정빛 눈동자, 관능적 코르셋 로브"},
                {"category": "핵심 결핍 & 트라우마", "details": "타인을 신뢰하지 못하고 지배로만 안전을 느끼는 결핍"},
                {"category": "은밀한 비밀 & 약점", "details": "마력 흐름이 끊겼을 때 신체 감각이 수십 배로 예민해짐"}
            ]
        )
        ledger = SomaticLedger(
            layer_1_reflex="도발적인 미소 뒤로 미세하게 떨리는 손가락 끝의 마력선.",
            layer_2_buffer="골반을 감싸 쥔 손길에 척추를 타고 오르는 찌릿한 전율.",
            layer_3_archive="내가 이 자를 시험하는 것인가, 시험당하는 것인가에 대한 혼란."
        )
        sp = SpatialPressure.create(1, "마탑 최상층 마법 연구실")
        return cls(
            id=None,
            name="세라피나",
            title="대마도사",
            gene_seed=seed,
            visual_dna=v_dna,
            personality_gene=p_gene,
            traits=traits,
            somatic_ledger=ledger,
            spatial_pressure=sp,
            portrait_url="",
            is_active=False
        )

    @classmethod
    def create_sylvia(cls) -> Character:
        """[Deprived] 실비아 — 몰락 귀족의 영애 (#SILV-70G-77E2)"""
        seed = GeneSeed.from_input("실비아", "#SILV-70G-77E2")
        v_dna = VisualDNA(
            face_geometry="가련하고 유약한 턱선, 눈물에 젖기 쉬운 촉촉한 입술",
            ocular_optics="불안하게 흔들리는 커다란 루비빛 적안",
            hair_physics="가슴까지 내려오는 부드러운 핑크빛 블론드 헤어",
            body_silhouette="158cm의 아담하고 보호 본능을 자극하는 연약한 체구",
            dermal_texture="상처 입기 쉬운 부드럽고 얇은 피부",
            apparel_accents="해진 레이스가 달린 낡은 귀족 드레스, 손목에 감긴 붉은 리본",
            somatic_flush_cue="작은 접촉에도 온몸이 붉게 달아오르는 과민 반응",
            lighting_contrast="희미한 촛불빛과 서글픈 어둠",
            danbooru_prompt="sylvia, masterpiece, best quality, 1girl, solo, pink_hair, long_hair, red_eyes, crying, frills, dress, fragile, dark_fantasy",
            negative_prompt="lowres, bad anatomy, bad hands, text, blurry"
        )
        inv = HardInvariants(
            primary_boundary="버림받는 것에 대한 극도의 유기 불안과 공포",
            ego_collapse_trigger="따뜻한 포옹과 동시에 절대 버리지 않겠다는 밀어의 속삭임",
            somatic_achilles_heel="귓바퀴와 목덜미로 이어지는 연약한 살결"
        )
        p_gene = PersonalityGene(
            hard_invariants=inv,
            axis_1_physical_reflex="손길이 닿을 때마다 소스라치게 놀라며 몸을 움츠림",
            axis_2_neuro_memory="체온이 멀어지면 극심한 불안과 패닉 상태에 빠짐",
            axis_3_social_deficit="가문의 몰락과 배신으로 인한 심각한 애정 결핍",
            axis_4_cognitive_distortion="쓸모가 없어지면 언제든 버려질 것이라는 절망",
            axis_5_shadow_ego="자신을 완전히 소유하고 영원히 가두어주길 바라는 의존증",
            axis_6_alchemy_submission="버림받지 않기 위해 무엇이든 바치려는 맹목적 순종",
            axis_7_gesture_ticks=["치맛자락을 불안하게 쥐기", "눈치를 보며 고개 숙이기", "상대의 옷소매 붙잡기"]
        )
        traits = CharacterTraits(
            archetype_title="몰락 귀족의 영애",
            archetype_class="Deprived (가련한 유기 불안)",
            stage_progression="Stage 1 (버려진 저택 - 흔들리는 촛불과 눈물)",
            gauges=PsychologicalGauges(trust=35, eroticism=10, shame=-10, guilt=20, submission=40),
            somatic_metrics=SomaticMetrics(odo="60.1%", taint="12.4%"),
            traits_list=[
                {"category": "외모 & 체형", "details": "핑크 블론드, 젖은 루비색 눈동자, 레이스 드레스와 아담한 체구"},
                {"category": "핵심 결핍 & 트라우마", "details": "가문 몰락 후 모두에게 버려졌던 극심한 유기 불안"},
                {"category": "은밀한 비밀 & 약점", "details": "다정한 온기와 칭찬 한마디에 모든 방어선이 무너짐"}
            ]
        )
        ledger = SomaticLedger(
            layer_1_reflex="손끝이 닿자마자 파르르 떨리며 감기는 눈꺼풀.",
            layer_2_buffer="체온이 스며든 뺨에서 식지 않는 뜨거운 눈물 자국.",
            layer_3_archive="제발 나를 버리지 말아달라는 무언의 애원과 종속."
        )
        sp = SpatialPressure.create(1, "몰락한 가문의 먼지 쌓인 침실")
        return cls(
            id=None,
            name="실비아",
            title="몰락 영애",
            gene_seed=seed,
            visual_dna=v_dna,
            personality_gene=p_gene,
            traits=traits,
            somatic_ledger=ledger,
            spatial_pressure=sp,
            portrait_url="",
            is_active=False
        )
