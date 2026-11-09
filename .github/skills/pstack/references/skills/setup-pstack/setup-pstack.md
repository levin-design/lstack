---
name: setup-pstack
description: 配置 pstack 在本项目中为每个角色使用哪些模型，以及偏好哪种推理预算。写入 .github/skills/pstack/references/pstack-models.md。当用户说 setup pstack、configure pstack models、pstack budget，或要求更改 pstack 的模型选择时使用。
---

# 配置 pstack

写入 `.github/skills/pstack/references/pstack-models.md`，这是一个记录 pstack 每个角色所用模型的项目文件。poteto mode 在每次调用 subagent 前都会读取它。

Copilot 不向 agent 暴露模型 API。唯一可靠的来源是用户看到的模型选择器。绝不要写入用户未确认的模型标签。

## 步骤

### 1. 确认可用模型

请用户粘贴他们希望分配给角色的模型在 Copilot 模型选择器中的确切标签。标签格式为 `Model Name (Vendor)`。如果他们不想要按角色选择，则每个角色都保持 `inherit-parent`。

`inherit-parent` 始终有效。它的含义是：在 `runSubagent` 中省略 `model`，让 subagent 在父聊天模型上运行。Copilot 中没有 `auto` 别名，也没有模型 slug 自动发现机制。

### 2. 加载当前状态

默认映射见步骤 5。如果 `.github/skills/pstack/references/pstack-models.md` 已存在，读取它，并将其 `# budget` 行和各角色值视为当前选择。否则从默认值开始。删除角色不在步骤 5 中的任何行，因为它来自已退役的角色。

### 3. 预算、映射与确认

**(a) 询问预算。** 使用 `vscode_askQuestions` 提供以下四个选项；如果文件中记录了当前预算，就说出它。没有文件时，说明 `large` 与默认值一致。

- `unlimited — 最高推理`
- `large — 高推理`
- `medium — 中等推理`
- `small — 快速或轻量推理`

**(b) 应用它。** 预算是建议性的。Copilot 通过所选模型及其设置来决定推理强度，因此记录预算，并在推荐选择哪个模型变体时使用它。它绝不改写已确认的标签。处于 `inherit-parent` 的角色不变。面板角色保持其列表长度，因为每个条目运行一个 subagent。

**(c) 展示角色并确认。** 展示每个角色及其模型，并把用户未确认的任何标签标记为需要选择。还要列出步骤 2 删除的每一行。询问是按原样接受还是更改特定角色，选项为已确认的标签加上 `inherit-parent`。使用 `vscode_askQuestions`，而不是自由文本。对于面板角色（arena runners、architect runners、interrogate reviewers），值是一个列表，每个条目运行一个 subagent，因此列表长度决定数量。`arena cross-judge pool` 也是一个列表，但 Arena 只运行一个评判者；它按列表顺序优先选择与父模型不同模型系列的值。`inherit-parent` 从不评判跨模型面板，因为它是父模型的模型。`swarm workers` 是每个 worker 的默认模型，除非一场竞赛为每个 arm 分配了另一个模型。

### 4. 校验

写入的每个模型标签都必须是用户从其选择器中确认过的。`inherit-parent` 始终通过。如果所选标签未确认，停止并再次询问。

### 5. 写入文件

写入 `.github/skills/pstack/references/pstack-models.md`，包含一行携带所选标签的 `# budget`，以及每个角色一行，使用与 poteto-mode 相同的角色名。覆盖整个文件，使重复运行保持幂等。形态如下：

```markdown
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` as a value: omit `model` in runSubagent, so the role runs on the parent chat model. List entries still count toward panel fan-out.
# budget: large (high)
feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
hillclimb: inherit-parent
judgment and prose: inherit-parent
hardest tasks: inherit-parent
how explorer: inherit-parent
how explainer: inherit-parent
why investigators: inherit-parent
why synthesizer: inherit-parent
reflect tooling: inherit-parent
reflect judgment, divergent, synthesizer: inherit-parent
arena runners: inherit-parent
arena cross-judge pool: inherit-parent
swarm workers: inherit-parent
architect runners: inherit-parent
interrogate reviewers: inherit-parent
```

### 6. 确认

告诉用户文件已写入，并且适用于本项目中的新 subagent 调用。重新运行本技能会更新它。

### 7. 提供验证技能（可选）

检查项目是否有驱动真实应用以获取证据的方式（`verify-*` 技能或现有的 harness）。如果没有，只提供一次：“想要一个项目本地验证技能，让 agent 能像用户那样驱动应用并证明改动有效吗？我可以用 create-verification-skill 技能生成一个。”若同意，读取 `../create-verification-skill/create-verification-skill.md` 并照做。若不同意，不再强推，继续后续步骤。

### 8. 提供形式化验证技能（可选）

检查项目是否已有形式化验证技能（一种针对代码运行模型检查器、证明或其他验证器的项目技能）。如果没有，只提供一次：“想要一个形式化验证技能，让 agent 能证明代码的关键性质在范围内的所有情形下都成立，而不仅是测试覆盖到的情况吗？我可以用 create-formal-verification-skill 技能生成一个。”若同意，读取 `../create-formal-verification-skill/create-formal-verification-skill.md` 并照做。若不同意，不再强推，继续后续步骤。
