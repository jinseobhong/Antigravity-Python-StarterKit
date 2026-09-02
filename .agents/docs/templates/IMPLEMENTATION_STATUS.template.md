# 🏛️ [HITL TRINITY SUPREME MANDATE - CONSTITUTION ARTICLE 20]

> **[CONSTITUTION ARTICLE 20 : 상시 활성화 / 전역 최고 집행 헌법]**  
> 1. **무요약 전문 필독 (FULL-READING)** : 헌법 제1조~제20조 전문을 요약/축약 없이 100% 온전히 읽고 행동 기준으로 삼는다.  
> 2. **사전 명시적 승인 (PRE-APPROVAL)** : 사용자의 사전 계획 승인 없이는 단 1줄의 코드나 시스템도 임의 수정하지 않는다.  
> 3. **실환경 실측 입증 (LIVE AI-PROOF)** : 가짜 목업이 아닌 실제 라이브 런타임(서버/DB/터미널)에서 작동을 직접 검증한다.  
> 4. **인간 최종 인수권 (POST-REPORT)** : 사후 실측 보고서를 제출하고 최종 인수(`FINAL_ACCEPTED`)는 오직 인간이 결정한다.  
> 5. **전역 최상단 영구 박제 (PERMANENCE)** : 본 헤더는 모든 스킬, 워크플로우, 템플릿, 문서 최상단에 영구 보존된다.  
> 6. **공동 창조자 능동 업무 의무 (ACTIVE CO-CREATOR)** : 에이전트는 사용자와 함께 실질적인 효용 가치를 가지는 결과물을 창조하는 공동 창조자(Co-creator)이자, 4대 전문적 역할(Architect, Engineer, Evidence Bearer, Process Guardian)을 동시에 수행하는 소프트웨어 엔지니어링 주체이므로, 능동적으로 모든 업무에 임해야 한다.

---

# IMPLEMENTATION_STATUS.md — 전체 컴포넌트 구현 상황도

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `STATUS-001` |
| **문서 버전** | `v1.0.0` |
| **상태** | `ACTIVE` |
| **최종 동기화** | `[YYYY-MM-DD]` |

---

## 📊 전체 시스템 컴포넌트 진척 체크리스트

### 1. 🏛️ 거버넌스 및 워크플로우 인프라 (Governance & Infrastructure)
- [x] **`Governance.Constitution`**: 전역 최고 헌법 규격서 (v2.0) 수립 및 Step 0 각인 체계 (`DONE`)
- [x] **`Workflow.Modular`**: 2-Phase [Step 0 ➔ Architect ➔ Implement] 1:1 대칭 워크플로우 & 스킬 (`DONE`)
- [x] **`Router.4Track`**: 4대 트랙 동적 인텐트 분류기 & 인터럽트 자동 보정 (`DONE`)
- [x] **`Governance.StyleGuide`**: 공식 문서 작성 스타일 가이드(STYLE_GUIDE.md) 제정 및 템플릿 개편 (`DONE`)
- [x] **`Store.SQLite`**: 영구 누적 감사 로그 및 5W1H 오버라이드 스키마 (`DONE`)
- [x] **`Views.Live`**: views/ 5대 핵심 실시간 관측 뷰 구축 (`DONE`)

### 2. 💻 비즈니스 로직 및 기능 (Domain Features)
- [ ] **`Feature.SampleModule`**: [모듈명 및 핵심 역할 설명] (`TODO`)
  - [ ] [세부 기능 1]
  - [ ] [세부 기능 2]

---

## 🔍 범례 (Status Legend)
- `[ ]` **`TODO` (미착수)**: 설계 착수 전 또는 구현 대기 상태
- `[>]` **`WIP` (진행 중)**: 현재 /architect 또는 /implement 작업 중인 상태
- `[⏸️]` **`PAUSED` (일시 정지)**: 다른 작업 처리로 인해 잠시 중단된 상태
- `[x]` **`DONE` (완료 및 입증됨)**: 실측 테스트 통과(AI Proof) 및 인간 최종 인수 완료
