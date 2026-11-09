---
name: reproduce-and-fix-issues
description: 通过配置的应用控制 adapter 复现已分类的 Slack bug，验证现有修复，并且只有在前后对比证明通过后才打开有边界的草稿 pull request。仅从配置的 Benny repro 自动化中使用。
disable-model-invocation: true
---

# 复现并修复 issue

在 source thread 中等待可信的 triage 标记。通过目标应用的真实 UI 复现完全相同的症状。存在现有修复时验证它。只有在确认复现之后，才尝试有边界的修复。

加载自动化提供的外部 Benny 配置。如果配置、所需操作、control adapter 或已完成的 feature map 缺失，fail closed。

## 硬性安全规则

- 在做任何工作之前，冻结 source channel 和根 thread 坐标。
- 绝不要在 source channel 中发布根消息。
- 在每次 source-thread 发帖之前对 source parent 做 preflight。
- 协调者是唯一的 Slack 发帖者。
- 被委派的分析 worker 只读，并返回发现或媒体备注。
- 修复阶段的代码 worker 只有在能证明其环境排除了 Slack 凭据和所有 Slack 写操作时才可以编辑。否则由协调者编辑。
- 每个子 prompt 都必须明确禁止 `SendSlackMessage`、`PostToSlack`、`chat.postMessage` 以及所有其他 Slack 写入。
- 绝不要给子代理 Slack token、发帖指令、用于发帖的 source 坐标，或对外报告的权限。
- 如果子代理需要 Slack 写权限才能运行，不要启动它。
- 工具机器人是证据来源。它们不拥有修复，除非有人明确把修复委派给它们。
- 通过真实 UI 交互，判别性症状必须出现两次。
- 状态检查可以确认观察结果。它不能注入或强制产生该症状。
- 没有确认的复现，就没有作者化的修复。
- 现有 pull request 或 commit 会把运行切换到验证模式。不要在其之上另写实现。
- 使用 `github.com` pull request 链接。
- 把截图、录像、日志和 token 排除在源代码管理之外。
- 对委派的分析使用 pstack 的 `principle-guard-the-context-window`。
- 在复现、修复和验证过程中应用 pstack 的 `principle-sequence-verifiable-units`、`principle-fix-root-causes` 和 `principle-prove-it-works`。

## 1. 冻结 source 坐标

在制定工作清单或委派之前：

1. 要求 trigger channel 等于配置的 source channel。
2. 当 `trigger.thread_ts` 存在时，把 `SOURCE_THREAD_TS` 设为它。否则使用 `trigger.ts`。
3. 要求 `SOURCE_THREAD_TS` 非空。
4. 把 `SOURCE_CHANNEL_ID` 和 `SOURCE_THREAD_TS` 存为不可变值。
5. 读取 source thread，验证其根消息正好具有这些坐标。
6. 获取 source permalink。

绝不要用回复时间戳、operations 时间戳或状态消息时间戳替换这些值。

在每次 source-channel 发帖之前：

1. 用不可变坐标读取 thread。
2. 确认 parent 存在、未被删除，且仍属于 source channel。
3. 只使用 `channel=SOURCE_CHANNEL_ID` 和 `thread_ts=SOURCE_THREAD_TS` 发送。
4. 再次读取 thread，验证新消息是一条回复。

如果任何检查失败，不发任何内容。绝不要在根消息处或回退频道中重试。

## 2. 等待 triage 契约

在配置的结论预算内观察 source thread。等待期间保持静默。

只在以下条件成立时接受结论：

- 作者匹配 `slack.triage_identity_user_id`。
- 它是 `SOURCE_THREAD_TS` 之下的一条回复。
- 它恰好包含一个配置的标记。

公开标记形式：

```text
[benny:bug]
[benny:bug] tracker=https://tracker.example/issue/123
[benny:performance]
[benny:performance] tracker=https://tracker.example/issue/123
[benny:other]
```

只对 `bug` 或 `performance` 继续。捕获可选的 tracker URL。对于 `other`、缺失的结论、不可信的作者、相互冲突的标记或超时，静默停止。

这个标记取代了私有机器人身份和自由格式的结论匹配。

## 3. 应用归属与修复制品门禁

在开始工作之前立即重新读取 thread。

### 有人明确在修复它

当有人明确认领修复、给出具体的实现计划，或要求另一个 agent 实现、打补丁、修复或打开 pull request 时，停止。

不要把以下情况视为修复归属：

- 机器人总结了证据。
- 工具查询了日志或工单。
- 有人要求机器人诊断、解释、检查或复现。
- 机器人发布了原因假设，但未同意实现。

