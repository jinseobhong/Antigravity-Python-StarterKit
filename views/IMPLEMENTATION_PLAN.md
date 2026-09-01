# IMPLEMENTATION_PLAN.md — 리버스 엔지니어링(reverse-engineer) 전용 스킬 및 워크플로우 구축

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-REVERSE-001` |
| **문서 버전** | `v1.0.0` |
| **작성 일자** | `2026-09-02` |
| **상태** | `APPROVED (사용자 사전 승인 완료)` |
| **작성자 / 승인자** | `AI Architect` / `Human Lead` |

---

## 📁 1. 변경 대상 파일 목록 (File Scope)

| 변경 구분 | 대상 파일 경로 | 변경 목적 및 구현 내용 |
| :---: | :--- | :--- |
| `[NEW]` | `.agents/skills/reverse-engineer/SKILL.md` | 레거시 코드 정밀 분석, 도메인/엔티티 추출 및 블루프린트 합성 런북 |
| `[NEW]` | `.agents/workflows/reverse-engineer.md` | 대화형 리버스 엔지니어링 슬래시 커맨드 (`/reverse-engineer`) |
| `[MODIFY]` | `.agents/CONVENTIONS.md` | 신규 5대 워크플로우/스킬 등록 |
| `[MODIFY]` | `.agents/README.md` | 신규 스킬 인덱싱 |
| `[MODIFY]` | `views/IMPLEMENTATION_STATUS.md` | `Governance.ReverseEngineer` 컴포넌트 [WIP] 등록 |
| `[MODIFY]` | `views/CURRENT_STATE.md` | 진행 좌표 및 상태 동기화 |

---

## 🛠️ 2. 단계별 구현 순서 (Execution Steps)

1. **[1단계: reverse-engineer 스킬 및 워크플로우 신설]**:
   - `skills/reverse-engineer/SKILL.md`: 레거시 코드 탐색, 비즈니스 엔티티/룰 추출, `views/ARCHITECTURE.md` 합성 절차 정의.
   - `workflows/reverse-engineer.md`: 1:1 대칭 슬래시 커맨드 생성.
2. **[2단계: CONVENTIONS.md 및 README.md 업데이트]**:
   - 5대 워크플로우 ⟷ 스킬 구조 반영.
3. **[3단계: verify_sync.py 무결성 검증]**:
   - 5대 워크플로우/스킬 1:1 대칭성 기계적 검증 실행.
4. **[4단계: auto_push.py 및 완료 보고]**:
   - SQLite 로깅 및 GitHub 원격 저장소 동시 푸시.

---

## 🧪 3. 검증 계획 (Verification Plan)
- **명령어**: `py -3 .agents/scripts/verify_sync.py`
- **기준**: 5대 워크플로우 ⟷ 스킬 1:1 대칭성 100% 검증 통과 (Exit Code 0)
