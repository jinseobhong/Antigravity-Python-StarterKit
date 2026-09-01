/**
 * src/presentation/web/static/js/app.js
 * 메인 애플리케이션 라이프사이클 & 3대 뷰 라우팅 매니저
 */

const App = {
  currentView: 'LOBBY',
  currentState: null,

  async init() {
    await this.refreshState();
    await this.refreshCharacters();
  },

  async refreshState() {
    try {
      this.currentState = await ApiClient.getState();
      this.render();
    } catch (err) {
      console.error('App.refreshState error:', err);
    }
  },

  async refreshCharacters() {
    try {
      const chars = await ApiClient.getCharacters();
      VaultView.setCharacters(chars);
    } catch (err) {
      console.error('App.refreshCharacters error:', err);
    }
  },

  render() {
    if (!this.currentState) return;
    const char = this.currentState.character;

    LobbyView.render(char, this.currentState);
    PlayView.render(char, this.currentState);
    SomaticView.render(char, this.currentState);
  },

  switchView(viewName) {
    this.currentView = viewName;
    const viewLobby = document.getElementById('viewLobby');
    const viewPlay = document.getElementById('viewPlay');
    const viewVault = document.getElementById('viewVault');

    const navLobby = document.getElementById('navLobby');
    const navPlay = document.getElementById('navPlay');
    const navVault = document.getElementById('navVault');

    // 모든 뷰 숨김
    [viewLobby, viewPlay, viewVault].forEach(el => el?.classList.add('hidden'));

    // 탭 스타일 초기화
    [navLobby, navPlay, navVault].forEach(btn => {
      if (btn) btn.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-gray-900/80 text-gray-400 hover:text-white hover:bg-gray-800 transition flex items-center gap-1.5';
    });

    if (viewName === 'LOBBY') {
      viewLobby?.classList.remove('hidden');
      if (navLobby) navLobby.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-purple-600 text-white shadow transition flex items-center gap-1.5';
    } else if (viewName === 'PLAY') {
      viewPlay?.classList.remove('hidden');
      if (navPlay) navPlay.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-purple-600 text-white shadow transition flex items-center gap-1.5';
    } else if (viewName === 'VAULT') {
      viewVault?.classList.remove('hidden');
      if (navVault) navVault.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-purple-600 text-white shadow transition flex items-center gap-1.5';
      this.refreshCharacters();
    }
  },

  async selectCharacter(seedHash, goToPlay = false) {
    try {
      this.currentState = await ApiClient.selectCharacter(seedHash);
      this.render();
      if (goToPlay) {
        this.switchView('PLAY');
      } else {
        this.switchView('LOBBY');
      }
    } catch (err) {
      alert('캐릭터 선택 실패: ' + err);
    }
  },

  async sendAction(customText, vectorType) {
    const input = document.getElementById('actionInput');
    const text = (customText || input?.value || '').trim();
    if (!text) return;

    if (input) input.value = '';
    try {
      this.currentState = await ApiClient.sendAction(text, vectorType || 'SUBJUGATION');
      this.render();
    } catch (err) {
      alert('턴 진행 실패: ' + err);
    }
  },

  async triggerUndo() {
    try {
      this.currentState = await ApiClient.undo();
      this.render();
    } catch (err) {
      alert('되돌리기 실패: ' + err);
    }
  },

  async triggerReset() {
    if (!confirm('세션을 1턴으로 초기화하시겠습니까?')) return;
    try {
      this.currentState = await ApiClient.reset();
      this.render();
    } catch (err) {
      alert('초기화 실패: ' + err);
    }
  }
};

window.App = App;

// 페이지 로드 시 즉시 부트스트랩
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
