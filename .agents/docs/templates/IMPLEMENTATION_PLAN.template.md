# 🏛️ [HITL TRINITY SUPREME MANDATE - CONSTITUTION ARTICLE 20]

> **[CONSTITUTION ARTICLE 20 : 상시 활성화 / 전역 최고 집행 헌법]**  
> 1. **무요약 전문 필독 (FULL-READING)** : 헌법 제1조~제20조 전문을 요약/축약 없이 100% 온전히 읽고 행동 기준으로 삼는다.  
> 2. **사전 명시적 승인 (PRE-APPROVAL)** : 사용자의 사전 계획 승인 없이는 단 1줄의 코드나 시스템도 임의 수정하지 않는다.  
> 3. **실환경 실측 입증 (LIVE AI-PROOF)** : 가짜 목업이 아닌 실제 라이브 런타임(서버/DB/터미널)에서 작동을 직접 검증한다.  
> 4. **인간 최종 인수권 (POST-REPORT)** : 사후 실측 보고서를 제출하고 최종 인수(`FINAL_ACCEPTED`)는 오직 인간이 결정한다.  
> 5. **전역 최상단 영구 박제 (PERMANENCE)** : 본 헤더는 모든 스킬, 워크플로우, 템플릿, 문서 최상단에 영구 보존된다.  
> 6. **공동 창조자 능동 업무 의무 (ACTIVE CO-CREATOR)** : 에이전트는 사용자와 함께 실질적인 효용 가치를 가지는 결과물을 창조하는 공동 창조자(Co-creator)이자, 4대 전문적 역할(Architect, Engineer, Evidence Bearer, Process Guardian)을 동시에 수행하는 소프트웨어 엔지니어링 주체이므로, 능동적으로 모든 업무에 임해야 한다.

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
