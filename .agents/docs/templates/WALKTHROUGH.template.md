# 🏛️ [HITL TRINITY SUPREME MANDATE - CONSTITUTION ARTICLE 20]

> **[CONSTITUTION ARTICLE 20 : 상시 활성화 / 전역 최고 집행 헌법]**  
> 1. **무요약 전문 필독 (FULL-READING)** : 헌법 제1조~제20조 전문을 요약/축약 없이 100% 온전히 읽고 행동 기준으로 삼는다.  
> 2. **사전 명시적 승인 (PRE-APPROVAL)** : 사용자의 사전 계획 승인 없이는 단 1줄의 코드나 시스템도 임의 수정하지 않는다.  
> 3. **실환경 실측 입증 (LIVE AI-PROOF)** : 가짜 목업이 아닌 실제 라이브 런타임(서버/DB/터미널)에서 작동을 직접 검증한다.  
> 4. **인간 최종 인수권 (POST-REPORT)** : 사후 실측 보고서를 제출하고 최종 인수(`FINAL_ACCEPTED`)는 오직 인간이 결정한다.  
> 5. **전역 최상단 영구 박제 (PERMANENCE)** : 본 헤더는 모든 스킬, 워크플로우, 템플릿, 문서 최상단에 영구 보존된다.  
> 6. **공동 창조자 능동 업무 의무 (ACTIVE CO-CREATOR)** : 에이전트는 사용자와 함께 실질적인 효용 가치를 가지는 결과물을 창조하는 공동 창조자(Co-creator)이자, 4대 전문적 역할(Architect, Engineer, Evidence Bearer, Process Guardian)을 동시에 수행하는 소프트웨어 엔지니어링 주체이므로, 능동적으로 모든 업무에 임해야 한다.

---

# WALKTHROUGH.md — 구현 완료 및 검증 결과 보고서 (Walkthrough)

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `WALK-[MODULE]-[NUM]` |
| **문서 버전** | `v1.0.0` |
| **완료 일자** | `[YYYY-MM-DD]` |
| **입증 등급** | `PROVEN (재현 가능 테스트 증거 확보)` |
| **최종 결정** | `FINAL_ACCEPTED (인간 최종 인수 완료)` |
| **작성자 / 승인자** | `AI Architect` / `Human Lead` |

---

## 📁 1. 변경된 파일 목록 및 Diff 요약 (Changes Summary)

| 파일 경로 | 변경 구분 | 주요 수정 내용 |
| :--- | :---: | :--- |
| `src/auth/password_reset.py` | `[NEW]` | 토큰 생성 및 15분 만료 검증 로직 구현 |
| `src/auth/service.py` | `[MODIFY]` | `reset_password` 엔드포인트 핸들러 연동 |
| `tests/test_password_reset.py` | `[NEW]` | 정상 발급 및 만료 토큰 단위 테스트 5종 추가 |

---

## 🧪 2. 실측 테스트 실행 결과 원문 (Executed AI Proof Logs)

```text
$ pytest tests/test_password_reset.py -v
============================= test session starts =============================
collected 5 items

tests/test_password_reset.py::test_generate_reset_token PASSED          [ 20%]
tests/test_password_reset.py::test_verify_valid_token PASSED            [ 40%]
tests/test_password_reset.py::test_verify_expired_token PASSED          [ 60%]
tests/test_password_reset.py::test_verify_invalid_signature PASSED      [ 80%]
tests/test_password_reset.py::test_password_update_success PASSED       [100%]

============================== 5 passed in 0.42s ==============================
```

- **린트 / 타입 검사 결과**: `0 errors, 0 warnings`
- **입증 등급 (Proof Grade)**: `PROVEN` (재현 가능 명령어 검증 완료)

---

## 💡 3. 시스템 영향도 3계층 심층 분석 (3-Tier Deep-Dive Impact Analysis)

### 3.1 💾 실제 데이터 흐름 추적 (Data Flow Pipeline Trace)
- [Mermaid 시퀀스/플로우 다이어그램 및 RAM ➔ Disk 데이터 전이 경로 기술]

### 3.2 🛡️ 방어된 구체적 결함 시나리오 (Prevented Failure Scenarios)
- **시나리오 A (데이터 무결성/롤백)**: [비정상 종료나 엣지 케이스 시 결함 방어 원리]
- **시나리오 B (동시성/타입 안정성)**: [경쟁 상태 및 1:N 관계 불일치 방어]

### 3.3 🧑‍💻 1인 개발자 체감 변화 및 차기 코드 예시 (DX & Next-Step Code)
```python
# [차기 개발 단계에서 실제로 호출할 3~5줄 내외의 간결한 코드 예시]
```
- [저수준 처리의 캡슐화 및 내일 작성할 코드의 단순화 효과 설명]

---

## 🔍 4. 미검증 영역 및 잔여 위험 (Known Gaps & Residual Risks)
- `[없음 | 실제 외부 통신은 Mocking 처리하여 검증함]`

---

## 👑 5. 사용자 최종 인수 (Human Acceptance Decision)
- [ ] `FINAL_ACCEPTED` (작업 완결 및 승인)
- [ ] `REWORK_REQUIRED` (보완 재작업 지시)

