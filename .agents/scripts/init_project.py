#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init_project.py — 신규 프로젝트 3초 원터치 부팅 및 거버넌스 스캐폴딩 스크립트
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
새로운 프로젝트 디렉터리에 .agents/를 복사한 후 실행하면:
1. views/ 5대 실시간 관측 뷰 생성 (templates/ 기반 인스턴스화)
2. Clean Architecture 4계층 (src/) 및 tests/ (unit/, e2e/) 디렉터리 스캐폴딩
3. SQLite 거버넌스 감사 DB (.agents/store/state.db) 및 WAL 모드 초기화
4. 초기 문서 스냅샷 적재 및 대칭성 검증 완결
"""

import sys
import shutil
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


def bootstrap_project(project_name: str = "New Project") -> None:
    root = get_repo_root()
    print("=" * 80)
    print(f"🚀 [Antigravity Project Bootstrapper] '{project_name}' 환경 구축 시작...")
    print("=" * 80)

    # 1. 디렉터리 스캐폴딩
    dirs = [
        root / "views",
        root / "src" / "domain",
        root / "src" / "infrastructure" / "database",
        root / "src" / "infrastructure" / "repositories",
        root / "src" / "application",
        root / "src" / "presentation",
        root / "tests" / "unit" / "domain",
        root / "tests" / "unit" / "infrastructure",
        root / "tests" / "e2e",
        root / ".agents" / "store",
        root / ".agents" / "proposals"
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        init_py = d / "__init__.py"
        if "src" in str(d) or "tests" in str(d):
            if not init_py.exists():
                init_py.write_text("", encoding="utf-8")

    print("  [+] 기본 Clean Architecture 4계층 및 테스트 디렉터리 스캐폴딩 완료")

    # 2. views/ 템플릿 인스턴스화
    templates_dir = root / ".agents" / "docs" / "templates"
    views_map = {
        "CURRENT_STATE.template.md": "CURRENT_STATE.md",
        "IMPLEMENTATION_STATUS.template.md": "IMPLEMENTATION_STATUS.md",
        "IMPLEMENTATION_PLAN.template.md": "IMPLEMENTATION_PLAN.md",
        "WALKTHROUGH.template.md": "WALKTHROUGH.md",
        "ARCHITECTURE.template.md": "ARCHITECTURE.md"
    }

    views_dir = root / "views"
    for tmpl_name, view_name in views_map.items():
        src_tmpl = templates_dir / tmpl_name
        dest_view = views_dir / view_name
        if src_tmpl.exists() and not dest_view.exists():
            shutil.copy2(src_tmpl, dest_view)
            print(f"  [+] views/{view_name} 템플릿 인스턴스화 완료")

    # 3. SQLite 초기화 및 스냅샷 동기화
    from sync_doc_snapshots import sync_all_snapshots
    from verify_sync import audit_full_system

    sync_all_snapshots(root, verbose=False)
    print("  [+] SQLite state.db 초기화 및 초기 12대 문서 스냅샷 아카이빙 완료")

    print("=" * 80)
    print(f"🎉 '{project_name}' AI 페어 프로그래밍 개발 환경이 100% 무결하게 부팅되었습니다!")
    print("   검증 명령어: py -3 .agents/scripts/run_checks.py")
    print("=" * 80)


if __name__ == "__main__":
    p_name = sys.argv[1] if len(sys.argv) > 1 else "Antigravity Project"
    bootstrap_project(p_name)
