/**
 * views/play.js — Play Room Theater View Controller
 */

const PlayView = {
  activeCharacter: null,
  isGenerating: false,

  async init() {
    this.activeCharacter = await API.getActiveCharacter();
    if (this.activeCharacter && this.activeCharacter.id) {
      await this.renderHeader();
      await this.loadTurnHistory();
    }
  },

  async renderHeader() {
    const char = this.activeCharacter;
    if (!char) return;

    // 이름 및 시드
    document.getElementById("play-char-name").innerText = `${char.name} (${char.title})`;
    document.getElementById("play-char-seed").innerText = char.seed_hash;
    document.getElementById("play-stage-badge").innerText = char.traits?.stage_progression || "Stage 1";

    // 5대 심리 게이지
    const g = char.traits?.gauges || {};
    document.getElementById("gauge-trust").innerText = `신뢰 ${g.trust ?? 20}%`;
    document.getElementById("gauge-eroticism").innerText = `성애 ${g.eroticism ?? 0}%`;
    document.getElementById("gauge-shame").innerText = `수치심 ${g.shame ?? -30}`;
    document.getElementById("gauge-guilt").innerText = `죄책감 ${g.guilt ?? 15}%`;
    document.getElementById("gauge-submission").innerText = `굴종 ${g.submission ?? 20}%`;
  },

  async loadTurnHistory() {
    const history = await API.getTurnHistory(this.activeCharacter.id);
    const chatContainer = document.getElementById("chat-stream");
    if (!chatContainer) return;

    if (history.length === 0) {
      chatContainer.innerHTML = `
        <div class="turn-bubble character">
          <span class="turn-meta-label">${this.activeCharacter.name} (초기 대면)</span>
          <div class="bubble-content">
            차가운 공기 속에서 ${this.activeCharacter.name}가 당신을 서늘한 눈빛으로 응시하고 있습니다. 침묵을 깨고 대화나 행동을 시도해 보세요.
          </div>
        </div>
      `;
      return;
    }

    chatContainer.innerHTML = history.map(h => `
      <div class="turn-bubble user">
        <span class="turn-meta-label">당신의 행동 / 대사</span>
        <div class="bubble-content">${this._escapeHtml(h.user_action)}</div>
      </div>
      <div class="turn-bubble character">
        <span class="turn-meta-label">${this.activeCharacter.name} (TURN ${h.turn_number})</span>
        <div class="bubble-content">
          ${this._formatProse(h.narrative_response)}
          <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px dashed rgba(255,255,255,0.1); font-size: 0.8rem; color: #94a3b8;">
            <strong>[3계층 신경·메모리 원장]</strong><br>
            • Layer 1: ${h.somatic_ledger?.layer_1_reflex || ""}<br>
            • Layer 2: ${h.somatic_ledger?.layer_2_buffer || ""}<br>
            • Layer 3: ${h.somatic_ledger?.layer_3_archive || ""}
          </div>
        </div>
      </div>
    `).join("");

    chatContainer.scrollTop = chatContainer.scrollHeight;
  },

  async sendTurn(actionText, stimulus = "DEFAULT") {
    if (!actionText || this.isGenerating) return;
    this.isGenerating = true;

    const inputEl = document.getElementById("chat-input");
    if (inputEl) inputEl.value = "";

    const chatContainer = document.getElementById("chat-stream");
    // 사용자 버블 즉시 렌더링
    const userBubble = document.createElement("div");
    userBubble.className = "turn-bubble user";
    userBubble.innerHTML = `
      <span class="turn-meta-label">당신의 행동 / 대사</span>
      <div class="bubble-content">${this._escapeHtml(actionText)}</div>
    `;
    chatContainer.appendChild(userBubble);

    // 로딩 인디케이터
    const loadingBubble = document.createElement("div");
    loadingBubble.className = "turn-bubble character";
    loadingBubble.id = "loading-bubble";
    loadingBubble.innerHTML = `
      <span class="turn-meta-label">${this.activeCharacter.name}가 서사를 집필하고 있습니다...</span>
      <div class="bubble-content" style="color: #c084fc;">
        신체 운동 연쇄 파동 전이 및 신경 원장 갱신 중 ✨
      </div>
    `;
    chatContainer.appendChild(loadingBubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    try {
      const res = await API.executeTurn(this.activeCharacter.id, actionText, stimulus);
      loadingBubble.remove();

      if (res && res.narrative_response) {
        const charBubble = document.createElement("div");
        charBubble.className = "turn-bubble character";
        charBubble.innerHTML = `
          <span class="turn-meta-label">${this.activeCharacter.name} (TURN ${res.turn_number})</span>
          <div class="bubble-content">
            ${this._formatProse(res.narrative_response)}
            <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px dashed rgba(255,255,255,0.1); font-size: 0.8rem; color: #94a3b8;">
              <strong>[3계층 신경·메모리 원장]</strong><br>
              • Layer 1: ${res.somatic_ledger?.layer_1_reflex || ""}<br>
              • Layer 2: ${res.somatic_ledger?.layer_2_buffer || ""}<br>
              • Layer 3: ${res.somatic_ledger?.layer_3_archive || ""}
            </div>
          </div>
        `;
        chatContainer.appendChild(charBubble);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        // 5대 게이지 실시간 업데이트
        if (res.gauges) {
          this.activeCharacter.traits.gauges = res.gauges;
          await this.renderHeader();
        }
      }
    } catch (e) {
      loadingBubble.innerHTML = `<div class="bubble-content" style="color: #f43f5e;">⚠️ 서사 생성 오류: ${e.message}</div>`;
    } finally {
      this.isGenerating = false;
    }
  },

  async handleUndo() {
    if (confirm("직전 턴을 되돌리고 신경 원장을 롤백하시겠습니까?")) {
      const res = await API.undoTurn(this.activeCharacter.id);
      if (res.success) {
        this.activeCharacter = await API.getActiveCharacter();
        await this.renderHeader();
        await this.loadTurnHistory();
      }
    }
  },

  async handleReset() {
    if (confirm("모든 대화 기록과 턴 원장을 초기화하시겠습니까?")) {
      await API.resetTurns(this.activeCharacter.id);
      await this.loadTurnHistory();
    }
  },

  _escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  },

  _formatProse(prose) {
    return prose.split("\n\n").map(p => `<p style="margin-bottom: 0.75rem;">${p.replace(/\n/g, "<br>")}</p>`).join("");
  }
};
