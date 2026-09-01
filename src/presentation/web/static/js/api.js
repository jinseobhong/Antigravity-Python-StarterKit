/**
 * api.js — AbyssEngine Web Studio REST API Client
 */

const API = {
  async getCharacters() {
    const res = await fetch("/api/characters");
    return res.json();
  },

  async getActiveCharacter() {
    const res = await fetch("/api/characters/active");
    return res.json();
  },

  async setActiveCharacter(charId) {
    const res = await fetch("/api/characters/active", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ character_id: charId })
    });
    return res.json();
  },

  async classifyConcept(conceptText) {
    const res = await fetch("/api/characters/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ concept: conceptText })
    });
    return res.json();
  },

  async compileSpec(payload) {
    const res = await fetch("/api/characters/compile-spec", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async synthesizeMaster(characterData) {
    const res = await fetch("/api/characters/synthesize-master", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ character_data: characterData })
    });
    return res.json();
  },

  async compileCharacter(payload) {
    const res = await fetch("/api/characters/compile", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async deleteCharacter(charId) {
    const res = await fetch("/api/characters/delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ character_id: charId })
    });
    return res.json();
  },

  async getTurnHistory(charId) {
    const url = charId ? `/api/turns?character_id=${charId}` : "/api/turns";
    const res = await fetch(url);
    return res.json();
  },

  async executeTurn(charId, userAction, stimulusType = "DEFAULT") {
    const res = await fetch("/api/turns", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        character_id: charId,
        user_action: userAction,
        stimulus_type: stimulusType
      })
    });
    return res.json();
  },

  async undoTurn(charId) {
    const res = await fetch("/api/turns/undo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ character_id: charId })
    });
    return res.json();
  },

  async resetTurns(charId) {
    const res = await fetch("/api/turns/reset", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ character_id: charId })
    });
    return res.json();
  },

  async getDanbooruPrompt(charId) {
    const res = await fetch("/api/characters/danbooru", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ character_id: charId })
    });
    return res.json();
  },

  async getMasterPrompt(charId) {
    const res = await fetch("/api/characters/prompt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ character_id: charId })
    });
    return res.json();
  },

  async importCharacter(jsonStr) {
    const res = await fetch("/api/import", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ character_json: jsonStr })
    });
    return res.json();
  },

  async getConfig() {
    const res = await fetch("/api/config");
    return res.json();
  }
};
