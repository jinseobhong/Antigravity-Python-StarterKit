# -*- coding: utf-8 -*-
"""
src/application/character_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
캐릭터 생성, 조회 및 시드 관리 유스케이스 서비스
"""

from __future__ import annotations
from typing import Dict, List, Optional

from src.domain.character import Character, LowenArmor
from src.infrastructure.database.repositories import CharacterRepository


class CharacterService:
    """캐릭터 라이프사이클 관리 서비스"""

    def __init__(self, character_repo: CharacterRepository):
        self.repo = character_repo

    def create_character(
        self,
        name: str,
        title: str,
        faction: str,
        armor_type: LowenArmor,
        traits: Optional[Dict[str, str]] = None,
        image_url: Optional[str] = None
    ) -> Character:
        """신규 캐릭터 생성 및 DB 저장"""
        char = Character(
            name=name,
            title=title,
            faction=faction,
            armor_type=armor_type,
            traits=dict(traits or {}),
            image_url=image_url,
        )
        self.repo.save(char)
        return char

    def get_character(self, seed_hash: str) -> Optional[Character]:
        """시드 해시 기준 캐릭터 조회"""
        return self.repo.find_by_seed_hash(seed_hash)

    def update_character(self, character: Character) -> None:
        """캐릭터 상태 영속화"""
        self.repo.save(character)
