# 🏛️ ARCHITECTURE.md — Clean Architecture 4-Tier 시스템 아키텍처

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `VIEW-ARCH-001` |
| **아키텍처 패턴** | `Clean Architecture 4-Tier Layered Pattern` |
| **적용 원칙** | 의존성 역전 원칙(DIP), 도메인 순수성(Pure Domain), 관심사 분리(SoC) |
| **최종 갱신일** | `2026-09-02` |

---

## 🧭 1. 계층 구조 및 단방향 의존성 방향

```text
[ Presentation Layer (Web API / CLI / UI) ]
                     ↓
[ Application Layer (Use Cases / Orchestrators / Services) ]
                     ↓
[ Domain Layer (Pure Entities / Value Objects / Domain Events) ]  <-- (의존성 0%)
                     ↑
[ Infrastructure Layer (SQLite Repositories / Adapters / External APIs) ]
```

---

## 🏛️ 2. 4대 계층별 책임 및 격리 규격

1. **`src/domain/` (도메인 계층)**:
   - 외부 라이브러리(DB, HTTP 등) 의존성이 완전히 0인 순수 불변 객체(`@dataclass(frozen=True)`).
   - 비즈니스 핵심 규칙 및 도메인 커스텀 예외(`DomainError`) 전담.
2. **`src/infrastructure/` (인프라 계층)**:
   - SQLite WAL 모드 트랜잭션 매니저(`DatabaseManager`) 및 도메인 인터페이스를 구현하는 리포지토리 어댑터.
3. **`src/application/` (애플리케이션 계층)**:
   - 유스케이스 흐름 제어, 트랜잭션 조율, 도메인-인프라 간 오케스트레이션.
4. **`src/presentation/` (프레젠테이션 계층)**:
   - FastAPI REST API 엔드포인트 또는 터미널 CLI 인터페이스.
