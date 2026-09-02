# FILESYSTEM_SPEC.md — 파일시스템 및 아키텍처 관측 뷰 규격서

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | SPEC-FS-001 |
| **표준 버전** | 1.0.0 (Hub-and-Spoke Architecture Edition) |
| **적용 범위** | 프로젝트 전체 디렉터리, iews/, .agents/, src/, 	ests/ |
| **상태** | ENFORCED (상시 강제 적용) |
| **최종 개정일** | 2026-09-02 |

---

## 📌 1. 목적 (Purpose)

본 사양서는 Antigravity 생태계 내 모든 프로젝트의 **디렉터리 계층 구조**, **5대 실시간 관측 뷰(iews/) 단일 진실(SSOT) 규격**, **브레인-프로젝트 자동 동기화(Twin-Call)** 및 **저장소 거버넌스 규칙**을 정의한다.

---

## 📂 2. 표준 파일시스템 계층 구조 (Standard Filesystem Hierarchy)

`	ext
<ProjectRoot>/
├── README.md                      # 프로젝트 비전 및 공식 진입 문서
├── views/                         # 👁️ [Project Live Views - 5대 실시간 관측 뷰]
│   ├── CURRENT_STATE.md           # [Core 1] 실시간 작업 닻, 당면 페이즈, 4단계 파이프라인 (SSOT)
│   ├── IMPLEMENTATION_STATUS.md   # [Core 2] 컴포넌트 진척 체크리스트 (TODO/WIP/PAUSED/DONE)
│   ├── IMPLEMENTATION_PLAN.md     # [Core 3] 현재 승인된 작업 상세 계획서 (Brain 동기화)
│   ├── WALKTHROUGH.md             # [Core 4] 작업 완료 및 터미널 AI Proof 검증 보고서
│   └── ARCHITECTURE.md            # [Core 5] 시스템 계층 구조, 도메인 경계 및 인터페이스 청사진
│
├── .agents/                       # 🌟 [Central Governance Hub - 거버넌스 허브]
│   ├── CONVENTIONS.md             # 🏛️ [Master Standards Hub] 모든 규격서의 중앙 인덱스
│   ├── GEMINI.md                  # 🔴 전역 최고 헌법 및 보안 가드레일 규격
│   ├── workflows/                 # 🎮 [Interactive Slash Commands] 인간 대화형 명령 인터페이스
│   ├── skills/                    # 🤖 [Autonomous Agent Skills] AI 자율 실행 런북
│   ├── docs/                      # 📄 도메인별 세부 사양서 및 템플릿
│   │   ├── CODING_STANDARDS.md    # 💻 파이썬 코딩 표준 및 타입/예외 규칙
│   │   ├── STYLE_GUIDE.md         # 📜 엔지니어링 문서 작성 스타일 가이드
│   │   ├── FILESYSTEM_SPEC.md     # [This File] 파일시스템 및 뷰 사양서
│   │   ├── LIFECYCLE_SPEC.md      # 🔄 2-Phase [Architect / Implement] 수명 주기
│   │   └── templates/             # 재사용 가능한 마크다운 템플릿
│   ├── scripts/                   # 🛠️ 검증 및 자동화 스크립트 (verify_sync, log_task)
│   └── store/                     # 🗄️ SQLite 감사 및 상태 저장소 (state.db, schema.sql)
│
├── src/                           # 💻 프로덕션 소스 코드 (Clean Architecture 4계층)
│   ├── domain/                    # 순수 비즈니스 엔티티 및 규칙
│   ├── infrastructure/            # 저장소 및 외부 어댑터
│   ├── application/               # 유스케이스 오케스트레이션
│   └── presentation/              # Web Studio, API, CLI
└── tests/                         # 🧪 자동화 테스트 슈트 (unit, integration, e2e)
`

---

## 🏛️ 3. iews/ 5대 핵심 실시간 관측 뷰 사양

| 문서명 | 국문 명칭 | 단일 진실 공급원(SSOT) 역할 및 내용 |
| :--- | :--- | :--- |
| **iews/CURRENT_STATE.md** | **현재 상황** | 현재 작업 중인 포커스, 활성 페이즈, 4단계 파이프라인 체크포인트. |
| **iews/IMPLEMENTATION_STATUS.md** | **구현 상황도** | 전사 컴포넌트별 4단 상태 마커([ ] TODO, [>] WIP, [⏸️] PAUSED, [x] DONE). |
| **iews/IMPLEMENTATION_PLAN.md** | **구현 계획** | 승인된 단위 작업 계획서 (파일 변경 목록, 실측 검증 계획). |
| **iews/WALKTHROUGH.md** | **구현 완료 (워크스루)** | 실제 터미널 실행 명령어 및 OS 출력 로그 원문(PROVEN)을 포함한 완료 보고서. |
| **iews/ARCHITECTURE.md** | **아키텍처 전체 설계도** | 계층형 아키텍처 다이어그램, 도메인 ERD, 인터페이스 계약 및 불변 제약. |

---

## 🔄 4. 브레인-프로젝트 트윈콜 동기화 규격 (Twin-Call Mirroring Mandate)

1. **설계 단계 (Architect Phase)**:
   - 에이전트가 <appDataDir>\brain\.../implementation_plan.md를 생성할 때, 반드시 <ProjectRoot>/views/IMPLEMENTATION_PLAN.md에 동일한 내용을 동시 기록(Twin-Call)하여 Git 버전 관리를 보장한다.
2. **구현 단계 (Implement Phase)**:
   - 에이전트가 <appDataDir>\brain\.../walkthrough.md를 생성할 때, 반드시 <ProjectRoot>/views/WALKTHROUGH.md에 동일한 내용을 동시 기록(Twin-Call)한다.
