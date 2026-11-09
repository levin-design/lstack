---
name: show-me-your-work
description: "为长时间运行或无人值守的工作保留可审阅的决策轨迹：用一个 TSV 日志记录每个决策一行（做什么、为什么、证据、结果）。默认仅本地保存；当审阅者需要这条轨迹来信任结果时再提交。用于 /show-me-your-work、自主或多阶段运行，或人类离开后回来审阅的工作。"
disable-model-invocation: true
---

# 展示你的工作

只保留一份权威日志。

## 格式

单个 TSV 文件，每个决策一行。单元格保持单行。证据是指针，不是散文。

复制 `references/decision-log-template.tsv`（表头行）来开始一份干净的日志。列包括：

- **ts.** ISO8601 时间戳。
- **phase.** 阶段或工作流。
- **decision.** 选择或完成了什么，一行。
- **why.** 用大白话说出原因。如果某个原则驱动了它，就直说，不要用术语标签。
- **evidence.** 能证明它的链接或路径：提交 SHA、PR 编号、`file:line`，或产物、trace、截图的路径。绝不写成一段话。
- **result.** 结果或谓词状态：`tests green`、`reverted`、`pixel-diff 0`、`INCONCLUSIVE`、`open`。

一个示例，用平实语言写成，让审阅者一眼就能读懂。

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## 记录一行

写每一条记录时，就像你在告诉同事你做了什么。用平实的词、具体的行动，不要 AI 腔或抽象术语（**unslop** 技能同样适用于日志文本）。

使用辅助脚本 `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`。它会写入 `ts`，在首次使用时写出表头，去掉多余的制表符/换行，并对以 `=`、`+`、`-` 或 `@` 开头的单元格加一个单引号前缀。直接用 `printf` 追加一行也可以，但如果单元格内容来自生成文本或用户提供的文本，同样要注意这些字符。

记录决策点和检查点，而不是每个动作：选择了一条分叉、完成了一个单元及其验证结果、一次转向或回滚及其触发原因、暴露出的阻塞、修复的关卡。对于循环运行，每次迭代记一行。跳过琐碎和不言自明的内容。

一次运行是一次 agent 对话，包括其后续轮次及对它的任何摘要。接手、替换 agent 或新开聊天都会开始一次新的运行。当一次运行向已有行的日志追加内容时，它的第一行使用阶段 `start`；在另一个运行的 `start` 行之后，它的第一行也是如此。因此，若一次运行在后续轮次回到日志，先读取日志末尾几行，看看此后是否有另一个运行写入。`start` 行会指明它之前那些不是本次运行写入的行的 `ts` 范围，其证据则标明本次运行，例如其 agent id。阶段 `start` 不得用于其他用途。

## 日志放在哪里

默认情况下，日志是工作产物，不提交。放在工作目录的 `decisions.tsv`，若同时有多个工作在进行，则放在 `.audit/<task-slug>.tsv`，并将其排除在 git 之外。

只有当工作足够宏大、审阅者需要这条轨迹才能信任结果时，才提交它。

## 规则

- 只追加。错误的判断用新的一行取代它。绝不编辑或删除历史。
- 优先使用已提交脚本产出的证据，而不是手工的一次性操作（**encode-lessons-in-structure** 原则技能）。

## 对照转录记录审计日志

在运行结束时、交回结果之前，检查日志是否说了真话。在会话的 Copilot 调试日志文件夹下读取本次运行的调试日志，可用时其路径由 `VSCODE_TARGET_SESSION_LOG` 指定。绝不要扫描其他工作区的文件夹。将本次运行的各行与实际发生的事情逐一核对。这些行的每一段都从本次运行的某个 `start` 行开始（如果日志由本次运行创建，则从第一行开始），到另一个运行的下一个 `start` 行结束：

- 检查每一行都对应真实的决策或行动。
- 检查每一行的证据可解析，并能显示该行所声称的内容。
- 影响过工作却未被记录的岔路、转向或放弃的方案都是缺口。补上它。

纠正日志，而不是纠正故事。审计绝不编辑或删除任何一行，即使是编造的行。当某一行既未记录真实决策也未记录真实行动，或其声称或证据有误时，添加一行取代它，写清实际发生的事和一个可解析的指针。本次审计不检查本次运行各段之外的行。如果本次运行自身的工作表明其中某行有误，就像对待任何错误判断一样，用新行取代它。

## 对轨迹进行跨模型评审

在交回结果之前，启动一个与完成工作的模型属于不同模型系列的 subagent。自我评审不能替代它。该 subagent 读取审计轨迹和本次运行的转录记录，然后标出用户应当注意的内容。这不是重做工作，而是扫描次优或有风险之处。

- 记录时证据薄弱或缺失的决策。
- 被跳过、或在转录记录中无证据却被声称完成的验证步骤。
- 事后看来有风险的选择（为时过早、范围蔓延、掩盖症状）。
- 用户随意扫读时否则会错过的缺口。

对于产生轨迹的运行，每次回复都以“Attention”小节结尾。先用单独一行写评审模型（`reviewed by <model>`），然后逐条列出指向具体行或时刻的标记。“No flags”是有效值；模型名称则不可省略。

## 审阅轨迹

从上到下阅读，跟随证据指针，抽样核对。GitHub 会把已提交的 TSV 渲染成表格。在终端中用 `column -s$'\t' -t decisions.tsv` 渲染。

## 与其他技能组合

其他技能把它们的审计轨迹交给这里处理，而不是另造一套。按名称引用它，让本技能拥有格式的定义权。不要重复描述各列。
