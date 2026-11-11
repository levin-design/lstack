# pstack in Claude Code

pstack skills use Cursor names. Read this file once per session, then map every Cursor name in a skill using the tables below. `<pstack>` is the folder that holds `skills/` and `docs/`. If a Cursor field has no row here, drop it and say so. Never pass a field or value the tool schema rejects.

## Tools

| Cursor | Claude Code |
| --- | --- |
| `Task` | `Agent` |
| `AskQuestion` | `AskUserQuestion`. In `-p` mode it is unavailable; ask in plain text. |
| Open a todo list | Use `TodoWrite` when the session provides it. Otherwise keep the list in the reply and update it at each phase. |
| Run another pstack skill (`/name` or "the **name** skill") | `Read` `<pstack>/skills/<name>/SKILL.md` and follow it. The `Skill` tool rejects most pstack skills. When telling the user to type it, write `/pstack:<name>`. |
| `Grep`, `Glob` | When the session lacks them, use `Bash` with `rg`. |

## Subagent fields

| Cursor | Claude Code |
| --- | --- |
| `subagent_type: generalPurpose` | `subagent_type: "general-purpose"` |
| `poteto-agent`, `comment-sicko` | `pstack:poteto-agent`, `pstack:comment-sicko` for a plugin install; `poteto-agent`, `comment-sicko` for a manual install. |
| `readonly: true` | `subagent_type: "Explore"`. It keeps `Bash`, so the brief must also say "do not edit files"; check `git status` afterwards. |
| `readonly: false` | `general-purpose`. It keeps the session's MCP servers. |
| `environment: "cloud"` | `isolation: "worktree"`. State the branch or commit the worker must check out. |
| `environment: "local"` | Omit. |
| `cloud_base_branch: <b>` | Tell the worker to check out `<b>` first. |
| `run_in_background: true` | Omit. Subagents run in the background by default and notify you when done. |
| `resume` | Spawn a new agent and paste the previous result into its brief. |
| `file_attachments` | List the paths in the brief. |

## Models

| Cursor | Claude Code |
| --- | --- |
| `claude-<family>-<version>-<effort>[-fast]`, for example `claude-opus-5-5-xhigh` | `model: "opus"` plus `effort: "xhigh"`. `model` accepts `opus`, `sonnet`, `haiku`, and `fable`. Drop `-fast`. |
| `grok-*`, `gpt-*`, or another non-Claude slug | Omit `model`, let the agent run on the session model, and say so. |
| `auto` or `inherit-parent` | Omit `model`. |
| `pstack-models.mdc`, `~/.cursor/rules/pstack-models.mdc` | `~/.claude/rules/pstack-models.md`. Claude Code loads it into every new session, so the role lines are already in context. If a file or role line is missing, use the skill defaults. |
| Role value `<model> <effort>`, for example `opus high` | `model: "opus"` plus `effort: "high"`. |

## setup-pstack

Claude Code loads every `.md` file in `~/.claude/rules/` into each new session, so `setup-pstack` writes the rule there. Apply these changes to its steps:

- Detection: the `model` values exposed by the `Agent` tool schema, each with an `effort` value. Write a real model as `<model> <effort>`, for example `opus xhigh`. The effort is the last token, so the budget step works as written.
- Defaults: map each default slug using the table above. `claude-opus-5-5-xhigh` becomes `opus xhigh`; `grok-4.7-xhigh-fast` becomes `inherit-parent`.
- Write: `~/.claude/rules/pstack-models.md`, with no frontmatter, then the comment lines, the `# budget` line, and one line per role from step 5. Overwrite the whole file. Never put role lines in `CLAUDE.md` or `AGENTS.md`.

## Paths

| Cursor | Claude Code |
| --- | --- |
| `.cursor/skills/`, `~/.cursor/skills/` | `.claude/skills/`, `~/.claude/skills/` |
| `~/.cursor/plugins/`, `.cursor-plugin/plugin.json` | `~/.claude/plugins/`, `.claude-plugin/plugin.json` |
| `.cursor/rules/*.mdc`, always-applied rules | `CLAUDE.md`, or `AGENTS.md` when there is no `CLAUDE.md`. Claude Code never reads `.mdc` files. Model rules are the exception. |
| `https://github.com/cursor/plugins/blob/main/pstack/<path>` | Use `<pstack>/<path>` when the file exists. Read the local copy, never fetch the remote one. Give the user a URL only when a link is needed. |
| Transcripts in `~/.cursor/projects/<slug>/agent-transcripts/` | `~/.claude/projects/<slug>/<session>.jsonl`. The slug is the workspace path with each `/` and `.` replaced by `-`. The newest `.jsonl` is the current session. Its `<session>/subagents/` folder holds subagent transcripts. Read only folders for this workspace. |

## Cursor-only features

Claude Code has no Cursor Automations, Bugbot, Cursor cloud agents, or built-in PR tooling. When a step needs one, write one line, `Skipped in Claude Code: <step>. <reason>.`, and continue. Do not stop, ask, or retry. When a later step needs an artifact from the skipped step, such as a URL or a key, leave a placeholder and explain it on that line.

| Cursor | Claude Code |
| --- | --- |
| Cursor Automations: routines, `update_state` routine calls, `api2.cursor.sh/automations` webhooks, routine wake-ups, `SendToUser` key requests | Note the skip and continue. |
| Bugbot | Bugbot comments on GitHub PRs are ordinary review threads. Classify them with the forge commands the step provides. When a PR has no Bugbot check or comment, skip the steps that start, wait for, or configure Bugbot. |
| Cursor cloud agents | `environment: "cloud"` maps to a worktree, as described under Subagent fields. Skip steps that need the cloud agent itself, such as its dashboard state or its own machine. |
| Built-in PR tooling | Use the forge commands the step provides, for example `gh pr create`. This is not a skip, so do not write the skip line. |
