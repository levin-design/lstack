# Datadog 遥测

## 本来源包含什么

Datadog 保存运行时记录——生产环境中实际发生了什么，而不是计划了什么或讨论了什么。

- **指标。** 团队埋点的 counter、gauge、histogram。某个指标的*存在*本身就是证据：有人认为这个数字值得关注。
- **监视器与告警。** 团队认定值得半夜叫人的条件。一个在 `rate_limit_hit > 10/min` 时触发的监视器，是团队担心该阈值的直接证据。
- **仪表盘。** 团队认为某个子系统重要的精选视图。
- **APM 轨迹与 span。** 请求级的运行时数据，用于回答"为什么这里慢" / "为什么这里有超时"。
- **日志。** 大容量事件记录，常常包含促成防御性代码的错误条件。
- **事故。** 带时间线与关联复盘的正式事故记录。
- **Notebook。** 团队的探索性调查，常常带有假设与分析。

## 如何检索

使用 Datadog MCP。先宽后窄。

1. **确定所属服务。**

   ```
   search_datadog_services (filter by name or team)
   search_datadog_service_dependencies (see upstream/downstream)
   ```

2. **先看仪表盘与监视器。**

   ```
   search_datadog_dashboards (query: feature name, service name, symbol)
   search_datadog_monitors   (same queries)
   ```

   当某个仪表盘或监视器覆盖了目标时，记录它的查询与所关注的阈值。阈值常常就是"为什么这里被钳制在 N"的答案。

3. **目标周边的指标。**

   ```
   search_datadog_metrics (by name pattern, e.g., the feature or symbol)
   get_datadog_metric_context (metadata: description, units, tags)
   get_datadog_metric (timeseries; "was there a spike around the PR date?")
   ```

   把某个指标的走势与目标的添加/变更日期关联起来，是有力的佐证："the `payment_timeout` metric spiked 2023-11-03, and the retry logic merged 2023-11-06."

4. **日志。要收窄，不要倾倒。**

   ```
   search_datadog_logs (raw log patterns near the target, set use_log_patterns=true)
   analyze_datadog_logs (SQL-style aggregations, only when you need counts)
   ```

   用符号、错误字符串或功能名来搜索。**强烈优先使用限定时间的查询**（例如变更前后 30 天）。

5. **APM span 与轨迹。**

   ```
   aggregate_spans    (stats: "how often does this endpoint fail?")
   search_datadog_spans (inspect individual spans)
   get_datadog_trace  (a specific trace ID)
   ```

   适用于超时、重试、慢路径以及跨服务行为。

6. **事故。**

   ```
   search_datadog_incidents (by title, team, date range)
   get_datadog_incident     (full detail for a specific incident)
   ```

   如果目标看起来是防御性的，就搜索其加入时间附近的事故。一份时间线中包含 "added defensive check for X" 的事故记录，几乎是直接证据。

## 这里的良好证据长什么样

- 查询与阈值同代码所强制的约束相匹配的监视器（代码钳制到 100，监视器在请求超过 100/min 时告警）
- 由目标作者创建的仪表盘，其组件与代码所度量或防御的内容相对应
- 一个在代码合并之前立即出现生产尖峰、之后数值稳定的指标
- 引用目标代码、相同符号或相同错误字符串的事故记录
- 显示防御性代码本可避免的特定错误模式、且时间戳落在变更前窗口内的日志

## 常见陷阱

- **相关不等于因果。** PR 之前的尖峰与之后的稳定只是提示性的，并非定论，因为同一窗口内可能还落地了其他变更。检查邻近的 PR。
- **对你找到的图表过拟合。** 图表反映其制作者的框定方式。一张名为"重试成功率"的图表只能证明团队在意重试成功率，并不能证明它就是某行代码存在的原因。
- **消失的遥测。** 指标可能被重命名、删除，或保留期很短。如果你找不到相关窗口的数据，那是缺口，不是空结果。
- **规模带来的噪声。** 积极地按服务、标签和时间窗口收窄日志搜索。用 `analyze_datadog_logs` 做聚合，而不是倾倒原始日志。
- **有埋点 != 有因果。** 指标说明有人在意到要度量某事，而不是代码*因为*它而被加入。要与提交/PR 日期交叉比对。

## 需要返回什么

对每一项相关条目：
- 类型（仪表盘 / 监视器 / 指标 / 日志模式 / 轨迹 / 事故 / notebook）
- 标题或名称
- 链接或标识（仪表盘 ID、监视器 ID、指标名、事故 ID）
- 所有者/作者与创建/修改日期
- 与问题相关的具体条件、查询或引文（尽可能逐字）
- 相关性：这对目标代码意味着什么，以及关联有多强