判断的是被请求的动作，而不是机器人的存在。

### 修复制品已经存在

如果打开的 pull request 或已合并 commit 有可能修复该报告，切换到 `references/verify-existing-fix.md`。

制品可以来自 thread、tracker issue、仓库历史或 pull request 搜索。没有 commit 或 pull request 的声明不是修复制品。

如果某人拥有这项工作但尚未产出制品，停止。不要与其竞速。

## 4. 打开可选的 operations thread

如果配置了 `slack.operations_channel_id`，协调者可以在那里创建一条根状态消息。这是 repro 工作流中唯一允许的根消息。

把它的坐标存为 `OPERATIONS_CHANNEL_ID` 和 `OPERATIONS_THREAD_TS`。绝不把它们与 source 坐标混淆。

使用配置的纯 Unicode 状态字符串。保持状态文本简短：

- Reproducing
- Could not reproduce
- Blocked
- Reproduced
- Verifying existing fix
- Attempting bounded fix
- Draft pull request opened
- Fix did not land

优先使用配置的 Cursor Slack actions。仅当用户为某个狭窄的缺失能力（例如编辑这一条状态消息）配置了 `BENNY_SLACK_BOT_TOKEN` 时才使用它。绝不把 token 暴露给 worker。

如果没有配置 operations channel，把详细状态保留在自动化运行输出中。不要用 source-channel 根消息替代。

## 5. 加载并检查 control adapter

读取 `references/control-adapter.md` 以及 `control.feature_map_path` 处已完成的地图，然后调用 `control.skill_name` 指定的技能。

找到与报告的用户路径匹配的 feature-map 小节。在驱动应用之前读取它。如果没有小节覆盖该功能，把运行标记为 blocked，而不是臆造路径或选择器。

要求全部七项能力：

1. 启动配置的目标应用和测试环境。
2. 导航到映射的功能并演练其记录在案的状态。
3. 通过点击、输入、按键、滚动、拖拽、调整大小或导航驱动真实 UI。
4. 检查状态而不改变它。
5. 采集截图。
6. 启动和停止屏幕录制。
7. 清理进程、会话、配置文件和临时数据。

如果 adapter 不存在或任何所需能力缺失，把 operations 状态标记为 blocked 并停止。不要把截图、单元测试、状态变更或源码阅读当成 UI 复现。

## 6. 研究报告

读取完整的 source thread 和 tracker issue（若存在）。

收集：

- 确切的动作路径
- 预期行为
- 观察到的行为
- 两者分歧处的判别性状态
- 频率
- 版本、环境和平台
- 附件和错误签名
- 候选代码区域

检查截图和视频。在有用时，为代码历史、测试想法、blast-radius 映射和媒体审阅使用只读的并行 worker。每个 worker 得到一个具体问题和 Slack 写入禁令。

使用 pstack 的 `how` skill 在仓库中追踪该动作。在回归历史和防御性代码上使用 `why`。提出相互竞争的原因假设，并找出能区分它们的关键证据。

## 7. 复现

通过 control adapter 启动目标应用。

在行动之前，确认正确的应用、工作区、账号、数据集和功能状态。使用稳定的应用标记。不要只依赖窗口顺序或熟悉的标题。

通过真实 UI 操作驱动报告路径。

在宣布已复现之前：

1. 说出正确的最终状态。
2. 说出损坏的最终状态。
3. 到达两者分歧的位置。
4. 观察到损坏的状态。
5. 重置足够的状态，使第二次尝试相互独立。
6. 重复同一条路径，再次观察到相同的损坏状态。
7. 尽可能交叉核对一个真实状态值。

预期的对话框、加载状态或安装步骤不是 bug。捕获能区分正确与错误行为的最终状态。

使用配置的复现预算。如果症状在该预算内未复现，报告干净的 `Could not reproduce` 结果。如果环境无法提供所需能力，报告 `Blocked` 并说明缺少什么。

## 8. 采集并审阅证据

对于成功的复现：

- 录制贯穿症状的完整路径。
- 采集损坏最终状态的截图。
- 保存一条简短说明，记录确切步骤和观察到的状态。
- 把制品保存在配置的临时制品目录中。

让一位只读的媒体审阅者回答一个问题：证据是否可见地展示了判别性的损坏状态？

如果答案是否定的或不确定，复现不算确认。采集更好的证据，或使用 `Could not reproduce`。

仅在配置了 operations thread 时在那里发布详细证据。保持 source 更新简洁。

## 9. 报告复现结果

先更新 operations 状态。

对于 `Could not reproduce` 或 `Blocked`，在 source thread 中不发任何内容。operations thread 或运行输出承载结果。

