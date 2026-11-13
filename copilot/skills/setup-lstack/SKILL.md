---
name: setup-lstack
description: 配置 lstack 在本项目中为每个角色使用哪些模型，以及偏好哪种推理预算。写入 .github/skills/lstack/references/lstack-models.md。当用户说 setup lstack、configure lstack models、lstack budget，或要求更改 lstack 的模型选择时使用。
---

# 配置 lstack

写入 `.github/skills/lstack/references/lstack-models.md`，这是一个记录 lstack 每个角色所用模型的项目文件。poteto mode 在每次调用 subagent 前都会读取它。

Copilot 不向 agent 暴露模型 API。唯一可靠的来源是用户看到的模型选择器。绝不要写入用户未确认的模型标签。

## 配置发现顺序（先读后问）

按顺序查找已有配置，找到第一个就停止：

1. `.github/skills/lstack/references/lstack-models.md`：本项目配置，Copilot 读取的位置。
2. `~/.copilot/lstack-models.md`：用户级默认，跨项目复用。
3. `~/.cursor/rules/pstack-models.mdc`：Cursor 的旧配置，只用于迁移。
4. 都没有：视为全部 `inherit-parent`，无需配置。

**短路规则。** 如果找到配置，且用户没有明确要求修改，只展示解析后的预算和角色表，问一句“沿用 / 修改某个角色 / 重新配置”，然后结束。不要重新询问预算，不要逐个角色确认。只有用户选择“重新配置”或点名要改某个角色时，才进入完整问答。

**零配置原则。** 默认值就是全部 `inherit-parent`。只有需要跨模型评审（`arena cross-judge pool` 用真实标签）或按角色分配不同模型时，才值得写这个文件。

## 步骤

### 1. 确认可用模型

请用户粘贴他们希望分配给角色的模型在 Copilot 模型选择器中的确切标签。标签格式为 `Model Name (Vendor)`。如果他们不想要按角色选择，则每个角色都保持 `inherit-parent`。

`inherit-parent` 始终有效。它的含义是：在 `runSubagent` 中省略 `model`，让 subagent 在父聊天模型上运行。Copilot 中没有 `auto` 别名，也没有模型 slug 自动发现机制。

### 2. 加载当前状态

默认映射见步骤 5。按“配置发现顺序”读取：把找到的 `# budget` 行和各角色值视为当前选择；只找到 Cursor 旧配置时，先按步骤 5 迁移到项目文件，不要继续读写 Cursor 路径。都没有时从默认值开始。删除角色不在步骤 5 中的任何行，因为它来自已退役的角色。

### 3. 预算、映射与确认

**(a) 询问预算。** 使用 `vscode_askQuestions` 提供以下四个选项；如果文件中记录了当前预算，就说出它。没有文件时，说明 `large` 与默认值一致。

- `unlimited — 最高推理（max）`
- `large — 极高推理（xhigh）`
- `medium — 高推理（high）`
- `small — 中等推理（medium）`

**(b) 应用它。** 预算是建议性的。Copilot 通过所选模型及其设置来决定推理强度，因此记录预算，并在推荐选择哪个模型变体时使用它。它绝不改写已确认的标签。处于 `inherit-parent` 的角色不变。面板角色保持其列表长度，因为每个条目运行一个 subagent。

**(c) 展示角色并确认。** 展示每个角色及其模型，并把用户未确认的任何标签标记为需要选择。还要列出步骤 2 删除的每一行。询问是按原样接受还是更改特定角色，选项为已确认的标签加上 `inherit-parent`。使用 `vscode_askQuestions`，而不是自由文本。对于面板角色（arena runners、architect runners、interrogate reviewers），值是一个列表，每个条目运行一个 subagent，因此列表长度决定数量。`arena cross-judge pool` 也是一个列表，但 Arena 只运行一个评判者；它按列表顺序优先选择与父模型不同模型系列的值。`inherit-parent` 从不评判跨模型面板，因为它是父模型的模型。`swarm workers` 是每个 worker 的默认模型，除非一场竞赛为每个 arm 分配了另一个模型。

### 4. 校验

写入的每个模型标签都必须是用户从其选择器中确认过的。`inherit-parent` 始终通过。如果所选标签未确认，停止并再次询问。

### 5. 写入文件

写入 `.github/skills/lstack/references/lstack-models.md`，包含一行携带所选标签的 `# budget`，以及每个角色一行，使用与 poteto-mode 相同的角色名。覆盖整个文件，使重复运行保持幂等。这是默认的唯一写入位置；不要写 `~/.cursor/rules/`，VS Code 不读它。只有用户明确要求跨项目复用时，才额外写一份 `~/.copilot/lstack-models.md`，项目文件仍然优先。若本次是从 Cursor 旧配置迁移，写完后告知用户旧文件可删除。形态如下：

```markdown
# lstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` as a value: omit `model` in runSubagent, so the role runs on the parent chat model. List entries still count toward panel fan-out.
# budget: large (xhigh)
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

告诉用户文件已写入，并且适用于本项目中的新 subagent 调用。补一句：除非模型变化或需要 Arena 跨模型评审，不要再次运行本技能。

### 7. 提供验证技能（可选）

检查项目是否有驱动真实应用以获取证据的方式（`verify-*` 技能或现有的 harness）。如果没有，只提供一次：“想要一个项目本地验证技能，让 agent 能像用户那样驱动应用并证明改动有效吗？我可以用 create-verification-skill 技能生成一个。”若同意，读取 `../create-verification-skill/SKILL.md` 并照做。若不同意，不再强推，继续后续步骤。

### 8. 提供形式化验证技能（可选）

检查项目是否已有形式化验证技能（一种针对代码运行模型检查器、证明或其他验证器的项目技能）。如果没有，只提供一次：“想要一个形式化验证技能，让 agent 能证明代码的关键性质在范围内的所有情形下都成立，而不仅是测试覆盖到的情况吗？我可以用 create-formal-verification-skill 技能生成一个。”若同意，读取 `../create-formal-verification-skill/SKILL.md` 并照做。若不同意，不再强推，继续后续步骤。
