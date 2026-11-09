---
name: poteto-help
description: 引导用户完成 pstack 安装配置、使用 /pstack，以及为任务挑选合适的技能、剧本或原则。当用户提出 pstack 帮助类问题时使用。
disable-model-invocation: true
---

# Poteto 帮助

回答用户关于 pstack 的问题，递给他们一段可以直接发送的提示词，并链接答案出处所在的文件。对于帮助类问题，不要开始干活。用户问的是怎么做，而一次 pstack 运行会消耗真实 token，所以把提示词交给他们去发送。

要求干活的请求，例如 "use pstack to fix this bug"，不算帮助类问题。阅读 [`poteto-mode`](../poteto-mode/poteto-mode.md)，在其指导下完成工作，并顺带提一次：Copilot 没有 Custom Mode，每个新任务都要重新发送 `/pstack`。

本文件把问题映射到承载答案的技能与指南页面。那些文件才拥有细节。引用前先阅读你要路由到的文件，当它与本映射冲突时以它为准。这里的链接指向已安装的插件，用户可能打不开，所以给用户该文件的公开副本：`https://github.com/cursor/plugins/blob/main/pstack/` 后接其路径。

## 弄清他们的需求

从消息和对话中推断需求。已明确的情境，例如 "which skill reviews a PR?"，直接进入对应小节。如果需求仍不清楚，问一个多选题，选项如下，然后只回答他们选中的小节：

- 完成安装配置
- 用 `/pstack` 启动任务
- 为某个情境挑选技能
- 修复出错的运行
- 定制 pstack

检查会影响答案的状态，并且只在确实影响时才提及：

- 没有 `.github/skills/pstack/references/pstack-models.md` 意味着该用户还没跑过 setup-pstack 技能，因此每个角色都继承聊天模型。
- 项目中没有 `verify-*` 技能或其他应用 harness 意味着 agent 没有脚本化方式来驱动应用。当问题涉及证明某项改动可用时，提及 `/create-verification-skill`。
- 项目中没有形式化验证技能意味着除测试能覆盖的部分之外，没有性质被检查。当问题涉及竞态、不变量或其他测试很少命中的情况时，提及 `/create-formal-verification-skill`。若已存在一个，而它覆盖的代码在其记录为最后同步的提交之后发生了变更，且问题触及该代码，则提及 `/maintain-formal-verification-skill`。

当模型文件缺失且这确实重要时，询问用户现在是否想为每个角色挑选模型和推理预算。重要的情况是：用户是新手、问题关于安装配置或成本，或答案取决于运行哪些模型。每次对话最多问一次。如果需求也还不清楚，把两个问题一起问。给出两个选项：

- 现在：让他们说 "set up pstack models"，同时也回答他们的问题。
- 以后：回答他们的问题，并加一句说明：在他们设置模型之前，每个角色都继承聊天模型。

## 安装配置

1. 该技能已安装在项目的 `.github/skills/pstack/`。无需安装插件。
2. 按名称调用 [`setup-pstack`](../setup-pstack/setup-pstack.md)，例如 "set up pstack models"。它会询问推理预算、为每个角色映射模型，并写入 `.github/skills/pstack/references/pstack-models.md`。随后它会各提供一次机会，为项目生成验证技能和形式化验证技能，除非项目已有其一。
3. 用 `/pstack`、一个目标和一个能通过或失败的检查来启动真实任务。

