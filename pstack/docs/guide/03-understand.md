# 改动之前先理解代码

编辑你不理解的代码，正是细微回归被发布出去的方式——这对 agent 和对你自己一样成立。agent 通常以两种方式失败：误读你的意图，或者缺乏把工作做对的上下文。[提示词里该写什么](./02-poteto-mode.md#提示词里该写什么)处理第一种。本页处理第二种。

pstack 给你四条入口。`/how` 解释代码现在做什么。`/why` 挖掘它为什么长成这样。`/teach` 把两者融合成一份解释。`/recall` 重建你自己关于某个主题的近期上下文。每一个都让 agent 用你可以检查的语言解释自己。这就是你监督一个可能比你更了解代码的 agent 的方式。

![一名侦探拿着放大镜研究机器蓝图，机器人递来卷宗；她身后的证据板在 /how 和 /why 下串起线索。](./images/understanding.jpg)

## 从只读调查开始

当原因不清楚时，要发现，而不是要修复：

```text
/poteto-mode investigate why background jobs time out every few hours. give me what we know, what data you used, and your best hypotheses. don't change any code yet.
```

"don't change any code yet" 会把这条路由到 [Investigation 剧本](../../skills/poteto-mode/playbooks/investigation.md)。它运行 `/how`，对动机类问题追加 `/why`，并返回带引用的解释。如果是在多个选项之间做选择，它返回带权衡表的推荐。要求"你用了什么数据"会让 agent 把证据和猜测分开。当发现指向一个修复时，把修复作为一个新任务开始。

## 用 `/how` 追踪行为

```text
/how do we dedupe notifications? is there an n+1 when we look up subscribers?
```

问出你真正有的问题。[`/how`](../../skills/how/SKILL.md) 读取代码，并以资深工程师为你讲解该子系统的水平作答，包含运行时流程、关键类型和不那么显然的部分。对于大型子系统，它先分派两到四个只读探索者。对于范围窄的问题，它直接读取并解释。

## 用 `/why` 挖掘历史

```text
/why was the retry limit set to five? does the reason still hold?
```

[`/why`](../../skills/why/SKILL.md) 从源代码管理开始，然后并行查询你的 MCP 暴露的各类证据，例如 issue tracker、长篇文档、团队聊天、可观测性、错误跟踪和分析。报告引用一切，把直接证据与推断分开，并在记录稀少时使用"似乎是"这样的措辞。空结果也会报告，因为"没有人写下原因"本身就是一个答案。

两者自然组合。当你怀疑历史能解释这团乱麻时，`do why first then how` 是一条好 prompt。

## 用 `/teach` 真正理解它

```text
/teach me how this PR changes retries. convince me it fixes the cause and not the symptom.
```

当你需要的不只是摘要时，用 [`/teach`](../../skills/teach/SKILL.md)。它运行 `/how` 和 `/why`（对于小改动可能只运行其中之一），并把发现编织成一份平实的解释，逐图递进。"convince me"的框架值得沿用。它把解释变成你可以检验的论证，而不是一次导览。

它对 agent 自己的选择同样有效：

```text
/teach me why you implemented it this way and not with a queue. what did you trade off, and why?
```

教学对 agent 的帮助不亚于对你的帮助。一个必须解释自己工作的 agent，必须阅读代码并用证据支撑每一个论断，而不是自信地陈述后就继续。

## 用 `/recall` 重建你自己的上下文

```text
/recall catch me up on the export work from last week
```

[`/recall`](../../skills/recall/SKILL.md) 挖掘你自己近期的聊天以及共享记录（issue、先前的修复、仍在触发的错误），交回一份关于现状和下一步的简报。你的旧聊天持有新 agent 缺乏的上下文，所以在旧主题上开始新工作时，先加载它，再移交新的输入：

```text
/recall my work on the virtualized list from yesterday, then read this bug report.
```

如果你想恢复某一具体聊天，那是下面的 Session pickup 剧本，而不是 `/recall`。

## 用 Session pickup 接管先前的工作

当另一个 agent（或上周的你自己）留下一个进行到一半的分支时：

```text
/poteto-mode take over this branch. read the decision log, figure out what's done, and continue from there. don't redo finished work.
```

[Session pickup 剧本](../../skills/poteto-mode/playbooks/session-pickup.md)把先前的轨迹视为权威。它重建分支状态和决策，指出恢复点，并对照原始目标验证继承来的声明，而不是从零重新推导一切。

**陷阱：** 不要因为"反正 agent 会读代码"就跳过本页的技能。没有追踪模型就开始编辑的 agent，往往会在第一个看似合理的位置修复症状。先运行 `/how` 比第二次 bug 更便宜。

下一步：[设计改动](./04-design.md)。
