# IMPLEMENTATION_PLAN.md — AbyssEngine 인프라 계층(src/infrastructure/) 재구축 및 검증

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-INFRA-001` |
| **문서 버전** | `v1.0.0` |
| **작성 일자** | `2026-09-02` |
| **상태** | `APPROVED (사용자 사전 승인 완료)` |
| **작성자 / 승인자** | `AI Architect` / `Human Lead` |

---

## 📁 1. 변경 대상 파일 목록 (File Scope)

| 변경 구분 | 대상 파일 경로 | 변경 목적 및 구현 내용 |
| :---: | :--- | :--- |
| `[NEW]` | `src/infrastructure/database/db_manager.py` | SQLite 트랜잭션 관리, 스키마 초기화 및 시드 데이터 적재 |
| `[NEW]` | `src/infrastructure/database/repositories.py` | Characters, Traits, TurnHistory, TensionGrid 전담 리포지토리 |
| `[NEW]` | `src/infrastructure/llm/config.py` | 중앙 환경변수(`.env`) 및 모델 풀 설정 로더 |
| `[NEW]` | `src/infrastructure/llm/client.py` | Gemini ➔ Claude 자동 캐스케이드 & 429 장애 극복 멀티 LLM 클라이언트 |
| `[NEW]` | `src/infrastructure/llm/prompt_builder.py` | Somatic Prose 주입 및 3+1 전술 선택지 프롬프트 조립기 |
| `[NEW]` | `src/infrastructure/media/portrait_client.py` | HuggingFace SD 초상화 생성 어댑터 |
| `[NEW]` | `tests/unit/infrastructure/test_db_manager.py` | SQLite DB 테이블 생성 및 CRUD 격리 테스트 |
| `[NEW]` | `tests/unit/infrastructure/test_llm_config.py` | LLM 설정 로딩 및 캐스케이드 해석 테스트 |
| `[MODIFY]` | `views/IMPLEMENTATION_STATUS.md` | 인프라 컴포넌트 4종 [WIP] 등록 |
| `[MODIFY]` | `views/CURRENT_STATE.md` | 진행 좌표 및 상태 동기화 |

---

## 🛠️ 2. 단계별 구현 순서 (Execution Steps)

1. **[1단계: 데이터베이스 어댑터 구현]**:
   - `db_manager.py` 및 `repositories.py`: 외래키(`PRAGMA foreign_keys = ON`) 활성화, 7개 테이블 CRUD 및 `src/domain/` 엔티티 매핑.
2. **[2단계: 멀티 LLM 탄력성 어댑터 구현]**:
   - `config.py` & `client.py`: 429 Quota Exceeded 및 타임아웃 발생 시 Gemini ➔ Claude 자동 스왑 캐스케이드 구현.
   - `prompt_builder.py`: 17대 텐서 및 70대 신체 헌법 노드를 문학적 프롬프트로 합성.
3. **[3단계: 단위 테스트 작성 및 실측 실행 (AI Proof)]**:
   - `tests/unit/infrastructure/` 실행 및 100% Pass 원문 로그 확보.
4. **[4단계: 상태 갱신 및 Git 자동 동기화]**:
   - `log_task.py` 적재, `views/WALKTHROUGH.md` 제출 및 `auto_push.py`로 GitHub 배포.

---

## 🧪 3. 검증 계획 (Verification Plan)
- **명령어**: `py -3 -m unittest discover -s tests/unit/infrastructure -v`
- **기준**: 모든 인프라 단위 테스트 100% Pass (0 errors)
