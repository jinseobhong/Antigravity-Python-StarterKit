---
name: workflow
description: >-
  Enforces the standard 4-step pair programming workflow for software development,
  feature implementation, bug fixes, refactoring, and architectural tasks:
  [Phase 1: Understand & State Sync -> Phase 2: Blueprint & Plan (Approval Gate) ->
   Phase 3: Execute & AI Proof (Raw Test Logs) -> Phase 4: Proof Report & Human Decision].
  Prevents premature coding without explicit human approval and mandates objective verification.
---

# Pair Programming Execution Runbook (Workflow)

이 스킬은 Antigravity 에이전트가 개발 및 구현 태스크를 수행할 때 준수해야 하는 **표준 4단계 페어링 및 입증 책임(Evidence Bearer) 강제 런북**이다.

---

## 📌 실전 4단계 파이프라인 (Execution Pipeline)

```
[1. 탐색 및 상태 복원] ──→ [2. 계획 수립 및 설계 제안] ──→ 🛑 【사용자 명시적 승인 대기】
                                                                    ↓
[4. 증거 보고 및 최종 인수]  ←── [3. 구현 및 실측 검증 (AI Proof)] ←──+
  👑 【사용자 최종 인수】
```

---

## 🔹 PHASE 1: 탐색 및 상태 복원 (Understand & State Sync)

### 필수 수행 행동 (Mandatory Actions)
1. **상태 복원 (State Anchor)**:
   - `<ProjectRoot>/CURRENT_STATE.md`를 최우선 조회하여 현재 진행 중인 작업, 파이프라인 좌표, 직전 변경 사항을 파악한다.
2. **요구사항 분석 (Requirements & Intent)**:
   - 사용자의 명시적 지시와 목표를 분석한다.
   - 요구사항이 모호하거나 다의적인 경우, 자의적으로 추측하지 않고 즉시 사용자에게 질문하여 일치시킨다.
3. **정적 분석 (Read Before Modify)**:
   - 수정 대상 파일, 의존성 관계, 기존 호출 흐름을 파악한다.

### 🚫 절대 금지 사항 (Forbidden)
- 사용자의 계획 승인 없이 소스코드 파일을 생성, 수정, 삭제하는 일체의 행위.

---

## 🔹 PHASE 2: 청사진 및 구현 계획 제안 (Blueprint & Plan)

### 필수 수행 행동 (Mandatory Actions)
1. **구현 계획서 작성 (`implementation_plan.md`)**:
   - `RequestFeedback: true`로 설정하여 아티팩트를 생성/업데이트한다.
   - 다음 항목을 누락 없이 포함한다:
     - 작업 배경 및 목표
     - 변경 대상 파일 목록 (`[NEW]`, `[MODIFY]`, `[DELETE]`)
     - 핵심 아키텍처 및 구현 방식 요약
     - 검증 계획 (실제 실행할 자동화 테스트 명령어)
2. **상태 파이프라인 갱신**:
   - `CURRENT_STATE.md`의 파이프라인 이정표를 `Step 3. 사용자 승인 대기 [CURRENT]`로 업데이트한다.

### 🛑 강제 정지 게이트 (HARD STOP)
- **에이전트는 계획서 제출 직후 도구 호출을 즉시 종료(Stop Turn)하고 사용자의 명시적 승인을 대기하여야 한다.**
- 사용자의 프롬프트/메시지 입력에 의한 "승인" 또는 UI의 `Proceed` 버튼이 제공되기 전까지는 어떠한 코드 변경도 실행할 수 없다.
- 중립적 출력("응", "좋아", "가자" 등)은 승인으로 간주하지 않는다.

---

## 🔹 PHASE 3: 승인 범위 내 구현 및 실측 테스트 (Execute & AI Proof)

### 필수 수행 행동 (Mandatory Actions)
1. **승인 범위 내 정밀 구현 (Minimum Necessary Change)**:
   - 승인된 `implementation_plan.md`의 범위 내에서만 코드를 작성/수정한다.
   - 임의의 리팩터링, 무단 라이브러리 추가, 범위 외 파일 수정을 금한다.
2. **실측 테스트 직접 실행 (AI Proof Mandate)**:
   - 코드 작성이 완료되면 `run_command` 도구를 사용하여 실제 테스트(`pytest`, `npm test`, 빌드, 린트 등)를 직접 실행한다.
   - 터미널 실행 원문 결과(Raw Output Log)를 확보한다.
3. **증거 등급 판정**:
   - `PROVEN`: 테스트 통과 및 원문 로그 확보 완료 (인간 심사 가능)
   - `PARTIALLY_PROVEN`: 일부 항목만 검증됨 (조건부 검토)
   - `UNPROVEN`: 미실행 또는 실패 (**승인 심사 진입 금지**)

---

## 🔹 PHASE 4: 증거 제출 및 최종 인수 (Proof Report & Human Decision)

### 필수 수행 행동 (Mandatory Actions)
1. **결과 보고서 작성 (`walkthrough.md`)**:
   - 변경된 파일 목록 요약 (Diff)
   - 실제 실행한 테스트 명령어 및 원문 로그 결과 제시
   - 미검증 영역 및 잔여 위험(Known Gaps) 명시
2. **상태 완료 동기화**:
   - `CURRENT_STATE.md`의 상태를 갱신한다.
3. **사용자 최종 확인 요청**:
   - 사용자에게 입증 자료를 보고하고 최종 인수(`FINAL_ACCEPTED`) 결정을 요청한다.

---

## ⚡ 패스트 트랙 규칙 (Fast Track Rule)

다음 경미한 작업은 Phase 2(계획서)를 대화창 내 1줄 요약으로 대체하고 신속히 처리할 수 있다:
- 단순 오타 및 주석 수정
- 문서 서식 및 줄바꿈 정렬
- 위험 영향도가 전혀 없는 1~2줄의 경미한 수정
- **단, 변경 후 Diff 및 결과 보고(Phase 4)는 반드시 거친다.**
