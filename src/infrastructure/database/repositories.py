# -*- coding: utf-8 -*-
"""
src/infrastructure/database/repositories.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
엔티티별 SQLite CRUD 전담 리포지토리 모음
"""

from __future__ import annotations
import json
from typing import Dict, List, Optional, Any, Tuple

from src.domain.character import Character, LowenArmor
from src.domain.pressure_stage import PressureStage
from src.domain.tensor_matrix import TensorMatrix
from src.domain.tension_grid import TensionGrid, TensionEdge
from .db_manager import DatabaseManager


class CharacterRepository:
    """캐릭터 및 특성 데이터 영속성 관리 리포지토리"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def save(self, character: Character) -> int:
        """캐릭터 저장 또는 갱신"""
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO characters (
                seed_hash, name, title, faction, armor_type, image_url,
                ego_durability, neural_taint, pressure_stage, active_spotlights, chain_history, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(seed_hash) DO UPDATE SET
                name=excluded.name,
                title=excluded.title,
                faction=excluded.faction,
                armor_type=excluded.armor_type,
                image_url=excluded.image_url,
                ego_durability=excluded.ego_durability,
                neural_taint=excluded.neural_taint,
                pressure_stage=excluded.pressure_stage,
                active_spotlights=excluded.active_spotlights,
                chain_history=excluded.chain_history,
                updated_at=CURRENT_TIMESTAMP;
            """, (
                character.seed_hash,
                character.name,
                character.title,
                character.faction,
                character.armor_type.value,
                character.image_url,
                character.ego_durability,
                character.neural_taint,
                character.pressure_stage.value,
                json.dumps(character.tensors.active_spotlights, ensure_ascii=False),
                json.dumps(character.tensors.recent_chain_history, ensure_ascii=False),
            ))

            char_id = cur.lastrowid
            if not char_id:
                cur.execute("SELECT id FROM characters WHERE seed_hash = ?", (character.seed_hash,))
                char_id = cur.fetchone()[0]

            # 특성 저장
            for k, v in character.traits.items():
                cur.execute("""
                INSERT INTO character_traits (character_id, trait_key, trait_value)
                VALUES (?, ?, ?)
                ON CONFLICT(character_id, trait_key) DO UPDATE SET trait_value=excluded.trait_value;
                """, (char_id, k, v))

            conn.commit()
            return char_id

    def find_by_seed_hash(self, seed_hash: str) -> Optional[Character]:
        """시드 해시로 캐릭터 조회"""
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM characters WHERE seed_hash = ?", (seed_hash,))
            row = cur.fetchone()
            if not row:
                return None

            # 특성 조회
            cur.execute("SELECT trait_key, trait_value FROM character_traits WHERE character_id = ?", (row["id"],))
            traits = {r["trait_key"]: r["trait_value"] for r in cur.fetchall()}

            # 텐서 복원
            active_spotlights = json.loads(row["active_spotlights"] or "[]")
            chain_history = json.loads(row["chain_history"] or "[]")

            tensors = TensorMatrix(
                active_spotlights=active_spotlights,
                recent_chain_history=chain_history
            )

            armor = LowenArmor.RIGID
            for a in LowenArmor:
                if a.value == row["armor_type"] or a.name == row["armor_type"]:
                    armor = a
                    break

            return Character(
                name=row["name"],
                title=row["title"],
                faction=row["faction"],
                armor_type=armor,
                image_url=row["image_url"],
                seed_hash=row["seed_hash"],
                ego_durability=float(row["ego_durability"]),
                neural_taint=float(row["neural_taint"]),
                traits=traits,
                tensors=tensors,
            )


class TurnHistoryRepository:
    """턴별 서사 및 수치 이력 원장 리포지토리"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def record_turn(
        self,
        character_id: int,
        turn_number: int,
        user_action: str,
        vector_type: str,
        narrative_prose: str,
        ego_durability: float,
        neural_taint: float,
        pressure_stage: str,
    ) -> int:
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO turn_history (
                character_id, turn_number, user_action, vector_type, narrative_prose,
                ego_durability, neural_taint, pressure_stage
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                character_id, turn_number, user_action, vector_type, narrative_prose,
                ego_durability, neural_taint, pressure_stage
            ))
            conn.commit()
            return cur.lastrowid

    def get_history(self, character_id: int) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM turn_history WHERE character_id = ? ORDER BY turn_number ASC", (character_id,))
            return [dict(r) for r in cur.fetchall()]