对于确认的复现，运行 source preflight，并最多发布一条未经请求的 source 回复：

- 说明 issue 已复现。
- 存在 operations 证据 thread 时链接它。
- 最多包含三条简短发现。
- 存在 tracker issue 时链接它。
- 默认不要 ping owner。

仅当配置的 Slack 操作把证据保持在同一 source thread 内，且组织的保留策略允许时，才附加证据。

等待配置的否决窗口。如果有人证明设置或解释有误，更正复现一次。在窗口关闭且没有有效否决之前，不要开始修复阶段。

## 10. 验证现有修复

当修复制品存在时，遵循 `references/verify-existing-fix.md`。

验证必须展示基线版本上存在该症状，而打过补丁的构建上不存在。两条路径都通过真实 UI 重复两次。

不要编辑现有修复、添加竞争性补丁，或打开替代的 pull request。

## 11. 判定有边界的修复是否可行

只有以下条件全部成立时才尝试修复：

- 结果是明确的确认复现。
- 媒体审阅确认了损坏的最终状态。
- 没有出现现有修复制品。
- 在否决窗口内无人认领修复。
- 运行时证据识别出根因。
- 可能的改动符合配置的修复预算和仓库范围。
- control adapter 可以运行基线构建和打过补丁的构建。

如果任何条件不满足，保留复现报告并停止，不打开 pull request。

当门禁通过时，把 operations 状态更新为 `Attempting bounded fix`。

## 12. 根因与实现

协调者拥有每一次 Slack 发帖、最终 diff 审阅、commit 和 pull request。

只读 worker 可以：

- 追踪代码和历史
- 提出测试
- 映射 blast radius
- 审阅 diff
- 审阅媒体

它们不编辑、不执行外部写入、不发状态，也不拥有修复。

只有当工具隔离从某个 worker 中移除 Slack 凭据和所有 Slack 写操作时，才可以在本阶段委派紧密限定范围的代码编辑。其 prompt 仍必须带有明确的 Slack 写入禁令。协调者审阅该编辑，并运行或验证所需的测试。如果工具隔离不确定，就把编辑留在协调者中。

用运行时证据确认机制。在编辑之前排除相互竞争的假设。

用最小且合理的改动修复根因。

- 当存在成本低的本地测试目标时，调用 pstack 的 `tdd` skill，并在修复前编写失败的测试。
- 当路径昂贵、不清晰或偏集成时，说明跳过 TDD 的原因。
- 不要包含无关清理。
- 如果改动超出配置的工作量或风险预算，停止。

## 13. 证明修复

保留原始的基线证据。

在打过补丁的构建上：

1. 运行相同的真实 UI 路径。
2. 重复两次。
3. 证明损坏状态已消失。
4. 证明预期状态取而代之。
5. 采集修复后的录像和截图。
6. 交叉核对与基线相同的真实状态值。

编译、单元测试、代码审阅或看似合理的 diff 都不是修复后证据。

先运行聚焦测试，再对改动行为周围的 blast radius 做冒烟检查。覆盖可能受影响的邻近状态、输入、权限、平台和失败路径。如果仍存在回归，停止，不打开 pull request。

## 14. 打开草稿 pull request

仅在前后对比证明之后：

- 审阅最终 diff，检查是否包含无关改动和密钥。
- 运行仓库要求的检查。
- 仓库工作流允许时，创建小型有序 commit。
- 打开草稿 pull request。绝不从此工作流合并或部署。
- 使用 tracker 支持的 pull request 语法链接配置的 tracker issue。
- 使用配置的公开 URL 形式，通常是 `https://github.com/{owner}/{repo}/pull/{number}`。
- 包含复现步骤、根因、测试结果、前后对比证据和 blast-radius 检查。
- 让 pull request 文本和所有 Slack 更新经过 pstack 的 `unslop` skill。

如果 pull request 创建失败，不要声称成功。把 commit 或分支状态保留在运行输出中，并把 operations 状态标记为 `Fix did not land`。

成功时，把 operations 状态标记为 `Draft pull request opened`，并在 operations thread 中发布一条简洁回复，附上已链接的 pull request。不要创建第二条 source-channel 根消息或未经请求的 source 回复。

## 15. 后续与清理

在配置的 operations thread 中观察一个后续窗口。

- 依据已经收集的证据回答直接问题。
- 应用一处具体更正，并在其使设置失效时重新运行复现一次。
- 不要介入人类协调和旁支闲聊。
- 被要求时停止。

始终调用 control adapter 的清理能力。制品只保留配置的保留策略允许的时长。
