# 把它变成你自己的

poteto-mode 是某个人的风格。它下面的剧本、路由和模型角色同样适用于你的风格。本页涵盖：生成个人模式、从一次会话中捕获教训、修复仓库让 agent 不再重复犯错、编写一个聚焦的技能，以及在信任之前测试技能改动。

起步要比你想象的更小。第一天你不需要很多技能，甚至不需要整个插件。平实地写 prompt，观察 agent 在哪里失败，当同样的失败出现两次时再加一个技能或检查。

## 用 `/automate-me` 生成你自己的模式

```text
/automate-me
```

你不用描述自己的风格，因为 [`/automate-me`](../../skills/automate-me/SKILL.md) 会从你的历史中读出来。它挖掘你在当前工作区中近期的 transcript，找出重复出现的偏好——你喜欢怎样回复、怎样委派、怎样验证、怎样写代码、写散文和组织流程——然后问哪些模式才是真正的你。它通过 Cursor 内置的 `create-skill` 流程起草 `.cursor/skills/<your-name>-mode/SKILL.md`，让草稿经过 [`/unslop`](../../skills/unslop/SKILL.md)，并从 worktree 打开一个 PR，让你像审阅其他改动一样审阅它。

当你的习惯漂移时再运行一次：

```text
/automate-me update my mode skill with everything since its last edit
```

更新模式只挖掘技能上次改动以来的历史。它保留你没有违背的规则，修订有新证据的规则，并只为新出现的模式添加小节。

## 用 `/reflect` 捕获一次会话的教训

在某个教会你东西的任务之后，立即运行：

```text
/reflect that took way too long. capture what we learned so the next run doesn't repeat it.
```

[`/reflect`](../../skills/reflect/SKILL.md) 把 transcript 发给三个并行审阅者，然后由综合者把提案分成 `Accepted`、`Rejected` 和 `Backlog`，并在任何技能改动之前等待你的批准。只有当提案会改变未来的决策时才批准它。一次奇怪的会话是轶事，不是规则。

## 从环境层面修复

当你一次又一次纠正 agent 的同一错误时，修复属于仓库，而不是你的下一条 prompt。按维持效果排序：

1. 用架构或更好的数据结构让错误不可能发生。
2. 用类型，或用错误信息点明修复方法的 lint 或 CI 检查来阻止它。
3. 用测试捕获它。
4. 把它写成文档或 agent 规则。agent 跳过规则时什么也不会失败，所以这排在最后。

人工审阅不在这份清单上。一个必须在每个 PR 上抓住同一错误的审阅者，正是这里要解决的问题。[`/correct`](../../skills/correct/SKILL.md) 做这项功课：

```text
/correct agents keep calling the database client directly instead of going through the repository layer
```

它读取近期 commit、revert、审阅评论，以及解释变通做法的评论，然后把错误归类。一类错误发生两次才算数。它按提交逐一修复最频繁的类，选择能奏效的最高层级，并证明每个新检查都会在一个真实的过去错误上失败。它还在 agent 指令文件中维护一张表，把每条规则与强制执行它的东西配对，这样没有任何东西强制执行的规则会以"重复"的形式浮现。回复列出每一类及其证据、所选的层级，以及更高层级为什么行不通。

不带参数运行它，它会自己从历史中发现类别。`/reflect` 和 `/correct` 分工明确。`/reflect` 从一次会话改进技能。`/correct` 改变仓库，使一类错误无法卷土重来。当修复是一个新边界时，把它与 `/architect` 配对。[并行运行多个项目](./07-overnight.md#并行运行多个项目)有一条在整个仓库上同时做这两件事的 prompt。

## 编写一个聚焦的技能

当你已经知道想要捕获的工作流时：

```text
/poteto-mode write a skill for verifying database migrations in this repo
```

写技能匹配 [Authoring or modifying a skill 剧本](../../skills/poteto-mode/playbooks/authoring-a-skill.md)，它通过 Cursor 内置的 `create-skill` 路由，校验 frontmatter 和链接，并通过 Opening a PR 剧本交付结果。面向 agent 的散文有比面向人类的散文更高的标准，因为一句无用的句子会变成未来某个 agent 遵循的指令。让剧本来把守这个标准，而不是凭空手写 `SKILL.md`。

两种特殊情况有自己的生成器。一个必须驱动你的应用并证明行为的技能是验证技能，所以改用 [`/create-verification-skill`](../../skills/create-verification-skill/SKILL.md) 和 [`/maintain-verification-skill`](../../skills/maintain-verification-skill/SKILL.md)。一个用模型检查器、证明或其他验证器检查代码性质的技能是形式化验证技能，所以改用 [`/create-formal-verification-skill`](../../skills/create-formal-verification-skill/SKILL.md) 和 [`/maintain-formal-verification-skill`](../../skills/maintain-formal-verification-skill/SKILL.md)。[验证并交付](./06-verify-and-ship.md#用形式化验证技能证明一个性质)涵盖这两种。

## 用 `/technical-writing` 按标准写文档

技能不是你交付的唯一散文。对于文档、RFC、readme、PR 描述和 commit 消息：

```text
/technical-writing review the readme changes
```

[`/technical-writing`](../../skills/technical-writing/SKILL.md) 应用一套分层标准。它的目标是让疲惫的工程师第一遍读就能理解的散文。它先选择文档的模式（教程、操作指南、参考或解释），然后逐句处理：谁做什么、一句一个想法、没有可以有两种读法的内容。用它审阅你或 agent 刚写的东西，或在请求文档时一开始就点名它。

## 盲测一次技能改动

技能编辑会影响未来每一个会话，所以像对待实验一样测试它。采用别人的技能也是如此。在保留它之前，先确认它让你的工作在 agent 手里变得更好。

```text
/poteto-mode run the eval playbook on this skill change. same task for both variants, candidates stay blind.
```

当一个技能总是漏掉，而你知道它应该做什么时，在同一个任务里修改并测试它：

```text
/poteto-mode update the review skill so it flags missing migrations, and eval the change.
```

一开始就要求 eval 能让修改保持诚实。根据一次糟糕会话写出的修复容易过拟合那次会话，经过多次编辑技能就会漂移。Eval 会在漂移发布之前抓住它。

[Eval 剧本](../../skills/poteto-mode/playbooks/eval.md)围绕一种失败模式构建：观察者效应。知道自己正在被评估的 agent 会表现不同。所以候选 agent 在清洗过的目录中得到一个看起来自然的任务，绝不出现"eval"或"candidate"这样的词，也绝不知道彼此的存在。一个评审者在中性标签下为所有输出打分，而链条追踪的评分依据是每个候选实际读了哪些文件，而不是它声称读了什么。

在接受裁决之前亲自阅读每一份输出。如果你不同意评审者，先怀疑评分标准，再怀疑自己的判断。

## 用 `/make-bot-ui` 构建 bot UI

有一个情境性技能面向 Grok Bot 用户。[`/make-bot-ui`](../../skills/make-bot-ui/SKILL.md) 构建一个小页面，其按钮通过 webhook 例行程序唤醒 bot。例如，你可以滑动浏览一个审阅队列，每次滑动都让 bot 对该条目采取行动。你机器上的一个服务器持有 webhook 的发送者密钥，所以密钥永远不会到达浏览器或聊天。该技能还涵盖在 Tailscale 上暴露该页面。

**陷阱：** 不要因为技能在任务中途表现不佳就编辑它。在它自己的 PR 中修复它，让任务继续推进。夹杂在功能工作中交付的技能编辑对审阅不可见，也无法评估。

下一步：[配方与陷阱](./10-recipes-and-pitfalls.md)。
