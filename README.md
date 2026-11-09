<!-- About 简介（推送后填写到仓库 About 栏）：
竞品分析专家：竞品名单→五维框架（产品/价格/渠道/营销/口碑）→对比矩阵→SWOT→差异化建议报告，一套流水线。 ｜ 一键安装：/plugin marketplace add lhg-plugs/lhg-competitor
-->
<!-- topics（推送后打）：claude-code, claude-plugin, agent-skills, competitor, competitor-analysis, swot, market-research, positioning -->

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="lhg-competitor — 竞品分析专家">
</p>

> **一句话介绍**：竞品分析专家：竞品名单→五维框架（产品/价格/渠道/营销/口碑）→对比矩阵→SWOT→差异化建议报告，一套流水线。

**一键安装**：在 Claude Code 里运行

```bash
/plugin marketplace add lhg-plugs/lhg-competitor
/plugin install lhg-competitor@lhg-plugs
```

## 它能帮你做出什么

每条产出先过确定性脚本自查，再交人工复核清单——数字全部数自仓库里的审计脚本，不靠模型"自觉"。

| 自查脚本 | 规则数 | blocker | warning | nit | 覆盖 |
|---|---|---|---|---|---|
| `scripts/audit/report_audit.py` | 12 | 4 | 6 | 2 | 维度、证据、SWOT、建议、诚实 |
| **合计** | **12** | **4** | **6** | **2** | |

- **零 LLM 成本**：规则是纯 Python 脚本，零第三方依赖，本地运行。
- **坏 / 好对照可验**：`fixtures/` 里备有坏/好用例，冒烟测试断言命中情况。
- **冒烟全绿**：`python3 smoke_test.py` 48 项全部通过（JSON 合法、frontmatter 完整、命令/skill/agent 齐全）。

## 它是什么

`lhg-competitor` 是一个 Claude Code 插件（plugin 为主、skill 为辅）：

- **4 个命令**（小白入口）：`audit` 竞品报告体检、`competitor` 一句话 → 完整竞品分析报告、`profile` 单个竞品深挖画像、`swot` SWOT 分析
- **4 个平台中立 skill**（方法论，可移植到豆包/Workbuddy 等 agent 平台）：lhg-cp-audit, lhg-cp-frame, lhg-cp-matrix, lhg-cp-profile
- **3 个专家 agent**：analyst, auditor, scout
- **2 个 hooks**（`hooks/`：post_write_remind.py, pre_commit_report_audit.py），关键操作前自动把关
- **12 条确定性自查规则**：纯 Python 脚本，见上表

## 为什么是它

不是一个 prompt，而是一套互相兜底的机制：

1. **确定性脚本（机器）+ 人工复核清单（人）**：先跑 `scripts/` 下的审计脚本（共 12 条规则），发现分三级：**blocker**（必须修）、**warning**（修或写豁免理由）、**nit**（顺手修）；再按对应 skill 的复核清单过一遍脚本抓不到的（内容真实性、越权、口径一致）。blocker 清零才算做完；为清零改规则算作弊，不许。
2. **硬门，不是提醒**：hooks 在关键操作前自动拦截或警告（见 `hooks/`），而不是只在文档里写一句"请注意"。
3. **方法论沉淀在 skill 里**：流程、检查清单、口径都写在 `skills/` 的方法论里，命令只是入口；换个 agent 平台也能复用同一套做法。
4. **可验，不是可信**：`fixtures/` 备有坏/好对照用例，`smoke_test.py` 一键验证，规则有没有生效、自己跑一遍就知道。

## 快速上手

```bash
# 1. 安装（Claude Code 里运行）
/plugin marketplace add lhg-plugs/lhg-competitor
/plugin install lhg-competitor@lhg-plugs

# 2. 一句话 → 完整竞品分析报告：竞品名单→五维框架→对比矩阵→SWOT→差异化建议
/lhg-competitor:competitor "AI 笔记应用" --me "我的笔记 App"
```

| 命令 | 作用 | 示例 |
|---|---|---|
| `/lhg-competitor:audit` | 竞品报告体检：跑确定性审计脚本（维度缺失/无来源结论/SWOT不完整/建议脱节），输出分级报告。 | `/lhg-competitor:audit reports/` |
| `/lhg-competitor:competitor` | 一句话 → 完整竞品分析报告：竞品名单→五维框架→对比矩阵→SWOT→差异化建议，流水线交付。 | `/lhg-competitor:competitor "AI 笔记应用" --me "我的笔记 App"` |
| `/lhg-competitor:profile` | 单个竞品深挖画像：产品/价格/渠道/营销/口碑五维情报 + 关键动作时间线 + 对我方的启示。 | `/lhg-competitor:profile "Notion" --deep` |
| `/lhg-competitor:swot` | SWOT 分析：对指定对象（我方产品或某竞品）做四象限拆解，每条带证据，不许空话。 | `/lhg-competitor:swot "我的笔记 App" --vs "Notion"` |

## 什么时候用 / 什么时候不用（FAQ）

**什么时候用：**

- 你需要竞品报告体检时 → 用 `/lhg-competitor:audit`
- 你需要一句话 → 完整竞品分析报告时 → 用 `/lhg-competitor:competitor`
- 你需要单个竞品深挖画像时 → 用 `/lhg-competitor:profile`

**什么时候不用：**

- 你只需要其中一个零散能力时 → 本插件是成套流程，单点需求用更轻量的 skill 更合适
- 你希望 AI 完全自由发挥、不接受任何自查与硬门时 → 它的规则审计与 hooks 会介入（可关，但那就别装它）
- 你的场景不在上面命令表覆盖范围内时 → 先看命令表，没有对应命令就别硬套

## 目录结构

```
lhg-competitor/
├── smoke_test.py          # 一键冒烟测试
├── ATTRIBUTION.md         # 灵感来源与许可声明
├── LICENSE                # MIT
├── README.md              # 本文件
├── .claude-plugin/
├── agents/
├── commands/
├── fixtures/
├── hooks/
├── scripts/
├── skills/
```

## 自检与反馈

本插件自带质检：每次使用后可跑 `python3 smoke_test.py` 一键验证（本次实测 48 项全部通过）。

发现 bug 或有改进建议，以 `[QC] <一句话问题>` 为标题提交到 https://github.com/lhg-plugs/lhg-competitor/issues，正文写清"复现步骤 → 实际表现 → 期望表现"。

同门插件见 [lhg-plugs](https://github.com/lhg-plugs)，86 个插件的完整矩阵在 [marketplace](https://github.com/lhg-plugs/marketplace) 维护。

## 出品：刘洪光

本插件由真人出镜 IP「刘洪光」（安徽合肥）出品，归属 [lhg-skills](https://github.com/lhg-skills)。

- GitHub 主页：https://github.com/lhg-skills —— 全部 skill 开源在此，欢迎 star
- 抖音：搜「刘老师讲AI实战」
- 微信：lhgsmsw
