---
name: typescript-best-practices
description: TypeScript 最佳实践。在阅读或编辑任何 .ts 或 .tsx 文件时使用。
disable-model-invocation: true
---

# TypeScript 最佳实践

适用于阅读或编辑任何 `.ts` 或 `.tsx` 文件。

先应用 **type-system-discipline** 原则技能。

| 规则 | 摘要 |
|------|---------|
| 可辨识联合（Discriminated unions） | 用 `kind` 字面量判别字段为各变体建模，使不可能的状态无法被表示。不要用可选字段堆成的“袋子”。 |
| 品牌类型（Branded types） | 用 `& { readonly __brand: "X" }` 为原始类型打上品牌，使其不会被混用。在边界处校验一次。品牌只能来自经过验证的类型守卫（`input is AgentId`），绝不来自 `as`。 |
| 构造式建模（Constructive modeling） | 把结构设计成非法值无法被构造。非空用 `[T, ...T[]]`，偶数长度用 `[T, T][]`，区间用 `start` 加 `duration`。这不是运行时守卫，也不是对细化类型（refinement types）的祈愿。 |
| 最简全函数类型（Simplest total type） | 只要对其的所有操作都是全函数（total），就保留 `T[]`。仅当宽松类型迫使你写 `!`、类型断言或“不应发生”的 throw 时，才强化为 `NonEmpty<T>`。 |
| `unknown` 优于 `any` | 外部数据一律是 `unknown`。 |
| 先 schema 后守卫 | 在逐属性手写类型守卫之前，先使用仓库已有的运行时 schema 库，并从 schema 推断类型，例如 `z.infer`。 |
| 禁止 `as` 断言 | 每一个 `as` 都是一场尚未发生的运行时崩溃。仅在验证之后才做断言。 |
| 收窄优先级 | 判别字段 switch > `in` 运算符 > `typeof`/`instanceof` > 用户定义类型守卫 > `as`。 |
| 类型守卫 | 必须真正验证其主张。说谎的守卫比 `as` 更糟，因为 bug 藏在一个声称安全的名字后面。命名为 `isX` 或 `hasX`。 |
| 穷尽性 | 在 default 分支内联 `const _exhaustive: never = x;`，这样新增变体时编译器会报错。 |
| `satisfies` 优于 `as` | 在验证值的同时不拓宽字面量类型。 |
| 边界校验 | 在数据进入之处进行解析，产出具名的领域类型。`Record<string, unknown>`（无论怎么拼写）止步于该解析。内部代码信任类型。参见 **boundary-discipline** 原则技能。 |
| 从 schema 派生类型 | 在声明新 interface 之前，先用 `Pick`/`Omit`/`Parameters`/`ReturnType`/`Awaited`/`typeof`。 |
| 对象参数 | 传对象而非位置参数，让参数顺序自解释。热路径（逐帧渲染、分词器、解析器）上跳过此规则。 |
| 真实测试 | 能真实运行的就不要 mock。优先使用框架提供的真实测试原语，配合泄漏/可释放（disposable）检查，并在运行中的构建里验证 UI。只 mock 无法在本地运行的部分。 |
| 结构化遥测 | 优先使用结构化日志诊断，携带足够上下文，能凭一个 id 排查问题。发布代码中不要出现 `console.log`。 |

示例：`references/patterns.md`。
