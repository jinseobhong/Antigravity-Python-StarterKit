# IMPLEMENTATION_PLAN.md — .agents 문서 규격 전수 감사 및 파일/디렉토리 생성 자동화 스킬(scaffold) 구축

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-SCAFFOLD-001` |
| **문서 버전** | `v1.0.0` |
| **작성 일자** | `2026-09-02` |
| **상태** | `APPROVED (사용자 사전 승인 완료)` |
| **작성자 / 승인자** | `AI Architect` / `Human Lead` |

---

## 📁 1. 변경 대상 파일 목록 (File Scope)

| 변경 구분 | 대상 파일 경로 | 변경 목적 및 구현 내용 |
| :---: | :--- | :--- |
| `[AUDIT/MODIFY]` | `.agents/README.md`, `CONVENTIONS.md`, `GEMINI.md.example` | `STYLE_GUIDE.md` 표준 메타데이터 헤더 및 규격 전수 보강 |
| `[AUDIT/MODIFY]` | `.agents/docs/LIFECYCLE_SPEC.md` | 표준 메타데이터 헤더 및 RFC 2119 규격 보강 |
| `[NEW]` | `.agents/skills/scaffold/SKILL.md` | 파일/디렉토리 생성 시 컨벤션을 100% 자동 강제하는 AI 스캐폴딩 스킬 |
| `[NEW]` | `.agents/workflows/scaffold.md` | 대화형 파일/모듈 생성 슬래시 커맨드 (`/scaffold`) |
| `[MODIFY]` | `.agents/scripts/verify_sync.py` | 4대 워크플로우 ⟷ 스킬 검증 및 문서 규격 자동 검사 기능 추가 |
| `[MODIFY]` | `views/IMPLEMENTATION_STATUS.md` | `Governance.Scaffold` 컴포넌트 [WIP] 등록 |
| `[MODIFY]` | `views/CURRENT_STATE.md` | 진행 좌표 및 상태 동기화 |

---

## 🛠️ 2. 단계별 구현 순서 (Execution Steps)

1. **[1단계: .agents/ 내부 전 문서 전수 감사 및 보완]**:
   - `README.md`, `CONVENTIONS.md`, `GEMINI.md.example`, `LIFECYCLE_SPEC.md` 등 모든 문서 최상단에 표준 메타데이터 헤더 장착 및 기술 문체 통일.
2. **[2단계: 스캐폴딩 스킬 및 워크플로우 신설 (scaffold)]**:
   - **`skills/scaffold/SKILL.md`**: 명명 규칙(`snake_case`, `kebab-case`, `UPPER_SNAKE_CASE.md`) 및 메타데이터 자동 주입 런북.
   - **`workflows/scaffold.md`**: 1:1 대칭 슬래시 커맨드.
3. **[3단계: 자동 동기화 검증 스크립트 실행]**:
   - `py -3 .agents/scripts/verify_sync.py`를 실행하여 4대 워크플로우/스킬 1:1 대칭 및 무결성 검증 (`PROVEN`).
4. **[4단계: 실측 검증 및 이중 Git 동기화]**:
   - `views/WALKTHROUGH.md` 제출 및 GitHub 원격 저장소 푸시.

---

## 🧪 3. 검증 계획 (Verification Plan)
- **명령어**: `py -3 .agents/scripts/verify_sync.py` 및 Git 상태 검사
- **기준**: `.agents/` 전 문서 메타데이터 헤더 100% 장착 & `verify_sync.py` Pass (Exit code 0)
