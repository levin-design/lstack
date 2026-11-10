---
name: lstack
description: poteto 的严谨工程工作流，已适配 Copilot。它把任务匹配到剧本，交给全新的子代理执行，应用工程原则，并在宣布完成前对真实产物进行验证。当用户提到 lstack 或 poteto-mode，或要求以严谨方式完成功能、缺陷修复、重构、迁移、性能优化、PR 评审、PR 跟进与合并、对抗式多代理评审、验证技能、技术写作，或把工作流固化为可复用技能时使用。
argument-hint: "[任务、问题或 setup]"
disable-model-invocation: true
---

# lstack

改编自 Lauren Tan 的 pstack v0.15.36（MIT 许可证，见 `LICENSE`）。

本技能是入口。运行 `/lstack <任务>` 即进入 poteto 模式。58 个内置技能与它同级，位于 `skills/<name>/SKILL.md`；剧本、脚本和参考资料都在各自技能目录内。

## 运行方式

1. 完整阅读 [`../poteto-mode/SKILL.md`](../poteto-mode/SKILL.md)。该文件就是模式本身：它负责匹配剧本、列出原则并定义回复风格。
2. 按它执行。当它提到某个技能 `foo` 时，完整阅读 `../foo/SKILL.md` 并照做。技能内部的链接（`references/...`、`playbooks/...`、`scripts/...`）都相对于该技能所在目录。
3. 斜杠名称与技能目录一一对应：`/lstack` 是入口，`/foo` 加载同级技能 `foo`。所有技能都会出现在 Copilot 斜杠菜单里，但完整工作流只由 `/lstack` 驱动。
4. 开始任何任务相关的工作前，先建立待办列表，并把匹配剧本的步骤原样复制进去，按 poteto 模式的要求执行。
5. 角色模型和推理预算：`references/lstack-models.md` 存在时先读它；用户要求配置时，运行 [`../setup-lstack/SKILL.md`](../setup-lstack/SKILL.md)。

## 运行环境

本包面向 GitHub Copilot（VS Code）。工具名、路径和模型策略都按 Copilot 的能力写好，不需要再做概念映射。

- **子代理**：用 `runSubagent`，传 `agentName` 选择代理。`poteto-agent` 与 `comment-sicko` 是自定义代理，安装到 `.github/agents/`。省略 `agentName` 使用默认代理。
- **同步且无状态**：`runSubagent` 不支持后台运行、恢复或中途干预。把独立调用放在同一个工具块中批量发起；每个新工作单元重新派生子代理，附上合并后的完整简报。
- **提问**：用 `vscode_askQuestions`，优先给选项。
- **模型**：省略 `model` 即继承父会话模型。只有用户从 Copilot 模型选择器中确认过准确名称，且已记录到 `references/lstack-models.md` 时，才传 `model`。绝不编造模型名称。
- **只读评审**：用仅含读取与搜索工具的代理（`comment-sicko` 已如此定义），或在提示词中禁止改文件。
- **会话转录**：环境提供 `VSCODE_TARGET_SESSION_LOG` 时，它指向 `~/.vscode-server/data/User/workspaceStorage/<id>/GitHub.copilot-chat/debug-logs/`。找不到时询问用户，绝不扫描其他工作区。
- **没有托管能力**：PR 操作使用 `gh`；重复执行依赖待办列表和用户重新发送 `/lstack`；没有 `/loop`、自定义模式、定时自动化、云端 VM 或托管评审机器人，用项目自己的 CI 或自动化评审流程替代。
- **技能编写**：使用本文件与 `../poteto-mode/playbooks/authoring-a-skill.md` 中的规则。

缺少某项能力时，对应步骤应保留在待办列表中并标注 `skip: <原因>`，绝不静默删除。

## 技能地图

使用技能前先读对应文件。路径相对于本 `SKILL.md`。

### 模式、配置与元技能

