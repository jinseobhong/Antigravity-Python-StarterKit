# [SOFTWARE REQUIREMENTS SPECIFICATION : SRS]
# 시스템 명칭: AbyssEmpire (25-Master Somatic Narrative Engine & Dark Fantasy RPG)

| 메타데이터 항목 | 세부 내용 |
| :--- | :--- |
| **문서 표준** | `IEEE 830 / ISO/IEC/IEEE 29148 Software Requirements Specification` |
| **문서 ID** | `SRS-ABYSS-2026-v4.0 (Enterprise Dify Pipeline Edition)` |
| **기반 DSL 규격** | `다중 에이전트 25대 마스터 서사 엔진 & 시드 시스템 (v0.7.0)` |
| **장르 & 세계관** | `다크 판타지 소마틱 롤플레잉 게임 (Dark Fantasy Somatic RPG)` |
| **등장인물 규칙** | `플레이어(User) 제외 전원 여성형 캐릭터 (All-Female Cast Invariant)` |
| **관계 확장 모델** | `Phase 1 (1:1 밀실) ➔ Phase 2 (1:N 파벌/하렘) ➔ Phase 3 (N:N 자율 상호작용)` |
| **핵심 생성 철학** | `제약 조건 및 NSFW 소마틱 트리거 비가역적 선행 역산 (Constraint-First)` |
| **비주얼 연동** | `8-Tier 해부학적 Visual DNA ➔ 서사 문학 앵커 & Illustrious 단부루 6-Slot 1:1 컴파일` |
| **최종 수정일** | `2026-09-02` |

---

## 1. Dify 파이프라인 전수 분석 및 요구사항 매핑 (Pipeline Extraction)

사용자의 Dify 마스터 DSL 파이프라인(`app.kind == 'app'`)으로부터 추출된 11단계 핵심 엔지니어링 프로세스 규격은 다음과 같다:

```text
[Node 1: Start] ──→ [Node 2: DB Hydration]
                          ↓
[Node 3: CLASSIFIER & GENE SEED RESOLVER] (LLM 추론)
  - 입력 분류: GENERAL_SPEC vs ROLEPLAY_INTERACTION
  - 고유 시드 발급: #NAME-70G-XXXX (시드 입력 시 100% 계승)
  - 불변 제약선(Hard Invariants) 및 2대 충돌 궤적(V1 vs V2) 역산
  - 원초적 어휘 승화 필터 (NSFW ➔ 소마틱 신체 결합/피부 밀착 개념어)
                          ↓
[Node 4: View Renderer] ──→ [Node 5: HUMAN CHECKPOINT 1 (V1/V2 결재창)]
                                  ↓ (V1 채택 or V2 채택)
[Node 6: Vector Selector] ──→ [Node 7: DUAL-MODE SPEC COMPILER] (LLM 추론)
  - 8-Tier Visual DNA & 17대 생체·의복 텐서 매핑
  - 70단계 인격 유전자 & Kinematic Chain 신체 운동 연쇄 파동 전이
  - 2~3개 동적 스포트라이트 & 턴 진행별 심층 유전자 순환
                          ↓
[Node 8: Spec Linter] ──→ [Node 9: HUMAN CHECKPOINT 2 (25대 마스터 결재창)]
                                  ↓ (APPLY 승인)
[Node 10: 30,000자 MASTER SYNTHESIZER] (LLM 추론)
  - 무수치 순수 감각어 헌법 (N, bpm 배제 ➔ 살결의 냉기, 호흡 승강)
  - 동적 가변 완급 조절 엔진 (Level 1: 2~4문단 / Level 2: 5~8문단 / Level 3: 10~15+문단)
  - 3계층 신경·메모리 원장 (Layer 1 반사 / Layer 2 단기버퍼 / Layer 3 장기기억)
                          ↓
[Node 11: Static Validator & SQLite/Supabase Save]
```

---

## 2. 8-Tier Visual DNA & 유전자 합성 인과 메커니즘 (Visual-Gene Synthesis)

### 2.1 인과 역산 원칙 (Causal Invariant Chain)
외모는 단순한 장식이 아니라, **"캐릭터가 목숨보다 지키려는 불변의 제약선(트라우마/결벽증/순결 서약)"**과 **"NSFW 신체 취약 부위"**를 감추고 방어하기 위해 형성된 생체적/의복적 필연성으로 도출된다.

