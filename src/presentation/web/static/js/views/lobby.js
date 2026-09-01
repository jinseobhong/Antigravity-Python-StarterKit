/**
 * src/presentation/web/static/js/views/lobby.js
 * [View 1] 메인 로비 허브 & 8-Tier Visual DNA 전신 액자 뷰
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

    // 8-Tier Visual DNA 렌더링
    const v = character.visual_dna;
    const vBox = document.getElementById('hubVisualDnaBox');
    if (vBox && v) {
      vBox.innerHTML = `
        <div class="space-y-1.5 text-[11px] text-gray-300">
          <div><span class="text-purple-400 font-bold">• 안면 골격:</span> ${v.face_geometry}</div>
          <div><span class="text-pink-400 font-bold">• 동공 광학:</span> ${v.ocular_optics}</div>
          <div><span class="text-amber-400 font-bold">• 모발 물리:</span> ${v.hair_physics}</div>
          <div><span class="text-emerald-400 font-bold">• 의복/초커:</span> ${v.apparel_accents}</div>
          <div><span class="text-cyan-400 font-bold">• 생체 홍조:</span> ${v.somatic_flush_cue}</div>
        </div>
      `;
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
