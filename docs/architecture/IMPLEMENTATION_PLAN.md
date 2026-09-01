# [IMPLEMENTATION PLAN : Clean 4-Tier Database-First Abyss Engine]

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-ABYSS-003` |
| **문서 버전** | `v1.0.0 (Database-First & Zero Hardcoding Edition)` |
| **철학 및 원칙** | `데이터베이스 영속화 및 실물 도메인 모델 우선 구축 ➔ UI 동적 바인딩` |
| **적용 표준** | `Clean 4-Tier Layered Architecture (DDD POPO Core)` |
| **상태** | `PROPOSED (승인 대기)` |

---

## 🏛️ 1. 개발 5단계 순차 파이프라인 (Step-by-Step Architecture Pipeline)

```text
[Step 1. 순수 도메인 모델 (POPO)]
  ├── 8-Tier Visual DNA & 16 RDB Traits 엔티티
  ├── 5대 심리 지표(신뢰/성애/수치/죄책/굴종) & 생체 지표(ODO/TAINT)
  ├── 7대 차원축 70단계 유전자 & 불변 제약선(Hard Invariants)
  └── 3계층 신경·메모리 원장 & 7단계 신체 운동 연쇄(Kinematic Chain)
        ↓
[Step 2. 데이터베이스 스키마 & CRUD 리포지토리]
  ├── SQLite WAL 모드 영속화 스키마 (`characters`, `turn_ledger`)
  ├── 16 RDB Traits 및 8-Tier DNA 직렬화/역직렬화 리포지토리
  └── 4대 대표 아키타입(릴리스, 에이라, 세라피나, 실비아) 실물 RDB 시딩
        ↓
[Step 3. 유스케이스 및 애플리케이션 서비스]
  ├── ClassifierService: 제약선 역산 및 직교 2대 궤적(V1 vs V2) 도출
  ├── GeneSynthesisService: 8-Tier 외모 + 70단계 유전자 동적 합성
  ├── NarrativeOrchestrator: 5대 심리 수치 및 3-Tier 원장 실시간 갱신
  └── UndoManager: TurnSnapshot 기반 불변 롤백 관리자
        ↓
[Step 4. 도메인 & DB 단위 테스트 전수 검증 (AI Proof)]
  └── `py -3 -m unittest discover -s tests/unit -v` 100% Pass 입증
        ↓
[Step 5. UI/UX 웹 스튜디오 동적 연동 (Zero Hardcoding)]
  └── 하드코딩 일체 없이, DB API로부터 실물 캐릭터 데이터를 100% 동적 렌더링
```

---

## 📁 2. 컴포넌트별 생성/구현 파일 명세

### 1) 도메인 계층 (`src/domain/`)
- `gene_seed.py`: 고유 시드 해시 (`#NAME-70G-XXXX`) 앵커링
- `visual_dna.py`: 8-Tier 해부학적 외모 규격 모델
- `personality_gene.py`: 7대 축 70단계 유전자 & `HardInvariants` 제약선 모델
- `somatic_ledger.py`: 3계층 신경·메모리 원장 (Layer 1, Layer 2, Layer 3)
- `character_traits.py`: 16대 RDB Traits & 5대 심리 게이지 (신뢰, 성애, 수치심, 죄책감, 굴종) 모델
- `spatial_pressure.py`: 3-Layer 공간 압력 챔버 (Layer 0, Layer 1, Layer 2)
- `kinematic_chain.py`: 7단계 신체 운동 연쇄 파동 전이 엔진
- `character.py`: Character 애그리게이트 루트

### 2) 인프라 계층 (`src/infrastructure/`)
- `database/db_manager.py`: SQLite WAL 커넥션 및 트랜잭션 관리자
- `database/repositories.py`: `CharacterRepository` (CRUD, Import, Export), `TurnLedgerRepository`
- `media/visual_compiler.py`: Illustrious-XL 6-Slot 단부루 태그 컴파일러
- `llm/client.py`: MultiLLMClient (Claude 3.7 / Gemini 3.6 자동 캐스케이드)
- `llm/prompt_synthesizer.py`: 30,000자급 마스터 헌법 & 턴별 프롬프트 조립기

### 3) 애플리케이션 계층 (`src/application/`)
- `classifier_service.py`: 제약선 역산 및 직교 2대 궤적(V1 vs V2) 분류기
- `gene_synthesis_service.py`: 8-Tier 외모 + 70단계 유전자 동적 합성 및 RDB 저장
- `narrative_orchestrator.py`: 완급 조절(Level 1~3), 운동 연쇄, 3-Tier 원장 갱신
- `undo_manager.py`: 불변 롤백 스택

### 4) 단위 테스트 계층 (`tests/unit/`)
- `test_domain_models.py`: 도메인 엔티티 무결성 검증
- `test_database_crud.py`: SQLite WAL 및 Character/TurnLedger CRUD 실물 검증
- `test_application_services.py`: 제약선 역산 및 유전자 합성 파이프라인 검증

### 5) 프레젠테이션 계층 (`src/presentation/`) - *DB 검증 완료 후 진행*
- `web/server.py`: ThreadedHTTPServer 기반 REST API 서버
- `web/static/`: 캡처 UI와 1:1 일치하는 모듈화 JS/CSS (DB 데이터 100% 동적 렌더링)
- `web/templates/index.html`: 메인 로비, 플레이 룸, 캐릭터 스튜디오 3대 뷰

---

## 🧪 3. 검증 계획 (Verification Plan)
- `py -3 -m unittest discover -s tests/unit -v` 실행하여 DB CRUD 및 서비스 계층 100% PASS 확인.
- `py -3 .agents/scripts/sync_doc_snapshots.py` 실행하여 스냅샷 SQLite 자동 기록.
- `py -3 .agents/scripts/verify_sync.py` 실행하여 대칭성 100% 확인.
