# [WALKTHROUGH : Contract-Driven Development & E2E Tracer-Bullet Verification]

| 메타데이터 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `WALKTHROUGH-METH-001` |
| **문서 버전** | `v1.0.0 (CDD & E2E HTTP Test Oracle Edition)` |
| **입증 상태** | `PROVEN (13 Unit Tests + 4 E2E HTTP Integration Scenarios 100% PASS)` |
| **적용 표준** | `OpenAPI / CDD Contract SSOT & Python E2E Testing Standard` |
| **최종 검증일** | `2026-09-02` |

---

## 🏛️ 1. 계약 주도 개발(CDD) & E2E 실측 테스트 오라클 완성 요약

더 이상 Mock 단위 테스트에만 의존하여 유저에게 수동 검증을 전가하지 않고, **실제 브라우저(`api.js`)가 보내는 5대 REST API 페이로드를 실제 임시 HTTP 서버에 전송하여 [생성 ➔ V1/V2 선택 ➔ 스펙 컴파일 ➔ DB 영구 저장 ➔ 캐릭터 전환 ➔ 턴 전송 ➔ 롤백 ➔ 삭제] 5대 시나리오를 기계적으로 100% 실측 검증(`PROVEN`)**하였습니다.

---

## 🧪 2. E2E 및 단위 테스트 실측 증거 (AI Proof & Test Oracles)

### 1) 단위 테스트 (13/13 PASS)
`py -3 -m unittest discover -s tests/unit -v` ➔ **OK (13 tests passed in 3.84s)**

### 2) 실제 HTTP E2E 통합 테스트 (4/4 PASS)
`py -3 -m unittest discover -s tests/e2e -v`:
```text
test_01_get_initial_state_and_characters (test_web_api_e2e.TestWebAPIEndToEnd) ... 
  GET /api/state 200 OK & GET /api/characters 200 OK -> ok
test_02_full_character_creation_and_apply_flow (test_web_api_e2e.TestWebAPIEndToEnd) ... 
  POST /api/characters/classify 200 OK
  POST /api/characters/compile-spec 200 OK
  POST /api/create_character 200 OK
  GET /api/state 200 OK -> ok
test_03_roleplay_turn_execution_undo_and_reset (test_web_api_e2e.TestWebAPIEndToEnd) ... 
  POST /api/action (Turn 1) 200 OK
  POST /api/action (Turn 2) 200 OK
  POST /api/undo (Rollback) 200 OK
  POST /api/reset (Clear) 200 OK -> ok
test_04_select_and_delete_character (test_web_api_e2e.TestWebAPIEndToEnd) ... 
  POST /api/select_character 200 OK
  POST /api/delete_character 200 OK -> ok

----------------------------------------------------------------------
Ran 4 tests in 3.719s

OK (100% PROVEN)
```

---

## 📁 3. 신규 및 개정 산출물 목록

1. **[신규 가이드] [`docs/architecture/DEVELOPMENT_GUIDE.md`](file:///d:/Development/projects/antigravity/아키텍트%20설계안/docs/architecture/DEVELOPMENT_GUIDE.md)**: 5대 REST API 통신 계약 SSOT 및 E2E/Fail-Visible UI 표준 제정
2. **[신규 E2E 테스트] [`tests/e2e/test_web_api_e2e.py`](file:///d:/Development/projects/antigravity/아키텍트%20설계안/tests/e2e/test_web_api_e2e.py)**: 실제 임시 HTTP 서버 기반 5대 시나리오 자동 검증기
3. **[거버넌스 개정] 워크플로우 5종 & 스킬 5종**: CDD 계약 준수 및 E2E 실측 테스트 통과 의무 조항 전면 주입
4. **[통신 일치] `server.py`, `api.js`, `app.js`**: 5대 REST API 통신 규격 1:1 완전 일치 및 Fail-Visible 토스트 연동
