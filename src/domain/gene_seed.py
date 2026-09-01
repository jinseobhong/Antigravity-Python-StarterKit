# -*- coding: utf-8 -*-
"""
src/domain/gene_seed.py
~~~~~~~~~~~~~~~~~~~~~~~
Domain Layer: 고유 GENE SEED 해시 앵커링 엔티티 (#NAME-70G-XXXX)
- 100턴 대화에서도 페르소나 표류를 방지하는 불변 식별자
"""

from __future__ import annotations
import re
import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class GeneSeed:
    """불변 GENE SEED 식별자"""
    seed_hash: str
    target_name: str
    entropy_hex: str

    @classmethod
    def from_input(cls, target_name: str, explicit_seed: str = "") -> GeneSeed:
        """사용자 입력 또는 명시적 시드로부터 결정론적 GeneSeed 생성"""
        clean_name = target_name.strip() or "ANONYMOUS"

        # 명시적 시드 형식 검증
        if explicit_seed and re.match(r'^#[A-Za-z0-9]{4}-70G-[A-Fa-f0-9]{4}$', explicit_seed.strip()):
            s = explicit_seed.strip()
            hex_part = s.split("-")[-1].upper()
            return cls(seed_hash=s, target_name=clean_name, entropy_hex=hex_part)

        # 4글자 네임태그 결정 (한글 아키타입 매핑 지원)
        known_map = {"릴리스": "LILI", "에이라": "AIRA", "세라피나": "SERA", "실비아": "SILV"}
        name_tag = ""
        for k, v in known_map.items():
            if k in clean_name:
                name_tag = v
                break

        if not name_tag:
            alpha = re.sub(r'[^A-Za-z0-9]', '', clean_name).upper()
            if len(alpha) >= 4:
                name_tag = alpha[:4]
            else:
                raw = hashlib.sha256(clean_name.encode("utf-8")).hexdigest().upper()
                name_tag = (alpha + raw)[:4]

        # 해시 발급
        raw_hash = hashlib.sha256(f"{clean_name}::GENE_SEED_ENTROPY".encode("utf-8")).hexdigest()
        hex_part = raw_hash[:4].upper()
        full_seed = f"#{name_tag}-70G-{hex_part}"
        return cls(seed_hash=full_seed, target_name=clean_name, entropy_hex=hex_part)
