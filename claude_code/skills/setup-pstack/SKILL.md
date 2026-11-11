---
name: setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget in Claude Code. Writes ~/.claude/rules/pstack-models.md.
---

# Setup pstack (Claude Code)

Write `~/.claude/rules/pstack-models.md`. Claude Code loads every `.md` file in `~/.claude/rules/` into each new session, so the role table is already in context.

## Steps

### 1. Detect available models

The `Agent` tool schema exposes the `model` values and `effort` levels you can pass to a subagent. Use them as the source of truth. If you cannot inspect the schema, ask the user to list the model and effort values they can use. Never write a model you have not confirmed. `inherit-parent` is always valid: omit `model` and the role runs on the session model.

Claude Code `model` values are `opus`, `sonnet`, `haiku`, and `fable`. Effort is a separate value such as `low`, `medium`, `high`, `xhigh`, or `max`.

### 2. Load current state

Read `~/.claude/rules/pstack-models.md` if it exists. Treat its `# budget` line and role values as current choices. Otherwise start from the defaults in step 5. Drop lines for retired roles.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Use `AskUserQuestion` when available; otherwise ask in plain text. Offer:

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Record the budget and use it when recommending an effort. The budget never rewrites a confirmed role value. `inherit-parent` stays `inherit-parent`. Panel lists keep their length: one subagent runs per entry.

**(c) Show the roles and confirm.** Show every role, mark any unconfirmed value, and ask whether to accept or change specific roles. For panel roles (`arena runners`, `architect runners`, `interrogate reviewers`) the value is a list and its length sets fan-out. `arena cross-judge pool` is a list, but Arena runs one judge from a family other than the parent's; `inherit-parent` never judges. `swarm workers` is the default for every worker unless a race assigns models per arm.

### 4. Validate

Every real value must be confirmed. `inherit-parent` always passes.

### 5. Write the rule

Write `~/.claude/rules/pstack-models.md` with no frontmatter, the comment lines, the `# budget` line, and one line per role. Overwrite the whole file so re-runs stay idempotent.

```
# pstack model configuration for Claude Code. One line per role.
# Values: `<model> <effort>` such as `opus xhigh`, or `inherit-parent` to use the session model.
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

### 6. Confirm

Tell the user the rule was written and applies to new sessions. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with the create-verification-skill skill." On yes, read `.claude/skills/create-verification-skill/SKILL.md` (or the user-level copy) and follow it. On no, move on without pushing.

### 8. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill. If not, offer once: "want a formal verification skill, so agents can prove a key property holds in every case in scope, not only the cases tests reach? I can generate one with the create-formal-verification-skill skill." On yes, read `.claude/skills/create-formal-verification-skill/SKILL.md` (or the user-level copy) and follow it. On no, move on without pushing.
