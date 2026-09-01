/**
 * modal.js — Modal Windows for HITL Checkpoints, Prompt Viewer, and Danbooru Tags
 */

const Modal = {
  open(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.add("open");
  },

  close(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.remove("open");
  },

  showDanbooruModal(posPrompt, negPrompt) {
    const body = document.getElementById("danbooru-modal-body");
    if (body) {
      body.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          <div>
            <label style="font-size: 0.8rem; font-weight: 700; color: #a855f7;">Positive Danbooru Tags (6-Slot Illustrious-XL)</label>
            <textarea readonly style="width: 100%; height: 110px; background: #0f111c; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #f1f5f9; padding: 0.6rem; font-size: 0.85rem; resize: none; margin-top: 0.3rem;">${posPrompt}</textarea>
            <button class="btn btn-sm btn-purple" style="margin-top: 0.4rem;" onclick="navigator.clipboard.writeText(\`${posPrompt.replace(/`/g, '\\`')}\`); alert('Positive 태그가 복사되었습니다!');">📋 Positive 태그 복사</button>
          </div>
          <div>
            <label style="font-size: 0.8rem; font-weight: 700; color: #f43f5e;">Negative Danbooru Tags</label>
            <textarea readonly style="width: 100%; height: 75px; background: #0f111c; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #f1f5f9; padding: 0.6rem; font-size: 0.85rem; resize: none; margin-top: 0.3rem;">${negPrompt}</textarea>
            <button class="btn btn-sm" style="margin-top: 0.4rem;" onclick="navigator.clipboard.writeText(\`${negPrompt.replace(/`/g, '\\`')}\`); alert('Negative 태그가 복사되었습니다!');">📋 Negative 태그 복사</button>
          </div>
        </div>
      `;
    }
    this.open("danbooru-modal");
  },

  showPromptModal(promptText) {
    const body = document.getElementById("prompt-modal-body");
    if (body) {
      body.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          <textarea readonly style="width: 100%; height: 320px; background: #0f111c; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #f1f5f9; padding: 0.75rem; font-size: 0.85rem; font-family: monospace; resize: none;">${promptText}</textarea>
          <button class="btn btn-primary" onclick="navigator.clipboard.writeText(\`${promptText.replace(/`/g, '\\`').replace(/\\/g, '\\\\')}\`); alert('25대 마스터 시스템 프롬프트가 복사되었습니다!');">📋 마스터 프롬프트 전체 복사</button>
        </div>
      `;
    }
    this.open("prompt-modal");
  }
};
