#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.py — AbyssEngine Web Studio One-Click Startup Entrypoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
구동: py -3 app.py
접속: http://127.0.0.1:8080
"""

import sys
import os

# UTF-8 출력 보장
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.presentation.web.server import run_server

if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port=port)
