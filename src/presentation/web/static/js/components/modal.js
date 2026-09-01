/**
 * src/presentation/web/static/js/components/modal.js
 * 팝업 모달 관리자 (마스터 프롬프트, 단부루 태그)
 */

const ModalManager = {
  async openPromptModal() {
    try {
      const data = await ApiClient.exportPrompt();
      document.getElementById('promptModalText').value = data.prompt || '';
      document.getElementById('promptModal').classList.remove('hidden');
    } catch (err) {
      alert('프롬프트 로드 실패: ' + err);
    }
  },

  closePromptModal() {
    document.getElementById('promptModal').classList.add('hidden');
  },

  copyPrompt() {
    const el = document.getElementById('promptModalText');
    el.select();
    document.execCommand('copy');
    alert('마스터 시스템 프롬프트가 클립보드에 복사되었습니다.');
  },

  async openDanbooruModal() {
    try {
      const data = await ApiClient.generateDanbooru();
      document.getElementById('danbooruPos').value = data.positive || '';
      document.getElementById('danbooruNeg').value = data.negative || '';
      document.getElementById('danbooruModal').classList.remove('hidden');
    } catch (err) {
      alert('단부루 태그 생성 실패: ' + err);
    }
  },

  closeDanbooruModal() {
    document.getElementById('danbooruModal').classList.add('hidden');
  },

  copyDanbooru(type) {
    const el = document.getElementById(type === 'pos' ? 'danbooruPos' : 'danbooruNeg');
    el.select();
    document.execCommand('copy');
    alert(`${type === 'pos' ? 'Positive' : 'Negative'} 태그가 복사되었습니다.`);
  }
};

window.ModalManager = ModalManager;
