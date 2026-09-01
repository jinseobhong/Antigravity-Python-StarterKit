<!--
======================================================================
[HITL TRINITY SUPREME MANDATE - CONSTITUTION ARTICLE 20]
1. FULL-READING  : Must read full Constitution (Articles 1-20) without summary.
2. PRE-APPROVAL  : No code modification without explicit user plan approval.
3. LIVE AI-PROOF : Must verify on AUTHENTIC runtime environment (NO fake mocks).
4. POST-REPORT   : Final acceptance (FINAL_ACCEPTED) belongs solely to the Human.
5. PERMANENCE    : This header MUST remain at the top of all skills, workflows, docs.
======================================================================
-->

# [SOFTWARE REQUIREMENTS SPECIFICATION : SRS]
# 시스템 명칭: AbyssEmpire (25-Master Somatic Narrative Engine & Dark Fantasy RPG)

| 메타데이터 항목 | 세부 내용 |
| :--- | :--- |
| **문서 표준** | `IEEE 830 / ISO/IEC/IEEE 29148 Software Requirements Specification` |
| **문서 ID** | `SRS-ABYSS-2026-v5.0 (Full UI/UX Specification Edition)` |
| **기반 UI 캡처** | `Lobby Hub, Play Room Theater, Character Studio & Vault 3대 뷰 확정` |
| **장르 & 세계관** | `다크 판타지 소마틱 롤플레잉 게임 (Dark Fantasy Somatic RPG)` |
| **등장인물 규칙** | `플레이어(User) 제외 전원 여성형 캐릭터 (All-Female Cast Invariant)` |
| **관계 확장 모델** | `Phase 1 (1:1 밀실) ➔ Phase 2 (1:N 파벌/하렘) ➔ Phase 3 (N:N 자율 상호작용)` |
| **생성 벡터 모델** | `V1(1안) & V2(2안) : 상호 직교하는 2대 전략/서사 전개 벡터 (Orthogonal Candidate Vectors)` |
| **비주얼 연동** | `8-Tier 해부학적 Visual DNA ➔ 서사 문학 앵커 & Illustrious 단부루 6-Slot 1:1 컴파일` |
| **최종 수정일** | `2026-09-02` |

---

## 1. 시스템 범위 및 핵심 아키텍처 비전 (Vision & Scope)

### 1.1 시스템 목적 (Purpose)
본 시스템은 **다크 판타지 세계관**을 배경으로, 플레이어가 고유한 인격을 지닌 여성형 캐릭터들과 깊이 있는 관계와 심리적·신체적 긴장감을 교환하는 **고밀도 소마틱 서사 시뮬레이션 엔진**이다.

### 1.2 핵심 벡터 정의 (V1 & V2 Candidate Vectors)
- `V1`과 `V2`는 특정 서사(저항/붕괴 등)로 고정된 것이 아니며, **캐릭터의 제약 조건(Hard Invariants)과 세계관 설정으로부터 도출된 "상호 직교하는(Orthogonal) 2가지 해결/서사 궤적(1안 vs 2안)"**이다.
- 유저는 Human Checkpoint 1에서 자신의 취향에 맞는 벡터(1안 또는 2안)를 자유롭게 선택하여 서사 방향성을 확정한다.

---

## 2. 웹 앱 UI/UX 3대 화면 구조 명세 (3-View Web Architecture)