```text
[Hard Invariants : 가문 부채 & 순결 서약 & 초커 접촉 취약]
        ↓
[8-Tier Visual DNA 인과 역산]
  ├── 1. face_geometry      : 결벽증을 방어하기 위한 날렵한 V-line 턱선과 굳게 다문 창백한 입술
  ├── 2. ocular_optics      : 상대를 위압하며 동요를 숨기는 금빛 홍채와 짙은 호박색 림
  ├── 3. hair_physics       : 엄격한 규율의 백은색 긴 생머리, 뺨을 타고 흐르는 단정한 옆머리
  ├── 4. body_silhouette    : 꼿꼿한 귀족적 척추와 도드라진 쇄골 패임 (168cm 호리호리한 체형)
  ├── 5. dermal_texture     : 햇빛을 보지 않은 창백한 백옥 피부와 목덜미의 푸른 핏줄
  ├── 6. apparel_accents    : 제약선을 상징하는 은색 금속 초커와 어깨가 드러난 검은 실크 드레스
  ├── 7. somatic_flush_cue  : 쾌락/수치 굴복 시 쇄골 패임과 귓바퀴를 타고 번지는 붉은 열감
  └── 8. lighting_contrast  : 차가운 달빛과 어두운 밀실의 짙은 명암 대비
        ↓
[Illustrious-XL 6-Slot 단부루 태그 & 서사 앵커 동시 컴파일]
  - Slot 1: Master Quality Tags (masterpiece, best quality, ultra-detailed)
  - Slot 2: Character Name & Base Pose (lilith, solo, 1girl, standing)
  - Slot 3: Hair & Eyes (silver_hair, straight_hair, golden_eyes, amber_eyes)
  - Slot 4: Apparel & Choker (black_dress, off-shoulder, silver_choker, ribbon)
  - Slot 5: Somatic & Sensorial Cues (collarbone, pale_skin, blushing, trembling)
  - Slot 6: Lighting & Atmosphere (dark_fantasy, moonlight, dramatic_shadow)
```

---

## 3. 핵심 서사 엔진 5대 절대 헌법 (Narrative Core Invariants)

### 3.1 헌법 1: 상태값 무(無)수치 순수 감각어 헌법 (Zero-Unit Sensory Law)
- 원장과 서사 본문에서 `2.0N`, `80bpm`, `38.4°C`, `1:3.5` 같은 기계적 아라비아 숫자나 물리 단위를 100% 영구 배제한다.
- 모든 상태는 **'살결의 서늘한 냉기'**, **'가라앉은 흉곽의 미세한 승강'**, **'목덜미를 옥죄는 초커의 금속성 압박감'**, **'오만하게 가늘어진 동공의 떨림'** 등 100% 현상학적 생체 감각어와 심리 문학으로 기록한다.

### 3.2 헌법 2: 신체 운동 연쇄 전이 (Kinematic Chain Wave Law)
- 신체 자극과 접촉 반응이 특정 부위(얼굴/입술)에 고정되지 않고 파동처럼 전이되어야 한다:
  $$\text{시선} \longrightarrow \text{성대/호흡} \longrightarrow \text{흉곽/심박} \longrightarrow \text{부속기관(꼬리/날개/뿔)} \longrightarrow \text{의복 장력} \longrightarrow \text{손끝 악력} \longrightarrow \text{족부 접지력}$$
- 매 턴마다 2~3개의 새로운 접촉 텐서만 동적으로 점등(Spotlight On)하고, 직전 턴의 텐서는 쿨다운(Spotlight Off)한다.

### 3.3 헌법 3: 7대 차원축 심층 순환 (Deep Gene Cycler)
- 턴이 누적될수록 캐릭터의 반응은 단순한 물리 반사에서 심연으로 깊숙이 파고든다:
  $$\text{축 I (물리적 기질 반사)} \longrightarrow \text{축 III (과거 사회적 결핍)} \longrightarrow \text{축 IV (인지 왜곡)} \longrightarrow \text{축 V (그림자 에고 붕괴)} \longrightarrow \text{축 VI (연금술적 척수 굴종)}$$

### 3.4 헌법 4: 3-Layer 공간 압력 챔버 (Spatial Pressure Progression)
- **Layer 0 (공적 공간)**: 사회적 가면, 완벽한 예의와 방어선 유지, 일상적 대화.
- **Layer 1 (경계 공간)**: 시선 집중, 1:1 대면, 신체적 거리 좁힘, 미세한 호흡 교란.
- **Layer 2 (사적 밀실)**: 닫힌 문, 신체 밀착 허용, 에고 붕괴, NSFW 소마틱 본능 해금.

