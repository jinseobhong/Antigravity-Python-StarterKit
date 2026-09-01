/**
 * app.js — AbyssEngine Web Studio Reactive Controller
 */

let currentView = 'MAIN';
let activeChoicesList = [];
let cachedVaultList = [];
let currentArmorFilter = 'ALL';
let lastAnimatedStep = 0;
let lastRenderedSeedHash = '';
let activeTypingTimer = null;
let skipActiveTyping = null;
let selectedProviderTab = 'claude';

let creationFlowState = {
  concept: "",
  target_name: "",
  title: "",
  seed_hash: "",
  hard_invariants: [],
  resolution_vectors: [],
  selected_vector: null,
  compiled_spec: null
};

// ====================================================
// TOAST & LOADING HELPERS
// ====================================================
function showToast(msg) {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = "bg-purple-950/95 border border-purple-500/70 text-purple-100 text-xs font-bold px-4 py-3 rounded-2xl shadow-2xl backdrop-blur-md transition-all transform duration-300 translate-y-2 opacity-0 flex items-center gap-2 pointer-events-auto shadow-purple-950/50";
  toast.innerHTML = `<i class="fa-solid fa-sparkles text-amber-400 text-sm"></i> <span>${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  }, 10);
  setTimeout(() => {
    toast.classList.add('opacity-0', '-translate-y-2');
    setTimeout(() => toast.remove(), 300);
  }, 2800);
}

function showLoading(msg = '처리 중...') {
  const el = document.getElementById('loadingOverlay');
  const txt = document.getElementById('loadingOverlayText');
  if (txt) txt.innerText = msg;
  if (el) el.classList.remove('hidden');
}

function hideLoading() {
  const el = document.getElementById('loadingOverlay');
  if (el) el.classList.add('hidden');
}

// ====================================================
// APP STATE (Single Source of Truth)
// ====================================================
const AppState = {
  character: null,
  chat_history: [],
  step: 1,
  last_action: '',
  last_narrative: '',
  active_tensors: [],
  choices: [],
  currentLlmConfig: {
    provider: 'claude',
    anthropic_model: 'claude-3-7-sonnet-20250219',
    gemini_model: 'gemini-2.5-flash'
  },

  setState(partial) {
    if (!partial) return;
    const incomingChar = partial.character || (partial.state && partial.state.character);
    if (incomingChar && incomingChar.seed_hash !== lastRenderedSeedHash) {
      lastRenderedSeedHash = incomingChar.seed_hash;
      lastAnimatedStep = 0;
      if (activeTypingTimer) {
        clearInterval(activeTypingTimer);
        activeTypingTimer = null;
      }
      const container = document.getElementById('chatLogContainer');
      if (container) container.innerHTML = '';
    }

    if (partial.state) {
      Object.assign(this, partial.state);
    } else {
      Object.assign(this, partial);
    }
    this.render();
  },

  async dispatch(actionFn, customLoadingMsg = '처리 중...') {
    showLoading(customLoadingMsg);
    try {
      const data = await actionFn();
      if (data && (data.character || (data.state && data.state.character))) {
        const nextState = data.state || data;
        this.setState(nextState);
      }
      return data;
    } catch (err) {
      console.error('[AppState Dispatch Error]:', err);
      showToast('통신 오류가 발생했습니다.');
      return null;
    } finally {
      hideLoading();
    }
  },

  render() {
    if (!this.character) return;
    renderState(this);
    this.updateLlmBadges();
  },

  updateLlmBadges() {
    const isClaude = this.currentLlmConfig.provider === 'claude';
    const modelName = isClaude ? this.currentLlmConfig.anthropic_model : this.currentLlmConfig.gemini_model;
    let shortName = isClaude ? '🟣 Claude ' : '🔵 Gemini ';
    if (modelName.includes('3-7-sonnet')) shortName += '3.7';
    else if (modelName.includes('3-5-sonnet')) shortName += '3.5';
    else if (modelName.includes('2.5-flash')) shortName += '2.5F';
    else if (modelName.includes('2.0-flash')) shortName += '2.0F';
    else shortName += (modelName.split('-')[1] || modelName);

    const hubBadge = document.getElementById('hubLlmLabel');
    if (hubBadge) hubBadge.innerText = shortName;
    const rpBadge = document.getElementById('rpLlmLabel');
    if (rpBadge) rpBadge.innerText = shortName;
    const wsBadge = document.getElementById('wsLlmLabel');
    if (wsBadge) wsBadge.innerText = `${shortName} 설정`;
  }
};

// ====================================================
// VIEW ROUTING
// ====================================================
function switchView(viewName) {
  currentView = viewName;
  try {
    localStorage.setItem('abyss_active_view', viewName);
  } catch (e) {}

  document.getElementById('viewMainHub')?.classList.add('hidden');
  document.getElementById('viewRoleplay')?.classList.add('hidden');
  document.getElementById('viewWorkshop')?.classList.add('hidden');

  if (viewName === 'MAIN') {
    document.getElementById('viewMainHub')?.classList.remove('hidden');
  } else if (viewName === 'ROLEPLAY') {
    document.getElementById('viewRoleplay')?.classList.remove('hidden');
    setTimeout(() => {
      const clc = document.getElementById('chatLogContainer');
      if (clc) clc.scrollTop = clc.scrollHeight;
      document.getElementById('roleplayInput')?.focus();
    }, 50);
  } else if (viewName === 'WORKSHOP') {
    document.getElementById('viewWorkshop')?.classList.remove('hidden');
    loadVaultCharacters();
  }
}

// ====================================================
// STATE RENDERING
// ====================================================
function getArmorTheme(armorType) {
  const a = (armorType || '').toLowerCase();
  if (a.includes('rigid')) {
    return {
      badgeClass: 'bg-amber-950/80 border border-amber-500/50 text-amber-300',
      activeBorder: 'border-amber-500 ring-2 ring-amber-500/40 shadow-xl shadow-amber-950/40',
      cardBorder: 'border-amber-500/40 hover:border-amber-400',
      gradient: 'from-amber-600 via-orange-600 to-purple-800',
      icon: 'fa-shield-halved text-amber-400'
    };
  } else if (a.includes('endurer')) {
    return {
      badgeClass: 'bg-sky-950/80 border border-sky-500/50 text-sky-300',
      activeBorder: 'border-sky-500 ring-2 ring-sky-500/40 shadow-xl shadow-sky-950/40',
      cardBorder: 'border-sky-500/40 hover:border-sky-400',
      gradient: 'from-slate-600 via-blue-600 to-indigo-800',
      icon: 'fa-cross text-sky-400'
    };
  } else if (a.includes('controller')) {
    return {
      badgeClass: 'bg-rose-950/80 border border-rose-500/50 text-rose-300',
      activeBorder: 'border-rose-500 ring-2 ring-rose-500/40 shadow-xl shadow-rose-950/40',
      cardBorder: 'border-rose-500/40 hover:border-rose-400',
      gradient: 'from-rose-600 via-purple-700 to-fuchsia-900',
      icon: 'fa-chess-queen text-rose-400'
    };
  } else {
    return {
      badgeClass: 'bg-teal-950/80 border border-teal-500/50 text-teal-300',
      activeBorder: 'border-teal-500 ring-2 ring-teal-500/40 shadow-xl shadow-teal-950/40',
      cardBorder: 'border-teal-500/40 hover:border-teal-400',
      gradient: 'from-teal-600 via-emerald-600 to-indigo-900',
      icon: 'fa-heart-crack text-teal-400'
    };
  }
}

function renderState(data) {
  if (!data || !data.character) return;
  const c = data.character;
  const theme = getArmorTheme(c.armor_type);

  // 1. Lobby Update
  const nameEl = document.getElementById('hubCharName');
  if (nameEl) nameEl.innerText = c.name;
  const titleEl = document.getElementById('hubCharTitle');
  if (titleEl) titleEl.innerText = `${c.title} • ${c.faction}`;
  const seedEl = document.getElementById('hubCharSeed');
  if (seedEl) seedEl.innerText = c.seed_hash;
  const armorEl = document.getElementById('hubCharArmor');
  if (armorEl) armorEl.innerHTML = `<i class="fa-solid ${theme.icon} mr-1.5"></i>${c.armor_type}`;

  const imgEl = document.getElementById('hubCharImg');
  const phEl = document.getElementById('hubCharImgPlaceholder');
  if (c.image_url && imgEl && phEl) {
    imgEl.src = c.image_url;
    imgEl.classList.remove('hidden');
    phEl.classList.add('hidden');
  } else if (imgEl && phEl) {
    imgEl.src = '';
    imgEl.classList.add('hidden');
    phEl.classList.remove('hidden');
  }

  // Traits
  let hubTraitsHtml = '';
  const t = c.traits || {};
  Object.entries(t).forEach(([k, v]) => {
    hubTraitsHtml += `
      <div class="p-2 bg-gray-900/90 rounded-xl border border-gray-800 space-y-0.5">
        <span class="text-purple-300 font-extrabold text-[11px]">• ${k}</span>
        <p class="text-gray-300 leading-relaxed text-[11px]">${v}</p>
      </div>
    `;
  });
  const traitsBox = document.getElementById('hubCharTraits');
  if (traitsBox) traitsBox.innerHTML = hubTraitsHtml || '<div class="text-gray-500 text-[11px]">등록된 헌법 특성이 없습니다.</div>';

  // 2. Play Room Update
  document.getElementById('rpCharName').innerText = c.name;
  document.getElementById('rpCharTitle').innerText = c.title;
  document.getElementById('rpCharSeed').innerText = c.seed_hash;
  document.getElementById('rpCharArmor').innerHTML = `<i class="fa-solid ${theme.icon} mr-1"></i>${c.armor_type}`;
  document.getElementById('rpCharStage').innerText = c.pressure_stage;

  // 3. Workshop Detail Update
  const wsAvatar = document.getElementById('wsCharAvatar');
  if (wsAvatar) {
    if (c.image_url) {
      wsAvatar.innerHTML = `<img src="${c.image_url}" class="w-full h-full object-cover rounded-xl">`;
    } else {
      wsAvatar.innerText = c.name.charAt(0);
    }
  }
  document.getElementById('wsCharHeader').innerText = `${c.name} (${c.title} • ${c.faction})`;
  document.getElementById('wsCharSeed').innerText = c.seed_hash;
  document.getElementById('wsCharArmor').innerHTML = `<span>${c.armor_type}</span><span class="text-pink-400 font-medium">${c.pressure_stage}</span>`;
  document.getElementById('wsCharTraits').innerHTML = hubTraitsHtml;

  // 4. Conversation Log Stream
  renderChatLog(data, theme);
}

function renderChatLog(data, theme) {
  const container = document.getElementById('chatLogContainer');
  if (!container) return;

  const historyList = (data.chat_history && data.chat_history.length > 0) ? data.chat_history : [
    {
      step: data.step,
      user_action: data.last_action,
      narrative_prose: data.last_narrative,
      pressure_stage: data.character.pressure_stage
    }
  ];

  let logHtml = `
    <div class="text-center my-4">
      <span class="text-[11px] font-mono text-purple-300 bg-purple-950/70 px-3.5 py-1 rounded-full border border-purple-800/50 shadow-sm">
        👑 《심연의 혈통 : 침식의 제국》 Play Room &bull; ${data.character.name} (${data.character.title})
      </span>
    </div>
  `;

  historyList.forEach((turn, idx) => {
    if (turn.user_action && turn.step > 1) {
      logHtml += `
        <div class="flex justify-end my-4">
          <div class="max-w-2xl bg-purple-950/40 border border-purple-800/50 rounded-2xl rounded-tr-sm p-4 text-sm text-purple-100 shadow-lg">
            <div class="text-[10px] font-bold text-purple-400 mb-1 flex items-center gap-1">
              <i class="fa-solid fa-user"></i> 당신의 행동 / 대사
            </div>
            <div class="leading-relaxed font-medium">${escapeHtml(turn.user_action)}</div>
          </div>
        </div>
      `;
    }

    if (turn.narrative_prose) {
      const parsed = window.marked ? marked.parse(turn.narrative_prose) : turn.narrative_prose;
      logHtml += `
        <div class="flex items-start gap-3.5 my-4">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-tr ${theme.gradient} flex items-center justify-center text-white text-sm font-black shadow-md shrink-0 mt-1">
            ${data.character.name.charAt(0)}
          </div>
          <div class="flex-1 glass-panel rounded-2xl rounded-tl-sm p-6 border border-cardBorder shadow-2xl">
            <div class="flex items-center justify-between border-b border-cardBorder pb-2.5 mb-3 text-xs">
              <div class="font-extrabold text-pink-300 flex items-center gap-2">
                <span>${data.character.name}</span>
                <span class="text-[10px] font-normal text-gray-400">(${turn.pressure_stage || data.character.pressure_stage})</span>
              </div>
              <div class="text-[10px] font-mono text-gray-500">TURN ${String(turn.step).padStart(2, '0')}</div>
            </div>
            <div class="prose-text text-sm md:text-[15px] leading-relaxed text-gray-100 font-normal">
              ${parsed}
            </div>
          </div>
        </div>
      `;
    }
  });

  container.innerHTML = logHtml;
  setTimeout(() => {
    container.scrollTop = container.scrollHeight;
  }, 50);
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// ====================================================
// INTERACTIVE ACTIONS
// ====================================================
function handleKeyDown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendRoleplayMessage();
  }
}

function fillAndSend(choiceIdx) {
  const chip = document.getElementById(`chip${choiceIdx}`);
  if (!chip) return;
  const textSpan = chip.querySelector('.chip-text');
  const txt = textSpan ? textSpan.innerText.trim() : chip.innerText.trim();
  const vectorTypes = ['DEVOTION_COMFORT', 'SUBJUGATION', 'SUBMISSION_FAWN', 'SOMATIC_SYNC', 'SUSPENSION'];
  const vec = vectorTypes[parseInt(choiceIdx, 10) - 1] || 'SUBJUGATION';

  document.getElementById('roleplayInput').value = txt;
  sendRoleplayMessage(txt, vec, choiceIdx);
}

async function sendRoleplayMessage(customTxt, vectorType, choiceId) {
  const inputEl = document.getElementById('roleplayInput');
  const txt = (customTxt || inputEl?.value || '').trim();
  if (!txt) return;

  if (inputEl) {
    inputEl.value = '';
    inputEl.style.height = 'auto';
  }

  await AppState.dispatch(async () => {
    const data = await API.sendAction(txt, vectorType || 'SUBJUGATION', choiceId || null);
    if (data && data.character) {
      showToast(`턴 ${data.step} 서사가 집필되었습니다.`);
    }
    return data;
  }, '서사 집필 중...');
}

async function triggerUndo() {
  await AppState.dispatch(async () => {
    const data = await API.triggerUndo();
    if (data && data.success) {
      showToast('직전 턴으로 되돌렸습니다.');
    } else {
      showToast('더 이상 되돌릴 턴이 없습니다.');
    }
    return data;
  }, '되돌리는 중...');
}

async function triggerReset() {
  if (!confirm('대화 기록을 초기화하시겠습니까?')) return;
  await AppState.dispatch(async () => {
    const data = await API.triggerReset();
    if (data && data.success) {
      showToast('대화 기록이 초기화되었습니다.');
    }
    return data;
  }, '초기화 중...');
}

async function triggerRegenerate() {
  const data = await API.triggerUndo();
  if (data && data.success && data.state && data.state.last_action) {
    await sendRoleplayMessage(data.state.last_action);
  }
}

// ====================================================
// VAULT & MODAL CONTROLLERS
// ====================================================
async function loadVaultCharacters() {
  try {
    const list = await API.getCharacters();
    cachedVaultList = list || [];
    filterVaultCharacters();
    renderModalCharList(cachedVaultList);
  } catch (err) {
    console.error(err);
  }
}

function filterVaultCharacters() {
  const query = (document.getElementById('vaultSearchInput')?.value || '').toLowerCase().trim();
  const filtered = cachedVaultList.filter(item => {
    if (currentArmorFilter !== 'ALL') {
      const armorType = (item.armor_type || '').toLowerCase();
      if (!armorType.includes(currentArmorFilter.toLowerCase())) return false;
    }
    if (query) {
      const name = (item.name || '').toLowerCase();
      const title = (item.title || '').toLowerCase();
      const seed = (item.seed_hash || '').toLowerCase();
      return name.includes(query) || title.includes(query) || seed.includes(query);
    }
    return true;
  });

  renderVaultGrid(filtered);
  const countEl = document.getElementById('vaultTotalCount');
  if (countEl) countEl.innerText = `조회: ${filtered.length}명 / 전체: ${cachedVaultList.length}명`;
}

function setArmorFilter(filterName) {
  currentArmorFilter = filterName;
  ['ALL', 'Rigid', 'Endurer', 'Controller', 'Deprived'].forEach(f => {
    const btn = document.getElementById(`chip-${f}`);
    if (btn) {
      if (f === filterName) {
        btn.className = "px-2.5 py-1 rounded-lg text-[11px] font-bold bg-purple-600 text-white shadow transition";
      } else {
        btn.className = "px-2.5 py-1 rounded-lg text-[11px] font-bold bg-gray-800 text-gray-400 hover:text-white hover:bg-gray-700 transition";
      }
    }
  });
  filterVaultCharacters();
}

function renderVaultGrid(list) {
  const grid = document.getElementById('vaultGrid');
  const currentActiveSeed = AppState.character?.seed_hash || '';
  if (!grid) return;

  if (!list || list.length === 0) {
    grid.innerHTML = '<div class="text-xs text-gray-500 col-span-4 p-8 text-center glass-panel rounded-2xl">캐릭터가 없습니다.</div>';
    return;
  }

  grid.innerHTML = list.map(item => {
    const theme = getArmorTheme(item.armor_type);
    const isActive = (item.seed_hash === currentActiveSeed);

    return `
      <div class="glass-panel rounded-2xl p-5 border ${isActive ? theme.activeBorder : theme.cardBorder} transition flex flex-col justify-between group shadow-lg relative bg-gradient-to-b from-gray-900/90 to-cardBg">
        ${isActive ? `
          <div class="absolute top-3 right-3 px-2 py-0.5 bg-emerald-950/90 border border-emerald-500/60 text-emerald-300 rounded-full font-extrabold text-[10px] flex items-center gap-1 shadow">
            <i class="fa-solid fa-crown text-amber-400"></i> 상주 중
          </div>
        ` : ''}
        <div>
          <div class="flex items-center gap-3 mb-3">
            <div class="w-11 h-11 rounded-xl bg-gradient-to-tr ${theme.gradient} flex items-center justify-center text-white text-base font-black shadow-md shrink-0">
              ${item.name.charAt(0)}
            </div>
            <div>
              <span class="text-[10px] font-mono text-amber-400 font-bold">${item.seed_hash}</span>
              <h4 class="text-base font-black text-white">${item.name}</h4>
              <p class="text-xs text-gray-400">${item.title}</p>
            </div>
          </div>
        </div>
        <div class="flex gap-1.5 mt-3">
          <button onclick="selectCharacter('${item.seed_hash}', false)" class="flex-1 py-2 bg-gradient-to-r from-purple-900 to-indigo-900 hover:from-purple-800 hover:to-indigo-800 text-white rounded-xl text-xs font-bold transition flex items-center justify-center gap-1 shadow">
            <i class="fa-solid fa-crown text-amber-300"></i> 선택
          </button>
          <button onclick="selectCharacter('${item.seed_hash}', true)" title="Play Room 즉시 입장" class="px-3.5 py-2 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white rounded-xl text-xs font-bold transition flex items-center justify-center shadow">
            <i class="fa-solid fa-play"></i>
          </button>
        </div>
      </div>
    `;
  }).join('');
}

function renderModalCharList(list) {
  const modalGrid = document.getElementById('modalCharGrid');
  if (!modalGrid) return;
  const currentActiveSeed = AppState.character?.seed_hash || '';

  modalGrid.innerHTML = list.map(item => {
    const theme = getArmorTheme(item.armor_type);
    const isActive = (item.seed_hash === currentActiveSeed);

    return `
      <div class="glass-panel rounded-2xl p-4 border ${isActive ? theme.activeBorder : theme.cardBorder} transition flex flex-col justify-between bg-gradient-to-b from-gray-900 to-cardBg">
        <div>
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr ${theme.gradient} flex items-center justify-center text-white text-base font-black mb-2 shadow">
            ${item.name.charAt(0)}
          </div>
          <span class="text-[10px] font-mono text-amber-400 font-bold">${item.seed_hash}</span>
          <h4 class="text-base font-black text-white">${item.name}</h4>
          <p class="text-xs text-purple-300 font-medium mb-3">${item.title}</p>
        </div>
        <div class="flex gap-1.5">
          <button onclick="selectCharacter('${item.seed_hash}', false)" class="flex-1 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl text-xs font-bold transition">
            선택
          </button>
          <button onclick="selectCharacter('${item.seed_hash}', true)" class="px-3.5 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-xl text-xs font-bold transition">
            <i class="fa-solid fa-play"></i>
          </button>
        </div>
      </div>
    `;
  }).join('');
}

async function selectCharacter(seedHash, enterRoleplay = false) {
  await AppState.dispatch(async () => {
    const data = await API.selectCharacter(seedHash);
    if (data && data.character) {
      closeCharListModal();
      showToast(`[${data.character.name}] 인격으로 전환되었습니다.`);
      if (enterRoleplay) {
        switchView('ROLEPLAY');
      } else {
        loadVaultCharacters();
      }
    }
    return data;
  }, '캐릭터 전환 중...');
}

// ====================================================
// MODAL OPEN / CLOSE
// ====================================================
function openCharListModal() {
  renderModalCharList(cachedVaultList);
  document.getElementById('charListModal')?.classList.remove('hidden');
}
function closeCharListModal() {
  document.getElementById('charListModal')?.classList.add('hidden');
}

function openLlmSettingsModal() {
  document.getElementById('llmSettingsModal')?.classList.remove('hidden');
}
function closeLlmSettingsModal() {
  document.getElementById('llmSettingsModal')?.classList.add('hidden');
}

function openExportModal() {
  const jsonStr = JSON.stringify(AppState.character || {}, null, 2);
  const promptArea = document.getElementById('promptArea');
  if (promptArea) promptArea.value = jsonStr;
  document.getElementById('exportModal')?.classList.remove('hidden');
}
function closeExportModal() {
  document.getElementById('exportModal')?.classList.add('hidden');
}

function openNewCharModal() {
  document.getElementById('createStep1')?.classList.remove('hidden');
  document.getElementById('createStep2')?.classList.add('hidden');
  document.getElementById('createStep3')?.classList.add('hidden');
  document.getElementById('newCharModal')?.classList.remove('hidden');
}
function closeNewCharModal() {
  document.getElementById('newCharModal')?.classList.add('hidden');
}

function openEditActiveCharacterModal() {
  const c = AppState.character;
  if (!c) return;
  document.getElementById('editSeedHash').value = c.seed_hash;
  document.getElementById('editName').value = c.name;
  document.getElementById('editTitle').value = c.title;
  document.getElementById('editTraitAppearance').value = c.traits['외모_특징'] || '';
  document.getElementById('editTraitDeficiency').value = c.traits['핵심_결핍'] || '';
  document.getElementById('editCharModal')?.classList.remove('hidden');
}
function closeEditCharModal() {
  document.getElementById('editCharModal')?.classList.add('hidden');
}

async function submitEditCharacter() {
  const seed_hash = document.getElementById('editSeedHash').value;
  const name = document.getElementById('editName').value.trim();
  const title = document.getElementById('editTitle').value.trim();
  const app = document.getElementById('editTraitAppearance').value.trim();
  const def = document.getElementById('editTraitDeficiency').value.trim();

  const traits = {};
  if (app) traits["외모_특징"] = app;
  if (def) traits["핵심_결핍"] = def;

  await AppState.dispatch(async () => {
    const data = await API.updateCharacter({ seed_hash, name, title, traits });
    if (data && data.success) {
      closeEditCharModal();
      showToast('캐릭터 정보가 수정되었습니다.');
      await loadVaultCharacters();
    }
    return data;
  }, '수정 중...');
}

async function deleteActiveCharacter() {
  const c = AppState.character;
  if (!c || !confirm(`[${c.name}] 캐릭터를 삭제하시겠습니까?`)) return;

  await AppState.dispatch(async () => {
    const data = await API.deleteCharacter(c.seed_hash);
    if (data && data.success) {
      showToast('캐릭터가 삭제되었습니다.');
      await loadVaultCharacters();
    }
    return data;
  }, '삭제 중...');
}

// ====================================================
// DIFY 11-NODE 2-CHECKPOINT CREATION
// ====================================================
async function startCharacterClassification() {
  const concept = document.getElementById('newCharConceptInput')?.value?.trim();
  if (!concept) {
    showToast('컨셉을 입력해주세요.');
    return;
  }

  showLoading('1단계: 제약선 및 직교 궤적 역산 중 (Dify Node 3)...');
  try {
    const res = await API.classifyConcept(concept);
    creationFlowState = {
      concept: concept,
      target_name: res.target_name || "미상의 귀족",
      title: res.title || "귀족",
      seed_hash: res.seed_hash || "#GENE-70G-INIT",
      hard_invariants: res.hard_invariants || [],
      resolution_vectors: res.resolution_vectors || []
    };

    // Render Checkpoint 1
    const choiceBox = document.getElementById('vectorChoiceContainer');
    if (choiceBox) {
      choiceBox.innerHTML = res.resolution_vectors.map((vec, idx) => `
        <div onclick="selectCreationVector(${idx})" class="p-3.5 bg-gray-900/90 hover:bg-purple-950/60 border border-gray-800 hover:border-purple-500/70 rounded-xl cursor-pointer transition flex flex-col gap-1">
          <div class="flex items-center justify-between">
            <span class="text-xs font-black text-white">${vec.label || (idx === 0 ? 'V1 (1안)' : 'V2 (2안)')}</span>
            <span class="text-[10px] text-purple-300 font-bold bg-purple-950 px-2 py-0.5 rounded border border-purple-800">${vec.armor_type || 'Rigid'}</span>
          </div>
          <p class="text-[11px] text-gray-300 leading-relaxed">${vec.summary || vec.description || ''}</p>
        </div>
      `).join('');
    }

    document.getElementById('createStep1')?.classList.add('hidden');
    document.getElementById('createStep2')?.classList.remove('hidden');
    showToast('Checkpoint 1: V1 vs V2 궤적 선택 단계에 진입했습니다.');
  } catch (e) {
    showToast('역산 실패: ' + e);
  } finally {
    hideLoading();
  }
}

async function selectCreationVector(idx) {
  creationFlowState.selected_vector = creationFlowState.resolution_vectors[idx] || {};

  showLoading('2단계: 8-Tier DNA & 70-Gene 스펙 컴파일 중 (Dify Node 7)...');
  try {
    const res = await API.compileSpec(
      creationFlowState.target_name,
      creationFlowState.title,
      creationFlowState.seed_hash,
      creationFlowState.hard_invariants,
      creationFlowState.selected_vector
    );
    creationFlowState.compiled_spec = res.spec;

    const previewEl = document.getElementById('compiledSpecPreview');
    if (previewEl) {
      previewEl.innerHTML = `
        <div class="text-amber-300 font-bold">DNA Seed: ${res.spec.seed_hash}</div>
        <div class="text-purple-300 font-bold">Name: ${res.spec.target_name} (${res.spec.title})</div>
        <div class="text-pink-300 font-bold">Danbooru Tags: ${res.spec.danbooru_prompt || 'N/A'}</div>
        <div class="mt-2 text-gray-400">Hard Invariants: ${res.spec.hard_invariants?.length || 0} rules mapped</div>
      `;
    }

    document.getElementById('createStep2')?.classList.add('hidden');
    document.getElementById('createStep3')?.classList.remove('hidden');
    showToast('Checkpoint 2: 8-Tier DNA 스펙 검토 단계에 진입했습니다.');
  } catch (e) {
    showToast('컴파일 실패: ' + e);
  } finally {
    hideLoading();
  }
}

async function applyAndPersistCharacter() {
  showLoading('3단계: 마스터 헌법 합성 및 DB 영구 저장 중 (Dify Node 10 & 11)...');
  try {
    const data = await API.createCharacter({
      target_name: creationFlowState.target_name,
      title: creationFlowState.title,
      seed_hash: creationFlowState.seed_hash,
      hard_invariants: creationFlowState.hard_invariants,
      selected_vector: creationFlowState.selected_vector
    });

    if (data && data.character) {
      closeNewCharModal();
      AppState.setState(data);
      showToast(`👑 [${data.character.name}] 인격이 영구 저장되고 즉시 활성화되었습니다!`);
      await loadVaultCharacters();
    }
  } catch (e) {
    showToast('저장 실패: ' + e);
  } finally {
    hideLoading();
  }
}

// ====================================================
// INITIALIZATION
// ====================================================
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const [stateData, charList, llmConfig] = await Promise.all([
      API.getState(),
      API.getCharacters(),
      API.getLlmConfig()
    ]);

    if (llmConfig) {
      AppState.currentLlmConfig = llmConfig;
      AppState.updateLlmBadges();
    }
    if (charList) {
      cachedVaultList = charList;
      filterVaultCharacters();
    }
    if (stateData) {
      AppState.setState(stateData);
    }
  } catch (err) {
    console.error('Boot error:', err);
  }

  const lastView = localStorage.getItem('abyss_active_view') || 'MAIN';
  switchView(lastView);
});
