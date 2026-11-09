# Sentry 错误历史

## 如何检索

使用 Sentry MCP。

1. **定位。** 如果你不知道项目 slug 和组织：

   ```
   find_organizations
   find_projects
   ```

2. **搜索与目标相关的问题。**

   ```
   search_issues (natural language, e.g., "errors in PaymentService timeout", "unhandled exceptions in uploadFile")
   ```

   根据目标所处理的异常类名、其函数或类名、它要检查的错误消息字符串，以及其文件路径来构建查询。

3. **按发布版本与时间窗口收窄。**

   ```
   search_issue_events (filter by release, time, environment, trace ID, tags)
   get_issue_tag_values (for an issue, see distribution across versions, users, environments)
   ```

   对某个疑似问题，检查**首次出现**与**最后出现**（停止时间是否与目标的上线日期吻合？）、**受影响的发布版本**（哪些版本出现过、哪个版本修复了它？）、以及**频率走势**（是否先激增、随后被解决？）。

4. **拉取完整事件以获得上下文。**

   ```
   get_sentry_resource (pass a Sentry URL or type+ID)
   ```

   堆栈轨迹是否经过目标代码？标签与面包屑是否与目标所防御的条件相符？

5. **检查目标附近落地的发布版本。**

   ```
   find_releases (around the commit date of the target)
   ```

   将发布版本与 PR 的合并日期交叉比对。

6. **谨慎使用 Seer。**

   ```
   analyze_issue_with_seer
   ```

   Seer 的 AI 根因分析是假设生成器。把它当作推断，而非权威结论。实际事件与堆栈轨迹才是主要证据。

## 需要返回什么

对每个相关 issue：
- Issue ID 与标题
- 项目与组织
- 首次出现 / 最后出现时间戳
- 事件数（如已知，附采样率）
- 受影响的发布版本
- 能体现与目标相关性的代表性堆栈轨迹片段（逐字摘录，不要总结）
- 首次/最后出现与目标上线日期的相关性
- 问题链接
- 任何作者评论或解决说明
