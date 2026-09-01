# -*- coding: utf-8 -*-
"""
src/infrastructure/database/db_manager.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Infrastructure Layer: SQLite WAL 데이터베이스 연결 및 트랜잭션 관리자
- Thread-safe 커넥션 관리
- WAL (Write-Ahead Logging) 모드 활성화로 동시성 및 데이터 무결성 보장
"""

from __future__ import annotations
import os
import sqlite3
from pathlib import Path
from typing import Optional


class DBManager:
    """SQLite WAL 데이터베이스 관리자"""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = Path(__file__).resolve().parent.parent.parent.parent
            self.db_path = str(base_dir / "abyss_engine.db")
        else:
            self.db_path = db_path
        
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        """WAL 모드가 활성화된 새 커넥션 생성"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def init_database(self) -> None:
        """데이터베이스 스키마 초기화"""
        conn = self.get_connection()
        with conn:
            # 1. 캐릭터 테이블
            conn.execute("""
                CREATE TABLE IF NOT EXISTS characters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    seed_hash TEXT NOT NULL UNIQUE,
                    visual_dna_json TEXT NOT NULL,
                    personality_gene_json TEXT NOT NULL,
                    traits_json TEXT NOT NULL,
                    somatic_ledger_json TEXT NOT NULL,
                    spatial_pressure_json TEXT NOT NULL,
                    portrait_url TEXT DEFAULT '',
                    is_active INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 2. 턴 및 서사 히스토리 테이블
            conn.execute("""
                CREATE TABLE IF NOT EXISTS turn_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    character_id INTEGER NOT NULL,
                    turn_number INTEGER NOT NULL,
                    user_action TEXT NOT NULL,
                    narrative_response TEXT NOT NULL,
                    meta_status_json TEXT NOT NULL,
                    somatic_ledger_json TEXT NOT NULL,
                    gauges_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(character_id) REFERENCES characters(id) ON DELETE CASCADE
                );
            """)

            # 3. 인덱스 생성
            conn.execute("CREATE INDEX IF NOT EXISTS idx_characters_seed ON characters(seed_hash);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_characters_active ON characters(is_active);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_turn_ledger_char_turn ON turn_ledger(character_id, turn_number);")
        conn.close()
