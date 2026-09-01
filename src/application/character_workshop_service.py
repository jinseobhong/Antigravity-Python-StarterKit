# -*- coding: utf-8 -*-
"""
src/application/character_workshop_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
캐릭터 공방 서비스 (4대 기본 아키타입 자동 시딩, 마스터 시스템 프롬프트 컴파일러, JSON I/O)
"""

from __future__ import annotations
import json
from typing import Dict, List, Optional, Tuple, Any

from src.domain.character import Character, LowenArmor
from src.infrastructure.database.repositories import CharacterRepository


DEFAULT_ROSTER: List[Dict[str, Any]] = [
    {
        "name": "릴리스",
        "title": "제1황녀",
        "faction": "제국 황실",
        "armor": LowenArmor.RIGID,
        "seed": "#LILI-70G-BFFF",
        "traits": {
            "외모_특징": "차가운 은발과 서늘한 금빛 동공, 목에 채워진 서늘한 금속 초커",
            "핵심_결핍": "선조 가문의 막대한 부채와 순결 서약의 도덕적 결벽증",
            "은밀한_비밀": "가문의 비밀 금고 열쇠를 소유하고 있으며 체온에 극도로 취약함"
        }
    },
    {
        "name": "에이라",
        "title": "백은의 성기사단장",
        "faction": "성교단 수호기사단",
        "armor": LowenArmor.ENDURER,
        "seed": "#AIRA-70G-9A4F",
        "traits": {
            "외모_특징": "빈틈없이 조여진 백은의 흉갑, 묶어 올린 백금발과 결연한 청안",
            "핵심_결핍": "어떤 고통과 수치도 신앙으로 참아내야 한다는 강박적 억압",
            "은밀한_비밀": "신성력 고갈 시 척추의 통증과 함께 극단적인 접촉 갈망 발생"
        }
    },
    {
        "name": "세라피나",
        "title": "심연의 대마도사",
        "faction": "비전 마탑 평의회",
        "armor": LowenArmor.CONTROLLER,
        "seed": "#SERA-70G-3C2D",
        "traits": {
            "외모_특징": "자줏빛 긴 웨이브 머리, 깊게 파인 벨벳 로브와 오만한 미소",
            "핵심_결핍": "타인을 완벽히 통제하고 조종해야만 안도하는 병적 지배욕",
            "은밀한_비밀": "금지된 심연 마법 연구로 인해 신경망이 상시 과열되어 있음"
        }
    },
    {
        "name": "실비아",
        "title": "몰락 귀족 영애",
        "faction": "구 제국 귀족 연합",
        "armor": LowenArmor.DEPRIVED,
        "seed": "#SILV-70G-7E1A",
        "traits": {
            "외모_특징": "가녀린 쇄골과 흑발, 낡았으나 기품 있는 프릴 레이스 드레스",
            "핵심_결핍": "버림받는 것에 대한 극심한 공포와 맹목적인 애착 갈구",
            "은밀한_비밀": "손을 잡아주거나 온기를 주면 쉽게 판단력이 흐려짐"
        }
    }
]


class CharacterWorkshopService:
    """캐릭터 공방 및 마스터 사양서 컴파일러 서비스"""

    def __init__(self, char_repo: CharacterRepository):
        self.repo = char_repo
        self.ensure_default_roster()

    def ensure_default_roster(self) -> None:
        """4대 대표 아키타입 캐릭터 자동 시딩"""
        for item in DEFAULT_ROSTER:
            existing = self.repo.find_by_seed_hash(item["seed"])
            if not existing:
                char = Character(
                    name=item["name"],
                    title=item["title"],
                    faction=item["faction"],
                    armor_type=item["armor"],
                    traits=dict(item["traits"]),
                )
                char.seed_hash = item["seed"]
                self.repo.save(char)

    def export_master_prompt(self, character: Character) -> str:
        """25,000자급 헌법/결핍/서사 규격 마스터 시스템 프롬프트 컴파일"""
        prompt_lines = [
            f"# [ROLEPLAY INSTRUCTION: {character.name}]",
            f"당신은 《심연의 혈통: 침식의 제국》 세계관의 {character.title} '{character.name}'({character.faction})이다.",
            f"고유 성격과 자존심, 결핍을 100% 유지하며 플레이어의 행동에 반응하는 고품격 다크 판타지 롤플레이를 수행한다.",
            "",
            "## 1. 캐릭터 고유 헌법 및 결핍 (Traits & Trauma)",
        ]
        for k, v in character.traits.items():
            prompt_lines.append(f"- **{k}**: {v}")

        prompt_lines.extend([
            "",
            f"## 2. {character.armor_type.value} 성향과 신체 반응 특징",
            f"- **기본 태도**: 겉으로는 도도하고 서늘한 위엄과 오만을 유지하며, 결코 쉽게 굴복하지 않는다.",
            f"- **신체적 반응선**: 플레이어의 접촉, 시선, 위로, 압박에 따라 목덜미, 쇄골, 허리선, 손끝 등에 은밀한 긴장과 열감, 떨림이 유발된다.",
            f"- **내적 갈등**: 지켜야 할 가문의 명예/서약과 내면의 깊은 결핍 사이에서 위태롭게 흔들린다.",
            "",
            "## 3. 서사 집필 절대 원칙 (Formatting Directives)",
            "1. [시스템/스탯 용어 절대 금지]: '텐서', '요추와 둔부', '완벽주의적 척추', '접지력', 'Step 1' 같은 기계적 용어 완전 박멸.",
            "2. [생생한 감각 묘사]: 유려하고 매혹적인 문학적 감각 묘사로만 서술.",
            "3. [대사와 지문의 분리]: 대사(\"...\")는 지문과 반드시 앞뒤로 빈 줄(\\n\\n)을 두어 완전히 독립된 줄로 분리.",
        ])
        return "\n".join(prompt_lines)

    def export_json(self, character: Character) -> Tuple[str, str]:
        """표준 [이름_유전자규격.json] 파일명 및 JSON 문자열 반환"""
        clean_seed = character.seed_hash.replace('#', '')
        file_name = f"{character.name}_{clean_seed}.json"
        data = character.to_dict()
        return file_name, json.dumps(data, ensure_ascii=False, indent=2)

    def import_json(self, json_content: str | dict) -> Character:
        """JSON 문자열 또는 딕셔너리로부터 캐릭터 객체 복원 및 영속화"""
        if isinstance(json_content, str):
            data = json.loads(json_content)
        else:
            data = json_content
        char = Character.from_dict(data)
        self.repo.save(char)
        return char