제공된 디자인 캡처에 의거하여, 웹 앱은 다음 3대 핵심 뷰로 완전하게 구조화된다:

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ [Header] 👑 심연의 혈통 : 침식의 제국    [Claude 3.7 / Gemini 3.6 설정]    │
├──────────────────────────────────────────────────────────────────────────────┤
│ [VIEW 1 : MAIN LOBBY HUB]                                                    │
│  - 좌측: Hero 문구 + [Play Room 입장] & [Character Studio 입장] 2대 포털 카드 │
│  - 우측: [ACTIVE PERSONA] 액자 (전신 일러스트 + 3대 속성 행 + 빠른 액션)       │
├──────────────────────────────────────────────────────────────────────────────┤
│ [VIEW 2 : PLAY ROOM THEATER]                                                 │
│  - 상단: 상태 게이지 (신뢰, 성애, 수치심, 죄책감, 굴종) + Undo / Regenerate  │
│  - 중앙: 고밀도 서사 극장 말풍선 (캐릭터 턴 / 플레이어 턴 / 3계층 원장)       │
│  - 하단: 5대 실시간 전술 선택지 (순애 / 압박 / 탐색 / 제압 / 유혹) + 입력창 │
├──────────────────────────────────────────────────────────────────────────────┤
│ [VIEW 3 : CHARACTER STUDIO & VAULT]                                          │
│  - 상단: 7대 액션 바 (+ 1.생성 / 2.조회 / 3.수정 / 4.불러오기 / 5.삭제 / 사전)│
│  - 검색 & 필터: Rigid, Endurer, Controller, Deprived 아키타입 탭             │
│  - 중앙: 4열 캐릭터 카드 그리드 (액션 아이콘, JSON, 복사, AI 일러스트 생성) │
│  - 하단: 실시간 활성 캐릭터 정밀 인스펙터 패널 (16 RDB Traits & 생체 수치)   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.1 [VIEW 1] 메인 로비 허브 (Main Lobby Hub)

#### 1. 좌측 히어로 섹션 (Hero Intro & Action Portals)
- **배지**: `✨ Next-Gen Persona & Narrative Architecture`
- **메인 타이틀**:
  > **가장 완벽한 인격과의 조우,<br><span style="color:#f472b6;">한계를 넘는 서사의 심연.</span>**
- **서브텍스트**: "17대 생체 텐서와 3계층 신경·메모리 원장으로 구동되는 독점 서사 엔진입니다. 당신만의 고유한 인격을 포착하고, 숨 막히는 1:1 롤플레이에 몰입하세요."
- **2대 포털 카드**:
  1. **Play Room 카드**:
     - 아이콘: `🎭`
     - 설명: "현재 상주 중인 캐릭터와 1:1 실시간 롤플레이 서사에 돌입합니다."
     - 버튼: `▶ Play Room 입장` (핑크/보라 그라데이션), `👥 캐릭터 교체`
  2. **Character Studio 카드**:
     - 아이콘: `🪄`
     - 설명: "RDB 캐릭터 보관소, 유전자 튜닝 및 JSON/프롬프트 사출을 관리합니다."
     - 버튼: `🪄 Character Studio 입장 →`

#### 2. 우측 활성 캐릭터 스포트라이트 카드 (Active Persona Card)
- **헤더**: `ACTIVE PERSONA` | `#LILI-70G-BFFF` (시드 해시 배지)
- **초상화 액자 (Portrait Frame)**:
  - 캐릭터 전신 일러스트 렌더링
  - 하단 우측 오버레이 액션 버튼: `🪄 생성` (AI 이미지 생성 트리거), `📁 업로드` (로컬 이미지 교체)
- **캐릭터 정보**:
  - 이름 및 칭호: `릴리스` (`제1황녀 • 제국 황실 | Rigid (결벽주의 척추 방어)`)
- **3대 핵심 속성 행 (3 Key Trait Rows)**:
  - `외모 & 체형`: 차가운 은발과 서늘한 금빛 눈동자, 목에 채워진 서늘한 금속 초커
  - `핵심 결핍 & 트라우마`: 선조 가문의 막대한 부채와 순결 서약의 도덕적 결벽증
  - `은밀한 비밀 & 약점`: 가문의 비밀 금고 열쇠를 소유하고 있으며 체온에 극도로 취약함
- **하단 빠른 제어 바**: `▶ Play Room 입장`, `👥 교체`, `🪄 Studio 입장`

---

