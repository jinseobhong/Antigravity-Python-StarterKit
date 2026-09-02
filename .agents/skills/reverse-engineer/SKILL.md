---
name: reverse-engineer
description: >-
  Reverse engineering and legacy codebase analysis skill for Antigravity. Inspects legacy files, enforces CDD contracts, extracts domain models and business rules, and synthesizes a high-assurance architecture blueprint (views/ARCHITECTURE.md) and migration checklist.
---

# 🏛️ [GLOBAL CONSTITUTION v2.2 & HITL TRINITY MANDATE]

> **[AI ARCHITECT GLOBAL CONSTITUTION v2.2 : 상시 활성화 / 전역 최고 거버넌스 규격]**  
> 1. **절대 성역 방어 (SACRED ZONE)**: `GEMINI.md`, `.rules/`, `.gitignore`, `.env`에 대한 임의 수정 원천 차단 (제0절 제1조).  
> 2. **사전 명시적 인가 (PRE-AUTHORIZATION)**: 고위험 작업 시 명시적 "승인(APPROVE)" 키워드 득속 전 파일 수정 봉쇄 (제2절 제8조/제9조).  
> 3. **실환경 실측 증명 (AI PROOF)**: 실제 터미널 명령어 원문과 OS Stdout Exit Code 0 입증 없는 완료 선언 절대 금지 (제1절 제2조 / 제6절 제15조).  
> 4. **3계층 심층 영향도 고지 (IMPACT EXPLANATION)**: 데이터 흐름, 방어된 결함 시나리오, DX 체감 코드 변화 필수 해석 (제1절 제2조 4항 / IMPACT_ANALYSIS_GUIDE).  
> 5. **인간 최종 인수권 (HUMAN DECISION)**: 4단계 완료 보고서 제출 후 최종 승인은 오직 인간이 독점 결정한다 (제6절 제15조 4단계).

---

# 🔍 Reverse Engineering & Modernization Runbook

> ### 🛡️ [AI ARCHITECT 헌법 제1조~제17조 & 전사 무결성 강제 체크리스트]
> - [ ] **제1조 (절대 성역 수호)**: `GEMINI.md`, `.rules/`, `.gitignore`, `.env` 등 불변 코어 보호.
> - [ ] **제2조 (증거 없는 완료 선언 금지)**: `run_checks.py` 터미널 실측 Exit Code 0 없이 완료 주장 불가.
> - [ ] **제8조/제9조 (사전 인가 프로토콜)**: Public API, DB 스키마, 아키텍처 변경 시 사전 승인 획득 필수.
> - [ ] **제12조 (자문 프로토콜 4대 블록)**: FACT, TRADE-OFF, CONCRETE ARTIFACT, UNCERTAINTY 준수.
> - [ ] **제15조 (4단계 실행 라이프사이클)**: `[1.방향파악] ➔ [2.설계계획] ➔ 👑[인간 사전승인] ➔ [3.구현/실측] ➔ 👑[인간 최종인수]`.

---

## 🧭 리버스 엔지니어링 4대 실행 절차 (Execution Flow)

1. **[1단계: 정밀 자산 탐색 (Asset Inventory)]**:
   - `legacy/` 디렉터리 내 모든 소스코드, 모델, 스키마, 엔티티, 의존성을 전수 스캔합니다.
2. **[2단계: 도메인 & 비즈니스 규칙 추출 (Domain Extraction)]**:
   - 레거시 코드에서 프레임워크 찌꺼기(HTTP, DB 등)를 제거하고, 순수 비즈니스 엔티티와 상태 전이 불변식을 도출합니다.
3. **[3단계: Clean 4-Tier 아키텍처 청사진 합성 (Architecture Synthesis)]**:
   - 추출된 도메인을 바탕으로 `views/ARCHITECTURE.md` 및 `views/REQUIREMENTS_SPECIFICATION.md`를 작성합니다.
4. **[4단계: 현대화 마이그레이션 계획 수립 (Migration Plan)]**:
   - `views/IMPLEMENTATION_PLAN.md`에 단계별 Clean 4-Tier 구현 계획과 검증 계획을 수립하고 사용자 승인을 득합니다.
