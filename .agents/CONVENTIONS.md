# 🏛️ Antigravity Master Governance & Conventions Hub

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `SPEC-HUB-001` |
| **표준 버전** | `v2.0.0` (Modular Hub-and-Spoke Edition) |
| **적용 범위** | Antigravity 전체 시스템 산출물 (코드, 문서, 구조, 프로세스 일체) |
| **상태** | `ENFORCED (상시 강제 적용)` |
| **최종 개정일** | `2026-09-02` |

---

## 📌 1. 목적 및 철학 (Purpose & Hub Role)

본 문서는 프로젝트 내 모든 소프트웨어 엔지니어링 산출물의 **규격화(Total Standardization)를 총괄하는 중앙 표준화 기구(Master Standards Hub)**이다.

모놀리식 단일 파일 방식의 컨텍스트 낭비를 배제하고, 관심사 분리(Separation of Concerns) 원칙에 따라 각 전문 영역별 세부 사양서로 분할·인덱싱하여 관리한다.

---

## 🧭 2. 전사 규격서 인덱스 매트릭스 (Master Specifications Matrix)

| 분류 (Domain) | 공식 세부 규격서 (Link) | 핵심 역할 및 표준화 대상 |
| :--- | :--- | :--- |
| **💻 코드 표준** | [CODING_STANDARDS.md](./docs/CODING_STANDARDS.md) | 파이썬 엄격한 정적 타입 힌트(PEP 484), Pure Domain 불변 모델, 커스텀 도메인 예외 계층, AAA 단위 테스트 패턴, Google Docstring. |
| **📜 문서 문체** | [STYLE_GUIDE.md](./docs/STYLE_GUIDE.md) | 엔지니어링 문서의 절제된 공학 문체, RFC 2119 표준 키워드(`MUST`, `SHOULD`), 메타데이터 헤더 의무화, 정량적 증거 기술. |
| **💬 대화 규격** | [TONE_AND_MANNER.md](./docs/TONE_AND_MANNER.md) | 품격 있는 시니어 파트너 톤, 전문+Diff 3단 대조, 시스템 영향도 중심 해석, 상황별 표준 대화 예제. |
| **🔍 영향도 분석** | [IMPACT_ANALYSIS_GUIDE.md](./docs/IMPACT_ANALYSIS_GUIDE.md) | 시스템 영향도 3계층 심층 분석(데이터 흐름, 방어된 결함 시나리오, 1인 개발자 체감 코드 변화). |
| **📂 파일 및 뷰** | [FILESYSTEM_SPEC.md](./docs/FILESYSTEM_SPEC.md) | Clean Architecture 4계층 디렉터리 구조, `views/` 5대 실시간 관측 뷰 단일 진실(SSOT) 규격, 브레인-프로젝트 트윈콜(Twin-Call) 동기화. |
| **🔄 프로세스** | [LIFECYCLE_SPEC.md](./docs/LIFECYCLE_SPEC.md) | 4-Track 동적 라우팅, 2-Phase [Architect ➔ Implement] 라이프사이클, 4단계 파이프라인 및 터미널 실측 AI Proof 검증. |
| **🌿 형상 관리** | [GIT_WORKFLOW_SPEC.md](./docs/GIT_WORKFLOW_SPEC.md) | Trunk-Based 브랜칭, Pre-Commit 검증 통과 의무, Conventional Commits 7대 표준 접두어 규격. |

---

## 🏛️ 3. 거버넌스 4대 축의 역할 분담

1. **🔴 최고 헌법 (`GEMINI.md`)**: 절대 성역 방어, 7대 금지사항, 고위험 작업 승인 게이트 (*안전 및 보안 통제*)
2. **🏛️ 규격 허브 (`CONVENTIONS.md` & `docs/`)**: 코드, 문서, 구조, 프로세스의 정적 품질 및 형식 표준 (*총괄 규격화*)
3. **⚙️ 실행 엔진 (`workflows/` & `skills/`)**: 인간 명령 인터페이스와 AI 자율 실행 런북의 1:1 대칭 파이프라인 (*작업 실행 절차*)
4. **👁️ 관측 및 감사 (`views/` & `store/state.db`)**: 5대 실시간 프로젝트 뷰와 SQLite 영구 트랜잭션 로그 (*실시간 투명성 & 감사*)

---

## 🛠️ 4. 규격 검증 및 상태 감사 도구

모든 규격의 대칭성과 상태는 자동화 도구로 상시 검증할 수 있다:

```powershell
# 1. 원클릭 전사 무결성 검증 (단위 테스트 + 뷰 대칭성 + 11대 문서 DB 스냅샷)
py -3 .agents/scripts/run_checks.py

# 2. 개별 워크플로/스킬/템플릿 대칭성 검증
py -3 .agents/scripts/verify_sync.py

# 3. SQLite 거버넌스 감사 저장소 상태 조회
py -3 .agents/scripts/log_task.py --status
```

