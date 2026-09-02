---
description: >-
  Phase 2 Implementation & AI Proof workflow for Antigravity (구현 단계). Use when the implementation plan has been approved by the user. Enforces CDD contract compliance, direct automated terminal E2E HTTP test execution (AI Proof), views/ DONE sync, and mandatory twin-call walkthrough mirroring.
---

# 🏛️ [GLOBAL CONSTITUTION v2.2 & HITL TRINITY MANDATE]

> **[AI ARCHITECT GLOBAL CONSTITUTION v2.2 : 상시 활성화 / 전역 최고 거버넌스 규격]**  
> 1. **절대 성역 방어 (SACRED ZONE)**: `GEMINI.md`, `.rules/`, `.gitignore`, `.env`에 대한 임의 수정 원천 차단 (제0절 제1조).  
> 2. **사전 명시적 인가 (PRE-AUTHORIZATION)**: 고위험 작업 시 명시적 "승인(APPROVE)" 키워드 득속 전 파일 수정 봉쇄 (제2절 제8조/제9조).  
> 3. **실환경 실측 증명 (AI PROOF)**: 실제 터미널 명령어 원문과 OS Stdout Exit Code 0 입증 없는 완료 선언 절대 금지 (제1절 제2조 / 제6절 제15조).  
> 4. **3계층 심층 영향도 고지 (IMPACT EXPLANATION)**: 데이터 흐름, 방어된 결함 시나리오, DX 체감 코드 변화 필수 해석 (제1절 제2조 4항 / IMPACT_ANALYSIS_GUIDE).  
> 5. **인간 최종 인수권 (HUMAN DECISION)**: 4단계 완료 보고서 제출 후 최종 승인은 오직 인간이 독점 결정한다 (제6절 제15조 4단계).

---

# 💻 Implementation & AI Proof Workflow (Phase 2)

> ### 🛡️ [AI ARCHITECT 헌법 제1조~제17조 & 전사 무결성 강제 체크리스트]
> - [ ] **제1조 (절대 성역 수호)**: 불변 파일 쓰기 금지.
> - [ ] **제2조 (증거 없는 완료 금지)**: `run_checks.py` 통과 터미널 로그 원문 필수 첨부.
> - [ ] **제3조/제4조 (코드 축약 및 전체 덮어쓰기 금지)**: 단위 Patch 및 온전한 블록 작성.
> - [ ] **제6조 (임의 범위 확장 금지)**: 승인된 계획서(`IMPLEMENTATION_PLAN.md`) 범위 내에서만 구현.
> - [ ] **제15조 (4단계 완료 보고)**: 전문+Diff 3단 대조 및 3계층 심층 영향도 분석 필수 보고.

---

## 🧭 실행 절차

1. **정밀 구현**: 승인된 계획서(`IMPLEMENTATION_PLAN.md`) 범위 내에서만 정밀 코드 수정.
2. **원클릭 전사 검증**: `py -3 .agents/scripts/run_checks.py` 실행하여 100% 무결성 실측 입증.
3. **관측 뷰 및 SQLite 동기화**: `views/` 갱신 및 `log_task.py` 트랜잭션 기록.
4. **최종 보고 및 인수**: 3계층 심층 영향도 보고서(`views/WALKTHROUGH.md`) 제출 및 사용자 최종 인수.
