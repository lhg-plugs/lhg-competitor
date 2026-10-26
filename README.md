<!-- About 简介（推送后填写到仓库 About 栏）：
竞品分析专家：一句话生成竞品情报报告（五维框架+对比矩阵+SWOT+差异化建议） ｜ 一键安装：/plugin marketplace add lhg-plugs/lhg-competitor
-->
<!-- topics（推送后打）：claude-code, claude-plugin, agent-skills, competitor-analysis, swot, market-research, business, chinese -->

# lhg-competitor：竞品分析专家

> **一句话介绍**：给 AI 装上"竞品分析流水线"——竞品名单→五维框架（产品/价格/渠道/营销/口碑）→对比矩阵→SWOT→差异化建议报告，小白一句话也能产出有来源、有矩阵、有打法的竞品情报。
>
> **一键安装**：在 Claude Code 里运行
> ```
> /plugin marketplace add lhg-plugs/lhg-competitor
> /plugin install lhg-competitor@lhg-plugs
> ```

## 它是什么

`lhg-competitor` 是一个 Claude Code 插件（plugin 为主、skill 为辅）：

- **4 个命令**（小白入口）：`competitor` 一句话跑完整流水线，`profile` 单竞品深挖画像，`swot` 四象限拆解，`audit` 报告体检
- **4 个平台中立 skill**（方法论，可移植到豆包/Workbuddy 等 agent 平台）：维度框架、单竞品画像、对比矩阵与差异化、报告质检
- **3 个专家 agent**：情报搜集员 scout、对比分析师 analyst、报告质检员 auditor
- **2 个 hooks**：commit 前报告审计拦截（硬门，可一键豁免）、写报告时质检提醒（警告级）
- **12 条确定性审计规则**：纯 Python、零第三方依赖，专治"维度缺失、无来源结论、SWOT 不完整、建议与分析脱节"

## 4 个命令用法

| 命令 | 作用 | 示例 |
|---|---|---|
| `/lhg-competitor:competitor` | 一句话 → 完整竞品分析报告（名单→框架→矩阵→SWOT→建议） | `/lhg-competitor:competitor "AI 笔记应用" --me "我的笔记 App"` |
| `/lhg-competitor:profile` | 单个竞品深挖画像（五维情报+动作时间线+可抄/可避/可打） | `/lhg-competitor:profile "Notion" --deep` |
| `/lhg-competitor:swot` | SWOT 四象限拆解（每条带证据+交叉策略推导） | `/lhg-competitor:swot "我的笔记 App" --vs "Notion"` |
| `/lhg-competitor:audit` | 竞品报告体检（脚本+人工 6 问，blocker 清零放行） | `/lhg-competitor:audit reports/` |

## 质检说明

质检 = 确定性脚本（机器）+ 人工评审清单（人）：

1. 先跑 `scripts/audit/report_audit.py --target reports/`（12 条规则，零 LLM 成本）；
2. 发现分三级：**blocker**（维度缺失、无来源结论、SWOT 不完整、建议脱节——必须修，commit 前 hook 会拦截）、**warning**（来源过少、矩阵单薄、建议空泛——修或写豁免理由）、**nit**（缺免责声明、缺我方对照——顺手修）；
3. 再按 `lhg-cp-audit` 的人工 6 问过一遍脚本抓不到的（编造数字、措辞超证据、cherry-picking）。

blocker 清零才算完稿；为清零改规则算作弊，不许。

## 诚实铁律

- 搜不到的写"未找到公开信息"，不许编造数字和来源链接。
- 每个关键结论必须标注来源；价格/评分/融资类数据必须标"截至日期"。
- 推断必须标注"（推断）"，事实与推断不许混在一起。

## 目录结构

```
lhg-competitor/
├── .claude-plugin/          # plugin.json（插件清单）+ marketplace.json（本仓即市场）
├── commands/                # 4 个命令：competitor / profile / swot / audit
├── skills/                  # 4 个平台中立 skill（lhg-cp-frame/profile/matrix/audit）
├── agents/                  # 3 个专家 agent（scout / analyst / auditor）
├── hooks/                   # 2 个门：commit 前报告审计拦截 / 写报告质检提醒 + 豁免说明
├── scripts/audit/           # 12 条确定性审计规则（零第三方依赖）
├── fixtures/                # 冒烟测试用例（坏/好报告对照）
├── smoke_test.py            # 一键冒烟测试
├── ATTRIBUTION.md           # 灵感来源与许可声明
└── LICENSE                  # MIT
```

## 什么时候用 / 什么时候不用（FAQ）

**什么时候用：**

- 你要立项/做产品决策，想快速搞清"对手在干嘛、我差在哪"时 → 用 `/lhg-competitor:competitor`
- 某个对手让你睡不着，想把它看透时 → 用 `/lhg-competitor:profile --deep`
- 团队要做战略讨论，需要一份"有证据、没空话"的 SWOT 时 → 用 `/lhg-competitor:swot`
- 收到一份竞品分析（自己写的或别人写的），想验证靠不靠谱时 → 用 `/lhg-competitor:audit`

**什么时候不用：**

- 你要的是实时市场数据/财报数字本身（如精确的市占率）→ 本插件做的是"分析框架+报告"，数据靠公开渠道搜集，不保证覆盖冷门赛道
- 你需要法律/合规层面的尽调 → 那是律师和会计师的活，AI 报告不能替代
- 你只想让 AI 夸你的产品比对手强 → 它的质检会把你这种 cherry-picking 拦下来，别装

