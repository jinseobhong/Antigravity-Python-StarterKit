# 🏛️ [GLOBAL CONSTITUTION v2.2 & HITL TRINITY MANDATE]

> **[AI ARCHITECT GLOBAL CONSTITUTION v2.2 : 상시 활성화 / 전역 최고 거버넌스 규격]**  
> 1. **절대 성역 방어 (SACRED ZONE)**: `GEMINI.md`, `.rules/`, `.gitignore`, `.env`에 대한 임의 수정 원천 차단 (제0절 제1조).  
> 2. **사전 명시적 인가 (PRE-AUTHORIZATION)**: 고위험 작업 시 명시적 "승인(APPROVE)" 키워드 득속 전 파일 수정 봉쇄 (제2절 제8조/제9조).  
> 3. **실환경 실측 증명 (AI PROOF)**: 실제 터미널 명령어 원문과 OS Stdout Exit Code 0 입증 없는 완료 선언 절대 금지 (제1절 제2조 / 제6절 제15조).  
> 4. **3계층 심층 영향도 고지 (IMPACT EXPLANATION)**: 데이터 흐름, 방어된 결함 시나리오, DX 체감 코드 변화 필수 해석 (제1절 제2조 4항 / IMPACT_ANALYSIS_GUIDE).  
> 5. **인간 최종 인수권 (HUMAN DECISION)**: 4단계 완료 보고서 제출 후 최종 승인은 오직 인간이 독점 결정한다 (제6절 제15조 4단계).

---
# 시스템 요구사항 명세서 (Software Requirements Specification)

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `SRS-[PROJECT_CODE]-[YEAR]-v1.0` |
| **시스템 명칭** | `[Project Name]` |
| **개발 패러다임** | `Clean Architecture 4-Tier Pattern` + `Deterministic AI Governance` |
| **작성일 / 개정일** | `YYYY-MM-DD` |
| **상태** | `DRAFT / APPROVED` |

---

## 🎯 1. 프로젝트 개요 및 비전 (Project Overview & Vision)

### 1.1 핵심 목적
- 본 프로젝트의 궁극적인 비즈니스 목적과 해결하고자 하는 핵심 문제를 기술합니다.

### 1.2 대상 사용자 (Target Audience)
- 본 시스템을 사용하는 핵심 페르소나 및 사용자 정의.

---

## 🏛️ 2. 도메인 엔티티 및 데이터 구조 (Domain Entities & Models)

### 2.1 불변 도메인 모델 (`@dataclass(frozen=True)`)
```python
@dataclass(frozen=True)
class ExampleEntity:
    """핵심 도메인 불변 엔티티 규격"""
    entity_id: str
    name: str
    status: str
    created_at: float
```

### 2.2 도메인 불변식 및 검증 규칙 (Invariants)
- **INV-01**: `entity_id`는 공백일 수 없으며 고유한 UUID 형식을 유지해야 한다.
- **INV-02**: 모든 상태 전이는 유효한 라이프사이클 규칙을 따라야 한다.

---

## ⚙️ 3. 기능 요구사항 (Functional Requirements - FR)

### [FR-01] 핵심 유스케이스 정의
- **설명**: 시스템이 제공해야 하는 핵심 기능의 입출력 및 비즈니스 로직.
- **입력 (Input)**: 유효성 검증을 마친 DTO 파라미터.
- **처리 흐름 (Processing Pipeline)**:
  1. 입력값 검증 및 도메인 엔티티 생성
  2. 비즈니스 규칙 검증 및 트랜잭션 처리
  3. SQLite 리포지토리 영구 커밋
- **출력 (Output)**: 처리 결과 DTO 및 이벤트 발행.

---

## 🌐 4. 인터페이스 규격 (API & CLI Endpoints)

| 엔드포인트 | 메서드 | 요청 규격 | 응답 규격 | 설명 |
| :--- | :---: | :--- | :--- | :--- |
| `/api/health` | `GET` | 없음 | `{ status: "ok" }` | 시스템 헬스체크 |
| `/api/items` | `POST` | `{ name: str }` | `{ item_id: str, ... }` | 신규 엔티티 생성 |

---

## 🛡️ 5. 비기능 요구사항 (Non-Functional Requirements - NFR)

1. **품질 검증 (AI Proof)**: 모든 기능은 `run_checks.py` 4단계 파이프라인(Unit+E2E+Sync)을 100% 무결하게 통과해야 한다.
2. **원자성 (ACID)**: 모든 영구 저장은 SQLite WAL 모드 트랜잭션을 통해 데이터 오염 없이 안전하게 격리되어야 한다.
