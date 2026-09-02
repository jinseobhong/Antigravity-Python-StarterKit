#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_doc_snapshots.py — 6대 핵심 문서 스냅샷 및 자동 변경 감지/저장 엔진
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
기능:
1. 6대 핵심 문서 (CURRENT_STATE, IMPLEMENTATION_STATUS, IMPLEMENTATION_PLAN,
   WALKTHROUGH, ARCHITECTURE, REQUIREMENTS_SPECIFICATION)의 해시 및 내용 감지
2. 변경 발생 시 SQLite(state.db) document_snapshots 테이블에 자동 INSERT
3. 과거 스냅샷 히스토리 조회 및 롤백 지원
"""

from __future__ import annotations
import os
import sys
import re
import sqlite3
import hashlib
import difflib
from pathlib import Path
from typing import Dict, Any, List, Optional

# UTF-8 출력 보장
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 전사 핵심 관측 뷰 및 거버넌스 규격 문서 매핑 (views/ & .agents/ 정렬)
CORE_DOCUMENTS: Dict[str, str] = {
    "CURRENT_STATE": "views/CURRENT_STATE.md",
    "IMPLEMENTATION_STATUS": "views/IMPLEMENTATION_STATUS.md",
    "IMPLEMENTATION_PLAN": "views/IMPLEMENTATION_PLAN.md",
    "WALKTHROUGH": "views/WALKTHROUGH.md",
    "ARCHITECTURE": "views/ARCHITECTURE.md",
    "CONVENTIONS": ".agents/CONVENTIONS.md",
    "CODING_STANDARDS": ".agents/docs/CODING_STANDARDS.md",
    "TONE_AND_MANNER": ".agents/docs/TONE_AND_MANNER.md",
    "IMPACT_ANALYSIS": ".agents/docs/IMPACT_ANALYSIS_GUIDE.md",
    "FILESYSTEM_SPEC": ".agents/docs/FILESYSTEM_SPEC.md",
    "LIFECYCLE_SPEC": ".agents/docs/LIFECYCLE_SPEC.md",
    "GIT_WORKFLOW_SPEC": ".agents/docs/GIT_WORKFLOW_SPEC.md"
}


def get_repo_root() -> Path:
    cwd = Path.cwd()
    if (cwd / ".agents").exists():
        return cwd
    elif (cwd.parent / ".agents").exists():
        return cwd.parent
    return Path(__file__).resolve().parent.parent.parent


def get_db_connection(repo_root: Path) -> sqlite3.Connection:
    store_dir = repo_root / ".agents" / "store"
    store_dir.mkdir(parents=True, exist_ok=True)
    db_path = store_dir / "state.db"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn


def init_snapshot_schema(conn: sqlite3.Connection) -> None:
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS document_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_key TEXT NOT NULL,
                file_path TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                content TEXT NOT NULL,
                version TEXT DEFAULT 'v1.0.0',
                diff_summary TEXT DEFAULT '',
                snapshot_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_doc_snapshots_key_hash 
            ON document_snapshots(doc_key, content_hash);
        """)


def extract_version(content: str) -> str:
    """문서 헤더 표에서 버전 정보 추출"""
    match = re.search(r'\|\s*(?:문서 버전|Version|Doc Version)\s*\|\s*`?([^`|\n]+)`?\s*\|', content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "v1.0.0"


def calculate_diff_summary(old_text: str, new_text: str) -> str:
    """두 텍스트 간 변경점 요약 생성"""
    if not old_text:
        line_count = len(new_text.splitlines())
        return f"+{line_count} lines (INITIAL CREATION)"
    
    diff = list(difflib.unified_diff(
        old_text.splitlines(),
        new_text.splitlines(),
        lineterm=""
    ))
    added = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    deleted = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
    return f"+{added} lines, -{deleted} lines"


def sync_all_snapshots(repo_root: Path, verbose: bool = True) -> int:
    """6대 핵심 문서 감지 및 변경 시 SQLite 스냅샷 자동 INSERT"""
    conn = get_db_connection(repo_root)
    init_snapshot_schema(conn)

    inserted_count = 0

    if verbose:
        print("=" * 70)
        print("[Antigravity Document Snapshot Sync Engine] Starting Scan...")
        print("=" * 70)

    for doc_key, rel_path in CORE_DOCUMENTS.items():
        file_path = repo_root / rel_path

        # views/ARCHITECTURE.md 폴백 확인
        if not file_path.exists() and doc_key == "ARCHITECTURE":
            fallback = repo_root / "views" / "ARCHITECTURE.md"
            if fallback.exists():
                file_path = fallback

        if not file_path.exists():
            if verbose:
                print(f"  [-] {doc_key:<28}: [NOT FOUND] ({rel_path})")
            continue

        content = file_path.read_text(encoding="utf-8")
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        version = extract_version(content)

        # 직전 최신 스냅샷 조회
        cur = conn.execute(
            "SELECT id, content_hash, content, version FROM document_snapshots WHERE doc_key = ? ORDER BY id DESC LIMIT 1",
            (doc_key,)
        )
        prev = cur.fetchone()

        if not prev or prev["content_hash"] != content_hash:
            # 변경 감지 -> 새 스냅샷 INSERT
            old_content = prev["content"] if prev else ""
            diff_summary = calculate_diff_summary(old_content, content)

            with conn:
                conn.execute("""
                    INSERT INTO document_snapshots (
                        doc_key, file_path, content_hash, content, version, diff_summary
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (doc_key, rel_path, content_hash, content, version, diff_summary))

            inserted_count += 1
            if verbose:
                print(f"  [+] {doc_key:<28}: [SNAPSHOT INSERTED] ({version}) [{diff_summary}] -> hash: {content_hash[:8]}")
        else:
            if verbose:
                print(f"  [*] {doc_key:<28}: [UNCHANGED] ({version}) -> hash: {content_hash[:8]}")

    if verbose:
        print("=" * 70)
        print(f"[SYNC SUMMARY] Total {len(CORE_DOCUMENTS)} Core Documents Scanned. {inserted_count} new snapshot(s) stored in SQLite.")
        print("=" * 70)

    conn.close()
    return inserted_count


def list_history(repo_root: Path, doc_key: Optional[str] = None) -> None:
    """스냅샷 히스토리 목록 조회"""
    conn = get_db_connection(repo_root)
    init_snapshot_schema(conn)

    query = "SELECT id, doc_key, version, diff_summary, snapshot_time, substr(content_hash, 1, 8) as hash FROM document_snapshots"
    params = ()
    if doc_key:
        query += " WHERE doc_key = ?"
        params = (doc_key,)
    query += " ORDER BY id DESC LIMIT 30"

    rows = conn.execute(query, params).fetchall()
    print(f"\n{'ID':<5} | {'DOC KEY':<28} | {'VERSION':<10} | {'HASH':<10} | {'TIMESTAMP':<20} | {'DIFF SUMMARY'}")
    print("-" * 105)
    for r in rows:
        print(f"{r['id']:<5} | {r['doc_key']:<28} | {r['version']:<10} | {r['hash']:<10} | {r['snapshot_time']:<20} | {r['diff_summary']}")
    conn.close()


if __name__ == "__main__":
    root = get_repo_root()
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        key = sys.argv[2] if len(sys.argv) > 2 else None
        list_history(root, key)
    else:
        sync_all_snapshots(root, verbose=True)
