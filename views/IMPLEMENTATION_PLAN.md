# IMPLEMENTATION_PLAN.md — 공식 문서 스타일 가이드(STYLE_GUIDE.md) 제정 및 템플릿 표준화

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-STYLE-001` |
| **문서 버전** | `v1.0.0` |
| **작성 일자** | `2026-09-02` |
| **상태** | `APPROVED (사용자 사전 승인 완료)` |
| **작성자 / 승인자** | `AI Architect` / `Human Lead` |

---

## 📁 1. 변경 대상 파일 목록 (File Scope)

| 변경 구분 | 대상 파일 경로 | 변경 목적 및 구현 내용 |
| :---: | :--- | :--- |
| `[NEW]` | `.agents/docs/STYLE_GUIDE.md` | 공식 문서 작성 스타일 가이드 (RFC 2119, 메타데이터, 문체) |
| `[MODIFY]` | `.agents/CONVENTIONS.md` | `STYLE_GUIDE.md` 준수 강제 조항 추가 |
| `[MODIFY]` | `.agents/docs/templates/*.template.md` | 5대 표준 템플릿에 공식 메타데이터 헤더 및 엔지니어링 문체 반영 |
| `[MODIFY]` | `views/IMPLEMENTATION_STATUS.md` | 해당 작업 [WIP] 등록 |
| `[MODIFY]` | `views/CURRENT_STATE.md` | 진행 좌표 및 상태 동기화 |

---

## 🛠️ 2. 단계별 구현 순서 (Execution Steps)

1. **[1단계: STYLE_GUIDE.md 제정]**: RFC 2119 용어, 메타데이터 헤더, 문체 규격 명시.
2. **[2단계: CONVENTIONS.md 연동]**: 문서 작성 시 스타일 가이드 준수 강제 조항 추가.
3. **[3단계: 표준 템플릿 5종 전면 개편]**: 메타데이터 헤더 및 엄격한 기술 문체 적용.
4. **[4단계: 실측 검증 및 동기화]**: Git 커밋/푸시 및 `views/WALKTHROUGH.md` 제출.

---

## 🧪 3. 검증 계획 (Verification Plan)
- **명령어**: `git status` 및 템플릿 문법 검사
- **기준**: Working Tree Clean & 5대 템플릿 100% 규격 일치
