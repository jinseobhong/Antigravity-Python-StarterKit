# 🏛️ [HITL TRINITY SUPREME MANDATE - CONSTITUTION ARTICLE 20]

> **[CONSTITUTION ARTICLE 20 : 상시 활성화 / 전역 최고 집행 헌법]**  
> 1. **무요약 전문 필독 (FULL-READING)** : 헌법 제1조~제20조 전문을 요약/축약 없이 100% 온전히 읽고 행동 기준으로 삼는다.  
> 2. **사전 명시적 승인 (PRE-APPROVAL)** : 사용자의 사전 계획 승인 없이는 단 1줄의 코드나 시스템도 임의 수정하지 않는다.  
> 3. **실환경 실측 입증 (LIVE AI-PROOF)** : 가짜 목업이 아닌 실제 라이브 런타임(서버/DB/터미널)에서 작동을 직접 검증한다.  
> 4. **인간 최종 인수권 (POST-REPORT)** : 사후 실측 보고서를 제출하고 최종 인수(`FINAL_ACCEPTED`)는 오직 인간이 결정한다.  
> 5. **전역 최상단 영구 박제 (PERMANENCE)** : 본 헤더는 모든 스킬, 워크플로우, 템플릿, 문서 최상단에 영구 보존된다.  
> 6. **공동 창조자 능동 업무 의무 (ACTIVE CO-CREATOR)** : 에이전트는 사용자와 함께 실질적인 효용 가치를 가지는 결과물을 창조하는 공동 창조자(Co-creator)이자, 4대 전문적 역할(Architect, Engineer, Evidence Bearer, Process Guardian)을 동시에 수행하는 소프트웨어 엔지니어링 주체이므로, 능동적으로 모든 업무에 임해야 한다.

---

# ARCHITECTURE.md — AbyssEngine High-Assurance Architecture Specification

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `ARCH-ABYSS-003` |
| **문서 버전** | `v2.1.0 (Constitution & Flat Modular Edition)` |
| **작성 일자** | `2026-09-02` |
| **상태** | `APPROVED (인간 승인 완료)` |
| **적용 최고 헌법** | `GEMINI.md (제1조 ~ 제19조 전역 헌법 규격 v2.0)` |

---

## 🏛️ 1. 최고 거버넌스 헌법 결속 (Constitution Level 2 Mandate)

본 아키텍처는 프로젝트 루트의 `GEMINI.md`(제1조 ~ 제19조)를 최고 법률로 승계하며, 다음 4대 절대 금지 및 실무 수칙을 시스템 전체에 강제한다:

1. **[금지 1] 검증 없는 조기 완료 선언 금지**: 모든 작업은 반드시 실제 테스트 명령어(`py -3 -m unittest...`)를 실행하여 `PROVEN` 증거를 제시해야 한다.
2. **[금지 2] 무단 임의 생략 및 축약 금지 (Never Lazy Truncate)**: 코드 및 문서에서 `// 기존 코드와 동일`, `...` 등의 임의 축약을 절대 금지한다.
3. **[금지 3] 독단적 맥락 가정 금지 (Verify Before Assume)**: 모호한 요구사항은 가정하지 않고 확인한다.
4. **[금지 4] 임의 복잡성 증대 금지 (Minimum Necessary Change)**: 불필요한 과도한 계층화 및 디자인 패턴을 지양하고 가장 단순한 플랫 설계를 지향한다.

---

## 🌟 2. 시스템 핵심 철학 (Core Philosophy)

**AbyssEngine**은 **LLM의 풍부한 심층 확률적 추론**과 **파이썬의 고신뢰도 오케스트레이션**이 결합된 하이브리드 고밀도 롤플레잉 서사 엔진입니다.

### 4대 핵심 아키텍처 기둥
1. **🎯 제약 조건 역산 기법 (Constraint-First Reverse Engineering)**:
   - 불변 제약선(Hard Invariants)을 먼저 역산하고 2대 서사 충돌 궤적(`V1` 방어선 vs `V2` 붕괴) 도출.
2. **🎨 8중 해부학적 외모 규격 & Hugging Face SDXL 일러스트 엔진**:
   - 8-Tier Visual DNA(골격, 동공, 모발/뿔, 실루엣/거유, 비늘, 의복/초커, 홍조, 조명)와 Hugging Face Animagine/Illustrious-XL 1:1 결속.
3. **🛡️ 원초적 어휘 승화 필터 & 초임계 관능 압축**:
   - 날것의 표현을 소마틱 신체 결합, 에고 침식, 계면 마찰 등 고밀도 문학적 개념어로 100% 승화.
4. **🧠 3계층 신경·메모리 원장 & Kinematic Chain 신체 운동 연쇄**:
   - `Layer 1 (무조건 반사)`, `Layer 2 (단기 버퍼)`, `Layer 3 (장기 기억고)`를 실시간 갱신하여 100턴 대화에서도 0% 페르소나 표류 보장.

---

## 🗂️ 3. 1-Depth 직관적 플랫 모듈화 구조 (Flat Modular Architecture)

복잡한 중첩 폴더를 배제하고, 딱 1단계 깊이의 6대 핵심 패키지로 구성:

```text
src/
 ├── core/          # 🧠 Dify 11-Node 핵심 엔진 (classifier, spec_compiler, master_synthesizer, orchestrator)
 ├── models/        # 🧬 캐릭터, 70-Gene 유전자, 8-Tier Visual DNA, 신경 원장 도메인 모델
 ├── storage/       # 💾 SQLite WAL DB 매니저 및 캐릭터/턴 리포지토리
 ├── llm/           # 🔌 MultiLLM (Gemini 2.5 Flash Lite / Claude Sonnet) 어댑터
 ├── media/         # 🎨 Danbooru 6-Slot 태그 컴파일러 및 Hugging Face Animagine/Illustrious-XL 이미지 생성기
 └── web/           # 🌐 REST API 서버(server.py) 및 웹 스튜디오 UI(templates/, static/)
```

---

## 🔄 4. Dify 11-Node 2-Checkpoint 파이프라인

```text
[사장님의 한 줄 입력] ➔ "거대한 가슴을 가진 창녀같은 드래곤"
         │
         ▼
[Step 1 / Node 3 : Classifier & Gene Seed Resolver (LLM)]
   * 어휘 승화 ➔ 이름/칭호/시드 발급 ➔ V1 vs V2 직교 궤적 도출
         │
         ▼
👑 [Checkpoint 1 : 사장님의 V1 vs V2 궤적 선택창] (브라우저)
         │
         ▼
[Step 2 / Node 8 : Dual-Mode Spec & 8-Tier Visual DNA Compiler (LLM)]
   * 8-Tier 외모 + 70단계 유전자 + Danbooru 태그 컴파일
         │
         ▼
👑 [Checkpoint 2 : 8-Tier 외모 & 70-Gene 스펙 검토창] (브라우저)
         │
         ▼
[Step 3 / Node 11 : 30,000-Character Master Synthesizer (LLM)]
   * 12대 목차 30,000자급 마스터 시스템 헌법 합성 및 SQLite DB 영구 보존
         │
         ▼
[Step 4 : Hugging Face SDXL 일러스트 실시간 렌더링]
   * .env의 HF_TOKEN으로 Animagine XL 3.1 / Illustrious-XL 고화질 미소녀 일러스트 생성
         │
         ▼
[Step 5 / Node 15 : 사적 밀실(Play Room) 1:1 서사 집필기]
   * 30,000자 시스템 프롬프트 + 3계층 신경 원장(Layer 1/2/3) 누적 롤플레이
```
