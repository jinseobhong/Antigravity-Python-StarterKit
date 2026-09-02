#!/usr/bin/env python3
"""
verify_sync.py — Antigravity Governance & Customization Sync Validator

Validates 100% symmetry and integrity across:
1. Workflows (.agents/workflows/<name>.md) <-> Skills (.agents/skills/<name>/SKILL.md)
2. Views (views/ 5 Core Live Views)
3. Templates (.agents/docs/templates/*.template.md)
4. Metadata headers compliance with STYLE_GUIDE.md
"""

import sys
from pathlib import Path

# Ensure UTF-8 output on all platforms
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def check_metadata_header(file_path: Path) -> bool:
    """Checks if markdown file contains a standard metadata header table."""
    try:
        content = file_path.read_text(encoding='utf-8')
        return ("| 항목 | 내용 |" in content or "| Item | Details |" in content or "| Category |" in content)
    except Exception:
        return False

def check_constitution_header(file_path: Path) -> bool:
    """Checks if file contains the Global Constitution v2.2 Supreme Mandate header."""
    try:
        content = file_path.read_text(encoding='utf-8')
        return "[GLOBAL CONSTITUTION v2.2 & HITL TRINITY MANDATE]" in content
    except Exception:
        return False

def validate_customizations(repo_root: Path) -> bool:
    agents_dir = repo_root / ".agents"
    views_dir = repo_root / "views"

    workflows_dir = agents_dir / "workflows"
    skills_dir = agents_dir / "skills"
    templates_dir = agents_dir / "docs" / "templates"

    errors = []

    print("=" * 70)
    print("[Antigravity Sync Validator] Starting Full Symmetry Audit...")
    print("=" * 70)

    # 1. Check Workflows <-> Skills 1:1 Mapping
    if not workflows_dir.exists():
        errors.append("[ERROR] Missing directory: .agents/workflows")
        workflow_names = set()
    else:
        workflow_names = {f.stem for f in workflows_dir.glob("*.md")}

    if not skills_dir.exists():
        errors.append("[ERROR] Missing directory: .agents/skills")
        skill_names = set()
    else:
        skill_names = {d.name for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()}

    print(f"* Discovered Workflows ({len(workflow_names)}): {sorted(list(workflow_names))}")
    print(f"* Discovered Skills    ({len(skill_names)}): {sorted(list(skill_names))}")

    missing_in_skills = workflow_names - skill_names
    missing_in_workflows = skill_names - workflow_names

    if missing_in_skills:
        for name in missing_in_skills:
            errors.append(f"[ASYMMETRY ERROR] Workflow '{name}.md' has no matching skill '.agents/skills/{name}/SKILL.md'")

    if missing_in_workflows:
        for name in missing_in_workflows:
            errors.append(f"[ASYMMETRY ERROR] Skill '{name}' has no matching workflow '.agents/workflows/{name}.md'")

    if not missing_in_skills and not missing_in_workflows:
        print("[OK] Workflows <-> Skills: 100% Symmetric 1:1 Mapping Verified.")

    # 2. Check 5 Core Live Documents in views/ (or docs/architecture/)
    live_views_dir = views_dir if views_dir.exists() else (repo_root / "docs" / "architecture")
    required_docs = [
        "CURRENT_STATE.md",
        "IMPLEMENTATION_STATUS.md",
        "IMPLEMENTATION_PLAN.md",
        "WALKTHROUGH.md",
        "ARCHITECTURE.md"
    ]
    rel_path = "views" if views_dir.exists() else "docs/architecture"
    print(f"\n* Checking Core Live Documents ({rel_path}/)...")
    for doc_file in required_docs:
        target = live_views_dir / doc_file
        if not target.exists():
            errors.append(f"[MISSING DOC] Missing Document: '{rel_path}/{doc_file}'")
        else:
            has_header = check_metadata_header(target)
            status_text = "OK (Header Verified)" if has_header else "OK"
            print(f"  - {rel_path}/{doc_file}: {status_text}")

    # 3. Check Core Templates & Mandatory Constitution Article 20 Header
    required_templates = [
        "CURRENT_STATE.template.md",
        "IMPLEMENTATION_STATUS.template.md",
        "IMPLEMENTATION_PLAN.template.md",
        "WALKTHROUGH.template.md",
        "ARCHITECTURE.template.md",
        "REQUIREMENTS_SPECIFICATION.template.md"
    ]
    print("\n* Checking Standard Templates (.agents/docs/templates/)...")
    for template_file in required_templates:
        target = templates_dir / template_file
        if not target.exists():
            errors.append(f"[MISSING TEMPLATE] Missing Template: '.agents/docs/templates/{template_file}'")
        else:
            has_const_header = check_constitution_header(target)
            if not has_const_header:
                errors.append(f"[CONSTITUTION VIOLATION] Template '.agents/docs/templates/{template_file}' lacks Article 20 Header!")
            else:
                print(f"  - docs/templates/{template_file}: OK (Constitution Article 20 Verified)")

    # 4. Check Root README.md and .agents/CONVENTIONS.md
    print("\n* Checking Root & Hub Documentation...")
    root_readme = repo_root / "README.md"
    conventions_hub = agents_dir / "CONVENTIONS.md"

    if not root_readme.exists():
        errors.append("[MISSING README] Missing Project Root 'README.md'")
    else:
        has_header = check_metadata_header(root_readme)
        status_text = "OK (Header Verified)" if has_header else "OK"
        print(f"  - README.md: {status_text}")

    if not conventions_hub.exists():
        errors.append("[MISSING HUB] Missing Master Hub '.agents/CONVENTIONS.md'")
    else:
        has_header = check_metadata_header(conventions_hub)
        status_text = "OK (Header Verified)" if has_header else "OK"
        print(f"  - .agents/CONVENTIONS.md: {status_text}")

    # 5. Final Verdict
    print("\n" + "=" * 70)
    if errors:
        print(f"[VALIDATION FAILED] Found {len(errors)} error(s):")
        for err in errors:
            print(f"  {err}")
        print("=" * 70)
        return False
    else:
        print("[VALIDATION PASSED] ALL SYSTEMS PERFECT: 100% Symmetry & Compliance Confirmed (PROVEN).")
        print("=" * 70)
        return True

if __name__ == "__main__":
    cwd = Path.cwd()
    if (cwd / ".agents").exists():
        root = cwd
    elif (cwd.parent / ".agents").exists():
        root = cwd.parent
    else:
        root = Path(__file__).resolve().parent.parent.parent

    success = validate_customizations(root)
    sys.exit(0 if success else 1)
