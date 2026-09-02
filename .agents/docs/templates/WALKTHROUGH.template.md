# 🏛️ [GLOBAL CONSTITUTION v2.2 & HITL TRINITY MANDATE]

> **[AI ARCHITECT GLOBAL CONSTITUTION v2.2 : 상시 활성화 / 전역 최고 거버넌스 규격]**  
> 1. **절대 성역 방어 (SACRED ZONE)**: `GEMINI.md`, `.rules/`, `.gitignore`, `.env`에 대한 임의 수정 원천 차단 (제0절 제1조).  
> 2. **사전 명시적 인가 (PRE-AUTHORIZATION)**: 고위험 작업 시 명시적 "승인(APPROVE)" 키워드 득속 전 파일 수정 봉쇄 (제2절 제8조/제9조).  
> 3. **실환경 실측 증명 (AI PROOF)**: 실제 터미널 명령어 원문과 OS Stdout Exit Code 0 입증 없는 완료 선언 절대 금지 (제1절 제2조 / 제6절 제15조).  
> 4. **3계층 심층 영향도 고지 (IMPACT EXPLANATION)**: 데이터 흐름, 방어된 결함 시나리오, DX 체감 코드 변화 필수 해석 (제1절 제2조 4항 / IMPACT_ANALYSIS_GUIDE).  
> 5. **인간 최종 인수권 (HUMAN DECISION)**: 4단계 완료 보고서 제출 후 최종 승인은 오직 인간이 독점 결정한다 (제6절 제15조 4단계).

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

