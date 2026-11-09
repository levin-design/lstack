# Triage automation prompt

> 复制后的 setup 工作流的源材料。在 `automate` 确认复制包已提交到 automation 将要运行的仓库之后，把这份意图转述进一个内置的 `automate` 草稿。

本次运行读取并遵循 `.cursor/automations/benny/skills/triage-issue-reports/SKILL.md`。

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

创建意图应把它描述为配置的 source Slack channel 中的一条新顶层报告。

把 source channel 和根 thread 时间戳视为不可变。如果任一缺失或与配置不符，停止且不要发帖，也不要写入 issue tracker。

已提交的操作文件负责分类、附件审阅、原因追踪、改派、去重、tracker 写入和最终结论。不要发布进度消息。绝不要在 source channel 中发布根消息。

协调者是唯一的 Slack 发帖者。任何被委派的 worker 都必须是只读的、只返回发现，并被明确禁止一切 Slack 写入操作。

用恰好一个配置的标记结束这条唯一的结论：

```text
[benny:bug]
[benny:performance]
[benny:other]
```

bug 或 performance 标记可以附加 `tracker=<URL>`。
