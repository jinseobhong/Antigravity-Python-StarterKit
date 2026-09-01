# AbyssEmpire — Interactive Somatic Narrative Simulator

| 항목 | 내용 |
| :--- | :--- |
| **프로젝트 명칭** | `AbyssEmpire (AbyssEngine Core)` |
| **아키텍처** | `Clean 4-Tier Layered Architecture (DDD + Pure Domain)` |
| **프로젝트 버전** | `v1.0.0` |
| **적용 거버넌스 규격** | `Constitution v2.0 (High-Assurance Specification)` |
| **검증 상태** | `31 Unit Tests 100% Pass (PROVEN)` |
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
│   └── media/                     # Illustrious-XL 단부루 6-Slot 태그 컴파일러 & 초상화 클라이언트
│
├── application/                   # 🧠 3. 유스케이스 및 오케스트레이션 계층
│   ├── narrative_orchestrator.py  # 턴 라이프사이클 총괄 오케스트레이터
│   ├── undo_manager.py            # TurnSnapshot 기반 불변 롤백 스택 관리자
│   ├── character_workshop_service.py # 4대 로스터 시딩, 마스터 프롬프트, JSON I/O
│   └── action_parser_service.py   # 자연어 지문/대사 분할 및 화행 분석 서비스
│
└── presentation/                  # 🌐 4. 프레젠테이션 계층
    ├── prose_sanitizer.py         # 시스템 태그 완전 박멸 및 대사 서식 정제기
    ├── cli.py                     # 터미널 대화형 롤플레이 인터페이스
    └── web/                       # 컴포넌트 기반 모듈화 웹 스튜디오 (static/, templates/, server.py)
```

---

## 🚀 빠른 시작 (Quick Start)

### 1. 테스트 스위트 실행 (Verification)
외부 라이브러리 설치 없이 Python 내장 `unittest`로 0.5초 만에 31개 단위 테스트를 전수 검증합니다:
```bash
py -3 -m unittest discover -s tests/unit -v
```

### 2. 로컬 웹 스튜디오 원클릭 실행 (Web Studio)
```bash
py -3 app.py
```

### 3. 터미널 대화형 롤플레이 CLI 실행 (Console)
```bash
py -3 -m src.presentation.cli
```