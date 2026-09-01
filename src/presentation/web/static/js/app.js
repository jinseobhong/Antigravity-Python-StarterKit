/**
 * app.js — AbyssEngine Web Studio Single Page App Controller
 */

const App = {
  currentView: "lobby",
  creationState: {
    target_name: "",
    title: "",
    seed_hash: "",
    hard_invariants: [],
    resolution_vectors: [],
    selected_vector: null
  },

  async init() {
    this.bindEvents();
    await this.switchView("lobby");
    await this.loadConfig();
  },

  bindEvents() {
    // 뷰 전환 버튼
    document.getElementById("btn-nav-lobby")?.addEventListener("click", () => this.switchView("lobby"));
    document.getElementById("btn-portal-play")?.addEventListener("click", () => this.switchView("play"));
    document.getElementById("btn-portal-vault")?.addEventListener("click", () => this.switchView("vault"));
    document.getElementById("btn-lobby-switch")?.addEventListener("click", () => this.switchView("vault"));
    document.getElementById("btn-play-switch")?.addEventListener("click", () => this.switchView("vault"));
    document.getElementById("btn-vault-lobby")?.addEventListener("click", () => this.switchView("lobby"));
    document.getElementById("btn-play-lobby")?.addEventListener("click", () => this.switchView("lobby"));

    // 전술 선택지 칩 바인딩
    document.querySelectorAll(".tactical-chip").forEach(chip => {
      chip.addEventListener("click", (e) => {
        const stimulus = chip.dataset.stimulus || "DEFAULT";
        const text = chip.dataset.actionText || chip.innerText.trim();
        PlayView.sendTurn(text, stimulus);
      });
    });

    // 플레이 룸 전송 버튼
    document.getElementById("btn-send-turn")?.addEventListener("click", () => {
      const text = document.getElementById("chat-input")?.value?.trim();
      if (text) PlayView.sendTurn(text);
    });

    // Enter 전송 / Shift+Enter 줄바꿈
    document.getElementById("chat-input")?.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        const text = e.target.value.trim();
        if (text) PlayView.sendTurn(text);
      }
    });

    // Undo / Reset
    document.getElementById("btn-play-undo")?.addEventListener("click", () => PlayView.handleUndo());
    document.getElementById("btn-play-reset")?.addEventListener("click", () => PlayView.handleReset());

    // 단부루 생성 버튼
    document.getElementById("btn-lobby-generate-danbooru")?.addEventListener("click", () => LobbyView.triggerGenerateDanbooru());

    // 캐릭터 생성 버튼
    document.getElementById("btn-vault-create")?.addEventListener("click", () => this.openCreateModal());
  },

  async switchView(viewName) {
    this.currentView = viewName;
    document.querySelectorAll(".view-section").forEach(el => el.classList.remove("active"));
    
    const targetSection = document.getElementById(`view-${viewName}`);
    if (targetSection) targetSection.classList.add("active");

    if (viewName === "lobby") {
      await LobbyView.init();
    } else if (viewName === "play") {
      await PlayView.init();
    } else if (viewName === "vault") {
      await VaultView.init();
    }
  },

  async loadConfig() {
    const config = await API.getConfig();
    const configBadge = document.getElementById("top-config-badge");
    if (configBadge) {
      configBadge.innerText = `${config.llm_provider.toUpperCase()} (${config.has_gemini_key || config.has_anthropic_key ? 'ONLINE' : 'OFFLINE'})`;
    }
  },

  // -------------------------------------------------------------
  // Dify Node 3 & 7 HITL 2단계 캐릭터 생성 플로우
  // -------------------------------------------------------------
  openCreateModal() {
    Modal.open("create-character-modal");
  },

  async handleStartClassification() {
    const conceptInput = document.getElementById("create-concept-input")?.value?.trim();
    if (!conceptInput) {
      alert("캐릭터 컨셉이나 배경 설정을 입력해주세요.");
      return;
    }

    const classifyBtn = document.getElementById("btn-start-classify");
    classifyBtn.disabled = true;
    classifyBtn.innerText = "제약선 및 직교 궤적 역산 중...";

    try {
      const res = await API.classifyConcept(conceptInput);
      this.creationState = {
        target_name: res.target_name || "미상의 귀족",
        title: res.title || "귀족",
        seed_hash: res.seed_hash || "#GENE-70G-INIT",
        hard_invariants: res.hard_invariants || [],
        resolution_vectors: res.resolution_vectors || []
      };

      // Checkpoint 1 렌더링
      this.renderCheckpoint1();
    } catch (e) {
      alert("분류 및 궤적 도출 오류: " + e.message);
    } finally {
      classifyBtn.disabled = false;
      classifyBtn.innerText = "1. 제약선 & 2대 직교 궤적 역산 시작";
    }
  },

  renderCheckpoint1() {
    const step1Div = document.getElementById("create-step-1");
    const step2Div = document.getElementById("create-step-2");
    step1Div.style.display = "none";
    step2Div.style.display = "flex";

    const s = this.creationState;
    document.getElementById("cp1-char-info").innerText = `${s.target_name} (${s.title}) | ${s.seed_hash}`;
    document.getElementById("cp1-invariants-list").innerHTML = s.hard_invariants.map(inv => `<li>${inv}</li>`).join("");

    const vectorsContainer = document.getElementById("cp1-vectors-container");
    vectorsContainer.innerHTML = s.resolution_vectors.map(v => `
      <div class="portal-card" style="cursor: pointer;" onclick="App.selectVector('${v.vector_id}')">
        <div style="font-weight: 700; font-size: 1.05rem; color: #f472b6;">[${v.vector_id}] ${v.vector_name}</div>
        <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.3rem;">${v.axis_description}</div>
        <button class="btn btn-sm btn-purple" style="margin-top: 0.6rem;">이 궤적 채택 (${v.vector_id})</button>
      </div>
    `).join("");
  },

  async selectVector(vectorId) {
    const selected = this.creationState.resolution_vectors.find(v => v.vector_id === vectorId);
    this.creationState.selected_vector = selected;

    const step2Div = document.getElementById("create-step-2");
    step2Div.innerHTML = `<div style="text-align: center; padding: 2rem; color: #c084fc;">8-Tier Visual DNA, 17대 텐서, 70단계 유전자 컴파일 중... ✨</div>`;

    try {
      // Dify Node 7 듀얼 모드 스펙 컴파일
      const res = await API.compileSpec({
        target_name: this.creationState.target_name,
        title: this.creationState.title,
        seed_hash: this.creationState.seed_hash,
        hard_invariants: this.creationState.hard_invariants,
        selected_vector: selected
      });

      if (res.success && res.spec) {
        this.creationState.compiled_spec = res.spec;
        this.renderCheckpoint2();
      }
    } catch (e) {
      alert("컴파일 실패: " + e.message);
      this.openCreateModal();
    }
  },

  renderCheckpoint2() {
    const step2Div = document.getElementById("create-step-2");
    const step3Div = document.getElementById("create-step-3");
    step2Div.style.display = "none";
    step3Div.style.display = "flex";

    const s = this.creationState;
    const spec = s.compiled_spec;
    const dna = spec.visual_dna || {};
    const traits = spec.traits || {};

    const summaryBox = document.getElementById("cp2-summary-box");
    summaryBox.innerHTML = `
      <div style="color: #f472b6; font-weight: 700; margin-bottom: 0.4rem;">[8-Tier Visual DNA Summary]</div>
      • 골격: ${dna.skeletal || "표준 골격"}<br>
      • 동공: ${dna.ocular || "표준 동공"}<br>
      • 모발: ${dna.hair || "표준 모발"}<br>
      • 의복/초커: ${dna.apparel || "표준 의복"}<br>
      • 홍조/반응: ${dna.blush || "표준 홍조"}<br>
      <div style="color: #38bdf8; font-weight: 700; margin-top: 0.6rem; margin-bottom: 0.4rem;">[70-Step Personality Genes & Traits]</div>
      • 아키타입: ${traits.archetype_class || "Rigid"}<br>
      • 불변 제약선: ${s.hard_invariants?.[0] || "가문의 명예"}<br>
      • 채택된 궤적: [${s.selected_vector?.vector_id}] ${s.selected_vector?.vector_name}<br>
      • 17대 텐서 및 Illustrious-XL 6-Slot 단부루 태그 연동 완료
    `;
  },

  async handleFinalApply() {
    const applyBtn = document.getElementById("btn-cp2-apply");
    applyBtn.disabled = true;
    applyBtn.innerText = "25대 마스터 헌법 합성 및 DB 영속화 중... ✨";

    try {
      const s = this.creationState;
      const res = await API.compileCharacter({
        target_name: s.target_name,
        title: s.title,
        seed_hash: s.seed_hash,
        hard_invariants: s.hard_invariants,
        selected_vector: s.selected_vector
      });

      if (res.success) {
        Modal.close("create-character-modal");
        await VaultView.loadCharacters();
        await this.switchView("vault");
        alert(`✨ ${s.target_name} (${s.title}) 캐릭터가 25대 마스터 헌법과 함께 영구히 발현되었습니다!`);
      }
    } catch (e) {
      alert("발현 인가 오류: " + e.message);
    } finally {
      applyBtn.disabled = false;
      applyBtn.innerText = "👑 [APPLY] 25대 마스터 헌법 합성 및 발현 인가";
    }
  }
};

window.addEventListener("DOMContentLoaded", () => App.init());
