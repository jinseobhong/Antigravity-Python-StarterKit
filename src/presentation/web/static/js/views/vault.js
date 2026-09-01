/**
 * src/presentation/web/static/js/views/vault.js
 * [View 3] 캐릭터 보관소 & 신규 발현 모달 뷰
 */

let cachedCharacters = [];

const VaultView = {
  setCharacters(chars) {
    cachedCharacters = chars || [];
    this.filterAndRender();
  },

  filterAndRender() {
    const query = (document.getElementById('vaultSearchInput')?.value || '').toLowerCase().trim();
    const activeSeed = document.getElementById('hubCharSeed')?.innerText?.trim() || '';

    const filtered = cachedCharacters.filter(char => {
      if (query) {
        const name = (char.name || '').toLowerCase();
        const title = (char.title || '').toLowerCase();
        const faction = (char.faction || '').toLowerCase();
        const seed = (char.seed_hash || '').toLowerCase();
        return name.includes(query) || title.includes(query) || faction.includes(query) || seed.includes(query);
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
      const v = char.visual_dna || {};
      const inv = char.personality_gene?.hard_invariants || {};

      return `
        <div class="glass-panel rounded-2xl p-5 border ${isActive ? 'border-amber-400 shadow-xl ring-1 ring-amber-400/50' : 'border-purple-900/40'} transition flex flex-col justify-between group shadow-lg bg-gradient-to-b from-gray-900/90 to-cardBg relative">
          ${isActive ? `
            <div class="absolute top-3 right-3 px-2.5 py-0.5 bg-emerald-950/90 border border-emerald-500/60 text-emerald-300 rounded-full font-extrabold text-[10px] flex items-center gap-1 shadow animate-pulse">
              <i class="fa-solid fa-crown text-amber-400"></i> 활성 페르소나
            </div>
          ` : ''}

          <div>
            <div class="flex items-center gap-3.5 mb-3">
              <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-purple-600 to-pink-500 flex items-center justify-center text-white text-lg font-black shadow-md shrink-0">
                ${char.name.charAt(0)}
              </div>
              <div class="overflow-hidden">
                <span class="text-[10px] font-mono text-amber-400 font-bold">${char.seed_hash}</span>
                <h4 class="text-base font-black text-white truncate">${char.name}</h4>
                <p class="text-xs text-gray-400 truncate">${char.title} &bull; ${char.faction}</p>
              </div>
            </div>

            <!-- 불변 제약선 뱃지 -->
            <div class="bg-gray-950/70 rounded-xl p-3 border border-gray-800/80 mb-4 space-y-1.5 text-[11px]">
              <div><span class="text-purple-400 font-bold">🛡️ 제약선:</span> ${inv.primary_boundary || '결벽증'}</div>
              <div><span class="text-pink-400 font-bold">👁️ 외모:</span> ${v.ocular_optics || '시선'} / ${v.apparel_accents || '의복'}</div>
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
