/**
 * src/presentation/web/static/js/api.js
 * Clean 4-Tier Backend API Client
 */

const ApiClient = {
  async getState() {
    const res = await fetch('/api/state');
    return await res.json();
  },

  async getCharacters() {
    const res = await fetch('/api/characters');
    return await res.json();
  },

  async selectCharacter(seedHash) {
    const res = await fetch('/api/select_character', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ seed_hash: seedHash })
    });
    return await res.json();
  },

  async classifyAndPropose(userQuery) {
    const res = await fetch('/api/classify_and_propose', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: userQuery })
    });
    return await res.json();
  },

  async synthesizeCharacter(payload) {
    const res = await fetch('/api/synthesize_character', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return await res.json();
  },

  async sendAction(actionText) {
    const res = await fetch('/api/action', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action_text: actionText })
    });
    return await res.json();
  },

  async undo() {
    const res = await fetch('/api/undo', { method: 'POST' });
    return await res.json();
  },

  async reset() {
    const res = await fetch('/api/reset', { method: 'POST' });
    return await res.json();
  },

  async exportPrompt() {
    const res = await fetch('/api/export_prompt');
    return await res.json();
  },

  async generateDanbooru() {
    const res = await fetch('/api/generate_danbooru', { method: 'POST' });
    return await res.json();
  }
};

window.ApiClient = ApiClient;
