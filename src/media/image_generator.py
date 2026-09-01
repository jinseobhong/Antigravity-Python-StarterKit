# -*- coding: utf-8 -*-
"""
src/media/image_generator.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Media Layer: Hugging Face Animagine / Illustrious-XL AI Portrait Generator Engine
- .env의 HF_TOKEN을 사용하여 Hugging Face Animagine-XL 3.1 / Illustrious-XL Gradio 엔진 직접 연동
- 단부루 6-Slot 태그 최적화 렌더링 (832x1216 고해상도 미소녀 화풍)
- 로컬 정적 디렉토리(src/web/static/images/portraits/) 자동 영구 저장
"""

from __future__ import annotations
import os
import re
import shutil
import urllib.request
import urllib.parse
from pathlib import Path

try:
    from gradio_client import Client
    GRADIO_AVAILABLE = True
except ImportError:
    GRADIO_AVAILABLE = False


class ImageGeneratorService:
    """Hugging Face 기반 정통 SDXL / Illustrious / Animagine-XL 일러스트 생성기"""

    BASE_IMAGE_DIR = Path("src/web/static/images/portraits")

    @classmethod
    def _get_hf_token(cls) -> str:
        env_path = Path(".env")
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("HF_TOKEN="):
                    return line.split("=", 1)[1].strip()
        return os.getenv("HF_TOKEN", "")

    @classmethod
    def generate_portrait(cls, seed_hash: str, danbooru_prompt: str) -> str:
        """단부루 프롬프트로부터 정통 SDXL Anime/Illustrious-XL 고화질 일러스트 생성"""
        cls.BASE_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        
        clean_seed = re.sub(r'[^a-zA-Z0-9_-]', '_', seed_hash.replace('#', ''))
        file_path = cls.BASE_IMAGE_DIR / f"{clean_seed}.png"
        relative_url = f"/static/images/portraits/{clean_seed}.png"

        hf_token = cls._get_hf_token()
        negative_prompt = (
            "nsfw, photo, deformed, black and white, realism, disfigured, low contrast, "
            "lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, "
            "cropped, worst quality, low quality, jpeg artifacts, signature, watermark, username, blurry"
        )

        # 1. Hugging Face Animagine XL 3.1 / Illustrious-XL Gradio 직결 시도
        if GRADIO_AVAILABLE and hf_token:
            try:
                print(f"[ImageGeneratorService] Connecting to Hugging Face Animagine XL 3.1 (HF_TOKEN)...")
                client = Client("cagliostrolab/animagine-xl-3.1", token=hf_token)
                result = client.predict(
                    danbooru_prompt,
                    negative_prompt,
                    42, # seed
                    832, # width
                    1216, # height
                    7.0, # guidance_scale
                    28, # number_of_inference_steps
                    "Euler a", # sampler
                    "832 x 1216", # aspect_ratio
                    "Anime", # style_preset
                    "Heavy v3.1", # quality_tags_presets
                    False, # use_upscaler
                    0.55, # strength
                    1.0, # upscale_by
                    True, # add_quality_tags
                    api_name="/run"
                )
                gallery = result[0] if isinstance(result, tuple) else result
                if gallery and len(gallery) > 0:
                    img_info = gallery[0]
                    img_path = img_info.get("image") if isinstance(img_info, dict) else img_info
                    shutil.copy(img_path, str(file_path))
                    print(f"[ImageGeneratorService] Hugging Face SDXL image generated successfully: {file_path}")
                    return relative_url
            except Exception as e:
                print(f"[ImageGeneratorService] Hugging Face Space generation failed: {e}. Cascading to fallback...")

        # 2. 고속 백업 엔드포인트 폴백
        try:
            enhanced_prompt = f"masterpiece, best quality, ultra-detailed, anime artwork, {danbooru_prompt}"
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            request_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=832&height=1216&model=flux-anime&nologo=true"
            
            req = urllib.request.Request(request_url, headers={"User-Agent": "AbyssEngine-Studio/1.0"})
            with urllib.request.urlopen(req, timeout=35) as response:
                image_data = response.read()
                with open(file_path, "wb") as f:
                    f.write(image_data)
            return relative_url
        except Exception as e:
            print(f"[ImageGeneratorService] Fallback generation failed: {e}")
            raise RuntimeError(f"모든 AI 일러스트 생성 엔진 호출 실패: {e}")
