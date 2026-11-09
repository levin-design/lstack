# 配方与陷阱

值得复制的 prompt，然后是每个人都会犯一次的错误。把路径和完成条件换成你自己的。配方故意写得随意。实践中就是这样输入的，而技能能很好地读出意图。

![她从配方盒旁品尝做好的菜，机器人在烹饪，台面上方钉着的卡片写着 /how、/tdd 和 /loop。](./images/recipes.jpg)

## 理解一个陌生的子系统

```text
use /how first to understand how this initialization works. then use /why to figure out why it broke recently.
```

先机制，后历史。每个技能的报告都会告诉你它搜索了哪些来源，这样你就知道答案建立在什么基础上。

## 改动代码之前先重述嘈杂的报告

```text
/poteto-mode read this thread. restate the underlying issue in your own words, in plain english. don't change any code yet.
```

误读会在重述中暴露，纠正它的代价是一条消息。在 agent 陈述自己的理解之前，先保留你自己的理论。`/in-your-own-words` 只要求重述，不带剧本。

## 发送之前先磨锐 prompt

```text
/sharpen write the onboarding doc for the new billing service.
```

agent 会点明专家会做而你没要求的事、他们会从什么原始材料开始、他们的方法和工具，以及一个外部检查来证明结果正确。它交回重写后的 prompt 来要求这些内容，不执行任务。改写稿读着对了就发送它。

## 选择之前先做原型

```text
/poteto-mode prototype a few options for the settings layout. put them behind a switcher and send me screenshots of each.
```

你从能运行的东西里选择，而不是从描述里选择。agent 在这个过程中用自己的方式回答布局和时序问题。

## 把确定的设计变成计划

```text
/poteto-mode turn this design into a plan. small verifiable PRs, each with its own proof.
```

只在设计确定之后才要。计划就是交付物，它会指出将执行它的剧本。

## 为设计获取第二意见

```text
ask /arena for a second opinion on this thread and our approach
```

你当前的设计成为多个候选之一，综合分析会告诉你评审组是找到了更好的东西，还是确认了你已有的方案。相对于一个难以逆转的设计，这点成本微不足道。

## 并行检查独立分片

```text
/swarm check every package under packages/ against its check.sh. one worker per package. one report.
```

每个 worker 负责一个包。父级等待每个分片，返回一份 `PASS`、`ISSUES` 或 `BLOCKED` 报告，而不是原始 worker 输出堆。

## 以怀疑态度审阅分支

```text
/interrogate the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's an actual bug or regression in behavior.
```

这些限定词发挥了真正的作用。"don't change anything yet"让它保持只读，而挑剔规则预先过滤噪音，让已验证的发现值得你花时间。

## 通过失败的测试修复 bug

```text
/poteto-mode repro the duplicate write first. if there's a cheap test path, /tdd it. then fix and rerun.
```

"if there's a cheap test path"很重要。通过脆弱的 mock 强行写测试，证明力不如运行真实命令，而剧本允许说明这一点。

## 带证明地复现并修复报告

```text
/poteto-mode repro this with /verify-<app>. if it repros on main, fix it and show me a video as proof.
```

"if it repros on main"让运行在 bug 已经消失时提前停止。视频让你在读 diff 之前检查修复。

## 证明测试很少触及的性质

```text
/create-formal-verification-skill the retry queue. a message must never be delivered twice.
```

你在声明的范围内对每一种情况检查一个性质，如果代码已经破坏它，你会得到以代码术语表示的反例，以及一个可供下一个 agent 在该代码有任何改动时运行的项目技能。

## 发布之前审核数字

```text
/benchmark-checklist vet this 40% speedup before it goes in the pr description
```

你会得到 faster、slower、no measurable difference 或 inconclusive，附带运行次数、范围和限制该数字的因素。

## 停止反复纠正同一错误

```text
/correct agents keep adding new config flags without registering them in the schema
```

修复以架构、类型、lint 或测试的形式落在仓库里，这样下一个 agent 无法再犯这个错误。

## 只问怎么做，不启动工作

```text
/poteto-help how do i get poteto-mode to stay on every turn?
```

