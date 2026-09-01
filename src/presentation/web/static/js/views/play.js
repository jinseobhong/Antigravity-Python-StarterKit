/**
 * src/presentation/web/static/js/views/play.js
 * [View 2] 1:1 서사 롤플레이 룸, 대화 이력 및 마크다운 렌더러
 */

const PlayView = {
  render(character, stateData) {
    if (!character) return;

    // 상단 캐릭터 프로필
    const playName = document.getElementById('playCharName');
    if (playName) playName.innerText = character.name;

    const playTitle = document.getElementById('playCharTitle');
    if (playTitle) playTitle.innerText = `${character.title} • ${character.faction}`;

    const playArmor = document.getElementById('playCharArmor');
    if (playArmor) playArmor.innerText = character.armor_type;

    const playAvatar = document.getElementById('playCharAvatar');
    if (playAvatar) playAvatar.innerText = (character.name || '👑').charAt(0);

    // 채팅 로그 렌더링
    const box = document.getElementById('playChatBox');
    if (!box) return;

    if (!stateData.chat_history || stateData.chat_history.length === 0) {
      box.innerHTML = `
        <div class="p-5 rounded-2xl bg-gradient-to-br from-purple-950/40 to-pink-950/20 border border-purple-900/50 text-sm leading-relaxed prose-text shadow-lg">
          <p class="font-bold text-purple-300 mb-2 flex items-center gap-2">
            <i class="fa-solid fa-sparkles text-amber-400"></i> ${character.name}와(과)의 1:1 서사 롤플레이가 시작되었습니다.
          </p>
          <p class="text-gray-300">
            서늘한 대리석 기둥 사이로 차가운 바람이 스며듭니다. 그녀의 꼿꼿한 시선이 당신을 향합니다. 첫 행동을 취하십시오.
          </p>
        </div>
      `;
    } else {
      box.innerHTML = stateData.chat_history.map(msg => {
        if (msg.role === 'user') {
          return `
            <div class="flex justify-end mb-4">
              <div class="bg-gradient-to-r from-purple-900/80 to-pink-900/80 border border-purple-600/50 text-white rounded-2xl rounded-tr-none px-5 py-3 max-w-xl text-xs sm:text-sm shadow-xl leading-relaxed">
                <div class="font-extrabold text-amber-300 text-[10px] mb-1 uppercase tracking-wider">Player Action</div>
                ${msg.content}
              </div>
            </div>
          `;
        } else {
          const proseHtml = window.marked ? marked.parse(msg.content) : msg.content;
          return `
            <div class="flex justify-start mb-4">
              <div class="bg-gray-900/95 border border-gray-800 text-gray-200 rounded-2xl rounded-tl-none px-5 py-4 max-w-2xl text-xs sm:text-sm shadow-2xl prose-text leading-relaxed">
                <div class="font-extrabold text-pink-400 text-xs mb-1.5 flex items-center gap-1.5 border-b border-gray-800 pb-1">
                  <i class="fa-solid fa-crown text-[10px] text-amber-400"></i> ${character.name}
                </div>
                ${proseHtml}
              </div>
            </div>
          `;
        }
      }).join('');
      box.scrollTop = box.scrollHeight;
    }
  }
};

window.PlayView = PlayView;
