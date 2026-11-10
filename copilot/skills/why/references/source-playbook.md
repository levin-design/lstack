# 来源剧本

why 技能为每个可用证据类别派生一名调查员，每人阅读下面一个特定来源的剧本。这些剧本是针对常见 MCP 的具体示例。对于同一类别中的其他 MCP，请对它们进行适配。

| 类别 | 剧本 | 它记录的示例 MCP |
|---|---|---|
| 源码控制历史 | [`code-archaeology.md`](./sources/code-archaeology.md) | git, `gh` |
| 问题 / 工单跟踪器 | [`linear.md`](./sources/linear.md) | Linear（可适配 Jira、GitHub Issues、Plane、Shortcut） |
| 长文档 | [`notion.md`](./sources/notion.md) | Notion（可适配 Confluence、Google Docs、Coda） |
| 实时团队聊天 | [`slack.md`](./sources/slack.md) | Slack（可适配 Discord、Microsoft Teams、Mattermost） |
| 基础设施可观测性 | [`datadog.md`](./sources/datadog.md) | Datadog（可适配 New Relic、Honeycomb、Grafana、Splunk） |
| 错误 / 异常跟踪 | [`sentry.md`](./sources/sentry.md) | Sentry（可适配 Rollbar、Bugsnag、Airbrake） |
| 产品分析数据仓库 | [`databricks.md`](./sources/databricks.md) | Databricks SQL（可适配 Snowflake、BigQuery、ClickHouse、dbt） |

跨类别：

- [`incident-postmortem.md`](./sources/incident-postmortem.md)。如果目标代码看起来是防御性的（空值检查、重试、超时、限流、功能开关、出口防护、OOM 处理），则添加此项。
