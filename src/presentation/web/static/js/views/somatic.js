/**
 * src/presentation/web/static/js/views/somatic.js
 * 17대 생체 텐서, 압력 궤적, Kinematic Chain 실시간 게이지 렌더러
 */

const TENSOR_NAMES = {
  // 1. 코어 척추
  cervical_spine: '경추 신경 긴장도',
  thoracic_spine: '흉추 압박도',
  lumbar_spine: '요추 긴장성 만곡',
  pelvic_floor: '골반저 근막 이완도',
  // 2. 호흡/순환
  diaphragm: '횡격막 경련성 호흡',
  heart_rate_variability: '심박 변이도',
  respiratory_rate: '호흡수 상승률',
  subclavius_tension: '쇄골하근 열감 긴장',
  // 3. 자율신경/체온
  galvanic_skin_response: '표피 긴장성 발한',
  skin_temperature: '목덜미/뺨 표피 체온',
  pupil_dilation: '동공 확장/산동률',
  swallowing_reflex: '인두 연하 반사 억제',
  // 4. 운동/접지
  grounding_stability: '하지 지탱 접지력',
  trapezius_rigidity: '승모근 경직도',
  jaw_clenching: '교근/턱관절 악물림',
  // 5. 의복/구속
  corset_constriction: '코르셋 흉곽 압박',
  choker_tightness: '초커 경부 결착도'
};

const SomaticView = {
  render(character, stateData) {
    if (!character) return;

    // 1. 자아 내구도
    const ego = character.ego_durability !== undefined ? character.ego_durability : 100;
    const egoBar = document.getElementById('egoBar');
    if (egoBar) {
      egoBar.style.width = `${Math.max(0, Math.min(100, ego))}%`;
    }
    const egoVal = document.getElementById('egoVal');
    if (egoVal) egoVal.innerText = `${ego.toFixed(1)}%`;

    // 2. 압력 궤적 단계
    const stageEl = document.getElementById('pressureStage');
    if (stageEl) {
      stageEl.innerText = character.pressure_stage || 'Stage 1 (정렬 방어)';
    }

    // 3. 최근 운동 연쇄 이벤트
    const chainEl = document.getElementById('chainEvent');
    if (chainEl) {
      chainEl.innerText = stateData.recent_chain || '신체 운동 연쇄 안정';
    }

    // 4. 활성 스포트라이트 텐서 배지
    const tensorBox = document.getElementById('activeTensorsBox');
    if (tensorBox && character.tensors) {
      const active = character.tensors.active_spotlights || [];
      if (active.length === 0) {
        tensorBox.innerHTML = '<span class="text-[10px] text-gray-500">감지된 이상 텐서 없음</span>';
      } else {
        tensorBox.innerHTML = active.map(tKey => {
          const label = TENSOR_NAMES[tKey] || tKey;
          return `<span class="px-2 py-0.5 rounded bg-purple-950/80 border border-purple-600/50 text-purple-200 text-[10px] font-bold shadow-sm">⚡ ${label}</span>`;
        }).join(' ');
      }
    }
  }
};

window.SomaticView = SomaticView;
