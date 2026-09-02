---
name: implement
description: >-
  Phase 2 Implementation & AI Proof skill for Antigravity (구현 단계). Use when the implementation plan has been approved by the user. Enforces CDD contract compliance, direct automated terminal E2E HTTP test execution (AI Proof), views/ DONE sync, and mandatory twin-call walkthrough mirroring.
---

# 🏛️ [GLOBAL CONSTITUTION v2.2 & HITL TRINITY MANDATE]

> **[AI ARCHITECT GLOBAL CONSTITUTION v2.2 : 상시 활성화 / 전역 최고 거버넌스 규격]**  
> 1. **절대 성역 방어 (SACRED ZONE)**: `GEMINI.md`, `.rules/`, `.gitignore`, `.env`에 대한 임의 수정 원천 차단 (제0절 제1조).  
> 2. **사전 명시적 인가 (PRE-AUTHORIZATION)**: 고위험 작업 시 명시적 "승인(APPROVE)" 키워드 득속 전 파일 수정 봉쇄 (제2절 제8조/제9조).  
> 3. **실환경 실측 증명 (AI PROOF)**: 실제 터미널 명령어 원문과 OS Stdout Exit Code 0 입증 없는 완료 선언 절대 금지 (제1절 제2조 / 제6절 제15조).  
> 4. **3계층 심층 영향도 고지 (IMPACT EXPLANATION)**: 데이터 흐름, 방어된 결함 시나리오, DX 체감 코드 변화 필수 해석 (제1절 제2조 4항 / IMPACT_ANALYSIS_GUIDE).  
> 5. **인간 최종 인수권 (HUMAN DECISION)**: 4단계 완료 보고서 제출 후 최종 승인은 오직 인간이 독점 결정한다 (제6절 제15조 4단계).

---

# 💻 Implementation & AI Proof Runbook (Phase 2)

> ### 🛡️ [AI ARCHITECT 헌법 제1조~제17조 & 전사 무결성 강제 체크리스트]
> - [ ] **제1조 (절대 성역 수호)**: 불변 파일 쓰기 금지.
> - [ ] **제2조 (증거 없는 완료 금지)**: `run_checks.py` 통과 터미널 로그 원문 필수 첨부.
> - [ ] **제3조/제4조 (코드 축약 및 전체 덮어쓰기 금지)**: 단위 Patch 및 온전한 블록 작성.
> - [ ] **제6조 (임의 범위 확장 금지)**: 승인된 계획서(`IMPLEMENTATION_PLAN.md`) 범위 내에서만 구현.
> - [ ] **제15조 (4단계 완료 보고)**: 전문+Diff 3단 대조 및 3계층 심층 영향도 분석 필수 보고.

---

## 🧭 구현 4대 실행 절차 (Execution Flow)

1. **[1단계: 계획서 범위 준수 구현 (Scope-Bounded Execution)]**:
   - `views/IMPLEMENTATION_PLAN.md`에서 승인된 파일만 정밀 수정 및 생성합니다.
   - `CODING_STANDARDS.md`의 정적 타입 힌트, Pure Domain 불변 모델, AAA 테스트 원칙을 100% 준수합니다.
2. **[2단계: 터미널 실측 자동 검증 (Automated AI Proof)]**:
   - `py -3 .agents/scripts/run_checks.py`를 실행하여 단위 테스트, E2E 시나리오, 거버넌스 대칭성, DB 스냅샷 100% 통과(`Exit Code 0`)를 확인합니다.
3. **[3단계: 관측 뷰 및 SQLite 감사 동기화 (Views & Store Sync)]**:
   - `views/CURRENT_STATE.md`, `views/IMPLEMENTATION_STATUS.md`를 `DONE`으로 갱신하고 `log_task.py`로 트랜잭션을 기록합니다.
4. **[4단계: 종합 완료 보고 및 인간 최종 인수 (Proof Report & Human Decision)]**:
   - `views/WALKTHROUGH.md`를 작성하고, 사용자에게 3계층 심층 영향도 분석 보고서를 제출하여 최종 인수를 받습니다.
