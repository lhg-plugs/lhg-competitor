# 灵感来源与致谢（Attribution）

本插件的**方法论灵感**来自以下优秀的开源项目，**所有实现代码、检测规则与文案均为原创**，未复制任何第三方的原文案。

| 项目 | 作者 / 组织 | 许可 | 链接 | 借鉴了什么思路 |
|---|---|---|---|---|
| competitor-sprint | shensh1 | MIT | https://github.com/shensh1/competitor-sprint | "给一个竞品、输出完整情报报告"的流水线思想（多角色分工：搜集→分析→建议）；本插件的 scout/analyst 分工与"结论先行"报告结构受其启发，**方法论与文案均为原创** |
| business-consulting | giljae | 未声明（思路借鉴） | https://github.com/giljae/business-consulting | 商业分析框架的产品化思路（market-scan / competitor-profile / swot 命令拆分）；本插件 competitor/profile/swot 命令拆分受其启发 |
| ship-fast | z-mahmood | MIT | https://github.com/z-mahmood/ship-fast | "一次调研输出可对比的评分文档"的思想；本插件对比矩阵"一格一事实"的填表纪律受其启发 |
| superpowers | Jesse Vincent（obra） | MIT | https://github.com/obra/superpowers | SDLC 硬门方法论；本插件 commit 前报告审计拦截的硬门思想受其启发 |
| impeccable | Paul Bakaus（Renaissance Geek） | Apache-2.0 | https://github.com/pbakaus/impeccable | "确定性检测规则 + 规则引擎"的架构思想；本插件审计脚本的规则注册表模式受其启发，**规则条目全部自研** |

## 声明

1. **借鉴思路，实现与文案均为原创**：以上项目的具体文案、规则原文、代码实现均未被复制。本插件的 skill 方法论文案、审计规则、命令流程均为独立撰写。
2. **许可合规**：上述 MIT / Apache-2.0 许可项目允许在保留声明的前提下进行思路借鉴与二次创作。本文件即为保留声明的一部分。
3. **商标与归属**：各项目名称与作者署名归其各自所有者所有。

## 本插件自身的许可

本插件原创部分采用 MIT 许可（见 `LICENSE` 文件），版权所有：刘洪光（https://github.com/lhg-skills）。
