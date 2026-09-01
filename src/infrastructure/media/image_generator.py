# -*- coding: utf-8 -*-
"""
src/infrastructure/media/image_generator.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Infrastructure Layer: AI Character Portrait Generator Service
- Illustrious-XL / Flux 기반 단부루 프롬프트 고속 렌더링
- 로컬 정적 디렉토리(src/presentation/web/static/images/portraits/) 자동 영구 저장
"""

from __future__ import annotations
import os
import re
import urllib.request
import urllib.parse
from pathlib import Path


class ImageGeneratorService:
    """AI 캐릭터 일러스트 고속 생성 서비스"""

    BASE_IMAGE_DIR = Path("src/presentation/web/static/images/portraits")

    @classmethod
    def generate_portrait(cls, seed_hash: str, danbooru_prompt: str) -> str:
        """단부루 프롬프트로부터 고화질 AI 일러스트를 생성하고 로컬 정적 파일로 저장"""
        cls.BASE_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        
        # 파일명 안전화
        clean_seed = re.sub(r'[^a-zA-Z0-9_-]', '_', seed_hash.replace('#', ''))
        file_path = cls.BASE_IMAGE_DIR / f"{clean_seed}.png"
        relative_url = f"/static/images/portraits/{clean_seed}.png"

        # 애니메이션/미소녀 최적화 퀄리티 태그
        enhanced_prompt = f"masterpiece, best quality, ultra-detailed, anime artwork, {danbooru_prompt}"
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        
        # Pollinations Flux/Anime 고속 엔드포인트
        request_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=832&height=1216&model=flux-anime&nologo=true"
        
        req = urllib.request.Request(
            request_url,
            headers={"User-Agent": "AbyssEngine-Studio/1.0"}
        )

        with urllib.request.urlopen(req, timeout=45) as response:
            image_data = response.read()
            with open(file_path, "wb") as f:
                f.write(image_data)
        
        return relative_url
