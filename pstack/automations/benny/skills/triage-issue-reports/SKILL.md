---
name: triage-issue-reports
description: 分类 Slack issue report，只在线程内给出一条结论，包含证据审阅、原因感知的改派、tracker 去重，以及 fail-closed 的工单创建。仅从配置的 Benny triage 自动化中使用。
disable-model-invocation: true
---

# 分类 issue report

对一条 Slack 报告进行分类，并在其 source thread 中发布一条有用的结论。只为明确的新 bug 创建 tracker issue。不要在这里复现或修复它。

加载自动化提供的外部 Benny 配置。如果配置缺失、格式错误或不完整，停止并且不要发帖，也不要写入 tracker。

## 硬性安全规则

- source channel 和根 thread 坐标不可变。
- 绝不要在 source channel 中发布根消息。
- 绝不要发帖到其他频道、广播回复、发送 DM，或另起替代 thread。
- 在任何 tracker 写入之前，以及发布结论之前，立即对 source parent 做 preflight。
- 如果 parent 缺失、被删除、不可访问或不确定，停止，不进行任何写入。
- 只发布一条实质性结论。不要叙述进度。
- 协调者是唯一的 Slack 发帖者。
- 被委派的 worker 只返回发现。它们必须只读，并且不得获得 Slack 凭据或写操作。
- 每个子 prompt 都必须禁止 `SendSlackMessage`、`PostToSlack`、`chat.postMessage` 以及所有其他 Slack 写入。
- 如果 worker 隔离无法强制执行这些限制，就在协调者中完成工作。
- 绝不创建无法链接回 source thread 的 issue。
- 宁可没有工单，也不要猜测的或重复的工单。
- 对 source 坐标应用 pstack 的 `principle-separate-before-serializing-shared-state`。
- 对最终结论应用 pstack 的 `principle-minimize-reader-load` 和 `unslop` 技能。

## 1. 冻结 source 坐标

在制定工作清单或委派之前：

1. 从 trigger 读取 `source_channel_id`。
2. 要求它等于配置的 source channel。
3. 当 `trigger.thread_ts` 存在时，把 `SOURCE_THREAD_TS` 设为它。否则使用 `trigger.ts`。
4. 要求 `SOURCE_THREAD_TS` 非空。
5. 把 `SOURCE_CHANNEL_ID` 和 `SOURCE_THREAD_TS` 存为不可变值。
6. 读取 thread，验证其根消息正好具有这些坐标。
7. 获取一个稳定的 source permalink。

之后每次读取 source 和发帖都必须使用这些存储值。绝不要用回复时间戳或 operations-thread 时间戳替换它们。

## 2. 读取完整报告

在做决定之前读取根消息和当前回复。

采集：

- 报告者的措辞
- 产品版本、应用 build、环境和平台（若存在）
- 预期行为
- 观察到的行为
- 频率和触发条件
- 错误文本或堆栈签名
- 现有 issue、commit 或 pull request 链接
- 任何明确说明已有人在修复的陈述

检查每个相关附件。

- 以完整可用的分辨率读取截图。
- 审阅视频中区分正确与错误行为的状态转换。
- 读取日志、trace 和崩溃文本以获取具体签名。
- 如果媒体需要专家审阅，使用只读的媒体 worker 并提出一个具体问题。worker 只返回发现。
- 如果某个附件无法读取，在结论中说明。不要臆测它显示了什么。

在向报告者追问之前，先使用 thread 中已有的证据。

## 3. 改派之前先追踪原因

在选择负责人或目的地之前，做一次有边界的源码与历史检查。使用 pstack 的 `how` skill 追踪从报告动作到观察结果的路径。当报告看起来像回归或涉及防御性代码时，使用 `why`。

1. 找出从报告动作到观察结果的可能代码路径。
2. 检查可见症状属于该代码路径，还是属于其下的某个依赖。
3. 当报告看起来像回归时，检查最近的改动。
4. 检查是否已有合并 commit 或打开的 pull request 处理同一症状。
5. 把已确认的事实与假设分开。

这次检查不需要完整的根因。它必须足够有力，以免把可见症状改派给错误的负责人。

如果无法读取仓库，不要猜测代码负责人。继续进行保守的分类，并说明原因追踪不可用。

## 4. 分类

选择一个类别。

### Bug

某物违反了预期行为。例如输出错误、状态损坏、报错、崩溃、挂起、静默无操作或回归。

### Performance

报告描述了可测量的缓慢、内存过高、电池耗尽、卡顿或其他资源问题。把它当作 bug 处理，但保留测量数据和 profile。

### Feature request

当前行为看起来是有意为之，而报告者想要不同的行为或交互方式。

### Question or feedback

报告询问某物如何工作、表达了偏好但没有具体缺陷，或给出一般性反馈。

### Reroute

原因追踪显示配置的另一个目的地负责该 issue。

当 bug 与 feature 的界线不清楚时，不要建单。这条唯一的结论可以提出一个聚焦的问题并使用 `other` 标记。

## 5. 应用配置的改派

