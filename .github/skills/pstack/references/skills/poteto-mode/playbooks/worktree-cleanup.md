### Worktree and simulator cleanup

1. 快照并审计。记录 `df -h /`，然后运行 `scripts/worktree-audit.sh [-b <pr-base-ref>] [repo-path]`（principle-build-the-lever）。不带 `-b` 时它对照 `origin/HEAD` 检查 `MERGED`，所以当 PR 目标分支是其他分支时要传 `-b origin/<branch>`。它从 `git worktree list` 读取路径，绝不手打，因为手打的 `myrepo-worktrees/x` 会漏掉位于 `.cursor/worktrees/myrepo/x` 的那个（principle-encode-lessons-in-structure）。它按大小、年龄、合并状态、未提交工作、PR 状态，以及最近触及它的对话来分类每个工作树，然后给出分桶建议。会话记录扫描很慢，放到后台跑。
2. 分桶是建议，不是许可。被固定和活跃的对话才是真实产物（principle-prove-it-works）。从用户或侧边栏取得该集合，并交叉核对每个候选。该杠杆曾把用户固定的工作树标为 `safe`，所以以固定集合为准。
3. 删除前先核实使用情况。对每个 `verify-recent-chat` 行，或任何你有疑问的项，把子代理铺开去读会话记录，报告该对话是否被固定或仍在进行，以及它触及哪些工作树（principle-guard-the-context-window，会话记录体量大）。一个被固定的对话会通过后台子代理把 arena 和复现树派生到兄弟工作树中，即便其名字从未出现在侧边栏，这些树也在使用中。按 Subagents 一节为每项工作选择子代理的推理级别以及快速或标准速度。
4. 遇到不可逆损失先暂停。`wip:N` 是 N 个已跟踪的未提交编辑。先展示差异并取得决策，因为删除干净的工作树可以从其分支恢复，而未提交的工作会永久丢失。`scratch:N` 是未跟踪的一次性内容，可以安全丢弃，但要列出文件。按 Autonomy，干净、已合并且未在使用则继续进行。`wip` 和在使用中则暂停。
5. 清理已确认的集合。逐个路径 `git worktree remove --force <path>`。如果目录因被忽略的构建产物而残留，`rm -rf` 它，然后 `git worktree prune`。分支引用会保留，因此不会丢提交。用 `df -h /` 确认并重新列出。
6. 模拟器与其他可回收项。模拟器通常是下一个最大的收益。`xcrun simctl --set testing delete all`（XCTestDevices 克隆）、`xcrun simctl delete unavailable`，以及 `xcrun simctl runtime list` 然后对旧运行时 `runtime delete <id>`。需要时更多：Xcode 的 `DerivedData` 与 `iOS DeviceSupport`、`~/Library/Application Support/Cursor`（`state.vscdb.backup`，以及 `snapshots/roots/<root>`——当某个以你作为工作区打开过的文件夹命名的 `<root>` 膨胀时），包缓存（pnpm、uv、brew、yarn）。只清理用户未表示要保留的缓存。

这是唯一一个删除用户状态却没有代码评审来把关失误的剧本，因此上面的闸门就是评审。

**回复：** 前后的 `df -h /` 及回收的空间、清理掉的工作树，以及每个被扣下的项用一行理由说明（被哪个对话占用，或存在未提交工作）。
