#!/usr/bin/env python3
"""lhg-competitor 确定性报告审计：12 条规则，零第三方依赖。

扫描目标目录下的竞品分析报告（Markdown），输出 JSON 与人类可读报告；
有 blocker 时以 exit code 2 退出（供 hooks 与 CI 使用）。

用法：
    python3 report_audit.py --target <报告目录> [--format json|text] [--fail-on blocker|warning|nit]

规则文案均为本项目原创（思路受 competitor-sprint / business-consulting /
ship-fast 等开源项目启发，未复制任何第三方原文）。
"""

import argparse
import json
import os
import re
import sys

VERSION = "1.0.0"
TOOL = "lhg-competitor/report-audit"

SKIP_DIRS = {".git", "__pycache__", "node_modules"}

DIMS = ["产品", "价格", "渠道", "营销", "口碑"]
CLAIM_RES = [
    re.compile(r"数据显示"),
    re.compile(r"据报道"),
    re.compile(r"调研显示"),
    re.compile(r"市占率"),
    re.compile(r"市场份额"),
    re.compile(r"同比(增长|下降)"),
    re.compile(r"用户规模"),
]
SOURCE_SECTION_RE = re.compile(r"^#{1,4}\s*.*(来源|参考|出处)", re.M)
URL_RE = re.compile(r"https?://[^\s\)>\]]+")
NUM_CLAIM_RE = re.compile(r"\d+(?:\.\d+)?\s*%|¥\s*[\d,]+(?:\.\d+)?|[￥$]\s*[\d,]+")
SWOT_QUADS = [
    ("S", re.compile(r"^#{1,4}\s*.*(优势|^S\b|S\s*[:：])", re.M)),
    ("W", re.compile(r"^#{1,4}\s*.*(劣势|^W\b|W\s*[:：])", re.M)),
    ("O", re.compile(r"^#{1,4}\s*.*(机会|^O\b|O\s*[:：])", re.M)),
    ("T", re.compile(r"^#{1,4}\s*.*(威胁|^T\b|T\s*[:：])", re.M)),
]
SUGGEST_RES = [re.compile(r"^#{1,4}\s*.*(建议|打法|策略|行动)", re.M)]
VAGUE_WORDS = ["加强", "提升", "优化", "加大", "重视", "深化"]
CONCRETE_WORDS = ["具体", "例如", "比如", "步骤", "时间表", "负责人", "指标", "验证", "试点"]
DISCLAIMER_RE = re.compile(r"仅供参考|不构成.*建议|免责声明")


class Finding:
    __slots__ = ("rule_id", "severity", "category", "title", "file", "line", "snippet", "detail")

    def __init__(self, rule_id, severity, category, title, file, line, snippet, detail):
        self.rule_id = rule_id
        self.severity = severity
        self.category = category
        self.title = title
        self.file = file
        self.line = line
        self.snippet = snippet
        self.detail = detail

    def to_dict(self):
        return {
            "rule_id": self.rule_id, "severity": self.severity,
            "category": self.category, "title": self.title,
            "file": self.file, "line": self.line,
            "snippet": self.snippet, "detail": self.detail,
        }


RULES = []
_RULE_BY_ID = {}


def rule(rule_id, severity, category, title, detail):
    def deco(fn):
        r = {"id": rule_id, "severity": severity, "category": category,
             "title": title, "detail": detail}
        _RULE_BY_ID[rule_id] = r
        r["check"] = fn
        RULES.append(r)
        return fn
    return deco


def _F(rule_id, path, line, snippet):
    r = _RULE_BY_ID[rule_id]
    return Finding(r["id"], r["severity"], r["category"], r["title"],
                   path, line, snippet[:160], r["detail"])


def has_source_section(text):
    return bool(SOURCE_SECTION_RE.search(text))


# ---------------- 维度 ----------------

@rule("CP-DIM-001", "blocker", "维度", "分析维度缺失",
      "产品/价格/渠道/营销/口碑五个维度覆盖不足 3 个。缺维度的竞品分析是管中窥豹，补齐或说明为什么不看。")
def r_dim_001(lines, text, path, ctx):
    hit = [d for d in DIMS if d in text]
    if len(hit) < 3:
        return [_F("CP-DIM-001", path, 1, "仅覆盖维度：%s" % "、".join(hit) if hit else "未覆盖任何维度")]
    return []


