# -*- coding: utf-8 -*-
"""
tests/unit/domain/test_domain_models.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Domain Layer 단위 테스트
- GeneSeed, VisualDNA, PersonalityGene, SomaticLedger, SpatialPressureChamber, KinematicChainState
"""

import unittest
from src.domain.gene_seed import GeneSeed
from src.domain.visual_dna import VisualDNA
from src.domain.personality_gene import PersonalityGene, HardInvariants
from src.domain.somatic_ledger import SomaticLedger
from src.domain.spatial_pressure import SpatialPressureChamber, SpatialLayer
from src.domain.kinematic_chain import KinematicChainState
from src.domain.character import Character


class TestDomainModels(unittest.TestCase):

    def test_gene_seed_generation_and_anchoring(self):
        """GeneSeed 해시 생성 및 앵커링 검증"""
        seed_1 = GeneSeed.from_input("릴리스")
        self.assertTrue(seed_1.seed_hash.startswith("#LILI-70G-"))
        self.assertEqual(len(seed_1.entropy_hex), 4)

        # 명시적 시드 주입 시 그대로 유지 검증
        seed_2 = GeneSeed.from_input("릴리스", explicit_seed="#LILI-70G-BFFF")
        self.assertEqual(seed_2.seed_hash, "#LILI-70G-BFFF")

    def test_8_tier_visual_dna_serialization(self):
        """8-Tier Visual DNA 생성, 직렬화 및 문학 앵커문 추출 검증"""
        v = VisualDNA(
            face_geometry="날렵한 v-line 턱선",
            ocular_optics="차가운 금빛 홍채",
            hair_physics="백은색 긴 생머리",
            body_silhouette="168cm 호리호리한 체형",
            dermal_texture="창백한 백옥 피부",
            apparel_accents="검은 실크 드레스와 은색 초커",
            somatic_flush_cue="쇄골의 붉은 열감",
            lighting_contrast="차가운 달빛 대비"
        )
        anchor = v.compile_literary_anchor()
        self.assertIn("백은색 긴 생머리", anchor)
        self.assertIn("차가운 금빛 홍채", anchor)

        d = v.to_dict()
        self.assertEqual(d["face_geometry"], "날렵한 v-line 턱선")

    def test_personality_gene_hard_invariants(self):
        """불변 제약선(Hard Invariants)과 7대 축 유전자 검증"""
        inv = HardInvariants(
            primary_boundary="가문의 명예와 순결 서약",
            ego_collapse_trigger="초커를 쥔 채 시선 강제",
            somatic_achilles_heel="쇄골 패임 접촉"
        )
        gene = PersonalityGene(
            hard_invariants=inv,
            axis_1_physical_reflex="목덜미 척추 경직",
            axis_2_neuro_memory="호흡 억압",
            axis_3_social_deficit="가문 부채",
            axis_4_cognitive_distortion="완벽주의 강박",
            axis_5_shadow_ego="피지배 갈망",
            axis_6_alchemy_submission="체온 밀착 시 굴복",
            axis_7_gesture_ticks=["초커 만지기"]
        )
        self.assertEqual(gene.hard_invariants.primary_boundary, "가문의 명예와 순결 서약")

    def test_kinematic_chain_wave_propagation(self):
        """7단계 신체 운동 연쇄 파동 전이 순환 검증"""
        kc = KinematicChainState()
        self.assertEqual(kc.current_focus_indices, [0, 1])

        active_1 = kc.advance_wave()
        self.assertEqual(len(active_1), 2)
        self.assertEqual(kc.current_focus_indices, [2, 3])

    def test_character_aggregate_root(self):
        """Character 애그리게이트 루트 생성 검증"""
        char = Character.create_archetype(
            name="릴리스",
            title="제1황녀",
            faction="제국 황실",
            explicit_seed="#LILI-70G-BFFF",
            visual_dict={"face_geometry": "서늘한 턱선"},
            gene_dict={"axis_1_physical_reflex": "척추 경직"}
        )
        self.assertEqual(char.seed_hash, "#LILI-70G-BFFF")
        self.assertEqual(char.name, "릴리스")


if __name__ == "__main__":
    unittest.main()
