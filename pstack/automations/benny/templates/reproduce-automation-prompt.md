# Reproduce automation prompt

> 复制后的 setup 工作流的源材料。在 `automate` 确认复制包已提交到 automation 将要运行的仓库之后，把这份意图转述进一个内置的 `automate` 草稿。

本次运行读取并遵循 `.cursor/automations/benny/skills/reproduce-and-fix-issues/SKILL.md`。

配置来源。仅当该仓库相对路径已提交到同一目标仓库时才包含它。否则转述配置值。绝不使用插件源路径或缓存路径：

```text
{{BENNY_CONFIG_PATH}}
```

触发：

```json
{
	"source_channel_id": "{{SLACK_CHANNEL_ID}}",
	"message_ts": "{{SLACK_MESSAGE_TS}}",
	"thread_ts": "{{SLACK_THREAD_TS_OR_EMPTY}}"
}
```

创建意图应把它描述为配置的 source Slack channel 中的一条新顶层报告。它应包含配置的仓库、默认分支、issue tracker、control adapter、feature map 和草稿 pull request 能力。

把 source channel 和根 thread 时间戳视为不可变。如果任一缺失或与配置不符，停止且不要发帖。

在这个确切的 thread 中等待来自配置的 triage 身份的配置 triage 标记。仅对 `[benny:bug]` 或 `[benny:performance]` 继续。

在尝试复现之前，要求配置的 control-adapter skill 就绪。通过真实 UI 两次复现完全相同的判别性症状。验证现有 pull request 或 commit，但不要在其之上另写实现。只有在确认复现并通过操作文件的修复门禁之后，才尝试有边界的修复。

协调者是唯一的 Slack 发帖者。每个子 prompt 都必须禁止 `SendSlackMessage`、`PostToSlack`、`chat.postMessage` 以及所有其他 Slack 写入。子代理只返回发现。

绝不要在 source channel 中发布根消息。
