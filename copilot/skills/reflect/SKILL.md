---
name: reflect
description: 在活动会话记录上并行启动三个评审子代理，提炼经验教训，并将每一条路由到对现有技能的具体修改上。在用户说 reflect 时使用。
disable-model-invocation: true
---

# Reflect

从当前对话中挖掘可长期保留的经验教训，然后将其路由到技能修改中。

当用户说 “reflect” 或 “/reflect” 时调用。当对话琐碎、离题，或已被父代理正确遵循的现有技能覆盖时跳过。一次性的偶发情况不算经验教训。

## 1. 定位活动会话记录

在展开并行任务之前，先找到本次对话的调试日志。环境变量 `VSCODE_TARGET_SESSION_LOG` 可用时会指向会话文件夹，位于 `~/.vscode-server/data/User/workspaceStorage/<id>/GitHub.copilot-chat/debug-logs/` 下。绝不要扫描其他工作区的文件夹。找不到日志时，改为传入一份精炼的会话摘要。

```bash
ls -t "$VSCODE_TARGET_SESSION_LOG"/* 2>/dev/null | head -10
```

读取匹配的日志，选取开头内容包含本次对话第一条用户提示词的那一份。若没有匹配项，改为传入一份精炼的会话摘要。

## 2. 并行启动三个评审者

一个工具调用块，三次 `runSubagent` 调用。评审者需要读取、搜索以及查找会话记录所引用的工单、聊天线程和可观测性追踪所需的任何 MCP 工具。不要让他们编辑文件。

用户确认了模型时，`.github/skills/lstack/references/lstack-models.md` 中的角色行会指明每个评审者使用的模型。没有确认的标签时，省略 `model`，让评审者继承父模型。绝不要编造模型标签。如果 `runSubagent` 拒绝某个标签，就省略 `model` 并说明情况。

| 视角 | 角色行 | 提示词模板 |
|---|---|---|
| 判断 | `reflect judgment, divergent, synthesizer` | `references/judgment-reviewer.md` |
| 工具 | `reflect tooling` | `references/tooling-reviewer.md` |
| 发散 | `reflect judgment, divergent, synthesizer` | `references/divergent-reviewer.md` |

逐字传入每个模板，并在标记处替换为会话记录路径或摘要。评审者在 `runSubagent` 的响应体中返回发现。

## 3. 综合

一次 `runSubagent` 调用；`model` 在已确认时取自 `reflect judgment, divergent, synthesizer` 行，否则省略以继承父代理。不要让它编辑已批准技能修改之外的仓库内容。它通过 MCP 抽查引用。逐字传入 `references/synthesizer.md`，并在标记处内联每个评审者的完整输出。它返回 Accepted / Rejected / Backlog 列表。

## 4. 结构强制检查

如果某个 Accepted 项能由 lint 规则、脚本、元数据标志或运行时检查更可靠地强制执行，就将其移到 Backlog。参见 **encode-lessons-in-structure** 原则技能。

## 5. 应用

展示综合者的完整 Accepted / Rejected / Backlog 输出，并在应用任何 Accepted 修改前等待明确批准。用户挑选子集，并可改变路由。技能变更会影响组织内每一个未来的代理。不要自动应用。

立即将每个 Backlog 项提交到你团队的 devex 或待办事项跟踪器，无需等待。只有 Accepted 列表需要等待批准。

绝不要编辑已安装的上游副本。批准前，展示其目标位置：项目技能为 `.github/skills/<skill>/`，个人技能为 `~/.copilot/skills/<skill>/`。批准后，将技能文件夹复制到该位置并编辑副本。绝不要开 PR 或推送。

严格按照每个已批准行的 Routing 执行：

- 对现有技能的琐碎修改（一行要点、收紧的句子、纠正过时事实）：由父代理直接完成。
- 对现有技能的实质性修改（新增章节、新增模式表、超过约 10 行）：遵循 `../poteto-mode/playbooks/authoring-a-skill.md` 及其“起草 / 测试 / 迭代”循环。
- `tune description: <skill path>`（技能存在，但本应触发时未触发）：围绕本应匹配的词语重写 description，然后对照 lstack 总览 `SKILL.md` 中的技能格式规则检查。
- `new skill: <kebab-name>`：创建 `.github/skills/<kebab-name>/SKILL.md`，目录名与之匹配并写具体 description；个人技能则用 `~/.copilot/skills/<kebab-name>/SKILL.md`。遵循编写手册，而不是自创格式。

如果你的环境自带 SKILL.md 校验器，在宣布完成前对每个改动过的技能运行它。

## 6. 向用户总结

简短列表，无开场白：

- 已应用的修改：`<skill path>`。每个一行说明改了什么。
- 新建的技能：`<skill path>`。每个一行（少见）。
- 已提交到 devex 跟踪器的 Backlog：`<issue title>`（`<tags>`）。每个一行。
- 丢弃：每个被拒绝的发现一行，附综合者给出的原因。
