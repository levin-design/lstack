# Linear 工单

## 本来源包含什么

- 描述功能、缺陷及其动机的 issue
- 附加在 issue 上的项目文档（通常是 PRD 或规格说明）
- 父/子 issue 关系（更宏大的计划 → 具体工单）
- issue 上的评论（澄清、范围变更、"我们为什么做这件事"的理由）
- 标签（例如 `compliance`、`customer-request`、`perf`），标示动机的类型
- 解释范围变更的状态更新
- 附件与关联的 GitHub PR

Linear 常常是产品/业务背景所在之处："我们做这件事是因为客户 X 提出了要求"，或者"这是为了 Q3 合规计划"这一层。

## 如何检索

使用 Linear MCP。

1. **从关联工单开始。** 如果种子提交或 PR 引用了工单 ID（例如 `ENG-1234`、`[BUG-567]`），先用 `get_issue` 获取它们。阅读完整 issue，包括评论。
2. **按关键词列出相关 issue。** 用 `list_issues` 按功能名、关键符号或业务术语做文本搜索。多试几种措辞。
3. **沿 issue 树向上走。** 如果你落在子 issue 上，获取它的父 issue。子 issue 是战术性的；父 issue 常常承载"为什么"。
4. **阅读项目文档。** 如果 issue 属于某个项目，用 `get_project` 并查看附加文档。规格与理由最常记录在项目级文档中。
5. **检查标签与里程碑。** 标签暗示动机类别（customer-request、incident-followup、compliance）。里程碑把工作与截止日期绑定，这常常揭示动机。

## 这里的良好证据长什么样

- issue 描述中陈述业务问题："Customer Acme needs X because of their SOC2 audit"
- 记录某项决策的评论："We decided to go with approach B because approach A would require touching the billing service"
- 标题类似计划的父 issue："Q3 Enterprise Readiness" 或 "Reduce Payment Failures"
- 附加的 PRD 或规格说明
- 类似 `customer:acme`、`incident-followup`、`compliance`、`perf-regression` 的标签

## 常见陷阱

- **范围漂移。** PR 引用的工单可能已被关闭，又以不同范围重新打开。要读完整历史。
- **机械模板。** 有些团队要求填写"Why"部分，却用套话填充。泛泛的文字（"改善用户体验"）大概不是真正的答案。
- **过时工单。** 旧工单常常反映的是已经改变的方案版本。检查日期，并与代码的上线日期交叉核对。
- **以重复关闭的链条。** 沿 duplicate-of 关系回溯到规范工单。
- **私有工作区内容。** 如果你无法访问某个 issue，将其记为缺口，而不是猜测。

## 需要返回什么

对每个相关工单：
- 工单 ID 与标题
- 从描述或评论中引用的原问题/动机（不要转述。综合者需要原文才能引用）
- 标签、父 issue、项目
- 作者、创建日期、关闭日期
- 工单链接（如果可用）
