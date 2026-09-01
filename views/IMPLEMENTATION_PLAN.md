# IMPLEMENTATION_PLAN.md — 새로운 LLM 하이브리드 서사 엔진 전면 구축

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-ABYSS-002` |
| **문서 버전** | `v2.0.0` |
| **작성 일자** | `2026-09-02` |
| **상태** | `APPROVED (사용자 승인 완료)` |
| **작성자 / 승인자** | `AI Architect` / `Human Lead` |

---

## 📁 1. 구축 대상 파일 목록 (File Scope)

### 🧬 [Phase 1] 도메인 계층 (`src/domain/`)
- `[NEW]` `src/domain/gene_seed.py`: 고유 시드 해시(`#NAME-70G-XXXX`) 및 엔트로피 모델
- `[NEW]` `src/domain/visual_dna.py`: 8-Tier 해부학적 외모 규격 모델 (골격, 동공, 모발, 체형, 표피, 의복/초커, 생체홍조, 조명)
- `[NEW]` `src/domain/personality_gene.py`: 7대 차원축 70단계 유전자 & 제약선(Hard Invariants) 모델
- `[NEW]` `src/domain/somatic_ledger.py`: 3계층 신경·메모리 원장 (`Layer 1: 반사`, `Layer 2: 단기버퍼`, `Layer 3: 장기기억`)
- `[NEW]` `src/domain/spatial_pressure.py`: 3-Layer 공간 압력 챔버 (`Layer 0`, `Layer 1`, `Layer 2`)
- `[NEW]` `src/domain/kinematic_chain.py`: 7단계 신체 운동 연쇄 파동 전이 엔진

### 🔌 [Phase 2] 인프라 계층 (`src/infrastructure/`)
- `[NEW]` `src/infrastructure/llm/client.py`: Gemini / Claude 멀티 LLM 클라이언트 (캐스케이드 & 온도 튜닝)
- `[NEW]` `src/infrastructure/llm/prompt_synthesizer.py`: 30,000자급 마스터 헌법 & 턴별 서사 프롬프트 조립기
- `[NEW]` `src/infrastructure/media/visual_compiler.py`: 서사용 문학적 앵커 & Illustrious-XL 6-Slot 단부루 태그 컴파일러
- `[NEW]` `src/infrastructure/database/db_manager.py`: SQLite 트랜잭션 관리자
- `[NEW]` `src/infrastructure/database/repositories.py`: Character, Gene Seed, Turn Ledger 리포지토리

### 🧠 [Phase 3] 유스케이스 및 애플리케이션 계층 (`src/application/`)
- `[NEW]` `src/application/classifier_service.py`: 제약선 역산 및 2대 서사 충돌 궤적(`V1` vs `V2`) 분류기
- `[NEW]` `src/application/gene_synthesis_service.py`: 8-Tier 외모 + 70단계 유전자 동적 합성기
- `[NEW]` `src/application/narrative_orchestrator.py`: 실시간 서사 롤플레이 턴 오케스트레이터
- `[NEW]` `src/application/undo_manager.py`: 불변 롤백 스택 관리자

### 🌐 [Phase 4] 프레젠테이션 & 웹 스튜디오 (`src/presentation/` & `app.py`)
- `[NEW]` `src/presentation/cli.py`: HITL 결재선(Checkpoint 1 & 2) 내장 터미널 롤플레이
- `[NEW]` `src/presentation/web/server.py`: 모듈화 웹 서버 & 4계층 REST API
- `[NEW]` `src/presentation/web/templates/index.html`: 8-Tier Visual DNA 뷰어 & Play Room 통합 웹 뷰
- `[NEW]` `src/presentation/web/static/css/style.css`: 스타일시트
- `[NEW]` `src/presentation/web/static/js/`: 모듈화된 프론트엔드 스크립트 모음
- `[NEW]` `app.py`: 최상위 원클릭 런처

### 🧪 [Phase 5] 단위 및 통합 테스트 스위트 (`tests/unit/`)
- `[NEW]` `tests/unit/domain/`: 도메인 엔티티 및 모델 무결성 단위 테스트
- `[NEW]` `tests/unit/infrastructure/`: 프롬프트 빌더, 단부루 태그 컴파일러, DB 단위 테스트
- `[NEW]` `tests/unit/application/`: 제약선 분류, 유전자 합성, 오케스트레이터 단위 테스트
- `[NEW]` `tests/unit/presentation/`: CLI 및 웹 서버 단위 테스트

---

## 🧪 2. 검증 계획 (Verification Plan)
- **명령어**: `py -3 -m unittest discover -s tests/unit -v`
- **기준**: 전체 단위 테스트 100% Pass (0 error, 0 failure) & 입증 등급 `PROVEN`
