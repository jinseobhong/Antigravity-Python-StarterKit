/**
 * src/presentation/web/static/js/views/vault.js
 * [View 3] 캐릭터 보관소 그리드, 갑주 필터 및 검색 뷰
 */

const ARMOR_THEMES = {
  'Rigid': {
    gradient: 'from-amber-600 via-purple-700 to-indigo-900',
    border: 'border-purple-800/60',
    badge: 'bg-purple-950/80 text-purple-200 border-purple-600/40',
    icon: 'fa-shield-halved'
  },
  'Endurer': {
    gradient: 'from-blue-600 via-indigo-700 to-slate-900',
    border: 'border-blue-800/60',
    badge: 'bg-blue-950/80 text-blue-200 border-blue-600/40',
    icon: 'fa-cross'
  },
  'Controller': {
    gradient: 'from-fuchsia-600 via-purple-700 to-pink-900',
    border: 'border-pink-800/60',
    badge: 'bg-pink-950/80 text-pink-200 border-pink-600/40',
    icon: 'fa-wand-magic-sparkles'
  },
  'Deprived': {
    gradient: 'from-rose-600 via-purple-800 to-gray-900',
    border: 'border-rose-800/60',
    badge: 'bg-rose-950/80 text-rose-200 border-rose-600/40',
    icon: 'fa-heart-crack'
  }
};

let currentFilter = 'ALL';
let cachedCharacters = [];

const VaultView = {
  setCharacters(chars) {
    cachedCharacters = chars || [];
    this.filterAndRender();
  },

  setFilter(filterName) {
    currentFilter = filterName;
    ['ALL', 'Rigid', 'Endurer', 'Controller', 'Deprived'].forEach(f => {
      const btn = document.getElementById(`chip-${f}`);
      if (btn) {
        if (f === filterName) {
          btn.className = 'px-3 py-1 rounded-xl text-xs font-extrabold bg-purple-600 text-white shadow transition';
        } else {
          btn.className = 'px-3 py-1 rounded-xl text-xs font-bold bg-gray-900 text-gray-400 hover:text-white hover:bg-gray-800 transition';
        }
      }
    });
    this.filterAndRender();
  },

  filterAndRender() {
    const query = (document.getElementById('vaultSearchInput')?.value || '').toLowerCase().trim();
    const activeSeed = document.getElementById('hubCharSeed')?.innerText?.trim() || '';

    const filtered = cachedCharacters.filter(char => {
      // 1. 갑주 필터
      if (currentFilter !== 'ALL') {
        const armor = (char.armor_type || '').toLowerCase();
        if (!armor.includes(currentFilter.toLowerCase())) return false;
      }
      // 2. 검색어 필터
      if (query) {
        const name = (char.name || '').toLowerCase();
        const title = (char.title || '').toLowerCase();
        const faction = (char.faction || '').toLowerCase();
        const seed = (char.seed_hash || '').toLowerCase();
        const traits = Object.values(char.traits || {}).join(' ').toLowerCase();
        return name.includes(query) || title.includes(query) || faction.includes(query) || seed.includes(query) || traits.includes(query);
      }
      return true;
    });

    const countEl = document.getElementById('vaultCountLabel');
    if (countEl) countEl.innerText = `조회: ${filtered.length}명 / 전체: ${cachedCharacters.length}명`;

    const grid = document.getElementById('vaultGrid');
    if (!grid) return;

    if (filtered.length === 0) {
      grid.innerHTML = '<div class="col-span-3 p-8 text-center glass-panel rounded-2xl text-xs text-gray-400">조건에 일치하는 캐릭터가 없습니다.</div>';
      return;
    }

    grid.innerHTML = filtered.map(char => {
      const isActive = (char.seed_hash === activeSeed);
      const armorKey = Object.keys(ARMOR_THEMES).find(k => (char.armor_type || '').includes(k)) || 'Rigid';
      const theme = ARMOR_THEMES[armorKey];

      const traitEntries = Object.entries(char.traits || {}).slice(0, 2);
      const traitHtml = traitEntries.map(([k, v]) => `
        <div class="text-[11px] text-gray-400 truncate">
          <span class="text-purple-400 font-bold">• ${k}:</span> ${v}
        </div>
      `).join('');

      return `
        <div class="glass-panel rounded-2xl p-5 border ${isActive ? 'border-amber-400 shadow-xl ring-1 ring-amber-400/50' : theme.border} transition flex flex-col justify-between group shadow-lg bg-gradient-to-b from-gray-900/90 to-cardBg relative">
          ${isActive ? `
            <div class="absolute top-3 right-3 px-2.5 py-0.5 bg-emerald-950/90 border border-emerald-500/60 text-emerald-300 rounded-full font-extrabold text-[10px] flex items-center gap-1 shadow animate-pulse">
              <i class="fa-solid fa-crown text-amber-400"></i> 상주 중
            </div>
          ` : ''}

          <div>
            <div class="flex items-center gap-3.5 mb-3">
              <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr ${theme.gradient} flex items-center justify-center text-white text-lg font-black shadow-md shrink-0">
                ${char.name.charAt(0)}
              </div>
              <div class="overflow-hidden">
                <span class="text-[10px] font-mono text-amber-400 font-bold">${char.seed_hash}</span>
                <h4 class="text-base font-black text-white truncate">${char.name}</h4>
                <p class="text-xs text-gray-400 truncate">${char.title}</p>
              </div>
            </div>

            <div class="mb-3 flex items-center justify-between">
              <span class="px-2.5 py-0.5 rounded-lg text-[10px] font-bold ${theme.badge} flex items-center gap-1 border">
                <i class="fa-solid ${theme.icon}"></i> ${char.armor_type.split(' ')[0]}
              </span>
              <span class="text-[11px] text-gray-400 font-medium">${char.faction || '독립 세력'}</span>
            </div>

            <div class="bg-gray-950/70 rounded-xl p-3 border border-gray-800/80 mb-4 space-y-1">
              ${traitHtml || '<span class="text-[11px] text-gray-500">설정 없음</span>'}
            </div>
          </div>

          <div class="space-y-2 pt-2 border-t border-gray-800/60">
            <button onclick="App.selectCharacter('${char.seed_hash}', true)" class="w-full py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 shadow">
              <i class="fa-solid fa-play text-[10px]"></i> Play Room 입장
            </button>
          </div>
        </div>
      `;
    }).join('');
  }
};

window.VaultView = VaultView;
