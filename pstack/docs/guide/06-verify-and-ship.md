# 验证结果并打开 PR

"它能编译"不是证据。[Prove It Works 原则](../../skills/principle-prove-it-works/SKILL.md)要求 agent 在报告成功之前检查真实制品，而你的工作是让"真实制品"可以被检查。本页涵盖：说明完成条件、审核测量数字、为你的应用生成验证技能、形式化验证测试很少触及的性质、打开 PR，以及推动它合并。

验证是大多数 agent 工作中最慢的一步，因为这一步通常要等人。让 agent 能做这一步，你就不再是瓶颈。跳过它，运行更多 agent 只会给你更多未经检查的工作要审阅。

![一架原型飞机在真实测试航道上飞行，她拿着秒表计时，机器人拍摄并对这次运行逐项打勾；终端显示 verify: pass, evidence: captured。](./images/verification.jpg)

## 事先说明完成条件

在第一条 prompt 里写清完成意味着什么，用什么措辞都行：

```text
/poteto-mode add json output to this command. text output stays byte-identical, the json parses, both run against the sample project. show me the evidence.
```

现在 agent 有三个可以运行的检查，而不是一种要去满足的心情。当回复回来时，它应该带着确切的命令和输出。如果某个检查无法运行，好的回复会写"inconclusive"。没有证据的自信回复是危险信号。

让检查匹配改动的类型：

- CLI 改动运行真实命令。
- UI 改动在运行中的应用里走一遍改动的流程。当它必须与参考实现逐像素一致时，[Visual parity 剧本](../../skills/poteto-mode/playbooks/visual-parity.md)会把截图与冻结的基线做 diff，而不是靠肉眼判断。
- 解析器或迁移重放一份保存的输入。
- perf 改动比较改动前后的 profile。
- 存储改动回读写入的值。

把证明作为一个你能亲自检查的制品来要求：先是失败的测试，然后是通过的测试；一段前后对比视频；trace；截图。如果修复已经合并，就在 main 上再要一次同样的检查。制品胜过看似合理的解释，因为你可以质疑它，而不必重放整个运行。

对于你不太信任的小 diff，[`/blast-radius`](../../skills/blast-radius/SKILL.md) 会找出它可能破坏的其他地方。它找出让改动安全的那一个事实，并通过运行代码而不是靠论证来证明它。

## 审核一个测量数字

前后对比数字是最容易意外弄错的证据。热的缓存、一侧使用调试构建，或从未在计时区内执行的工作，都可能产生一个令人信服的加速。在报告或依据某个数字行动之前，输入：

```text
/benchmark-checklist vet the export speedup before it goes in the pr
```

[`/benchmark-checklist`](../../skills/benchmark-checklist/SKILL.md) 提出七个问题，并要求每个问题都有来自一次运行的证据：

1. 什么限制了这个数字，为什么不是两倍？
2. 每一侧都按生产的方式调优了吗？
3. 结果是否突破了物理限制，例如磁盘带宽或核心数量？
4. 是否有任何东西出错或返回了错误输出？
5. 在交替运行中它是否可复现，有中位数和范围吗？
6. 它是否在用户实际等待的路径上端到端有意义？
7. 工作是否真的在计时区内完成？

结论以 faster、slower、no measurable difference 或 inconclusive 返回，附带运行次数、范围和限制因素。当它无法指出限制因素，或某一侧未调优时，它会说 inconclusive。`/poteto-mode` 已经在 Perf issue 和 Hillclimb 剧本内部运行该清单，所以你自己输入它，是在这些剧本之外做了测量，或别人的数字看起来好得可疑时。它是 [Explain the Number 原则](../../skills/principle-explain-the-number/SKILL.md)的可操作形式。

## 创建项目验证技能

上面关于 UI 的那一条隐含了一个真实要求。agent 需要一种脚本化的方式来驱动你的应用。如果你的项目已经有了，很好。如果没有，运行：

```text
/create-verification-skill
```

[`/create-verification-skill`](../../skills/create-verification-skill/SKILL.md) 采访的是仓库，而不是你。它会弄清用户会触碰什么、应用如何在本地启动、用什么可以驱动它（优先使用现有 harness，否则用浏览器和 CDP、PTY 或普通 HTTP）、什么证据能证明行为，以及两个实例能否并排运行。它只问你代码无法回答的问题。

