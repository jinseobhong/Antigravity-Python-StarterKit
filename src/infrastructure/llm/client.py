# -*- coding: utf-8 -*-
"""
src/infrastructure/llm/client.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Infrastructure Layer: MultiLLMClient (Claude 3.7 & Gemini 3.6 Cascade Adapter)
- Claude Messages API & Gemini REST API 듀얼 캐스케이드 연동
- .env 환경변수 자동 로드 및 페일오버 지원
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
    """Claude 3.7 / Gemini 3.6 듀얼 LLM 클라이언트"""

    def __init__(self):
        load_env()
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.anthropic_model = os.getenv("ANTHROPIC_MODEL", "claude-3-7-sonnet-20250219")
        self.anthropic_workspace_id = os.getenv("ANTHROPIC_WORKSPACE_ID", "")
        self.primary_provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        """설정된 기본 프로바이더로 생성 후 오류 시 상호 페일오버"""
        if self.primary_provider == "claude" and self.anthropic_key:
            try:
                return self._call_claude(system_prompt, user_prompt, max_tokens)
            except Exception as e:
                print(f"[MultiLLMClient] Claude call failed: {e}. Cascading to Gemini...")
                if self.gemini_key:
                    return self._call_gemini(system_prompt, user_prompt, max_tokens)
                raise e
        else:
            if self.gemini_key:
                try:
                    return self._call_gemini(system_prompt, user_prompt, max_tokens)
                except Exception as e:
                    print(f"[MultiLLMClient] Gemini call failed: {e}. Cascading to Claude...")
                    if self.anthropic_key:
                        return self._call_claude(system_prompt, user_prompt, max_tokens)
                    raise e
            elif self.anthropic_key:
                return self._call_claude(system_prompt, user_prompt, max_tokens)
            else:
                raise ValueError("No valid API Key found in .env (GEMINI_API_KEY or ANTHROPIC_API_KEY required)")

    def _call_gemini(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        model = self.gemini_model if self.gemini_model != "gemini-2.5-flash" else "gemini-3.6-flash"
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
