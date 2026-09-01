# ARCHITECTURE.md — AbyssEmpire Core Architecture Specification

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `ARCH-ABYSS-002` |
| **문서 버전** | `v2.0.0 (Constraint-First LLM Hybrid Edition)` |
| **작성 일자** | `2026-09-02` |
| **상태** | `APPROVED (인간 승인 완료)` |
| **적용 거버넌스 규격** | `Constitution v2.0 (High-Assurance Specification)` |

---

## 🌟 1. 시스템 핵심 철학 (Core Philosophy & Soul)

**AbyssEmpire**는 기계적이고 딱딱한 수식 계산기가 아닌, **LLM의 풍부한 확률적 추론(Probabilistic Inference)과 파이썬의 고신뢰도 오케스트레이션(Sovereign Orchestration)이 결합된 하이브리드 고밀도 서사 시뮬레이터**입니다.

### 4대 핵심 아키텍처 기둥
1. **🎯 제약 조건 역산 기법 (Constraint-First Reverse Engineering)**:
   - 캐릭터 생성 시 뜬구름 잡는 성격이 아닌, **절대 무너지지 않아야 할 불변 제약선(Hard Invariants)**을 먼저 역산하고, 이로부터 2대 서사 충돌 궤적(`V1` 저항 vs `V2` 붕괴)을 도출.
2. **🎨 8중 해부학적 외모 규격 (8-Tier Visual DNA Matrix)**:
   - 안면 골격, 동공 광학, 모발 물리, 체형 실루엣, 표피 질감, 의복/초커, 생체 홍조, 환경광의 8중 규격을 확정하여 **서사 묘사와 이미지 생성(Danbooru)의 1:1 완벽 일치 및 외모 표류(Zero Drift) 보장**.
3. **🛡️ 원초적 어휘 승화 필터 & 초임계 관능 압축**:
   - 세이프티 필터를 100% 안전하게 통과하면서도, 계면 마찰, 나노 호흡 파열, 0.1초 신경 연쇄, 쇄골의 열감 등 **고밀도 문학적·생체역학적 개념어로 극상의 관능미와 서사적 텐션을 창조**.
4. **🧠 3계층 신경·메모리 원장 & 신체 운동 연쇄 (Kinematic Chain)**:
   - `Layer 1 (반사계)`, `Layer 2 (단기버퍼)`, `Layer 3 (장기기억고)`를 실시간으로 갱신하여 100턴 대화에서도 캐릭터의 인격과 기억을 영구 보존.

---

## 🏛️ 2. Clean 4-Tier 레이어드 아키텍처 구조

```text
src/
├── domain/                               # 🧬 1. 순수 도메인 계층 (POPO)
│   ├── gene_seed.py                      # GENE SEED 해시 앵커링 (#NAME-70G-XXXX)
│   ├── visual_dna.py                     # 8-Tier 해부학적 외모 규격 모델
│   ├── personality_gene.py               # 7대 차원축 70단계 인격 유전자 & 제약선 모델
│   ├── somatic_ledger.py                 # 3계층 신경·메모리 원장 (Layer 1, Layer 2, Layer 3)
│   ├── spatial_pressure.py               # 3-Layer 공간 압력 챔버 (공적 ➔ 경계 ➔ 사적 밀실)
│   └── kinematic_chain.py                # 7단계 신체 운동 연쇄 파동 전이 엔진
│
├── infrastructure/                       # 🔌 2. 인프라 및 어댑터 계층
│   ├── llm/
│   │   ├── client.py                     # Gemini / Claude 자동 스왑 멀티 LLM 클라이언트
│   │   └── prompt_synthesizer.py         # 30,000자급 헌법 및 턴별 서사 프롬프트 조립기
│   ├── media/
│   │   └── visual_compiler.py            # 서사용 문학 앵커 & Illustrious-XL 6-Slot 단부루 태그 컴파일러
│   └── database/
│       ├── db_manager.py                 # SQLite 트랜잭션 관리자
│       └── repositories.py               # Character / Ledger / Spec CRUD 리포지토리
│
├── application/                          # 🧠 3. 유스케이스 및 오케스트레이션 계층
│   ├── classifier_service.py             # [Dify Node 1] 제약선 역산 및 V1/V2 궤적 분류 서비스
│   ├── gene_synthesis_service.py         # [Dify Node 2] 8-Tier 외모 + 70단계 유전자 동적 합성
│   ├── narrative_orchestrator.py         # [Dify Node 3] 턴 오케스트레이션 & 3-Tier 원장 갱신
│   └── undo_manager.py                   # TurnSnapshot 기반 불변 롤백 관리자
│
└── presentation/                         # 🌐 4. 프레젠테이션 계층
    ├── cli.py                            # HITL Checkpoint 1 & 2가 내장된 터미널 롤플레이
    └── web/                              # 모듈화 웹 스튜디오 (static/css, static/js, templates/)
```

---

## 🔄 3. 전체 라이프사이클 파이프라인 (The 5-Step Pipeline)

```text
[1. 사용자 입력 (예: "오만한 제1황녀")]
        ↓ (classifier_service)
【2. 제약선 역산 및 2대 서사 충돌 궤적 도출】
        ├── 불변 제약선: "선조 가문의 부채와 순결 서약"
        ├── V1: 차가운 귀족적 저항과 방어선 고수
        └── V2: 강렬한 프라이드 붕괴와 소마틱 동기화
        ↓
🛑 【Human Checkpoint 1: 궤적 결재 (V1 vs V2)】
        ↓ (gene_synthesis_service & visual_compiler)
【3. 8-Tier Visual DNA & 70단계 유전자 마스터 헌법 컴파일】
        ├── 8중 외모 규격 & 단부루 6-Slot 태그 발급
        └── 25,000 ~ 30,000자급 마스터 프롬프트 생성
        ↓
🛑 【Human Checkpoint 2: 캐릭터 헌법 승인】
        ↓ (narrative_orchestrator)
【4. 실시간 1:1 서사 롤플레이 (하이브리드 비결정론적 생성)】
        ├── 3-Layer 공간 압력 해금 (공적 ➔ 경계 ➔ 사적 밀실)
        ├── 신체 운동 연쇄(Kinematic Chain) & 2~3 스포트라이트
        ├── 3계층 신경·메모리 원장(Layer 1/2/3) 동적 누적
        └── 단부루 태그 실시간 복사 및 원클릭 Undo 롤백
```
