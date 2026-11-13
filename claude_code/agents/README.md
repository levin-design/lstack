# Agents

Claude Code subagents. All are project-agnostic; project details come from the brief and the project's own docs.

Tool names match each file's `tools` frontmatter.

| File | Role | Tools | Use when |
| --- | --- | --- | --- |
| `tech-lead.md` | Technical lead | Read, Write, Edit, Bash, Grep, Glob, Agent, TodoWrite | Cross-role work that needs planning, dispatch, and acceptance |
| `architect.md` | Architect | Read, Grep, Glob, TodoWrite | Interfaces, module boundaries, contracts, trade-offs |
| `engineer.md` | Engineer | Read, Write, Edit, Bash, Grep, Glob, TodoWrite | Implement against a frozen contract |
| `ci-engineer.md` | CI/CD engineer | Read, Write, Edit, Bash, Grep, Glob, TodoWrite | Maintain pipelines, workflow config, caching, and release automation |
| `reviewer.md` | Reviewer | Read, Grep, Glob, TodoWrite | Find blocking problems before merge |
| `verifier.md` | Verifier | Read, Grep, Glob, Bash, TodoWrite | Independently run builds, tests, and acceptance steps |
| `writer.md` | Technical writer | Read, Write, Edit, Grep, Glob, TodoWrite | README, design docs, PR descriptions |
| `poteto-agent.md` | Poteto delegate | Read, Write, Edit, Bash, Grep, Glob, TodoWrite | Delegate code work inside a poteto-mode run |
| `comment-sicko.md` | Comment reviewer | Read, Grep, Glob, TodoWrite | Delete comments that carry no constraint |

## Install

Run from the `claude_code/` directory:

```bash
find agents -maxdepth 1 -name '*.md' ! -name README.md -exec cp {} <project>/.claude/agents/ \;
```

Or install for the current user:

```bash
mkdir -p ~/.claude/agents
find agents -maxdepth 1 -name '*.md' ! -name README.md -exec cp {} ~/.claude/agents/ \;
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
