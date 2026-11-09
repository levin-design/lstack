# 组织提示词

提示词要说明意图和完成检查。步骤由剧本提供，所以几句朴素的话胜过一份规格说明。

## 要写进去的

- 目标。说明哪里不对，或用户想要什么。
- 完成检查。它能通过或失败。"Make it better" 和一段时长都不算检查。
- 要展示的证据。要求真实的命令输出、流程视频、存储的值，或前后对比的数字。
- 用户已知的信息。症状、复现步骤、日志或链接能让 agent 少搜一轮。
- 真实约束。"repro first"、"don't change any code yet"、"zero behavior change" 和 "let me review before proceeding" 都会改变 agent 的行为。

## 要省略的

- 怎么做。只说要达成什么，给 agent 留出寻找更好办法的空间。
- 技能或步骤清单。手写的顺序会丢掉或打乱剧本保留的步骤。只有要覆盖某个选择时才点名技能。
- 用户对原因的理论，直到 agent 复述问题之后再说。说出的猜测会缩小搜索范围。

## 先加载上下文

- 面对嘈杂的报告，先让 agent 用自己的话、用平实的英语复述底层问题，然后再做任何事。误读会在任何代码出现之前暴露。
- 在新对话中，用 `/recall` 找回该主题的早期工作。旧对话持有新 agent 缺少的上下文。
- 在改动不熟悉的代码前，用 `/how` 了解机制，用 `/why` 了解原因。没有追踪过模型的 agent 会在第一个看似合理的地方修症状。
- 用 `/teach` 让 agent 为某个选择立论，例如 "convince me it fixes the cause and not the symptom"。立论比摘要更容易核查。

## 先设计，后计划

- 绝不接受第一个设计。要求为几个选项做原型，UI 要附截图或视频，再从证据中选择。
- 让原型回答悬而未决的问题。不要对抗性地审查抽象计划，因为评审者会杜撰永远不会发生的风险。
- 对于共享包或 API，先要 README 或教程，再回溯到代码。文档会成为 agent 自我校验的目标。
- 设计定下之后才要计划。计划的每一步都以一个检查结尾。

## 简短跟进

- 一旦对话里装着任务，"do it"、"continue" 和 "keep going until done" 就是完整的提示词。
- 主题变化时以 "new task" 开头。否则模式会把消息当作下一步。

## 离开之前

- 说 "im going to bed" 或 "im stepping away"，让 agent 停止提问。
- 把完成写成每次迭代都能运行的检查，并把该判定条件交给重复唤醒机制。
- 要求基于一个指定基线开一个全新的工作树。
- 预先回答 agent 会为之停下的问题，例如 "don't ask me before committing"。
- 要求一份决策日志以便事后审计。
- 给出退出条件："if you're truly stuck after a few hours, stop and write up why"。

## 一行式引导

- 复述目标："i said the goal is to repro. i did not ask for a fix yet."
- 点名原则："apply prove it works. show me the real output, not the build log."
- 原则名称之所以有效，是因为 agent 已经读过该规则。它的回复会点名该规则改变的那个决定。
