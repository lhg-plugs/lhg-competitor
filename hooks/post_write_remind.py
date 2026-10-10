#!/usr/bin/env python3
"""lhg-competitor 提醒（警告级，不拦截）：写 reports/ 下的报告 md 时提醒跑审计。

触发：PostToolUse / Write|Edit。只做提醒，永远 exit 0、不拦截写入。

逃生方式：LHG_CP_HOOKS_OFF=1（环境变量）可关闭本提醒；
或 /plugin disable lhg-competitor 停用整个插件。
零第三方依赖。
"""

import json
import os
import sys


def main() -> int:
    if os.environ.get("LHG_CP_HOOKS_OFF") == "1":
        return 0

    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0

    tool_input = payload.get("tool_input", {}) or {}
    file_path = (tool_input.get("file_path", "") or "").replace("\\", "/")
    if not file_path.endswith(".md"):
        return 0
    parts = file_path.split("/")
    if "reports" not in parts and "report" not in "".join(parts[-2:-1]):
        return 0

    msg = (
        "质检提醒（lhg-competitor）：%s 疑似竞品分析报告。\n"
        "交付前请跑 /lhg-competitor:audit（或 scripts/audit/report_audit.py）做一次体检，"
        "blocker 清零才算完稿。\n"
        "关闭本提醒：export LHG_CP_HOOKS_OFF=1（当前会话有效）。"
    ) % file_path
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": msg,
        }
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
