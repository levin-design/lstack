# 设置 pstack

本页你会安装插件、选择 pstack 使用的模型，并运行第一个任务。设置只需要一条命令加一段简短对话。

## 安装插件

在 Cursor 聊天中运行：

```text
/add-plugin pstack
```

Cursor 会确认插件已安装。

在 Claude Code 中，运行 `/plugin marketplace add cursor/plugins`，然后运行 `/plugin install pstack@cursor-plugins`。Claude Code 会给插件命令加前缀，所以本指南中的每条命令在那里都要加 `pstack:` 前缀，例如 `/pstack:setup-pstack`，它会把模型规则写入 `~/.claude/rules/pstack-models.md`。[Claude Code 适配指南](../harness/claude-code.md)涵盖了其他差异。

## 选择你的模型

运行：

```text
/setup-pstack
```

[`/setup-pstack`](../../skills/setup-pstack/SKILL.md) 会检测你有权访问的模型，询问推理预算，展示每个角色（代码委派、判断、评审面板），并询问你想要什么。回答这些问题。它会写入 `~/.cursor/rules/pstack-models.mdc`，这是一条每个 pstack 技能都会读取的小规则。

默认以 `xhigh` 推理运行，与 `large` 预算相同。`unlimited` 会把每个模型提升到其最高档位，最高到 `max`。Opus 会到 `max`。Grok 最高只到 `xhigh`，所以停留在那里。`medium` 和 `small` 会降低推理并消耗更少 token。

你只需覆盖你在意的部分。规则中没有对应行的角色保持技能默认值。要恢复默认，删除该角色的行。重新运行 `/setup-pstack` 会保留任何模型与默认值不同的角色。当默认值变化时，变化之前写入的规则仍会钉住旧默认值，所以请删除那些角色行，或删除整个文件，然后再次运行 `/setup-pstack`。

你可能想知道使用 Auto 会发生什么。把角色设为 `inherit-parent` 或 `auto`，pstack 会省略 subagent 的 `model` 字段，因此 subagent 继承你父聊天的模型。两个值含义相同，也都不是 model slug。对于面板角色，该值是一个列表，每个条目运行一个 subagent，因此列表长度决定面板大小。Setup 还会配置 `swarm workers`，即每个 `/swarm` worker 的默认模型，除非某场竞赛为每个分支指定了模型。

## 接受或拒绝验证提议

在 setup 结束时，`/setup-pstack` 会寻找证明你项目中应用行为的方法，要么是 `verify-*` 技能，要么是现有的 harness。如果两者都没找到，它会提议用 [`/create-verification-skill`](../../skills/create-verification-skill/SKILL.md) 生成一个。

回答 yes，它会写入 `.cursor/skills/verify-<app>/`，这是一个项目本地技能，教 agent 像用户一样驱动你的应用。它在交接之前会先证明该技能可用一次。回答 no，setup 继续。你随时可以自己运行 `/create-verification-skill`。[验证并交付](./06-verify-and-ship.md#创建项目验证技能)深入介绍了它。

如果你是 pstack 新手，请回答 yes。能检查自己工作的 agent 会一直推进到检查通过。不能检查的 agent 会把每个结果交回给你手工核对。在本指南的所有内容中，验证技能的回报最大。

随后 setup 会提议用 [`/create-formal-verification-skill`](../../skills/create-formal-verification-skill/SKILL.md) 生成一个形式化验证技能，除非项目已经有这样的技能。测试检查的是有人想到要写的用例。形式化验证技能会在声明的范围内检查你代码的一个关键性质，例如"一个任务绝不会同时运行两次"，并覆盖范围内的每一种情况。当你的代码涉及并发、重试、状态机或解析器时回答 yes——这类地方的 bug 代价高昂，而测试很少触及会出错的那种情况。否则回答 no，以后情况变化时再运行。[验证并交付](./06-verify-and-ship.md#用形式化验证技能证明一个性质)涵盖了它。

完成 setup 后，开始一个新聊天。模型规则会应用于新会话。

## 控制成本

pstack 会在 subagent 和评审面板上花费额外 token。这是严谨性的代价。要少花一些：

- 重新运行 `/setup-pstack`，选择更小的推理预算或更便宜的模型。主聊天用强模型、代码角色用更便宜更快的模型，是一个好组合。
- 把角色设为 `auto` 或 `inherit-parent`，让它使用聊天自身的模型。
- 缩短面板列表。每个条目运行一个 subagent。
- 把 `/poteto-mode` 留给需要严谨性的工作。小而明显的编辑不需要。

## 运行你的第一个任务

挑一件真实但很小的事，像对同事描述那样描述它：

```text
/poteto-mode add a --json flag to this command. text output stays byte-identical. verify both.
```

观察待办列表。它的第一批条目是匹配到的剧本步骤复制进来的，对于这条 prompt 就是 Feature 剧本。如果 `/poteto-mode` 跳过了某个步骤，该步骤会带着 `skip: <reason>` 留在列表中，这样你能看到它选择不做什么。

从这里开始，你可以输入普通的后续消息。要让 `/poteto-mode` 在整个聊天中保持开启，在 `/` 菜单中选择它时用 Option+Enter（Mac）或 Alt+Enter（Windows），而不是 Enter。这会把技能变成 [Custom Mode](https://cursor.com/docs/skills#using-a-skill-as-a-custom-mode)，在每一轮都保留在上下文中，直到你退出。Custom Modes 在 Agents Window 和 CLI 中可用。普通 Enter 只会把技能附加到一条消息上，随着聊天推进它就会淡出。

下一步：[通过 `/poteto-mode` 引导工作](./02-poteto-mode.md)。
