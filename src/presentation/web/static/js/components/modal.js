/**
 * src/presentation/web/static/js/components/modal.js
 * 팝업 모달 관리자 (마스터 프롬프트, 단부루 태그, HITL 신규 발현 모달)
 */

let creationCache = null;

const ModalManager = {
  // 1. 마스터 헌법 모달
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
    alert('마스터 시스템 헌법이 클립보드에 복사되었습니다.');
  },

  // 2. 단부루 태그 모달
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
  },

  // 3. LLM API 키 설정 모달
  async openKeyModal() {
    try {
      const status = await ApiClient.getLlmStatus();
      document.getElementById('currentKeyInfo').innerText = `현재 상태: ${status.masked_key} (${status.model})`;
      document.getElementById('keyModal').classList.remove('hidden');
    } catch (err) {
      alert('LLM 상태 확인 실패: ' + err);
    }
  },

  closeKeyModal() {
    document.getElementById('keyModal').classList.add('hidden');
  },

  async saveApiKey() {
    const key = document.getElementById('inputApiKey').value.trim();
    if (!key) {
      alert('API 키를 입력해 주세요.');
      return;
    }
    try {
      await ApiClient.configLlm(key);
      alert('✨ Gemini / Claude API 키가 성공적으로 연동 및 .env에 저장되었습니다!');
      this.closeKeyModal();
      App.checkLlmStatus();
    } catch (err) {
      alert('API 키 저장 실패: ' + err);
    }
  },

  // 4. HITL 다단계 캐릭터 생성 모달
  openCreationModal() {
    creationCache = null;
    document.getElementById('createStep1').classList.remove('hidden');
    document.getElementById('createStep2').classList.add('hidden');
    document.getElementById('createLoading').classList.add('hidden');
    document.getElementById('createInputIntent').value = '';
    document.getElementById('createInputName').value = '';
    document.getElementById('createInputTitle').value = '';
    document.getElementById('creationModal').classList.remove('hidden');
  },

  closeCreationModal() {
    document.getElementById('creationModal').classList.add('hidden');
  },

  backToStep1() {
    document.getElementById('createStep1').classList.remove('hidden');
    document.getElementById('createStep2').classList.add('hidden');
    document.getElementById('createLoading').classList.add('hidden');
  },

  async submitCreationStep1() {
    const intent = document.getElementById('createInputIntent').value.trim();
    if (!intent) {
      alert('캐릭터의 컨셉이나 설정을 입력해 주세요.');
      return;
    }

    const name = document.getElementById('createInputName').value.trim();
    const title = document.getElementById('createInputTitle').value.trim() || '고위 귀족';

    document.getElementById('createStep1').classList.add('hidden');
    document.getElementById('createLoading').classList.remove('hidden');
    document.getElementById('createLoadingText').innerText = '⏳ [1단계] 제약 조건(Hard Invariants) 역산 및 2대 서사 궤적 분석 중...';

    try {
      const fullQuery = name ? `${name} - ${intent}` : intent;
      const res = await ApiClient.classifyAndPropose(fullQuery);
      creationCache = {
        name: name || res.target_name || '새 캐릭터',
        title: title,
        faction: '독립 세력',
        seed_hash: res.seed_hash,
        hard_invariants: res.hard_invariants,
        vectors: res.resolution_vectors
      };

      // Checkpoint 1 뷰 세팅
      document.getElementById('createResSeed').innerText = res.seed_hash;
      document.getElementById('createResBoundary').innerText = res.hard_invariants.primary_boundary;
      document.getElementById('createResTrigger').innerText = res.hard_invariants.ego_collapse_trigger;
      document.getElementById('createResHeel').innerText = res.hard_invariants.somatic_achilles_heel;

      const v1 = res.resolution_vectors[0] || {};
      const v2 = res.resolution_vectors[1] || {};

      document.getElementById('createV1Title').innerText = v1.vector_name || '1안: 저항 궤적';
      document.getElementById('createV1Desc').innerText = v1.axis_description || '';

      document.getElementById('createV2Title').innerText = v2.vector_name || '2안: 붕괴 궤적';
      document.getElementById('createV2Desc').innerText = v2.axis_description || '';

      document.getElementById('createLoading').classList.add('hidden');
      document.getElementById('createStep2').classList.remove('hidden');
    } catch (err) {
      alert('제약선 역산 실패: ' + err);
      this.backToStep1();
    }
  },

  async selectVectorAndSynthesize(vectorId) {
    if (!creationCache) return;

    const selectedV = creationCache.vectors.find(v => v.vector_id === vectorId) || creationCache.vectors[0];

    document.getElementById('createStep2').classList.add('hidden');
    document.getElementById('createLoading').classList.remove('hidden');
    document.getElementById('createLoadingText').innerText = `⏳ [2단계] [${vectorId}] 궤적으로부터 8-Tier Visual DNA 및 70단계 유전자 합성 중...`;

    try {
      const payload = {
        name: creationCache.name,
        title: creationCache.title,
        faction: creationCache.faction,
        seed_hash: creationCache.seed_hash,
        hard_invariants: creationCache.hard_invariants,
        selected_vector: selectedV
      };

      await ApiClient.synthesizeCharacter(payload);
      await App.refreshCharacters();
      await App.refreshState();

      this.closeCreationModal();
      alert(`✨ [${creationCache.name}] (${creationCache.seed_hash}) 캐릭터가 성공적으로 발현되었습니다!`);
      App.switchView('LOBBY');
    } catch (err) {
      alert('캐릭터 합성 실패: ' + err);
      this.backToStep1();
    }
  }
};

window.ModalManager = ModalManager;
