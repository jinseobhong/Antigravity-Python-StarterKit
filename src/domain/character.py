# -*- coding: utf-8 -*-
"""
src/domain/character.py
~~~~~~~~~~~~~~~~~~~~~~~
AbyssEmpire 캐릭터 애그리게이트 루트 (Aggregate Root)
- GeneSeed, VisualDNA, PersonalityGene, SomaticLedger, SpatialPressureChamber, KinematicChainState를 유기적으로 결합
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from src.domain.gene_seed import GeneSeed
from src.domain.visual_dna import VisualDNA
from src.domain.personality_gene import PersonalityGene, HardInvariants
from src.domain.somatic_ledger import SomaticLedger
from src.domain.spatial_pressure import SpatialPressureChamber
from src.domain.kinematic_chain import KinematicChainState


@dataclass
class Character:
    """살아 숨 쉬는 하이브리드 캐릭터 엔티티"""
    gene_seed: GeneSeed
    name: str
    title: str
    faction: str
    visual_dna: VisualDNA
    personality_gene: PersonalityGene
    somatic_ledger: SomaticLedger = field(default_factory=SomaticLedger)
    spatial_pressure: SpatialPressureChamber = field(default_factory=SpatialPressureChamber)
    kinematic_chain: KinematicChainState = field(default_factory=KinematicChainState)
    image_url: str = ""

    @property
    def seed_hash(self) -> str:
        return self.gene_seed.seed_hash

    @classmethod
    def create_archetype(cls, name: str, title: str, faction: str, visual_dict: dict, gene_dict: dict, explicit_seed: str = "") -> Character:
        seed = GeneSeed.from_input(name, explicit_seed=explicit_seed)
        v_dna = VisualDNA.from_dict(visual_dict)
        p_gene = PersonalityGene.from_dict(gene_dict)
        return cls(
            gene_seed=seed,
            name=name,
            title=title,
            faction=faction,
            visual_dna=v_dna,
            personality_gene=p_gene
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "seed_hash": self.seed_hash,
            "name": self.name,
            "title": self.title,
            "faction": self.faction,
            "visual_dna": self.visual_dna.to_dict(),
            "personality_gene": self.personality_gene.to_dict(),
            "somatic_ledger": self.somatic_ledger.to_dict(),
            "spatial_pressure": self.spatial_pressure.to_dict(),
            "kinematic_chain": self.kinematic_chain.to_dict(),
            "image_url": self.image_url
        }
