# 🏛️ [GLOBAL CONSTITUTION v2.2 & HITL TRINITY MANDATE]

> **[AI ARCHITECT GLOBAL CONSTITUTION v2.2 : 상시 활성화 / 전역 최고 거버넌스 규격]**  
> 1. **절대 성역 방어 (SACRED ZONE)**: `GEMINI.md`, `.rules/`, `.gitignore`, `.env`에 대한 임의 수정 원천 차단 (제0절 제1조).  
> 2. **사전 명시적 인가 (PRE-AUTHORIZATION)**: 고위험 작업 시 명시적 "승인(APPROVE)" 키워드 득속 전 파일 수정 봉쇄 (제2절 제8조/제9조).  
> 3. **실환경 실측 증명 (AI PROOF)**: 실제 터미널 명령어 원문과 OS Stdout Exit Code 0 입증 없는 완료 선언 절대 금지 (제1절 제2조 / 제6절 제15조).  
> 4. **3계층 심층 영향도 고지 (IMPACT EXPLANATION)**: 데이터 흐름, 방어된 결함 시나리오, DX 체감 코드 변화 필수 해석 (제1절 제2조 4항 / IMPACT_ANALYSIS_GUIDE).  
> 5. **인간 최종 인수권 (HUMAN DECISION)**: 4단계 완료 보고서 제출 후 최종 승인은 오직 인간이 독점 결정한다 (제6절 제15조 4단계).

---

# IMPLEMENTATION_PLAN.md — 작업 구현 계획서

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-[MODULE]-[NUM]` |
| **문서 버전** | `v1.0.0` |
| **작성 일자** | `[YYYY-MM-DD]` |
| **상태** | `REVIEW_REQUIRED (사용자 사전 승인 대기)` |
| **작성자 / 승인자** | `AI Architect` / `Human Lead` |

---

## 📁 1. 변경 대상 파일 목록 (File Modifications)

| 변경 구분 | 대상 파일 경로 | 변경 목적 및 구현 내용 |
| :---: | :--- | :--- |
| `[NEW]` | `src/auth/password_reset.py` | 비밀번호 재설정 토큰 발급 및 검증 로직 |
| `[MODIFY]` | `src/auth/service.py` | 재설정 요청 핸들러 및 이메일 발송 연동 |
| `[NEW]` | `tests/test_password_reset.py` | 비밀번호 재설정 단위 및 예외 시나리오 테스트 |

---

## 🛠️ 2. 단계별 구현 순서 (Implementation Steps)
1. **[1단계: 테스트 작성]**: 만료된 토큰 및 정상 토큰에 대한 단위 테스트 작성
2. **[2단계: 핵심 로직 구현]**: `password_reset.py`에 토큰 해싱 및 검증 함수 구현
3. **[3단계: 서비스 통합]**: 기존 `service.py`에 재설정 함수 연결
4. **[4단계: 실측 검증]**: `pytest tests/test_password_reset.py` 실행 및 통과 로그 확보

---

## 🔄 3. 롤백 방안 (Rollback Strategy)
- 문제 발생 시 신규 생성 파일 삭제 및 `service.py`를 `git restore`로 즉시 원복.

---

## 🧪 4. 검증 계획 (Verification Plan)
- **실행할 테스트 명령어**: `pytest tests/test_password_reset.py -v`
- **목표 검증 기준**: 5개 테스트 케이스 100% Pass 및 린트 에러 0건

---

## 🛑 사용자 승인 (User Approval Gate)
- [ ] **사용자 명시적 승인 (User Approval)**: `APPROVED` (승인 완료 시 구현 착수)
