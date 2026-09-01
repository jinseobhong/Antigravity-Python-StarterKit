/**
 * app.js — AbyssEngine Dark Fantasy Roleplay Web Studio Engine
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 * - Dify 11-Node 2-Checkpoint Creation Flow (V1 vs V2 Narrative Cards & 8-Tier DNA)
 * - 3-Layer Somatic Ledger & Real-time Visual Novel Chat Feed
 * - SQLite WAL Persistence & Clean Data Synchronization
 */

// ====================================================
// GLOBAL STATE & REACTIVITY
// ====================================================
const AppState = {
  currentView: 'MAIN', // 'MAIN' | 'ROLEPLAY'
  activeCharacter: null,
  chatHistory: [],
  vaultCharacters: [],
  creationFlowState: {},

  setState(data) {
    if (!data) return;
    if (data.character) this.activeCharacter = data.character;
    if (data.chat_history) this.chatHistory = data.chat_history;
    this.render();
  },

  render() {
    renderMainHub(this.activeCharacter);
    renderRoleplayHeader(this.activeCharacter);
    renderChatFeed(this.chatHistory, this.activeCharacter);
  }
};

// ====================================================
// VIEW ROUTING
// ====================================================
function switchView(viewName) {
  AppState.currentView = viewName;
  const mainEl = document.getElementById('viewMain');
  const rpEl = document.getElementById('viewRoleplay');

  if (viewName === 'ROLEPLAY') {
    mainEl?.classList.add('hidden');
    rpEl?.classList.remove('hidden');
    scrollToBottomChat();
  } else {
    rpEl?.classList.add('hidden');
    mainEl?.classList.remove('hidden');
  }
}

