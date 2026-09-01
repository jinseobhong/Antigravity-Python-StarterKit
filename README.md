# AbyssEmpire-python-narrative

> **Antigravity 고신뢰도 AI 아키텍트 거버넌스 및 `views/` 5대 핵심 뷰 적용 프로젝트**

---

## 🏛️ `views/` 5대 실시간 관측 뷰 (The 5 Core Live Views)

본 프로젝트는 Antigravity 에이전트와 완벽한 실시간 싱크를 유지하기 위해 `views/` 디렉토리에 다음 5대 실시간 뷰를 운용합니다:

1. **[views/CURRENT_STATE.md](./views/CURRENT_STATE.md)**: 실시간 당면 과제, 현재 페이즈 및 5단계 파이프라인 좌표 (SSOT)
2. **[views/IMPLEMENTATION_STATUS.md](./views/IMPLEMENTATION_STATUS.md)**: 전체 시스템 컴포넌트 완성도 현황판 (`TODO` / `WIP` / `DONE`)
3. **[views/IMPLEMENTATION_PLAN.md](./views/IMPLEMENTATION_PLAN.md)**: 현재 작업 세부 계획서 (세션 브레인 실시간 미러링)
4. **[views/WALKTHROUGH.md](./views/WALKTHROUGH.md)**: 작업 구현 완료 및 AI 실측 검증 보고서 (세션 브레인 실시간 미러링)
5. **[views/ARCHITECTURE.md](./views/ARCHITECTURE.md)**: 3계층 아키텍처 및 시스템 전체 설계 청사진

---

## 🌟 중앙 거버넌스 허브 (.agents/)

본 프로젝트의 `.agents/` 디렉토리는 [Antigravity-Common-Core](https://github.com/jinseobhong/Antigravity-Common-Core) 중앙 저장소와 **Git Submodule**로 연결되어 있습니다:

- **[CONVENTIONS.md](./.agents/CONVENTIONS.md)**: 파일 시스템 구조 및 명명 규칙 공식 명세
- **[workflows/workflow.md](./.agents/workflows/workflow.md)**: 2-Phase 페어링 및 입증 책임 강제 워크플로우
- **[skills/workflow/SKILL.md](./.agents/skills/workflow/SKILL.md)**: 개발 작업 자동 활성화 실행 런북
- **[docs/templates/](./.agents/docs/templates/)**: 5대 표준 문서 템플릿 모음
- **[store/schema.sql](./.agents/store/schema.sql)**: SQLite 데이터베이스 영구 로깅 스키마
- **[GEMINI.md.example](./.agents/GEMINI.md.example)**: 전역 최고 헌법 규격서 예시 (v2.0)