从 `routing.map_path` 读取可选的 routing map。

- 基于已确认的产品领域、代码路径或错误签名进行匹配。
- 当原因追踪指向别处时，仅凭可见症状是不够的。
- 如果没有路由匹配，说明负责人不明确。不要猜测。
- 不要跨频道转发。在 source thread 中告诉报告者该把 issue 带到哪里。

owner ping 默认关闭。只有以下条件全部成立时才允许 ping：

1. routing map 明确写出该 owner。
2. 配置允许该类型的 ping。
3. 该条目是需要 owner 输入的功能请求，或最近历史以强证据识别出可能的回归作者。
4. owner 不是宽泛的 on-call 组。

其他任何情况都不发 ping。

## 6. 使用 issue-tracker adapter

tracker 是一个 adapter，而不是必需的供应商。Linear adapter 是一个有效示例。GitHub Issues adapter 或其他 tracker 也可以实现同样的契约。

配置的 adapter 必须提供：

- 按文本、状态、标签、source URL 和日期范围搜索 issue
- 读取单个 issue 及其链接
- 创建带 title、body、status、labels 和 source URL 的 issue
- 更新现有 issue 而不替换无关字段
- 添加 source 链接和复现说明
- 当 Slack 交接失败时，取消、关闭或删除本次运行创建的 issue

如果某项必需操作不可用，对该写入 fail closed。

在运行时解析配置的 team、project、status 和 labels。不要臆造 ID、创建标签、指派 owner 或设置优先级，除非配置明确要求。

## 7. 去重

始终检查该 source permalink 是否已链接到某个 tracker issue 或先前的 triage 回复。如果是，则不要发帖或创建重复项。

对于 bug 和 performance 报告，使用以下条件搜索 tracker：

- 精确的错误或崩溃签名
- 产品领域
- 触发条件
- 症状
- 版本或日期范围
- 疑似回归 commit
- source permalink

选择一个结果：

- 有把握的重复项：相同签名，或相同的领域、触发条件和症状，或已确认的共同原因。
- 可能相关：共同原因有可能性但未经证明。
- 弱相似：相似性只停留在表面。
- 无匹配。

对于有把握的重复项，用 source permalink 和一条简短的再次出现说明更新现有 issue。除非配置要求，不要重新打开、重设标签或重新指派它。

对于可能的匹配，在结论中作为不确定项链接它，不创建任何东西。

长期关闭的 issue 是回归线索，不自动视为仍活跃的重复项。

## 8. 决定是否创建

只有以下条件全部为真时才创建：

1. 分类是 bug 或 performance。
2. 行为明显已损坏。
3. 该 issue 仍然活跃或未被确认修复。
4. 去重未发现任何有把握或合理的活跃匹配。
5. source parent 和 permalink 通过了 preflight。
6. tracker 目标字段已解析。
7. 如果结论发布失败，adapter 能够进行补偿。

绝不要为功能请求、问题、反馈、改派、可能重复、有把握的重复或已修复的 issue 创建工单。

新 issue 必须自包含：

- 朴素直白的 title，点明领域和症状
- 报告者原话
- 预期行为与观察到的行为
- 版本和环境，或 `unknown`
- 触发条件和频率
- source thread permalink
- 简短的原因追踪发现，假设须标注为假设
- 内嵌截图或代表性视频帧（若支持）
- 其余制品的链接
- 配置的 intake 状态和 labels

不要把猜测的根因写进 title。

## 9. 发布一条结论

运行一次全新的 source-parent preflight。然后用 `channel=SOURCE_CHANNEL_ID` 和 `thread_ts=SOURCE_THREAD_TS` 发布恰好一条回复。

绝不要在 `thread_ts` 为空时调用 source-channel 发帖操作。

保持回复简短：

- 以结果开头。
- 有 tracker issue（现有的或新建的）时链接它。
- 必要时提及改派或缺失的一个事实。
- 最多包含一个被允许的 owner ping。
- 以恰好一行标记结束。

标记契约：

```text
[benny:bug]
[benny:bug] tracker=https://tracker.example/issue/123
[benny:performance]
[benny:performance] tracker=https://tracker.example/issue/123
[benny:other]
```

只使用配置的标记字符串。repro 自动化仅在标记来自该 source thread 中配置的 triage 身份时才信任它。

发帖之后，读取同一 source thread，验证结论出现在 `SOURCE_THREAD_TS` 之下。如果没有出现，绝不要在根消息处重试。

如果本次运行创建了 tracker issue 而结论没有落地，使用 adapter 的补偿操作。验证该 issue 已被取消、关闭或删除。如果无法验证补偿，只在自动化运行输出中报告失败。

## 10. 观察一个后续窗口

在配置的后续窗口内观察 source thread，然后停止。

- 只回答直接针对 triage 身份的问题。
- 在安全时对 tracker issue 应用一处具体的更正。
- 不要在同一次运行中发出第二个标记。
- 不要介入人类协调和旁支闲聊。
- 如果有人要求自动化停止，提前停止。

窗口最多延长一次。新的报告应启动新的运行。
