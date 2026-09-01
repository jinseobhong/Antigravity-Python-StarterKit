# -*- coding: utf-8 -*-
"""
tests/unit/test_domain_models.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unit Tests: 순수 도메인 모델(POPO) 무결성 및 불변식 검증
"""

import unittest
from src.models.gene_seed import GeneSeed
from src.models.visual_dna import VisualDNA
from src.models.personality_gene import PersonalityGene, HardInvariants
from src.models.character_traits import CharacterTraits, PsychologicalGauges, SomaticMetrics
from src.models.somatic_ledger import SomaticLedger
from src.models.spatial_pressure import SpatialPressure
from src.models.kinematic_chain import KinematicChain
from src.models.character import Character


class TestDomainModels(unittest.TestCase):

    def test_gene_seed_deterministic_generation(self):
        seed1 = GeneSeed.from_input("릴리스")
        self.assertTrue(seed1.seed_hash.startswith("#LILI-70G-"))
        self.assertEqual(len(seed1.seed_hash), 14)

        seed2 = GeneSeed.from_input("실비아", "#SILV-70G-77E2")
        self.assertEqual(seed2.seed_hash, "#SILV-70G-77E2")

    def test_visual_dna_serialization(self):
        dna = VisualDNA(
            face_geometry="V-line",
            ocular_optics="golden eyes",
            hair_physics="silver straight",
            body_silhouette="168cm slender",
            dermal_texture="pale skin",
            apparel_accents="black dress, silver choker",
            somatic_flush_cue="blushing collarbone",
            lighting_contrast="moonlight contrast"
        )
        d = dna.to_dict()
        restored = VisualDNA.from_dict(d)
        self.assertEqual(restored.hair_physics, "silver straight")
        self.assertEqual(restored.apparel_accents, "black dress, silver choker")
        self.assertIn("[외모 규격]", dna.compile_literary_anchor())

    def test_character_lilith_factory(self):
        lilith = Character.create_lilith()
        self.assertEqual(lilith.name, "릴리스")
        self.assertEqual(lilith.title, "제1황녀")
        self.assertEqual(lilith.gene_seed.seed_hash, "#LILI-70G-BFFF")
        self.assertEqual(lilith.traits.archetype_class, "Rigid (결벽주의 척추 방어)")
        self.assertEqual(lilith.traits.gauges.trust, 20)
        self.assertEqual(lilith.traits.gauges.submission, 20)

    def test_kinematic_chain_spotlights(self):
        sp0 = KinematicChain.get_spotlight_tensors(0)
        self.assertIsInstance(sp0, list)
        self.assertGreaterEqual(len(sp0), 2)
        
        sp_conquest = KinematicChain.get_spotlight_tensors(1, "압박")
        self.assertIn("07_digital_and_grip_strength", sp_conquest)


if __name__ == "__main__":
    unittest.main()
