# [SOFTWARE REQUIREMENTS SPECIFICATION : SRS]
# 시스템 명칭: AbyssEmpire (Dark Fantasy Somatic RPG Engine)

| 메타데이터 항목 | 세부 내용 |
| :--- | :--- |
| **문서 표준** | `IEEE 830 / ISO/IEC/IEEE 29148 Software Requirements Specification` |
| **문서 ID** | `SRS-ABYSS-2026-v3.0` |
| **장르 & 세계관** | `다크 판타지 소마틱 롤플레잉 게임 (Dark Fantasy Somatic RPG)` |
| **대상자 관계 모델** | `Phase 1: 1:1 → Phase 2: 1:N → Phase 3: N:N 상호작용 확장` |
| **캐릭터 풀 규칙** | `플레이어(User)를 제외한 모든 등장인물은 여성형 캐릭터` |
| **핵심 생성 철학** | `비가역적 제약 조건 선행 역산 (NSFW 관능·서사 텐션 필수 결합)` |
| **엔진 아키텍처** | `Pure Native Python Core + Multi-LLM Probabilistic Hybrid Engine` |
| **최종 수정일** | `2026-09-02` |

---

## 1. 시스템 범위 및 핵심 아키텍처 비전 (Vision & Scope)

### 1.1 시스템 목적 (Purpose)
본 시스템은 깊은 어둠과 타락, 엄격한 규율과 본능이 교차하는 **다크 판타지 세계관**을 무대로 하는 **고밀도 롤플레잉 게임 엔진**이다.
- **다자간 확장성**: `1:1 (단일 캐릭터 심층 조교/서사)` ➔ `1:N (파티/하렘/파벌 대립)` ➔ `N:N (진영 간 자율 상호작용 및 난입)`으로 단계적 확장 가능한 아키텍처를 제공한다.
- **여성형 캐릭터 생태계**: 유저를 제외한 모든 등장인물은 고유한 가문, 결벽증, 신체적 결함, 트라우마를 가진 여성형 인격체로 구성된다.
- **Python + LLM 하이브리드**: 상태 보존, 스택 관리, 수학적 앵커링은 **Native Python**으로 철저히 통제하고, 문학적 긴장감과 관능적 대사/행동 묘사는 **LLM의 비결정론적 추론**에 위임한다.

---

## 2. 캐릭터 생성 메커니즘 (Constraint-First Reverse Engineering)

### 2.1 비가역적 제약 조건 선행 역산 (Hard Invariants First)
캐릭터 생성 시 이름이나 외모를 먼저 정하는 것이 아니라, **"캐릭터가 목숨보다 지키려는 불변의 제약선"**과 **"성적/신체적 파멸 트리거(NSFW Somatic Trigger)"**를 먼저 역산하여 불변값으로 못 박는다.

```text
[User Concept Input] 
        ↓
[Step 1. Hard Invariants & NSFW Somatic Trigger Resolution]
   - Primary Boundary (가문 순결 서약, 도덕적 결벽, 종교적 금기)
   - Ego Collapse Trigger (초커 강제 시선 고정, 체온 밀착, 갑주 해제 등)
   - Somatic Achilles Heel (쇄골 패임, 목덜미 척수, 늑골 압박 등)
        ↓
[Step 2. 8-Tier Visual DNA & 7-Axis Personality Compilation]
   - 제약선과 취약 부위를 감추기 위한 의복(초커/갑주/드레스), 신체 반응, 8중 외모 규격 역산
```

### 2.2 NSFW 관능 텐션의 문학적 승화 (Sensorial & Somatic Protocol)
- 저급한 직설적 슬랭을 배제하고, **계면 마찰, 나노 호흡 파열, 0.1초 신경 연쇄 반응, 쇄골 열감, 생체 림프 반응** 등 고밀도 생체역학적·문학적 개념어로 세이프티 필터를 100% 무결하게 통과하면서도 압도적인 관능적 쾌감과 서사적 긴장감을 극대화한다.

---

## 3. 다자간 상호작용 확장 모델 (Interaction Progression)

