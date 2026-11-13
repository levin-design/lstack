# pstack for Claude Code

A Claude Code adaptation of [pstack](https://github.com/cursor/plugins/tree/main/pstack). The skills are the upstream English skills, copied unchanged except for `setup-pstack` and the documentation links in `poteto-help`. The only adaptation layer is `docs/claude-code-adapter.md`, which maps Cursor names to Claude Code equivalents at runtime. This package adds a generic digital-employee team in `agents/`.

## What is different from pstack

| Area | Change |
|---|---|
| Skills | Copied from `pstack/skills` (English). `setup-pstack` is rewritten to write `~/.claude/rules/pstack-models.md`, and `poteto-help` links are rewritten to this package's docs. |
| Cursor names | Mapped at runtime by `docs/claude-code-adapter.md`: `Task` → `Agent`, `AskQuestion` → `AskUserQuestion`, `run_in_background` → omit, model slugs → `opus`/`sonnet`/`haiku`/`fable` plus effort. |
| Agents | Nine Claude Code subagents in `agents/`: seven generic employees plus `poteto-agent` and `comment-sicko`. |
| Model config | `~/.claude/rules/pstack-models.md` instead of `~/.cursor/rules/pstack-models.mdc`. |
| Cursor-only features | Automations, Bugbot, cloud agents, and built-in PR tooling are skipped with a one-line note. |

## Install

Project install:

```bash
cp -R skills/. <project>/.claude/skills/
find agents -maxdepth 1 -name '*.md' ! -name README.md -exec cp {} <project>/.claude/agents/ \;
```

User install:

```bash
mkdir -p ~/.claude/skills ~/.claude/agents
cp -R skills/. ~/.claude/skills/
find agents -maxdepth 1 -name '*.md' ! -name README.md -exec cp {} ~/.claude/agents/ \;
```

Model rule (optional):

```bash
mkdir -p ~/.claude/rules
cp docs/pstack-models.example.md ~/.claude/rules/pstack-models.md
```

## Use

1. At session start, read `docs/claude-code-adapter.md` once. It is the mapping contract.
2. Type `/pstack:<skill>` when installed as a plugin, or `/<skill>` when the skills are installed directly. If a skill does not resolve, read `.claude/skills/<skill>/SKILL.md` (or `~/.claude/skills/...`) and follow it.
3. For cross-role work, ask Claude to use the `tech-lead` subagent.
4. For a single capability, use the skill directly, for example `/architect`, `/swarm`, `/interrogate`, or `/tdd`.

Example:

```text
Use the tech-lead subagent. Goal: add a refund endpoint to the payments module.
Scope: services/payments. Done when: build, tests, and an end-to-end request all pass.
Start with recon and a contract draft. Do not write code until I freeze the contract.
```

## Structure

```text
claude_code/
  README.md
  LICENSE
  docs/
    claude-code-adapter.md      Cursor to Claude Code mapping
    guide.md                    practical guide
    pstack-models.example.md    example model rule
  agents/
    README.md                   roster
    tech-lead.md
    architect.md
    engineer.md
    ci-engineer.md
    reviewer.md
    verifier.md
    writer.md
    poteto-agent.md
    comment-sicko.md
  skills/                       58 upstream pstack skills
```

## Limits

- Skills are not rewritten. Cursor-specific names are mapped by the adapter, not removed.
- The `Skill` tool rejects most pstack skills; read the `SKILL.md` file directly.
- Subagents are stateless. Every brief must be self-contained.
- Claude Code has no Cursor Automations, Bugbot, or cloud agents. Steps that need them are skipped with a note.
- No background loop or scheduler. Long runs need the user to send the next message.
