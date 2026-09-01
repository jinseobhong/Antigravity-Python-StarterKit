# IMPLEMENTATION_PLAN.md — Clean 4-Tier 웹 스튜디오(Web Studio) 신규 구축

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-WEB-001` |
| **문서 버전** | `v1.0.0` |
| **작성 일자** | `2026-09-02` |
| **상태** | `APPROVED (사용자 사전 승인 완료)` |
| **작성자 / 승인자** | `AI Architect` / `Human Lead` |

---

## 📁 1. 변경 대상 파일 목록 (File Scope)

| 변경 구분 | 대상 파일 경로 | 변경 목적 및 구현 내용 |
| :---: | :--- | :--- |
| `[NEW]` | `src/presentation/web/__init__.py` | 웹 프레젠테이션 패키지 초기화 |
| `[NEW]` | `src/presentation/web/server.py` | Clean 4-Tier 전용 Python 표준 http.server 및 Glassmorphism UI 서빙 |
| `[NEW]` | `tests/unit/presentation/test_web_server.py` | 웹 서버 API 핸들러 및 상태 동기화 단위 테스트 |
| `[MODIFY]` | `views/IMPLEMENTATION_STATUS.md` | 현황 갱신 |
| `[MODIFY]` | `views/CURRENT_STATE.md` | 진행 좌표 및 상태 동기화 |

---

## 🛠️ 2. 단계별 구현 순서 (Execution Steps)

1. **[1단계: src/presentation/web/server.py 구현]**:
   - `CharacterWorkshopService`, `NarrativeOrchestrator`, `DanbooruPromptBuilder`, `ProseSanitizer`를 100% 결합.
   - Glassmorphism & TailwindCSS 기반 고품격 다크 판타지 싱글 페이지 웹 UI 내장.
   - `/api/state`, `/api/characters`, `/api/select_character`, `/api/action`, `/api/undo`, `/api/create_character`, `/api/export_prompt` 엔드포인트 완비.
2. **[2단계: 단위 테스트 작성 및 전수 실행 (AI Proof)]**:
   - `tests/unit/presentation/test_web_server.py` 작성 및 전체 테스트 스위트 100% Pass 검증.
3. **[3단계: 상태 갱신 및 Git 자동 동기화]**:
   - `log_task.py` 적재 및 `auto_push.py` 실행.
4. **[4단계: 웹 서버 백그라운드 구동]**:
   - `py -3 -m src.presentation.web.server` 백그라운드 가동 및 브라우저 즉시 오픈.

---

## 🧪 3. 검증 계획 (Verification Plan)
- **명령어**: `py -3 -m unittest discover -s tests/unit -v`
- **기준**: 전체 단위 테스트 100% Pass (0 errors) & 입증 등급 `PROVEN`
