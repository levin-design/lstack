# 用原则名称引导

pstack 以独立技能的形式发布了 24 条原则。`/poteto-mode` 在每个多步任务开始时读取其索引，应用任务触发的原则，并在回复中点名每条应用的原则及其改变的决策。

你不"调用"原则。你用它们的名称来引导。每个名称指向一条 agent 已经读过的完整规则，所以一个短语比一段指令更精确地重定向工作。

## 实践中的引导

假设 agent 即将在三个现有 adapter 之上再加一个新 adapter：

```text
use subtract before you add. delete the obsolete adapters first, then design what's left.
```

假设它因为构建通过就声称成功：

```text
apply prove it works. run the real import flow and show me the written records.
```

假设两次并行尝试即将写入同一个分支：

```text
separate before serializing shared state. give each attempt its own worktree, no locks.
```

每个短语都生效，因为它背后的规则足够具体。agent 仍必须在回复中说明该规则改变了哪个决策。如果引用了原则却没有对应决策，说明 agent 只是点名而没应用。

## 24 条原则简述

核心原则决定构建多少、何时重新考虑设计：

- [Laziness Protocol](../../skills/principle-laziness-protocol/SKILL.md) 优先删除，优先选择解决问题的最小改动。
- [Foundational Thinking](../../skills/principle-foundational-thinking/SKILL.md) 在编写逻辑之前先选择核心数据结构。
- [Redesign from First Principles](../../skills/principle-redesign-from-first-principles/SKILL.md) 把新需求整合得就像它从第一天就存在。
- [Attack the Premise](../../skills/principle-attack-the-premise/SKILL.md) 写下两次或更多失败修复共享的前提，并在下一次修复之前直接检验它。
- [Subtract Before You Add](../../skills/principle-subtract-before-you-add/SKILL.md) 在构建之前先移除死重量。
- [Minimize Reader Load](../../skills/principle-minimize-reader-load/SKILL.md) 合并读者必须在脑中持有的层次和隐藏状态。
- [Outcome-Oriented Execution](../../skills/principle-outcome-oriented-execution/SKILL.md) 让重写收敛到目标设计，而不是保留一次性的兼容状态。
- [Experience First](../../skills/principle-experience-first/SKILL.md) 选择用户的结果而非实现的便利。
- [Exhaust the Design Space](../../skills/principle-exhaust-the-design-space/SKILL.md) 在没有先例时构建两到三个相互竞争的原型。
- [Build the Lever](../../skills/principle-build-the-lever/SKILL.md) 构建能做或能证明这项工作的脚本，让审阅者可以重跑它。当 agent 反复手工做同一件事时，让它写一个自己希望拥有的工具或技能。如果脚本可以每次都同样地完成某个步骤，就用脚本，把 agent 留给需要判断的调用。

架构原则决定状态、校验和兼容性住在哪里：

- [Model the Domain](../../skills/principle-model-the-domain/SKILL.md) 把重复的规则编码进一个结构，而不是散落的条件分支。
- [Boundary Discipline](../../skills/principle-boundary-discipline/SKILL.md) 在边界处校验，信任内部类型。
- [Type System Discipline](../../skills/principle-type-system-discipline/SKILL.md) 让非法状态无法表达。
- [Make Operations Idempotent](../../skills/principle-make-operations-idempotent/SKILL.md) 让重试收敛到相同的最终状态。
- [Migrate Callers Then Delete Legacy APIs](../../skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) 在同一波中迁移并删除。
- [Separate Before Serializing Shared State](../../skills/principle-separate-before-serializing-shared-state/SKILL.md) 在添加协调之前先移除共享。

验证原则定义什么算证明：

- [Prove It Works](../../skills/principle-prove-it-works/SKILL.md) 验证真实制品，而不是替代物。
- [Fix Root Causes](../../skills/principle-fix-root-causes/SKILL.md) 在改代码之前先复现并追踪到原因。
- [Sequence Work into Verifiable Units](../../skills/principle-sequence-verifiable-units/SKILL.md) 每个小单元以一次检查结束，然后再开始下一个。
- [Test Behavior, Not Implementation](../../skills/principle-test-behavior-not-implementation/SKILL.md) 断言代码用户能观察到的内容，这样当行为被破坏时测试会失败，而内部改动后测试仍能存活。
- [Explain the Number](../../skills/principle-explain-the-number/SKILL.md) 在任何人信任或报告一个测量数字之前，指出什么限制了它，并排除它测的是别的东西。[`/benchmark-checklist`](../../skills/benchmark-checklist/SKILL.md) 把它变成七个问题，由你从真实运行中回答。

委派原则让并行工作保持理智：

- [Guard the Context Window](../../skills/principle-guard-the-context-window/SKILL.md) 把批量阅读路由给 subagent，把发现留在主聊天。
- [Never Block on the Human](../../skills/principle-never-block-on-the-human/SKILL.md) 对可逆的工作继续推进，并呈交结果。

还有一条元原则：

- [Encode Lessons in Structure](../../skills/principle-encode-lessons-in-structure/SKILL.md) 把你已经重复过两次的建议变成 lint、检查或脚本。[`/correct`](../../skills/correct/SKILL.md) 把它应用到一个整个仓库，如[把它变成你自己的](./09-make-it-yours.md#从环境层面修复)所示。

不要背这份清单。现在浏览一遍，然后在发现 agent 做了某个这里的原则名本可阻止的事情时，再回来查。词汇就是这样扎根的。

下一步：[把它变成你自己的](./09-make-it-yours.md)。