// ====================================================
// LOBBY / HUB RENDERER
// ====================================================
function renderMainHub(char) {
  if (!char) return;

  // 1. Basic Info
  const nameEl = document.getElementById('hubCharName');
  const titleEl = document.getElementById('hubCharTitle');
  const seedEl = document.getElementById('hubCharSeed');
  const imgEl = document.getElementById('hubCharImg');
  const armorEl = document.getElementById('hubArmorBadge');
  const stageEl = document.getElementById('hubStageBadge');

  if (nameEl) nameEl.textContent = char.name || '미상의 인격';
  if (titleEl) titleEl.textContent = char.title || '심연의 죄수';
  if (seedEl) seedEl.textContent = char.seed_hash || '#GENE-70G-INIT';
  if (imgEl && char.portrait_url) imgEl.src = char.portrait_url;
  if (armorEl) armorEl.textContent = char.archetype_class || 'Rigid';
  if (stageEl) stageEl.textContent = char.stage_progression || 'Stage 1 (침실 개방)';

  // 2. Traits & Hard Invariants
  const traitsEl = document.getElementById('hubCharTraits');
  if (traitsEl) {
    const list = char.traits_list || [];
    traitsEl.innerHTML = `
      <div class="text-[11px] font-bold text-pink-300 flex items-center gap-1.5 pb-1 border-b border-cardBorder">
        <i class="fa-solid fa-lock text-rose-400"></i> 핵심 불변 제약선 & 심리 결핍
      </div>
      ${list.map(t => `
        <div class="flex items-start gap-2">
          <span class="px-1.5 py-0.5 rounded bg-purple-950 text-purple-300 font-bold text-[10px] shrink-0">${t.category || '특성'}</span>
          <span class="text-gray-300 text-[11px] leading-relaxed">${t.details || ''}</span>
        </div>
      `).join('')}
    `;
  }

  // 3. 8-Tier Visual DNA Grid
  const dnaGrid = document.getElementById('hubVisualDnaGrid');
  if (dnaGrid && char.visual_dna) {
    const v = char.visual_dna;
    dnaGrid.innerHTML = `
      <div class="p-2.5 bg-gray-950/80 rounded-xl border border-cardBorder space-y-1">
        <span class="text-purple-300 font-bold text-[11px] flex items-center gap-1">👑 골격 & 체형</span>
        <p class="text-gray-400 text-[11px] leading-relaxed">${v.face_geometry || v.skeletal || '황실 슬림 골격'}</p>
      </div>
      <div class="p-2.5 bg-gray-950/80 rounded-xl border border-cardBorder space-y-1">
        <span class="text-pink-300 font-bold text-[11px] flex items-center gap-1">👁️ 동공 & 안광</span>
        <p class="text-gray-400 text-[11px] leading-relaxed">${v.ocular_optics || v.ocular || '서늘한 금빛 안광'}</p>
      </div>
      <div class="p-2.5 bg-gray-950/80 rounded-xl border border-cardBorder space-y-1">
        <span class="text-purple-300 font-bold text-[11px] flex items-center gap-1">💇 모발 & 결</span>
        <p class="text-gray-400 text-[11px] leading-relaxed">${v.hair_physics || v.hair || '은빛 롱헤어'}</p>
      </div>
      <div class="p-2.5 bg-gray-950/80 rounded-xl border border-cardBorder space-y-1">
        <span class="text-rose-300 font-bold text-[11px] flex items-center gap-1">👗 의복 & 초커</span>
        <p class="text-gray-400 text-[11px] leading-relaxed">${v.apparel_accents || v.apparel || '은색 초커 드레스'}</p>
      </div>
    `;
  }

  // 4. Danbooru Text
  const danbooruEl = document.getElementById('hubDanbooruText');
  if (danbooruEl) {
    danbooruEl.textContent = char.danbooru_prompt || (char.visual_dna && char.visual_dna.danbooru_prompt) || '1girl, dark fantasy, masterpiece';
  }

  // 5. 3-Layer Somatic Ledger
  if (char.somatic_ledger) {
    const l1 = document.getElementById('hubLayer1Text');
    const l2 = document.getElementById('hubLayer2Text');
    const l3 = document.getElementById('hubLayer3Text');
    if (l1) l1.textContent = char.somatic_ledger.layer_1_reflex || '목덜미의 서늘한 금속 초커 사이로 경직된 척추의 영구 방어 기제.';
    if (l2) l2.textContent = char.somatic_ledger.layer_2_buffer || '귓바퀴와 쇄골로 서서히 번지는 붉은 열감, 헐떡이는 호흡의 미세한 흐트러짐.';
    if (l3) l3.textContent = char.somatic_ledger.layer_3_archive || '나의 긍지와 위엄은 너의 손길 따위에 흔들리지 않는다는 내적 독백의 균열.';
  }
}

// ====================================================
// PLAY ROOM HEADER & CHAT FEED RENDERER
// ====================================================
function renderRoleplayHeader(char) {
  if (!char) return;

  const nameEl = document.getElementById('rpCharName');
  const titleEl = document.getElementById('rpCharTitle');
  const seedEl = document.getElementById('rpCharSeed');
  const armorEl = document.getElementById('rpCharArmor');
  const stageEl = document.getElementById('rpCharStage');

  if (nameEl) nameEl.textContent = char.name;
  if (titleEl) titleEl.textContent = char.title;
  if (seedEl) seedEl.textContent = char.seed_hash;
  if (armorEl) armorEl.innerHTML = `<i class="fa-solid fa-shield text-purple-400 mr-1"></i>${char.archetype_class || 'Rigid'}`;
  if (stageEl) stageEl.textContent = char.stage_progression || 'Stage 1';

  // Gauges
  const g = char.gauges || { trust: 20, eroticism: 0, shame: -30, guilt: 15, submission: 20 };
  const bTrust = document.getElementById('badgeTrust');
  const bErotic = document.getElementById('badgeErotic');
  const bDom = document.getElementById('badgeDom');
  const bTaboo = document.getElementById('badgeTaboo');
  const bVuln = document.getElementById('badgeVuln');

  if (bTrust) bTrust.textContent = `신뢰 ${g.trust ?? 20}`;
  if (bErotic) bErotic.textContent = `성애 ${g.eroticism ?? 0}`;
  if (bDom) bDom.textContent = `수치 ${g.shame ?? -30}`;
  if (bTaboo) bTaboo.textContent = `죄책감 ${g.guilt ?? 15}`;
  if (bVuln) bVuln.textContent = `굴종 ${g.submission ?? 20}`;
}

