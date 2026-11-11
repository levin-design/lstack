# Agents

Claude Code subagents. All are project-agnostic; project details come from the brief and the project's own docs.

| File | Role | Tools | Use when |
| --- | --- | --- | --- |
| `tech-lead.md` | Technical lead | read, write, edit, bash, agent, todo | Cross-role work that needs planning, dispatch, and acceptance |
| `architect.md` | Architect | read-only | Interfaces, module boundaries, contracts, trade-offs |
| `engineer.md` | Engineer | read, write, edit, bash | Implement against a frozen contract |
| `reviewer.md` | Reviewer | read-only | Find blocking problems before merge |
| `verifier.md` | Verifier | read, bash | Independently run builds, tests, and acceptance steps |
| `writer.md` | Technical writer | read, write, edit | README, design docs, PR descriptions |
| `poteto-agent.md` | Poteto delegate | read, write, edit, bash | Delegate code work inside a poteto-mode run |
| `comment-sicko.md` | Comment reviewer | read-only | Delete comments that carry no constraint |

## Install

```bash
cp agents/*.md <project>/.claude/agents/
```

Or install for the current user:

```bash
mkdir -p ~/.claude/agents
cp agents/*.md ~/.claude/agents/
```

## Use

Ask Claude to use a subagent by name. For example:

```text
Use the tech-lead subagent. Goal: <one sentence>. Scope: <directories>.
Done when: <verifiable condition>. Start with recon; do not write code yet.
```

`tech-lead` dispatches the other agents through the `Agent` tool. Multiple independent dispatches in one message run concurrently.

## Customization

- Do not put project paths or module names in these files.
- Pass project facts through the brief.
- When a project needs a permanent role, copy one file, change `name`, `description`, tool list, and boundaries, and keep the generic version untouched.
