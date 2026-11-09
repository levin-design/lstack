# Claude Code 中的 pstack

pstack 技能使用 Cursor 的名称。在 Claude Code 中，每个会话读一次本文件，然后用下面的表格映射技能中的每个 Cursor 名称。`<pstack>` 表示存放 `skills/` 和 `docs/` 的文件夹。如果某个 Cursor 字段没有对应行，就丢弃它并说明。绝不要传入工具的 schema 会拒绝的字段或值。

## 工具

| Cursor | Claude Code |
| --- | --- |
| `Task` | `Agent` |
| `AskQuestion` | `AskUserQuestion`。在 `-p` 模式下它不存在，所以用纯文本提问。 |
| 打开待办列表 | 如果会话提供 `TodoWrite`，就用它。否则把列表保存在回复中，并在每个阶段更新。 |
| 运行另一个 pstack 技能（`/name` 或"the **name** skill"） | `Read` `<pstack>/skills/<name>/SKILL.md` 并遵循它。`Skill` 工具会拒绝大多数 pstack 技能。当你告诉用户输入它时，写 `/pstack:<name>`。 |
| `Grep`、`Glob` | 当会话没有 `Grep` 或 `Glob` 时，用 `Bash` 配合 `rg`。 |

## Subagent 字段

| Cursor | Claude Code |
| --- | --- |
| `subagent_type: generalPurpose` | `subagent_type: "general-purpose"` |
| `poteto-agent`、`comment-sicko` | `pstack:poteto-agent`、`pstack:comment-sicko` |
| `readonly: true` | `subagent_type: "Explore"`。它保留 `Bash`，所以任务简报还要写"不要编辑文件"，之后你再检查 `git status`。 |
| `readonly: false` | `general-purpose`。它保留会话的 MCP server。 |
| `environment: "cloud"` | `isolation: "worktree"`。写明 worker 检出的分支或 commit。 |
| `environment: "local"` | 省略。 |
| `cloud_base_branch: <b>` | 告诉 worker 先检出 `<b>`。 |
| `run_in_background: true` | 省略。Subagent 默认在后台运行，完成时通知你。 |
| `resume` | 派生一个新 agent，并把之前的结果粘贴进它的简报。 |
| `file_attachments` | 在简报中列出路径。 |

## 模型

| Cursor | Claude Code |
| --- | --- |
| `claude-<family>-<version>-<effort>[-fast]`，例如 `claude-opus-5-5-xhigh` | `model: "opus"` 和 `effort: "xhigh"`。`model` 只接受 `opus`、`sonnet`、`haiku`、`fable`。丢弃 `-fast`。 |
| `grok-*`、`gpt-*` 或其他非 Claude slug | 省略 `model`，让 agent 使用会话模型运行，并说明这一点。 |
| `auto` 或 `inherit-parent` | 省略 `model`。 |
| `pstack-models.mdc` 规则，`~/.cursor/rules/pstack-models.mdc` | `~/.claude/rules/pstack-models.md`。Claude Code 会把它加载进每个新会话，所以其中的角色行已经在上下文中。如果不在，读取该文件。如果文件或角色的行缺失，使用技能的默认 slug。 |
| 角色值 `<model> <effort>`，例如 `opus high` | `model: "opus"` 和 `effort: "high"`。 |

## setup-pstack

Claude Code 会把 `~/.claude/rules/` 中的每个 `.md` 文件加载进每个新会话，所以 `setup-pstack` 把规则写在那里。按以下更改遵循它的步骤：

- 检测。检测到的模型是 `Agent` 工具 schema 列出的 `model` 值，每个配上其 `effort` 值中的一个。把真实模型写成 `<model> <effort>`，例如 `opus xhigh`。effort 是最后一个 token，所以预算步骤可以按原文工作。
- 默认值。用上面的行映射每个默认 slug：`claude-opus-5-5-xhigh` 是 `opus xhigh`，`grok-4.7-xhigh-fast` 是 `inherit-parent`。
- 写入。写入 `~/.claude/rules/pstack-models.md`，不带 frontmatter，然后是注释行、`# budget` 行，以及第 5 步为每个角色写的一行。覆盖整个文件。绝不要把角色行放进 `CLAUDE.md` 或 `AGENTS.md`。

## 路径

| Cursor | Claude Code |
| --- | --- |
| `.cursor/skills/`、`~/.cursor/skills/` | `.claude/skills/`、`~/.claude/skills/` |
| `~/.cursor/plugins/`、`.cursor-plugin/plugin.json` | `~/.claude/plugins/`、`.claude-plugin/plugin.json` |
| `.cursor/rules/*.mdc`，始终生效的规则 | `CLAUDE.md`，或当没有 `CLAUDE.md` 时的 `AGENTS.md`。Claude Code 从不读取 `.mdc` 文件。模型规则是例外。见"模型"。 |
| `https://github.com/cursor/plugins/blob/main/pstack/<path>` | 当该文件存在时使用 `<pstack>/<path>`。插件发布技能、`docs/guide/` 和 `README.md`。读取本地副本，绝不抓取远端。需要链接时给用户 URL。 |
| `~/.cursor/projects/<slug>/agent-transcripts/` 中的 transcript | `~/.claude/projects/<slug>/<session>.jsonl`。slug 是工作区路径，每个 `/` 和 `.` 改为 `-`，例如 `/Users/you/proj` 是 `-Users-you-proj`。该文件夹下最新的 `.jsonl` 是当前会话。其 `<session>/subagents/` 文件夹保存 subagent transcript。只读本工作区的文件夹。 |

## 仅 Cursor 的功能

Claude Code 没有 Cursor Automations、Bugbot、Cursor cloud agents 或内置 PR 工具。当某个步骤需要其中之一时，在回复中写一行 `Skipped in Claude Code: <step>. <reason>.`，然后继续下一步。不要停止、询问或重试。当后续步骤需要被跳过步骤产出的东西时，例如一个 URL 或一个键，留一个占位符并在该行中说明。

| Cursor | Claude Code |
| --- | --- |
| Cursor Automations：routine、`update_state` routine 调用、`api2.cursor.sh/automations` webhook、routine 唤醒，以及 `SendToUser` 密钥请求 | 用那一行注明跳过。 |
| Bugbot | GitHub PR 上的 Bugbot 评论是普通的审阅 thread，所以用步骤给出的 forge 命令分类。当 PR 没有 Bugbot 检查或评论时，跳过启动、等待或配置 Bugbot 的步骤。 |
| Cursor cloud agents | `environment: "cloud"` 映射为 worktree，如"Subagent 字段"所述。跳过需要 cloud agent 本身的步骤，例如其 dashboard 状态或其自有机器。 |
| 内置 PR 工具 | 使用步骤给出的 forge 命令，例如 `gh pr create`。这不算跳过，所以不要写那一行。 |