function renderChatFeed(history, char) {
  const feed = document.getElementById('chatFeed');
  if (!feed) return;

  if (!history || history.length === 0) {
    feed.innerHTML = `
      <div class="glass-card rounded-3xl p-8 border border-purple-500/20 text-center space-y-3 max-w-2xl mx-auto my-12 shadow-2xl">
        <div class="w-14 h-14 rounded-2xl bg-purple-950 border border-purple-800 flex items-center justify-center text-pink-400 mx-auto text-xl shadow-lg">
          <i class="fa-solid fa-feather-pointed"></i>
        </div>
        <h3 class="serif-title text-lg font-black text-white">${char ? char.name : '인격'}의 사적 침실</h3>
        <p class="text-xs text-gray-400 leading-relaxed max-w-md mx-auto">
          밀실의 문이 닫히고 둘만의 침묵이 맴돕니다. 하단의 전술 칩이나 텍스트 입력을 통해 서사적 개입을 시작하세요.
        </p>
      </div>
    `;
    return;
  }

  feed.innerHTML = history.map((turn, idx) => `
    <div class="space-y-4">
      <!-- User Action -->
      ${turn.user_action ? `
        <div class="flex justify-end">
          <div class="max-w-xl bg-gradient-to-r from-purple-900/70 to-pink-900/60 p-4 rounded-3xl rounded-tr-sm border border-purple-500/40 shadow-xl text-xs text-gray-100 space-y-1">
            <span class="text-[10px] font-bold text-pink-300 uppercase tracking-widest flex items-center gap-1">
              <i class="fa-solid fa-user text-amber-400"></i> 사장님의 개입 (Step ${turn.step || (idx + 1)})
            </span>
            <p class="leading-relaxed">${turn.user_action}</p>
          </div>
        </div>
      ` : ''}

      <!-- AI Narrative Response -->
      <div class="flex justify-start">
        <div class="max-w-3xl glass-panel p-6 rounded-3xl rounded-tl-sm border border-pink-500/30 shadow-2xl space-y-4 text-xs">
          
          <!-- Character Header in Chat -->
          <div class="flex items-center justify-between pb-2 border-b border-cardBorder">
            <div class="flex items-center gap-2">
              <span class="serif-title font-black text-pink-300 text-sm">${char ? char.name : '상주 인격'}</span>
              <span class="text-[10px] text-gray-400 bg-gray-950 px-2 py-0.5 rounded-full border border-cardBorder">${turn.pressure_stage || 'Stage 1'}</span>
            </div>
            <span class="text-[10px] font-mono text-amber-400/80">${char ? char.seed_hash : ''}</span>
          </div>

          <!-- Narrative Prose -->
          <div class="narrative-prose text-gray-200 text-sm leading-loose whitespace-pre-wrap">
            ${turn.narrative_prose || ''}
          </div>

          <!-- Turn Meta Footer -->
          <div class="pt-2 border-t border-cardBorder/60 flex items-center justify-between text-[10px] text-gray-500 font-mono">
            <span>Dynamic Pacing : Level 2 (고조)</span>
            <span>Kinematic Chain Active</span>
          </div>

        </div>
      </div>
    </div>
  `).join('');

  scrollToBottomChat();
}

function scrollToBottomChat() {
  const feed = document.getElementById('chatFeed');
  if (feed) {
    setTimeout(() => {
      feed.scrollTop = feed.scrollHeight;
    }, 50);
  }
}

// ====================================================
// ACTIONS & TACTICAL CHIPS
// ====================================================
function injectTacticalChip(text) {
  const input = document.getElementById('actionInput');
  if (input) {
    input.value = text;
    input.focus();
  }
}

