/**
 * src/presentation/web/static/js/views/somatic.js
 * 3-Tier 신경·메모리 원장 및 신체 운동 연쇄 게이지 렌더러
 */

const SomaticView = {
  render(character, stateData) {
    if (!character) return;

    // 1. 공간 압력 상태
    const spaceEl = document.getElementById('spatialLayerBadge');
    if (spaceEl && character.spatial_pressure) {
      spaceEl.innerText = character.spatial_pressure.current_layer || 'Layer 1 (경계 공간)';
    }

    // 2. 운동 연쇄
    const chainEl = document.getElementById('chainEvent');
    if (chainEl && character.kinematic_chain) {
      chainEl.innerText = character.kinematic_chain.recent_chain_log || '신체 운동 연쇄 안정';
    }

    // 3. 3계층 원장 상태
    const ledger = character.somatic_ledger;
    if (ledger) {
      const l1 = document.getElementById('ledgerL1');
      if (l1) l1.innerText = ledger.layer_1_reflex?.spine_rigidity || '척추 긴장 안정';

      const l2 = document.getElementById('ledgerL2');
      if (l2) l2.innerText = ledger.layer_2_short_term?.sensory_hysteresis || '감각 잔향 안정';

      const l3 = document.getElementById('ledgerL3');
      if (l3) l3.innerText = ledger.layer_3_long_term?.relationship_inversion_rate || '0%';
    }
  }
};

window.SomaticView = SomaticView;