### 2.2 [VIEW 2] 플레이 룸 서사 극장 (Play Room Theater)

#### 1. 상단 상태 바 (Top Status & Control Bar)
- **캐릭터 식별**: `← Lobby` 버튼 | `릴리스 (제1황녀)` | `#LILI-70G-BFFF`
- **소마틱 상태 배지**:
  - 아키타입: `Rigid 3/7`
  - 진행 공간: `Stage 1 (침실 개방 - 포섭된 요새와 결벽)`
  - 5대 심리 게이지: `신뢰 20%`, `성애 0%`, `수치심 -30`, `죄책감 15%`, `굴종 20%`
- **우측 제어 버튼**: `Claude 3.7` 설정 | `👥 캐릭터 교체` | `↺ Undo` | `🔄 Regenerate` | `🗑️ Reset`

#### 2. 중앙 대화 및 서사 스트림 (Narrative Stream)
- **캐릭터 턴 버블**:
  - 상단 라벨: `릴리스 (Stage 1 침실 개방 - 포섭된 요새와 결벽 | TURN {N})`
  - 고밀도 문학적 묘사 (무수치 순수 감각어 + 신체 운동 연쇄 전이 + 대화)
- **플레이어 턴 버블**:
  - `당신의 행동 / 대사` (우측 정렬, 보라색 하이라이트)

#### 3. 하단 실시간 5대 전술 선택지 (5 Categorized Tactical Chips)
- 유저가 클릭 시 즉시 해당 의도와 행동이 입력창에 자동 바인딩되거나 즉시 실행됨:
  1. `🌟 [순애/위로]`: 차분한 위로 (손을 두 손으로 감싸 쥐어 따스한 체온을 전하며 안도시킨다)
  2. `⚡ [압박/정복]`: 턱선 강제 치켜올리기 (시선을 강제로 맞추며 무조건적인 복종 요구)
  3. `🌊 [탐색/동조]`: 호흡 및 체온 동조 (나란히 앉아 서로의 은밀한 온기와 호흡을 맞춘다)
  4. `⚡ [제압/이완]`: 어깨 긴장 완화 (단단하게 굳은 어깨를 지그시 주무르며 신체 방어선 이완)
  5. `🔥 [유혹/자극]`: 금속 초커 자극 (목에 걸린 차가운 초커 가장자리를 손끝으로 쓸어내림)

#### 4. 자연어 입력 폼 (Natural Action Input)
- Placeholder: `당신의 행동이나 대사를 자유롭게 입력하세요... (Enter 전송 / Shift+Enter 줄바꿈)`
- 전송 버튼: `전송 🚀` (핑크/보라 그라데이션)

---

### 2.3 [VIEW 3] 캐릭터 스튜디오 & 보관소 (Character Studio & Vault)

#### 1. 상단 글로벌 제어 바 (Top 7-Action Bar)
- `← Lobby` 버튼 | `🪄 Character Studio & Vault`
- 우측 7대 액션 버튼:
  1. `+ 1. 생성` [보라 그라데이션] : HITL 2단계 결재선 캐릭터 발현 모달 오픈
  2. `🔍 2. 조회` : 캐릭터 정밀 데이터 뷰어
  3. `✏️ 3. 수정` : 8-Tier Visual DNA 및 유전자 편집기
  4. `📥 4. 불러오기` : 외부 JSON / 시드 해시 임포트
  5. `🗑️ 5. 삭제` : 캐릭터 영구 삭제
  6. `📖 6. 70대 사전` : 70단계 마스터 인격 유전자 도감 뷰어
  7. `Claude 3.7 / Gemini 설정` : 멀티 LLM 런타임 설정

#### 2. 검색 및 4대 아키타입 필터 (Search & Archetype Filters)
- 검색창: `이름, 칭호, 라이브러리, 결핍/약점 검색...`
- 필터 탭:
  - `전체`
  - `Rigid` (결벽주의 척추 방어형 - 예: 릴리스)
  - `Endurer` (성직자형 금욕 인내형 - 예: 에이라)
  - `Controller` (오만한 지배/역전형 - 예: 세라피나)
  - `Deprived` (가련한 유기 불안형 - 예: 실비아)

