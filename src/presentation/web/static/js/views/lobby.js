/**
 * views/lobby.js — Main Lobby Hub View Controller
 */

const LobbyView = {
  activeCharacter: null,

  async init() {
    await this.renderActivePersona();
  },

  async renderActivePersona() {
    const char = await API.getActiveCharacter();
    this.activeCharacter = char;
    if (!char || !char.id) return;

    // 시드 및 헤더
    const seedEl = document.getElementById("lobby-seed-badge");
    if (seedEl) seedEl.innerText = char.seed_hash || "";

    // 이름 및 칭호
    const nameEl = document.getElementById("lobby-char-name");
    if (nameEl) nameEl.innerText = char.name || "";

    const titleEl = document.getElementById("lobby-char-title");
    if (titleEl) titleEl.innerText = `${char.title || ""} • ${char.traits?.archetype_class || ""}`;

    // 3 Key Traits
    const traits = char.traits?.traits_list || [];
    const container = document.getElementById("lobby-traits-container");
    if (container) {
      container.innerHTML = traits.map(t => `
        <div class="trait-row">
          <div class="trait-row-title">${t.category}</div>
          <div class="trait-row-desc">${t.details}</div>
        </div>
      `).join("");
    }

    // 초상화 액자
    const portraitImg = document.getElementById("lobby-portrait-img");
    const placeholder = document.getElementById("lobby-portrait-placeholder");
    if (portraitImg && placeholder) {
      if (char.portrait_url) {
        portraitImg.src = char.portrait_url;
        portraitImg.style.display = "block";
        placeholder.style.display = "none";
      } else {
        portraitImg.style.display = "none";
        placeholder.style.display = "flex";
      }
    }
  },

  async triggerGenerateDanbooru() {
    if (!this.activeCharacter || !this.activeCharacter.id) return;
    const res = await API.getDanbooruPrompt(this.activeCharacter.id);
    if (res && res.positive_prompt) {
      Modal.showDanbooruModal(res.positive_prompt, res.negative_prompt);
    }
  }
};
