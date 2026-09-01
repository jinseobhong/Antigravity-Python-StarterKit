# -*- coding: utf-8 -*-
"""
src/infrastructure/database/repositories.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Infrastructure Layer: CharacterRepository & TurnLedgerRepository
- 완전한 CRUD 및 직렬화/역직렬화 지원
- 외부 JSON Import / Export 및 활성 캐릭터 스위칭 트랜잭션
"""

from __future__ import annotations
import json
import sqlite3
from typing import List, Optional, Dict, Any

from src.domain.character import Character
from src.infrastructure.database.db_manager import DBManager


class CharacterRepository:
    """Character 영속화 리포지토리"""

    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def save(self, char: Character) -> Character:
        """캐릭터 저장 (INSERT or UPDATE)"""
        conn = self.db_manager.get_connection()
        with conn:
            if char.id is None:
                # 활성 상태일 경우 다른 캐릭터 비활성화
                if char.is_active:
                    conn.execute("UPDATE characters SET is_active = 0 WHERE is_active = 1;")

                cur = conn.execute("""
                    INSERT INTO characters (
                        name, title, seed_hash, visual_dna_json, personality_gene_json,
                        traits_json, somatic_ledger_json, spatial_pressure_json,
                        portrait_url, is_active, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
                """, (
                    char.name,
                    char.title,
                    char.gene_seed.seed_hash,
                    json.dumps(char.visual_dna.to_dict(), ensure_ascii=False),
                    json.dumps(char.personality_gene.to_dict(), ensure_ascii=False),
                    json.dumps(char.traits.to_dict(), ensure_ascii=False),
                    json.dumps(char.somatic_ledger.to_dict(), ensure_ascii=False),
                    json.dumps(char.spatial_pressure.to_dict(), ensure_ascii=False),
                    char.portrait_url,
                    1 if char.is_active else 0
                ))
                char.id = cur.lastrowid
            else:
                if char.is_active:
                    conn.execute("UPDATE characters SET is_active = 0 WHERE id != ?;", (char.id,))

                conn.execute("""
                    UPDATE characters SET
                        name = ?, title = ?, seed_hash = ?,
                        visual_dna_json = ?, personality_gene_json = ?,
                        traits_json = ?, somatic_ledger_json = ?, spatial_pressure_json = ?,
                        portrait_url = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?;
                """, (
                    char.name,
                    char.title,
                    char.gene_seed.seed_hash,
                    json.dumps(char.visual_dna.to_dict(), ensure_ascii=False),
                    json.dumps(char.personality_gene.to_dict(), ensure_ascii=False),
                    json.dumps(char.traits.to_dict(), ensure_ascii=False),
                    json.dumps(char.somatic_ledger.to_dict(), ensure_ascii=False),
                    json.dumps(char.spatial_pressure.to_dict(), ensure_ascii=False),
                    char.portrait_url,
                    1 if char.is_active else 0,
                    char.id
                ))
        conn.close()
        return char

    def get_by_id(self, char_id: int) -> Optional[Character]:
        conn = self.db_manager.get_connection()
        cur = conn.execute("SELECT * FROM characters WHERE id = ?;", (char_id,))
        row = cur.fetchone()
        conn.close()
        return self._row_to_character(row) if row else None

    def get_by_seed(self, seed_hash: str) -> Optional[Character]:
        conn = self.db_manager.get_connection()
        cur = conn.execute("SELECT * FROM characters WHERE seed_hash = ?;", (seed_hash,))
        row = cur.fetchone()
        conn.close()
        return self._row_to_character(row) if row else None

    def get_active(self) -> Optional[Character]:
        conn = self.db_manager.get_connection()
        cur = conn.execute("SELECT * FROM characters WHERE is_active = 1 LIMIT 1;")
        row = cur.fetchone()
        if not row:
            # 활성 캐릭터가 없으면 첫 번째 캐릭터를 활성화
            cur = conn.execute("SELECT * FROM characters ORDER BY id ASC LIMIT 1;")
            row = cur.fetchone()
            if row:
                with conn:
                    conn.execute("UPDATE characters SET is_active = 1 WHERE id = ?;", (row["id"],))
        conn.close()
        return self._row_to_character(row) if row else None

    def set_active(self, char_id: int) -> bool:
        conn = self.db_manager.get_connection()
        with conn:
            conn.execute("UPDATE characters SET is_active = 0;")
            cur = conn.execute("UPDATE characters SET is_active = 1 WHERE id = ?;", (char_id,))
            affected = cur.rowcount
        conn.close()
        return affected > 0

    def list_all(self) -> List[Character]:
        conn = self.db_manager.get_connection()
        cur = conn.execute("SELECT * FROM characters ORDER BY id ASC;")
        rows = cur.fetchall()
        conn.close()
        return [self._row_to_character(r) for r in rows]

    def delete(self, char_id: int) -> bool:
        conn = self.db_manager.get_connection()
        with conn:
            cur = conn.execute("DELETE FROM characters WHERE id = ?;", (char_id,))
            affected = cur.rowcount
        conn.close()
        return affected > 0

    def seed_defaults_if_empty(self) -> None:
        """하드코딩 더미 시딩 비활성화 (순수 유저 생성 인격만 관리)"""
        pass

    def _row_to_character(self, row: sqlite3.Row) -> Character:
        data = {
            "id": row["id"],
            "name": row["name"],
            "title": row["title"],
            "seed_hash": row["seed_hash"],
            "visual_dna": json.loads(row["visual_dna_json"]),
            "personality_gene": json.loads(row["personality_gene_json"]),
            "traits": json.loads(row["traits_json"]),
            "somatic_ledger": json.loads(row["somatic_ledger_json"]),
            "spatial_pressure": json.loads(row["spatial_pressure_json"]),
            "portrait_url": row["portrait_url"] or "",
            "is_active": bool(row["is_active"])
        }
        return Character.from_dict(data)