| 단계 (Phase) | 모델 (Topology) | 설명 및 인터랙션 범위 |
| :--- | :--- | :--- |
| **Phase 1 (기본)** | `1:1 Focused` | 플레이어와 단일 여성 캐릭터 간의 밀실/심층 심리 및 소마틱 서사 롤플레이 |
| **Phase 2 (확장)** | `1:N Multi-Party` | 플레이어 1인에 대해 2인 이상의 여성 캐릭터가 질투, 충성 경쟁, 협력 서사 전개 |
| **Phase 3 (완성)** | `N:N Living Abyss`| 플레이어가 개입하지 않아도 여성 캐릭터들 간의 파벌 대립, 관계 전이, 자율 상호작용 |

---

## 4. UI/UX 디자인 요구사항 (Web Studio App)

1. **다크 판타지 비주얼 무드**:
   - Deep Obsidian Black (`#090a10`), Royal Velvet Purple, Blood Rose Red 팔레트 적용.
   - 글래스모피즘(Glassmorphism) 및 부드러운 반응형 트랜지션.
2. **3대 핵심 뷰 체계**:
   - **Lobby Hub**: 활성 캐릭터 8-Tier Visual DNA 액자 및 전신 스테이터스 관측.
   - **Play Room**: 3-Tier 신경·메모리 원장 실시간 모니터링, 서사 극장, 전술 칩, 자연어 턴 입력.
   - **Character Studio & Vault**: RDB 캐릭터 보관소, Illustrious-XL 단부루 태그 복사, HITL 캐릭터 발현기.
3. **사용자 경험 극대화 (Zero-Friction UX)**:
   - 비동기 AJAX / 멀티스레드 서빙으로 타이핑 및 턴 실행 시 UI 프리징 완전 제거.
   - Undo(되돌리기), Reset, 마스터 헌법 원클릭 복사 지원.

---

## 5. 데이터 엔티티 및 스키마 규격

### 5.1 8-Tier Visual DNA Matrix (외모 표류 Zero Drift 보장)
- `face_geometry`: 턱선, 입술 색상, 코선
- `ocular_optics`: 홍채 색상, 동공 림, 속눈썹
- `hair_physics`: 모발 길이, 색상, 결, 잔머리 물리
- `body_silhouette`: 신장, 체형 실루엣, 쇄골/골격 돌출도
- `dermal_texture`: 피부 톤, 표피 질감, 핏줄 가시성
- `apparel_accents`: 메인 의복, 초커/리본/갑주/장신구
- `somatic_flush_cue`: 수치/체온 상승 시 쇄골·귓바퀴 홍조 경로
- `lighting_contrast`: 기본 광원 및 명암비

### 5.2 3-Tier Somatic Ledger (3계층 신경·메모리 원장)
- `Layer 1 (반사계)`: 밀리초 단위 척추/호흡/근육 방어 반사
- `Layer 2 (단기버퍼)`: 수 분간 유지되는 체온/압박/피부 잔향
- `Layer 3 (장기기억)`: 영구 각인되는 굴종/순종/애착 지수

---

## 6. 인수 조건 (Acceptance Criteria)

- [ ] **AC-01 (Constraint-First Integrity)**: 캐릭터 생성 시 제약 조건(Hard Invariants)과 NSFW 소마틱 트리거가 먼저 계산되지 않으면 생성이 진행되지 않아야 한다.
- [ ] **AC-02 (All-Female Cast Invariant)**: 플레이어를 제외한 모든 생성/등장 엔티티는 여성형 캐릭터 규격을 만족해야 한다.
- [ ] **AC-03 (Scalable Topology)**: 1:1 엔진 코어가 향후 1:N 및 N:N 상호작용으로 확장 가능한 상태 모델 구조를 갖추어야 한다.
- [ ] **AC-04 (Hybrid Execution)**: Native Python이 상태/되돌리기/DB를 100% 결정론적으로 통제하고, LLM이 문학적 텐션을 비결정론적으로 생산해야 한다.
