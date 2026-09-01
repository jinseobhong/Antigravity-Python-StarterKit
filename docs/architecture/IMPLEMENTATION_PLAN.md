# [PLAN-METH-001] 계약 주도 개발(CDD) & E2E 실측 테스트 오라클 방법론 수립 및 전면 주입 계획서

| 메타데이터 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-METH-001` |
| **문서 버전** | `v1.0.0 (Contract-Driven Development & E2E Oracle Edition)` |
| **상태** | `AWAITING_HUMAN_APPROVAL` |
| **적용 표준** | `AI ARCHITECT GLOBAL CONSTITUTION v2.0 & CDD / E2E Standards` |
| **기안일** | `2026-09-02` |

---

## 🎯 작업 목적 및 배경
- 유저에게 수동 검증을 전가하지 않고, AI 에이전트가 실제 사용자 관점(E2E)에서 웹 앱의 5대 핵심 루프(생성 ➔ 선택 ➔ 플레이 ➔ Undo/Reset ➔ 삭제)가 100% 무결하게 작동함을 기계적으로 입증하기 위한 개발 방법론을 정립합니다.
- `docs/architecture/DEVELOPMENT_GUIDE.md`를 단일 진실 공급원(SSOT)으로 제정하고, 5개 워크플로우 및 5개 스킬에 E2E 실측 검증 의무를 강제 규칙으로 주입합니다.

---

## 📋 세부 변경 계획

### 1) [NEW] `docs/architecture/DEVELOPMENT_GUIDE.md` 제정
- **1장: 계약 주도 개발 (CDD / API Contract Specification)**:
  - 프론트엔드(`api.js`)와 백엔드(`server.py`) 간 5대 REST API의 입력/출력 JSON 스키마 표준 정의.
- **2장: 실제 HTTP 트레이서 불릿 테스트 (E2E Tracer-Bullet Testing Standard)**:
  - Mock 기반 단위 테스트의 한계를 극복하고 실제 임시 HTTP 서버와 네트워크 페이로드를 검증하는 E2E 오라클 규격 정의.
- **3장: Fail-Visible UI 에러 가시성 가이드라인**:
  - 통신 실패, 유효성 실패 시 화면에 즉각적인 피드백(토스트/경고 모달)을 바인딩하는 프론트엔드 표준.

### 2) [MODIFY] 워크플로우 5종 & 스킬 5종에 CDD / E2E 실측 검증 게이트 주입
- `.agents/workflows/` (5개) & `.agents/skills/` (5개)
- 체크리스트에 **`[E2E Tracer-Bullet 실측 증거 획득 의무]`** 및 **`[API Contract 100% 준수 의무]`**를 추가하여 단위 테스트만으로 조기 완료 선언하는 것을 원천 차단.

### 3) [NEW] 실제 HTTP E2E 통합 테스트 스위트 (`tests/e2e/test_web_api_e2e.py`)
- Python `http.server` 임시 인스턴스 구동 ➔ `urllib.request`로 실제 HTTP API 연속 호출:
  1. `GET /api/state` : 초기 상태 및 상주 캐릭터 응답 검증
  2. `POST /api/characters/classify` : Dify Node 3 자연어 컨셉 역산 및 V1/V2 궤적 검증
  3. `POST /api/characters/compile-spec` : Dify Node 7 8-Tier DNA 및 70대 유전자 컴파일 검증
  4. `POST /api/create_character` : 캐릭터 DB 영구 저장 및 활성화 검증
  5. `POST /api/select_character` : 캐릭터 간 상주 인격 전환 검증
  6. `POST /api/action` : 5대 전술 칩 및 턴 서사 집필, 턴 원장(Ledger) 기록 검증
  7. `POST /api/undo` & `POST /api/reset` : 롤백 및 초기화 검증
  8. `POST /api/delete_character` : 캐릭터 삭제 및 차순위 자동 활성화 검증

### 4) [MODIFY] 백엔드 & 프론트엔드 통신 무결성 및 에러 가시성 보강
- `src/presentation/web/server.py`: API Contract와 100% 일치하도록 라우트 및 페이로드 핸들러 보강.
- `src/presentation/web/static/js/api.js` & `src/presentation/web/static/js/app.js`: 실패 시 콘솔 침묵 대신 `showToast("❌ " + error_msg)` 에러 가시성 전면 바인딩.

---

## 🧪 검증 계획
1. **단위 테스트 실행**: `py -3 -m unittest discover -s tests/unit -v` (13/13 PASS)
2. **E2E 통합 테스트 실행**: `py -3 -m unittest discover -s tests/e2e -v` (전체 E2E 시나리오 100% PASS)
3. **대칭성 및 스냅샷 감사**: `verify_sync.py` 및 `sync_doc_snapshots.py` 실행
4. **Git 동기화**: `auto_push.py` 실행 (백그라운드 데몬 잔존 프로세스 0개 확인)
