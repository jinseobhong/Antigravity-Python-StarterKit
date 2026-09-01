# -*- coding: utf-8 -*-
"""
src/domain
~~~~~~~~~~
AbyssEngine 순수 도메인 계층 패키지 (외부 I/O 의존성 0)
"""

from .pressure_stage import PressureStage
from .relational_vector import RelationalVector
from .tensor_matrix import TensorMatrix, TENSOR_REGISTRY, KINEMATIC_CHAIN_FLOW
from .character import Character, LowenArmor
from .tension_grid import TensionGrid, TensionEdge
from .action_frame import ActionFrame, ObservableEvent, SpeechAct, Segment

__all__ = [
    "PressureStage",
    "RelationalVector",
    "TensorMatrix",
    "TENSOR_REGISTRY",
    "KINEMATIC_CHAIN_FLOW",
    "Character",
    "LowenArmor",
    "TensionGrid",
    "TensionEdge",
    "ActionFrame",
    "ObservableEvent",
    "SpeechAct",
    "Segment",
]
