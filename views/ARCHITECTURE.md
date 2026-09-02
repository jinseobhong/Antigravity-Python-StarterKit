# 🏛️ ARCHITECTURE.md — AbyssEmpire 하이브리드 소매틱 시스템 아키텍처

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | VIEW-ARCH-001 |
| **아키텍처 패턴** | Clean Architecture 4-Tier Pattern |
| **최종 갱신일** | 2026-09-02 |

---

## 🧭 계층 구조 및 의존성 방향
`
[ Presentation (Web Studio / CLI) ]
             ↓
[ Application (NarrativeOrchestrator / CharacterWorkshop) ]
             ↓
[ Domain (Character, SomaticGene, TensionGrid, SceneState) ]
             ↑
[ Infrastructure (SQLite Persistence / LLM Cascade) ]
`
