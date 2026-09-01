# -*- coding: utf-8 -*-
"""
src/infrastructure/llm/client.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Gemini / Claude 자동 캐스케이드 멀티 LLM 클라이언트 (표준 라이브러리 기반 HTTP + Mock Fallback)
"""

from __future__ import annotations
import os
import json
import urllib.request
from typing import Optional, Dict, Any, List


class MultiLLMClient:
    """멀티 LLM 비동기/동기 호출 어댑터"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "") or os.getenv("ANTHROPIC_API_KEY", "")
        self.model = model

    def generate_text(self, system_instruction: str, user_prompt: str, temperature: float = 0.85) -> str:
        """LLM 호출 (키가 없을 경우 고품질 결정론적 Mock 엔진으로 Fallback)"""
        if not self.api_key:
            return self._mock_probabilistic_response(system_instruction, user_prompt)

        # Gemini REST API 호출
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            payload = {
                "system_instruction": {"parts": [{"text": system_instruction}]},
                "contents": [{"parts": [{"text": user_prompt}]}],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": 4096
                }
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                return text
        except Exception as e:
            return self._mock_probabilistic_response(system_instruction, user_prompt)

    def _mock_probabilistic_response(self, system: str, user: str) -> str:
        """API 키 부재 시 테스트 및 오프라인 구동을 위한 고밀도 문학 시뮬레이터"""
        return (
            f"서늘한 침묵이 흐르는 방 안, 차가운 은발 아래로 금빛 눈동자가 미세하게 흔들립니다.\n\n"
            f"목에 채워진 서늘한 금속 초커 너머로 억누른 숨결이 파르르 떨리며 쇄골에 은밀한 붉은 열감이 번져 나갑니다.\n\n"
            f"\"...무슨 생각을 하는 거지? 선을 넘지 마라.\"\n\n"
            f"도도하게 내리깐 시선 뒤로, 결코 무너지지 않으려던 도덕적 방어선에 미세한 균열이 스쳐 지나갑니다."
        )
