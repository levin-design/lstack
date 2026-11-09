---
name: principle-attack-the-premise
description: "当两个或更多共享同一前提的修复在同一条关卡上失败时应用。在写下又一个假设该前提的修复之前，把前提写下来并直接检验它。"
disable-model-invocation: true
---

# Attack the Premise

当两个或更多共享同一前提的修复在同一条关卡上失败时，怀疑前提，而不是修复。

**为什么：** 每个失败的修复都是对它假设的信念的反证。在同一前提上的第三个修复，会把精力花在证据已经指出原因不在的地方。

**模式：**
- **把前提写下来。** 前提就是每个失败修复都假设的那一句话。
- **在下一次修复之前检验前提。** 找一个若前提为假就会呈现不同结果的观察，并去做它。看失败是如何分布的，而不只看它们有多大。按 [Build the Lever](../principle-build-the-lever/principle-build-the-lever.md) 让检查可重跑。
- **跟随证据。** 如果它与前提矛盾，原因在别处。寻找失败之间的共同点，即前提未能预测的东西。如果它确认了前提，就按 [Fix Root Causes](../principle-fix-root-causes/principle-fix-root-causes.md) 问下一个"为什么"。先前的修复可能治的是后果而不是原因。
- **消除条件，而不是补偿它**，按照 [Laziness Protocol](../principle-laziness-protocol/principle-laziness-protocol.md)。如果证据显示某个部分总是落在失败的一侧，就改变使它如此的东西。事后清理的机制会把原因留在原地，并在每次运行时增加工作。

**停止：** 在前提被写下并检验之前，不要开始下一次修复。

这条原则不同于 [Redesign from First Principles](../principle-redesign-from-first-principles/principle-redesign-from-first-principles.md)，后者围绕新需求重建一个设计。它质疑的是当前设计所假设的一个事实。
