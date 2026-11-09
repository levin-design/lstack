# pstack 指南

当你不再微观管理 agent 时，pstack 才能发挥最大作用。你描述想要什么，以及你如何判断它已经完成。`/poteto-mode` 会挑选剧本，在步骤需要时运行其他技能，并向你展示证据。本指南用贴近真实的 prompt 教你养成这个习惯。

你将学到：

1. [设置 pstack](./01-setup.md)。安装插件并选择你的模型。
2. [通过 `/poteto-mode` 引导工作](./02-poteto-mode.md)。给它一个目标，看它挑选剧本。
3. [理解代码](./03-understand.md)。先做只读调查，然后在改动任何代码之前使用 `/how`、`/why`、`/teach` 和 `/recall`。
4. [设计改动](./04-design.md)。在代码固化成某个形态之前，使用 `/architect`、`/arena`、`/swarm`、`/interrogate`、原型和计划。
5. [构建并清理改动](./05-build-and-clean.md)。构建类剧本、`/tdd`、`/unslop` 和 `/no-comments`。
6. [验证并交付](./06-verify-and-ship.md)。在真实应用上证明行为，对测试很少触及的部分做形式化验证，用 `/benchmark-checklist` 审核数字，然后打开一个聚焦的 PR 并推动它合并。
7. [在你睡觉时继续工作](./07-overnight.md)。先建立信任再开循环、过夜契约、可供审计的决策日志，以及能扩展到多个 agent 的 Projects 和 automations。
8. [用原则名称引导](./08-principles.md)。24 个能在任务中途让 agent 转向的名称。
9. [把它变成你自己的](./09-make-it-yours.md)。你自己的模式、用于反复出现的错误的 `/correct`，以及如何测试技能改动。
10. [配方与陷阱](./10-recipes-and-pitfalls.md)。可以复制的 prompt 和需要避开的错误。

第一次请按顺序阅读。之后每一页都可以独立阅读。

当你卡住了，或分不清哪个技能合适时，输入 [`/poteto-help`](../../skills/poteto-help/SKILL.md) 并附上你的问题：

```text
/poteto-help which skill should i use to review this branch?
```

它会回答，交给你一条可发送的 prompt，并链接答案来源的技能或指南页。它不会启动工作，因为一次 pstack 运行会消耗真实 token，所以由你在准备好时发送 prompt。它只在你输入时运行。

## 如果你只记住一件事

用你自己的话，给 agent 一个目标和一个检查它的方法：

```text
/poteto-mode the export writes duplicate rows when a retry lands mid-run. repro first, then fix and verify.
```

你不需要点名剧本或列出技能。"repro first" 和一个可检查的结果，就是 `/poteto-mode` 需要的全部路由信号。它会匹配 Bug fix 剧本，把步骤复制进待办列表，并在每一步触发时调用正确的技能。

下一步：[设置 pstack](./01-setup.md)。