| 技能 | 用途 |
|---|---|
| [poteto-mode](../poteto-mode/SKILL.md) | 主模式：剧本路由、原则、子代理和回复风格。 |
| [poteto-help](../poteto-help/SKILL.md) | 回答 lstack、配置或技能选择方面的问题。 |
| [setup-lstack](../setup-lstack/SKILL.md) | 配置各角色模型和推理预算。 |
| [automate-me](../automate-me/SKILL.md) | 把用户的工作习惯整理成个人模式技能。 |
| [reflect](../reflect/SKILL.md) | 把已结束的会话转化为经批准技能修改。 |

### 规划、设计与纠错

| 技能 | 用途 |
|---|---|
| [figure-it-out](../figure-it-out/SKILL.md) | 为大型或特殊任务设计专门的剧本。 |
| [architect](../architect/SKILL.md) | 写代码前先确定类型、签名和模块形态。 |
| [sharpen](../sharpen/SKILL.md) | 让任务更深而不是更大，然后重写提示词。 |
| [correct](../correct/SKILL.md) | 让代理在本仓库中无法重复同类错误。 |
| [blast-radius](../blast-radius/SKILL.md) | 找出变更在差异之外可能破坏的内容。 |
| [benchmark-checklist](../benchmark-checklist/SKILL.md) | 在报告或依据性能数据行动前审查测量。 |
| [tdd](../tdd/SKILL.md) | 存在廉价本地测试时，以测试先行的方式修复缺陷。 |

### 多代理协作

| 技能 | 用途 |
|---|---|
| [swarm](../swarm/SKILL.md) | 按切片、竞速或覆盖矩阵分派多个工作代理。 |
| [arena](../arena/SKILL.md) | 让多个候选方案处理同一任务，再择优嫁接。 |
| [interrogate](../interrogate/SKILL.md) | 对设计或差异进行对抗式或多代理评审。 |
| [reflect](../reflect/SKILL.md) | 并行评审会话记录，再修改技能。 |

### 理解与汇报

| 技能 | 用途 |
|---|---|
| [how](../how/SKILL.md) | 代码如何工作，以及新代码应放在哪里。 |
| [why](../why/SKILL.md) | 代码为何是现在这样，以及某个数字从何而来。 |
| [teach](../teach/SKILL.md) | 用平实语言解释一整块工作。 |
| [recall](../recall/SKILL.md) | 跨会话重建近期上下文。 |
| [ketchup](../ketchup/SKILL.md) | 追平本会话中发生的变更。 |
| [ketchup-video](../ketchup-video/SKILL.md) | 以带字幕的短视频形式完成同样的追平。 |
| [bro](../bro/SKILL.md) | 用平实语言复述上一条消息。 |
| [in-your-own-words](../in-your-own-words/SKILL.md) | 开始前先复述用户的目标和问题。 |
| [show-me-your-work](../show-me-your-work/SKILL.md) | 为长时间或无人值守的工作保留决策轨迹。 |
| [statechart](../statechart/SKILL.md) | 检查 TLA+ 模型并绘制状态图。 |

### 验证与评审

| 技能 | 用途 |
|---|---|
| [create-verification-skill](../create-verification-skill/SKILL.md) | 生成一个驱动真实应用的项目的验证技能。 |
| [maintain-verification-skill](../maintain-verification-skill/SKILL.md) | 保持验证技能和功能地图与实际一致。 |
| [create-formal-verification-skill](../create-formal-verification-skill/SKILL.md) | 生成基于模型检查或定理证明的验证技能。 |
| [maintain-formal-verification-skill](../maintain-formal-verification-skill/SKILL.md) | 代码变更后让形式化验证重新对齐。 |
| [no-comments](../no-comments/SKILL.md) | 用独立评审者（`comment-sicko`）清理注释。 |

### 写作

| 技能 | 用途 |
|---|---|
| [unslop](../unslop/SKILL.md) | 清除任何文字中的 AI 腔，包括回复本身。 |
| [technical-writing](../technical-writing/SKILL.md) | 文档、RFC、README、PR 描述和提交信息。 |
| [typescript-best-practices](../typescript-best-practices/SKILL.md) | `.ts` 和 `.tsx` 工作的 TypeScript 规则。 |

