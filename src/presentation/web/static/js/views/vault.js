/**
 * views/vault.js — Character Studio & Vault View Controller
 */

const VaultView = {
  characters: [],
  selectedCharacter: null,
  currentFilter: "전체",

  async init() {
    await this.loadCharacters();
  },

  async loadCharacters() {
    this.characters = await API.getCharacters();
    const active = this.characters.find(c => c.is_active) || this.characters[0];
    this.selectedCharacter = active;
    this.renderGrid();
    this.renderInspector();
  },

  setFilter(filterName) {
    this.currentFilter = filterName;
    document.querySelectorAll(".filter-pill").forEach(el => {
      el.classList.toggle("active", el.innerText === filterName);
    });
    this.renderGrid();
  },

  renderGrid() {
    const grid = document.getElementById("vault-character-grid");
    if (!grid) return;

    let filtered = this.characters;
    if (this.currentFilter !== "전체") {
      filtered = this.characters.filter(c => 
        c.traits?.archetype_class?.toLowerCase().includes(this.currentFilter.toLowerCase())
      );
    }

    grid.innerHTML = filtered.map(c => `
      <div class="char-grid-card ${c.id === this.selectedCharacter?.id ? 'active-selected' : ''}" onclick="VaultView.selectCharacter(${c.id})">
        <div class="char-card-avatar-row">
          <div class="char-avatar-circle">${c.name.charAt(0)}</div>
          <div>
            <div style="font-weight: 700; font-size: 1.05rem;">${c.name}</div>
            <div style="font-size: 0.78rem; color: var(--text-muted);">${c.title}</div>
          </div>
        </div>

        <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
          <span class="pill-badge">${c.seed_hash}</span>
          <span class="pill-badge emerald">${c.traits?.archetype_class?.split(' ')[0] || 'Rigid'}</span>
        </div>

        <div style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4;">
          <strong>외모:</strong> ${c.traits?.traits_list?.[0]?.details || "고유 외모"}<br>
          <strong>결핍:</strong> ${c.traits?.traits_list?.[1]?.details || "고유 결핍"}
        </div>

        <div class="char-card-actions-row">
          <button class="btn btn-sm btn-icon" title="활성화 및 선택" onclick="event.stopPropagation(); VaultView.activateCharacter(${c.id})">▶</button>
          <button class="btn btn-sm" title="JSON 추출" onclick="event.stopPropagation(); VaultView.exportJson(${c.id})">📥 JSON</button>
          <button class="btn btn-sm" title="프롬프트 복사" onclick="event.stopPropagation(); VaultView.showMasterPrompt(${c.id})">📋 복사</button>
          <button class="btn btn-sm btn-purple" title="AI 일러스트 생성" onclick="event.stopPropagation(); VaultView.showDanbooruTags(${c.id})">🪄 AI</button>
        </div>
      </div>
    `).join("");
  },

  selectCharacter(charId) {
    this.selectedCharacter = this.characters.find(c => c.id === charId);
    this.renderGrid();
    this.renderInspector();
  },

  async activateCharacter(charId) {
    await API.setActiveCharacter(charId);
    await this.loadCharacters();
    App.switchView("play");
  },

  renderInspector() {
    const c = this.selectedCharacter;
    const inspector = document.getElementById("vault-inspector-body");
    if (!inspector || !c) return;

    const traits = c.traits?.traits_list || [];

    inspector.innerHTML = `
      <div class="inspector-header-row">
        <div style="display: flex; align-items: center; gap: 1rem;">
          <div class="char-avatar-circle" style="width: 52px; height: 52px; font-size: 1.3rem;">${c.name.charAt(0)}</div>
          <div>
            <div style="font-size: 1.25rem; font-weight: 800;">${c.name} (${c.title})</div>
            <div style="font-size: 0.85rem; color: var(--text-pink);">${c.seed_hash} | ${c.traits?.archetype_class}</div>
          </div>
        </div>
        <div style="display: flex; gap: 0.5rem;">
          <button class="btn btn-primary" onclick="VaultView.activateCharacter(${c.id})">▶ Play Room 입장</button>
          <button class="btn" onclick="VaultView.exportJson(${c.id})">📥 JSON 추출</button>
          <button class="btn" onclick="VaultView.showMasterPrompt(${c.id})">📋 25대 프롬프트</button>
          <button class="btn" style="color: #f43f5e;" onclick="VaultView.deleteCharacter(${c.id})">🗑️ 삭제</button>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 0.75rem;">
        <div class="trait-row">
          <div class="trait-row-title">발현 단계 & 생체 지표 (ODO / TAINT)</div>
          <div class="trait-row-desc">
            ${c.traits?.stage_progression} | ODO: ${c.traits?.somatic_metrics?.odo || "54.2%"} / TAINT: ${c.traits?.somatic_metrics?.taint || "7.1%"}
          </div>
        </div>
        <div class="trait-row">
          <div class="trait-row-title">불변 제약선 (Hard Invariants)</div>
          <div class="trait-row-desc">
            ${c.personality_gene?.hard_invariants?.primary_boundary || "가문의 명예"}
          </div>
        </div>
      </div>

      <div class="trait-rows-container" style="margin-top: 0.5rem;">
        ${traits.map(t => `
          <div class="trait-row">
            <div class="trait-row-title">${t.category}</div>
            <div class="trait-row-desc">${t.details}</div>
          </div>
        `).join("")}
      </div>
    `;
  },

  async showMasterPrompt(charId) {
    const res = await API.getMasterPrompt(charId);
    if (res && res.master_prompt) {
      Modal.showPromptModal(res.master_prompt);
    }
  },

  async showDanbooruTags(charId) {
    const res = await API.getDanbooruPrompt(charId);
    if (res && res.positive_prompt) {
      Modal.showDanbooruModal(res.positive_prompt, res.negative_prompt);
    }
  },

  async exportJson(charId) {
    const char = this.characters.find(c => c.id === charId);
    if (char) {
      const jsonStr = JSON.stringify(char, null, 2);
      const blob = new Blob([jsonStr], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${char.name}_${char.seed_hash}.json`;
      a.click();
    }
  },

  async deleteCharacter(charId) {
    if (confirm("이 캐릭터를 영구히 삭제하시겠습니까?")) {
      await API.deleteCharacter(charId);
      await this.loadCharacters();
    }
  }
};
