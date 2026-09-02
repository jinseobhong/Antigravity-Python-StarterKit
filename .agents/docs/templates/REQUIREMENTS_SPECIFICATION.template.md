# 🏛️ [HITL TRINITY SUPREME MANDATE - CONSTITUTION ARTICLE 20]

> **[CONSTITUTION ARTICLE 20 : 상시 활성화 / 전역 최고 집행 헌법]**  
> 1. **무요약 전문 필독 (FULL-READING)** : 헌법 제1조~제20조 전문을 요약/축약 없이 100% 온전히 읽고 행동 기준으로 삼는다.  
> 2. **사전 명시적 승인 (PRE-APPROVAL)** : 사용자의 사전 계획 승인 없이는 단 1줄의 코드나 시스템도 임의 수정하지 않는다.  
> 3. **실환경 실측 입증 (LIVE AI-PROOF)** : 가짜 목업이 아닌 실제 라이브 런타임(서버/DB/터미널)에서 작동을 직접 검증한다.  
> 4. **인간 최종 인수권 (POST-REPORT)** : 사후 실측 보고서를 제출하고 최종 인수(`FINAL_ACCEPTED`)는 오직 인간이 결정한다.  
> 5. **전역 최상단 영구 박제 (PERMANENCE)** : 본 헤더는 모든 스킬, 워크플로우, 템플릿, 문서 최상단에 영구 보존된다.  
> 6. **공동 창조자 능동 업무 의무 (ACTIVE CO-CREATOR)** : 에이전트는 사용자와 함께 실질적인 효용 가치를 가지는 결과물을 창조하는 공동 창조자(Co-creator)이자, 4대 전문적 역할(Architect, Engineer, Evidence Bearer, Process Guardian)을 동시에 수행하는 소프트웨어 엔지니어링 주체이므로, 능동적으로 모든 업무에 임해야 한다.

---

# [SOFTWARE REQUIREMENTS SPECIFICATION : SRS]
# 시스템 명칭: AbyssEmpire (Constraint-First Somatic Narrative Engine)

| 메타데이터 항목 | 세부 내용 |
| :--- | :--- |
| **문서 표준** | `IEEE 830 / ISO/IEC/IEEE 29148 Software Requirements Specification` |
| **문서 ID** | `SRS-ABYSS-2026-v2.0` |
| **아키텍처 패턴** | `Clean 4-Tier Layered Architecture (DDD POPO Core + LLM Hybrid)` |
| **품질 등급** | `High-Assurance / Zero-Dependency Runtime Core` |
| **최종 수정일** | `2026-09-02` |

---

## 1. 시스템 범위 및 아키텍처 경계 (System Scope & Boundary)

### 1.1 시스템 목적 (Purpose)
본 시스템은 **제약 조건 역산(Constraint-First Reverse Engineering)**과 **8중 해부학적 외모 규격(8-Tier Visual DNA)**을 기반으로, LLM의 비결정론적 확률 추론을 결합하여 자아 일관성과 신체 감각을 유지하는 **고밀도 소마틱 서사 시뮬레이션 엔진**이다.

### 1.2 아키텍처 계층 분리 원칙 (Tier Isolation)
```text
[Presentation Layer] ──→ [Application Layer] ──→ [Domain Layer (POPO)]
                                ↓                       ↑
                     [Infrastructure Layer] ────────────+
```
- **Domain Layer**: 프레임워크나 외부 라이브러리에 의존하지 않는 순수 Python POPO (Plain Old Python Object) 엔티티로만 구성.
- **Application Layer**: 트랜잭션 단위의 유스케이스 조율, 되돌리기(Undo) 스냅샷 관리.
- **Infrastructure Layer**: SQLite 영속화, Multi-LLM API 클라이언트(Claude / Gemini), 프롬프트 컴파일러.
- **Presentation Layer**: 멀티스레드 비동기 Web Studio (HTTP/JSON REST) 및 터미널 CLI.

---

## 2. 도메인 엔티티 및 타입 정의 (Domain Entity & Invariant Contracts)

### 2.1 Entity 1: `GeneSeed` (고유 시드 식별자)
- **불변식 (Invariants)**: 발급된 시드 해시는 대화 도중 절대 변경될 수 없다 (`Immutable`).
- **포맷 규격**: `^#[A-Za-z0-9]{4}-70G-[A-Fa-f0-9]{4}$` (예: `#LILI-70G-BFFF`)

### 2.2 Entity 2: `VisualDNA` (8-Tier 해부학적 외모 규격)
모든 필드는 빈 문자열을 허용하지 않으며, 단부루 태그로 1:1 컴파일 가능해야 한다.