@rule("CP-DIM-002", "warning", "维度", "对比矩阵单薄",
      "全文 Markdown 表格的数据行不足 3 行。竞品少于 3 个或指标太少，对比结论站不住。")
def r_dim_002(lines, text, path, ctx):
    rows = 0
    for ln in lines:
        s = ln.strip()
        if s.startswith("|") and s.endswith("|") and not re.match(r"^\|[\s:\-|]+\|$", s):
            rows += 1
    rows = max(0, rows - 1)  # 减表头
    if rows < 3:
        return [_F("CP-DIM-002", path, 1, "表格数据行仅 %d 行" % rows)]
    return []


@rule("CP-DIM-003", "warning", "维度", "无对比矩阵",
      "全文没有 Markdown 表格。竞品分析没有对比矩阵，等于没有横向对比，请补一张。")
def r_dim_003(lines, text, path, ctx):
    if not any(ln.strip().startswith("|") for ln in lines):
        return [_F("CP-DIM-003", path, 1, "全文无表格")]
    return []


@rule("CP-DIM-004", "nit", "维度", "缺我方对照",
      "全文没有'我方/我们'视角。竞品分析是为我方决策服务的，没有对照视角容易写成行业综述。")
def r_dim_004(lines, text, path, ctx):
    if not re.search(r"我方|我们(的|要|可以|应该)|自有产品", text):
        return [_F("CP-DIM-004", path, 1, "无我方对照视角")]
    return []


# ---------------- 证据 ----------------

@rule("CP-EVD-001", "blocker", "证据", "结论无来源",
      "出现'数据显示/据报道/市占率'类断言，但全文无来源/参考节。没出处的结论不许进报告。")
def r_evd_001(lines, text, path, ctx):
    if has_source_section(text):
        return []
    out = []
    for i, ln in enumerate(lines):
        if any(rx.search(ln) for rx in CLAIM_RES):
            out.append(_F("CP-EVD-001", path, i + 1, ln.strip()))
    return out


@rule("CP-EVD-002", "warning", "证据", "来源过少",
      "有来源节，但链接不足 2 个。关键结论至少要有两个独立出处交叉验证。")
def r_evd_002(lines, text, path, ctx):
    if not has_source_section(text):
        return []
    n = len(URL_RE.findall(text))
    if n < 2:
        return [_F("CP-EVD-002", path, 1, "全文仅 %d 个链接" % n)]
    return []


@rule("CP-EVD-003", "warning", "证据", "数字断言缺出处",
      "含百分比/金额类数字断言，但全文无来源节。精确数字必须有出处，否则降为定性描述。")
def r_evd_003(lines, text, path, ctx):
    if has_source_section(text):
        return []
    out = []
    for i, ln in enumerate(lines):
        if NUM_CLAIM_RE.search(ln):
            out.append(_F("CP-EVD-003", path, i + 1, ln.strip()))
            if len(out) >= 3:
                break
    return out


# ---------------- SWOT ----------------

@rule("CP-SWOT-001", "blocker", "SWOT", "SWOT 象限不完整",
      "报告提到 SWOT，但 S/W/O/T 任一象限缺失。缺象限的 SWOT 是残次品，补齐或删掉 SWOT。")
def r_swot_001(lines, text, path, ctx):
    if "SWOT" not in text.upper():
        return []
    missing = [q for q, rx in SWOT_QUADS if not rx.search(text)]
    if missing:
        return [_F("CP-SWOT-001", path, 1, "缺失象限：%s" % "、".join(missing))]
    return []


@rule("CP-SWOT-002", "warning", "SWOT", "SWOT 条目单薄",
      "四象限条目总数不足 8 条。每象限至少 2 条有证据的条目，否则分析深度不够。")
def r_swot_002(lines, text, path, ctx):
    if "SWOT" not in text.upper():
        return []
    if any(q for q, rx in SWOT_QUADS if not rx.search(text)):
        return []  # 象限都不全，CP-SWOT-001 已报
    n = sum(1 for ln in lines if re.match(r"^\s*[-*]\s+\S", ln))
    if n < 8:
        return [_F("CP-SWOT-002", path, 1, "全文条目仅 %d 条" % n)]
    return []


