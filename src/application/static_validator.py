# -*- coding: utf-8 -*-
"""
src/application/static_validator.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Application Layer: Dify Node 11 기반 정적 산출물 린터 및 플레이스홀더 검증기
- [TODO], [TBD], 미완성, /* TODO */ 등의 미작성 마커 감지
- 최소 길이 및 마크다운 포맷 검증
"""

from __future__ import annotations
import re
from typing import Dict, Any, List


class StaticValidator:
    """정적 산출물 검증기"""

    PLACEHOLDER_PATTERNS = [
        r'\[\s*(?:TODO|TBD|미완성|추후작성)\s*\]',
        r'\b(?:TODO|TBD)\s*[:\-=_]',
        r'(?:추후\s*작성\s*예정|구현\s*예정|내용\s*추가\s*예정|내용\s*보완\s*예정)',
        r'/\*\s*(?:TODO|TBD)\s*\*/',
        r'<!--\s*(?:TODO|TBD)\s*-->'
    ]

    @classmethod
    def validate_master_prompt(cls, final_text: str, min_length: int = 500) -> Dict[str, Any]:
        """최종 마스터 시스템 프롬프트의 완결성 정적 검증"""
        if not final_text or len(final_text.strip()) < min_length:
            return {
                "is_valid": False,
                "error_code": "EMPTY_OR_TOO_SHORT",
                "message": f"최종 산출물이 너무 짧습니다 (최소 {min_length}자 필요, 현재 {len(final_text.strip())}자)."
            }

        found_markers: List[str] = []
        for pat in cls.PLACEHOLDER_PATTERNS:
            matches = re.findall(pat, final_text, re.IGNORECASE)
            if matches:
                found_markers.extend(matches)

        if found_markers:
            unique_markers = list(set(found_markers))
            return {
                "is_valid": False,
                "error_code": "INCOMPLETE_PLACEHOLDER_DETECTED",
                "message": f"미완성 플레이스홀더 패턴이 감지되었습니다: {', '.join(unique_markers)}"
            }

        clean_text = final_text.strip()
        if clean_text.startswith("```"):
            clean_text = re.sub(r"^```[a-zA-Z0-9_-]*\n?", "", clean_text)
            clean_text = re.sub(r"\n?```$", "", clean_text).strip()

        return {
            "is_valid": True,
            "error_code": "NONE",
            "message": "OK",
            "clean_text": clean_text
        }