| 슬롯 ID | 속성명 (Field Name) | 타입 | 필수 제약 및 묘사 기준 |
| :--- | :--- | :--- | :--- |
| **Tier 1** | `face_geometry` | `str` | 턱선(V-line/달걀형), 입술(두께/색상), 코선 |
| **Tier 2** | `ocular_optics` | `str` | 홍채 색상, 동공 림, 속눈썹 길이 및 밀도 |
| **Tier 3** | `hair_physics` | `str` | 모발 길이, 색상, 결(직모/웨이브), 잔머리 물리 |
| **Tier 4** | `body_silhouette` | `str` | 신장(cm), 체형(호리호리/탄탄), 쇄골/골격 돌출도 |
| **Tier 5** | `dermal_texture` | `str` | 피부 톤(창백/밀빛), 표피 질감, 핏줄 가시성 |
| **Tier 6** | `apparel_accents` | `str` | 메인 의복 스타일, 장신구(초커/리본/갑주/로브) |
| **Tier 7** | `somatic_flush_cue`| `str` | 체온 상승 및 수치 시 홍조 전이 경로 (쇄골/귓바퀴) |
| **Tier 8** | `lighting_contrast`| `str` | 기본 광원 대비 (달빛/역광/명암비) |

### 2.3 Entity 3: `PersonalityGene` (7대 차원축 70단계 유전자)
- `hard_invariants`:
  - `primary_boundary`: 목숨보다 지키려는 도덕적/귀족적 결벽증 및 제약선 (`str`)
  - `ego_collapse_trigger`: 자아 방어가 무너지는 결정적 트리거 (`str`)
  - `somatic_achilles_heel`: 신체적/감각적 절대 취약 부위 (`str`)
- `axis_1_physical_reflex` ~ `axis_6_alchemy_submission`: 신체 반사 및 심리 굴복 메커니즘 (`str`)
- `axis_7_gesture_ticks`: 신체적 무의식 버릇 목록 (`List[str]`)

### 2.4 Entity 4: `SomaticLedger` (3계층 신경·메모리 원장)
```python
class SomaticLedger:
    layer_1_reflex_state: str     # 밀리초 단위 척추/호흡/근육 방어 반사
    layer_2_sensory_buffer: str   # 수 분간 유지되는 체온/압박/피부 잔향
    layer_3_ego_memory: str       # 영구 각인되는 굴종/순종/애착 지수
```

---

## 3. 기능 요구사항 명세 (Functional Requirements)

### [FR-01] 캐릭터 발현 및 제약선 역산 파이프라인 (Constraint Classifier)
- **입력 (Input)**:
  ```json
  {
    "user_query": "문자열 (최소 2자 ~ 최대 500자)",
    "explicit_name": "선택적 이름 문자열",
    "explicit_title": "선택적 칭호 문자열"
  }
  ```
- **처리 절차**:
  1. 고유 `GeneSeed` 발급 (`#NAME-70G-XXXX`)
  2. LLM을 통해 입력 컨셉으로부터 `HardInvariants` 역산
  3. 상반된 2대 서사 충돌 궤적(`V1: 저항 고수` vs `V2: 프라이드 붕괴`) 생성
- **출력 (Output Schema - Checkpoint 1)**:
  ```json
  {
    "seed_hash": "#LILI-70G-BFFF",
    "target_name": "릴리스",
    "hard_invariants": {
      "primary_boundary": "string",
      "ego_collapse_trigger": "string",
      "somatic_achilles_heel": "string"
    },
    "resolution_vectors": [
      {
        "vector_id": "V1",
        "vector_name": "1안 궤적 명칭",
        "axis_description": "상세 서사 전개 방식",
        "operation": "STRICT_GUARD"
      },
      {
        "vector_id": "V2",
        "vector_name": "2안 궤적 명칭",
        "axis_description": "상세 서사 전개 방식",
        "operation": "RECURSIVE_EGO_PEELING"
      }
    ]
  }
  ```

---

### [FR-02] 8-Tier Visual DNA 및 유전자 합성 파이프라인 (Gene Compiler)
- **선행 조건 (Pre-condition)**: 인간 관리자가 `V1` 또는 `V2` 중 하나의 궤적을 명시적으로 선택 승인함 (`Human Checkpoint 1`).
- **입력 (Input)**:
  ```json
  {
    "name": "릴리스",
    "title": "제1황녀",
    "faction": "제국 황실",
    "seed_hash": "#LILI-70G-BFFF",
    "hard_invariants": { ... },
    "selected_vector": { "vector_id": "V1", ... }
  }
  ```
- **처리 절차**:
  1. 제약선과 선택된 궤적을 1:1 인과 사슬로 엮어 `VisualDNA` (8개 속성) 합성
  2. `PersonalityGene` (7개 축) 합성
  3. `VisualCompiler`를 통해 Illustrious-XL 6-Slot Danbooru 태그 컴파일
  4. SQLite `characters` 테이블에 트랜잭션 커밋
