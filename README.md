# AbyssEmpire — Constraint-First LLM-Hybrid Somatic Simulator

| 항목 | 내용 |
| :--- | :--- |
| **프로젝트 명칭** | `AbyssEmpire (Constraint-First Somatic Engine)` |
| **아키텍처** | `Clean 4-Tier Layered Architecture (DDD + LLM Hybrid)` |
| **프로젝트 버전** | `v2.0.0` |
| **적용 거버넌스 규격** | `Constitution v2.0 (High-Assurance Specification)` |
| **검증 상태** | `16 Unit Tests 100% Pass (PROVEN)` |
| **원격 저장소** | [GitHub Repository](https://github.com/jinseobhong/AbyssEmpire-python-narrative) |

---

## 🌟 시스템 개요 (System Overview)

**AbyssEmpire**는 **제약 조건 역산 기법(Constraint-First Reverse Engineering)**과 **8중 해부학적 외모 규격(8-Tier Visual DNA)**, 그리고 **LLM의 확률적 추론(Probabilistic Inference)**을 결합한 하이브리드 고밀도 서사 시뮬레이션 시스템입니다.

- **🎯 제약 조건 역산 (Hard Invariants First)**: 캐릭터가 목숨보다 지키려는 불변 제약선을 먼저 역산하고 2대 서사 충돌 궤적(`V1` 저항 vs `V2` 붕괴) 도출.
- **🎨 8-Tier Visual DNA Matrix**: 안면 골격, 동공 광학, 모발 물리, 체형 실루엣, 표피 질감, 의복/초커, 생체 홍조, 조명 대비의 8중 규격을 확정하여 서사와 일러스트 태그(Danbooru)의 1:1 완벽 일치 및 외모 표류(Zero Drift) 보장.
- **🌊 신체 운동 연쇄 (Kinematic Chain)**: 시선 ➔ 목/성대 ➔ 흉곽/심박 ➔ 의복 장력 ➔ 손끝 악력 ➔ 족부 접지력으로 자극을 파동처럼 전이.
- **🧠 3-Tier 신경·메모리 원장**: `Layer 1 (반사계)`, `Layer 2 (단기버퍼)`, `Layer 3 (장기기억고)`를 영구 누적하여 100턴 대화에서도 인격 붕괴 방지.
- **🛡️ 원초적 어휘 승화 필터 & 초임계 관능 압축**: 세이프티 필터를 100% 안전하게 준수하면서도, 고밀도 문학적·생체역학적 개념어로 숨 막히는 서사적 텐션 창조.

---

## 🏛️ Clean 4-Tier 아키텍처 구조

```text
src/
├── domain/                               # 🧬 1. 순수 도메인 계층 (POPO)
│   ├── gene_seed.py                      # GENE SEED 해시 앵커링 (#NAME-70G-XXXX)
│   ├── visual_dna.py                     # 8-Tier 해부학적 외모 규격 모델
│   ├── personality_gene.py               # 7대 차원축 70단계 인격 유전자 & 제약선 모델
│   ├── somatic_ledger.py                 # 3계층 신경·메모리 원장 (Layer 1, Layer 2, Layer 3)
│   ├── spatial_pressure.py               # 3-Layer 공간 압력 챔버 (공적 ➔ 경계 ➔ 사적 밀실)
│   ├── kinematic_chain.py                # 7단계 신체 운동 연쇄 파동 전이 엔진
│   └── character.py                      # Character 애그리게이트 루트
│
├── infrastructure/                       # 🔌 2. 인프라 및 어댑터 계층
│   ├── llm/
│   │   ├── client.py                     # Gemini / Claude 멀티 LLM 클라이언트
│   │   └── prompt_synthesizer.py         # 30,000자급 헌법 & 턴별 서사 프롬프트 조립기
│   ├── media/
│   │   └── visual_compiler.py            # 서사용 문학 앵커 & Illustrious-XL 6-Slot 단부루 태그 컴파일러
│   └── database/
│       ├── db_manager.py                 # SQLite 트랜잭션 관리자
│       └── repositories.py               # Character & TurnLedger CRUD 리포지토리
│
├── application/                          # 🧠 3. 유스케이스 및 오케스트레이션 계층
│   ├── classifier_service.py             # [Dify Node 1] 제약선 역산 및 V1/V2 궤적 분류기
│   ├── gene_synthesis_service.py         # [Dify Node 2] 8-Tier 외모 + 70단계 유전자 동적 합성기
│   ├── narrative_orchestrator.py         # [Dify Node 3] 턴 오케스트레이터 & 3-Tier 원장 갱신
│   └── undo_manager.py                   # TurnSnapshot 기반 불변 롤백 관리자
│
└── presentation/                         # 🌐 4. 프레젠테이션 계층
    ├── cli.py                            # HITL Checkpoint 1 & 2 내장 터미널 CLI
    └── web/                              # 모듈화 웹 스튜디오 (static/, templates/, server.py)
```

---

## 🚀 빠른 시작 (Quick Start)

### 1. 단위 테스트 전수 검증 (Verification)
외부 라이브러리 없이 Python 내장 `unittest`로 3초 만에 16개 단위 테스트를 전수 검증합니다:
```bash
py -3 -m unittest discover -s tests/unit -v
```

### 2. 로컬 웹 스튜디오 원클릭 실행 (Web Studio)
```bash
py -3 app.py
```

### 3. HITL 2단계 결재선 내장 콘솔 CLI 실행 (Console)
```bash
py -3 -m src.presentation.cli
```