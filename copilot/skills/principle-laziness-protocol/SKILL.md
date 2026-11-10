---
name: principle-laziness-protocol
description: "在重构、评估差异大小，或忍不住要加抽象、加层、穿信号时应用。倾向删除，以及解决问题的最小改动。"
disable-model-invocation: true
---

# Laziness Protocol

- **合并决策。** 不要在多个地方重复同一个选择。把它放在单一事实来源之后，把结果作为简单标志传递。
- **最小化差异。** 做解决问题的最小改动。更少的行胜过"优雅"的样板。
