# 事故与复盘背景

- **Linear**：查找带有 `incident`、`sev-*`、`postmortem-action-item`、`reliability` 标签的工单
- **Slack**：在目标代码加入的日期前后，搜索 `#sev-*` 和 `#incident-*` 频道
- **Git**：提交信息形如 "fix for incident"、"add defensive check"，以及 "revert" 之后又跟 "re-apply with..." 的提交，都是强信号