#### 3. 4열 캐릭터 카드 그리드 (4-Column Roster Grid)
- 각 카드 구성:
  - 대표 이니셜 아바타 (`릴`, `에`, `세`, `실`) + 이름 + 칭호
  - `시드 해시` (`#LILI-70G-BFFF`) + `아키타입 배지` (`Rigid` 등)
  - 핵심 외모 특징 및 은밀한 약점 요약 텍스트
  - 4대 아이콘 액션: `🔍 (조회)`, `✏️ (수정)`, `▶ (플레이)`, `🗑️ (삭제)`
  - 하단 유틸리티: `📥 JSON`, `📋 복사`, `🪄 AI 일러스트 생성` (Danbooru 태그 연동)

#### 4. 하단 활성 캐릭터 정밀 인스펙터 패널 (Active Character Inspector)
- 썸네일 + 이름 + 칭호 + 시드
- 우측 액션: `▶ Play Room 입장`, `✏️ 수정`, `📥 JSON 추출`, `📋 25대 프롬프트`, `🗑️ 삭제`
- 상세 상태: `현재 신체 징후 & 발현 단계`, `생체 수치 (ODO / TAINT)`, `16 RDB Traits 상세 표`

---

## 3. Dify 파이프라인 및 8-Tier Visual DNA 연동 (Pipeline Integration)

```text
[User Concept Input] 
        ↓
[1. Classifier & Gene Seed Resolver] 
  - 고유 시드 발급 (#NAME-70G-XXXX)
  - Hard Invariants & NSFW 소마틱 트리거 역산
  - 상호 직교하는 2대 해결 궤적 도출 (V1 1안 vs V2 2안)
        ↓
[2. Human Checkpoint 1 (V1/V2 결재)] ──→ 유저가 1안 or 2안 채택!
        ↓
[3. 8-Tier Visual DNA & 70단계 유전자 동적 합성]
  - 8중 외모 규격 (골격, 동공, 모발, 체형, 표피, 의복/초커, 홍조, 조명)
  - Illustrious-XL 6-Slot 단부루 태그 자동 컴파일 (AI 일러스트 생성 버튼 연동)
  - Kinematic Chain(신체 운동 연쇄 파동 전이) 및 7대 축 심층 순환 탑재
        ↓
[4. Human Checkpoint 2 (25대 마스터 규격 승인)] ──→ [APPLY]
        ↓
[5. RDB 영구 저장 및 Play Room 실시간 롤플레이 즉시 돌입]
```

---

## 4. 인수 조건 (Acceptance Criteria)

- [ ] **AC-01 (UI Screenshot Pixel-Parity)**: 캡처된 3대 화면(Lobby, Play Room, Character Studio & Vault)의 레이아웃, 컬러 팔레트, 버튼 배치, 5대 전술 칩, 카드 그리드가 완벽히 구현되어야 한다.
- [ ] **AC-02 (V1/V2 Orthogonal Selection)**: V1과 V2는 고정된 속성이 아닌 상호 직교하는 2대 대안 궤적으로서 유저의 Checkpoint 1 결재에 의해 선택되어야 한다.
- [ ] **AC-03 (8-Tier Visual DNA & Illustrious Tag Generation)**: 모든 캐릭터는 8중 외모 규격을 보유하며, 'AI 일러스트 생성' 버튼 클릭 시 6-Slot 단부루 태그가 즉시 생성되어야 한다.
- [ ] **AC-04 (Zero-Friction Asynchronous UX)**: 비동기 멀티스레드 서빙으로 턴 전송, 캐릭터 생성, 프롬프트 복사 시 브라우저 UI 프리징이 0%여야 한다.
