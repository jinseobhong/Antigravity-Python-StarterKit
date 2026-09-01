# IMPLEMENTATION_PLAN.md — AbyssEngine 순수 도메인 계층(src/domain/) 구축 및 단위 테스트

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-DOMAIN-001` |
| **문서 버전** | `v1.0.0` |
| **작성 일자** | `2026-09-02` |
| **상태** | `APPROVED (사용자 사전 승인 완료)` |
| **작성자 / 승인자** | `AI Architect` / `Human Lead` |

---

## 📁 1. 변경 대상 파일 목록 (File Scope)

| 변경 구분 | 대상 파일 경로 | 변경 목적 및 구현 내용 |
| :---: | :--- | :--- |
| `[NEW]` | `src/domain/__init__.py` | 도메인 패키지 초기화 및 모듈 익스포트 |
| `[NEW]` | `src/domain/character.py` | Character 엔티티 및 LowenArmor (5대 로웬 신체 갑주) |
| `[NEW]` | `src/domain/pressure_stage.py` | PressureStage (4단계 신경생리학적 압력 궤적 상태 머신) |
| `[NEW]` | `src/domain/tensor_matrix.py` | 17대 생체 텐서 매트릭스 & Kinematic Chain 운동 연쇄 전이 엔진 |
| `[NEW]` | `src/domain/relational_vector.py` | 5대 범용 관계역학 상성 벡터 정의 |
| `[NEW]` | `src/domain/tension_grid.py` | N x N 상호 관계역학 및 질투/부채 매트릭스 |
| `[NEW]` | `src/domain/action_frame.py` | ActionFrame, ObservableEvent, SpeechAct (자연어 사건 모델) |
| `[NEW]` | `tests/unit/domain/test_character.py` | 로웬 갑주 및 캐릭터 속성 단위 테스트 |
| `[NEW]` | `tests/unit/domain/test_tensor_matrix.py` | 17대 텐서 외력 자극 및 운동 연쇄 파동 전이 테스트 |
| `[NEW]` | `tests/unit/domain/test_pressure_stage.py` | 압력 단계 전이 및 임계치 검증 테스트 |
| `[NEW]` | `tests/unit/domain/test_action_frame.py` | 화행 및 5D 정서 델타 데이터 모델 테스트 |
| `[MODIFY]` | `views/IMPLEMENTATION_STATUS.md` | 도메인 컴포넌트 5종 [WIP] 등록 |
| `[MODIFY]` | `views/CURRENT_STATE.md` | 진행 좌표 및 상태 동기화 |

---

## 🛠️ 2. 단계별 구현 순서 (Execution Steps)

1. **[1단계: 순수 도메인 모델 구현]**:
   - `src/domain/` 디렉토리에 외부 의존성(DB, HTTP) 없는 순수 POPO 엔티티 및 상태 머신 구현.
2. **[2단계: 단위 테스트 스위트 작성]**:
   - `tests/unit/domain/`에 각 도메인 모델의 엣지 케이스 및 인과율 검증 테스트 작성.
3. **[3단계: pytest 실측 테스트 실행 (AI Proof)]**:
   - `pytest tests/unit/domain/` 실행 및 100% Pass 원문 로그 확보.
4. **[4단계: SQLite 감사 로그 적재 및 상태 갱신]**:
   - `log_task.py`에 태스크 및 검증 로그 영구 적재.
   - `views/IMPLEMENTATION_STATUS.md` 도메인 항목 `[x] DONE` 갱신.
5. **[5단계: 워크스루 제출 및 원격 푸시]**:
   - `views/WALKTHROUGH.md` 쌍둥이 동기화 및 `auto_push.py`로 GitHub 배포.

---

## 🧪 3. 검증 계획 (Verification Plan)
- **명령어**: `pytest tests/unit/domain/ -v` 및 `py -3 .agents/scripts/verify_sync.py`
- **기준**: 모든 단위 테스트 100% Pass (0 failed, 0 errors) & 입증 등급 `PROVEN`
