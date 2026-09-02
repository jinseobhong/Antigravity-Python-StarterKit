# 🚀 Antigravity AI Pair Engineering Master Starter Kit
> **1인 개발자를 위한 초생산성 AI 거버넌스 운영체제 & 플러그앤플레이 템플릿**

| 항목 | 내용 |
| :--- | :--- |
| **템플릿 ID** | `ANTIGRAVITY-STARTER-KIT-v1.0` |
| **핵심 목적** | 1인 개발 + AI 페어 프로그래밍 환경에서 100% 결함 없는 고신뢰성 소프트웨어 고속 개발 |
| **지원 아키텍처** | `Clean Architecture 4-Tier Pattern` + `Deterministic AI Constitution` |
| **최종 갱신일** | `2026-09-02` |

---

## 📌 1. 이 템플릿의 가치와 역할

본 저장소는 새로운 제품(웹, 모바일, 게임, SaaS, AI 파이프라인 등)을 만들 때 **`.agents/` 폴더와 거버넌스 헌법을 그대로 이식(Drop-in)하여 사용할 수 있는 마스터 스타터 킷**입니다.

### 🌟 4대 핵심 역량
1. **🔴 최고 헌법 거버넌스 (`GEMINI.md`)**: 무단 코드 수정 방지, 사전 승인 게이트, 터미널 실측 AI Proof 의무화.
2. **🏛️ 7대 전문 규격서 (`.agents/CONVENTIONS.md`)**: 코딩 표준, 문서 서식, 대화 톤앤매너, 3계층 시스템 영향도 분석, Git 형상 관리.
3. **🚀 원클릭 전사 무결성 검증기 (`run_checks.py`)**: 0.4초 만에 단위 테스트 + E2E + 뷰 대칭성 + 12대 문서 DB 스냅샷 완결.
4. **👁️ 5대 실시간 관측 창구 (`views/`)**: 프로젝트의 현재 상태(SSOT)를 인간과 AI가 완벽히 동기화.

---

## 🛠️ 2. 빠른 시작 (Quick Start)

### 1단계: 의존성 설치
```powershell
py -3 -m pip install -r requirements.txt
```

### 2단계: 전사 무결성 검증 실행
```powershell
py -3 .agents/scripts/run_checks.py
```

### 3단계: SQLite 거버넌스 감사 저장소 상태 확인
```powershell
py -3 .agents/scripts/log_task.py --status
```

---

## 🧭 3. 디렉터리 구조

```text
├── 🔴 GEMINI.md                    # 전역 최고 거버넌스 헌법 (Immutable Core)
├── 👁️ views/                       # 5대 실시간 프로젝트 관측 뷰 (SSOT)
│   ├── CURRENT_STATE.md            # 현재 진행 페이즈 및 당면 과제
│   ├── IMPLEMENTATION_STATUS.md    # 컴포넌트별 4단 상태 마커
│   ├── IMPLEMENTATION_PLAN.md      # 기능 구현 계획서
│   ├── WALKTHROUGH.md              # 작업 완료 보고 및 AI Proof
│   └── ARCHITECTURE.md             # 시스템 아키텍처 명세
├── 📁 src/                         # Clean Architecture 4계층 소스 코드
│   ├── domain/                     # 순수 불변 비즈니스 엔티티 (의존성 0%)
│   ├── infrastructure/             # SQLite WAL 저장소 및 리포지토리 어댑터
│   ├── application/                # 유스케이스 및 서비스 오케스트레이션
│   └── presentation/               # API 및 CLI 인터페이스
├── 🧪 tests/                       # 자동화 테스트 슈트
│   ├── unit/                       # 단위 테스트 (AAA 패턴)
│   └── e2e/                        # 종단간 격리 시나리오 테스트
└── 🏛️ .agents/                     # AI 페어 엔지니어링 마스터 거버넌스 코어
```
