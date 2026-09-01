# AbyssEmpire — Interactive Somatic Narrative Simulator

| 항목 | 내용 |
| :--- | :--- |
| **프로젝트 명칭** | `AbyssEmpire (AbyssEngine Core)` |
| **아키텍처** | `Clean 4-Tier Layered Architecture (DDD + Pure Domain)` |
| **현재 버전** | `v2.0.0 (High-Assurance Architecture Edition)` |
| **검증 상태** | `23 Unit Tests 100% Pass (PROVEN)` |
| **원격 저장소** | [GitHub Repository](https://github.com/jinseobhong/AbyssEmpire-python-narrative) |

---

## 🌟 시스템 개요 (System Overview)

**AbyssEngine**은 **100% 결정론적인 파이썬 생체 물리 엔진**과 **문학적 서사를 집필하는 멀티 LLM(Gemini / Claude)**을 결합한 하이브리드 인터랙티브 서사 시뮬레이션 시스템입니다.

- **결정론적 생체 역학**: 5대 로웬 신체 갑주(`LowenArmor`), 17대 생체·의복 텐서, 7단계 신체 운동 연쇄(`Kinematic Chain`) 파동 전이.
- **탄력적 멀티 LLM 캐스케이드**: 429 Quota Exceeded 및 장애 발생 시 Gemini ➔ Claude 실시간 자동 스왑.
- **불변 스냅샷 롤백 (Undo)**: `TurnSnapshot` 스택 기반 100% 오차 없는 이전 턴 상태 복원.
- **N x N 관계역학 그리드**: 캐릭터 간 질투/부채/오염도 상호작용 매트릭스.

---

## 🏛️ Clean 4-Tier 아키텍처 구조

```text
src/
├── domain/                        # 🧬 1. 순수 도메인 계층 (외부 의존성 제로 POPO)
│   ├── character.py               # Character 엔티티 및 LowenArmor (5대 로웬 신체 갑주)
│   ├── pressure_stage.py          # 4단계 신경생리학적 압력 궤적 상태 머신
│   ├── tensor_matrix.py           # 17대 생체 텐서 & Kinematic Chain 운동 연쇄 전이 엔진
│   ├── relational_vector.py       # 5대 범용 관계역학 상성 벡터
│   ├── tension_grid.py            # N x N 캐릭터 관계역학 및 질투/부채 매트릭스
│   └── action_frame.py            # ActionFrame & ObservableEvent 모델
│
├── infrastructure/                # 🔌 2. 인프라 및 어댑터 계층
│   ├── database/                  # SQLite 트랜잭션 매니저 및 CRUD 리포지토리
│   ├── llm/                       # Gemini ➔ Claude 자동 스왑 멀티 LLM 클라이언트 & 프롬프트 빌더
│   └── media/                     # HuggingFace SD 초상화 렌더링 어댑터
│
├── application/                   # 🧠 3. 유스케이스 및 오케스트레이션 계층
│   ├── narrative_orchestrator.py  # 턴 라이프사이클 총괄 오케스트레이터
│   ├── undo_manager.py            # TurnSnapshot 기반 불변 롤백 스택 관리자
│   ├── action_parser_service.py   # 자연어 지문/대사 분할 및 화행 분석 서비스
│   └── character_service.py       # 캐릭터 생성 및 시드 관리 서비스
│
└── presentation/                  # 🌐 4. 프레젠테이션 계층
    ├── prose_sanitizer.py         # 시스템 태그 완전 박멸 및 대사 서식 정제기
    └── cli.py                     # 터미널 대화형 롤플레이 인터페이스
```

---

## 🚀 빠른 시작 (Quick Start)

### 1. 테스트 스위트 실행 (Verification)
외부 라이브러리 설치 없이 Python 내장 `unittest`로 0.3초 만에 23개 단위 테스트를 전수 검증합니다:
```bash
py -3 -m unittest discover -s tests/unit -v
```

### 2. 터미널 대화형 롤플레이 CLI 실행
```bash
py -3 -m src.presentation.cli
```

---

## 📁 `views/` 5대 실시간 관측 뷰 (The 5 Core Live Views)

본 프로젝트는 Antigravity 에이전트와 완벽한 실시간 싱크를 유지하기 위해 `views/` 디렉토리에 5대 실시간 관측 뷰를 운용합니다:

1. **[views/CURRENT_STATE.md](./views/CURRENT_STATE.md)**: 실시간 당면 과제, 현재 페이즈 및 5단계 파이프라인 좌표 (SSOT)
2. **[views/IMPLEMENTATION_STATUS.md](./views/IMPLEMENTATION_STATUS.md)**: 전체 시스템 컴포넌트 완성도 현황판 (`TODO` / `WIP` / `DONE`)
3. **[views/IMPLEMENTATION_PLAN.md](./views/IMPLEMENTATION_PLAN.md)**: 현재 작업 세부 계획서 (세션 브레인 실시간 미러링)
4. **[views/WALKTHROUGH.md](./views/WALKTHROUGH.md)**: 작업 구현 완료 및 AI 실측 검증 보고서 (세션 브레인 실시간 미러링)
5. **[views/ARCHITECTURE.md](./views/ARCHITECTURE.md)**: 7대 고신뢰도 아키텍처 및 시스템 전체 설계 청사진

---

## 🌟 중앙 거버넌스 허브 (.agents/)

본 프로젝트의 `.agents/` 디렉토리는 [Antigravity-Common-Core](https://github.com/jinseobhong/Antigravity-Common-Core) 중앙 저장소와 **Git Submodule**로 연결되어 있습니다:

- **[CONVENTIONS.md](./.agents/CONVENTIONS.md)**: 파일 시스템 구조 및 1:1 대칭 명명 규칙
- **[workflows/](./.agents/workflows/)**: 5대 대화형 슬래시 커맨드 (`/main-stream`, `/architect`, `/implement`, `/scaffold`, `/reverse-engineer`)
- **[skills/](./.agents/skills/)**: 5대 AI 전문 런북 모듈
- **[scripts/](./.agents/scripts/)**: 자동화 도구 (`verify_sync.py`, `auto_push.py`, `log_task.py`)