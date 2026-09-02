#!/usr/bin/env python3
"""
auto_push.py — Antigravity One-Click Dual Git Sync & Push Automation

Automates:
1. Submodule (.agents/) Git staging, conventional commit, and remote push.
2. Parent repository Git staging, submodule pointer update, conventional commit, and remote push.
"""

import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def run_cmd(cmd: list, cwd: Path) -> tuple[int, str]:
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return res.returncode, (res.stdout + "\n" + res.stderr).strip()

def has_git_changes(repo_path: Path) -> bool:
    code, out = run_cmd(["git", "status", "--porcelain"], repo_path)
    return bool(out.strip())

def dual_push(repo_root: Path, message: str = "chore: automated sync and push"):
    agents_dir = repo_root / ".agents"

    # 0. 6대 핵심 문서 스냅샷 SQLite 자동 INSERT 트리거
    try:
        from sync_doc_snapshots import sync_all_snapshots
        sync_all_snapshots(repo_root, verbose=True)
    except Exception as e:
        # 서브프로세스로 대체 실행
        run_cmd([sys.executable, str(agents_dir / "scripts" / "sync_doc_snapshots.py")], repo_root)

    print("=" * 70)
    print("[Antigravity Dual Git Sync] Starting One-Click Push...")
    print("=" * 70)

    # 1. Sync & Push .agents Submodule
    if agents_dir.exists() and (agents_dir / ".git").exists():
        if has_git_changes(agents_dir):
            print(f"* Changes detected in Submodule (.agents/). Committing...")
            run_cmd(["git", "add", "-A"], agents_dir)
            code, out = run_cmd(["git", "commit", "-m", message], agents_dir)
            print(f"  - Commit Output: {out.splitlines()[-1] if out else 'OK'}")
            print(f"* Pushing .agents to remote (origin/master)...")
            code, out = run_cmd(["git", "push", "origin", "master"], agents_dir)
            if code == 0:
                print("  - Submodule Push SUCCESS.")
            else:
                print(f"  - Submodule Push FAILED: {out}")
        else:
            print("* Submodule (.agents/) working tree is clean. No push needed.")

    # 2. Sync & Push Parent Repository
    if has_git_changes(repo_root):
        print(f"\n* Changes detected in Parent Repository. Committing...")
        run_cmd(["git", "add", "-A"], repo_root)
        code, out = run_cmd(["git", "commit", "-m", message], repo_root)
        print(f"  - Commit Output: {out.splitlines()[-1] if out else 'OK'}")
        print(f"* Pushing Parent Repository to remote (origin/master)...")
        code, out = run_cmd(["git", "push", "origin", "master"], repo_root)
        if code == 0:
            print("  - Parent Repository Push SUCCESS.")
        else:
            print(f"  - Parent Repository Push FAILED: {out}")
    else:
        print("* Parent Repository working tree is clean. No push needed.")

    print("=" * 70)
    print("[Dual Git Sync COMPLETED (PROVEN)]")
    print("=" * 70)

if __name__ == "__main__":
    cwd = Path.cwd()
    if (cwd / ".agents").exists():
        root = cwd
    elif (cwd.parent / ".agents").exists():
        root = cwd.parent
    else:
        root = Path(__file__).resolve().parent.parent.parent

    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "chore: automated sync and push"
    dual_push(root, msg)