### 其他

| 技能 | 用途 |
|---|---|
| [make-bot-ui](../make-bot-ui/SKILL.md) | 构建一个通过 Webhook 触发机器人的小型 Web UI。 |

### 原则

应用任何原则前，先完整阅读对应的叶子文件，然后在回复中按名称引用它。每个原则位于 `../principle-<name>/SKILL.md`。

| 原则 | 适用时机 |
|---|---|
| laziness-protocol | 重构、评估差异大小，或想增加抽象时。 |
| foundational-thinking | 编写逻辑之前：类型、数据结构、顺序安排。 |
| redesign-from-first-principles | 把新需求融入既有设计时。 |
| attack-the-premise | 两个或更多修复共享同一个失败前提时。 |
| subtract-before-you-add | 安排新增、重构或重写时。 |
| minimize-reader-load | 代码难以追踪时。 |
| outcome-oriented-execution | 计划中的重写和迁移。 |
| experience-first | 产品、体验或范围取舍。 |
| exhaust-the-design-space | 没有先例的新交互或架构决策。 |
| build-the-lever | 任何非平凡工作：构建能证明它的工具。 |
| model-the-domain | 有状态或分支复杂的逻辑，或反复出现同一形状假设时。 |
| boundary-discipline | 接入校验、错误处理或框架适配器时。 |
| type-system-discipline | 设计类型或签名时。 |
| make-operations-idempotent | 命令、生命周期步骤和重试循环。 |
| migrate-callers-then-delete-legacy-apis | 在旧调用方仍存在时引入内部 API。 |
| separate-before-serializing-shared-state | 并发参与者共享文件、分支、键或对象时。 |
| prove-it-works | 任务完成后、宣布完成之前。 |
| fix-root-causes | 调试时。 |
| sequence-verifiable-units | 多步骤工作，以及堆叠提交或 PR 时。 |
| test-behavior-not-implementation | 编写、修改或保留测试时。 |
| explain-the-number | 信任、报告或依据某个测量值行动之前。 |
| guard-the-context-window | 上下文被大输出或长文件占满时。 |
| never-block-on-the-human | 想就可逆工作询问用户时。 |
| encode-lessons-in-structure | 第二次写同一条指令时。 |

## 剧本

剧本是 `../poteto-mode/playbooks/` 下的步骤清单，不是技能。poteto 模式把任务匹配到其中一个，并把步骤复制到待办列表。完整列表见 `../poteto-mode/SKILL.md` 的 Playbooks 一节。常见条目：

- Investigation（调查）、Bug fix（缺陷修复）、Perf issue（性能问题）、Hillclimb（指标爬坡）、Runtime forensics（运行时取证）、Trace forensics（轨迹取证）
- Feature（功能）、Refactoring（重构）、Prototype（原型）、Visual parity（视觉一致性）
- Authoring a skill（编写技能）、Eval（评测）
- Babysit（PR 跟进）、Shipping（合并交付）
- Autonomous run（自主运行）、Orchestrate（统筹）、Autopilot-full（全自动驾驶）、Autopilot-stack（自动叠栈）
- Session pickup（会话接续）、Pause safely（安全暂停）、Multi-phase plan（多阶段计划）、Worktree cleanup（工作树清理）、Opening a PR（创建 PR）

## 来源与维护

- 来源：Lauren Tan 的 pstack v0.15.36，MIT 许可证。随附 `LICENSE`。
- 转换说明：每个上游技能现在都是本包中的一个同级技能（`skills/<name>/SKILL.md`），会独立注册并可以单独调用。工具名、模型策略、会话路径和安装说明都按 Copilot 重写；上游产品专用的 frontmatter 键已移除；PR 平台回退逻辑只使用 `gh`。
- 更新方式：用上游新的 `skills/` 和 `agents/` 覆盖 `skills/` 与 `agents/`，保持每个技能目录内的文件名为 `SKILL.md`，然后重新应用「运行环境」一节的替换。
