# -*- coding: utf-8 -*-
"""
src/presentation/web
~~~~~~~~~~~~~~~~~~~~
AbyssEngine 로컬 웹 스튜디오 패키지
"""

from .server import launch_web_studio, WebStudioHandler

__all__ = [
    "launch_web_studio",
    "WebStudioHandler",
]
