# -*- coding: utf-8 -*-
"""
src/infrastructure/database/db_manager.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SQLite 기반 고신뢰도 트랜잭션 관리자 (Zero-Dependency)
"""

from __future__ import annotations
import sqlite3
import os
import threading
from typing import Optional


class DatabaseManager:
    """SQLite 커넥션 풀 및 스키마 관리자"""

    def __init__(self, db_path: str = "abyss_engine.db"):
        self.db_path = db_path
        self._local = threading.local()
        self.init_schema()

    def get_connection(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA foreign_keys = ON;")
            self._local.conn = conn
        return self._local.conn

    def init_schema(self) -> None:
        """새로운 8-Tier Visual DNA 및 70단계 유전자 스키마 초기화 (레거시 테이블 전수 완전 정리)"""
        conn = self.get_connection()
        with conn:
            # 모든 비인가 레거시 테이블 완전 삭제
            conn.execute("PRAGMA foreign_keys = OFF;")
            try:
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                existing_tables = [r[0] for r in cursor.fetchall()]
                for tbl in existing_tables:
                    if tbl not in ("characters", "turn_ledger"):
                        conn.execute(f"DROP TABLE IF EXISTS {tbl};")
            except Exception:
                pass
            conn.execute("PRAGMA foreign_keys = ON;")

            # 구버전 스키마 감지 시 characters / turn_ledger 테이블 리셋
            try:
                conn.execute("SELECT visual_dna_json FROM characters LIMIT 1;")
            except Exception:
                conn.execute("PRAGMA foreign_keys = OFF;")
                conn.execute("DROP TABLE IF EXISTS turn_ledger;")
                conn.execute("DROP TABLE IF EXISTS characters;")
                conn.execute("PRAGMA foreign_keys = ON;")

            # 1. 캐릭터 & 유전자 테이블
            conn.execute("""
                CREATE TABLE IF NOT EXISTS characters (
                    seed_hash TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    faction TEXT NOT NULL,
                    visual_dna_json TEXT NOT NULL,
                    personality_gene_json TEXT NOT NULL,
                    somatic_ledger_json TEXT NOT NULL,
                    spatial_pressure_json TEXT NOT NULL,
                    kinematic_chain_json TEXT NOT NULL,
                    image_url TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 2. 턴 서사 원장 테이블
            conn.execute("""
                CREATE TABLE IF NOT EXISTS turn_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    seed_hash TEXT NOT NULL,
                    turn_number INTEGER NOT NULL,
                    player_action TEXT NOT NULL,
                    narrative_prose TEXT NOT NULL,
                    ledger_snapshot_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (seed_hash) REFERENCES characters(seed_hash) ON DELETE CASCADE
                );
            """)