class TurnLedgerRepository:
    """턴별 서사 및 원장 히스토리 영속화 리포지토리"""

    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def record_turn(
        self,
        character_id: int,
        turn_number: int,
        user_action: str,
        narrative_response: str,
        meta_status: Dict[str, Any],
        somatic_ledger: Dict[str, Any],
        gauges: Dict[str, Any]
    ) -> int:
        conn = self.db_manager.get_connection()
        with conn:
            cur = conn.execute("""
                INSERT INTO turn_ledger (
                    character_id, turn_number, user_action, narrative_response,
                    meta_status_json, somatic_ledger_json, gauges_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                character_id,
                turn_number,
                user_action,
                narrative_response,
                json.dumps(meta_status, ensure_ascii=False),
                json.dumps(somatic_ledger, ensure_ascii=False),
                json.dumps(gauges, ensure_ascii=False)
            ))
            row_id = cur.lastrowid
        conn.close()
        return row_id

    def get_history(self, character_id: int) -> List[Dict[str, Any]]:
        conn = self.db_manager.get_connection()
        cur = conn.execute("""
            SELECT * FROM turn_ledger WHERE character_id = ? ORDER BY turn_number ASC;
        """, (character_id,))
        rows = cur.fetchall()
        conn.close()

        history = []
        for r in rows:
            history.append({
                "id": r["id"],
                "turn_number": r["turn_number"],
                "user_action": r["user_action"],
                "narrative_response": r["narrative_response"],
                "meta_status": json.loads(r["meta_status_json"]),
                "somatic_ledger": json.loads(r["somatic_ledger_json"]),
                "gauges": json.loads(r["gauges_json"]),
                "created_at": r["created_at"]
            })
        return history

    def clear_history(self, character_id: int) -> None:
        conn = self.db_manager.get_connection()
        with conn:
            conn.execute("DELETE FROM turn_ledger WHERE character_id = ?;", (character_id,))
        conn.close()

    def remove_last_turn(self, character_id: int) -> Optional[Dict[str, Any]]:
        conn = self.db_manager.get_connection()
        res = None
        with conn:
            cur = conn.execute("""
                SELECT * FROM turn_ledger WHERE character_id = ? ORDER BY turn_number DESC LIMIT 1;
            """, (character_id,))
            row = cur.fetchone()
            if row:
                conn.execute("DELETE FROM turn_ledger WHERE id = ?;", (row["id"],))
                res = {
                    "id": row["id"],
                    "turn_number": row["turn_number"],
                    "user_action": row["user_action"],
                    "narrative_response": row["narrative_response"],
                    "meta_status": json.loads(row["meta_status_json"]) if "meta_status_json" in row.keys() else {},
                    "somatic_ledger": json.loads(row["somatic_ledger_json"]) if "somatic_ledger_json" in row.keys() else {},
                    "gauges": json.loads(row["gauges_json"]) if "gauges_json" in row.keys() else {}
                }
        conn.close()
        return res
