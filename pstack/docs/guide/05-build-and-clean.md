# 构建改动并清理 diff

构建类剧本共享同一种纪律。你说出观察到什么，让剧本去要求证据。本页展示每个常见构建任务的 prompt 该写什么，然后讲保持 diff 可审阅的清理习惯。

## 用你已知的信息喂给每个构建剧本

bug prompt 陈述症状并要求先复现：

```text
/poteto-mode this command emits two records after a retry. repro first, then fix and verify.
```

feature prompt 陈述行为以及什么绝不能变：

```text
/poteto-mode add a --json flag. text output stays byte-identical. verify both forms.
```

refactoring prompt 在结构移动之前钉住行为：

```text
/poteto-mode move parsing into one module, zero behavior change. record the current output first and prove it's unchanged after.
```

perf prompt 陈述测量值，而不是印象：

```text
/poteto-mode startup takes 1.8s on this fixture. trace it, fix the measured cause, show me before and after.
```

每一条都会路由到对应的剧本（[Bug fix](../../skills/poteto-mode/playbooks/bug-fix.md)、[Feature](../../skills/poteto-mode/playbooks/feature.md)、[Refactoring](../../skills/poteto-mode/playbooks/refactoring.md)、[Perf issue](../../skills/poteto-mode/playbooks/perf-issue.md)），剧本会补上你没写的步骤：修复前先复现、实现前先命名数据结构、重构前先钉住行为、优化前先做 profile。

如果要持续改进某一个数字，有 [Hillclimb 剧本](../../skills/poteto-mode/playbooks/hillclimb.md)。给它指标、目标和尝试次数下限，它会带着冻结的测量 harness 一次循环一个假设。它保留赢的方案，回退其他一切。

两个 perf 剧本都会对它们的数字运行 [`/benchmark-checklist`](../../skills/benchmark-checklist/SKILL.md)。Perf issue 会审核其基线以及之后的每一个数字，Hillclimb 会在冻结之前审核其 harness。[验证并交付](./06-verify-and-ship.md#审核一个测量数字)展示了什么时候该自己输入它。

有时你想在任何修复之前先弄清原因。对于活跃症状，例如泄漏、空闲 CPU 空转或视觉故障，[Runtime forensics 剧本](../../skills/poteto-mode/playbooks/runtime-forensics.md)会对运行中的进程加装观测。对于你已经采集的 profile，[Trace forensics 剧本](../../skills/poteto-mode/playbooks/trace-forensics.md)读取制品并把热点帧映射到源码。两者都返回诊断，而不是修复：

```text
/poteto-mode here's a cpuprofile from the slow startup. tell me where the time goes and which source lines own it. no fix yet.
```

## 用 `/tdd` 先写失败的测试

当 bug 有成本低的本地测试路径时，整条 prompt 可以只有两个字：

```text
/tdd implement
```

在上下文中，这就够了。[`/tdd`](../../skills/tdd/SKILL.md) 先写因预期原因失败的最小测试，然后修复，再重跑测试。如果测试需要大范围搭建 harness 或脆弱的 mock，技能会说明这一点，并改用最接近的可执行检查。不要在真实命令是更强证据的地方强行写测试。

## 按名称加载 TypeScript 规则

[`typescript-best-practices`](../../skills/typescript-best-practices/SKILL.md) 把类型系统原则转化为具体规则：可辨识联合、边界处的 `unknown`、穷尽变体、从 schema 推导的类型。它不会自动加载，所以当任务涉及 `.ts` 或 `.tsx` 文件时，输入 `/typescript-best-practices`。

## 提交前先清理

[Opening a PR 剧本](../../skills/poteto-mode/playbooks/opening-a-pr.md)在每次提交前对 diff 运行 `/deslop`，并对 PR 描述和 commit 正文应用 [`/unslop`](../../skills/unslop/SKILL.md)。`/deslop` 随 `cursor-team-kit` 插件发布，不在 pstack 中。如果你没有它，就用平实的语言要求同样的效果：删除叙述性注释、没有依据的防御性检查、死的兼容路径和无关编辑。

对于散文，`/unslop` 接收一个目标和你的额外规则：

```text
/unslop the readme changes, no emdashes
```

你会形成自己的简写。该技能能从 `unslop that, tighten it` 这样简洁的 prompt 中很好地读出意图。

## 用 `/no-comments` 剥掉注释

注释需要单独一轮处理，而且不应由写注释的 agent 来做。作者会像你一样为自己的注释辩护。所以在审阅之前，把它们交给全新的眼睛：

```text
/no-comments the diff
```

[`/no-comments`](../../skills/no-comments/SKILL.md) 会派生 [Comment Sicko](../../agents/comment-sicko.md)，一个只读审阅者，持有一份很短的保留清单：许可证头、公共 API 上的 doc 注释、解释代码无法表达之事的链接、被无法改变的外部依赖强制的行为。其余全部移除。你自己代码里的意外不会获得这种豁免。注释会作为重构标记返回，`/no-comments` 会从根因上修复它接受的标记。当注释宣称某个约束时，例如"不要删除"，技能会提议把该声明编码为类型、测试或 lint。无论哪种方式，注释都会被移除。

分工值得记清。`/deslop` 清理代码中的 slop，`/unslop` 清理散文中的 slop，`/no-comments` 把注释交给没有写它们的人审阅。

**陷阱：** 清理不是可选的润色。带有叙述性注释和防御性死重量的 diff 在审阅者看来就像没做完，而多余的代码正是下一个 bug 藏身的地方。如果 diff 感觉注水了，在提交前说 `deslop it`，而不是等审阅指出之后。

下一步：[验证并交付](./06-verify-and-ship.md)。
