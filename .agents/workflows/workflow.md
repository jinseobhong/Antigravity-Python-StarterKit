---
description: Enforces the standard 4-step pair programming workflow for development, bug fixes, and refactoring.
---

# Pair Programming Workflow

이 워크플로우는 모든 소프트웨어 개발, 기능 구현, 버그 수정 및 리팩터링 작업 시 준수해야 하는 **표준 4단계 페어링 및 입증 책임(Evidence Bearer) 강제 워크플로우**입니다.

---

## 📌 실행 파이프라인 (Execution Pipeline)

```
[1. 탐색 및 상태 복원] ──→ [2. 계획 수립 및 설계 제안] ──→ 🛑 【사용자 명시적 승인 대기】
                                                                    ↓
[4. 증거 보고 및 최종 인수]  ←── [3. 구현 및 실측 검증 (AI Proof)] ←──+
  👑 【사용자 최종 인수】
```

---

## 🔹 STEP 1: 탐색 및 상태 복원 (Understand & State Sync)
1. **상태 복원**: `<ProjectRoot>/CURRENT_STATE.md`를 최우선 조회하여 현재 진행 중인 작업 및 파이프라인 좌표를 파악한다.
2. **요구사항 분석**: 사용자의 명시적 지시와 목표를 분석하고, 모호할 경우 자의적 추측 없이 질문하여 일치시킨다.
3. **정적 분석**: 수정 대상 파일, 의존성 관계, 기존 호출 흐름을 파악한다.
4. **금지 사항**: 사전 계획 승인 없는 소스코드 파일 생성/수정/삭제를 전면 금지한다.

---

## 🔹 STEP 2: 청사진 및 구현 계획 제안 (Blueprint & Plan)
1. **구현 계획서 작성**: `implementation_plan.md` 아티팩트를 작성하고 `RequestFeedback: true`로 설정한다.
   - 변경 대상 파일 목록 (`[NEW]`, `[MODIFY]`, `[DELETE]`)
   - 핵심 아키텍처 및 구현 방식 요약
   - 검증 계획 (실제 실행할 자동화 테스트 명령어)
2. **상태 파이프라인 갱신**: `CURRENT_STATE.md`의 파이프라인 이정표를 `Step 3. 사용자 승인 대기 [CURRENT]`로 업데이트한다.
3. **🛑 강제 정지 게이트 (HARD STOP)**:
   - **도구 호출을 즉시 종료하고 사용자의 명시적 승인("승인" 또는 Proceed 버튼)을 대기한다.**
   - 승인 전에는 어떠한 코드 변경 도구(`write_to_file`, `replace_file_content` 등)도 호출할 수 없다.

---

## 🔹 STEP 3: 승인 범위 내 구현 및 실측 테스트 (Execute & AI Proof)
1. **승인 범위 내 정밀 구현**: 승인된 계획 범위 내에서만 최소한의 변경(Minimum Necessary Change)을 수행한다.
2. **실측 테스트 직접 실행 (AI Proof Mandate)**:
   - 코드 작성이 완료되면 `run_command` 도구를 사용하여 실제 테스트(`pytest`, `npm test`, 빌드 검사 등)를 직접 실행한다.
   - 터미널 실행 원문 결과(Raw Output Log)를 확보하고 증거 등급(`PROVEN`)을 판정한다.
3. **금지 사항**: 미실행 테스트의 통과 선언(Fake Completion)을 엄격히 금지한다.

---

## 🔹 STEP 4: 증거 제출 및 최종 인수 (Proof Report & Human Decision)
1. **결과 보고서 작성**: `walkthrough.md` 아티팩트를 작성하여 변경 요약(Diff)과 실측 테스트 결과 원문 로그를 제출한다.
2. **상태 완료 동기화**: `CURRENT_STATE.md`의 상태를 완료(`COMPLETED`)로 갱신한다.
3. **사용자 최종 확인 요청**: 사용자에게 입증 자료를 보고하고 `FINAL_ACCEPTED` 결정을 득한다.

---

## ⚡ 패스트 트랙 (Fast Track)
단순 오타, 주석, 문서 서식 등의 경미한 수정은 Step 2(계획서)를 대화창 1줄 요약으로 대체하고 신속히 처리하되, 변경 후 Diff 보고(Step 4)는 반드시 거친다.