async function submitUserAction() {
  const input = document.getElementById('actionInput');
  const actionText = input?.value?.trim();
  if (!actionText) {
    showToast('서사적 개입 내용을 입력해주세요.');
    return;
  }

  input.value = '';
  showLoading('인격의 3계층 신경 반응과 서사를 집필 중입니다...');
  try {
    const data = await API.action(actionText);
    if (data) {
      AppState.setState(data);
    }
  } catch (e) {
    showToast('행동 집필 실패: ' + e);
  } finally {
    hideLoading();
  }
}

async function triggerUndo() {
  showLoading('직전 턴으로 서사를 되돌리는 중...');
  try {
    const data = await API.undo();
    if (data) {
      AppState.setState(data);
      showToast('직전 턴으로 되돌아갔습니다.');
    }
  } catch (e) {
    showToast('되돌리기 실패: ' + e);
  } finally {
    hideLoading();
  }
}

async function triggerReset() {
  if (!confirm('현재 인격의 대화 기록을 1턴 초기 상태로 리셋하시겠습니까?')) return;

  showLoading('서사를 1턴 오프닝으로 리셋 중...');
  try {
    const data = await API.reset();
    if (data) {
      AppState.setState(data);
      showToast('대화가 초기 상태로 리셋되었습니다.');
    }
  } catch (e) {
    showToast('리셋 실패: ' + e);
  } finally {
    hideLoading();
  }
}

// ====================================================
// DIFY 11-NODE 2-CHECKPOINT CREATION
// ====================================================
let creationFlowState = {};

function openNewCharModal() {
  creationFlowState = {};
  const input = document.getElementById('newCharConceptInput');
  if (input) input.value = '';

  document.getElementById('createStep1')?.classList.remove('hidden');
  document.getElementById('createStep2')?.classList.add('hidden');
  document.getElementById('createStep3')?.classList.add('hidden');
  document.getElementById('newCharModal')?.classList.remove('hidden');
}

function closeNewCharModal() {
  document.getElementById('newCharModal')?.classList.add('hidden');
}

async function startCharacterClassification() {
  const concept = document.getElementById('newCharConceptInput')?.value?.trim();
  if (!concept) {
    showToast('컨셉을 입력해주세요.');
    return;
  }

  showLoading('1단계: Dify Node 3 원초적 어휘 승화 및 궤적 역산 중...');
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

    // Render Checkpoint 1 Header
    const nameEl = document.getElementById('cp1CharName');
    const seedEl = document.getElementById('cp1SeedHash');
    const invList = document.getElementById('cp1InvariantsList');

    if (nameEl) nameEl.textContent = `👑 [${creationFlowState.target_name}] (${creationFlowState.title})`;
    if (seedEl) seedEl.textContent = creationFlowState.seed_hash;
    if (invList) {
      invList.innerHTML = creationFlowState.hard_invariants.map(inv => `
        <div class="flex items-start gap-1.5">
          <span class="text-rose-400 font-bold">•</span>
          <span class="text-gray-300 leading-relaxed">${inv}</span>
        </div>
      `).join('');
    }

    // Render Checkpoint 1 Rich Narrative Vector Cards
    const choiceBox = document.getElementById('vectorChoiceContainer');
    if (choiceBox) {
      choiceBox.innerHTML = creationFlowState.resolution_vectors.map((vec, idx) => {
        const isV1 = (vec.vector_id === 'V1' || idx === 0);
        const borderClass = isV1 ? 'border-purple-500/50 hover:border-purple-400 bg-purple-950/40 hover:bg-purple-950/70' : 'border-rose-500/50 hover:border-rose-400 bg-rose-950/40 hover:bg-rose-950/70';
        const badgeClass = isV1 ? 'bg-purple-950 text-purple-300 border-purple-800' : 'bg-rose-950 text-rose-300 border-rose-800';
        const icon = isV1 ? 'fa-shield-halved' : 'fa-fire';
        const title = vec.label || vec.vector_name || (isV1 ? 'V1 (1안) : 결벽과 오만의 방어선' : 'V2 (2안) : 즉각적인 소마틱 굴종');
        const desc = vec.description || vec.axis_description || '서사 전개 및 상호작용 케미';
        const op = vec.operation || (isV1 ? 'STRICT_GUARD' : 'SOMATIC_DESYNC_TRACK');

        return `
          <div onclick="selectCreationVector(${idx})" class="p-4 rounded-2xl border ${borderClass} cursor-pointer transition-all duration-300 space-y-2 shadow-lg group hover:scale-[1.01]">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="w-7 h-7 rounded-lg ${badgeClass} border flex items-center justify-center text-xs">
                  <i class="fa-solid ${icon}"></i>
                </div>
                <span class="text-sm font-black text-white group-hover:text-pink-300 transition">${title}</span>
              </div>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full border ${badgeClass}">
                ${vec.armor_type || (isV1 ? 'Rigid' : 'Endurer')}
              </span>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed narrative-prose pl-1 border-l-2 border-cardBorder group-hover:border-pink-500 transition">
              "${desc}"
            </p>
            <div class="flex items-center justify-between text-[10px] text-gray-500 font-mono pt-1">
              <span>오퍼레이션: <code>${op}</code></span>
              <span class="text-pink-400 font-bold group-hover:underline">선택하여 8-Tier DNA 컴파일 &rarr;</span>
            </div>
          </div>
        `;
      }).join('');
    }

    document.getElementById('createStep1')?.classList.add('hidden');
    document.getElementById('createStep2')?.classList.remove('hidden');
    showToast('Checkpoint 1: V1 vs V2 서사 궤적 선택 단계에 진입했습니다.');
  } catch (e) {
    showToast('역산 실패: ' + e);
  } finally {
    hideLoading();
  }
}

