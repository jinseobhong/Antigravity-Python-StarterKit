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

        # 명시적 시드 형식 검증 (유연한 네임태그 2~12글자 허용)
        if explicit_seed and re.match(r'^#[A-Za-z0-9_-]{2,12}-70G-[A-Fa-f0-9]{4}$', explicit_seed.strip()):
            s = explicit_seed.strip()
            hex_part = s.split("-")[-1].upper()
            return cls(seed_hash=s, target_name=clean_name, entropy_hex=hex_part)

        if explicit_seed and explicit_seed.strip().startswith("#"):
            s = explicit_seed.strip()
            parts = s.split("-")
            hex_part = parts[-1].upper() if len(parts) > 1 else "INIT"
            return cls(seed_hash=s, target_name=clean_name, entropy_hex=hex_part)

        # 4글자 네임태그 결정 (한글 아키타입 매핑 지원)
        known_map = {"릴리스": "LILI", "에이라": "AIRA", "세라피나": "SERA", "실비아": "SILV"}
        name_tag = ""
        for k, v in known_map.items():
            if k in clean_name:
                name_tag = v
                break

        if not name_tag:
            # 영문 변환 또는 해시 기반 태그 추출
            ascii_chars = re.sub(r'[^A-Za-z]', '', clean_name).upper()
            name_tag = ascii_chars[:4].ljust(4, 'X') if ascii_chars else "GENE"

        # 결정론적 4자리 16진수 엔트로피 계산
        entropy_hash = hashlib.sha256(f"{clean_name}:abyss_soul_seed".encode('utf-8')).hexdigest()[:4].upper()
        seed_hash = f"#{name_tag}-70G-{entropy_hash}"

        return cls(
            seed_hash=seed_hash,
            target_name=clean_name,
            entropy_hex=entropy_hash
        )
