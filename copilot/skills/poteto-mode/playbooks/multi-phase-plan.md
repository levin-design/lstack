### Multi-phase or multi-PR plan

**你负责计划，不负责代码。计划是一份清单，由负责人逐框执行，由操作者依据证据审计。** 计划就是交付物。不要实现。

1. 当改动只有一两个文件且方法显而易见时，跳过计划。说明原因并停止。
2. 写之前先用原型解决未决问题。每个问题运行一次 `playbooks/prototype.md`。保留分支、SHA 和截图供附录 A 使用。只向操作者询问任何运行都无法定夺的产品或偏好决策。给出选项（**never-block-on-the-human** 原则技能）。
3. 用 `agentName: "poteto-agent"` 并按照子代理一节指定显式模型的子代理进行探索（**guard-the-context-window** 原则技能）。按子代理一节，为每项工作选择每个子代理的推理水平和 fast 或 standard 速度。每个子代理返回文件指针、约定、测试命令和入口点。不要内联转储。
4. 把下面的骨架复制到计划文件并填写每个占位符。除非操作者指定路径，否则把文件写在代理存储的 `docs/` 下。保持每个标题和每个子块的显示顺序。每个 PR 一节。一个 PR 是一个改动，带自己的证据（**sequence-verifiable-units** 原则技能）。在 **How to read this** 中点名执行剧本。运行可能合并时选 `playbooks/autopilot-full.md`。由操作者落地 PR 时选 `playbooks/autopilot-stack.md`。常设项目采用 `playbooks/orchestrate.md`。
5. 完整按 `/technical-writing` 写作，然后 `/unslop`。正文是一种 Diátaxis 模式：how-to。附录承载解释与参考。每个标题陈述任务或发现。不用长破折号。不用句中冒号。
6. 运行 `node .github/skills/poteto-mode/scripts/check-plan.mjs <plan.md>` 并修复它打印的每一行（**encode-lessons-in-structure** 原则技能）。
7. 交回。贴出计划路径和脚本输出，然后停止。执行在操作者明确放行后、按计划点名的执行剧本开始。

**验证。** 仅靠测试不是充分的验证。只有当 PR 的 unit、live 和 perf 框全部勾选时，该 PR 才算验证通过（**prove-it-works** 原则技能）。这句话就是验证规则。每个验证块都以它开头。live 块是强制的。PR 尖端的十条通道按 **swarm** 技能，用 `swarm workers` 模型（当模型文件记录了已确认标签时，否则用父模型），通过其控制技能驱动真实界面。每条通道是一个框，含具体场景、它保存的截图及其通过谓词。一条通道是 **Regression lane against trunk。** 它在 trunk 和尖端运行同一承重场景。如果 trunk 没有该功能，该通道记录这一事实，并改为门禁差异新增的行为加上用户等待的终态，而不是凭空编造 trunk 结果。perf 门禁是双向的。trunk 和尖端都必须产出点名的指标。如果 trunk 缺少该功能，还要隔离差异新增的工作，并为该工作加上用户等待的端到端状态设定绝对预算。不要在不同场景之间声称比率。perf 块点名指标、交错探针、先测的 trunk 基线，以及带失败数字的规则。改变交互的 PR 受评审门禁。操作者在合并前通过聊天结合截图和视频评审它。不改变交互的 PR 写下 `**Review gate.** None. <PR id> is not review-gated.` 且其下没有框。

**控制技能。** 按界面选择。浏览器、Electron 和 Web UI 使用项目的浏览器驱动 harness。CLI 和 TUI 使用项目的 CLI harness。原生移动端使用仓库已有的任何模拟器驱动技能。触及两个界面的 PR 在两边都有通道。没有控制技能的界面是附录 C 中的风险，其 live 块仍要点名每条通道如何驱动它。

````markdown
# <Program> plan

<Under ten lines. What changes, for whom, the rule the program enforces, and the PR ids in order.>

## How to read this

One box is one unit of work. Every box names the evidence that checks it. A nested box is a sub-step of the box above it. Check a box only when its evidence exists, a file, a log line, a screenshot, a test run, or a SHA. The body is a how-to. The appendices explain and record.

The program runs `.github/skills/poteto-mode/playbooks/<execution playbook>.md`. <Who merges, and which PR ids are the operator's items that stop at merge-ready.>

Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

## Program checklist

### Arm the program

- [ ] State the protocol and this plan to the operator, then stop. Start execution only on the operator's explicit go.
- [ ] Read these from trunk at program start. Re-read them at every tick.
  - [ ] `git show origin/main:.github/skills/poteto-mode/playbooks/<execution playbook>.md`
  - [ ] `git show origin/main:.github/skills/swarm/SKILL.md`
  - [ ] `git show origin/main:<control skill path>`
  - [ ] `git show origin/main:.github/skills/poteto-mode/playbooks/opening-a-pr.md`
  - [ ] `git show origin/main:.github/skills/<each other leaf skill the program uses>/SKILL.md`
- [ ] On the operator's go, arm the audit tick as a 1-hour audit cadence you run manually with the tick prompt below. Never leave the cadence to memory.
- [ ] Use this tick prompt, verbatim. "Re-read the execution playbook from trunk. Audit the operation against it and fix drift in this tick. Probe every active lane and judge progress by side effects only. Stand down a stuck lane and dispatch its replacement now. Then post a short status message to the operator in chat only when the audit found a tracked change that no earlier status message reported, such as a PR opened, a code-ready head, a round launched or closed, a verdict, a merge, a stuck agent and the action taken, a blocker added or cleared, or a decision only the operator can make. Name every such change and nothing else. Do not repeat a table, the merged list, or an unchanged blocker. If the audit found none, end the turn with no reply text. Either way, log this tick's row in your decision trail. The row names the items reported, or none."
- [ ] On the operator's hold or stand-down, send every owner a zero-writes order at once.

