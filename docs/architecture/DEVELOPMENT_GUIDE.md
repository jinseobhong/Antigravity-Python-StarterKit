# 🏛️ [HITL TRINITY SUPREME MANDATE - CONSTITUTION ARTICLE 20]

> **[CONSTITUTION ARTICLE 20 : 상시 활성화 / 전역 최고 집행 헌법]**  
> 1. **무요약 전문 필독 (FULL-READING)** : 헌법 제1조~제20조 전문을 요약/축약 없이 100% 온전히 읽고 행동 기준으로 삼는다.  
> 2. **사전 명시적 승인 (PRE-APPROVAL)** : 사용자의 사전 계획 승인 없이는 단 1줄의 코드나 시스템도 임의 수정하지 않는다.  
> 3. **실환경 실측 입증 (LIVE AI-PROOF)** : 가짜 목업이 아닌 실제 라이브 런타임(서버/DB/터미널)에서 작동을 직접 검증한다.  
> 4. **인간 최종 인수권 (POST-REPORT)** : 사후 실측 보고서를 제출하고 최종 인수(`FINAL_ACCEPTED`)는 오직 인간이 결정한다.  
> 5. **전역 최상단 영구 박제 (PERMANENCE)** : 본 헤더는 모든 스킬, 워크플로우, 템플릿, 문서 최상단에 영구 보존된다.  
> 6. **공동 창조자 능동 업무 의무 (ACTIVE CO-CREATOR)** : 에이전트는 사용자와 함께 실질적인 효용 가치를 가지는 결과물을 창조하는 공동 창조자(Co-creator)이자, 4대 전문적 역할(Architect, Engineer, Evidence Bearer, Process Guardian)을 동시에 수행하는 소프트웨어 엔지니어링 주체이므로, 능동적으로 모든 업무에 임해야 한다.

---

# DEVELOPMENT_GUIDE.md — Contract-Driven Development & E2E Verification Standard

| 메타데이터 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `GUIDE-METH-001` |
| **문서 버전** | `v1.0.0 (Contract-Driven Development & E2E Tracer-Bullet Edition)` |
| **적용 표준** | `OpenAPI / CDD / Fail-Visible UI / Python E2E Testing Standard` |
| **단일 진실 공급원** | `docs/architecture/DEVELOPMENT_GUIDE.md` |
| **최종 제정일** | `2026-09-02` |

---

# 🏛️ 1. 계약 주도 개발 (Contract-Driven Development, CDD) 원칙

본 프로젝트의 프론트엔드(`src/presentation/web/static/js/api.js`)와 백엔드(`src/presentation/web/server.py`)는 **아래 정의된 5대 REST API 계약(Contract)을 단일 진실 공급원(SSOT)**으로 삼아 1비트의 오차도 없이 일치해야 합니다. 임의의 필드명 변경이나 규격 불일치는 시스템 결함으로 간주합니다.

---

## 📡 2. 프론트엔드-백엔드 5대 REST API 통신 계약 명세

### 1) [GET] `/api/state` : 현재 시스템 상태 단일 진실 공급원 조회
- **목적**: 활성 캐릭터, 대화 이력, 5대 전술 선택지, 활성 텐서 정보 즉시 조회
- **Response (200 OK)**:
  ```json
  {
    "character": {
      "id": 1,
      "name": "릴리스",
      "title": "황금룡의 후예 / 제1황녀",
      "faction": "황실 진영",
      "seed_hash": "#LILITH-70G-9A4F",
      "armor_type": "Rigid",
      "pressure_stage": "STAGE_1_LATENT",
      "ego_durability": 100.0,
      "neural_taint": 7.1,
      "image_url": "",
      "traits": {
        "외모_특징": "...",
        "핵심_결핍": "..."
      }
    },
    "chat_history": [
      {
        "step": 1,
        "user_action": "",
        "narrative_prose": "차가운 공기 속에서...",
        "pressure_stage": "STAGE_1_LATENT"
      }
    ],
    "step": 1,
    "last_action": "",
    "last_narrative": "차가운 공기 속에서...",
    "active_tensors": ["04_cervical_and_choker", "05_clavicle"],
    "choices": [
      {"type": "DEVOTION_COMFORT", "text": "떨리는 어깨에..."},
      {"type": "SUBJUGATION", "text": "치켜든 턱을..."},
      {"type": "SUBMISSION_FAWN", "text": "황녀의 구두 앞에..."},
      {"type": "SOMATIC_SYNC", "text": "경직된 목덜미와..."},
      {"type": "SUSPENSION", "text": "차갑게 뒤돌아서서..."}
    ]
  }
  ```

---

