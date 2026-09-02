# GIT_WORKFLOW_SPEC.md — Git 커밋 및 형상 관리 규격서

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `SPEC-GIT-001` |
| **표준 버전** | `v1.0.0` (Trunk-Based Agile Edition) |
| **적용 범위** | Antigravity 프로젝트 내 모든 Git 커밋, 브랜칭, 태깅, 스테이징 일체 |
| **상태** | `ENFORCED (상시 강제 적용)` |
| **최종 개정일** | `2026-09-02` |

---

## 📌 1. 목적 및 철학 (Purpose & Philosophy)

본 규격서는 Antigravity 환경에서 1인 개발자와 AI 에이전트가 협업할 때, **'메인라인 중심의 가볍고 빠른 트렁크 기반 개발(Trunk-Based Development)'**을 유지하면서도 **'완벽히 검증된 원자적 커밋(Atomic Commits with Verified AI Proof)'**만을 저장소에 기록하는 Git 형상 관리 표준을 정의한다.

---

## 🏛️ 2. 커밋 4대 절대 불변 규칙 (4 Commit Invariants)

### 2.1 Pre-Commit 무결성 통과 의무 (Zero Broken Commits)
- `py -3 .agents/scripts/run_checks.py`가 100% 통과(`Exit Code 0`, `PROVEN`)되지 않은 상태에서는 단 1건의 커밋도 생성할 수 없다.
- 깨진 테스트나 검증되지 않은 코드는 커밋될 수 없으며, 모든 커밋은 언제든 배포 가능한 상태를 유지해야 한다.

### 2.2 원자적 커밋 원칙 (Atomic Single-Purpose Commit)
- 1개의 커밋은 1개의 명확한 기능, 버그 패치, 혹은 거버넌스 갱신만을 포함해야 한다.
- 관련 없는 여러 파일의 변경을 한 번에 뒤섞어 커밋하는 행위를 금지한다.

### 2.3 SQLite 및 로컬 아티팩트 커밋 원천 차단 (Zero Artifact Pollution)
- `state.db`, `*.db-wal`, `*.db-shm` 등 SQLite 바이너리 파일과 `scratch/` 임시 파일은 `.gitignore`에 의해 완전 격리되어야 하며 Git 트래킹에 절대 포함되지 않는다.

### 2.4 인간 승인 기반 커밋 제안 (Human Review Before Commit)
- AI 에이전트는 파일 수정 직후 임의로 커밋하지 않으며, 변경 내역과 표준 커밋 메시지를 사용자에게 제안하고 승인을 득한 후 커밋을 집행한다.

---

## 🏷️ 3. Conventional Commits 7대 표준 접두어 규격

| 접두어 (Prefix) | 대상 작업 영역 | 커밋 메시지 권장 형식 |
| :--- | :--- | :--- |
| **`feat:`** | 신규 비즈니스 기능, 도메인 모델, API 추가 | `feat: implement SomaticGene immutable model` |
| **`fix:`** | 버그 수정, 런타임 결함 패치 | `fix: resolve sqlite lock on connection close` |
| **`gov:`** | 헌법, 규격서, 제안서, 거버넌스 스크립트 변경 | `gov: establish GIT_WORKFLOW_SPEC and update hub` |
| **`test:`** | 단위(Unit) 및 종단간(E2E) 테스트 추가/보강 | `test: add character roundtrip persistence e2e` |
| **`refactor:`** | 기능 동작 변경 없는 코드 리팩터링 및 성능 최적화 | `refactor: extract DatabaseManager context manager` |
| **`docs:`** | views/ 관측 뷰 및 사용자 문서 갱신 | `docs: sync CURRENT_STATE for phase 1 completion` |
| **`chore:`** | 패키지 의존성(`requirements.txt`), 설정 변경 | `chore: update requirements.txt with pydantic` |

---

## 🌿 4. 브랜치 전략 (Trunk-Based Branching)

1. **`main` 브랜치**:
   - 상시 개발 및 빌드가 무결하게 유지되는 단일 진실 메인라인(Trunk).
2. **`v0` 브랜치**:
   - 초기 레거시 베이스라인 백업 보존용 불변 브랜치.
3. **`v1` 브랜치**:
   - 마스터 거버넌스 템플릿 완성본 보존용 마일스톤 브랜치.
4. **`spike/` 브랜치 (선택적)**:
   - 파괴적 기술 검증이나 대규모 아키텍처 실험 시에만 단기 생성 후 폐기 또는 `main`으로 스쿼시 머지.

---

## 🏷️ 5. Git 저장소 명명 규칙 (Repository Naming Convention)

모든 Git 저장소는 색인성과 일관성을 위해 다음 표준 3단 구조를 준수한다:

`[git.]<ProjectName>-<DevelopmentEnvironment>-<Purpose>`

1. **Project Name**: 프로젝트 고유명사 (대문자 시작 카멜 표기)
2. **Development Environment**: 주 언어/런타임 (`Python`, `Common`, `Nodejs`, `Cpp` 등)
3. **Purpose**: 저장소 용도 (`StarterKit`, `Core`, `Cli`, `Backend`, `Frontend`, `Sdk` 등)
- 예시: `Antigravity-Python-StarterKit`, `Antigravity-Common-Core`

---

## 📝 6. 저장소 메타데이터 표준 (Description & Topics Guidelines)

GitHub 저장소 생성 및 관리 시 다음 표준 메타데이터를 필수로 지정한다:

1. **저장소 설명 (Description)**:
   - 120~160자 내외의 명쾌한 단문으로 `[대상 사용자] + [핵심 솔루션] + [차별화 가치]`를 기술 (국문/영문 표준 세트).
2. **토픽 태그 (GitHub Topics)**:
   - 5~8개의 검색 최적화(SEO) 핵심 기술/도메인 태그 지정.
- **`Antigravity-Python-StarterKit` 표준 세트**:
  - Description: `1인 개발자를 위한 초생산성 AI 페어 프로그래밍 마스터 거버넌스 & 클린 아키텍처 스타터 킷`
  - Topics: `ai-pair-programming`, `clean-architecture`, `python3`, `governance`, `starter-kit`, `sqlite-wal`, `solo-developer`, `antigravity`
- **`Antigravity-Common-Core` 표준 세트**:
  - Description: `모든 제품에 즉시 이식 가능한 플러그앤플레이 AI 에이전트 거버넌스 헌법, 7대 규격서 및 원클릭 검증 툴체인 코어`
  - Topics: `ai-agents`, `agent-governance`, `prompt-engineering`, `developer-tools`, `sqlite-audit`, `compliance`, `workflow-automation`