它会写入 `.cursor/skills/verify-<app>/`，这是面向 agent 的指令，包含确切的 Launch、Doctor、Drive、Evidence 和 Cleanup 小节，一个用于其附带脚本的 Helpers 小节，以及 `features/` 下的 feature map，索引应用做什么以及什么结果证明每个功能可用。该技能附带一个[可参考的 feature-map 示例](../../skills/create-verification-skill/references/feature-map-example/)，包含 README 索引和每个功能一个文件，使用四个必需的 H2。在交接之前，生成器会端到端证明该技能一次：启动、doctor 检查、驱动一个功能、采集证据、清理，然后确认证据在清理后仍然存在。如果这个证明失败，就不要使用输出。

从那时起，"在应用里验证它"就是任何 agent 都能执行的一步，就在这个仓库里，不需要再做 setup 对话。当你想让证明以特定形式出现时，在 prompt 中点名它：

```text
/poteto-mode build the bulk-archive action. use /verify-<app> to verify your changes and show me a video and screenshots as proof.
```

```text
/poteto-mode repro this with /verify-<app>. if it repros on main, fix it and show me a video as proof.
```

一旦验证技能可用，[`/swarm`](../../skills/swarm/SKILL.md) 就可以按 feature-map 条目拆分完整的一轮验证并汇总结果。一群验证者还能在足够大的样本上确认性能收益，或在 PR 交付前对应用做回归模糊测试。

把验证技能当作基础设施，而不是一次性产物。提交它，让团队里的每个人和每个 agent 都以同样的方式驱动应用。然后[构建杠杆](../../skills/principle-build-the-lever/SKILL.md)。当 agent 不断写一次性脚本来点击应用时，要求一个小的控制 CLI 让技能来调用。agent 消耗的 token 更少，每次运行都可重复。agent 用得好的 CLI 具有这些特征：

- 少量可组合的命令，每个都做真正的工作，而不是许多薄命令。
- 任何破坏性操作都有 `--dry-run` 选项。
- 子命令逐步显露功能，而不是一次全给。
- 错误消息说明该怎么做。
- 丰富的 `--help` 文本。
- 机器可读的输出，例如 JSON。

顺便把开发环境也做成可重复的：种子数据、测试用户，以及一条每次都同样拉起环境的命令。

## 让验证技能保持诚实

应用会变，feature map 会过时。至少每天运行一次，最好从定时自动化运行，这样没人需要记得：

```text
/maintain-verification-skill
```

[`/maintain-verification-skill`](../../skills/maintain-verification-skill/SKILL.md) 审计生成的技能：每个功能并行一个只读源码读取者，然后一次实时检查驱动每个已映射的功能。它以三种结果之一结束。`clean` 表示完整覆盖且没有需要交付的内容。`changed` 表示一个只包含已证明修正的 PR，且限于验证技能自己的目录。`blocked` 说明阻塞原因。它绝不编辑产品代码。如果实时检查发现产品回归，它会报告回归，而不是用文档编辑把它掩盖。

## 用形式化验证技能证明一个性质

验证技能证明你驱动的路径。有些 bug 活在没人驱动的路径上：两次重叠的重试、在写入中途过期的锁、乱序到达的状态变更。测试很少触及这些情况。对于这类 bug 代价高昂的代码，运行：

```text
/create-formal-verification-skill
```

[`/create-formal-verification-skill`](../../skills/create-formal-verification-skill/SKILL.md) 从代码中挑选目标：代码作出的承诺，其破坏会伤害用户，且测试很少触及会破坏它的情况。它挑选最强的目标，而不是最容易验证的。你也可以点名一个区域或一个 bug 作为起点：

```text
/create-formal-verification-skill the job lease and retry logic. a job must never run twice at once.
```

问题决定工具。事件是否会以糟糕的顺序发生，适合对设计的小模型做模型检查，TLA+ 是任何语言中这类问题的默认选择。代码是否对每个输入都表现正确，适合在代码上运行的验证器。如果没有任何验证器能运行在你的语言上，agent 会说明这一点，并用生成的输入测试真实代码，而不是手写函数模型。一个必须在所有规模上成立的性质可能需要证明。agent 会告诉你它选择了哪个工具以及为什么。

