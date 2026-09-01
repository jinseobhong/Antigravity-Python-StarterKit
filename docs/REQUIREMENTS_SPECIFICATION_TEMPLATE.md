# [프로젝트 요구사항 정의서 양식 : SRS Template]

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `SRS-TEMPLATE-001` |
| **문서 버전** | `v1.0.0` |
| **용도** | `High-Assurance AI Narrative & System Requirements Blueprint` |

---

## 1. 프로젝트 비전 및 핵심 철학 (Vision & Philosophy)
- **Q1. 단 하나의 궁극적인 재미/경험 (Ultimate Core Value)**
  - 이 시스템/서사 시뮬레이터가 유저에게 제공해야 하는 핵심 재미와 궁극적 경험은 무엇인가요?
  - → 
- **Q2. 절대 타협할 수 없는 핵심 철학 (Non-Negotiable Principles)**
  - 시스템 동작 시 반드시 지켜져야 하는 철학 (예: 비결정론적 확률 추론, 문학적 긴장감, 무(無)수치 순수 감각어 묘사 등)은 무엇인가요?
  - → 

---

## 2. 캐릭터 생성 메커니즘 (Character Creation & Generation)
- **Q1. 사용자 최초 입력 데이터 (Initial Input Payload)**
  - 사용자가 캐릭터를 생성할 때 입력하는 최소/최대 정보는 무엇인가요? (예: 단일 문장, 세계관 키워드, 선택지 등)
  - → 
- **Q2. 생성 파이프라인 단계 (Step-by-Step Generation Pipeline)**
  - 캐릭터가 생성될 때 거쳐야 하는 구체적인 단계와 결재선(HITL)은 어떻게 흘러가야 하나요?
  - → 
- **Q3. 제약 조건 및 유전자 도출 논리 (Constraint-First & Gene Resolution)**
  - 캐릭터의 불변 제약선(Hard Invariants), 트라우마, 성격 유전자는 어떤 논리적 인과 사슬로 도출되어야 하나요?
  - → 

---

## 3. 외모(Visual) 생성 및 묘사 규격 (Visual DNA & Imagery)
- **Q1. 8중 해부학적 외모 규격 (8-Tier Visual DNA Specifications)**
  - 외모 묘사 부재나 표류(Drift) 문제를 원천 차단하기 위해 반드시 고정/정의되어야 하는 외모 속성들은 무엇인가요?
  - → 
- **Q2. 서사 문학과 이미지 태그 연동 (Literary Anchor & Danbooru Mapping)**
  - 생성된 외모 규격이 본문 서사 묘사와 일러스트 생성 프롬프트(Illustrious/SD Danbooru 태그)에 어떻게 1:1로 컴파일되어야 하나요?
  - → 

---

## 4. 턴 진행 및 서사 롤플레이 (Turn Loop & Somatic Mechanics)
- **Q1. 1턴 실행 시 AI 사고 및 응답 파이프라인 (Turn Execution Flow)**
  - 유저의 행동/대사 입력 시, AI가 어떤 순서와 컨텍스트(30,000자 헌법, 원장, 운동 연쇄)를 참조하여 서사를 작성해야 하나요?
  - → 
- **Q2. 3계층 신경·메모리 원장 누적 (3-Tier Somatic Ledger Evolution)**
  - 신체 반사(Layer 1), 단기 감각 버퍼(Layer 2), 장기 인격 기억(Layer 3)은 대화가 누적되면서 어떻게 변화하고 보존되어야 하나요?
  - → 
- **Q3. 세이프티 필터 통과 및 초임계 관능 압축 (Safety & Sensorial Compression)**
  - LLM 세이프티 필터를 100% 안전하게 준수하면서도 최고조의 문학적/생체역학적 텐션을 자아내는 문체와 어휘 규칙은 무엇인가요?
  - → 

---

## 5. UI/UX 및 인터랙션 요구사항 (User Interface & Control)
- **Q1. 화면 구성 및 주요 뷰 (View Architecture)**
  - 메인 로비, Play Room(서사 극장), 캐릭터 보관소(Studio Vault) 등 각 화면이 유저에게 제공해야 하는 핵심 인터랙션은 무엇인가요?
  - → 
- **Q2. 필수 유틸리티 기능 (Core Convenience Features)**
  - 되돌리기(Undo), 리셋, 시스템 헌법 원클릭 복사, 단부루 태그 복사, API 키 설정 등 반드시 필요한 유저 편의 기능은 무엇인가요?
  - → 

---

## 6. 기술 및 연동 제약 조건 (Tech Stack & Integration)
- **Q1. 멀티 LLM 연동 및 프로바이더 전략 (LLM Orchestration)**
  - Anthropic Claude(3.7 / 3.5 Sonnet)와 Google Gemini(3.6 Flash / 1.5 Pro)의 주력/보조 역할 및 장애 대응(Fallback) 방식은 무엇인가요?
  - → 
- **Q2. 데이터 영속성 및 아키텍처 제약 (Persistence & Architecture)**
  - SQLite 트랜잭션, POPO 도메인 격리, Clean 4-Tier 계층 분리 수준은 어떻게 유지되어야 하나요?
  - → 

---

## 7. 절대 금기 사항 (Anti-Patterns / DO NOTs)
- **Q1. AI 출력 및 시스템 동작 금기 (Critical Breaches)**
  - AI가 대사를 출력하거나 상태를 다룰 때 "절대 나와서는 안 되는" 최악의 패턴(예: 뜬구름 잡는 추상화, 급발진 완료 선언, 외모 왜곡 등)은 무엇인가요?
  - → 
