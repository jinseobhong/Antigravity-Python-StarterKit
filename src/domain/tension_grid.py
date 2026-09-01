# -*- coding: utf-8 -*-
"""
src/domain/tension_grid.py
~~~~~~~~~~~~~~~~~~~~~~~~~~
N x N 캐릭터 간 상호 관계역학 및 질투/부채 매트릭스 (TensionGrid)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple, Any

from .pressure_stage import PressureStage


@dataclass
class TensionEdge:
    """두 캐릭터 간의 관계역학 간선"""
    source_seed_hash: str
    target_seed_hash: str
    taint_level: float = 0.0       # 상호 오염도 (0.0 ~ 100.0)
    debt_amount: float = 0.0       # 심리적/물리적 부채
    jealousy_index: float = 0.0    # 질투 및 경쟁 지수 (0.0 ~ 100.0)
    pressure_stage: PressureStage = PressureStage.STAGE_1_ELASTIC

    def update_dynamics(self, taint_delta: float, debt_delta: float, jealousy_delta: float) -> None:
        """역학 수치 갱신"""
        self.taint_level = max(0.0, min(100.0, self.taint_level + taint_delta))
        self.debt_amount = max(0.0, self.debt_amount + debt_delta)
        self.jealousy_index = max(0.0, min(100.0, self.jealousy_index + jealousy_delta))
        self.pressure_stage = PressureStage.from_neural_taint(self.taint_level)


@dataclass
class TensionGrid:
    """N x N 상호 관계역학 그리드 매니저"""
    edges: Dict[Tuple[str, str], TensionEdge] = field(default_factory=dict)

    def get_or_create_edge(self, source_hash: str, target_hash: str) -> TensionEdge:
        """두 캐릭터 간 간선 조회 또는 생성"""
        pair_key = (source_hash, target_hash)
        if pair_key not in self.edges:
            self.edges[pair_key] = TensionEdge(source_seed_hash=source_hash, target_seed_hash=target_hash)
        return self.edges[pair_key]

    def record_interaction(self, source_hash: str, target_hash: str, taint_delta: float, debt_delta: float, jealousy_delta: float) -> TensionEdge:
        """상호작용 반영"""
        edge = self.get_or_create_edge(source_hash, target_hash)
        edge.update_dynamics(taint_delta, debt_delta, jealousy_delta)
        return edge
