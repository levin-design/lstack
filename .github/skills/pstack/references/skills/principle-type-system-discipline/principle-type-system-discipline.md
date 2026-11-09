---
name: principle-type-system-discipline
description: "在设计类型、审查函数签名，或在任何静态类型语言中编写代码时应用。让非法状态无法表示，给语义原语打上品牌，在边界解析外部数据，穷尽变体，从权威模式派生。"
disable-model-invocation: true
---

# 类型系统纪律

让编译器拒绝不可能的状态、不匹配的原语和未处理的变体。优先把错误和特殊情况定义得不复存在，而不是让处理器不断增殖。TypeScript 语法见 `typescript-best-practices` 技能。

- **给语义原语打上品牌。** `UserId` 和 `OrderId` 底层都是字符串，但不应可互换。给每个各自的类型，例如 TypeScript 中的品牌化交叉类型，或其他语言中的 newtype。在创建时校验一次，下游信任该类型。如果两个参数共享同一原语类型但含义不同，给它们打品牌。
- **外部数据在被解析前都是无类型的。** RPC 载荷、JSON、IPC 消息、CLI 参数、配置文件、环境变量、数据库行。在每个边界上都应有一个解析函数，把非结构化输入变成类型化模型。**boundary-discipline** 原则技能说明了把校验放在哪里。
- **从权威模式派生类型。** 当 protocol buffer、OpenAPI 规范、GraphQL schema、数据库迁移、design token 文件或其他文件拥有某种形状时，从它派生，而不是手写一个并行的类型。见 **encode-lessons-in-structure** 原则技能。
