# -*- coding: utf-8 -*-
"""
src/infrastructure/database/db_manager.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SQLite 데이터베이스 트랜잭션 관리자 및 스키마 초기화 (DatabaseManager)
"""

from __future__ import annotations
import os
import sqlite3
from pathlib import Path
from typing import Optional


DEFAULT_DB_PATH = str(Path(__file__).resolve().parent.parent.parent.parent / "abyss_engine.db")


class DatabaseManager:
    """관계형 데이터베이스(RDB) 전담 트랜잭션 매니저"""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self._init_schema()
        self._seed_master_somatic_data()

    def get_connection(self) -> sqlite3.Connection:
        """외래키(Foreign Key) 활성화된 DB 커넥션 획득"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self):
        """관계형 테이블 스키마 초기화"""
        with self.get_connection() as conn:
            cur = conn.cursor()

            # 1. 캐릭터 메인 엔티티
            cur.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seed_hash VARCHAR(64) UNIQUE NOT NULL,
                name VARCHAR(64) NOT NULL,
                title VARCHAR(128) NOT NULL,
                faction VARCHAR(128) NOT NULL,
                armor_type VARCHAR(32) NOT NULL,
                image_url TEXT,
                ego_durability REAL DEFAULT 100.0,
                neural_taint REAL DEFAULT 0.0,
                pressure_stage VARCHAR(64) DEFAULT 'Stage 1 (탄성 저항: 꼿꼿한 오만과 반발)',
                active_spotlights TEXT DEFAULT '["04_cervical"]',
                chain_history TEXT DEFAULT '[]',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # 2. 캐릭터 결핍 및 세부 특성 (1:N)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS character_traits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                trait_key VARCHAR(64) NOT NULL,
                trait_value TEXT NOT NULL,
                FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE,
                UNIQUE (character_id, trait_key)
            );
            """)

            # 3. 턴별 롤플레이 서사 및 수치 이력 원장 (1:N)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS turn_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                turn_number INTEGER NOT NULL,
                user_action TEXT NOT NULL,
                vector_type VARCHAR(32) NOT NULL,
                narrative_prose TEXT NOT NULL,
                ego_durability REAL NOT NULL,
                neural_taint REAL NOT NULL,
                pressure_stage VARCHAR(64) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
            );
            """)

            # 4. N x N 관계역학 텐션 그리드 (N:N)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS tension_grid (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_char_id INTEGER NOT NULL,
                target_char_id INTEGER NOT NULL,
                taint_level REAL DEFAULT 0.0,
                debt_amount REAL DEFAULT 0.0,
                jealousy_index REAL DEFAULT 0.0,
                pressure_stage VARCHAR(64) DEFAULT 'Stage 1 (탄성 저항: 꼿꼿한 오만과 반발)',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_char_id) REFERENCES characters(id) ON DELETE CASCADE,
                FOREIGN KEY (target_char_id) REFERENCES characters(id) ON DELETE CASCADE,
                UNIQUE (source_char_id, target_char_id)
            );
            """)

            # 5. 17대 생체 텐서 정의 테이블
            cur.execute("""
            CREATE TABLE IF NOT EXISTS tensor_definitions (
                tensor_key VARCHAR(32) PRIMARY KEY,
                name_kr VARCHAR(64) NOT NULL,
                category VARCHAR(64) NOT NULL,
                unit VARCHAR(16) NOT NULL,
                min_val REAL DEFAULT 0.0,
                max_val REAL DEFAULT 100.0,
                default_val REAL DEFAULT 0.0,
                armor_affinity VARCHAR(32),
                description TEXT
            );
            """)

            # 6. 70대 신체 미세 감각 반응 노드
            cur.execute("""
            CREATE TABLE IF NOT EXISTS somatic_nodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_code VARCHAR(32) UNIQUE NOT NULL,
                body_part VARCHAR(64) NOT NULL,
                armor_type VARCHAR(32) NOT NULL,
                stage_level INTEGER NOT NULL,
                sensory_vector VARCHAR(32) NOT NULL,
                reaction_text TEXT NOT NULL
            );
            """)

            conn.commit()

    def _seed_master_somatic_data(self):
        """마스터 텐서 및 기본 데이터 시딩"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM tensor_definitions;")
            if cur.fetchone()[0] == 0:
                tensors = [
                    ("01_cranial", "두상/관자놀이 텐서", "신경계", "%", 0, 100, 0, "All", "두부 압박 및 이명"),
                    ("02_ocular", "동공 산대/시선 회피 텐서", "안구계", "%", 0, 100, 0, "All", "시선 떨림 및 산대"),
                    ("03_vocal", "성대 쇳소리/호흡 파열 텐서", "발성계", "%", 0, 100, 0, "All", "성대 잠김 및 숨소리"),
                    ("04_cervical", "경추 굳음/초커 조임 텐서", "경추계", "%", 0, 100, 0, "All", "목덜미 굳음"),
                    ("06_thoracic", "흉곽 팽창/심박 가속 텐서", "흉곽계", "%", 0, 100, 0, "All", "심장 박동 가속"),
                    ("09_sartorial", "의복 솔기/단추 장력 텐서", "의복계", "%", 0, 100, 0, "All", "의복 장력"),
                    ("10_manual", "손가락 악력/손끝 땀 텐서", "상지계", "%", 0, 100, 0, "All", "손끝 긴장"),
                    ("14_pedal", "족부 접지력 상실 텐서", "하지계", "%", 0, 100, 0, "All", "무릎 꺾임 및 접지 상실"),
                ]
                cur.executemany("""
                INSERT OR IGNORE INTO tensor_definitions (tensor_key, name_kr, category, unit, min_val, max_val, default_val, armor_affinity, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, tensors)
                conn.commit()