你会得到一个回答、一条可发送的 prompt，以及一个来源链接。在你发送那条 prompt 之前什么都不会运行。

## 离开时让运行保持诚实

```text
im going to bed, keep going autonomously until every fixture passes. do not stop. keep a decision log i can audit in the morning.
```

完整契约在[过夜页面](./07-overnight.md)。当任务和完成条件已经在对话中时，简短形式就够用。

## 重定向一个漂移的运行

引导 prompt 只有一行：

```text
i said the goal is to repro. i did not ask for a fix yet.
```

```text
apply prove it works. show me the real output, not the build log.
```

```text
/unslop that, no emdashes
```

你很少需要更多词。你需要正确的名称，而[原则页面](./08-principles.md)就是词汇表。

## 用平实的话得到回复

```text
/bro
```

这就是整条 prompt。[`/bro`](../../skills/bro/SKILL.md) 像一个人对另一个人说话那样重述最后一条消息，没有术语，更短。当回复技术上很详尽而你仍然不知道它在说什么时使用它。

## 追上你留下运行的聊天

```text
/ketchup
```

[`/ketchup`](../../skills/ketchup/SKILL.md) 用平实的语言告诉你自你最后一条消息以来发生了什么变化，然后列出每一个等你处理的事项及其建议、证据和风险。它在报告的同时不改变任何东西。

如果想看视频版的追赶，运行 [`/ketchup-video`](../../skills/ketchup-video/SKILL.md)。它用一段带字幕的幻灯片短视频展示发生了什么，并在下方以文字列出等你处理的事项。

## 陷阱

- **在 prompt 中罗列技能。** "先用 /how 再用 /architect 再用 /arena"会重排剧本已经排好的步骤。说清目标和约束。只在覆盖默认值时点名技能。
- **含糊的完成条件。** "把它做得更好"没有给 `/loop` 任何可检查的东西。给一个能通过或失败的命令或制品。
- **一开始就抛出你的原因猜想。** agent 会在你指向的地方搜索。先让它重述问题，再分享你的直觉。
- **接受第一个设计。** 一次尝试会锁定模型想到的第一个形态。要原型或 `/architect`，从证据中选择。
- **打磨抽象计划。** 对没有代码支撑的计划做对抗性审阅，会发明永远不会发生的风险。用原型敲定悬而未决的问题，然后审阅真正构建出来的东西。
- **多个并行 agent 共用一个 worktree。** 它们互相覆盖，没人能分辨哪个 agent 改了什么。把它们作为 cloud agent 运行，或说"own worktree per attempt"。
- **在信任循环之前就开循环。** 无法验证自己工作的循环只会更快地产出未经检查的工作。先让验证技能跑通。
- **信任未审核的数字。** 热的缓存或跳过的代码路径可能伪造一个加速。在数字出现在任何地方之前运行 `/benchmark-checklist`。
- **手工纠正同一错误。** 聊天中的纠正只帮助一次运行。`/correct` 修复仓库，让之后的运行不再重复它。
- **用 `/arena` 做覆盖。** `/arena` 重复同一份设计或代码简报，然后选一个基础并嫁接最佳部分。`/swarm` 划分分片或声明的竞赛分支并汇总成一份报告。
- **接受每一条审阅评论。** 机器人和人类都把真正的捕获和噪音放进同一个列表。`/interrogate` 只保留重跑能证明的发现，并列出它丢弃了什么以及为什么，你可以往任一方向推翻。
- **把 `auto` 当作 model slug。** `auto` 和 `inherit-parent` 的意思是"省略 model 字段，让 subagent 继承父聊天模型"。[设置](./01-setup.md)涵盖了角色。
- **凭绿灯构建就报告成功。** 构建证明它能编译。要真实命令、流程、存储值或 profile，并期望证据出现在回复中。
- **凭空手写 `SKILL.md`。** 通过 [Authoring or modifying a skill 剧本](../../skills/poteto-mode/playbooks/authoring-a-skill.md)路由，让校验和审阅发生。

这就是整份指南。如果你跳着读了，回到[设置](./01-setup.md)并运行一个真实任务。习惯来自使用，而不是阅读。

回到[指南索引](./README.md)。