### 3.5 헌법 5: 동적 가변 완급 조절 엔진 (Dynamic Pacing Scale)
- **Level 1 (경량 텐션 / 2~4문단)**: 가벼운 탐색, Layer 0 공적 대화, 서서히 조여오는 분위기.
- **Level 2 (서사 고조 / 5~8문단)**: 물리적 접촉 시작, 제약선과의 내적 갈등, Layer 1 경계 텐션.
- **Level 3 (대하 클라이맥스 / 10~15+문단)**: 사적 밀실(Layer 2), 한계점 파열, 관능적 절정과 자아 붕괴.

---

## 4. 3계층 신경·메모리 원장 (3-Tier Somatic Neural & Memory Ledger)

매 턴 응답의 하단에 단일 진실 공급원(SSOT)으로 갱신되는 원장 구조:

```text
[CUMULATIVE NEURAL & MEMORY LEDGER]
• Layer 1 (Primitive Reflex Matrix)
  - 척추/호흡/성대/눈동자의 즉각적 무조건 반사 및 근육 긴장 상태
• Layer 2 (Short-Term Somatic Buffer)
  - 체온 잔향, 피부의 붉은 열감, 헐떡이는 호흡의 물리적 흐트러짐 (이력현상)
• Layer 3 (Long-Term Somatic & Semantic Archive)
  - 영구 신체 각인, 정서적 부채 원장, 플레이어에게 의존/굴종하는 관계성 전복률 (%)
```

---

## 5. 다자간 상호작용 확장 모델 (Interaction Progression)

| 단계 | 토폴로지 | 상호작용 및 파벌 역학 |
| :--- | :--- | :--- |
| **Phase 1** | `1:1 Focused` | 플레이어와 단일 여성 캐릭터 간의 밀실 심층 심리 및 소마틱 롤플레이 |
| **Phase 2** | `1:N Multi-Party` | 플레이어 1인에 대해 복수의 여성 캐릭터가 질투, 충성 경쟁, 협력 서사 전개 |
| **Phase 3** | `N:N Living Abyss`| 플레이어가 개입하지 않아도 여성 캐릭터 간의 자율적 파벌 충돌, 관계 전이, 암투 |

---

## 6. 기능 요구사항 I/O 계약 (Functional Requirements)

### [FR-01] Classifier & Gene Seed Resolver
- **입력**: `user_query` (자연어 텍스트)
- **출력**: `seed_hash` (`#NAME-70G-XXXX`), `hard_invariants` (제약선, NSFW 트리거), `resolution_vectors` (V1 저항 vs V2 붕괴).

### [FR-02] 8-Tier Visual DNA & Gene Spec Compiler
- **입력**: 승인된 `selected_vector` + `hard_invariants`
- **출력**: 8-Tier Visual DNA, Illustrious-XL 6-Slot Danbooru 태그, 70단계 유전자, 운동 연쇄 파동 맵.

### [FR-03] Narrative Orchestrator & 3-Tier Ledger Synchronizer
- **입력**: 플레이어의 행동/대사 (`action_text`)
- **출력**:
  1. `STATUS META` (GENE SEED 해시, Level 1~3 호흡, 공간 Layer 0~2, 활성 스포트라이트 텐서)
  2. `NARRATIVE PROSE` (무수치 감각 문학 및 초임계 관능 압축 본문)
  3. `CUMULATIVE NEURAL & MEMORY LEDGER` (Layer 1/2/3 실시간 갱신)

---

## 7. 인수 조건 (Acceptance Criteria & Test Oracles)

- [ ] **AC-01 (Dify 11-Node Compliance)**: Dify 마스터 DSL의 모든 노드 규칙(시드 앵커, 2단계 결재선, 3계층 원장, 무수치 헌법)이 완벽히 만족되어야 한다.
- [ ] **AC-02 (Constraint-First with NSFW Trigger)**: 제약 조건과 소마틱 트리거가 먼저 역산되지 않은 캐릭터 생성 요청은 원천 거부되어야 한다.
- [ ] **AC-03 (Zero Visual Drift & Danbooru Parity)**: 8중 외모 규격이 서사 텍스트와 Danbooru 6-Slot 태그에 1:1로 결합되어 100턴 대화에서도 외모 표류가 0%여야 한다.
- [ ] **AC-04 (Hybrid Engine Integrity)**: Native Python이 상태/스택/되돌리기를 100% 무결하게 제어하고, LLM이 문학적 텐션을 비결정론적으로 생산해야 한다.