在用户调用技能之前，安装不会改变任何东西。这里只有 `/pstack` 是斜杠命令。其他技能在 `/pstack` 读取它们时加载，或由用户按名称请求时加载。[README](https://github.com/cursor/plugins/blob/main/pstack/README.md) 与 [指南第 1 页](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/01-setup.md) 有上游细节。可按 [`references/prompting.md`](references/prompting.md) 与他们一起敲定第一条提示词。

如果担心成本，说明 token 花在哪里以及如何少花。pstack 会把额外的 token 花在子代理和评审小组上。重跑 setup-pstack，选一个更小的预算或更便宜的模型。角色设为 `inherit-parent` 时运行在聊天所用模型上，当聊天用更便宜的模型时能省 token。更短的评审列表会运行更少的子代理，每个条目一个。把 `/pstack` 留给需要严谨的工作。

本副本已适配 Copilot。内置技能、剧本和脚本都位于 `.github/skills/pstack/references/` 下。仅 Copilot 的约束：子代理通过 `runSubagent` 运行，不能在后台运行或被恢复；模型标签来自用户的选择器；没有 Bugbot、Automations、Custom Modes 或云端 VM。

## 用 `/pstack` 启动任务

`/pstack` 把任务匹配到剧本，把剧本的步骤复制到待办列表，并按步骤需要运行其他技能。被跳过的步骤会以 `skip: <reason>` 留在列表里。好的提示词会说明目标以及如何判断完成。它不列技能，因为手写的顺序往往会丢掉或打乱剧本会保留的步骤。帮助措辞前先阅读 [`references/prompting.md`](references/prompting.md)。[指南第 2 页](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/02-poteto-mode.md) 有示例。

每条 `/pstack` 消息都携带该任务的模式。Copilot 没有等价的 Custom Mode，所以每个新任务都以 `/pstack` 开始。对话中途说 "new task" 会让模式匹配一份全新的剧本。`/pstack` 已经用 `poteto-agent` 来运行其剧本步骤派生的子代理。想让你自己的子代理保持同样风格，用 `agentName: "poteto-agent"` 派生它。

## 挑选技能

默认答案是 `/pstack`，它会在步骤需要时运行大多数其他技能。当用户想要的比剧本给出的更多或更少时，直接点名某个技能。推荐前先阅读该技能，并给出一条示例提示词。

| 用户想要 | 技能 |
|---|---|
| 以严谨的方式完成任何非平凡任务 | [`/pstack`](../poteto-mode/poteto-mode.md) |
| 在开工前确认 agent 已理解他们的目标与问题 | [`/in-your-own-words`](../in-your-own-words/in-your-own-words.md) |
| 在发送前把提示词改得更深入而非更长：顶尖专业人士会补充什么、他们的原始素材与方法，以及一次外部校验。它只返回提示词，不执行任务 | [`/sharpen`](../sharpen/sharpen.md) |
| 了解代码当前如何工作，或新代码应放在哪里 | [`/how`](../how/how.md) |
| 了解代码为何是这种形态，或某个数字从何而来 | [`/why`](../why/why.md) |
| 用通俗方式理解某个改动或子系统 | [`/teach`](../teach/teach.md) |
| 追上自己近期在某个主题上的工作进展 | [`/recall`](../recall/recall.md) |
| 用通俗语言和小图示了解本次对话自他们上次发言以来的变化，列出所有等待他们处理的事项，且仅凭回复即可决策 | [`/ketchup`](../ketchup/ketchup.md) |
| 像 `/ketchup` 一样补课，但以带字幕的短视频幻灯片呈现，等待中的决策以文字列在下方 | [`/ketchup-video`](../ketchup-video/ketchup-video.md) |
| 了解一个小 diff 可能在自身之外破坏什么 | [`/blast-radius`](../blast-radius/blast-radius.md) |
| 在编写跨越函数边界的代码前先定下类型和模块形态 | [`/architect`](../architect/architect.md) |
| 对同一份简报获得多个尝试并合并为最佳版本 | [`/arena`](../arena/arena.md) |
| 以子代理方式对切片并行检查，或让 worker 竞速 | [`/swarm`](../swarm/swarm.md) |
| 让不同模型审查 diff 并尝试攻破它 | [`/interrogate`](../interrogate/interrogate.md) |
| 当存在廉价的本地测试时，以测试先行方式修 bug | [`/tdd`](../tdd/tdd.md) |
| 对 `.ts` 或 `.tsx` 工作应用 TypeScript 规则 | [`/typescript-best-practices`](../typescript-best-practices/typescript-best-practices.md) |
| 审查前去掉注释，并由未编写这些注释的审查者进行 | [`/no-comments`](../no-comments/no-comments.md) |
| 清除文字中的 AI 痕迹 | [`/unslop`](../unslop/unslop.md) |
| 按标准撰写文档、RFC、README、PR 描述或提交信息 | [`/technical-writing`](../technical-writing/technical-writing.md) |
| 用大白话再听一遍上一条回复 | [`/bro`](../bro/bro.md) |
| 给 agent 一种脚本化方式驱动应用并证明行为 | [`/create-verification-skill`](../create-verification-skill/create-verification-skill.md) |
| 让验证技能及其功能映射与应用重新对齐 | [`/maintain-verification-skill`](../maintain-verification-skill/maintain-verification-skill.md) |
| 对测试很少触及的竞态、不变量或其他性质做形式化验证 | [`/create-formal-verification-skill`](../create-formal-verification-skill/create-formal-verification-skill.md) |
| 在覆盖的代码变更后重新对齐形式化验证，并判断失败是漂移还是缺陷 | [`/maintain-formal-verification-skill`](../maintain-formal-verification-skill/maintain-formal-verification-skill.md) |
| 用经 TLA+ 模型检验的图表向 PM 或设计师展示用户所见，并给出到达每个违规状态的最短路径 | [`/statechart`](../statechart/statechart.md) |
| 在汇报或依据某个性能数字行动前先校验它 | [`/benchmark-checklist`](../benchmark-checklist/benchmark-checklist.md) |
| 执行大型或跨领域的改动，或执行离开后回来再审查的改动 | [`/figure-it-out`](../figure-it-out/figure-it-out.md) |
| 在运行期间记录决策日志，并在结束后回顾 | [`/show-me-your-work`](../show-me-your-work/show-me-your-work.md) |
| 为每个角色挑选模型和推理预算 | [`setup-pstack`](../setup-pstack/setup-pstack.md) |
| 把他们自己的工作习惯转化为个人模式技能 | [`/automate-me`](../automate-me/automate-me.md) |
| 把已完成任务中的经验转化为技能修改 | [`/reflect`](../reflect/reflect.md) |
| 阻止 agent 在本仓库重复同样的错误 | [`/correct`](../correct/correct.md) |
| 构建一个页面，其按钮通过 webhook 唤醒 Grok Bot | [`/make-bot-ui`](../make-bot-ui/make-bot-ui.md) |
| 在 pstack 中找到自己的路 | `/poteto-help` |

如果紧邻本目录的某个技能目录未出现在表中，阅读其 frontmatter 并按 description 路由。`principle-*` 目录在下面的原则部分覆盖。

容易混淆之处：

- `/how` 解释代码做什么。`/why` 解释原因。`/teach` 运行其一或两者，并通俗地解释结果。
- `/arena` 给每个 worker 同一份简报并合并最佳部分。`/swarm` 把工作切分为切片或一场竞速，并返回一份报告。
- `/architect` 在定下设计后立即实现。加上 "with checkpoint" 可在写代码前先审查设计。
- `/interrogate` 审查 diff。`/blast-radius` 寻找 diff 之外的破坏，并证明使改动安全的那一个事实。
- `/recall` 跨越近期对话重建上下文。`/ketchup` 只覆盖用户上次消息以来的本次对话。恢复某个特定的对话或分支属于 Session pickup 剧本。
- `/figure-it-out` 设计一次严谨的运行。Orchestrate 剧本运行一个跨越数天和许多 PR 的程序。Autonomous run 剧本把一个任务推进到完成条件。

本 Copilot 副本中不包含：

- `cursor-team-kit` 插件。**unslop** 与 **no-comments** 技能已内置，但项目自己的 UI 与 CLI harness 需由项目提供。
- 重复唤醒机制、Custom Modes、Automations 以及 authoring 内置项都是 Cursor 特性，在 Copilot 中没有直接等价物。
- pstack 没有 `/orchestrate` 命令。Orchestrate 是一个 `/pstack` 剧本。

## 剧本与原则

剧本是 `/pstack` 内部的步骤列表，不是技能，因此没有斜杠命令。在 `/pstack` 内，描述任务即可选中一个，而以下短语直接点名：

- "babysit this pr" 或 "check on pr 123" 运行 Babysit。它把 PR 推进到可合并就绪并停在那里。除非用户要求 merge、land 或 ship，否则不合并。
- "land the stack" 运行 Shipping。
- "take over this branch" 运行 Session pickup。
- "pause safely" 运行 Pause safely。
- "full autopilot on this queue" 运行 Autopilot-full。"autopilot, don't merge" 运行 Autopilot-stack。
- "run the eval playbook" 运行 Eval。

没有 `/pstack` 时，诸如 "babysit this pr" 的短语可能改为启动一个通用的 PR 助手。[`poteto-mode`](../poteto-mode/poteto-mode.md) 的 Playbooks 小节列出了每个剧本及其适用时机。[指南第 6 页](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/06-verify-and-ship.md) 覆盖打开、照看和落地 PR。

pstack 没有规划技能。Copilot 的 plan 模式可与之配合。对于跨越阶段或堆叠 PR 的工作，向 `/pstack` 要一个计划会运行 [Multi-phase plan 剧本](../poteto-mode/playbooks/multi-phase-plan.md)，它写出计划而不实现它。对于设计问题，Prototype 剧本或 `/architect` 先在代码中定下它。

原则是单条规则的技能，由 `/pstack` 读取并在回复中引用。用户很少直接调用其中之一。他们改用名字来引导，例如 "apply prove it works. show me the real output."。要按需加载一个，按名称请求它并阅读 `references/skills/principle-<name>/` 下的文件。[指南第 8 页](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/08-principles.md) 列出了它们。

## 修复出错的运行

| 症状 | 修复 |
|---|---|
| 模式在几轮之后不再生效 | Copilot 没有 Custom Mode。每个任务都以 `/pstack` 开始。 |
| 某个问题被当成上一个任务的下一步 | 说 "new task"，或说明这一轮不需要该模式。 |
| 新的模型选择没有生效 | 模型文件只对新的子代理调用生效。检查 `.github/skills/pstack/references/pstack-models.md` 以及选择器中的准确标签。 |
| 运行成本超出预期 | 见“安装配置”下的成本段落。 |
| 某个技能没有自动加载 | 内置技能只在 `/pstack` 读取它或用户按名称请求时加载。`/pstack` 不会运行每一个技能。 |
| 并行 agent 互相覆盖 | 给每个 agent 各自的工作树。Copilot 子代理共享工作区，因此要把写入者串行化或隔离。 |
| 通宵运行有进展却什么都没完成 | 长时间运行需要一个能通过或失败的检查，而不是一个时长，并且必须由人重新调用。Copilot 没有 `/loop`。见 [指南第 7 页](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/07-overnight.md)。 |
| 回复仅凭构建通过就宣称成功 | 要求给出真实命令、流程、存储值或 profile。这就是 prove-it-works 原则。 |

运行发生漂移时，[`references/prompting.md`](references/prompting.md) 有一行式引导。[指南第 10 页](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/10-recipes-and-pitfalls.md) 有更多陷阱和值得照抄的食谱。

## 定制 pstack

- [`/automate-me`](../automate-me/automate-me.md) 根据用户自己的历史起草一个个人模式技能，与 `/pstack` 配合使用。
- 会话结束后用 [`/reflect`](../reflect/reflect.md) 把其中的经验转化为经用户批准的技能修改。
- `/pstack write a skill for <workflow>` 运行 authoring 剧本。eval 剧本以盲测方式测试技能改动。
- 在它自己的 PR 中修复表现不佳的技能，而不是在它出错的功能工作里修。

[指南第 9 页](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/09-make-it-yours.md) 覆盖以上各项。

## 回复

以答案开头。最多给一条放在代码块里的示例提示词，合适时从 [`references/recipes.md`](references/recipes.md) 改编，然后给出该文件的链接。保持简短，除非用户要的是整张地图。
