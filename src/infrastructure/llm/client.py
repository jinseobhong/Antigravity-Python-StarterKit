# -*- coding: utf-8 -*-
"""
src/infrastructure/llm/client.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Gemini ➔ Claude 멀티 프로바이더 캐스케이드 & 자동 스왑 탄력성 클라이언트
"""

from __future__ import annotations
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List

from .config import LLMConfig, GEMINI_MODEL_CASCADE, CLAUDE_MODEL_CASCADE


class UniversalLLMClient:
    """429 Quota Exceeded 및 에러 발생 시 자동 스왑을 지원하는 탄력적 멀티 LLM 클라이언트"""

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig.load_from_env()

    def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 2048, temperature: float = 0.85) -> Optional[str]:
        """주 제공자 호출 ➔ 실패 시 보조 제공자 및 모델 풀 순차 자동 스왑"""
        # 1. Gemini 시도
        if self.config.gemini_api_key:
            for model_name in GEMINI_MODEL_CASCADE:
                try:
                    res = self._call_gemini(model_name, system_prompt, user_prompt, max_tokens, temperature)
                    if res:
                        return res
                except Exception as e:
                    # 429 또는 에러 시 다음 모델로 캐스케이드
                    continue

        # 2. Claude 크로스-프로바이더 폴백 시도
        if self.config.claude_api_key:
            for model_name in CLAUDE_MODEL_CASCADE:
                try:
                    res = self._call_claude(model_name, system_prompt, user_prompt, max_tokens, temperature)
                    if res:
                        return res
                except Exception as e:
                    continue

        return None

    def _call_gemini(self, model: str, system_prompt: str, user_prompt: str, max_tokens: int, temperature: float) -> Optional[str]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.config.gemini_api_key}"
        payload = {
            "contents": [{"parts": [{"text": user_prompt}]}],
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]

    def _call_claude(self, model: str, system_prompt: str, user_prompt: str, max_tokens: int, temperature: float) -> Optional[str]:
        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.config.claude_api_key,
                "anthropic-version": "2023-06-01"
            }
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"]
