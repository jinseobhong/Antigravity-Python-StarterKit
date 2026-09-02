---
name: scaffold
description: >-
  Automated file, module, and directory scaffolding skill for Antigravity. Enforces 100% compliance with CDD contracts, CONVENTIONS.md, and STYLE_GUIDE.md.
---

# 🏛️ [GLOBAL CONSTITUTION v2.2 & HITL TRINITY MANDATE]

> **[AI ARCHITECT GLOBAL CONSTITUTION v2.2 : 상시 활성화 / 전역 최고 거버넌스 규격]**  
> 1. **절대 성역 방어 (SACRED ZONE)**: `GEMINI.md`, `.rules/`, `.gitignore`, `.env`에 대한 임의 수정 원천 차단 (제0절 제1조).  
> 2. **사전 명시적 인가 (PRE-AUTHORIZATION)**: 고위험 작업 시 명시적 "승인(APPROVE)" 키워드 득속 전 파일 수정 봉쇄 (제2절 제8조/제9조).  
> 3. **실환경 실측 증명 (AI PROOF)**: 실제 터미널 명령어 원문과 OS Stdout Exit Code 0 입증 없는 완료 선언 절대 금지 (제1절 제2조 / 제6절 제15조).  
> 4. **3계층 심층 영향도 고지 (IMPACT EXPLANATION)**: 데이터 흐름, 방어된 결함 시나리오, DX 체감 코드 변화 필수 해석 (제1절 제2조 4항 / IMPACT_ANALYSIS_GUIDE).  
> 5. **인간 최종 인수권 (HUMAN DECISION)**: 4단계 완료 보고서 제출 후 최종 승인은 오직 인간이 독점 결정한다 (제6절 제15조 4단계).

---

# 🏗️ Scaffolding & Blueprint Runbook

> ### 🛡️ [AI ARCHITECT 헌법 제1조~제17조 & 전사 무결성 강제 체크리스트]
> - [ ] **제1조 (절대 성역 수호)**: 불변 파일 쓰기 금지.
> - [ ] **제6조 (무단 파일 생성 금지)**: 계획서에 없는 불필요한 임시 파일 생성 금지.
> - [ ] **제8조 (신규 영구 파일 생성 통제)**: 디렉터리 및 아키텍처 파일 생성 시 사전 승인 획득.
> - [ ] **규격 준수**: `FILESYSTEM_SPEC.md` 및 `CODING_STANDARDS.md` 표준 100% 준수.

---

## 🧭 스캐폴딩 4대 실행 절차 (Execution Flow)

1. **[1단계: 패키지 토폴로지 검토 (Topology Check)]**:
   - `FILESYSTEM_SPEC.md`의 Clean Architecture 4계층(`src/`) 및 테스트 디렉터리 구조를 확인합니다.
2. **[2단계: 표준 템플릿 인스턴스화 (Template Instantiation)]**:
   - `.agents/docs/templates/`의 표준 양식을 기반으로 메타데이터 헤더가 포함된 문서를 생성합니다.
3. **[3단계: 패키지 초기화 및 심볼 등록 (Package Init)]**:
   - 디렉터리 생성 시 `__init__.py` 및 정적 타입 익스포트를 등록합니다.
4. **[4단계: 대칭성 및 무결성 검증 (Sync Audit)]**:
   - `py -3 .agents/scripts/run_checks.py`를 실행하여 뷰와 스키마 대칭성을 즉시 입증합니다.