# ---------------- 建议 ----------------

def _suggest_section(lines):
    idx = [i for i, ln in enumerate(lines) if any(rx.match(ln) for rx in SUGGEST_RES)]
    if not idx:
        return ""
    return "\n".join(lines[idx[0]:])


@rule("CP-ADV-001", "blocker", "建议", "建议与分析脱节",
      "有建议节，但建议内容未呼应报告中的任何分析维度（产品/价格/渠道/营销/口碑）。"
      "建议必须从分析中长出来，追溯不到的不许写。")
def r_adv_001(lines, text, path, ctx):
    seg = _suggest_section(lines)
    if not seg:
        return []
    if not any(d in seg for d in DIMS):
        return [_F("CP-ADV-001", path, 1, "建议节未提及任何分析维度")]
    return []


@rule("CP-ADV-002", "warning", "建议", "建议空泛",
      "建议节出现'加强/提升/优化'类泛词，却无具体动作词（具体/例如/步骤/指标等）。"
      "不说怎么做的建议等于没说。")
def r_adv_002(lines, text, path, ctx):
    seg = _suggest_section(lines)
    if not seg:
        return []
    vague = any(w in seg for w in VAGUE_WORDS)
    concrete = any(w in seg for w in CONCRETE_WORDS)
    if vague and not concrete:
        return [_F("CP-ADV-002", path, 1, "泛词多、无具体动作")]
    return []


# ---------------- 诚实 ----------------

@rule("CP-HON-001", "nit", "诚实", "缺免责声明",
      "全文无'仅供参考/不构成建议/免责声明'。竞品报告基于公开信息，必须声明局限。")
def r_hon_001(lines, text, path, ctx):
    if not DISCLAIMER_RE.search(text):
        return [_F("CP-HON-001", path, 1, "无免责声明")]
    return []


# ---------------------------------------------------------------- 运行器

def collect_files(target):
    out = []
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".md"):
                out.append(os.path.join(root, f))
    return sorted(out)


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def run(target):
    files = collect_files(target)
    findings = []
    for path in files:
        text = read_text(path)
        lines = text.split("\n")
        rel = os.path.relpath(path, target)
        for r in RULES:
            try:
                for f in r["check"](lines, text, path, {}) or []:
                    f.file = rel
                    findings.append(f)
            except Exception:
                continue
    return files, findings


def main(argv=None):
    ap = argparse.ArgumentParser(description="lhg-competitor 竞品报告确定性审计")
    ap.add_argument("--target", default=".", help="报告目录")
    ap.add_argument("--format", choices=["json", "text"], default="text")
    ap.add_argument("--fail-on", choices=["blocker", "warning", "nit"], default="blocker")
    args = ap.parse_args(argv)

    target = os.path.abspath(args.target)
    if not os.path.isdir(target):
        print("target 不是目录：%s" % args.target, file=sys.stderr)
        return 1

    files, findings = run(target)
    sev_rank = {"blocker": 3, "warning": 2, "nit": 1}
    counts = {"blocker": 0, "warning": 0, "nit": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1

    result = {
        "tool": TOOL,
        "version": VERSION,
        "target": args.target,
        "summary": {
            "files_scanned": len(files),
            "rules_run": len(RULES),
            "blocker": counts["blocker"],
            "warning": counts["warning"],
            "nit": counts["nit"],
        },
        "findings": [f.to_dict() for f in sorted(
            findings, key=lambda x: (-sev_rank.get(x.severity, 0), x.file, x.line))],
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        s = result["summary"]
        print("竞品报告审计：扫描 %d 文件，运行 %d 条规则" % (s["files_scanned"], s["rules_run"]))
        print("blocker=%d warning=%d nit=%d" % (s["blocker"], s["warning"], s["nit"]))
        for f in result["findings"]:
            print("[%s][%s] %s:%d %s" % (
                f["severity"].upper(), f["rule_id"], f["file"], f["line"], f["title"]))
            print("    %s" % f["detail"])
            if f["snippet"]:
                print("    → %s" % f["snippet"])

    level = sev_rank[args.fail_on]
    bad = any(sev_rank.get(f.severity, 0) >= level for f in findings)
    return 2 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