### Spawn owners

- [ ] Spawn one owner per PR with the full lifecycle the execution playbook names.
- [ ] Follow this dependency graph. Start dependent work only after its parent merges, or base it on the parent branch when the execution playbook stacks.
  - [ ] <PR id> and <PR id> are independent and first. Both branch from `main`.
  - [ ] <PR id> after <PR id>.
- [ ] Hold the file boundaries. <PR id or class> touches only `<glob>`.
- [ ] Hold the review gate. <PR ids> change an interaction. They wait for the operator's review in chat with screenshots and a video before merge.

### PR mechanics, for every PR

- [ ] Resolve the forge once. Use the GitHub CLI (`gh`) for every PR operation. Never require `gt`.
- [ ] Open the PR ready, never draft, per **Opening a PR**. Use an MCP or tool PR integration when the run has one, else `gh pr create --base <base-branch>`. A stack child targets its parent branch.
- [ ] Run the repo's lint and typecheck once before the PR-facing push. Push with hooks on.
- [ ] Run the **unslop** skill before each commit and the **no-comments** skill before review.
- [ ] Triage every automated-review and security-reviewer comment per `../references/automated-review-triage.md`.
- [ ] Rebase onto current trunk before the code-ready report and babysit. Keep that merge base in fix rounds. Rebase again only at merge prep, on a `git merge-tree` conflict with trunk, on a CI failure that comes from a change on trunk, or when a known concurrent change to the same files lands.

### Verdict and merge, for every PR

- [ ] A full swarm runs once, at the code-ready head. Another full swarm runs only for new behavior, a redesign, or a large new diff. A rebase, a merge-conflict resolution, or a minor fix gets a single verifier at the new head, and a wording-only change gets none. Run each full swarm per the **swarm** skill. One gates lane. The ten live lanes from the PR's **Verify, live** block. The perf lane from its **Verify, perf** block. Two or more audit lanes, each with its own focus, that read the diff and the receipts and distrust the PR body. The root audits the receipts in the merge-ready report before the verdict.
- [ ] Judge every finding by the execution playbook's blocking rule. The verdict is clean when none blocks. A failure on trunk behavior in a lane marked `Regression lane against trunk.` is recorded against trunk and does not block the PR. A new head gets a fresh verdict, except for results that stay valid under the patch-id rule in `playbooks/shipping.md`.
- [ ] <The merge or handoff rule from the execution playbook, with the patch-id rule from `playbooks/shipping.md`.>

### Boot recipe, for every live lane

Each live lane runs in its own worktree at the PR head. Drive through the project's own UI or CLI harness.

- [ ] `git fetch origin <head-branch> && git checkout <head SHA>`.
- [ ] <Start the backend and the surface. Wait for ready.>
- [ ] <Deliver input only through the control skill's commands. Name the read-only diagnostics.>
- [ ] Save every screenshot to `/tmp/swarm-<pr-id>/worker-<n>/<slug>.png` and return the paths with the report.

## <Task as a verb phrase> (<PR id>)

**Depends on.** <PR id, or None.>

**Files.**

- [ ] Edit `<path>`.
- [ ] Create `<path>`.
- [ ] Delete `<path>`.

**Build.**

- [ ] <One change. Name the symbol and the file.>

**You see.**

- [ ] <One observable result, with the exact log line or screen state.>

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] <Test file and the case it gains.> Run `<command>`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `<swarm workers model>` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run <the same load-bearing scenario> at trunk and head. If trunk lacks the feature, record that and gate <the behavior the diff adds plus the end state the user waits for>. Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 2. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 3. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 4. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 5. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 6. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 7. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 8. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 9. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 10. <Scenario.> Save `<slug>.png`. Pass when <predicate>.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. <What is measured at both trunk and head. If trunk lacks the feature, also name the diff-added work and the end-to-end state the user waits for.>
- [ ] Probe. <The command or procedure, run at trunk and at the head, interleaved. Both sides must produce the metric.>
- [ ] Baseline. Record the trunk <value> first.
- [ ] Rule. <Head against trunk, with the number that fails. If the scenarios differ, add absolute budgets for the diff-added work and the user-visible end state instead of an invalid ratio.>

**Review gate.** The operator reviews before merge.

- [ ] Copy lane <n> screenshots into `<media path>/<pr-id>-review-<slug>.png`.
- [ ] Record a 30 to 60 second video of the change on a lane VM. Save it as `<media path>/<pr-id>-review.mp4`.
- [ ] Post the screenshots and the video in chat. Stop at merge-ready. Wait for the operator's click.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] automated review bot triage done.
- [ ] Rebased onto current trunk after the verdict, patch-id unchanged.
- [ ] <The owner squash-merges its own PR, or the root appends it to the base-branch stack and the operator lands it bottom-up.>

## Close the program

- [ ] Every box above is checked with its evidence.
- [ ] Reply to the operator with the report the execution playbook names.

## Appendix A. Prototype evidence

<Each open question a prototype answered, with the branch, the SHA, and the artifact links. Each question that stays unproven.>

## Appendix B. Alternatives rejected

<Each approach weighed and why it lost.>

## Appendix C. Risks

<Each risk with the PR it lands in and what the owner watches.>

## Appendix D. Links and reading list

<Docs to read before editing. Which PRs get `.github/skills/how/SKILL.md` and `.github/skills/interrogate/SKILL.md`. The trail per `.github/skills/show-me-your-work/SKILL.md`.>
````

**回复：** 计划路径、PR id 及其依赖和受评审门禁的集合、原型证明了什么、什么仍未证明，以及检查脚本的输出。