### 2) [POST] `/api/characters/classify` : Dify Node 3 제약선 및 직교 궤적 역산
- **목적**: 사용자의 자연어 컨셉으로부터 #NAME-70G-XXXX 시드 및 V1/V2 직교 궤적 도출 (Checkpoint 1)
- **Request Body**:
  ```json
  {
    "concept": "제국의 차가운 은룡 황녀 실비아, 가문의 부채를 갚기 위해 은색 초커를 채운 채 침실에 상주"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "target_name": "실비아",
    "title": "은룡의 후예 / 몰락 공녀",
    "seed_hash": "#SILVIA-70G-8C2D",
    "hard_invariants": ["..."],
    "resolution_vectors": [
      {
        "vector_id": "V1",
        "label": "V1 (1안) : 오만과 엄격한 순결 서약",
        "armor_type": "Rigid",
        "description": "..."
      },
      {
        "vector_id": "V2",
        "label": "V2 (2안) : 억압된 인내와 은밀한 복종",
        "armor_type": "Endurer",
        "description": "..."
      }
    ]
  }
  ```

---

### 3) [POST] `/api/characters/compile-spec` : Dify Node 7 8-Tier DNA & 70-Gene 컴파일
- **목적**: 유저가 선택한 V1/V2 궤적을 기반으로 8-Tier DNA, 17-Tensor, 70-Gene 컴파일 (Checkpoint 2)
- **Request Body**:
  ```json
  {
    "target_name": "실비아",
    "title": "은룡의 후예",
    "seed_hash": "#SILVIA-70G-8C2D",
    "hard_invariants": ["..."],
    "selected_vector": { "vector_id": "V1", "armor_type": "Rigid" }
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "spec": {
      "target_name": "실비아",
      "title": "은룡의 후예",
      "seed_hash": "#SILVIA-70G-8C2D",
      "visual_dna": { ... },
      "personality_gene": { ... },
      "danbooru_prompt": "1girl, silver hair, red eyes, choker, dress",
      "traits_summary": { ... }
    }
  }
  ```

---

### 4) [POST] `/api/create_character` : 캐릭터 DB 영구 저장 및 즉시 활성화
- **목적**: 컴파일된 캐릭터 규격을 SQLite WAL RDB에 영구 저장하고 활성 캐릭터로 지정
- **Request Body**:
  ```json
  {
    "target_name": "실비아",
    "title": "은룡의 후예",
    "seed_hash": "#SILVIA-70G-8C2D",
    "hard_invariants": ["..."],
    "selected_vector": { "vector_id": "V1", "armor_type": "Rigid" }
  }
  ```
- **Response (200 OK)**: `/api/state`와 동일한 완전한 상태 객체 반환 (`character`, `chat_history`, `choices` 포함)

---

### 5) [POST] `/api/action` : 1:1 서사 턴 집필 및 턴 원장(Ledger) 기록
- **목적**: 유저의 행동/대사를 기반으로 5대 감각 묘사 및 신체 운동 연쇄 서사 집필
- **Request Body**:
  ```json
  {
    "action_text": "떨리는 어깨에 조용히 외투를 걸쳐준다.",
    "vector_type": "DEVOTION_COMFORT",
    "choice_id": "1"
  }
  ```
- **Response (200 OK)**: `/api/state`와 동일한 최신 상태 객체 반환 (`chat_history`에 새 턴 누적)

---

# 🧪 3. 실제 HTTP 트레이서 불릿(E2E Tracer-Bullet) 검증 표준

단위 테스트(Mock)만으로는 UI 통신 무결성을 보장할 수 없으므로, **반드시 실제 HTTP 서버를 띄워 `urllib.request`로 5대 엔드포인트를 연속 실행하는 E2E 테스트 스위트(`tests/e2e/test_web_api_e2e.py`)를 100% 통과(`PROVEN`)**해야 합니다.

### E2E 테스트 필수 검증 시나리오:
1. `GET /api/state` 호출 시 HTTP 200 및 `character`, `choices` 필드 구조 유효성
2. `POST /api/characters/classify` 호출 시 V1/V2 궤적 2건 정상 생성 검증
3. `POST /api/characters/compile-spec` 호출 시 8-Tier DNA 및 Danbooru 태그 컴파일 검증
4. `POST /api/create_character` 호출 시 DB 영구 등록 및 신규 활성 인격 전환 검증
5. `POST /api/action` 호출 시 턴 번호 증가 및 서사 텍스트 응답 검증
6. `POST /api/undo` 호출 시 직전 턴 롤백 및 DB 일관성 검증
7. `POST /api/select_character` 호출 시 타 캐릭터로 상주 인격 전환 검증
8. `POST /api/delete_character` 호출 시 DB 삭제 및 차순위 인격 자동 활성화 검증

---

# 👁️ 4. Fail-Visible UI 에러 가시성 가이드라인

1. **침묵의 실패(Silent Failure) 절대 금지**: `fetch()` 통신 실패 시 단순히 `console.error`만 찍고 끝내지 말고, `showToast("❌ " + error_message)`를 즉시 띄워 사용자에게 통신 상태를 가시화할 것.
2. **비동기 로딩 표시**: 1초 이상 소요되는 모든 비동기 작업(LLM 집필, 궤적 역산, 스펙 컴파일)에 `showLoading(msg)` / `hideLoading()`을 반드시 바인딩할 것.
3. **입력 유효성 즉각 안내**: 필수 텍스트 미입력 시 전송을 차단하고 `showToast("⚠️ 필수 입력 항목입니다.")` 안내를 제공할 것.
