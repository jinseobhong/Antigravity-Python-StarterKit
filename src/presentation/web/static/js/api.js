/**
 * api.js — AbyssEngine REST API Client
 */

const API = {
  async getState() {
    const res = await fetch("/api/state");
    return await res.json();
  },

  async getCharacters() {
    const res = await fetch("/api/characters");
    return await res.json();
  },

  async selectCharacter(seedHash) {
    const res = await fetch("/api/select_character", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ seed_hash: seedHash })
    });
    return await res.json();
  },

  async sendAction(actionText, vectorType = "SUBJUGATION", choiceId = null) {
    const res = await fetch("/api/action", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action_text: actionText,
        vector_type: vectorType,
        choice_id: choiceId
      })
    });
    return await res.json();
  },

  async triggerUndo() {
    const res = await fetch("/api/undo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({})
    });
    return await res.json();
  },

  async triggerReset() {
    const res = await fetch("/api/reset", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({})
    });
    return await res.json();
  },

  async classifyConcept(concept) {
    const res = await fetch("/api/characters/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ concept })
    });
    return await res.json();
  },

  async compileSpec(targetName, title, seedHash, hardInvariants, selectedVector) {
    const res = await fetch("/api/characters/compile-spec", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        target_name: targetName,
        title: title,
        seed_hash: seedHash,
        hard_invariants: hardInvariants,
        selected_vector: selectedVector
      })
    });
    return await res.json();
  },

  async createCharacter(data) {
    const res = await fetch("/api/create_character", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    return await res.json();
  },

  async updateCharacter(data) {
    const res = await fetch("/api/update_character", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    return await res.json();
  },

  async deleteCharacter(seedHash) {
    const res = await fetch("/api/delete_character", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ seed_hash: seedHash })
    });
    return await res.json();
  },

  async getLlmConfig() {
    const res = await fetch("/api/llm_config");
    return await res.json();
  },

  async saveLlmConfig(data) {
    const res = await fetch("/api/save_llm_config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    return await res.json();
  }
};
