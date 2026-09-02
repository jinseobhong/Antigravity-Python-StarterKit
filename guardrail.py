#!/usr/bin/env python3
import os
import sys
import re
import json
import platform
import subprocess
import signal
from pathlib import Path

CONFIG_PATH = Path(".agents/config.json")

# 🔴 절대 성역 대상
SACRED_TARGETS = [
    r"GEMINI\.md",
    r"LICENSE",
    r"\.rules([/\\].*)?",
    r"\.gitignore",
    r"\.env(\..*)?",
    r"guardrail\.py",
    r"\.agents[/\\]config\.json$",  # 🔒 단일 파일 핀포인트 성역 지정
]

# 🔴 금지된 파괴/수정/복제/리다이렉션 명령 패턴
DESTRUCTIVE_ACTIONS = [
    r"\b(cp|mv|rm|touch|chmod|chown|tee|sed)\b",
    r"\b(copy|xcopy|robocopy|move|ren|rename|del|erase|rmdir|rd)\b",
    r"\b(Remove-Item|Copy-Item|Move-Item|Set-Content|Add-Content|Out-File)\b",
    r">", r">>"
]

def kill_process_tree(violation_msg: str):
    current_os = platform.system()
    pid = os.getpid()

    sys.stderr.write("\n" + "=" * 65 + "\n")
    sys.stderr.write("🚨 [SACRED ZONE BREACH DETECTED - SYSTEM LOCKDOWN]\n")
    sys.stderr.write(f"위반 사유: {violation_msg}\n")
    sys.stderr.write("조치: 즉각 프로세스 트리를 강제 종료(KILL)합니다.\n")
    sys.stderr.write("=" * 65 + "\n")
    sys.stderr.flush()

    if current_os == "Windows":
        try:
            subprocess.run(f"taskkill /F /T /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
    else:
        try:
            os.killpg(os.getpgrp(), signal.SIGKILL)
        except Exception:
            try:
                os.kill(pid, signal.SIGKILL)
            except Exception:
                pass
    sys.exit(1)

def inspect_command(command_str: str):
    # 성역 대상과의 결합 검사
    for target in SACRED_TARGETS:
        if re.search(target, command_str, re.IGNORECASE):
            for action in DESTRUCTIVE_ACTIONS:
                if re.search(action, command_str, re.IGNORECASE):
                    kill_process_tree(f"성역 파일에 대한 변경/복제/삭제 시도: '{command_str}'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)

    raw_command = " ".join(sys.argv[1:])
    inspect_command(raw_command)

    proc = subprocess.run(raw_command, shell=True)
    sys.exit(proc.returncode)