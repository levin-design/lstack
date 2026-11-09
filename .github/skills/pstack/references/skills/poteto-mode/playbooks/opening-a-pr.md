### Opening a PR

在其他每个剧本末尾调用。

**工作树。** 从 main 上的 git 工作树工作。子代理继承它。同一分支上的多次 `runSubagent` 调用各自获得自己的工作树，或在它们之间执行 `git fetch && git reset --hard origin/<branch>`。分支上有无关工作的脏状态：patch 出来，换新工作树，应用。工作树一团糟：从 main 重置，最小化重做。

**提交。** 放开提交。打开 PR 前 rebase 成小而有序的提交。每个提交都是未来的一个 PR：可落地，顺序能讲清故事。修复属于刚做的提交时用 amend。可分离时用新提交。提交正文不复述主题。

**PR。** 提交前对差异运行 **unslop** 技能，评审前运行 `/no-comments`。用 `/technical-writing` 写每个 PR 标题、描述和提交正文（除 Diátaxis 外的每一层，并应用 STE 词汇规则：一个动作一个词、保留冠词、能用普通动词就不用 `-ing`），然后应用 `/unslop`。

**标题。** Conventional Commits `type(scope): subject`，不加句末句号。类型如 `feat`、`fix`、`docs`、`refactor`、`test`、`chore` 或 `perf`。Scope 是领域，如 `pstack` 或 `poteto-mode`。Subject 简短、祈使式，当某个真实符号承载改动时点名它，例如 `fix(pstack): retarget opening-a-pr babysit trigger`。

**描述。** PR 正文是给已有差异的评审者的一分钟简报，不是实验记录。它说明改动为何存在、遗漏了什么、可能破坏什么，以及你如何证明它有效。写简短、简单的句子，少用标识符，不要大段文字墙。正文会成为 squash 提交正文，所以让该提交保持在约 40 行以内。按此顺序使用 `##` 标题而非加粗引导语，没有内容可说的章节直接删掉：

- `## Why`：问题与方法，1–3 个短句。不写 SHA、rebase 家谱或 “based on main” 前言。
- `## What changed`：1–3 个简短条目。只有当真实符号或路径承载改动时才点名。重命名或重定向要写出两侧。
- `## Scope`：始终保留。1–3 个简短条目，说明覆盖什么、有意排除什么（后续项、已知缺口）。不写符号、路径或逐文件长文。
- `## Tradeoffs`：只写评审者否则会问的被拒替代方案。没有真正选择时跳过。
- `## Blast Radius`：1–2 句，说明触及谁或什么，以及为何安全或有风险。如果 main 是红的，说明让它保持红色的代价。
- `## Verification`：1–3 个条目，每条是真实运行路径及其结果。性能：一个带单位的主数字、`before → after`，其余链接到 arena 或 swarm 目录。不写样本量方法学、swarm 朗诵或指标表。

在各章节之后，当视频或截图能证明某条声称时附上它们。完整 SHA、swarm 或 arena 通道朗诵、杠杆修正长文、逐文件清单和 “CLEAN” 裁决放进链接的产物，而不是正文。

**托管平台。** 每个 PR 操作都用 GitHub CLI（`gh`）：创建、编辑、查看、监视、合并。不要求 Graphite（`gt`）。如果 `gh` 不可用，停下并告诉用户该运行哪些命令。

**内置 PR 工具。** 当 MCP 服务器或另一个工具提供 PR 操作时，通过它创建、编辑、重定向并标记就绪，工具未覆盖的一切用 `gh`。本次运行没有此类工具时，每个 PR 操作都用 `gh`。

**规模与栈。** 五个窄 PR 优于一个大 PR。栈是一条基分支链。根 PR 指向 trunk。每个子分支 rebase 到其父分支的确切尖端，其 PR 指向父分支。父分支合并时，按 `playbooks/shipping.md` 第 4 步把其子分支移到 trunk 上。没有 MCP PR 工具时，用 `gh pr create --base <parent-branch>` 创建子 PR，用 `gh pr edit <pr> --base <parent-branch>` 重定向。只有独立工作才从 trunk 拉分支。做实质性的栈工作前先在 trunk 上 rebase。

**就绪状态。** 每个 PR 都以就绪状态打开，绝不作为草稿。PR 工具可能默认草稿，所以通过它每次创建调用都设 `draft: false`。用 `gh` 时省略 `--draft`。如果 PR 仍以草稿打开，用 `gh pr ready <number>` 标记就绪。在提及 PR 状态之前先运行 `gh pr view <number>`。

**Babysit。** 打开 PR 不会启动 babysit。贴出 URL 继续构建。先完成阶段或栈。只有当整个栈存在后用户要求时，才单独跑一轮 babysit。为每个新 PR 各跑一次 babysit 会拖住构建，并把检查花在后续波会重启的提交上。当反馈偏离意图时提出反驳。

打开 PR 的子代理运行 **unslop** 技能和 `/no-comments`，并贴出 URL。它不做 babysit 就返回父级，除非它是 Autopilot-full 或 Autopilot-stack 的负责人。该负责人的简报指派了 babysit 循环，也就是 `playbooks/babysit.md` 等待的请求。负责人在其代码就绪报告之后启动循环，报告可合并，并豁免此处及 `playbooks/babysit.md` 中“等整个栈建好再做 babysit”的规则。
