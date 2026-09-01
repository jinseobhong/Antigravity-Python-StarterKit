# IMPLEMENTATION_PLAN.md — AbyssEngine 캐릭터 공방 및 Illustrious-XL 태그 컴파일러 복구

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-WORKSHOP-001` |
| **문서 버전** | `v1.0.0` |
| **작성 일자** | `2026-09-02` |
| **상태** | `APPROVED (사용자 사전 승인 완료)` |
| **작성자 / 승인자** | `AI Architect` / `Human Lead` |

---

## 📁 1. 변경 대상 파일 목록 (File Scope)

| 변경 구분 | 대상 파일 경로 | 변경 목적 및 구현 내용 |
| :---: | :--- | :--- |
| `[NEW]` | `src/infrastructure/media/danbooru_prompt_builder.py` | Illustrious-XL 6-Slot 단부루 태그 컴파일러 (ApexFlux/URL생성 제외) |
| `[NEW]` | `src/application/character_workshop_service.py` | 4대 기본 아키타입 시딩, 마스터 시스템 프롬프트 컴파일러, JSON I/O |
| `[NEW]` | `tests/unit/infrastructure/test_danbooru_prompt_builder.py` | 단부루 6-Slot 태그 조립 단위 테스트 |
| `[NEW]` | `tests/unit/application/test_character_workshop_service.py` | 4대 로스터 시딩, 마스터 프롬프트 및 JSON I/O 단위 테스트 |
| `[MODIFY]` | `views/IMPLEMENTATION_STATUS.md` | 현황 갱신 |
| `[MODIFY]` | `views/CURRENT_STATE.md` | 진행 좌표 및 상태 동기화 |

---

## 🛠️ 2. 단계별 구현 순서 (Execution Steps)

1. **[1단계: danbooru_prompt_builder.py 구현]**:
   - 6-Slot (Quality ➔ Framing ➔ Genetics/NSFW ➔ Armor ➔ Shader ➔ Atmosphere) 단부루 긍정/부정 태그 컴파일러 구현.
2. **[2단계: character_workshop_service.py 구현]**:
   - 4대 대표 아키타입(`릴리스`, `에이라`, `세라피나`, `실비아`) 자동 시딩, `export_master_prompt`, `export_json`, `import_json`.
3. **[3단계: 단위 테스트 작성 및 실측 실행 (AI Proof)]**:
   - `tests/unit/` 전체 테스트 스위트 실행 및 25+개 테스트 100% Pass 확인.
4. **[4단계: 상태 갱신 및 Git 자동 동기화]**:
   - `log_task.py` 적재, `views/WALKTHROUGH.md` 제출 및 `auto_push.py`로 GitHub 배포.

---

## 🧪 3. 검증 계획 (Verification Plan)
- **명령어**: `py -3 -m unittest discover -s tests/unit -v`
- **기준**: 전체 단위 테스트 100% Pass (0 errors) & 입증 등급 `PROVEN`