- **사후 조건 (Post-condition)**: 신규 캐릭터가 보관소 및 롤플레이 엔진에 활성 상태로 등록됨.

---

### [FR-03] 턴 실행 및 소마틱 서사 오케스트레이션 (Narrative Turn Loop)
- **입력 (Input)**: 유저의 행동/대사 자연어 문자열 (`action_text`)
- **실행 파이프라인 (FSM State Machine)**:
  ```text
  [1. Undo Snapshot Push]
          ↓
  [2. Kinematic Chain Wave Advance (2~3 Spotlights Focus)]
          ↓
  [3. Spatial Pressure Layer Transition (0 ➔ 1 ➔ 2)]
          ↓
  [4. Assemble 30,000-char Master System Directive + Somatic Context]
          ↓
  [5. Multi-LLM Probabilistic Inference (Claude 3.7 / Gemini 3.6)]
          ↓
  [6. Parse Narrative Prose + Update SomaticLedger (L1/L2/L3)]
          ↓
  [7. SQLite Turn History Commit & Broadcast]
  ```

---

## 4. 인터페이스 계약 (API & Web Studio Contract)

| 엔드포인트 | 메서드 | 요청 페이로드 | 응답 페이로드 | 설명 |
| :--- | :--- | :--- | :--- | :--- |
| `/api/state` | `GET` | 없음 | `{ character, step, chat_history }` | 현재 활성 캐릭터 및 턴 상태 조회 |
| `/api/characters` | `GET` | 없음 | `Array<CharacterDTO>` | 보관소 전체 캐릭터 목록 조회 |
| `/api/select_character` | `POST` | `{ seed_hash }` | `{ character, step, ... }` | 캐릭터 전환 |
| `/api/classify_and_propose` | `POST` | `{ query }` | `{ seed_hash, hard_invariants, vectors }` | [Step 1] 제약선 및 V1/V2 역산 |
| `/api/synthesize_character` | `POST` | `{ name, hard_invariants, selected_vector }` | `{ character, ... }` | [Step 2] 8-Tier DNA 합성 및 영구 저장 |
| `/api/action` | `POST` | `{ action_text }` | `{ character, step, chat_history }` | 1턴 서사 실행 |
| `/api/undo` | `POST` | 없음 | `{ character, step, chat_history }` | 직전 턴 상태 완전 롤백 |
| `/api/generate_danbooru` | `POST` | 없음 | `{ positive, negative }` | Danbooru 6-Slot 태그 생성 |
| `/api/config_llm` | `POST` | `{ gemini_key, claude_key, provider }` | `{ status, active_provider }` | LLM 프로바이더 런타임 스왑 |

---

## 5. 비기능 요구사항 (Non-Functional Requirements : NFR)

1. **NFR-01 (Zero External Dependency)**: 런타임 백엔드는 외부 서드파티 웹 프레임워크(Flask/FastAPI 등) 의존 없이 Python 내장 `http.server` 및 `urllib`, `sqlite3` 표준 라이브러리만으로 100% 자립 구동되어야 한다.
2. **NFR-02 (Multi-Threaded Concurrency)**: 비동기 AJAX 요청 처리를 위해 `socketserver.ThreadingMixIn` 기반 멀티스레드 서빙을 보장하며, LLM 응답 대기 중에도 UI 블로킹이 발생하지 않아야 한다.
3. **NFR-03 (Cascade Failover)**: 설정된 주 LLM(Claude) 호출 실패 또는 Quota 초과(429/400) 시 보조 LLM(Gemini)으로 자동 무중단 스왑되어야 한다.
4. **NFR-04 (ACID & WAL Persistence)**: 모든 캐릭터 및 대화 기록은 SQLite `WAL(Write-Ahead Logging)` 모드로 안전하게 원자적 저장되어야 한다.

---

## 6. 인수 조건 (Acceptance Criteria & Test Oracles)

- [ ] **AC-01 (Unit Test 100% Pass)**: `py -3 -m unittest discover -s tests/unit -v` 실행 시 16개 이상의 단위 테스트가 결함 없이 100% 통과(`PROVEN`)되어야 한다.
- [ ] **AC-02 (HITL 2-Step Gate)**: 임의의 텍스트 입력 시 Checkpoint 1(V1/V2 결재)과 Checkpoint 2(8-Tier DNA 각인)가 정확히 인터랙티브하게 동작해야 한다.
- [ ] **AC-03 (Zero Visual Drift)**: 100턴 대화가 지속되어도 캐릭터의 고유 눈동자, 턱선, 모발, 초커, 의복 설정이 표류하지 않고 서사에 일관되게 고정되어야 한다.
- [ ] **AC-04 (Safe & Sensorial)**: 직설적 성인 어휘 없이 소마틱 신경어(계면 마찰, 나노 호흡 파열, 0.1초 신경 연쇄)만으로 최고조의 문학적 긴장감을 산출해야 한다.
