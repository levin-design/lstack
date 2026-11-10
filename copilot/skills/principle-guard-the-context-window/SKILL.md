---
name: principle-guard-the-context-window
description: "当上下文正在填满时应用：大输出、长文件、重复读取、扇出规划。把批量工作交给子代理；主线程只保留摘要，不保留原始载荷。"
disable-model-invocation: true
---

# Guard the Context Window

**为什么：** 上下文溢出会降低推理质量，产生压缩伪影，并使进展停滞。

**模式：**
- **为阶段设定规模并限制范围。** 限制每阶段的文件数，设定轮次预算，计入机制成本。