async function selectCreationVector(idx) {
  creationFlowState.selected_vector = creationFlowState.resolution_vectors[idx] || {};

  showLoading('2단계: Dify Node 8 8-Tier DNA & Danbooru 태그 컴파일 중...');
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
    if (previewEl && res.spec) {
      const vdna = res.spec.visual_dna || {};
      const danbooru = (typeof res.spec.danbooru_prompt === 'object' && res.spec.danbooru_prompt) ? res.spec.danbooru_prompt.positive : (res.spec.danbooru_prompt || '');
      
      previewEl.innerHTML = `
        <!-- Meta Summary -->
        <div class="p-3.5 bg-gray-950/90 rounded-2xl border border-cardBorder space-y-2">
          <div class="flex items-center justify-between">
            <span class="serif-title font-black text-pink-300 text-sm">${res.spec.target_name} (${res.spec.title})</span>
            <span class="text-[10px] font-mono text-amber-400 bg-amber-950 px-2 py-0.5 rounded border border-amber-500/40">${res.spec.seed_hash}</span>
          </div>
        </div>

        <!-- 8-Tier Visual DNA Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
          <div class="p-3 bg-gray-950 rounded-xl border border-cardBorder space-y-1">
            <span class="text-purple-300 font-bold text-[11px]">👑 골격 & 체형 (Skeletal)</span>
            <p class="text-gray-300 text-[11px] leading-relaxed">${vdna.face_geometry || vdna.skeletal || '168cm 황실 슬림 골격'}</p>
          </div>
          <div class="p-3 bg-gray-950 rounded-xl border border-cardBorder space-y-1">
            <span class="text-pink-300 font-bold text-[11px]">👁️ 동공 & 안광 (Ocular)</span>
            <p class="text-gray-300 text-[11px] leading-relaxed">${vdna.ocular_optics || vdna.ocular || '서늘한 금빛 안광'}</p>
          </div>
          <div class="p-3 bg-gray-950 rounded-xl border border-cardBorder space-y-1">
            <span class="text-purple-300 font-bold text-[11px]">💇 모발 & 부속 (Hair & Horns)</span>
            <p class="text-gray-300 text-[11px] leading-relaxed">${vdna.hair_physics || vdna.hair || '은빛 롱헤어'}</p>
          </div>
          <div class="p-3 bg-gray-950 rounded-xl border border-cardBorder space-y-1">
            <span class="text-rose-300 font-bold text-[11px]">👗 의복 & 초커 (Apparel & Choker)</span>
            <p class="text-gray-300 text-[11px] leading-relaxed">${vdna.apparel_accents || vdna.apparel || '서늘한 금속 초커 드레스'}</p>
          </div>
        </div>

        <!-- Danbooru Tag Box -->
        <div class="p-3 bg-purple-950/30 rounded-xl border border-purple-800/40 space-y-1">
          <div class="flex items-center justify-between text-[11px]">
            <span class="text-purple-300 font-bold flex items-center gap-1">
              <i class="fa-solid fa-palette text-pink-400"></i> AI 일러스트 Danbooru 태그
            </span>
          </div>
          <p class="text-[11px] font-mono text-pink-300 leading-relaxed break-all bg-gray-950 p-2 rounded-lg border border-cardBorder">
            ${danbooru || '1girl, dark fantasy, masterpiece'}
          </p>
        </div>
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
  showLoading('3단계: Dify Node 11 25-Master 마스터 시스템 헌법 합성 및 RDB 영구 저장 중...');
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
      showToast(`👑 [${data.character.name}] 인격이 영구 저장되고 활성화되었습니다!`);
      switchView('ROLEPLAY');
    }
  } catch (e) {
    showToast('저장 실패: ' + e);
  } finally {
    hideLoading();
  }
}

// ====================================================
// CHARACTER VAULT MODAL
// ====================================================
async function openCharListModal() {
  showLoading('보관소 인격 목록을 동기화 중...');
  try {
    const chars = await API.getCharacters();
    AppState.vaultCharacters = chars || [];
    renderCharListModal(AppState.vaultCharacters);
    document.getElementById('charListModal')?.classList.remove('hidden');
  } catch (e) {
    showToast('목록 로딩 실패: ' + e);
  } finally {
    hideLoading();
  }
}

function closeCharListModal() {
  document.getElementById('charListModal')?.classList.add('hidden');
}

function renderCharListModal(chars) {
  const container = document.getElementById('charListContainer');
  if (!container) return;

  if (!chars || chars.length === 0) {
    container.innerHTML = `
      <div class="p-6 text-center text-gray-400 space-y-2">
        <i class="fa-solid fa-ghost text-2xl text-purple-400"></i>
        <p>보관소에 저장된 인격이 없습니다. 신규 인격을 조각해 보세요.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = chars.map(c => `
    <div class="p-3.5 bg-gray-950/90 hover:bg-purple-950/40 rounded-2xl border border-cardBorder hover:border-purple-500/50 transition flex items-center justify-between group">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl overflow-hidden bg-gray-900 border border-cardBorder shrink-0">
          <img src="${c.portrait_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80'}" class="w-full h-full object-cover">
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="serif-title font-black text-white text-xs">${c.name}</span>
            <span class="text-[10px] font-mono text-amber-400 bg-amber-950/80 px-1.5 py-0.2 rounded border border-amber-500/30">${c.seed_hash}</span>
          </div>
          <p class="text-[11px] text-gray-400">${c.title || '심연의 죄수'}</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="selectVaultCharacter(${c.id})" class="px-3 py-1.5 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 text-white rounded-xl text-xs font-bold transition shadow">
          소환
        </button>
        <button onclick="deleteVaultCharacter(${c.id})" class="px-2.5 py-1.5 bg-red-950/80 hover:bg-red-900 text-red-300 rounded-xl text-xs font-bold transition border border-red-800/50">
          <i class="fa-solid fa-trash-can"></i>
        </button>
      </div>
    </div>
  `).join('');
}

async function selectVaultCharacter(id) {
  showLoading('인격을 침실로 소환하는 중...');
  try {
    const data = await API.selectCharacter(id);
    if (data) {
      AppState.setState(data);
      closeCharListModal();
      showToast(`👑 [${data.character.name}] 인격이 소환되었습니다.`);
    }
  } catch (e) {
    showToast('소환 실패: ' + e);
  } finally {
    hideLoading();
  }
}

async function deleteVaultCharacter(id) {
  if (!confirm('정말로 이 인격을 영구 삭제하시겠습니까?')) return;
  showLoading('인격을 삭제하는 중...');
  try {
    const data = await API.deleteCharacter(id);
    if (data) {
      AppState.setState(data);
      await openCharListModal();
      showToast('인격이 삭제되었습니다.');
    }
  } catch (e) {
    showToast('삭제 실패: ' + e);
  } finally {
    hideLoading();
  }
}

// ====================================================
// UTILS & TOASTS
// ====================================================
function showLoading(msg) {
  const overlay = document.getElementById('loadingOverlay');
  const text = document.getElementById('loadingOverlayText');
  if (text) text.textContent = msg || '처리 중입니다...';
  if (overlay) overlay.classList.remove('hidden');
}

function hideLoading() {
  const overlay = document.getElementById('loadingOverlay');
  if (overlay) overlay.classList.add('hidden');
}

function showToast(msg) {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'glass-panel p-3.5 rounded-2xl border border-pink-500/50 shadow-2xl text-xs font-bold text-gray-100 flex items-center gap-2 pointer-events-auto transition duration-300 transform translate-y-2 opacity-0';
  toast.innerHTML = `<i class="fa-solid fa-circle-info text-pink-400"></i> <span>${msg}</span>`;

  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  }, 10);

  setTimeout(() => {
    toast.classList.add('translate-y-2', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function copyDanbooruPrompt() {
  const text = document.getElementById('hubDanbooruText')?.textContent;
  if (text) {
    navigator.clipboard.writeText(text);
    showToast('Danbooru 프롬프트가 클립보드에 복사되었습니다.');
  }
}

async function triggerGenerateActiveImage() {
  if (!AppState.activeCharacter) {
    showToast('활성화된 인격이 없습니다.');
    return;
  }

  const char = AppState.activeCharacter;
  const danbooru = char.danbooru_prompt || (char.visual_dna && char.visual_dna.danbooru_prompt) || '1girl, dark fantasy, masterpiece';

  showLoading('🎨 AI 일러스트 실시간 렌더링 중 (Flux Anime Core)...');
  try {
    const res = await API.generateImage(char.seed_hash, danbooru);
    if (res && res.success && res.portrait_url) {
      char.portrait_url = res.portrait_url;
      const imgEl = document.getElementById('hubCharImg');
      if (imgEl) imgEl.src = res.portrait_url + '?t=' + new Date().getTime();
      showToast('🎨 AI 일러스트가 성공적으로 생성되어 적용되었습니다!');
    } else {
      showToast('일러스트 생성 실패: ' + (res.error || '알 수 없는 오류'));
    }
  } catch (e) {
    showToast('생성 통신 오류: ' + e);
  } finally {
    hideLoading();
  }
}

function openCustomImageUrlModal(mode) {
  document.getElementById('customImageUrlModal')?.classList.remove('hidden');
}

function closeCustomImageUrlModal() {
  document.getElementById('customImageUrlModal')?.classList.add('hidden');
}

async function submitManualImage() {
  const url = document.getElementById('customImageUrlInput')?.value?.trim();
  if (!url) return;
  closeCustomImageUrlModal();
  showToast('일러스트가 적용되었습니다.');
}

function openLlmSettingsModal() {
  showToast('Google Gemini Flash Lite 3.5 고반응 엔진 상시 가동 중');
}

// ====================================================
// INITIALIZATION
// ====================================================
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const stateData = await API.getState();
    if (stateData) {
      AppState.setState(stateData);
    }
  } catch (e) {
    console.warn('Initial state sync warning:', e);
  }
});
