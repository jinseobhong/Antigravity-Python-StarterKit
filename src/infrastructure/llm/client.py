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


def load_local_env(filepath: str = ".env") -> None:
    """순수 파이썬 의존성 제로 .env 파일 로더"""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'").strip('"')
                        if k and v:
                            os.environ[k] = v
        except Exception:
            pass


load_local_env()


class MultiLLMClient:
    """Gemini / Claude 자동 캐스케이드 멀티 LLM 클라이언트"""

    def __init__(
        self,
        gemini_key: Optional[str] = None,
        claude_key: Optional[str] = None,
        active_provider: Optional[str] = None,
        gemini_model: Optional[str] = None,
        claude_model: Optional[str] = None
    ):
        load_local_env()
        self.gemini_key = gemini_key or os.getenv("GEMINI_API_KEY", "")
        self.claude_key = claude_key or os.getenv("ANTHROPIC_API_KEY", "") or os.getenv("CLAUDE_API_KEY", "")
        
        # 환경변수 LLM_PROVIDER / ACTIVE_LLM_PROVIDER 지원 (대소문자 무관)
        raw_prov = (active_provider or os.getenv("LLM_PROVIDER", "") or os.getenv("ACTIVE_LLM_PROVIDER", "CLAUDE")).strip().upper()
        self.active_provider = "CLAUDE" if "CLAUDE" in raw_prov else "GEMINI"

        self.gemini_model = gemini_model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.claude_model = claude_model or os.getenv("ANTHROPIC_MODEL", "claude-3-7-sonnet-20250219")
        self.hf_token = os.getenv("HF_TOKEN", "")

    @property
    def api_key(self) -> str:
        if self.active_provider == "CLAUDE":
            return self.claude_key or self.gemini_key
        return self.gemini_key or self.claude_key

    @property
    def model(self) -> str:
        if self.active_provider == "CLAUDE":
            return self.claude_model
        return self.gemini_model

    def set_keys_and_provider(self, gemini_key: str = "", claude_key: str = "", provider: str = "CLAUDE") -> None:
        if gemini_key.strip():
            self.gemini_key = gemini_key.strip()
            os.environ["GEMINI_API_KEY"] = self.gemini_key
        if claude_key.strip():
            self.claude_key = claude_key.strip()
            os.environ["ANTHROPIC_API_KEY"] = self.claude_key

        if provider.upper() in ["GEMINI", "CLAUDE"]:
            self.active_provider = provider.upper()

        # .env 파일에 영구 동기화
        try:
            with open(".env", "w", encoding="utf-8") as f:
                f.write(f"GEMINI_API_KEY={self.gemini_key}\n")
                f.write(f"GEMINI_MODEL={self.gemini_model}\n")
                f.write(f"ANTHROPIC_API_KEY={self.claude_key}\n")
                f.write(f"ANTHROPIC_MODEL={self.claude_model}\n")
                f.write(f"LLM_PROVIDER={self.active_provider.lower()}\n")
                if self.hf_token:
                    f.write(f"HF_TOKEN={self.hf_token}\n")
        except Exception:
            pass

    def generate_text(self, system_instruction: str, user_prompt: str, temperature: float = 0.85) -> str:
        """선택된 프로바이더로 호출하고 장애 시 자동 캐스케이드 스왑"""
        if self.active_provider == "CLAUDE" and self.claude_key:
            try:
                return self._call_claude(system_instruction, user_prompt, temperature)
            except Exception as e:
                # Claude 실패 시 Gemini로 캐스케이드
                if self.gemini_key:
                    try:
                        return self._call_gemini(system_instruction, user_prompt, temperature)
                    except Exception:
                        pass
        elif self.gemini_key:
            try:
                return self._call_gemini(system_instruction, user_prompt, temperature)
            except Exception as e:
                # Gemini 실패 시 Claude로 캐스케이드
                if self.claude_key:
                    try:
                        return self._call_claude(system_instruction, user_prompt, temperature)
                    except Exception:
                        pass

        # 둘 다 없거나 실패 시 오프라인 시뮬레이터 Fallback
        return self._mock_probabilistic_response(system_instruction, user_prompt)

    def _call_gemini(self, system_instruction: str, user_prompt: str, temperature: float) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent?key={self.gemini_key}"
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
        with urllib.request.urlopen(req, timeout=35) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["candidates"][0]["content"]["parts"][0]["text"]

    def _call_claude(self, system_instruction: str, user_prompt: str, temperature: float) -> str:
        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": self.claude_model,
            "max_tokens": 4096,
            "temperature": temperature,
            "system": system_instruction,
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "x-api-key": self.claude_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=35) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["content"][0]["text"]

    def _mock_probabilistic_response(self, system: str, user: str) -> str:
        """API 키 부재 시 테스트 및 오프라인 구동을 위한 고밀도 문학 시뮬레이터"""
        return (
            f"서늘한 침묵이 흐르는 방 안, 차가운 은발 아래로 금빛 눈동자가 미세하게 흔들립니다.\n\n"
            f"목에 채워진 서늘한 금속 초커 너머로 억누른 숨결이 파르르 떨리며 쇄골에 은밀한 붉은 열감이 번져 나갑니다.\n\n"
            f"\"...무슨 생각을 하는 거지? 선을 넘지 마라.\"\n\n"
            f"도도하게 내리깐 시선 뒤로, 결코 무너지지 않으려던 도덕적 방어선에 미세한 균열이 스쳐 지나갑니다."
        )
