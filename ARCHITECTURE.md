# ARCHITECTURE.md — 아키텍처 전체 설계도 (Blueprint)

## 1. 시스템 개요 및 핵심 목표 (System Overview)
- **시스템 목적**: Google Antigravity 에이전트 환경에서 1인 개발 및 페어 프로그래밍 시, AI의 무단 자의적 판단과 환각을 방지하고 고신뢰도 소프트웨어를 기민하게 생산하는 전역 거버넌스 및 워크플로우 인프라.
- **핵심 아키텍처 패턴**: Two-Tier Hybrid Architecture (실시간 관측 뷰 Markdown + 영구 누적 로그 SQLite Store + Git Submodule Hub).

---

## 2. 계층 구조 및 모듈 인터페이스 (Layered Architecture & Boundaries)

```text
[Tier 1: Global Supreme Constitution (전역 최고 헌법)]
   └── user_global (GEMINI.md) ──→ 상시 강제 (ALWAYS ON)

[Tier 2: Central Governance & Customization Hub (.agents/)]
   ├── workflows/workflow.md    ──→ 2-Phase 실전 페어링 파이프라인
   ├── skills/workflow/SKILL.md ──→ 자동 활성화 실행 런북
   ├── docs/templates/          ──→ 5대 표준 문서 템플릿
   ├── store/schema.sql         ──→ SQLite 영구 누적 로그 저장소
   └── CONVENTIONS.md           ──→ 파일 시스템 및 명명 규칙 공식 명세

[Tier 3: Project 5 Core Live Views (실시간 관측 뷰 5종)]
   ├── CURRENT_STATE.md         ──→ 👁️ [1] 당면 작업 및 5단계 파이프라인 좌표 (SSOT)
   ├── IMPLEMENTATION_STATUS.md ──→ 👁️ [2] 전체 컴포넌트 완성도 현황판
   ├── IMPLEMENTATION_PLAN.md   ──→ 👁️ [3] 구현 계획서 (세션 브레인 자동 미러링)
   ├── WALKTHROUGH.md           ──→ 👁️ [4] 구현 완료 보고서 (세션 브레인 자동 미러링)
   └── ARCHITECTURE.md          ──→ 👁️ [5] 시스템 설계 청사진
```

---

## 3. 핵심 기술 스택 및 제약 조건 (Tech Stack & Constraints)
- **런타임 및 IDE**: Google Antigravity Agentic IDE
- **설정 및 명세 형식**: YAML Frontmatter + GitHub Flavored Markdown
- **영구 로깅 스키마**: SQLite 3 (`.agents/store/schema.sql`)
- **형상 관리**: Git + Git Submodules (이중 분리 저장소 구조)
