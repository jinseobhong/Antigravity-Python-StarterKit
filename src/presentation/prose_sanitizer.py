# -*- coding: utf-8 -*-
"""
src/presentation/prose_sanitizer.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
최종 문학 서사 정제기 (시스템 태그 완전 박멸 및 대사 단독 줄바꿈 서식화)
"""

from __future__ import annotations
import re


class ProseSanitizer:
    """서사 출력물 정제 및 서식 포맷팅 유틸리티"""

    @classmethod
    def sanitize(cls, raw_out: str) -> str:
        """기계적 시스템 태그 및 스탯 단어 완전 소멸, 대사(\"... \") 독립 줄 분리"""
        if not raw_out:
            return ""

        text = raw_out
        if "[NARRATIVE]" in text:
            text = text.split("[NARRATIVE]")[-1]
        if "[NARRATIVE PROSE]" in text:
            text = text.split("[NARRATIVE PROSE]")[-1]
        if "[CUMULATIVE NEURAL" in text:
            text = text.split("[CUMULATIVE NEURAL")[0]

        # 1. 모든 형태의 시스템 태그, 스탯 단어, 대괄호 박멸
        text = re.sub(r'\[\s*(?:SOM_[A-Z0-9_]+|[0-9]{1,2}_[a-zA-Z0-9_]+|STATUS|UNIV|KIN)?[^\]]*\]', '', text)
        text = re.sub(r'SOM_[A-Z0-9_]+(?:\s*의\s*(?:법칙|생체\s*반사|원리|연쇄|에\s*따라)?)?', '', text)
        text = re.sub(r'\[\s*\]', '', text)
        text = re.sub(r'\s*\([^)]*(?:Stage\s*\d|\d+\s*Nm|산대|연하음|강직|호흡폭발|피부열|발한|\/)[^)]*\)', '', text)
        text = re.sub(r'Step\s*\d+에서\s*전이된\s*자극은\s*', '신체에 전이된 긴장감은 ', text)
        text = re.sub(r'Step\s*\d+[:\s]*', '', text)

        # 2. 기계적 명칭 문학적 치환
        text = re.sub(r'에고의?\s*자아\s*내구도(?:가|는|를|의)?', '내면의 자존심이', text)
        text = re.sub(r'자아\s*내구도(?:가|는|를|의)?', '자존심이', text)
        text = re.sub(r'신경\s*오염도(?:가|는|를|의)?', '감각의 붕괴가', text)
        text = re.sub(r'완벽주의적\s*척추(?:\s*방어)?(?:\s*자세)?(?:가|는|를|의|인)?', '도도하게 꼿꼿한 허리와 등줄기가', text)

        # 3. 대사("...") 및 큰따옴표 블록을 독립된 문단으로 분리 (\n\n"..."\n\n)
        def quote_repl(m):
            q = m.group(0).strip()
            q_clean = re.sub(r'\s*\n+\s*', ' ', q)
            return f"\n\n{q_clean}\n\n"

        text = re.sub(r'["“][^"”]+["”]', quote_repl, text)

        # 4. 다중 공백 및 다중 개행 정리
        text = re.sub(r'[ \t]{2,}', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text).strip()

        return text
