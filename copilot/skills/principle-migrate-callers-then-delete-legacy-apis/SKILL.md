---
name: principle-migrate-callers-then-delete-legacy-apis
description: "当引入新的内部 API 而旧调用方仍然存在时应用。在同一波次内迁移调用方并删除旧 API，而不是保留兼容层。"
disable-model-invocation: true
---

# 先迁移调用方，再删除旧 API

- 更新测试以断言新契约，并删除那些只保护重构前实现细节的测试

**适用时机：**
- 没有外部用户依赖向后兼容
- 项目能够承受协同的破坏性变更
- 新 API 属于简化或重构计划的一部分
