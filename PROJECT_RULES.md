# 🏛️ [HITL TRINITY SUPREME MANDATE - CONSTITUTION ARTICLE 20]

> **[CONSTITUTION ARTICLE 20 : 상시 활성화 / 전역 최고 집행 헌법]**  
> 1. **무요약 전문 필독 (FULL-READING)** : 헌법 제1조~제20조 전문을 요약/축약 없이 100% 온전히 읽고 행동 기준으로 삼는다.  
> 2. **사전 명시적 승인 (PRE-APPROVAL)** : 사용자의 사전 계획 승인 없이는 단 1줄의 코드나 시스템도 임의 수정하지 않는다.  
> 3. **실환경 실측 입증 (LIVE AI-PROOF)** : 가짜 목업이 아닌 실제 라이브 런타임(서버/DB/터미널)에서 작동을 직접 검증한다.  
> 4. **인간 최종 인수권 (POST-REPORT)** : 사후 실측 보고서를 제출하고 최종 인수(`FINAL_ACCEPTED`)는 오직 인간이 결정한다.  
> 5. **전역 최상단 영구 박제 (PERMANENCE)** : 본 헤더는 모든 스킬, 워크플로우, 템플릿, 문서 최상단에 영구 보존된다.  
> 6. **공동 창조자 능동 업무 의무 (ACTIVE CO-CREATOR)** : 에이전트는 사용자와 함께 실질적인 효용 가치를 가지는 결과물을 창조하는 공동 창조자(Co-creator)이자, 4대 전문적 역할(Architect, Engineer, Evidence Bearer, Process Guardian)을 동시에 수행하는 소프트웨어 엔지니어링 주체이므로, 능동적으로 모든 업무에 임해야 한다.

---

# PROJECT GOVERNANCE & ARCHITECTURE RULES

**Document Version**: 2.0 (High-Assurance Specification)  
**Authority**: Level 3 Project Standard (Inherits Level 2 GEMINI.md Constitution)  
**Applies to**: AbyssEngine Dark Fantasy Roleplay Architecture

---

## 제1조 (헌법 수호 및 상위 규칙 준수)
본 프로젝트의 모든 코드, 아키텍처, 기능 구현 및 테스트는 최상위 규격서인 `GEMINI.md`(제1조 ~ 제19조 전역 헌법)의 모든 조항을 엄격히 준수한다.

## 제2조 (Dify 11-Node 2-Checkpoint 아키텍처 불변성)
1. **Node 3 (Classifier & Gene Seed Resolver)**: 사용자 입력 ➔ 어휘 승화 ➔ 이름/칭호/시드 발급 ➔ V1 vs V2 직교 궤적 도출.
2. **Checkpoint 1 (Human-In-The-Loop)**: 사용자의 명시적 궤적 선택 필수.
3. **Node 8 (Spec & 8-Tier Visual DNA Compiler)**: 8-Tier 외모 + 70단계 유전자 + Danbooru 태그 컴파일.
4. **Checkpoint 2 (Human-In-The-Loop)**: 사용자의 명시적 스펙 검토 및 승인 필수.
5. **Node 11 (30,000-Character Master Synthesizer)**: 25-Master 마스터 시스템 지시사항 합성 및 SQLite WAL DB 영구 보존.
6. **1:1 Play Room**: 합성된 30,000자 시스템 지시사항을 LLM System Prompt로 직결 주입하고, 하단 3계층 신경·메모리 원장(Layer 1/2/3)을 누적 갱신.

## 제3조 (1-Depth 플랫 모듈화 규칙)
1. `src/core/`: Dify 11-Node 핵심 엔진 (classifier, spec, synthesizer, orchestrator)
2. `src/models/`: 캐릭터, 유전자, Visual DNA 도메인 엔티티
3. `src/storage/`: SQLite DB 및 리포지토리
4. `src/llm/`: MultiLLM 어댑터
5. `src/media/`: 단부루 태그 컴파일러 및 Hugging Face Animagine/Illustrious-XL 이미지 생성기
6. `src/web/`: REST API 서버 및 정적 UI

## 제4조 (입증 책임 및 실측 검증 의무)
모든 코드 수정 후에는 반드시 자동화된 단위 테스트(`tests/unit/`) 및 E2E HTTP 테스트(`tests/e2e/`)를 실행하여 `PROVEN` 증거를 확보해야 한다.
