# [IMPLEMENTATION PLAN : Full 11-Node 25-Master Character Creation Algorithm]

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-ABYSS-004` |
| **문서 버전** | `v1.0.0 (Full 25-Master Pipeline Edition)` |
| **철학 및 원칙** | `Dify DSL 11개 노드 및 인간 2단계 결재선(HITL Checkpoint 1 & 2) 완전 구현` |
| **적용 표준** | `Clean 4-Tier Layered Architecture & 70-Step Gene Spec` |
| **상태** | `APPROVED (인간 승인 완료)` |

---

## 🏛️ 1. 전체 11단계 파이프라인 아키텍처

```text
[Node 1: User Concept Query]
        ↓
[Node 2: DB Hydration & Base Spec Read]
        ↓
[Node 3: CLASSIFIER & GENE SEED RESOLVER]
  - #NAME-70G-XXXX 시드 발급
  - Hard Invariants (Primary Boundary, Somatic Triggers) 선행 역산
  - 상호 직교하는 V1 (1안) vs V2 (2안) 도출
        ↓
[Node 4 & 5: HUMAN CHECKPOINT 1] (Web UI Modal 1)
  - 유저가 V1 1안 vs V2 2안 비교 검토 후 채택
        ↓
[Node 6 & 7: DUAL-MODE SPEC COMPILER]
  - 8-Tier Visual DNA & Illustrious-XL 6-Slot 단부루 태그
  - 17대 완전 범용 생체·의복 텐서 (Track 1)
  - 7대 차원축 70단계 인격 유전자 (Track 2)
  - Kinematic Chain 7단계 신체 운동 연쇄 파동 전이 매핑
        ↓
[Node 8 & 9: HUMAN CHECKPOINT 2] (Web UI Modal 2)
  - 컴파일된 Diff 요약 검토 후 유저가 [APPLY] 최종 인가
        ↓
[Node 10: 30,000-CHAR RECURSIVE MASTER SYNTHESIZER]
  - 무수치 순수 감각어 헌법 + 동적 완급조절 + 3계층 신경 원장 결합
  - 25,000자 ~ 30,000자급 마스터 시스템 지시사항 전문 합성
        ↓
[Node 11: STATIC LINTER & SQLITE WAL DB PERSISTENCE]
  - 플레이스홀더([TODO], [TBD]) 정적 린터 검증 후 DB 저장 ➔ 즉시 롤플레이 투입
```

---

## 📁 2. 컴포넌트별 구현/개정 파일 명세

1. **`src/domain/`**:
   - `personality_gene.py`: 17대 텐서 목록 및 70단계 마스터 인격 유전자 스키마 보강
2. **`src/infrastructure/`**:
   - `llm/prompt_synthesizer.py`: 30,000자급 초고밀도 마스터 지시사항 생성기 및 Dify 전수 프롬프트 이식
3. **`src/application/`**:
   - `classifier_service.py`: Dify Node 3 전수 프롬프트 및 정밀 직교 벡터 추출기
   - `spec_compiler_service.py` (`NEW`): Dify Node 7 8-Tier DNA & 17대 텐서 & 70단계 유전자 컴파일러
   - `master_synthesizer_service.py` (`NEW`): Dify Node 10 30,000자급 마스터 지시사항 합성기
   - `static_validator.py` (`NEW`): Dify Node 11 정적 플레이스홀더 정규식 검증기
4. **`src/presentation/web/`**:
   - `server.py`: Node 3 (`/api/characters/classify`), Node 7 (`/api/characters/compile-spec`), Node 10 (`/api/characters/synthesize-master`) 엔드포인트 연동
   - `static/js/views/vault.js` & `app.js`: Checkpoint 1 (V1/V2 선택) 및 Checkpoint 2 (Spec Diff 검토 및 APPLY) 2단계 결재선 완벽 연동
   - `templates/index.html`: Checkpoint 1 & 2 모달 UI 확장
5. **`tests/unit/`**:
   - `test_creation_pipeline.py`: Node 3부터 Node 11까지의 전 파이프라인 E2E 단위 테스트

---

## 🧪 3. 검증 계획
- `py -3 -m unittest discover -s tests/unit -v` 실행하여 전 파이프라인 100% PASS 확인.
- SQLite DB에 실제 25대 마스터 프롬프트 및 8-Tier DNA가 저장되는지 확인.
- 브라우저 UI에서 Checkpoint 1 ➔ Checkpoint 2 ➔ 발현 완결 인터랙션 검증.
