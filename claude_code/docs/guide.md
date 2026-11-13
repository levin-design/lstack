# Practical guide

This guide covers the daily use of pstack in Claude Code: what to type, when to use an agent, how parallelism works, and how model selection is configured.

## Mental model

| Piece | What it is | Who reads it |
| --- | --- | --- |
| Skill (`SKILL.md`) | Workflow knowledge, playbooks, principles | You type `/name`, or an agent reads the file |
| Agent (`agents/*.md`) | A role with tool boundaries and an output contract | Claude Code dispatches it as a subagent |
| Principle (`principle-*`) | Behavioral constraint | Referenced by skills and agents |
| Model rule | Role-to-model mapping | Subagents read it before dispatch |

Installing skills, defining agents, configuring models, and constraining behavior are four separate things.

## Install

Project install:

```bash
cp -R skills/. <project>/.claude/skills/
cp agents/*.md <project>/.claude/agents/
```

User install:

```bash
mkdir -p ~/.claude/skills ~/.claude/agents
cp -R skills/. ~/.claude/skills/
cp agents/*.md ~/.claude/agents/
```

The model rule is optional. See `pstack-models.example.md`.

## Entry points

| Need | Entry |
| --- | --- |
| A rigorous end-to-end workflow | `/pstack:poteto-mode` or read `skills/poteto-mode/SKILL.md` |
| One specific capability | `/pstack:<skill>` or read the skill file |
| Cross-role work with a team | Use the `tech-lead` subagent |
| Unsure which skill fits | `/pstack:poteto-help` |

## Skills

| Goal | Skill |
| --- | --- |
| Understand a subsystem | `how` |
| Understand why it was built this way | `why` |
| Recover recent context | `recall` |
| Design interfaces and module boundaries | `architect` |
| Try N candidates and graft the best parts | `arena` |
| Fan out N workers across slices | `swarm` |
| Adversarial review of a diff | `interrogate` |
| Write the failing test first | `tdd` |
| Vet a performance number | `benchmark-checklist` |
| Estimate blast radius | `blast-radius` |
| Draw a statechart | `statechart` |
| Remove AI slop from writing | `unslop` |
| Restate in plain language | `bro` |
| Technical writing standard | `technical-writing` |
| Deepen a prompt | `sharpen` |
| Play back the goal before starting | `in-your-own-words` |
| Turn lessons into a skill | `reflect` |
| Fix recurring mistakes at the root | `correct` |
| Generate a project verification skill | `create-verification-skill` |
| Configure models | `setup-pstack` |
| Catch up on this session | `ketchup` |
| Keep a reviewable decision trail | `show-me-your-work` |

## Playbooks

`poteto-mode` selects from 23 playbooks:

| Group | Playbooks |
| --- | --- |
| Investigation | `investigation`, `runtime-forensics`, `trace-forensics` |
| Change | `bug-fix`, `feature`, `refactoring`, `perf-issue`, `hillclimb`, `prototype`, `visual-parity` |
| Process | `orchestrate`, `autopilot-full`, `autopilot-stack`, `multi-phase-plan`, `babysit`, `shipping`, `session-pickup`, `pause-safely`, `opening-a-pr`, `worktree-cleanup` |
| Other | `eval`, `authoring-a-skill`, `autonomous-run` |

## Parallelism

Claude Code subagents run in the background by default. To run work in parallel, dispatch multiple independent `Agent` calls in one message. Each subagent is stateless and cannot see the others, so every brief must be self-contained.

Good fan-out:

- 2-5 workers per wave.
- Independent slices with isolated write areas.
- A clear completion criterion and verification command per worker.
- A report format of PASS, ISSUES, or BLOCKED with evidence.

Do not fan out work that shares files, depends on another slice's output, or needs a contract that is not frozen yet.

## Proving parallelism

Add a probe to every worker's brief:

```bash
echo "$(date -u +%FT%T.%3NZ) START <role> pid=$$" >> /tmp/<project>-parallel.log
# ... work ...
echo "$(date -u +%FT%T.%3NZ) END <role> pid=$$" >> /tmp/<project>-parallel.log
```

After all workers return, read the log. Overlapping intervals mean real parallelism. Starts spaced by roughly the previous worker's duration mean serial execution. Wall-clock time close to the longest single task is another signal.

## Model rule

`~/.claude/rules/pstack-models.md` is loaded into every new session. Values are `<model> <effort>` such as `opus xhigh`, or `inherit-parent` to use the session model.

- `inherit-parent`: omit `model`; the role runs on the session model.
- A real value: the role uses that model and effort.
- A comma-separated list on a panel role (`arena runners`, `architect runners`, `interrogate reviewers`) sets the fan-out count.
- `arena cross-judge pool` runs one judge from a family other than the parent's. `inherit-parent` never judges.

## Agents

| Agent | Tools | Role |
| --- | --- | --- |
| `tech-lead` | read, write, edit, bash, agent, todo | Orchestrates the team and owns acceptance |
| `architect` | read-only | Interfaces, boundaries, contracts, trade-offs |
| `engineer` | read, write, edit, bash | Implements against a frozen contract |
| `ci-engineer` | read, write, edit, bash | Maintains CI/CD pipelines, caching, and release automation |
| `reviewer` | read-only | BLOCKING and NON-BLOCKING findings |
| `verifier` | read, bash | Runs build, tests, and acceptance steps |
| `writer` | read, write, edit | README, design docs, PR descriptions |
| `poteto-agent` | read, write, edit, bash | Delegate for poteto-mode work |
| `comment-sicko` | read-only | Deletes comments that carry no constraint |

## Common pitfalls

| Symptom | Cause | Fix |
| --- | --- | --- |
| A skill does not resolve | Skills are installed directly, not as a plugin | Read `.claude/skills/<name>/SKILL.md` and follow it |
| A subagent cannot see prior results | Subagents are stateless | Paste the prior result into the new brief |
| Parallel workers conflict | Shared files or unfrozen contracts | Split by file or serialize the dependent slice |
| The model rule is ignored | It is not in `~/.claude/rules/`, or the role line is missing | Create the file or add the role line |
| Arena has no judge | The pool only contains `inherit-parent` | Add a real model from a different family |
| A Cursor-only step fails | No Automations, Bugbot, or cloud agents | Write the skip line and continue |