它验证一个性质，并展示该性质在代码的一个破坏变体上失败，因为你从未见过失败的检查什么也证明不了。当当前代码已经破坏该性质时，你会得到一个以你代码术语表示的简短步骤序列作为反例。性质保持原样陈述，所以发现仍然是发现。除非你要求，产品代码不会改变。

它会写入一个项目本地技能，告诉下一个 agent 某项改动是否触及已验证的代码、如何用一条命令运行检查，以及如何区分真实 bug 和建模错误。在交接之前，生成器会在一个破坏该性质的一次性改动上遵循该技能一次，检查必须抓住它。交接内容说明验证了什么、用什么工具和边界、检查发现了什么、以及它不覆盖什么。一次通过覆盖的是模型或边界，而不是整个系统。

该技能还会记录每个检查覆盖哪些代码，以及检查最后一次匹配这些代码的 commit。跳过该技能的合并和重构可能让检查继续在一个已消失代码的描述上通过。在这些操作之后，运行 [`/maintain-formal-verification-skill`](../../skills/maintain-formal-verification-skill/SKILL.md)。它会从代码更新验证、重跑它、展示每个更新后的检查仍能失败，并告诉你每个失败是验证的漂移还是代码的 bug。

## 用状态图展示行为

模型术语的反例能说服你。拥有该行为的 PM 或设计师需要用他们的术语看到它。运行：

```text
/statechart what the user sees when they edit a note offline
```

[`/statechart`](../../skills/statechart/SKILL.md) 从 TLA+ 模型生成用户所见内容的 Mermaid 状态图，因此图和被检查的模型不会彼此漂移。读者的规则（"你离线时永远不会看到 Synced"）变成不变量。图中标出每个违反规则的状态，报告用读者的语言给出到达它的最短路径。在交接之前，agent 会在真实代码中复现每条 bug 路径，这样建模错误不会作为 bug 到达读者那里。

## 打开 PR

```text
/poteto-mode open the pr. small ordered commits, evidence in the description.
```

[Opening a PR 剧本](../../skills/poteto-mode/playbooks/opening-a-pr.md)从 worktree 工作，把工作 rebase 成小型有序 commit，清理 diff，unslop 散文，并返回 PR 链接。五个窄 PR 胜过一个臃肿的 PR，堆叠的后续 PR 胜过不断长大的分支。

## 用 Babysit 把 PR 推动到可合并

打开的 PR 会立即开始收集阻塞项。检查失败、审阅者评论、主干前进。把这种杂务交给 [Babysit 剧本](../../skills/poteto-mode/playbooks/babysit.md)：

```text
/poteto-mode babysit this pr. get it green.
```

Babysit 盯着 PR，在可用时使用内置的 GitHub 或 Origin CLI 监视器，并按顺序处理阻塞项：冲突、然后是审阅 thread、然后是 CI。每个已知修复都批处理进一次 push，这样检查只重启一次，而不是每次修复后都重启。评论分类是怀疑式的，因为人和机器人都把真正的捕获和噪音放进同一个列表。真实发现得到修复，噪音则在 thread 上发布反证后驳回。当你只想要状态时，问得更小，Babysit 会直接回答而不启动循环：

```text
/poteto-mode check on pr 123. anything outstanding?
```

Babysit 停在可合并状态。它绝不合并，即使一切绿灯，因为合并是另一个决策。

## 用 Shipping 落地整个栈

Green 不等于安全。当你准备落地时，说出来：

```text
/poteto-mode land the stack.
```

[Shipping 剧本](../../skills/poteto-mode/playbooks/shipping.md)在武装任何东西之前独立验证每个 PR。每个 PR 一个全新 agent 实时证明行为，评判改动的 agent 永远不是写它的那个。然后 Shipping 只从底部落地连续的已验证序列，默认一次一个 PR 通过 GitHub，或在 Origin CLI 可用时通过 Origin，并报告第一个破坏链条的 PR。一个已验证的 PR 停在一个未验证的 PR 之上时会等待，因为合并它会把缺口拉到下面。

下一步：[在你睡觉时继续工作](./07-overnight.md)。
