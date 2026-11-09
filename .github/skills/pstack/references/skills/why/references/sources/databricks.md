# Databricks 分析与系统表

## 本来源包含什么

Databricks 是产品分析、数据管道与仓库遥测层。它与 Datadog 互补。Datadog 是*基础设施/运行时*视角，Databricks 是*产品/数据*视角（用户做了什么、跑了哪些实验、功能使用如何演变、某个阈值常量从何而来）。

- **产品分析事件。** `your_warehouse.events.analytics_track_event`（原始表），以及 `<your_analytics_db>.<schema>.<table>` 中按事件类型建模的、去重且有类型的 dbt 模型。用户行为：功能调用、点击、接受/拒绝、提交、客户端上报的错误。
- **用量与计费事件。** `your_warehouse.events.usage_event` / `<your_analytics_db>.<schema>.stg_usage_events`、`your_warehouse.events.raw_model_event` / `<your_analytics_db>.<schema>.stg_raw_model_events`。用于成本或用量驱动的决策。
- **实验 / 功能开关数据。** 曝光表与结果表。**schema 因公司而异。** 在假定名称之前，先用 `SHOW TABLES` 探测。
- **系统表。** `system.query.history`、`system.compute.warehouses`、`system.billing.*`、`system.access.audit`。回答"这条查询是否昂贵？""究竟多久有人运行它？""仓库负载何时激增？"
- **dbt 血缘。** `<your_analytics_db>.<schema>` 中的模型揭示哪些管道依赖于某张表/某个字段。上游变更常常促使下游消费方代码变更。
- **Databricks notebook。** 工程师在改代码之前写的探索性分析。**无法通过 SQL MCP 查询。** 如果你怀疑理由存在于某个 notebook 中，把它列为缺口。

## 如何检索

使用 Databricks SQL MCP。主要工具：`execute_sql_read_only`。如果它返回 `statement_id`，用 `poll_sql_result` 轮询，而不是重新运行。

**先定位再查询。** schema 因公司而异。在信任某个表名之前先探测：

```sql
SHOW TABLES IN <your_analytics_db>.<schema> LIKE '*<keyword>*';
DESCRIBE TABLE <your_analytics_db>.<schema>.stg_<event>;
```

**为每个查询限定时间。** 这些表非常大，无约束的扫描会超时。按 `_timestamp`（事件表）或 `start_time`（`system.query.history`）过滤，窗口围绕上线日期，通常为前后各约 30 天，只有在有充分理由时才放宽。

**优先使用有类型的 dbt 模型，而不是原始表。** `<your_analytics_db>.<schema>.<table>` 是去重、有类型且采用 liquid clustering 的。`your_warehouse.events.analytics_track_event` 存在重复且属性是无类型的 `properties_json`。模型命名模式为 `stg_<source>_<event_name_with_underscores>`，其中 `<source>` 是 `app`、`backend`、`website` 或 `cli`。当仅凭模式无法确定时，用 `SHOW TABLES` 确认确切的模型名。只有在尚无 dbt 模型，或你需要 dbt 刷新滞后期间的事件时，才降级到原始表。

**有类型 dbt 模型上的列约定**（了解这些可避免一次 `DESCRIBE` 往返）：

- `_timestamp`、`_id`、`_auth_id`、`_request_id`、`event_name`。每个模型都有的标准列
- `properties_<name>`。有类型、以下划线命名的事件属性（`properties_entrypoint`、`properties_size_bytes`、……）
- `context_team_id`、`context_client_version`、`context_country`、`context_client_os`。预提取的客户端上下文

### 通常卓有成效的调查模式

选择与目标匹配的表 + 列组合：

1. **事件使用走势。** 在 PR 合并前后 ±30 天窗口内，统计相关 `stg_*` 模型的每日计数。合并后一两天内从零跃升到稳定量的阶跃函数，是 PR 启动了该功能的有力间接证据。衰减到零则暗示弃用或删除。
2. **护栏 / 防御性检查的起源。** PR *之前* 14 天内相关 `properties_<name>` 列的分布（中位数 / p99 / 最大值）。若 p99 与目标的阈值常量吻合，说明这个数字很可能是从数据中选出来的。
3. **实验 / 功能开关查询。** 用 `SHOW TABLES ... LIKE '*experiment*'` 找到曝光表，然后按变体拉取 PR 日期附近相关开关键的曝光计数。
4. **用于迁移、回填或性能重写的查询历史证据。** 用 `statement_text ILIKE '%<table_or_symbol>%'` 过滤 `system.query.history`，并配合紧凑的 `start_time` 窗口，能浮现出很可能促成本次改动的昂贵查询（按 `total_duration_ms` 排序，或聚合 `SUM(read_bytes)`、`COUNT(*)`）。
5. **dbt 血缘。** 如果目标读自或写入某个 `<your_analytics_db>.<schema>` 模型，该模型自身（在本仓库中）的 git 历史常常承载理由。把这个线索交回 git 调查者，而不是自己去追。

## 这里的良好证据长什么样

除了上述模式形态之外：

- 某个错误分类事件在防御性代码 PR 之后几天内计数降到接近零。说明该 PR 解决了这类错误
- 曝光表中的某行以 PR 上线日期前后记录了目标功能开关的 key 以及 "shipped" / "concluded" 决策

## 常见陷阱

- **有埋点 ≠ 有因果。** 某个事件的存在只说明有人在意到要记录它，并不意味着目标代码*因为*它而存在。在断言因果之前，先配以 git 调查者的 PR/提交引用。
- **悄无声息的埋点变更。** 事件量的阶跃可能意味着某个新事件开始被记录，而不是用户行为发生了改变。在把这段爬升解读为功能上线信号之前，先检查同一窗口内是否有埋点相关的 PR。
- **Schema 漂移。** 事件属性会演进。今天 dbt 类型模型上的某一列，在目标代码编写时可能并不存在。更早的数据可能只在原始 `properties_json` 中携带该属性。
- **dbt 刷新滞后。** `<your_analytics_db>.<schema>.*` 按计划重建（通常是每小时/每天）。对于最近几小时的事件，回退到 `your_warehouse.events.*` 并按 `_id` 去重。
- **因公司而异的表。** 实验、功能开关、计费与用量表各不相同。报告一张你从未确认其存在的表的结果，是典型的失败模式。先用 `SHOW TABLES` / `DESCRIBE TABLE` 探测。
- **保留期断崖。** 如果相关窗口早于表的保留期或 dbt 模型的创建日期，那是*缺口*，不是空结果。要明确说明，以免综合者把"无结果"读成"无活动"。
- **Notebook 不可查询。** SQL MCP 看不到 Databricks notebook。如果你怀疑理由在某个 notebook 中，返回一个缺口。

## 需要返回什么

对每项相关发现：
- 类型（产品事件 / 实验曝光 / 用量或计费事件 / 系统表行 / dbt 模型）
- 全限定表名与你运行的确切查询
- 查询的时间窗口
- 精简的数值摘要（计数、百分位数、首次/最后出现时间戳）。**不要倾倒原始行。**
- 与目标上线日期的时间相关性（例如 "first row 2024-08-15, PR #49074 merged 2024-08-14"）
- 相关性 + 强度：直接 / 间接 / 弱
