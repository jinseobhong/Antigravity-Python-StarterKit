# -*- coding: utf-8 -*-
"""
app.py — AbyssEmpire Web Studio 최상위 원클릭 런처
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
실행 명령어:
  py -3 app.py
"""

import sys
import os

# 프로젝트 루트 경로 보장
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.presentation.web.server import launch_web_studio

if __name__ == "__main__":
    launch_web_studio(port=8877, open_browser=True)
