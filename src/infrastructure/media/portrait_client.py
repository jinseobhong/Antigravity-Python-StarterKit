# -*- coding: utf-8 -*-
"""
src/infrastructure/media/portrait_client.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HuggingFace SD 기반 초상화(Portrait) 생성 어댑터
"""

from __future__ import annotations
import os
import json
import urllib.request
import urllib.error
from typing import Optional


class PortraitClient:
    """캐릭터 초상화 이미지 렌더링 클라이언트"""

    def __init__(self, hf_token: Optional[str] = None):
        self.hf_token = hf_token or os.environ.get("HF_TOKEN", "")

    def generate_portrait(self, prompt: str) -> Optional[bytes]:
        """프롬프트 기반 이미지 바이트 생성 (토큰 부재 시 None 반환)"""
        if not self.hf_token:
            return None

        # SD Anime endpoint
        url = "https://api-inference.huggingface.co/models/anima-pencil-xl"
        req = urllib.request.Request(
            url,
            data=json.dumps({"inputs": prompt}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.hf_token}",
                "Content-Type": "application/json"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except Exception:
            return None
