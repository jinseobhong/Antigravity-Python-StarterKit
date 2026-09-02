#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_checks.py — Antigravity 전사 무결성 원클릭 통합 검증 엔진 (All-in-One Validator)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
실행 순서:
1. 전체 단위 테스트 실행 (Unit Test Suite with Exit Code Audit)
2. 거버넌스 템플릿 및 views/ 대칭성 검증 (verify_sync)
3. 11대 핵심 문서 변경 감지 및 SQLite 자동 스냅샷 적재 (sync_doc_snapshots)
4. 종합 헬스체크 대시보드 출력
"""

import sys
import time
import subprocess
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def get_repo_root() -> Path:
    cwd = Path.cwd()
    if (cwd / ".agents").exists():
        return cwd
    elif (cwd.parent / ".agents").exists():
        return cwd.parent
    return Path(__file__).resolve().parent.parent.parent


def run_step(title: str, command: list, cwd: Path) -> tuple:
    start_time = time.time()
    try:
        res = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        duration = time.time() - start_time
        out_text = res.stdout or ""
        if res.stderr:
            out_text += "\n" + res.stderr
        return (res.returncode == 0, out_text.strip(), duration)
    except Exception as e:
        duration = time.time() - start_time
        return (False, str(e), duration)


def main() -> int:
    root = get_repo_root()
    py_exec = sys.executable

    print("=" * 80)
    print("🚀 [Antigravity All-in-One Validator] 원클릭 전사 무결성 검증 시작...")
    print("=" * 80)

    steps = [
        ("1. 단위 테스트 전수 검증 (Unit Tests)", [py_exec, "-m", "unittest", "discover", "-s", "tests/unit", "-p", "test_*.py", "-v"]),
        ("2. 종단간 E2E 시나리오 검증 (E2E Tests)", [py_exec, "-m", "unittest", "discover", "-s", "tests/e2e", "-p", "test_*.py", "-v"]),
        ("3. 거버넌스 & views/ 대칭성 검증 (verify_sync)", [py_exec, ".agents/scripts/verify_sync.py"]),
        ("4. 11대 핵심 문서 스냅샷 DB 동기화 (sync_doc_snapshots)", [py_exec, ".agents/scripts/sync_doc_snapshots.py"])
    ]

    results = []
    overall_success = True

    for name, cmd in steps:
        print(f"\n▶ 실행 중: {name}...")
        success, output, duration = run_step(name, cmd, root)
        status_str = "[PASS]" if success else "[FAIL]"
        results.append((name, success, duration, output))
        if not success:
            overall_success = False
            print(f"   ❌ {status_str} ({duration:.3f}s)")
            print(f"   [상세 에러 출력]:\n{output}\n")
            break
        else:
            print(f"   ✅ {status_str} ({duration:.3f}s)")

    print("\n" + "=" * 80)
    print("📊 [종합 무결성 검증 대시보드 (Executive Summary)]")
    print("=" * 80)
    print(f"{'검증 항목':<48} | {'상태':<8} | {'소요 시간':<10}")
    print("-" * 80)

    total_time = 0.0
    for name, success, duration, _ in results:
        total_time += duration
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name:<48} | {status:<8} | {duration:.3f}s")

    print("-" * 80)
    print(f"{'총 소요 시간':<48} |          | {total_time:.3f}s")
    print("=" * 80)

    if overall_success:
        print("🎉 [ALL SYSTEMS PERFECT] 모든 테스트, 거버넌스 대칭성, DB 스냅샷이 100% 무결합니다 (PROVEN).")
        return 0
    else:
        print("⚠️ [AUDIT FAILED] 무결성 검증에 실패한 항목이 있습니다. 상기 로그를 점검하십시오.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
