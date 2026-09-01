# -*- coding: utf-8 -*-
"""
src/domain/relational_vector.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
5대 범용 관계역학 상성 벡터 (RelationalVector)
"""

from __future__ import annotations
from enum import Enum


class RelationalVector(str, Enum):
    """5대 범용 관계역학 상성 벡터"""
    DEVOTION_COMFORT = "🌸 순애 및 정서적 위로 벡터"
    SUBJUGATION = "🔴 정복적 압박 벡터"
    SUBMISSION_FAWN = "🟣 자발적 복종 및 헌신 벡터"
    SOMATIC_SYNC = "🟢 체성 감응 결속 벡터"
    SUSPENSION = "🟡 전술적 유예 및 덫 벡터"

    @classmethod
    def from_string(cls, raw: str) -> RelationalVector:
        """문자열에서 가장 유사한 관계역학 벡터 매핑"""
        raw_clean = raw.strip()
        for member in cls:
            if member.name.lower() in raw_clean.lower() or member.value in raw_clean:
                return member
        if "위로" in raw_clean or "순애" in raw_clean:
            return cls.DEVOTION_COMFORT
        elif "정복" in raw_clean or "압박" in raw_clean or "지배" in raw_clean:
            return cls.SUBJUGATION
        elif "복종" in raw_clean or "헌신" in raw_clean:
            return cls.SUBMISSION_FAWN
        elif "체성" in raw_clean or "감응" in raw_clean or "결속" in raw_clean:
            return cls.SOMATIC_SYNC
        return cls.SUSPENSION
