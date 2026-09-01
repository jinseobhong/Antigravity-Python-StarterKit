# -*- coding: utf-8 -*-
"""
src/infrastructure/database/repositories.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Character 및 TurnLedger 리포지토리 (CRUD & 불변 영속화)
"""

from __future__ import annotations
import json
from typing import Optional, List, Dict, Any

from src.domain.character import Character
from src.domain.gene_seed import GeneSeed
from src.domain.visual_dna import VisualDNA
from src.domain.personality_gene import PersonalityGene
from src.domain.somatic_ledger import SomaticLedger
from src.domain.spatial_pressure import SpatialPressureChamber, SpatialLayer
from src.domain.kinematic_chain import KinematicChainState
from src.infrastructure.database.db_manager import DatabaseManager


class CharacterRepository:
    """Character 엔티티 영속화 리포지토리"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def save(self, char: Character) -> None:
        conn = self.db.get_connection()
        with conn:
            conn.execute("""
                INSERT OR REPLACE INTO characters (
                    seed_hash, name, title, faction, visual_dna_json,
                    personality_gene_json, somatic_ledger_json,
                    spatial_pressure_json, kinematic_chain_json, image_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                char.seed_hash,
                char.name,
                char.title,
                char.faction,
                json.dumps(char.visual_dna.to_dict(), ensure_ascii=False),
                json.dumps(char.personality_gene.to_dict(), ensure_ascii=False),
                json.dumps(char.somatic_ledger.to_dict(), ensure_ascii=False),
                json.dumps(char.spatial_pressure.to_dict(), ensure_ascii=False),
                json.dumps(char.kinematic_chain.to_dict(), ensure_ascii=False),
                char.image_url
            ))

    def find_by_seed_hash(self, seed_hash: str) -> Optional[Character]:
        conn = self.db.get_connection()
        row = conn.execute("SELECT * FROM characters WHERE seed_hash = ?", (seed_hash,)).fetchone()
        if not row:
            return None
        return self._row_to_character(row)

    def list_all(self) -> List[Character]:
        conn = self.db.get_connection()
        rows = conn.execute("SELECT * FROM characters ORDER BY created_at ASC").fetchall()
        return [self._row_to_character(r) for r in rows]

    def _row_to_character(self, row) -> Character:
        v_data = json.loads(row["visual_dna_json"])
        p_data = json.loads(row["personality_gene_json"])
        s_data = json.loads(row["somatic_ledger_json"])
        sp_data = json.loads(row["spatial_pressure_json"])
        kc_data = json.loads(row["kinematic_chain_json"])

        seed = GeneSeed.from_input(row["name"], explicit_seed=row["seed_hash"])
        v_dna = VisualDNA.from_dict(v_data)
        p_gene = PersonalityGene.from_dict(p_data)
        s_ledger = SomaticLedger.from_dict(s_data)

        sp = SpatialPressureChamber()
        if "current_layer" in sp_data:
            sp.current_layer = SpatialLayer(sp_data["current_layer"])
        sp.touch_unlocked = sp_data.get("touch_unlocked", False)
        sp.intimacy_stage = sp_data.get("intimacy_stage", 1)

        kc = KinematicChainState(
            current_focus_indices=[0, 1],
            recent_chain_log=kc_data.get("recent_chain_log", "초기 파동 전이")
        )

        return Character(
            gene_seed=seed,
            name=row["name"],
            title=row["title"],
            faction=row["faction"],
            visual_dna=v_dna,
            personality_gene=p_gene,
            somatic_ledger=s_ledger,
            spatial_pressure=sp,
            kinematic_chain=kc,
            image_url=row["image_url"] or ""
        )


class TurnLedgerRepository:
    """턴 서사 히스토리 리포지토리"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def record_turn(self, seed_hash: str, turn_num: int, action: str, prose: str, ledger_snap: dict) -> None:
        conn = self.db.get_connection()
        with conn:
            conn.execute("""
                INSERT INTO turn_ledger (seed_hash, turn_number, player_action, narrative_prose, ledger_snapshot_json)
                VALUES (?, ?, ?, ?, ?)
            """, (seed_hash, turn_num, action, prose, json.dumps(ledger_snap, ensure_ascii=False)))

    def get_history(self, seed_hash: str) -> List[Dict[str, Any]]:
        conn = self.db.get_connection()
        rows = conn.execute("""
            SELECT turn_number, player_action, narrative_prose, ledger_snapshot_json, created_at
            FROM turn_ledger WHERE seed_hash = ? ORDER BY turn_number ASC
        """, (seed_hash,)).fetchall()
        return [{
            "turn": r["turn_number"],
            "action": r["player_action"],
            "prose": r["narrative_prose"],
            "ledger": json.loads(r["ledger_snapshot_json"]),
            "created_at": r["created_at"]
        } for r in rows]
