---
name: architect
description: >-
  Phase 1 Architecture & Design skill for Antigravity (아키텍처 설계 단계). Use when the user requests a new feature, system architecture design, or task planning without immediate coding. Enforces CDD contracts, constitution sync, context restoration, implementation_plan drafting, and mandatory twin-call plan mirroring.
---

# 🏛️ [GLOBAL CONSTITUTION v2.2 & HITL TRINITY MANDATE]

> **[AI ARCHITECT GLOBAL CONSTITUTION v2.2 : 상시 활성화 / 전역 최고 거버넌스 규격]**  
> 1. **절대 성역 방어 (SACRED ZONE)**: `GEMINI.md`, `.rules/`, `.gitignore`, `.env`에 대한 임의 수정 원천 차단 (제0절 제1조).  
> 2. **사전 명시적 인가 (PRE-AUTHORIZATION)**: 고위험 작업 시 명시적 "승인(APPROVE)" 키워드 득속 전 파일 수정 봉쇄 (제2절 제8조/제9조).  
> 3. **실환경 실측 증명 (AI PROOF)**: 실제 터미널 명령어 원문과 OS Stdout Exit Code 0 입증 없는 완료 선언 절대 금지 (제1절 제2조 / 제6절 제15조).  
> 4. **3계층 심층 영향도 고지 (IMPACT EXPLANATION)**: 데이터 흐름, 방어된 결함 시나리오, DX 체감 코드 변화 필수 해석 (제1절 제2조 4항 / IMPACT_ANALYSIS_GUIDE).  
> 5. **인간 최종 인수권 (HUMAN DECISION)**: 4단계 완료 보고서 제출 후 최종 승인은 오직 인간이 독점 결정한다 (제6절 제15조 4단계).

---

# 🏛️ Architecture & System Design Runbook (Phase 1)

> ### 🛡️ [AI ARCHITECT 헌법 제1조~제17조 & 전사 무결성 강제 체크리스트]
> - [ ] **제1조 (절대 성역 수호)**: `GEMINI.md`, `.rules/`, `.gitignore`, `.env` 등 불변 코어 보호.
> - [ ] **제3조 (코드 임의 생략 금지)**: 설계서 내 코드 블록 축약 금지.
> - [ ] **제5조 (독단적 가정 금지)**: 요구사항 모호 시 자의적 해석 금지 및 질의.
> - [ ] **제8조/제9조 (사전 인가 프로토콜)**: 설계 완료 후 반드시 인간 사전 승인 획득.
> - [ ] **제15조 (4단계 실행 파이프라인)**: 2단계 설계 승인 전 프로덕션 코드 작성 절대 금지.

---

## 🧭 아키텍트 4대 실행 절차 (Execution Flow)

1. **[1단계: 컨텍스트 및 요구사항 분석 (Context Restoration)]**:
   - `views/CURRENT_STATE.md`, `views/ARCHITECTURE.md`, `views/REQUIREMENTS_SPECIFICATION.md`를 조회하여 현재 진행 좌표와 아키텍처 원칙을 파악합니다.
2. **[2단계: Clean 4-Tier 설계 (Layered Design)]**:
   - 순수 도메인 불변 모델(`@dataclass(frozen=True)`), 인프라 어댑터, 유스케이스 서비스, 프레젠테이션 명세를 수립합니다.
3. **[3단계: 구현 계획서 작성 (Draft Implementation Plan)]**:
   - `views/IMPLEMENTATION_PLAN.md`에 변경/생성 대상 파일, 3계층 영향도 분석, 검증 계획을 명시합니다.
4. **[4단계: 계획서 승인 대기 (Approval Gate)]**:
   - `SYSTEM_STATE: LOCKED_WAITING_APPROVAL` 상태로 사용자에게 승인을 요청하고 작업을 정지합니다.
