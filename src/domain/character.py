# -*- coding: utf-8 -*-
"""
src/domain/character.py
~~~~~~~~~~~~~~~~~~~~~~~
순수 객체지향(OOP) 캐릭터 엔티티 및 로웬 신체 갑주 (Character & LowenArmor)
"""

from __future__ import annotations
import hashlib
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Any

from .pressure_stage import PressureStage
from .tensor_matrix import TensorMatrix


class LowenArmor(str, Enum):
    """알렉산더 로웬 5대 신체 갑주 유형"""
    RIGID = "Rigid (완벽주의 척추 방어)"
    CONTROLLER = "Controller (상체 팽창 및 지배)"
    ENDURER = "Endurer (신체 억압 및 인내)"
    DEPRIVED = "Deprived (흉곽 함몰 및 애착 갈망)"
    DETACHED = "Detached (체온 냉각 및 해리)"


@dataclass
class Character:
    """순수 도메인 캐릭터 엔티티"""
    name: str
    title: str
    faction: str
    armor_type: LowenArmor
    image_url: Optional[str] = None
    seed_hash: str = field(default="")
    ego_durability: float = 100.0  # 자아 내구도 (100.0 -> 0.0)
    neural_taint: float = 0.0     # 신경 오염도 (0.0 -> 100.0)
    traits: Dict[str, str] = field(default_factory=dict)
    tensors: TensorMatrix = field(default_factory=TensorMatrix)

    def __post_init__(self):
        if not self.seed_hash:
            seed_raw = f"{self.name}_{self.title}_{self.faction}_{self.armor_type.value}"
            self.seed_hash = hashlib.sha256(seed_raw.encode("utf-8")).hexdigest()[:16]

    @property
    def pressure_stage(self) -> PressureStage:
        """신경 오염도 기반 실시간 압력 단계 계산"""
        return PressureStage.from_neural_taint(self.neural_taint)

    def apply_damage_and_taint(self, ego_damage: float, taint_gain: float) -> Tuple[float, float, PressureStage]:
        """자아 내구도 감소 및 신경 오염도 증가 인과율 연산"""
        self.ego_durability = max(0.0, min(100.0, self.ego_durability - ego_damage))
        self.neural_taint = max(0.0, min(100.0, self.neural_taint + taint_gain))
        return self.ego_durability, self.neural_taint, self.pressure_stage

    def to_dict(self) -> Dict[str, Any]:
        """직렬화"""
        return {
            "seed_hash": self.seed_hash,
            "name": self.name,
            "title": self.title,
            "faction": self.faction,
            "armor_type": self.armor_type.value,
            "image_url": self.image_url,
            "ego_durability": self.ego_durability,
            "neural_taint": self.neural_taint,
            "pressure_stage": self.pressure_stage.value,
            "traits": dict(self.traits),
            "tensors": self.tensors.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Character:
        """역직렬화"""
        armor_raw = data.get("armor_type", LowenArmor.RIGID.value)
        armor = LowenArmor.RIGID
        for a in LowenArmor:
            if a.value == armor_raw or a.name == armor_raw:
                armor = a
                break

        tensors = TensorMatrix.from_dict(data.get("tensors", {}))

        char = cls(
            name=data["name"],
            title=data.get("title", ""),
            faction=data.get("faction", ""),
            armor_type=armor,
            image_url=data.get("image_url"),
            seed_hash=data.get("seed_hash", ""),
            ego_durability=float(data.get("ego_durability", 100.0)),
            neural_taint=float(data.get("neural_taint", 0.0)),
            traits=dict(data.get("traits", {})),
            tensors=tensors,
        )
        return char
