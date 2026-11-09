---
name: principle-build-the-lever
description: "适用于任何非平凡的工作，不只是批量工作：编辑、迁移、分析、检查。构建完成它或证明它的工具（codemod、脚本、生成器，或你的子代理遵循的技能），而不是手工去做。这个工具是评审者可以重跑的产物。"
disable-model-invocation: true
---
# Build the Lever

当工作不平凡时，构建完成它的工具，而不是手工去做。

codemod、生成器或脚本每次都以同样的方式完成工作，并且可以免费重跑。工具是评审者可以阅读并重跑以检查工作的一个产物。手工完成的改动只能靠重做来重新验证。确定性的脚本把"相信我"变成"跑这个"。

默认构建杠杆。只有当任务平凡、只是几处一眼可见的编辑时才跳过。

- 先手工完成第一个单元来学习配方，然后构建工具。在那个单元上重跑工具，并与手工版本做差异比较来证明它。让杠杆可以安全重跑。
- 编辑用 codemod 或脚本，重复文件用生成器，分析用导出到 sqlite 的查询，验证用可重跑的检查。
- 确定性的杠杆胜过扇出。如果工具能一遍处理每个单元，就自己运行它。不要把脚本能做的事扇出给代理手工应用。
- 当你把工作扇出给子代理时，把杠杆写成一个它们都会读的技能：配方、验证契约和不得触碰的围栏放在同一个产物里。把它放在委托者的写入范围之外，这样它们无法悄悄修改契约。
- 应用这条原则会产生一个文件。如果你引用了它，而差异里没有 codemod、脚本、生成器或委托技能，你就没有应用它。
- 当工作活得比本次会话更久时，提交这个杠杆。

标准是平凡性，而不是重复性。一次性任务仍然值得一个杠杆，只要杠杆正是让工作可检查的东西。按照 [Laziness Protocol](../principle-laziness-protocol/principle-laziness-protocol.md)，构建完成或证明该工作的最小脚本，绝不要框架。

与 [Encode Lessons in Structure](../principle-encode-lessons-in-structure/principle-encode-lessons-in-structure.md) 不同，后者把反复出现的指令变成持久的护栏。这条管的是眼前工作的吞吐量和可评审性。关于把验证本身脚本化，见 [Prove It Works](../principle-prove-it-works/principle-prove-it-works.md)。
