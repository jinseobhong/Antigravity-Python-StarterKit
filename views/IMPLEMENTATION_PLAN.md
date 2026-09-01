# IMPLEMENTATION_PLAN.md — AbyssEngine 유스케이스 및 프레젠테이션 계층 완결 구축

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-APP-PRES-001` |
| **문서 버전** | `v1.0.0` |
| **작성 일자** | `2026-09-02` |
| **상태** | `APPROVED (사용자 사전 승인 완료)` |
| **작성자 / 승인자** | `AI Architect` / `Human Lead` |

---

## 📁 1. 변경 대상 파일 목록 (File Scope)

| 변경 구분 | 대상 파일 경로 | 변경 목적 및 구현 내용 |
| :---: | :--- | :--- |
| `[NEW]` | `src/application/undo_manager.py` | TurnSnapshot 기반 불변 롤백 스택 관리자 |
| `[NEW]` | `src/application/action_parser_service.py` | 자연어 지문/대사 분할 및 화행 분석 서비스 |
| `[NEW]` | `src/application/character_service.py` | 캐릭터 생성, 결핍 특성 주입 및 워크숍 서비스 |
| `[NEW]` | `src/application/narrative_orchestrator.py` | 턴 라이프사이클 총괄 오케스트레이터 |
| `[NEW]` | `src/presentation/prose_sanitizer.py` | 시스템 태그 소멸 및 대사 줄바꿈 정제기 |
| `[NEW]` | `src/presentation/cli.py` | 터미널 대화형 롤플레이 인터페이스 |
| `[NEW]` | `tests/unit/application/test_undo_manager.py` | Undo/Rollback 스택 무결성 단위 테스트 |
| `[NEW]` | `tests/unit/application/test_action_parser_service.py` | 자연어 분할 및 화행 파싱 서비스 테스트 |
| `[NEW]` | `tests/unit/application/test_narrative_orchestrator.py` | 턴 오케스트레이션 및 상태 전이 통합 단위 테스트 |
| `[NEW]` | `tests/unit/presentation/test_prose_sanitizer.py` | 시스템 태그 박멸 정제기 단위 테스트 |
| `[MODIFY]` | `views/IMPLEMENTATION_STATUS.md` | 전체 컴포넌트 현황 갱신 |
| `[MODIFY]` | `views/CURRENT_STATE.md` | 진행 좌표 및 상태 동기화 |

---

## 🛠️ 2. 단계별 구현 순서 (Execution Steps)

1. **[1단계: application 계층 구현]**:
   - `undo_manager.py`, `action_parser_service.py`, `character_service.py`, `narrative_orchestrator.py` 구축.
2. **[2단계: presentation 계층 구현]**:
   - `prose_sanitizer.py` (시스템 태그 완전 박멸 및 대사 독립 분리) 및 `cli.py` 구축.
3. **[3단계: 단위 테스트 작성 및 실측 실행 (AI Proof)]**:
   - `tests/unit/` 전체 테스트 스위트 실행 및 전수 Pass 확인.
4. **[4단계: 상태 갱신 및 Git 자동 동기화]**:
   - `log_task.py` 적재, `views/WALKTHROUGH.md` 제출 및 `auto_push.py`로 GitHub 배포.

---

## 🧪 3. 검증 계획 (Verification Plan)
- **명령어**: `py -3 -m unittest discover -s tests/unit -v`
- **기준**: 전체 20+ 단위 테스트 100% Pass (0 errors) & 입증 등급 `PROVEN`
