# -*- coding: utf-8 -*-
"""
src/infrastructure/llm/config.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
중앙 멀티 LLM 환경변수 및 모델 풀 설정 관리자
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Dict, Any, List


GEMINI_MODEL_CASCADE: List[str] = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]

CLAUDE_MODEL_CASCADE: List[str] = [
    "claude-3-7-sonnet-20250219",
    "claude-3-5-sonnet-20241022",
    "claude-3-opus-20240229",
    "claude-3-5-haiku-20241022",
    "claude-3-haiku-20240307",
]


class LLMConfig:
    """LLM 설정 캡슐화 객체"""

    def __init__(
        self,
        gemini_api_key: str = "",
        claude_api_key: str = "",
        provider: str = "gemini",
        gemini_model: str = "gemini-3.6-flash",
        claude_model: str = "claude-3-7-sonnet-20250219",
    ):
        self.gemini_api_key = gemini_api_key or os.environ.get("GEMINI_API_KEY", "") or os.environ.get("GOOGLE_API_KEY", "")
        self.claude_api_key = claude_api_key or os.environ.get("ANTHROPIC_API_KEY", "") or os.environ.get("CLAUDE_API_KEY", "")
        self.provider = provider.lower()
        self.gemini_model = gemini_model
        self.claude_model = claude_model

    @classmethod
    def load_from_env(cls, env_path: Optional[str] = None) -> LLMConfig:
        """환경변수 및 파일로부터 설정 로드"""
        cfg = cls()
        if env_path and os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip().strip('"').strip("'")
                        if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
                            cfg.gemini_api_key = v
                        elif k in ("ANTHROPIC_API_KEY", "CLAUDE_API_KEY"):
                            cfg.claude_api_key = v
                        elif k == "LLM_PROVIDER":
                            cfg.provider = v.lower()
                        elif k == "GEMINI_MODEL":
                            cfg.gemini_model = v
                        elif k == "ANTHROPIC_MODEL":
                            cfg.claude_model = v
        return cfg
