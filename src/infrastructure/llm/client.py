# -*- coding: utf-8 -*-
"""
src/infrastructure/llm/client.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Infrastructure Layer: MultiLLMClient (Multi-Model Adaptive Cascade Adapter)
- Google Gemini (gemini-flash-lite-latest, gemini-2.5-flash-lite, gemini-flash-latest, etc.) 
- Anthropic Claude (claude-3-7-sonnet-20250219)
- Quota (429) & Model Availability (404) 자동 감지 및 스마트 캐스케이드
"""

from __future__ import annotations
import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional, List


def load_env() -> None:
    """루트 .env 로드"""
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    env_path = base_dir / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip("'\"")


class MultiLLMClient:
    """Gemini / Claude 멀티 모델 지능형 캐스케이드 클라이언트"""

    # 가용 쿼터 자동 탐색용 Gemini 모델 우선순위 풀
    GEMINI_FALLBACK_MODELS = [
        "gemini-flash-lite-latest",
        "gemini-2.5-flash-lite",
        "gemini-flash-latest",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-3.6-flash"
    ]

    def __init__(self):
        load_env()
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.anthropic_model = os.getenv("ANTHROPIC_MODEL", "claude-3-7-sonnet-20250219")
        self.anthropic_workspace_id = os.getenv("ANTHROPIC_WORKSPACE_ID", "")
        self.primary_provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        """설정된 기본 프로바이더로 생성 후 쿼터/오류 시 모델 풀 및 프로바이더 자동 페일오버"""
        if self.primary_provider == "claude" and self.anthropic_key:
            try:
                return self._call_claude(system_prompt, user_prompt, max_tokens)
            except Exception as e:
                print(f"[MultiLLMClient] Claude call failed: {e}. Cascading to Gemini...")
                if self.gemini_key:
                    return self._call_gemini_with_cascade(system_prompt, user_prompt, max_tokens)
                raise e
        else:
            if self.gemini_key:
                try:
                    return self._call_gemini_with_cascade(system_prompt, user_prompt, max_tokens)
                except Exception as e:
                    print(f"[MultiLLMClient] Gemini cascade failed: {e}. Cascading to Claude...")
                    if self.anthropic_key:
                        return self._call_claude(system_prompt, user_prompt, max_tokens)
                    raise e
            elif self.anthropic_key:
                return self._call_claude(system_prompt, user_prompt, max_tokens)
            else:
                raise ValueError("No valid API Key found in .env (GEMINI_API_KEY or ANTHROPIC_API_KEY required)")

    def _call_gemini_with_cascade(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        """지정 모델 우선 시도 후 429/404 발생 시 대체 모델 풀 순차 회전"""
        models_to_try = [self.gemini_model] + [m for m in self.GEMINI_FALLBACK_MODELS if m != self.gemini_model]
        last_error = None

        for model in models_to_try:
            try:
                result = self._call_gemini_single(model, system_prompt, user_prompt, max_tokens)
                if result:
                    # 성공한 활성 모델로 업데이트
                    self.gemini_model = model
                    return result
            except urllib.error.HTTPError as e:
                last_error = e
                # 429 (Quota) 또는 404 (Model not found) 발생 시 다음 모델 시도
                if e.code in (404, 429, 400):
                    continue
                raise e
            except Exception as e:
                last_error = e
                continue

        if last_error:
            raise last_error
        raise RuntimeError("All Gemini models in cascade failed to generate content.")

    def _call_gemini_single(self, model: str, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.gemini_key}"
        
        payload = {
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_prompt}]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.85
            }
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        
        with urllib.request.urlopen(req, timeout=60) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            candidates = res_json.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
            return ""

    def _call_claude(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.anthropic_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        if self.anthropic_workspace_id:
            headers["anthropic-workspace-id"] = self.anthropic_workspace_id

        payload = {
            "model": self.anthropic_model,
            "system": system_prompt,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.85
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers)

        with urllib.request.urlopen(req, timeout=60) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            content_blocks = res_json.get("content", [])
            if content_blocks:
                return content_blocks[0].get("text", "").strip()
            return ""
