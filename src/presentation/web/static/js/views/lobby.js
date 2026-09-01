/**
 * src/presentation/web/static/js/views/lobby.js
 * [View 1] 메인 로비 허브 & 액티브 캐릭터 스포트라이트 액자 뷰
 */

const LobbyView = {
  render(character, stateData) {
    if (!character) return;

    // 시드 및 기본 정보
    const seedEl = document.getElementById('hubCharSeed');
    if (seedEl) seedEl.innerText = character.seed_hash || '#SEED';

    const nameEl = document.getElementById('hubCharName');
    if (nameEl) nameEl.innerText = character.name || '알 수 없음';

    const titleEl = document.getElementById('hubCharTitle');
    if (titleEl) titleEl.innerText = `${character.title || ''} • ${character.faction || ''}`;

    const armorEl = document.getElementById('hubCharArmor');
    if (armorEl) armorEl.innerText = character.armor_type || '';

    // 특성 미리보기
    const traitsEl = document.getElementById('hubCharTraits');
    if (traitsEl && character.traits) {
      const traitHtml = Object.entries(character.traits).map(([k, v]) => `
        <div class="text-[11px] text-gray-300">
          <span class="text-purple-400 font-bold">• ${k}:</span> ${v}
        </div>
      `).join('');
      traitsEl.innerHTML = traitHtml || '<span class="text-xs text-gray-500">설정된 특성 없음</span>';
    }

    // 초상화 액자
    const imgEl = document.getElementById('hubCharImg');
    const placeholderEl = document.getElementById('hubCharPlaceholder');
    if (character.image_url && character.image_url.trim()) {
      if (imgEl) {
        imgEl.src = character.image_url;
        imgEl.classList.remove('hidden');
      }
      if (placeholderEl) placeholderEl.classList.add('hidden');
    } else {
      if (imgEl) imgEl.classList.add('hidden');
      if (placeholderEl) {
        placeholderEl.classList.remove('hidden');
        placeholderEl.innerText = (character.name || '👑').charAt(0);
      }
    }
  }
};

window.LobbyView = LobbyView;
