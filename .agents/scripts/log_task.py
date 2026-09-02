#!/usr/bin/env python3
"""
log_task.py — Antigravity SQLite Audit Logger & CLI Tool

Manages permanent task archival, verification logs, component status,
5W1H decision overrides, agent asset mutations, and session snapshots in `.agents/store/state.db`.
"""

import sys
import sqlite3
import argparse
from pathlib import Path
import json

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def get_db_path(repo_root: Path) -> Path:
    store_dir = repo_root / ".agents" / "store"
    store_dir.mkdir(parents=True, exist_ok=True)
    return store_dir / "state.db"

def get_connection(repo_root: Path) -> sqlite3.Connection:
    db_path = get_db_path(repo_root)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn

def init_db(repo_root: Path):
    db_path = get_db_path(repo_root)
    schema_path = repo_root / ".agents" / "store" / "schema.sql"
    
    if not schema_path.exists():
        print(f"[ERROR] Schema file not found: {schema_path}")
        return False

    with get_connection(repo_root) as conn:
        with open(schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
    print(f"[OK] SQLite database initialized successfully (WAL mode active) at: {db_path}")
    return True

def record_task(repo_root: Path, name: str, phase: str, auth: str, proof: str, decision: str) -> int:
    init_db(repo_root)
    with get_connection(repo_root) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tasks (task_name, current_phase, implementation_auth, proof_status, decision_status, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (name, phase, auth, proof, decision)
        )
        conn.commit()
        task_id = cursor.lastrowid
        print(f"[OK] Task recorded successfully (Task ID: {task_id})")
        return task_id

def record_mutation(repo_root: Path, asset_path: str, change_type: str, approval_keyword: str, diff_summary: str, patch_content: str = "", applied_by: str = "AI_AGENT") -> int:
    init_db(repo_root)
    with get_connection(repo_root) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO agent_asset_mutations (asset_path, change_type, approval_keyword, diff_summary, patch_content, applied_by, applied_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (asset_path, change_type, approval_keyword, diff_summary, patch_content, applied_by)
        )
        conn.commit()
        mutation_id = cursor.lastrowid
        print(f"[OK] Asset mutation recorded successfully (Mutation ID: {mutation_id})")
        return mutation_id

def record_snapshot(repo_root: Path, conversation_id: str, active_track: str, last_action: str, snapshot_data: dict) -> int:
    init_db(repo_root)
    with get_connection(repo_root) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO agent_session_snapshots (conversation_id, active_track, last_action, snapshot_data, created_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (conversation_id, active_track, last_action, json.dumps(snapshot_data, ensure_ascii=False))
        )
        conn.commit()
        session_id = cursor.lastrowid
        print(f"[OK] Session snapshot recorded successfully (Session ID: {session_id})")
        return session_id

def show_status(repo_root: Path):
    init_db(repo_root)
    with get_connection(repo_root) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT task_id, task_name, current_phase, proof_status, decision_status, updated_at FROM tasks ORDER BY task_id DESC LIMIT 5")
        task_rows = cursor.fetchall()
        
        print("=" * 80)
        print("🗄️  [Antigravity SQLite Store] Recent Audit Logs (state.db - WAL Mode)")
        print("=" * 80)
        if not task_rows:
            print("No tasks recorded yet in SQLite store.")
        else:
            print(f"{'ID':<4} | {'Task Name':<35} | {'Phase':<10} | {'Proof':<8} | {'Decision':<14}")
            print("-" * 80)
            for r in task_rows:
                print(f"{r[0]:<4} | {r[1][:33]:<35} | {r[2]:<10} | {r[3]:<8} | {r[4]:<14}")

        cursor.execute("SELECT mutation_id, asset_path, change_type, approval_keyword, applied_at FROM agent_asset_mutations ORDER BY mutation_id DESC LIMIT 5")
        mutation_rows = cursor.fetchall()
        if mutation_rows:
            print("-" * 80)
            print("📝 [Recent Agent Asset Mutations]")
            print(f"{'ID':<4} | {'Asset Path':<35} | {'Type':<8} | {'Auth':<10} | {'Applied At':<19}")
            print("-" * 80)
            for m in mutation_rows:
                print(f"{m[0]:<4} | {m[1][:33]:<35} | {m[2]:<8} | {m[3]:<10} | {str(m[4])[:19]}")
        print("=" * 80)

def main():
    cwd = Path.cwd()
    if (cwd / ".agents").exists():
        root = cwd
    elif (cwd.parent / ".agents").exists():
        root = cwd.parent
    else:
        root = Path(__file__).resolve().parent.parent.parent

    parser = argparse.ArgumentParser(description="Antigravity SQLite Audit Logger")
    parser.add_argument("--init", action="store_true", help="Initialize SQLite state.db")
    parser.add_argument("--status", action="store_true", help="Show recent task audit logs")
    parser.add_argument("--record-task", type=str, help="Task name to record")
    parser.add_argument("--phase", type=str, default="Completed", help="Current task phase")
    parser.add_argument("--auth", type=str, default="APPROVED", help="Implementation authorization")
    parser.add_argument("--proof", type=str, default="PROVEN", help="AI Proof status")
    parser.add_argument("--decision", type=str, default="FINAL_ACCEPTED", help="Human decision status")
    parser.add_argument("--record-mutation", type=str, help="Asset path for mutation record")
    parser.add_argument("--change-type", type=str, default="UPDATE", help="Mutation change type (CREATE/UPDATE/DELETE)")
    parser.add_argument("--approval-keyword", type=str, default="APPROVE", help="User approval keyword")
    parser.add_argument("--diff-summary", type=str, default="", help="Summary of changes")

    args = parser.parse_args()

    if args.init:
        init_db(root)
    elif args.record_task:
        record_task(root, args.record_task, args.phase, args.auth, args.proof, args.decision)
    elif args.record_mutation:
        record_mutation(root, args.record_mutation, args.change_type, args.approval_keyword, args.diff_summary)
    else:
        show_status(root)

if __name__ == "__main__":
    main()

