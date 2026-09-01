# -*- coding: utf-8 -*-
"""
src/application/action_parser_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
자연어 행동 지문 및 대사 분할, 7대 화행 및 17대 텐서 매핑 파서 서비스
"""

from __future__ import annotations
import re
from typing import List, Dict, Any, Tuple

from src.domain.action_frame import ActionFrame, ObservableEvent, SpeechAct, Segment
from src.domain.relational_vector import RelationalVector


class ActionParserService:
    """자연어 지문/대사 파서 서비스"""

    @staticmethod
    def parse_input(raw_text: str) -> ActionFrame:
        """사용자 입력 텍스트를 구조화된 ActionFrame으로 파싱"""
        clean_text = raw_text.strip()
        segments: List[Segment] = []

        # 1. 큰따옴표 대사("...") 및 지문 분할
        pattern = re.compile(r'["“]([^"”]+)["”]')
        last_idx = 0
        for match in pattern.finditer(clean_text):
            start, end = match.span()
            if start > last_idx:
                action_part = clean_text[last_idx:start].strip()
                if action_part:
                    segments.append(Segment(type="action", text=action_part))
            dialogue_part = match.group(1).strip()
            if dialogue_part:
                segments.append(Segment(type="dialogue", text=dialogue_part))
            last_idx = end
        if last_idx < len(clean_text):
            trailing_part = clean_text[last_idx:].strip()
            if trailing_part:
                segments.append(Segment(type="action", text=trailing_part))

        if not segments:
            segments.append(Segment(type="action", text=clean_text))

        # 2. 17대 신체 부위 텐서 키워드 매핑
        primary_tensor = "04_cervical"
        if any(w in clean_text for w in ["눈", "시선", "동공", "바라보", "쳐다"]):
            primary_tensor = "02_ocular"
        elif any(w in clean_text for w in ["목소리", "속삭", "말하", "소리", "숨"]):
            primary_tensor = "03_vocal"
        elif any(w in clean_text for w in ["목", "경추", "초커", "목덜미"]):
            primary_tensor = "04_cervical"
        elif any(w in clean_text for w in ["가슴", "흉곽", "심장", "어깨"]):
            primary_tensor = "06_thoracic"
        elif any(w in clean_text for w in ["옷", "단추", "의복", "지퍼", "솔기"]):
            primary_tensor = "09_sartorial"
        elif any(w in clean_text for w in ["손", "손목", "손가락", "악력", "잡"]):
            primary_tensor = "10_manual"
        elif any(w in clean_text for w in ["발", "다리", "무릎", "주저앉", "꺾"]):
            primary_tensor = "14_pedal"

        # 3. 7대 화행 및 관계역학 벡터 분류
        speech_act = SpeechAct.CONSOLATION
        dominant_vector = RelationalVector.DEVOTION_COMFORT
        intensity = 2.0

        if any(w in clean_text for w in ["위협", "명령", "굴복", "포기해", "닥쳐", "강압"]):
            speech_act = SpeechAct.INTIMIDATION
            dominant_vector = RelationalVector.SUBJUGATION
            intensity = 4.0
        elif any(w in clean_text for w in ["아름다", "예쁘", "경배", "찬미", "사랑"]):
            speech_act = SpeechAct.ADORATION
            dominant_vector = RelationalVector.DEVOTION_COMFORT
            intensity = 2.5
        elif any(w in clean_text for w in ["도발", "조롱", "웃기", "비웃"]):
            speech_act = SpeechAct.PROVOCATION
            dominant_vector = RelationalVector.SUSPENSION
            intensity = 3.0
        elif any(w in clean_text for w in ["애원", "부탁", "제발", "도와"]):
            speech_act = SpeechAct.ENTREATY
            dominant_vector = RelationalVector.SUBMISSION_FAWN
            intensity = 2.0
        elif any(w in clean_text for w in ["유혹", "손짓", "키스", "만지", "접촉"]):
            speech_act = SpeechAct.SEDUCTION
            dominant_vector = RelationalVector.SOMATIC_SYNC
            intensity = 3.5

        contact = any(w in clean_text for w in ["잡", "만지", "닿", "포옹", "누르", "감싸"])
        distance_change = "closer" if any(w in clean_text for w in ["다가", "접근", "가까이", "밀착"]) else "none"

        event = ObservableEvent(
            actor="player",
            target="character",
            action_verb="interact",
            body_targets=[primary_tensor],
            contact=contact,
            distance_change=distance_change,
            force="medium" if intensity >= 3.0 else "low"
        )

        return ActionFrame(
            raw_text=clean_text,
            segments=segments,
            event=event,
            primary_tensor=primary_tensor,
            dominant_vector=dominant_vector,
            speech_act=speech_act,
            intensity=intensity,
            predicted_deltas={
                "dominance": 0.3 if dominant_vector == RelationalVector.SUBJUGATION else 0.0,
                "vulnerability": 0.2 if intensity >= 3.0 else 0.0,
            }
        )