## lhg-plugs 插件矩阵

| 插件 | 一句话 | 安装 |
|---|---|---|
| [lhg-fullstack](https://github.com/lhg-plugs/lhg-fullstack) | 小白一句话 → 高质量全栈应用 | `/plugin install lhg-fullstack@lhg-plugs` |
| [lhg-video-edit](https://github.com/lhg-plugs/lhg-video-edit) | 一句话把口播素材剪成爆款短视频（+口播脚本子命令） | `/plugin install lhg-video-edit@lhg-plugs` |
| [lhg-wechat-article](https://github.com/lhg-plugs/lhg-wechat-article) | 公众号写作专家：选题到排版一气呵成 | `/plugin install lhg-wechat-article@lhg-plugs` |
| [lhg-xiaohongshu](https://github.com/lhg-plugs/lhg-xiaohongshu) | 小红书种草专家：卖点到爆款笔记一键生成 | `/plugin install lhg-xiaohongshu@lhg-plugs` |
| [lhg-resume](https://github.com/lhg-plugs/lhg-resume) | 简历优化专家：ATS诊断到模拟面试一条龙 | `/plugin install lhg-resume@lhg-plugs` |
| [lhg-ppt](https://github.com/lhg-plugs/lhg-ppt) | PPT制作专家：述职融资答辩一键成稿 | `/plugin install lhg-ppt@lhg-plugs` |
| [lhg-excel](https://github.com/lhg-plugs/lhg-excel) | 表格数据专家：清洗透视图表一条龙 | `/plugin install lhg-excel@lhg-plugs` |
| [lhg-thesis](https://github.com/lhg-plugs/lhg-thesis) | 毕业论文助手：开题到盲审的写作流水线 | `/plugin install lhg-thesis@lhg-plugs` |
| [lhg-miniprogram](https://github.com/lhg-plugs/lhg-miniprogram) | 小程序开发专家：一句话生成微信小程序 | `/plugin install lhg-miniprogram@lhg-plugs` |
| [lhg-contract](https://github.com/lhg-plugs/lhg-contract) | 合同审查助手：风险条款标红+修改建议 | `/plugin install lhg-contract@lhg-plugs` |
| [lhg-geo](https://github.com/lhg-plugs/lhg-geo) | AI搜索优化专家：品牌在AI回答里的可见度 | `/plugin install lhg-geo@lhg-plugs` |
| [lhg-poster](https://github.com/lhg-plugs/lhg-poster) | 海报设计专家：一句话生成手机端海报 | `/plugin install lhg-poster@lhg-plugs` |
| [lhg-shopify](https://github.com/lhg-plugs/lhg-shopify) | 独立站建站专家：高转化店铺一键搭建 | `/plugin install lhg-shopify@lhg-plugs` |
| [lhg-fiction](https://github.com/lhg-plugs/lhg-fiction) | 网文写作专家：大纲到逐章+人设一致性检测 | `/plugin install lhg-fiction@lhg-plugs` |
| [lhg-drama-script](https://github.com/lhg-plugs/lhg-drama-script) | 短剧剧本专家：分集大纲到单集剧本 | `/plugin install lhg-drama-script@lhg-plugs` |
| [lhg-lit-review](https://github.com/lhg-plugs/lhg-lit-review) | 文献综述专家：框架到引用校验一条龙 | `/plugin install lhg-lit-review@lhg-plugs` |
| [lhg-salary-talk](https://github.com/lhg-plugs/lhg-salary-talk) | 薪酬谈判专家：策略到话术演练 | `/plugin install lhg-salary-talk@lhg-plugs` |
| [lhg-biz-report](https://github.com/lhg-plugs/lhg-biz-report) | 商业分析专家：数据到图文报告一键生成 | `/plugin install lhg-biz-report@lhg-plugs` |
| [lhg-study-abroad](https://github.com/lhg-plugs/lhg-study-abroad) | 留学文书专家：PS推荐信多轮打磨 | `/plugin install lhg-study-abroad@lhg-plugs` |
| [lhg-meal-plan](https://github.com/lhg-plugs/lhg-meal-plan) | 营养食谱专家：测算到一周食谱+采购单 | `/plugin install lhg-meal-plan@lhg-plugs` |
| [lhg-competitor](https://github.com/lhg-plugs/lhg-competitor) | 竞品分析专家：五维框架+对比矩阵+SWOT+差异化建议报告 | `/plugin install lhg-competitor@lhg-plugs` |
| *（后续插件在此追加，保持表格格式一致）* | | |

## 自检与反馈

本插件自带质检：每次使用后可跑 `python3 smoke_test.py` 一键验证（JSON 合法、skill/command/agent 完整性、12 条规则、fixtures 命中、hooks 行为）。

发现 bug 或有改进建议，以 `[QC] <一句话问题>` 为标题提交到 https://github.com/lhg-plugs/lhg-competitor/issues，正文写清"复现步骤 → 实际表现 → 期望表现"。

## 出品：刘洪光

本插件由真人出镜 IP「刘洪光」（安徽合肥）出品，归属 [lhg-skills](https://github.com/lhg-skills)。

- GitHub 主页：https://github.com/lhg-skills —— 全部 skill 开源在此，欢迎 star
- 抖音：搜「刘老师讲AI实战」
- 微信：lhgsmsw
